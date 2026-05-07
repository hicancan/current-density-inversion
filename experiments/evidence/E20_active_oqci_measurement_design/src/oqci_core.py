"""Core OQCI algorithm: consistent set construction with regularized fitting.

Adapted from E19.2 quotient.py. Round 4 adds:
- ridge_regularized hypothesis fitting
- reduced_basis_ridge fitting with compact physically-motivated bases
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

from hypotheses import HYPOTHESES, HypothesisBasis
from operators import OperatorBundle


@dataclass
class HypothesisFit:
    hypothesis: str
    residual: float
    residual_normalized: float
    coefficients: np.ndarray
    predicted_field: np.ndarray
    is_consistent: bool
    effective_dof: int
    fit_mode: str = "ols"
    lambda_reg: float = 0.0


@dataclass
class ConsistentSetResult:
    case_id: str
    truth_hypothesis: str
    fits: dict[str, HypothesisFit]
    epsilon: float
    consistent_hypotheses: list[str]
    non_consistent_hypotheses: list[str]
    epsilon_mode: str
    epsilon_meta: dict


# ── reduced basis column indices ──────────────────────────────────────────

def _reduced_basis_mask(hb: HypothesisBasis, hypothesis: str) -> np.ndarray:
    """Select compact physically-motivated columns per hypothesis."""
    k = hb.B.shape[1]
    mask = np.zeros(k, dtype=bool)
    for i, meta in enumerate(hb.column_metadata):
        kind = meta.get("block_kind", "")
        name = meta.get("block_name", "")
        if hypothesis == "H0_no_via":
            if kind in ("graph", "residual"):
                mask[i] = True
        elif hypothesis == "H1_via":
            if kind in ("graph", "residual", "via_vertical", "via_compensation"):
                mask[i] = True
        elif hypothesis == "H2_model_gap":
            if kind in ("graph", "residual", "gap_registration", "gap_standoff"):
                mask[i] = True
        elif hypothesis == "H3_return_path":
            if kind in ("graph", "residual", "return_loop", "return_edge"):
                mask[i] = True
    # Fallback: if nothing selected, use all
    if not np.any(mask):
        mask[:] = True
    return mask


# ── stable least squares ─────────────────────────────────────────────────

def _stable_lstsq(B: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    k = B.shape[1]
    if k == 0:
        return np.zeros(0), float(np.linalg.norm(y))
    lhs = B.T @ B; rhs = B.T @ y
    jitter = 1e-12
    for _ in range(6):
        try:
            L = np.linalg.cholesky(lhs + jitter * np.eye(k))
            break
        except np.linalg.LinAlgError:
            jitter *= 10.0
    else:
        coef = np.linalg.lstsq(B, y, rcond=None)[0]
        pred = B @ coef
        return coef, float(np.linalg.norm(y - pred))
    tmp = np.linalg.solve(L, rhs)
    coef = np.linalg.solve(L.T, tmp)
    pred = B @ coef
    return coef, float(np.linalg.norm(y - pred))


def _ridge_fit(B: np.ndarray, y: np.ndarray, lambda_reg: float) -> tuple[np.ndarray, float, int]:
    """Ridge regression: (B^T B + lambda I)^{-1} B^T y."""
    k = B.shape[1]
    if k == 0:
        return np.zeros(0), float(np.linalg.norm(y)), 0
    lhs = B.T @ B + lambda_reg * np.eye(k)
    rhs = B.T @ y
    try:
        L = np.linalg.cholesky(lhs)
        tmp = np.linalg.solve(L, rhs)
        coef = np.linalg.solve(L.T, tmp)
    except np.linalg.LinAlgError:
        coef = np.linalg.lstsq(B, y, rcond=None)[0]
    pred = B @ coef
    residual = float(np.linalg.norm(y - pred))
    # Effective degrees of freedom (Hastie-Tibshirani)
    try:
        S = np.linalg.svd(B, compute_uv=False)
        s2 = S ** 2
        eff_dof = int(np.sum(s2 / (s2 + lambda_reg)))
    except Exception:
        eff_dof = k
    return coef, residual, eff_dof


# ── regularized hypothesis fitting ───────────────────────────────────────

def fit_hypothesis(
    y: np.ndarray, hb: HypothesisBasis, epsilon: float,
) -> HypothesisFit:
    """OLS baseline fit."""
    coef, residual = _stable_lstsq(hb.B, y)
    pred = hb.B @ coef if hb.B.shape[1] > 0 else np.zeros_like(y)
    y_norm = max(float(np.linalg.norm(y)), 1e-18)
    return HypothesisFit(
        hypothesis=hb.hypothesis, residual=residual,
        residual_normalized=residual / y_norm, coefficients=coef,
        predicted_field=pred, is_consistent=residual <= epsilon,
        effective_dof=hb.B.shape[1], fit_mode="ols", lambda_reg=0.0,
    )


def fit_hypothesis_ridge(
    y: np.ndarray, hb: HypothesisBasis, epsilon: float, lambda_reg: float,
) -> HypothesisFit:
    """Ridge-regularized fit with effective degrees of freedom."""
    coef, residual, eff_dof = _ridge_fit(hb.B, y, lambda_reg)
    pred = hb.B @ coef if hb.B.shape[1] > 0 else np.zeros_like(y)
    y_norm = max(float(np.linalg.norm(y)), 1e-18)
    return HypothesisFit(
        hypothesis=hb.hypothesis, residual=residual,
        residual_normalized=residual / y_norm, coefficients=coef,
        predicted_field=pred, is_consistent=residual <= epsilon,
        effective_dof=eff_dof, fit_mode="ridge", lambda_reg=lambda_reg,
    )


def fit_hypothesis_reduced_ridge(
    y: np.ndarray, hb: HypothesisBasis, epsilon: float, lambda_reg: float,
) -> HypothesisFit:
    """Reduced-basis ridge fit: select compact basis per hypothesis, then ridge."""
    mask = _reduced_basis_mask(hb, hb.hypothesis)
    B_reduced = hb.B[:, mask]
    coef_full = np.zeros(hb.B.shape[1])
    if B_reduced.shape[1] == 0:
        pred = np.zeros_like(y)
        residual = float(np.linalg.norm(y))
        eff_dof = 0
    else:
        coef_r, residual, eff_dof = _ridge_fit(B_reduced, y, lambda_reg)
        coef_full[mask] = coef_r
        pred = B_reduced @ coef_r
    y_norm = max(float(np.linalg.norm(y)), 1e-18)
    return HypothesisFit(
        hypothesis=hb.hypothesis, residual=residual,
        residual_normalized=residual / y_norm, coefficients=coef_full,
        predicted_field=pred, is_consistent=residual <= epsilon,
        effective_dof=eff_dof, fit_mode="reduced_ridge", lambda_reg=lambda_reg,
    )


FIT_MODES = {
    "ols": fit_hypothesis,
    "ridge": fit_hypothesis_ridge,
    "reduced_ridge": fit_hypothesis_reduced_ridge,
}


def fit_all_hypotheses(
    y: np.ndarray, bases: dict[str, HypothesisBasis], epsilon: float,
    fit_mode: str = "ols", lambda_reg: float = 0.0,
) -> dict[str, HypothesisFit]:
    """Fit all hypotheses with a given fitting mode."""
    fn = FIT_MODES.get(fit_mode, fit_hypothesis)
    if fit_mode in ("ridge", "reduced_ridge"):
        return {h: fn(y, bases[h], epsilon, lambda_reg) for h in HYPOTHESES}
    return {h: fn(y, bases[h], epsilon) for h in HYPOTHESES}


def consistent_set_for_case(
    case, bundle: OperatorBundle, bases: dict[str, HypothesisBasis],
    epsilon: float, fit_mode: str = "ols", lambda_reg: float = 0.0,
) -> ConsistentSetResult:
    y = case.field_observed
    fits = fit_all_hypotheses(y, bases, epsilon, fit_mode, lambda_reg)
    consistent = [h for h in HYPOTHESES if fits[h].is_consistent]
    non_consistent = [h for h in HYPOTHESES if not fits[h].is_consistent]
    return ConsistentSetResult(
        case_id=case.case_id, truth_hypothesis=case.truth_hypothesis,
        fits=fits, epsilon=epsilon,
        consistent_hypotheses=consistent,
        non_consistent_hypotheses=non_consistent,
        epsilon_mode="known_noise",
        epsilon_meta={"epsilon": epsilon, "fit_mode": fit_mode, "lambda_reg": lambda_reg},
    )


def compute_epsilon_from_policy(sigma: float, obs_dim: int, policy: dict) -> list[float]:
    if policy["mode"] == "known_noise":
        c = float(policy.get("c", 1.5))
        return [float(c * sigma * math.sqrt(obs_dim))]
    if policy["mode"] == "sensitivity":
        multipliers = [float(m) for m in policy["multipliers"]]
        return [float(m * sigma * math.sqrt(obs_dim)) for m in multipliers]
    raise ValueError(f"Unknown epsilon mode: {policy['mode']}")


def compute_epsilon_from_quantile(fitted_residuals: np.ndarray, quantile: float) -> float:
    """Compute epsilon as a quantile of truth residual distribution."""
    if fitted_residuals.size == 0:
        return 1e-6
    return float(np.quantile(fitted_residuals, quantile))


def run_consistent_set_analysis(
    cases: list, bundle: OperatorBundle, bases: dict[str, HypothesisBasis],
    cfg: dict,
) -> dict:
    sigma = float(cfg["noise_sigma"])
    obs_dim = bundle.A.shape[0]
    policy = cfg["epsilon_policy"]
    eps_values = compute_epsilon_from_policy(sigma, obs_dim, policy)

    all_results: list[list[ConsistentSetResult]] = []
    for epsilon in eps_values:
        case_results = []
        for case in cases:
            case_results.append(consistent_set_for_case(case, bundle, bases, epsilon))
        all_results.append(case_results)

    primary_idx = 0; primary_results = all_results[primary_idx]; primary_eps = eps_values[primary_idx]
    n = len(primary_results)
    nonempty_count = sum(1 for r in primary_results if len(r.consistent_hypotheses) > 0)
    ambiguous_count = sum(1 for r in primary_results if len(r.consistent_hypotheses) > 1)
    multi_count = sum(1 for r in primary_results if len(r.consistent_hypotheses) >= 2)

    truth_intervals = {}
    for truth_h in HYPOTHESES:
        subset = [r for r in primary_results if r.truth_hypothesis == truth_h]
        if not subset: continue
        for claim_h in HYPOTHESES:
            key = f"{truth_h}__{claim_h}"
            forced_false = sum(1 for r in subset if claim_h in r.non_consistent_hypotheses)
            forced_true = sum(1 for r in subset if claim_h in r.consistent_hypotheses and
                            all(x == claim_h for x in r.consistent_hypotheses))
            unidentifiable = sum(1 for r in subset if claim_h in r.consistent_hypotheses and
                                len(r.consistent_hypotheses) > 1)
            truth_intervals[key] = {"truth": truth_h, "claim": claim_h,
                "target": 1.0 if claim_h == truth_h else 0.0,
                "forced_false": forced_false, "forced_true": forced_true,
                "unidentifiable": unidentifiable, "count": len(subset)}

    mean_interval_width = 0.0; interval_count = 0
    by_truth_width = {}
    for truth_h in HYPOTHESES:
        subset = [r for r in primary_results if r.truth_hypothesis == truth_h]
        width_sum = 0.0
        for r in subset:
            for claim_h in HYPOTHESES:
                if claim_h in r.consistent_hypotheses and len(r.consistent_hypotheses) > 1:
                    width_sum += 1.0; interval_count += 1
                else:
                    interval_count += 1
        by_truth_width[truth_h] = width_sum / max(len(subset) * len(HYPOTHESES), 1)
        mean_interval_width += width_sum
    mean_interval_width /= max(interval_count, 1)

    decisions = []
    for r in primary_results:
        if len(r.consistent_hypotheses) == 1: decisions.append("single_consistent")
        elif len(r.consistent_hypotheses) > 1: decisions.append("ambiguous")
        elif len(r.consistent_hypotheses) == 0: decisions.append("empty_consistent_set")
        else: decisions.append("unknown")

    wrong_accept_count = 0
    for r in primary_results:
        if len(r.consistent_hypotheses) == 1 and r.consistent_hypotheses[0] != r.truth_hypothesis:
            wrong_accept_count += 1

    return {
        "case_count": n, "epsilon_primary": primary_eps, "epsilon_values": eps_values,
        "consistent_set_nonempty_rate": nonempty_count / max(n, 1),
        "ambiguity_rate": ambiguous_count / max(n, 1),
        "multi_consistent_rate": multi_count / max(n, 1),
        "mean_interval_width": mean_interval_width, "by_truth_width": by_truth_width,
        "claim_intervals": truth_intervals,
        "decision_distribution": {dt: sum(1 for d in decisions if d == dt) for dt in sorted(set(decisions))},
        "wrong_high_confidence_accept_count": wrong_accept_count,
        "residuals_by_truth": _compute_residuals_by_truth(primary_results),
    }


def _compute_residuals_by_truth(results: list[ConsistentSetResult]) -> dict:
    out = {}
    for truth_h in HYPOTHESES:
        subset = [r for r in results if r.truth_hypothesis == truth_h]
        if not subset:
            continue
        per_fit = {}
        for h in HYPOTHESES:
            resids = [r.fits[h].residual for r in subset]
            per_fit[h] = {"mean": float(np.mean(resids)), "median": float(np.median(resids))}
        out[truth_h] = per_fit
    return out
