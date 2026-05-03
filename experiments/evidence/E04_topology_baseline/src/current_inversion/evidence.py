from __future__ import annotations

import math
from typing import Any


def _finite_float(value: Any, default: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def _proximity(distance_px: Any, radius_px: float) -> float:
    if distance_px is None:
        return 0.0
    distance = max(_finite_float(distance_px, 1.0e9), 0.0)
    radius = max(float(radius_px), 1.0e-9)
    return max(0.0, 1.0 - min(distance / radius, 1.0))


def null_via_hypothesis_evidence(row: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Score H1(true via) against H0(artifact/no-via) for one candidate row.

    This is deliberately evidence reporting, not a new tuned detector. The
    defaults are conservative and are not fit on PyPEEC rows.
    """
    params = params or {}
    bend_radius = _finite_float(params.get("bend_radius_px"), 2.0)
    return_radius = _finite_float(params.get("return_radius_px"), 2.0)
    s1_peak = max(_finite_float(row.get("s1_peak_abs_current_scale")), 0.0)
    topology_gain = max(_finite_float(row.get("topology_improvement")), 0.0)
    physical_gain = _finite_float(row.get("physical_b_improvement"))
    dog_score = max(_finite_float(row.get("dog_score_peak_over_threshold")), 0.0)
    compactness = max(_finite_float(row.get("candidate_compactness"), 0.5), 0.0)
    stability = max(_finite_float(row.get("stability_proxy"), 0.0), 0.0)
    bend_prox = _proximity(row.get("distance_to_bend_px"), bend_radius)
    return_prox = _proximity(row.get("distance_to_return_px"), return_radius)
    trace_prox = _proximity(row.get("distance_to_trace_px"), max(bend_radius, return_radius))

    h1 = (
        0.95 * min(s1_peak, 3.0)
        + 0.70 * min(topology_gain, 2.0)
        + 1.10 * max(physical_gain, 0.0)
        + 0.18 * math.log1p(dog_score)
        + 0.20 * min(compactness, 1.0)
        + 0.12 * min(stability, 1.0)
        + 0.08 * trace_prox
    )
    h0_artifact = (
        0.85 * bend_prox
        + 0.95 * return_prox
        + 1.20 * max(-physical_gain, 0.0)
        + 0.25 * max(0.0, 1.0 - min(compactness, 1.0))
    )
    return_evidence = return_prox + 0.50 * max(-physical_gain, 0.0)
    margin = h1 - h0_artifact
    uncertainty = 1.0 / (1.0 + abs(margin))
    if not bool(row.get("candidate_present", False)):
        decision = "no_candidate"
    elif margin >= 0.75 and physical_gain >= -0.01:
        decision = "high_confidence_via"
    elif return_evidence >= 0.80 and margin < 0.75:
        decision = "return_path_ambiguous"
    elif h0_artifact > h1:
        decision = "probable_artifact"
    elif uncertainty >= 0.65:
        decision = "low_confidence_residual"
    else:
        decision = "needs_extra_observation"
    return {
        "h1_true_via_evidence": float(h1),
        "h0_artifact_evidence": float(h0_artifact),
        "return_path_evidence": float(return_evidence),
        "evidence_margin_h1_minus_h0": float(margin),
        "uncertainty_proxy": float(uncertainty),
        "bend_proximity": float(bend_prox),
        "return_proximity": float(return_prox),
        "trace_proximity": float(trace_prox),
        "decision": decision,
    }


def summarize_evidence_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for model in sorted({str(row.get("model")) for row in rows}):
        model_rows = [row for row in rows if str(row.get("model")) == model]
        counts: dict[str, int] = {}
        for row in model_rows:
            label = str(row.get("decision", "unknown"))
            counts[label] = counts.get(label, 0) + 1
        high_via = [row for row in model_rows if row.get("decision") == "high_confidence_via"]
        artifact = [row for row in model_rows if row.get("decision") == "probable_artifact"]
        ambiguous = [
            row
            for row in model_rows
            if row.get("decision") in {"low_confidence_residual", "return_path_ambiguous", "needs_extra_observation"}
        ]
        out[model] = {
            "n_rows": len(model_rows),
            "decision_counts": counts,
            "high_confidence_via_fraction": len(high_via) / max(len(model_rows), 1),
            "probable_artifact_fraction": len(artifact) / max(len(model_rows), 1),
            "ambiguous_or_refusal_fraction": len(ambiguous) / max(len(model_rows), 1),
            "mean_uncertainty_proxy": sum(_finite_float(row.get("uncertainty_proxy")) for row in model_rows) / max(len(model_rows), 1),
        }
    return out


def generative_hypothesis_score(row: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Compare H1(with predicted via/source) against H0(predicted sheets, s1=0).

    The score is a frozen model-selection diagnostic. It uses two explicit
    re-forwarded hypotheses that are already available in the row:

    - H1 keeps the model's predicted s1 channel.
    - H0 removes the predicted s1 channel and asks whether the remaining sheet
      currents explain the same PyPEEC field.

    Positive ``delta_evidence_h1_minus_h0`` means H1 is favored. The defaults
    are fixed, not fit on PyPEEC rows.
    """
    params = params or {}
    bend_radius = _finite_float(params.get("bend_radius_px"), 2.0)
    return_radius = _finite_float(params.get("return_radius_px"), 2.0)
    w_topology = _finite_float(params.get("weight_topology_energy"), 0.65)
    w_physical = _finite_float(params.get("weight_physical_energy"), 1.00)
    w_complexity = _finite_float(params.get("weight_s1_complexity"), 0.08)
    w_artifact = _finite_float(params.get("weight_artifact_penalty"), 0.45)
    w_unexplained = _finite_float(params.get("weight_h0_unexplained_peak"), 0.18)

    topology_h1 = max(_finite_float(row.get("topology_pred")), 0.0)
    topology_h0 = max(_finite_float(row.get("topology_zero_s1")), 0.0)
    physical_h1 = max(_finite_float(row.get("physical_b_pred")), 0.0)
    physical_h0 = max(_finite_float(row.get("physical_b_zero_s1")), 0.0)
    s1_peak = max(_finite_float(row.get("s1_peak_abs_current_scale")), 0.0)
    n_components = max(_finite_float(row.get("candidate_components")), 0.0)
    physical_gain = physical_h0 - physical_h1
    bend_prox = _proximity(row.get("distance_to_bend_px"), bend_radius)
    return_prox = _proximity(row.get("distance_to_return_px"), return_radius)
    artifact_prox = max(bend_prox, return_prox)

    # H1 should pay a small complexity/artifact penalty. A via-like explanation
    # near known artifact zones only wins if it improves physical re-forward.
    energy_h1 = (
        w_topology * math.log1p(topology_h1)
        + w_physical * physical_h1
        + w_complexity * math.log1p(s1_peak + n_components)
        + w_artifact * artifact_prox * max(0.0, 0.02 - physical_gain)
    )
    # H0 should pay an unexplained-candidate penalty when a strong source/sink
    # candidate exists but removing it leaves the field/topology worse.
    energy_h0 = (
        w_topology * math.log1p(topology_h0)
        + w_physical * physical_h0
        + w_unexplained * max(0.0, s1_peak - 0.20)
    )
    delta = energy_h0 - energy_h1
    uncertainty = 1.0 / (1.0 + abs(delta))
    if not bool(row.get("candidate_present", False)):
        decision = "no_candidate"
    elif delta >= 0.15 and physical_gain >= -0.01:
        decision = "generative_h1_true_via_favored"
    elif delta <= -0.15:
        decision = "generative_h0_artifact_favored"
    elif artifact_prox >= 0.50:
        decision = "generative_ambiguous_artifact_zone"
    else:
        decision = "generative_low_margin_refusal"
    return {
        "generative_energy_h1_with_s1": float(energy_h1),
        "generative_energy_h0_zero_s1": float(energy_h0),
        "delta_evidence_h1_minus_h0": float(delta),
        "generative_physical_gain_h1_over_h0": float(physical_gain),
        "generative_uncertainty_proxy": float(uncertainty),
        "generative_artifact_proximity": float(artifact_prox),
        "generative_decision": decision,
    }


def binary_auc(labels: list[bool], scores: list[float]) -> float:
    """Return rank AUC for labels/scores without adding sklearn as a dependency."""
    pairs = [(float(score), bool(label)) for label, score in zip(labels, scores)]
    pos = [score for score, label in pairs if label]
    neg = [score for score, label in pairs if not label]
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return float(wins / (len(pos) * len(neg)))


def calibration_curve(rows: list[dict[str, Any]], score_key: str, label_key: str, n_bins: int = 6) -> list[dict[str, Any]]:
    valid = [
        row
        for row in rows
        if math.isfinite(_finite_float(row.get(score_key), float("nan")))
    ]
    if not valid:
        return []
    valid = sorted(valid, key=lambda row: _finite_float(row.get(score_key)))
    n = len(valid)
    bins: list[dict[str, Any]] = []
    for b in range(max(int(n_bins), 1)):
        lo = int(round(b * n / max(int(n_bins), 1)))
        hi = int(round((b + 1) * n / max(int(n_bins), 1)))
        part = valid[lo:hi]
        if not part:
            continue
        scores = [_finite_float(row.get(score_key)) for row in part]
        labels = [bool(row.get(label_key, False)) for row in part]
        bins.append(
            {
                "bin": b + 1,
                "n": len(part),
                "score_min": min(scores),
                "score_max": max(scores),
                "score_mean": sum(scores) / max(len(scores), 1),
                "observed_true_via_rate": sum(1 for label in labels if label) / max(len(labels), 1),
                "observed_no_via_rate": sum(1 for label in labels if not label) / max(len(labels), 1),
            }
        )
    return bins


def selective_risk_curve(
    rows: list[dict[str, Any]],
    score_key: str,
    label_key: str,
    confidence_key: str,
    coverages: list[float] | None = None,
) -> list[dict[str, Any]]:
    """Risk-coverage rows for selective via/no-via prediction.

    Prediction is H1 when ``score_key > 0``. Confidence is usually the absolute
    generative evidence margin. Rows are sorted by confidence descending.
    """
    coverages = coverages or [0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 1.00]
    valid = [
        row
        for row in rows
        if math.isfinite(_finite_float(row.get(score_key), float("nan")))
        and math.isfinite(_finite_float(row.get(confidence_key), float("nan")))
    ]
    if not valid:
        return []
    valid = sorted(valid, key=lambda row: _finite_float(row.get(confidence_key)), reverse=True)
    out: list[dict[str, Any]] = []
    n = len(valid)
    for cov in coverages:
        coverage = min(max(float(cov), 0.0), 1.0)
        k = max(1, int(math.ceil(coverage * n)))
        part = valid[:k]
        truth_via = [row for row in part if bool(row.get(label_key, False))]
        truth_no_via = [row for row in part if not bool(row.get(label_key, False))]
        pred_via = [row for row in part if _finite_float(row.get(score_key)) > 0.0]
        errors = [
            row
            for row in part
            if (_finite_float(row.get(score_key)) > 0.0) != bool(row.get(label_key, False))
        ]
        true_pos = [
            row
            for row in part
            if (_finite_float(row.get(score_key)) > 0.0) and bool(row.get(label_key, False))
        ]
        false_pos = [
            row
            for row in part
            if (_finite_float(row.get(score_key)) > 0.0) and not bool(row.get(label_key, False))
        ]
        precision = len(true_pos) / max(len(pred_via), 1)
        recall = len(true_pos) / max(len(truth_via), 1)
        out.append(
            {
                "coverage": float(k / n),
                "requested_coverage": float(coverage),
                "n_selected": int(k),
                "n_total": int(n),
                "selective_risk": float(len(errors) / max(len(part), 1)),
                "selective_accuracy": float(1.0 - len(errors) / max(len(part), 1)),
                "via_precision": float(precision),
                "via_recall_within_selected": float(recall),
                "no_via_false_positive_rate_within_selected": float(len(false_pos) / max(len(truth_no_via), 1)),
                "mean_confidence": sum(_finite_float(row.get(confidence_key)) for row in part) / max(len(part), 1),
            }
        )
    return out


def return_path_hypothesis(row: dict[str, Any]) -> dict[str, Any]:
    """Classify whether a return-path row is via-like or return-current-like."""
    allocation_error = _finite_float(row.get("layer_allocation_fraction_error"))
    return_l2 = _finite_float(row.get("return_path_rel_l2"))
    shape_residual = _finite_float(row.get("physical_reforward_shape_rel_l2_to_bpypeec"))
    amplitude_error = _finite_float(row.get("physical_reforward_amplitude_log_error_abs"))
    excess_vias = _finite_float(row.get("excess_predicted_via_components"))
    physical_delta = _finite_float(row.get("physical_b_delta_vs_no_topology"))
    topology_mse = _finite_float(row.get("topology_mse"))

    via_like = 0.40 * excess_vias + 0.30 * max(_finite_float(row.get("s1_peak_abs_current_scale")), 0.0)
    return_like = (
        0.80 * min(allocation_error, 2.0)
        + 0.35 * min(return_l2, 3.0)
        + 0.55 * min(shape_residual, 3.0)
        + 0.45 * min(amplitude_error, 3.0)
        + 0.80 * max(physical_delta, 0.0)
    )
    if return_like > via_like + 0.40:
        decision = "return_current_mismatch"
    elif via_like > return_like + 0.40:
        decision = "via_like_excess_source"
    elif topology_mse > 1.0 and physical_delta > 0.0:
        decision = "topology_physics_conflict"
    else:
        decision = "mixed_or_bounded"
    return {
        "via_like_evidence": float(via_like),
        "return_current_evidence": float(return_like),
        "return_margin_minus_via": float(return_like - via_like),
        "hypothesis_decision": decision,
    }


def summarize_return_path_hypotheses(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for model in sorted({str(row.get("model")) for row in rows}):
        model_rows = [row for row in rows if str(row.get("model")) == model]
        counts: dict[str, int] = {}
        for row in model_rows:
            label = str(row.get("hypothesis_decision", "unknown"))
            counts[label] = counts.get(label, 0) + 1
        out[model] = {
            "n_rows": len(model_rows),
            "decision_counts": counts,
            "mean_return_margin_minus_via": sum(_finite_float(row.get("return_margin_minus_via")) for row in model_rows)
            / max(len(model_rows), 1),
        }
    return out
