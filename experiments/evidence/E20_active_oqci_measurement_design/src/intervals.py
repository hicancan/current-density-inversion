"""Claim interval computation for OQCI.

Copied from E19.2 intervals.py.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from hypotheses import HYPOTHESES
from oqci_core import ConsistentSetResult


def binary_claim_interval(
    results: list[ConsistentSetResult],
    claim_hypothesis: str,
    truth_hypothesis: str,
) -> dict:
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


def claim_intervals_matrix(results: list[ConsistentSetResult]) -> dict[str, dict]:
    matrix = {}
    for truth_h in HYPOTHESES:
        for claim_h in HYPOTHESES:
            key = f"{truth_h}__{claim_h}"
            matrix[key] = binary_claim_interval(results, claim_h, truth_h)
    return matrix


def aggregate_claim_intervals(results: list[ConsistentSetResult]) -> dict:
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
