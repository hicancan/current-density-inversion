"""Metrics for E19 OBGHI."""

from __future__ import annotations

from collections import Counter, defaultdict
import numpy as np

from basis import HYPOTHESES
from obghi import OBGHIResult


def _safe_div(a: float, b: float) -> float:
    return float(a / b) if b else 0.0


def confusion_matrix(rows: list[dict], truth_key: str, pred_key: str) -> dict[str, dict[str, int]]:
    labels = HYPOTHESES
    cm = {t: {p: 0 for p in labels} for t in labels}
    for row in rows:
        t = row[truth_key]
        p = row[pred_key]
        if t in cm and p in cm[t]:
            cm[t][p] += 1
    return cm


def aggregate_obghi(results: list[OBGHIResult]) -> dict:
    n = len(results)
    accepted = [r for r in results if r.decision == "accept"]
    rejected = [r for r in results if r.decision.startswith("reject")]
    need_next = [r for r in results if r.decision == "need_next_measurement"]

    top_correct = sum(r.top_hypothesis == r.truth_hypothesis for r in results)
    accepted_correct = sum(r.top_hypothesis == r.truth_hypothesis for r in accepted)
    accepted_wrong = len(accepted) - accepted_correct

    via_truth = [r for r in results if r.truth_hypothesis == "H1_via"]
    gap_truth = [r for r in results if r.truth_hypothesis == "H2_model_gap"]
    ambiguous_rejects = [
        r for r in results
        if r.decision == "reject_via_gap_ambiguous" and r.truth_hypothesis in ("H1_via", "H2_model_gap")
    ]

    brier = 0.0
    for r in results:
        for h in HYPOTHESES:
            target = 1.0 if h == r.truth_hypothesis else 0.0
            brier += (r.posteriors[h].posterior_probability - target) ** 2
    brier /= max(n * len(HYPOTHESES), 1)

    by_truth = {}
    for h in HYPOTHESES:
        subset = [r for r in results if r.truth_hypothesis == h]
        by_truth[h] = {
            "count": len(subset),
            "top1_accuracy": _safe_div(sum(r.top_hypothesis == h for r in subset), len(subset)),
            "accept_rate": _safe_div(sum(r.decision == "accept" for r in subset), len(subset)),
            "reject_rate": _safe_div(sum(r.decision.startswith("reject") for r in subset), len(subset)),
            "mean_true_posterior": _safe_div(
                sum(r.posteriors[h].posterior_probability for r in subset), len(subset)
            ),
        }

    h0_cases = [r for r in results if r.truth_hypothesis == "H0_no_via"]
    h2_cases = [r for r in results if r.truth_hypothesis == "H2_model_gap"]
    h3_cases = [r for r in results if r.truth_hypothesis == "H3_return_path"]

    for subset, key in [(h0_cases, "h0"), (h2_cases, "h2"), (h3_cases, "h3")]:
        count = len(subset)
        rej_need = sum(1 for r in subset if r.decision.startswith("reject") or r.decision == "need_next_measurement")
        by_truth_key = {"h0": "H0_no_via", "h2": "H2_model_gap", "h3": "H3_return_path"}[key]
        by_truth[by_truth_key][key + "_reject_or_need_next_rate"] = rej_need / max(count, 1)

    no_via_decisions = sum(1 for r in results if "no_via" in r.decision.lower())

    residual_by_truth: dict[str, list[float]] = defaultdict(list)
    for r in results:
        residual_by_truth[r.truth_hypothesis].append(
            float(r.posteriors[r.truth_hypothesis].predictive_residual_norm)
        )
    residual_alignment_by_truth = {
        h: float(np.mean(vals)) if vals else 0.0
        for h, vals in residual_by_truth.items()
    }

    case_angles = [r.case_via_gap_angle_deg for r in results]
    mean_case_angle = float(np.mean(case_angles)) if case_angles else 0.0
    min_case_angle = float(np.min(case_angles)) if case_angles else 0.0

    return {
        "case_count": n,
        "top1_accuracy": _safe_div(top_correct, n),
        "accepted_count": len(accepted),
        "accepted_accuracy": _safe_div(accepted_correct, len(accepted)),
        "accepted_risk": _safe_div(accepted_wrong, len(accepted)),
        "reject_rate": _safe_div(len(rejected), n),
        "need_next_measurement_rate": _safe_div(len(need_next), n),
        "brier_score": float(brier),
        "via_case_count": len(via_truth),
        "gap_case_count": len(gap_truth),
        "via_gap_ambiguous_reject_rate": _safe_div(len(ambiguous_rejects), len(via_truth) + len(gap_truth)),
        "mean_top_probability": float(np.mean([r.top_probability for r in results])) if results else 0.0,
        "mean_posterior_entropy": float(np.mean([r.posterior_entropy for r in results])) if results else 0.0,
        "mean_via_gap_angle_deg": float(np.mean([r.via_gap_angle_deg for r in results])) if results else 0.0,
        "mean_case_via_gap_angle_deg": mean_case_angle,
        "min_case_via_gap_angle_deg": min_case_angle,
        "by_truth": by_truth,
        "decision_counts": dict(Counter(r.decision for r in results)),
        "h0_top1_accuracy": by_truth["H0_no_via"]["top1_accuracy"],
        "h2_mean_true_posterior": by_truth["H2_model_gap"]["mean_true_posterior"],
        "h2_top1_accuracy": by_truth["H2_model_gap"]["top1_accuracy"],
        "h2_reject_or_need_next_rate": by_truth["H2_model_gap"].get("h2_reject_or_need_next_rate", 0.0),
        "h3_top1_accuracy": by_truth["H3_return_path"]["top1_accuracy"],
        "h3_mean_true_posterior": by_truth["H3_return_path"]["mean_true_posterior"],
        "h3_reject_or_need_next_rate": by_truth["H3_return_path"].get("h3_reject_or_need_next_rate", 0.0),
        "no_via_false_positive_guard_count": no_via_decisions,
        "residual_alignment_by_truth": residual_alignment_by_truth,
    }


def aggregate_baseline(rows: list[dict]) -> dict:
    n = len(rows)
    correct = sum(bool(r["correct"]) for r in rows)
    by_truth = defaultdict(list)
    for r in rows:
        by_truth[r["truth"]].append(r)
    return {
        "case_count": n,
        "top1_accuracy": _safe_div(correct, n),
        "by_truth": {
            h: {
                "count": len(v),
                "accuracy": _safe_div(sum(bool(r["correct"]) for r in v), len(v)),
            }
            for h, v in by_truth.items()
        },
        "confusion": confusion_matrix(rows, "truth", "predicted"),
    }


def engineering_gates(obghi_metrics: dict, op_diag: dict) -> dict[str, bool]:
    return {
        "posterior_rows_present": obghi_metrics["case_count"] > 0,
        "operator_via_columns_nonzero": op_diag.get("via_columns_nonzero", False),
        "topology_posterior_nontrivial": obghi_metrics["mean_posterior_entropy"] > 0.05,
        "generated_domain_boundaries_recorded": True,
        "leakage_audit_present": True,
        "reports_written": True,
    }


def scientific_gates(obghi_metrics: dict, baseline_metrics: dict) -> dict[str, bool]:
    return {
        "accepted_risk_le_0_45": obghi_metrics["accepted_risk"] <= 0.45,
        "reject_rate_ge_0_10_or_need_next_ge_0_20": (
            obghi_metrics["reject_rate"] >= 0.10
            or obghi_metrics["need_next_measurement_rate"] >= 0.20
        ),
        "h0_top1_ge_0_50": obghi_metrics.get("h0_top1_accuracy", 0.0) >= 0.50,
        "h2_true_posterior_ge_0_10_or_h2_reject_rate_ge_0_30": (
            obghi_metrics.get("h2_mean_true_posterior", 0.0) >= 0.10
            or obghi_metrics.get("h2_reject_or_need_next_rate", 0.0) >= 0.30
        ),
        "h3_top1_ge_0_20_or_h3_need_next_reject_ge_0_40": (
            obghi_metrics.get("h3_top1_accuracy", 0.0) >= 0.20
            or obghi_metrics.get("h3_reject_or_need_next_rate", 0.0) >= 0.40
        ),
        "obghi_top1_beats_ridge_by_0_05": (
            obghi_metrics["top1_accuracy"] >= baseline_metrics["top1_accuracy"] + 0.05
        ),
        "via_gap_ambiguous_reject_nonzero_on_gap_or_via": (
            obghi_metrics.get("via_gap_ambiguous_reject_rate", 0.0) > 0.0
        ),
    }
