"""Core OQCI algorithm: consistent set construction.

Implements Steps 3-4 of the OQCI design document:

For each hypothesis g in {H0, H1, H2, H3}:
  solve min_z ||y - B_g z||_2^2  (ordinary least squares)
  record: data_residual_g

G_consistent(y) = {g : residual_g <= epsilon}

Epsilon policies: known_noise, sensitivity sweep.
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


def _stable_lstsq(B: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    """Ordinary least squares with jittered Cholesky for stability."""
    k = B.shape[1]
    if k == 0:
        residual = float(np.linalg.norm(y))
        return np.zeros(0), residual

    lhs = B.T @ B
    rhs = B.T @ y

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
        residual = float(np.linalg.norm(y - pred))
        return coef, residual

    tmp = np.linalg.solve(L, rhs)
    coef = np.linalg.solve(L.T, tmp)
    pred = B @ coef
    residual = float(np.linalg.norm(y - pred))
    return coef, residual


def fit_hypothesis(
    y: np.ndarray, hb: HypothesisBasis, epsilon: float,
) -> HypothesisFit:
    """Fit one hypothesis to data using OLS on its forward basis B."""
    coef, residual = _stable_lstsq(hb.B, y)
    pred = hb.B @ coef if hb.B.shape[1] > 0 else np.zeros_like(y)
    y_norm = max(float(np.linalg.norm(y)), 1e-18)
    return HypothesisFit(
        hypothesis=hb.hypothesis,
        residual=residual,
        residual_normalized=residual / y_norm,
        coefficients=coef,
        predicted_field=pred,
        is_consistent=residual <= epsilon,
        effective_dof=hb.B.shape[1],
    )


def consistent_set_for_case(
    case, bundle: OperatorBundle, bases: dict[str, HypothesisBasis],
    epsilon: float,
) -> ConsistentSetResult:
    """Compute the consistent hypothesis set for one case."""
    y = case.field_observed
    fits = {}
    for h in HYPOTHESES:
        fits[h] = fit_hypothesis(y, bases[h], epsilon)

    consistent = [h for h in HYPOTHESES if fits[h].is_consistent]
    non_consistent = [h for h in HYPOTHESES if not fits[h].is_consistent]

    return ConsistentSetResult(
        case_id=case.case_id,
        truth_hypothesis=case.truth_hypothesis,
        fits=fits,
        epsilon=epsilon,
        consistent_hypotheses=consistent,
        non_consistent_hypotheses=non_consistent,
        epsilon_mode="known_noise",
        epsilon_meta={"epsilon": epsilon},
    )


def compute_epsilon_from_policy(sigma: float, obs_dim: int, policy: dict) -> list[float]:
    """Compute epsilon values from policy. Returns list for sensitivity mode."""
    if policy["mode"] == "known_noise":
        c = float(policy.get("c", 1.5))
        return [float(c * sigma * math.sqrt(obs_dim))]
    if policy["mode"] == "sensitivity":
        multipliers = [float(m) for m in policy["multipliers"]]
        return [float(m * sigma * math.sqrt(obs_dim)) for m in multipliers]
    raise ValueError(f"Unknown epsilon mode: {policy['mode']}")


def run_consistent_set_analysis(
    cases: list, bundle: OperatorBundle, bases: dict[str, HypothesisBasis],
    cfg: dict,
) -> dict:
    """Run consistent set analysis across all cases and epsilon values."""
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

    # Use the primary epsilon (first in list) for aggregate metrics
    primary_idx = 0
    primary_results = all_results[primary_idx]
    primary_eps = eps_values[primary_idx]

    n = len(primary_results)
    nonempty_count = sum(1 for r in primary_results if len(r.consistent_hypotheses) > 0)
    ambiguous_count = sum(1 for r in primary_results if len(r.consistent_hypotheses) > 1)
    multi_count = sum(1 for r in primary_results if len(r.consistent_hypotheses) >= 2)

    # Claim interval computation
    truth_intervals = {}
    for truth_h in HYPOTHESES:
        subset = [r for r in primary_results if r.truth_hypothesis == truth_h]
        if not subset:
            continue
        for claim_h in HYPOTHESES:
            key = f"{truth_h}__{claim_h}"
            forced_false = sum(1 for r in subset if claim_h in r.non_consistent_hypotheses)
            forced_true = sum(1 for r in subset if claim_h in r.consistent_hypotheses and
                            all(x == claim_h for x in r.consistent_hypotheses))
            unidentifiable = sum(1 for r in subset if claim_h in r.consistent_hypotheses and
                                len(r.consistent_hypotheses) > 1)

            claim_target = 1.0 if claim_h == truth_h else 0.0
            truth_intervals[key] = {
                "truth": truth_h,
                "claim": claim_h,
                "target": claim_target,
                "forced_false": forced_false,
                "forced_true": forced_true,
                "unidentifiable": unidentifiable,
                "count": len(subset),
            }

    mean_interval_width = 0.0
    interval_count = 0
    by_truth_width = {}
    for truth_h in HYPOTHESES:
        subset = [r for r in primary_results if r.truth_hypothesis == truth_h]
        width_sum = 0.0
        for r in subset:
            for claim_h in HYPOTHESES:
                if claim_h in r.consistent_hypotheses and len(r.consistent_hypotheses) > 1:
                    width_sum += 1.0  # wide interval
                    interval_count += 1
                else:
                    width_sum += 0.0  # narrow interval
                    interval_count += 1
        by_truth_width[truth_h] = width_sum / max(len(subset) * len(HYPOTHESES), 1)
        mean_interval_width += width_sum
    mean_interval_width /= max(interval_count, 1)

    # Decision: accept if single consistent hypothesis matches truth need more data
    decisions = []
    for r in primary_results:
        if len(r.consistent_hypotheses) == 1:
            decisions.append("single_consistent")
        elif len(r.consistent_hypotheses) > 1:
            decisions.append("ambiguous")
        elif len(r.consistent_hypotheses) == 0:
            decisions.append("empty_consistent_set")
        else:
            decisions.append("unknown")

    # Sensitivity: how does consistent set change with epsilon?
    sensitivity_by_case = []
    for i in range(n):
        row = {"case_id": primary_results[i].case_id}
        for j, eps in enumerate(eps_values):
            row[f"eps_{eps:.4f}"] = all_results[j][i].consistent_hypotheses
        sensitivity_by_case.append(row)

    return {
        "case_count": n,
        "epsilon_primary": primary_eps,
        "epsilon_values": eps_values,
        "consistent_set_nonempty_rate": nonempty_count / max(n, 1),
        "ambiguity_rate": ambiguous_count / max(n, 1),
        "multi_consistent_rate": multi_count / max(n, 1),
        "mean_interval_width": mean_interval_width,
        "by_truth_width": by_truth_width,
        "claim_intervals": truth_intervals,
        "decision_distribution": {
            dt: sum(1 for d in decisions if d == dt) for dt in sorted(set(decisions))
        },
        "sensitivity_by_case": sensitivity_by_case,
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
            per_fit[h] = {
                "mean": float(np.mean(resids)),
                "median": float(np.median(resids)),
            }
        out[truth_h] = per_fit
    return out
