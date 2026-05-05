"""Claim interval computation for OQCI.

For each binary claim L_Hi (is hypothesis Hi active?):
  I_Hi = [0,1] if both Hi and non-Hi are consistent (unidentifiable)
  I_Hi = [1,1] if only Hi is consistent (data forces claim true)
  I_Hi = [0,0] if no Hi state is consistent (data forces claim false)

For numeric claims (like "total current on layer 3"):
  Sample coefficients within the consistent residual threshold and compute
  min/max of the claim over the consistent set.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from hypotheses import HYPOTHESES, HypothesisBasis
from quotient import ConsistentSetResult, fit_hypothesis
from operators import OperatorBundle


@dataclass
class ClaimInterval:
    claim_name: str
    is_binary: bool
    interval: tuple[float, float]
    width: float
    truth_value: float
    interpretation: str


def binary_claim_interval(
    results: list[ConsistentSetResult],
    claim_hypothesis: str,
    truth_hypothesis: str,
) -> dict:
    """Compute claim interval statistics for a binary topology claim.

    A binary claim is: "Is this hypothesis the true explanation?"

    Returns aggregated stats over all cases with the given truth hypothesis.
    """
    subset = [r for r in results if r.truth_hypothesis == truth_hypothesis]
    if not subset:
        return {"count": 0}

    n = len(subset)
    forced_false = 0
    forced_true = 0
    unidentifiable = 0
    empty_consistent = 0

    for r in subset:
        if len(r.consistent_hypotheses) == 0:
            empty_consistent += 1
        elif claim_hypothesis in r.consistent_hypotheses and len(r.consistent_hypotheses) == 1:
            forced_true += 1
        elif claim_hypothesis not in r.consistent_hypotheses:
            forced_false += 1
        else:
            unidentifiable += 1

    return {
        "claim": claim_hypothesis,
        "truth": truth_hypothesis,
        "count": n,
        "forced_false": forced_false,
        "forced_false_rate": forced_false / n,
        "forced_true": forced_true,
        "forced_true_rate": forced_true / n,
        "unidentifiable": unidentifiable,
        "unidentifiable_rate": unidentifiable / n,
        "empty_consistent": empty_consistent,
        "mean_width": (forced_false * 0.0 + forced_true * 0.0 + unidentifiable * 1.0) / n,
    }


def claim_intervals_matrix(
    results: list[ConsistentSetResult],
) -> dict[str, dict]:
    """Compute the full truth-claim interval matrix.

    Returns a dict keyed by "truth__claim" with interval stats.
    """
    matrix = {}
    for truth_h in HYPOTHESES:
        for claim_h in HYPOTHESES:
            key = f"{truth_h}__{claim_h}"
            matrix[key] = binary_claim_interval(results, claim_h, truth_h)
    return matrix


def numeric_claim_interval(
    consistent_fits: list[np.ndarray],
    claim_fn,
) -> dict:
    """Compute min/max of a numeric claim over consistent coefficient samples.

    consistent_fits: list of coefficient vectors from each consistent hypothesis
    claim_fn: function mapping coefficients -> float

    Returns the claim interval [min_val, max_val] and its width.
    """
    if not consistent_fits:
        return {"min": 0.0, "max": 0.0, "width": 0.0, "n_samples": 0}

    values = [claim_fn(coef) for coef in consistent_fits]
    vals_arr = np.array(values, dtype=float)
    return {
        "min": float(np.min(vals_arr)),
        "max": float(np.max(vals_arr)),
        "width": float(np.max(vals_arr) - np.min(vals_arr)),
        "n_samples": len(values),
    }


def aggregate_claim_intervals(
    results: list[ConsistentSetResult],
) -> dict:
    """Aggregate claim interval statistics across all cases."""
    matrix = claim_intervals_matrix(results)

    total_forced = 0
    total_unidentifiable = 0
    total = 0
    for key, stats in matrix.items():
        if stats["count"] == 0:
            continue
        truth_h, claim_h = key.split("__")
        if truth_h == claim_h:
            total_forced += stats["forced_true"]
            total_unidentifiable += stats["unidentifiable"]
            total += stats["count"]

    return {
        "interval_matrix": matrix,
        "overall_forced_true_rate": total_forced / max(total, 1),
        "overall_unidentifiable_rate": total_unidentifiable / max(total, 1),
        "overall_mean_width": total_unidentifiable / max(total, 1),
    }
