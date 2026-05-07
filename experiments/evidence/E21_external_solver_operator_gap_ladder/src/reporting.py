"""Report writing for E21 operator-gap ladder evidence package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from external_artifacts import ExternalArtifactReport
from gap_metrics import FieldGap
from decision_stability import DecisionStabilityResult, DecisionSwap


def write_metrics_json(
    outputs_dir: Path,
    metrics: Dict[str, Any],
) -> None:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    path = outputs_dir / "metrics.json"
    path.write_text(json.dumps(_sanitize(metrics), indent=2, default=str), encoding="utf-8")


def write_run_report(
    outputs_dir: Path,
    metrics: Dict[str, Any],
) -> None:
    gates = metrics.get("acceptance_gates", {})
    gate_lines = "\n".join(
        f"- {name}: {'PASS' if g.get('pass', False) else 'FAIL'} — {g.get('threshold', 'N/A')}"
        for name, g in gates.items()
    )
    all_pass = metrics.get("all_acceptance_gates_passed", False)

    gap_table = metrics.get("operator_gap_summary", [])
    gap_rows = "\n".join(
        f"| {g.get('pair', '?')} | {g.get('rel_rmse', 0):.4e} | "
        f"Bx={g.get('per_component_rel_rmse', {}).get('Bx', 0):.4e} "
        f"By={g.get('per_component_rel_rmse', {}).get('By', 0):.4e} "
        f"Bz={g.get('per_component_rel_rmse', {}).get('Bz', 0):.4e} |"
        for g in gap_table
    )

    decision = metrics.get("decision_instability", {})
    ds_summary = decision.get("instability_summary", "no cross-operator tests run") if isinstance(decision, dict) else "N/A"

    ext = metrics.get("external_validation_status", {})
    if isinstance(ext, dict):
        ext_status = ext.get("status", "unknown")
    else:
        ext_status = str(ext)

    report = f"""# E21 External-Solver Operator-Gap Ladder — Run Report

## Gate Summary

Overall: {'PASS' if all_pass else 'FAIL'}

{gate_lines}

## Key Metrics

- case_count: {metrics.get('case_count', 0)}
- available_operator_count: {metrics.get('available_operator_count', 0)}
- external_solver_artifacts_present: {metrics.get('external_solver_artifacts_present', False)}
- unit_sanity_passed: {metrics.get('unit_sanity_passed', False)}

### Operator Gap Table

| Pair | Rel RMSE | Per-Component |
|---|---|---|
{gap_rows}

### Spectral Gaps

See `outputs/SPECTRAL_GAP.md` for per-frequency analysis.

### Decision Instability

{ds_summary}

### External Validation Status

{ext_status}

## Cannot Claim

- COMSOL/FastHenry/FEM validation unless real external artifacts are loaded
- PyPEEC is ground-truth real physics
- Generated operator agreement proves real CAD/GDS or real QDM/NV validation
- Inverse decisions transfer to real hardware

## Boundary

This package quantifies operator gaps among implemented/generated operators.
External solver validation is {'blocked — no COMSOL/FastHenry artifacts loaded' if ext_status == 'blocked' else ext_status}.
All PyPEEC results are generated-domain evidence.
"""
    (outputs_dir / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def write_operator_gap_table(
    outputs_dir: Path,
    gaps: List[FieldGap],
) -> None:
    lines = [
        "# Operator Gap Table\n\n",
        "| Pair | Rel RMSE | Bx | By | Bz | Spectral Low-k | Spectral High-k | Polarity | Sign Match |\n",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for g in gaps:
        bx = g.per_component_rel_rmse.get("Bx", float("nan"))
        by_v = g.per_component_rel_rmse.get("By", float("nan"))
        bz = g.per_component_rel_rmse.get("Bz", float("nan"))
        lines.append(
            f"| {g.pair_name} | {g.rel_rmse:.4e} | {bx:.4e} | {by_v:.4e} | {bz:.4e} | "
            f"{g.spectral_low_k:.4e} | {g.spectral_high_k:.4e} | {g.polarity_consistency:.4f} | {g.sign_match_rate:.4f} |\n"
        )
    lines.append("\nAll gaps are field-level comparisons on generated-domain geometries.\n")
    (outputs_dir / "OPERATOR_GAP_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_spectral_gap(
    outputs_dir: Path,
    gaps: List[FieldGap],
) -> None:
    lines = [
        "# Spectral Gap Analysis\n\n",
        "Low-k (below median spatial frequency) and high-k (above median) operator gaps.\n\n",
        "| Pair | Low-k gap | High-k gap | Interpretation |\n",
        "|---|---:|---:|---|\n",
    ]
    for g in gaps:
        interp = "low-k dominated" if g.spectral_low_k > g.spectral_high_k else "high-k dominated"
        lines.append(f"| {g.pair_name} | {g.spectral_low_k:.4e} | {g.spectral_high_k:.4e} | {interp} |\n")
    lines.append(
        "\nNote: high-k gap dominance suggests finite-width/nuisance differences; "
        "low-k gap dominance suggests return-path or geometry-scale differences.\n"
    )
    (outputs_dir / "SPECTRAL_GAP.md").write_text("".join(lines), encoding="utf-8")


def write_decision_instability(
    outputs_dir: Path,
    ds_result: DecisionStabilityResult,
    mechanism_results: dict = None,
    template_results: dict = None,
    gates: dict = None,
) -> None:
    """Write comprehensive decision instability report with all three analysis levels."""
    lines = [
        "# Decision Instability Report\n\n",
        "## 1. Ridge Reconstruction Instability\n\n",
        "Decoder trained on operator A_i, evaluated on fields from operator A_j.\n\n",
        "### Same-Operator Errors\n\n",
    ]
    for op, err in ds_result.same_operator_errors.items():
        lines.append(f"- {op}: {err:.4e}\n")
    lines.append("\n### Cross-Operator Errors\n\n")
    for pair, err in ds_result.cross_operator_errors.items():
        lines.append(f"- {pair}: {err:.4e}\n")
    lines.append("\n### Ridge Instability Ratios (cross / same)\n\n")
    lines.append("| Swap | Same Err | Cross Err | Ratio |\n")
    lines.append("|---|---:|---:|---:|\n")
    for s in ds_result.swaps:
        lines.append(f"| {s.pair} | {s.same_operator_error:.4e} | {s.cross_operator_error:.4e} | {s.instability_ratio:.1f}x |\n")
    lines.append(f"\n### Ridge Summary\n\n{ds_result.instability_summary}\n")

    # --- Mechanism decision instability (linear classifier) ---
    if mechanism_results and len(mechanism_results) > 0:
        lines.append("\n## 2. Mechanism Decision Instability (Linear Classifier)\n\n")
        lines.append("H0/H1/H2/H3 classification under operator swaps.\n\n")
        for op_name, mr in mechanism_results.items():
            lines.append(f"### Decoder: {op_name}\n\n")
            lines.append(f"- Same-operator accuracy: {mr.same_operator_accuracy:.4f}\n")
            lines.append(f"- False via rate (H0→H1): {mr.false_via_rate:.4f}\n")
            lines.append(f"- Return-path confusion (H3→H1): {mr.return_path_confusion_rate:.4f}\n\n")

            lines.append("#### Cross-Operator Accuracy\n\n")
            for test_op, acc in mr.cross_operator_accuracy.items():
                lines.append(f"- {test_op}: {acc:.4f}\n")

            lines.append("\n#### Mechanism Instability Ratios (same / cross)\n\n")
            for ratio_name, ratio_val in mr.cross_same_accuracy_ratio.items():
                lines.append(f"- {ratio_name}: {ratio_val:.2f}x\n")

            lines.append("\n#### Confusion Matrix\n\n")
            cm = mr.confusion_matrix
            if cm and len(cm) > 0:
                n = len(cm)
                lines.append("| Truth \\\\ Pred |" + "|".join(f" H{i}" for i in range(n)) + "|\n")
                lines.append("|---|" + "|".join("---:" for _ in range(n)) + "|\n")
                for i in range(n):
                    lines.append(f"| H{i} |" + "|".join(f" {cm[i][j]}" for j in range(n)) + "|\n")
            lines.append("\n")

    # --- Template evidence scorer instability ---
    if template_results and len(template_results) > 0:
        lines.append("\n## 3. Template Evidence Scorer Instability\n\n")
        lines.append("Class-mean template scorer: score_h = min_alpha || y - alpha * T_h ||^2.\n\n")
        for op_name, tr in template_results.items():
            lines.append(f"### Templates from: {op_name}\n\n")
            lines.append(f"- Same-operator accuracy: {tr.same_operator_accuracy:.4f}\n")
            lines.append(f"- False via rate (H0→H1): {tr.false_via_rate:.4f}\n")
            lines.append(f"- Return-path confusion (H3→H1): {tr.return_path_confusion_rate:.4f}\n\n")

            lines.append("#### Cross-Operator Accuracy\n\n")
            for test_op, acc in tr.cross_operator_accuracy.items():
                lines.append(f"- {test_op}: {acc:.4f}\n")

            lines.append("\n#### Template Instability Ratios (same / cross)\n\n")
            for ratio_name, ratio_val in tr.instability_ratio.items():
                lines.append(f"- {ratio_name}: {ratio_val:.2f}x\n")

            lines.append("\n#### Confusion Matrix\n\n")
            cm = tr.confusion_matrix
            if cm and len(cm) > 0:
                n = len(cm)
                lines.append("| Truth \\\\ Pred |" + "|".join(f" H{i}" for i in range(n)) + "|\n")
                lines.append("|---|" + "|".join("---:" for _ in range(n)) + "|\n")
                for i in range(n):
                    lines.append(f"| H{i} |" + "|".join(f" {cm[i][j]}" for j in range(n)) + "|\n")
            lines.append("\n")

    # --- Gate summary ---
    if gates:
        lines.append("\n## 4. Acceptance Gate Summary\n\n")
        lines.append("| Gate | Result | Value |\n")
        lines.append("|---|---|---|\n")
        for gate_name, gate_info in gates.items():
            status = "PASS" if gate_info.get("pass", False) else "FAIL"
            val = gate_info.get("value", "N/A")
            if isinstance(val, float):
                val_str = f"{val:.4g}"
            else:
                val_str = str(val)
            lines.append(f"| {gate_name} | {status} | {val_str} |\n")
        lines.append("\n")
    else:
        lines.append("\n## Decision Instability Summary\n\n")
        lines.append(f"{ds_result.instability_summary}\n")
    (outputs_dir / "DECISION_INSTABILITY.md").write_text("".join(lines), encoding="utf-8")


def write_mechanism_decision_instability(
    outputs_dir: Path,
    mechanism_results: dict,
) -> None:
    lines = [
        "# Mechanism-Level Decision Instability Report\n\n",
        "H0/H1/H2/H3 hypothesis classification under operator swaps.\n\n",
    ]
    if not mechanism_results:
        lines.append("Mechanism decision stress not executed.\n")
    else:
        for op_name, mr in mechanism_results.items():
            lines.append(f"## Decoder trained on: {op_name}\n\n")
            lines.append(f"- Same-operator accuracy: {mr.same_operator_accuracy:.4f}\n")
            lines.append(f"- False via rate (H0→H1): {mr.false_via_rate:.4f}\n")
            lines.append(f"- Return-path confusion (H3→H1): {mr.return_path_confusion_rate:.4f}\n\n")

            lines.append("### Cross-Operator Accuracy\n\n")
            for test_op, acc in mr.cross_operator_accuracy.items():
                lines.append(f"- On {test_op}: {acc:.4f}\n")

            lines.append("\n### Cross/Same Accuracy Ratios\n\n")
            for ratio_name, ratio_val in mr.cross_same_accuracy_ratio.items():
                lines.append(f"- {ratio_name}: {ratio_val:.2f}x\n")

            lines.append("\n### Confusion Matrix (same-operator)\n\n")
            cm = mr.confusion_matrix
            if cm and len(cm) > 0:
                n = len(cm)
                header = "| Truth \\ Pred |" + "|".join(f" H{i}" for i in range(n)) + "|\n"
                lines.append(header)
                lines.append("|---|" + "|".join("---:" for _ in range(n)) + "|\n")
                for i in range(n):
                    row = f"| H{i} |" + "|".join(f" {cm[i][j]}" for j in range(n)) + "|\n"
                    lines.append(row)
            lines.append("\n")
    (outputs_dir / "MECHANISM_DECISION_INSTABILITY.md").write_text("".join(lines), encoding="utf-8")


def write_external_artifact_contract(
    outputs_dir: Path,
    ext_report: ExternalArtifactReport,
) -> None:
    lines = [
        "# External Artifact Contract\n\n",
        f"- COMSOL artifact present: {ext_report.comsol_present}\n",
        f"- FastHenry artifact present: {ext_report.fasthenry_present}\n",
        f"- Status: {ext_report.status}\n\n",
    ]
    if ext_report.comsol_validation:
        v = ext_report.comsol_validation
        lines.append(f"## COMSOL Schema Validation: {'PASS' if v.passed else 'FAIL'}\n")
        if v.errors:
            for e in v.errors:
                lines.append(f"- ERROR: {e}\n")
        if v.warnings:
            for w in v.warnings:
                lines.append(f"- WARNING: {w}\n")
    if ext_report.fasthenry_validation:
        v = ext_report.fasthenry_validation
        lines.append(f"\n## FastHenry Schema Validation: {'PASS' if v.passed else 'FAIL'}\n")
        if v.errors:
            for e in v.errors:
                lines.append(f"- ERROR: {e}\n")
        if v.warnings:
            for w in v.warnings:
                lines.append(f"- WARNING: {w}\n")
    lines.append("\n## Cannot Claim\n\n")
    for c in ext_report.cannot_claim:
        lines.append(f"- {c}\n")
    (outputs_dir / "EXTERNAL_ARTIFACT_CONTRACT.md").write_text("".join(lines), encoding="utf-8")


def write_failure_modes(
    outputs_dir: Path,
    metrics: Dict[str, Any],
) -> None:
    lines = [
        "# Failure Modes\n\n",
        "## Blocked Validation Paths\n\n",
    ]
    ext_status = metrics.get("external_validation_status", {})
    if isinstance(ext_status, dict) and ext_status.get("status") == "blocked":
        lines.append("- External solver (COMSOL/FastHenry/FEM) validation: BLOCKED — no artifact files loaded.\n")
    else:
        lines.append("- External solver validation: partial or full.\n")

    pypeec = metrics.get("pypeec_status", {})
    if isinstance(pypeec, dict) and not pypeec.get("available", False):
        lines.append("- PyPEEC operator: BLOCKED — PyPEEC not installed or available.\n")
    else:
        lines.append("- PyPEEC operator: available (generated-domain evidence only).\n")

    gaps = metrics.get("operator_gap_summary", [])
    for g in gaps:
        if g.get("rel_rmse", 0) > 100:
            lines.append(f"- Very large gap for {g.get('pair', '?')}: rel_rmse={g['rel_rmse']:.2e}.\n")

    decision = metrics.get("decision_instability", {})
    if isinstance(decision, dict):
        swaps = decision.get("swaps", [])
        for s in swaps:
            if s.get("instability_ratio", 1.0) > 100:
                lines.append(f"- High decision instability: {s.get('pair', '?')} ratio={s['instability_ratio']:.1f}x.\n")

    lines.append("\n## Known Limitations\n\n")
    lines.append("- All operators are generated-domain; no real CAD/GDS or QDM/NV data.\n")
    lines.append("- PyPEEC bridge is generated-domain higher-fidelity, not ground truth.\n")
    lines.append("- Decision instability is measured on toy current prediction, not full hypothesis scoring.\n")

    (outputs_dir / "FAILURE_MODES.md").write_text("".join(lines), encoding="utf-8")


# --- Round 4: Ridge evidence scorer and margin refusal audit reports ---

def write_ridge_evidence_scorer_audit(
    outputs_dir: Path,
    ridge_results: dict,
) -> None:
    lines = [
        "# Ridge Evidence Scorer Audit\n\n",
        "Per-hypothesis ridge evidence: score_h = min_alpha ||y - alpha*T_h||^2 + lambda*alpha^2\n\n",
    ]
    if not ridge_results:
        lines.append("Ridge evidence stress not executed.\n")
    else:
        for op_name, rr in ridge_results.items():
            lines.append(f"## Scorer trained on: {op_name}\n\n")
            lines.append(f"- Best lambda: {rr.best_lambda:.4e}\n")
            lines.append(f"- Same-operator accuracy: {rr.same_operator_accuracy:.4f}\n")
            lines.append(f"- False via rate (H0->H1): {rr.false_via_rate:.4f}\n")
            lines.append(f"- Return-path confusion (H3->H1): {rr.return_path_confusion_rate:.4f}\n\n")

            lines.append("### Cross-Operator Accuracy\n\n")
            for test_op, acc in rr.cross_operator_accuracy.items():
                lines.append(f"- On {test_op}: {acc:.4f}\n")

            lines.append("\n### Ridge Instability Ratios (same / cross)\n\n")
            for ratio_name, ratio_val in rr.instability_ratio.items():
                lines.append(f"- {ratio_name}: {ratio_val:.2f}x\n")

            lines.append("\n### Confusion Matrix (same-operator)\n\n")
            cm = rr.confusion_matrix_same
            _write_cm_table(lines, cm)

            for test_op, cm_c in rr.confusion_matrix_cross.items():
                lines.append(f"\n### Confusion Matrix (cross-operator: templates on {test_op})\n\n")
                _write_cm_table(lines, cm_c)
    (outputs_dir / "RIDGE_EVIDENCE_SCORER_AUDIT.md").write_text("".join(lines), encoding="utf-8")


def write_margin_refusal_audit(
    outputs_dir: Path,
    margin_results: dict,
) -> None:
    lines = [
        "# Margin Refusal Operator Gap Audit\n\n",
        "Margin = score_second_best - score_best. Accept if margin >= 50th-percentile threshold.\n\n",
    ]
    if not margin_results:
        lines.append("Margin/refusal audit not executed.\n")
    else:
        for op_name, mr in margin_results.items():
            lines.append(f"## Scorer trained on: {op_name}\n\n")
            lines.append(f"- Margin threshold: {mr.margin_threshold:.6e}\n")
            lines.append(f"- Accepted rate (same-op): {mr.accepted_rate_same:.4f}\n")
            lines.append(f"- Accepted accuracy (same-op): {mr.accepted_accuracy_same:.4f}\n\n")

            lines.append("### Cross-Operator Margin Audit\n\n")
            lines.append("| Test Op | Accept Rate | Accept Acc | Wrong Accept | Refusal Rate |\n")
            lines.append("|---|---:|---:|---:|---:|\n")
            for test_op in sorted(mr.accepted_rate_cross.keys()):
                ar = mr.accepted_rate_cross.get(test_op, 0.0)
                aa = mr.accepted_accuracy_cross.get(test_op, 0.0)
                wa = mr.wrong_accept_rate_cross.get(test_op, 0.0)
                rr = mr.refusal_rate_cross.get(test_op, 0.0)
                lines.append(f"| {test_op} | {ar:.4f} | {aa:.4f} | {wa:.4f} | {rr:.4f} |\n")
            lines.append("\n")
    (outputs_dir / "MARGIN_REFUSAL_OPERATOR_GAP_AUDIT.md").write_text("".join(lines), encoding="utf-8")


def write_round4_gate_audit(
    outputs_dir: Path,
    gates: dict,
    ridge_results: dict,
    margin_results: dict,
) -> None:
    lines = [
        "# Round 4 Operator Gap Gate Audit\n\n",
        "Breakthrough gates for ridge evidence scorer and margin refusal.\n\n",
        "| Gate | Result | Value | Threshold |\n",
        "|---|---:|---:|---:|\n",
    ]
    if gates:
        for gate_name, gate_info in gates.items():
            status = "PASS" if gate_info.get("pass", False) else "FAIL"
            val = gate_info.get("value", "N/A")
            thr = gate_info.get("threshold", "N/A")
            if isinstance(val, float):
                val_str = f"{val:.4g}"
            else:
                val_str = str(val)
            lines.append(f"| {gate_name} | {status} | {val_str} | {thr} |\n")
    lines.append("\n")
    (outputs_dir / "ROUND4_OPERATOR_GAP_GATE_AUDIT.md").write_text("".join(lines), encoding="utf-8")


def _write_cm_table(lines: List[str], cm) -> None:
    if not cm or len(cm) == 0:
        lines.append("(empty)\n")
        return
    n = len(cm)
    lines.append("| Truth \\\\ Pred |" + "|".join(f" H{i}" for i in range(n)) + "|\n")
    lines.append("|---|" + "|".join("---:" for _ in range(n)) + "|\n")
    for i in range(n):
        lines.append(f"| H{i} |" + "|".join(f" {cm[i][j]}" for j in range(n)) + "|\n")


# --- Round 5: Multi-basis and margin-shift certificate reports ---

def write_multibasis_audit(
    outputs_dir: Path,
    multibasis_results: dict,
) -> None:
    lines = [
        "# Multi-Basis Evidence Scorer Audit\n\n",
        "Per-hypothesis PCA subspace evidence: d_h(y)^2 = ||y - Q_h Q_h^T y||^2.\n\n",
    ]
    if not multibasis_results:
        lines.append("Multi-basis stress not executed.\n")
    else:
        for op_name, mr in multibasis_results.items():
            lines.append(f"## Scorer trained on: {op_name}\n\n")
            lines.append(f"- k components: {mr.k_components}\n")
            lines.append(f"- Energy retained: {mr.energy_retained:.4f}\n")
            lines.append(f"- Same-operator accuracy: {mr.same_operator_accuracy:.4f}\n")
            lines.append(f"- Cross-operator drop: {mr.cross_operator_drop:.4f}\n")
            lines.append(f"- False via rate (H0->H1): {mr.false_via_rate:.4f}\n")
            lines.append(f"- Return-path confusion (H3->H1): {mr.return_path_confusion_rate:.4f}\n\n")

            lines.append("### Cross-Operator Accuracy\n\n")
            for test_op, acc in mr.cross_operator_accuracy.items():
                lines.append(f"- On {test_op}: {acc:.4f}\n")

            lines.append("\n### Confusion Matrix (same-operator)\n\n")
            _write_cm_table(lines, mr.confusion_matrix_same)
            for test_op, cm_c in mr.confusion_matrix_cross.items():
                lines.append(f"\n### Confusion Matrix (cross: {test_op})\n\n")
                _write_cm_table(lines, cm_c)
    (outputs_dir / "MULTIBASIS_EVIDENCE_SCORER_AUDIT.md").write_text("".join(lines), encoding="utf-8")


def write_margin_shift_certificate(
    outputs_dir: Path,
    cert: object,
) -> None:
    """cert is a MarginShiftCertificate."""
    lines = [
        "# Margin-Shift Operator-Gap Certificate\n\n",
        "Quantifies whether the operator perturbation exceeds the inter-class mechanism margin.\n\n",
        "## Certificate\n\n",
        f"- min inter-class delta: {cert.interclass_delta_min:.6e}\n",
        f"- max operator shift radius: {cert.operator_shift_radius_max:.6e}\n",
        f"- gap-to-margin ratio: {cert.gap_to_margin_ratio:.4f}\n",
        f"- stable classification possible by margin: **{cert.stable_classification_possible_by_margin}**\n\n",
        f"## Summary\n\n{cert.certificate_summary}\n\n",
        "## Inter-Class Pairwise Deltas\n\n",
    ]
    for pair, delta in sorted(cert.interclass_delta_by_pair.items()):
        lines.append(f"- {pair}: {delta:.6e}\n")
    lines.append("\n## Operator Shift Radius by Hypothesis\n\n")
    for key, val in sorted(cert.operator_shift_radius_by_hypothesis.items()):
        lines.append(f"- {key}: {val:.6e}\n")
    (outputs_dir / "MARGIN_SHIFT_CERTIFICATE.md").write_text("".join(lines), encoding="utf-8")


def write_round5_boundary_audit(
    outputs_dir: Path,
    gates: dict,
    cert: object,
) -> None:
    lines = [
        "# Round 5 Operator Gap Boundary Audit\n\n",
        "## Certificate Result\n\n",
        f"- stable_classification_possible_by_margin: **{cert.stable_classification_possible_by_margin}**\n",
        f"- gap_to_margin_ratio: {cert.gap_to_margin_ratio:.4f}\n",
        f"- certificate_summary: {cert.certificate_summary}\n\n",
        "## Gates\n\n",
        "| Gate | Result | Value | Threshold |\n",
        "|---|---:|---:|---:|\n",
    ]
    if gates:
        for gate_name, gate_info in gates.items():
            status = "PASS" if gate_info.get("pass", False) else "FAIL"
            val = gate_info.get("value", "N/A")
            thr = gate_info.get("threshold", "N/A")
            if isinstance(val, float):
                val_str = f"{val:.4g}"
            else:
                val_str = str(val)
            lines.append(f"| {gate_name} | {status} | {val_str} | {thr} |\n")
    lines.append("\n")
    (outputs_dir / "ROUND5_OPERATOR_GAP_BOUNDARY_AUDIT.md").write_text("".join(lines), encoding="utf-8")


def _sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


import numpy as np
