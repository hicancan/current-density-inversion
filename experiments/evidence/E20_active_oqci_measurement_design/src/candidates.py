"""Candidate measurement pool for E20 Active OQCI with regularization and calibration (round 4)."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from operators import (
    OperatorBundle, build_candidate_operator, multi_height_operator_stack,
    build_multi_state_operator, operator_diagnostics,
)
from hypotheses import build_all_hypothesis_bases, HYPOTHESES
from oqci_core import (
    run_consistent_set_analysis, consistent_set_for_case, compute_epsilon_from_policy,
    fit_hypothesis, fit_hypothesis_ridge, fit_hypothesis_reduced_ridge,
    compute_epsilon_from_quantile, _reduced_basis_mask,
)
from distances import pairwise_distinguishability
from nullspace import near_null_modes
from intervals import aggregate_claim_intervals
from pairwise_margin import compute_pairwise_margins


LAMBDA_GRID = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]
CALIBRATION_FRAC = 0.5  # half for calibration, half for evaluation


@dataclass
class CandidateMeasurement:
    candidate_id: str
    height_um: float
    components: list[str]
    description: str
    cost: float = 1.0
    n_states: int = 1


def build_candidate_pool(cfg: dict) -> list[CandidateMeasurement]:
    pool = []
    for entry in cfg["candidate_pool"]:
        pool.append(CandidateMeasurement(
            candidate_id=entry["id"], height_um=float(entry["height_um"]),
            components=entry["components"],
            description=entry.get("description", entry["id"]),
            cost=float(entry.get("cost", 1.0)),
            n_states=int(entry.get("n_states", 1)),
        ))
    return pool


def _split_cases(cases: list, calib_frac: float = CALIBRATION_FRAC) -> tuple[list, list]:
    """Deterministic split by case index: first frac for calibration, rest for eval."""
    n = len(cases)
    n_calib = max(1, int(n * calib_frac))
    return cases[:n_calib], cases[n_calib:]


def _coverage_metrics(cases, bundle, bases, eps_val, fit_mode="ols", lambda_reg=0.0):
    """Compute truth coverage metrics for a given epsilon and fit config."""
    n = len(cases)
    if n == 0:
        return {"n_cases": 0, "empty_rate": 0.0, "valid_disambiguation_rate": 0.0}

    results = [consistent_set_for_case(c, bundle, bases, eps_val, fit_mode, lambda_reg) for c in cases]

    empty_count = 0; singleton_correct = 0; singleton_wrong = 0
    multi_count = 0; truth_in_set_count = 0; truth_missing_count = 0
    per_case = []; set_sizes = []

    for i, r in enumerate(results):
        truth = r.truth_hypothesis; cs = r.consistent_hypotheses
        cs_size = len(cs); set_sizes.append(cs_size)
        if cs_size == 0:
            case_type = "empty"; empty_count += 1; truth_in_set = False
        elif cs_size == 1:
            if cs[0] == truth:
                case_type = "singleton_correct"; singleton_correct += 1
            else:
                case_type = "singleton_wrong"; singleton_wrong += 1
            truth_in_set = (cs[0] == truth)
        else:
            case_type = "multi"; multi_count += 1
            truth_in_set = (truth in cs)
        if truth_in_set: truth_in_set_count += 1
        else: truth_missing_count += 1
        per_case.append({"case_id": r.case_id, "truth": truth,
            "consistent_hypotheses": cs, "size": cs_size,
            "type": case_type, "truth_in_set": truth_in_set})

    singleton_count = singleton_correct + singleton_wrong
    valid_disambig = singleton_correct
    return {
        "n_cases": n, "empty_count": empty_count,
        "singleton_correct": singleton_correct, "singleton_wrong": singleton_wrong,
        "singleton_count": singleton_count, "multi_count": multi_count,
        "truth_in_set_count": truth_in_set_count, "truth_missing_count": truth_missing_count,
        "valid_disambiguation_count": valid_disambig,
        "empty_rate": empty_count / max(n, 1),
        "nonempty_rate": (n - empty_count) / max(n, 1),
        "singleton_rate": singleton_count / max(n, 1),
        "singleton_correct_rate": singleton_correct / max(n, 1),
        "singleton_wrong_rate": singleton_wrong / max(n, 1),
        "truth_in_consistent_set_rate": truth_in_set_count / max(n, 1),
        "truth_missing_rate": truth_missing_count / max(n, 1),
        "multi_consistent_rate": multi_count / max(n, 1),
        "mean_consistent_set_size": float(np.mean(set_sizes)) if set_sizes else 0.0,
        "accepted_accuracy": singleton_correct / max(singleton_count, 1),
        "accepted_risk": singleton_wrong / max(singleton_count, 1),
        "valid_disambiguation_rate": valid_disambig / max(n, 1),
        "valid_disambiguation_count": valid_disambig,
        "per_case": per_case,
    }


def _regularized_sweep(cases, bundle, bases, sigma, obs_dim, eps_mult):
    """Run regularized fitting sweep across fit modes and lambda values.

    Returns dict with best per-mode metrics and residuals for calibration.
    """
    eps_val = float(eps_mult * sigma * np.sqrt(obs_dim))
    n = len(cases)
    if n == 0:
        return {"fit_mode_results": {}, "truth_residuals_for_calibration": np.array([])}

    modes = {}
    truth_residuals_all = {}

    # OLS baseline
    cov_ols = _coverage_metrics(cases, bundle, bases, eps_val, "ols", 0.0)
    truth_resids_ols = []
    for h in HYPOTHESES:
        for c in cases:
            r = consistent_set_for_case(c, bundle, bases, eps_val, "ols", 0.0)
            if c.truth_hypothesis == h:
                truth_resids_ols.append(r.fits[h].residual)
    modes["ols"] = {**cov_ols, "lambda": 0.0, "fit_mode": "ols",
                     "truth_residuals": np.array(truth_resids_ols)}

    # Ridge sweep
    best_ridge = None; best_ridge_vdr = -1.0
    for lam in LAMBDA_GRID:
        cov = _coverage_metrics(cases, bundle, bases, eps_val, "ridge", lam)
        truth_resids = []
        for c in cases:
            r = consistent_set_for_case(c, bundle, bases, eps_val, "ridge", lam)
            truth_resids.append(r.fits[c.truth_hypothesis].residual)
        cov["truth_residuals"] = np.array(truth_resids)
        cov["lambda"] = lam; cov["fit_mode"] = "ridge"
        key = f"ridge_{lam:.0e}"
        modes[key] = cov
        vdr = cov["valid_disambiguation_rate"]
        if vdr > best_ridge_vdr or (vdr == best_ridge_vdr and best_ridge and lam < best_ridge["lambda"]):
            best_ridge_vdr = vdr; best_ridge = cov
    if best_ridge:
        modes["ridge_best"] = best_ridge

    # Reduced-basis ridge sweep
    best_rr = None; best_rr_vdr = -1.0
    for lam in LAMBDA_GRID:
        cov = _coverage_metrics(cases, bundle, bases, eps_val, "reduced_ridge", lam)
        truth_resids = []
        for c in cases:
            r = consistent_set_for_case(c, bundle, bases, eps_val, "reduced_ridge", lam)
            truth_resids.append(r.fits[c.truth_hypothesis].residual)
        cov["truth_residuals"] = np.array(truth_resids)
        cov["lambda"] = lam; cov["fit_mode"] = "reduced_ridge"
        key = f"reduced_ridge_{lam:.0e}"
        modes[key] = cov
        vdr = cov["valid_disambiguation_rate"]
        if vdr > best_rr_vdr:
            best_rr_vdr = vdr; best_rr = cov
    if best_rr:
        modes["reduced_ridge_best"] = best_rr

    # OLS truth residuals for calibration
    ols_resids = modes.get("ols", {}).get("truth_residuals", np.array([]))

    return {
        "epsilon_multiplier": eps_mult,
        "epsilon": eps_val,
        "fit_mode_results": modes,
        "ols_truth_residuals": ols_resids,
    }


def _run_calibrated_evaluation(
    calib_cases, eval_cases, bundle, bases, sigma, obs_dim, eps_mult, best_fit_mode,
    best_lambda, quantiles=[0.90, 0.95, 0.99],
):
    """Calibrate epsilon from truth residuals on calibration set, evaluate on eval set."""
    n_calib = len(calib_cases); n_eval = len(eval_cases)
    if n_calib == 0 or n_eval == 0:
        return {"calibration": {}, "evaluation": {}}

    # Fit truth hypothesis on calibration set with best mode
    calib_resids = []
    for c in calib_cases:
        r = consistent_set_for_case(c, bundle, bases, 1e9, best_fit_mode, best_lambda)
        calib_resids.append(r.fits[c.truth_hypothesis].residual)
    calib_resids_arr = np.array(calib_resids)

    calib_result = {
        "n_cases": n_calib,
        "fit_mode": best_fit_mode,
        "lambda": best_lambda,
        "truth_residual_mean": float(np.mean(calib_resids_arr)),
        "truth_residual_median": float(np.median(calib_resids_arr)),
    }
    eval_results = {}

    for q in quantiles:
        eps_q = compute_epsilon_from_quantile(calib_resids_arr, q)
        calib_cov = _coverage_metrics(calib_cases, bundle, bases, eps_q, best_fit_mode, best_lambda)
        eval_cov = _coverage_metrics(eval_cases, bundle, bases, eps_q, best_fit_mode, best_lambda)

        calib_result[f"epsilon_q{q:.2f}"] = float(eps_q)
        calib_result[f"coverage_q{q:.2f}"] = calib_cov

        eval_results[f"q{q:.2f}"] = {
            "epsilon": float(eps_q),
            "quantile": q,
            **eval_cov,
        }

    return {
        "calibration": calib_result,
        "evaluation": eval_results,
        "calibration_case_count": n_calib,
        "evaluation_case_count": n_eval,
    }


def evaluate_candidate(
    cfg: dict,
    baseline_case_results: list,
    baseline_heights: list[float],
    baseline_oqci: dict,
    baseline_nullspace: dict,
    baseline_pairwise: dict,
    candidate: CandidateMeasurement,
) -> dict:
    import data_adapter

    n_states = candidate.n_states

    if candidate.height_um <= 0.01:
        bundle_ss = multi_height_operator_stack(cfg)
    else:
        bundle_ss = build_candidate_operator(
            cfg, baseline_heights, candidate.height_um, candidate.components,
        )
    if n_states > 1:
        bundle = build_multi_state_operator(bundle_ss, n_states)
    else:
        bundle = bundle_ss

    op_diag = operator_diagnostics(bundle)
    bases = build_all_hypothesis_bases(bundle, cfg)

    if n_states > 1:
        cases = data_adapter.generate_multi_state_cases(bundle, cfg, n_states)
    else:
        cases = data_adapter.generate_cases(bundle, cfg)

    sigma = float(cfg["noise_sigma"])
    obs_dim = bundle.A.shape[0]
    eps_values = compute_epsilon_from_policy(sigma, obs_dim, cfg["epsilon_policy"])
    primary_eps = eps_values[0] if eps_values else 0.0

    # Primary OQCI (OLS only, for backward compat)
    oqci_primary = run_consistent_set_analysis(cases, bundle, bases, cfg)
    per_case = []
    for case in cases:
        r = consistent_set_for_case(case, bundle, bases, primary_eps)
        per_case.append({"case_id": r.case_id, "truth": r.truth_hypothesis,
            "consistent_hypotheses": r.consistent_hypotheses,
            "non_consistent_hypotheses": r.non_consistent_hypotheses})
    oqci_primary["per_case"] = per_case

    # Epsilon sweep with truth coverage (OLS baseline)
    eps_multipliers = cfg.get("epsilon_multipliers", [2.5])
    eps_sweep_results = []
    for eps_mult in eps_multipliers:
        eps_val = float(eps_mult * sigma * np.sqrt(obs_dim))
        cov = _coverage_metrics(cases, bundle, bases, eps_val, "ols", 0.0)
        intervals = aggregate_claim_intervals(
            [consistent_set_for_case(c, bundle, bases, eps_val, "ols", 0.0) for c in cases]
        )
        cov["epsilon"] = float(eps_val)
        cov["epsilon_multiplier"] = eps_mult
        cov["mean_interval_width"] = intervals.get("overall_mean_width", 0.0)
        cov["intervals"] = intervals
        cov["ambiguity_rate"] = cov["multi_consistent_rate"]
        cov["wrong_accept_count"] = cov["singleton_wrong"]
        eps_sweep_results.append(cov)

    # Regularized sweep
    calib_cases, eval_cases = _split_cases(cases)
    # Use eps_mult=1.0 for regularization sweep (moderate stringency)
    reg_eps_mult = 1.0
    reg_results = _regularized_sweep(cases, bundle, bases, sigma, obs_dim, reg_eps_mult)

    # Best regularized mode
    best_ridge = reg_results["fit_mode_results"].get("ridge_best", {})
    best_rr = reg_results["fit_mode_results"].get("reduced_ridge_best", {})
    ols_result = reg_results["fit_mode_results"].get("ols", {})
    ols_vdr = ols_result.get("valid_disambiguation_rate", 0.0)
    ridge_vdr = best_ridge.get("valid_disambiguation_rate", 0.0)
    rr_vdr = best_rr.get("valid_disambiguation_rate", 0.0)

    # Determine if regularization beats OLS
    best_reg_vdr = max(ridge_vdr, rr_vdr)
    best_reg_mode = "ridge" if ridge_vdr >= rr_vdr else "reduced_ridge"
    best_reg_lambda = best_ridge.get("lambda", 0.01) if best_reg_mode == "ridge" else best_rr.get("lambda", 0.01)
    reg_beats_ols = (best_reg_vdr > ols_vdr + 0.05)

    # Calibrated evaluation with best regularized mode
    calib_eval = _run_calibrated_evaluation(
        calib_cases, eval_cases, bundle, bases, sigma, obs_dim, reg_eps_mult,
        best_reg_mode, best_reg_lambda,
    )

    # Normal metrics
    nullspace_primary = near_null_modes(bundle, bases, float(cfg["nullspace_threshold"]))
    pairwise_primary = pairwise_distinguishability(bases, bundle, cases)
    oqci_primary["near_null_count"] = nullspace_primary["near_null_count"]
    oqci_primary["effective_rank"] = nullspace_primary["effective_rank"]

    all_results = [consistent_set_for_case(case, bundle, bases, primary_eps) for case in cases]
    intervals = aggregate_claim_intervals(all_results)

    # Pairwise margin: compute for this candidate's bases/bundle
    sigma_pm = float(cfg["noise_sigma"])
    eps_pm = sigma_pm * np.sqrt(obs_dim) if obs_dim > 0 else 1.0
    candidate_margins = compute_pairwise_margins(bases, bundle, eps_pm)

    return {
        "candidate_id": candidate.candidate_id,
        "height_um": candidate.height_um, "components": candidate.components,
        "n_states": n_states, "cost": candidate.cost, "obs_dim": obs_dim,
        "operator_diagnostics": op_diag, "oqci": oqci_primary,
        "nullspace": nullspace_primary, "pairwise": pairwise_primary,
        "intervals": intervals, "epsilon_sweep": eps_sweep_results,
        "pairwise_margin": candidate_margins,
        # Regularized results
        "regularized_sweep": reg_results,
        "best_regularized_vdr": best_reg_vdr,
        "best_regularized_fit_mode": best_reg_mode,
        "best_regularized_lambda": best_reg_lambda,
        "regularization_beats_ols": reg_beats_ols,
        "ols_vdr": ols_vdr, "ridge_vdr": ridge_vdr, "reduced_ridge_vdr": rr_vdr,
        "calibrated_evaluation": calib_eval,
    }
