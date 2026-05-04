"""Markdown and JSON reporting for E19."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from basis import HYPOTHESES
from obghi import OBGHIResult, result_to_row


def _f(x: float | int | None) -> str:
    if x is None:
        return "N/A"
    if isinstance(x, int):
        return str(x)
    if abs(float(x)) >= 1e-3:
        return f"{float(x):.4f}"
    return f"{float(x):.3e}"


def posterior_table(results: list[OBGHIResult]) -> str:
    lines = [
        "# E19 Posterior Table",
        "",
        "| case | truth | top | p_top | decision | p_H0 | p_H1 | p_H2 | p_H3 | logBF_via_gap | angle_deg |",
        "|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        lines.append(
            "| {case} | {truth} | {top} | {p_top} | {decision} | {p0} | {p1} | {p2} | {p3} | {bf} | {ang} |".format(
                case=r.case_id,
                truth=r.truth_hypothesis,
                top=r.top_hypothesis,
                p_top=_f(r.top_probability),
                decision=r.decision,
                p0=_f(r.posteriors["H0_no_via"].posterior_probability),
                p1=_f(r.posteriors["H1_via"].posterior_probability),
                p2=_f(r.posteriors["H2_model_gap"].posterior_probability),
                p3=_f(r.posteriors["H3_return_path"].posterior_probability),
                bf=_f(r.logbf_via_gap),
                ang=_f(r.via_gap_angle_deg),
            )
        )
    return "\n".join(lines) + "\n"


def gates_markdown(gates: dict[str, bool], title: str = "# E19 Acceptance Gates") -> str:
    lines = [title, "", "| gate | passed |", "|---|---:|"]
    for k, v in gates.items():
        lines.append(f"| {k} | {bool(v)} |")
    lines.append("")
    lines.append(f"All gates passed: {all(gates.values())}")
    return "\n".join(lines) + "\n"


def scientific_gates_markdown(metrics: dict) -> str:
    eng = metrics.get("engineering_gates", {})
    sci = metrics.get("scientific_gates", {})
    lines = [
        "# E19.1 Scientific Gates",
        "",
        f"Engineering run status: {'PASS' if metrics.get('engineering_gates_passed') else 'FAIL'}",
        f"Scientific status: {'PASS' if metrics.get('scientific_gates_passed') else 'FAIL'}",
        "",
        "## Engineering Gates",
        "",
        "| gate | passed |",
        "|---|---:|",
    ]
    for k, v in eng.items():
        lines.append(f"| {k} | {bool(v)} |")
    lines += [
        "",
        "## Scientific Gates",
        "",
        "| gate | passed |",
        "|---|---:|",
    ]
    for k, v in sci.items():
        lines.append(f"| {k} | {bool(v)} |")
    lines += [
        "",
        f"Engineering gates passed: {all(eng.values())}",
        f"Scientific gates passed: {all(sci.values())}",
    ]
    return "\n".join(lines) + "\n"


def diagnostics_summary(metrics: dict, results: list[OBGHIResult]) -> str:
    obghi = metrics.get("obghi", {})
    lines = [
        "# E19.1 Diagnostics Summary",
        "",
        "## Case-specific via/gap angle",
        "",
        f"- mean case_via_gap_angle_deg: {_f(obghi.get('mean_case_via_gap_angle_deg', 'N/A'))}",
        f"- min case_via_gap_angle_deg: {_f(obghi.get('min_case_via_gap_angle_deg', 'N/A'))}",
        f"- global via_gap_angle_deg: {_f(obghi.get('mean_via_gap_angle_deg', 'N/A'))}",
        f"- via_gap_ambiguous_reject_rate: {_f(obghi.get('via_gap_ambiguous_reject_rate', 'N/A'))}",
        "",
        "## Residual alignment by truth",
        "",
        "| truth | mean alignment |",
        "|---|---:|",
    ]
    align = obghi.get("residual_alignment_by_truth", {})
    for h, val in align.items():
        lines.append(f"| {h} | {_f(val)} |")
    lines += [
        "",
        "## No-via false positive guard",
        "",
        f"- guard triggered count: {obghi.get('no_via_false_positive_guard_count', 'N/A')}",
        f"- h0_top1_accuracy: {_f(obghi.get('h0_top1_accuracy', 'N/A'))}",
        f"- h0_reject_or_need_next_rate: {_f(by_truth_h(obghi, 'H0_no_via', 'h0_reject_or_need_next_rate'))}",
        "",
        "## Decision distribution",
        "",
        "| decision | count |",
        "|---|---:|",
    ]
    for dec, count in obghi.get("decision_counts", {}).items():
        lines.append(f"| {dec} | {count} |")
    return "\n".join(lines) + "\n"


def by_truth_h(obghi: dict, h_key: str, field: str) -> float:
    bt = obghi.get("by_truth", {}).get(h_key, {})
    return bt.get(field, float("nan"))


def basis_audit(results: list[OBGHIResult]) -> str:
    lines = [
        "# E19.1 Basis Audit",
        "",
        "## Per-hypothesis column counts",
        "",
        "| hypothesis | kept_columns | dropped_columns | total_blocks |",
        "|---|---|---|---:|",
    ]
    if results:
        r = results[0]
        for h in HYPOTHESES:
            post = r.posteriors[h]
            blocks = len(post.per_block_column_counts) if hasattr(post, "per_block_column_counts") else 0
            lines.append(f"| {h} | {post.kept_column_count} | {post.dropped_column_count} | {blocks} |")
        lines += [
            "",
            "## Per-block column counts (first case sample)",
            "",
            "| hypothesis | block_kind | count |",
            "|---|---:|",
        ]
        for h in HYPOTHESES:
            post = r.posteriors[h]
            if hasattr(post, "per_block_column_counts"):
                for kind, count in post.per_block_column_counts.items():
                    lines.append(f"| {h} | {kind} | {count} |")
    return "\n".join(lines) + "\n"


def failure_cases(results: list[OBGHIResult]) -> str:
    lines = [
        "# E19 Failure Cases",
        "",
        "| case | truth | top | p_top | decision | failure_mode |",
        "|---|---|---|---:|---|---|",
    ]
    any_failure = False
    for r in results:
        failure = None
        if r.decision == "accept" and r.top_hypothesis != r.truth_hypothesis:
            failure = "accepted_wrong_topology"
        elif r.decision.startswith("reject") and r.truth_hypothesis == r.top_hypothesis:
            failure = "correct_topology_rejected"
        elif r.decision == "need_next_measurement":
            failure = "insufficient_posterior_separation"
        if failure:
            any_failure = True
            lines.append(
                f"| {r.case_id} | {r.truth_hypothesis} | {r.top_hypothesis} | {_f(r.top_probability)} | {r.decision} | {failure} |"
            )
    if not any_failure:
        lines.append("| none | - | - | - | - | no failure rows under current rules |")
    lines.append("")
    lines.append("Failures are preserved as generated-domain evidence boundaries.")
    return "\n".join(lines) + "\n"


def run_report(
    metrics: dict,
    gates: dict[str, bool],
    operator_diag: dict,
    baseline_metrics: dict,
) -> str:
    obghi = metrics.get("obghi", {})
    eng_passed = metrics.get("engineering_gates_passed", False)
    sci_passed = metrics.get("scientific_gates_passed", False)
    lines = [
        "# RUN REPORT - E19.1 OBGHI Calibrated Posterior Diagnostics",
        "",
        "E19.1 is generated-domain algorithm evidence. It does not constitute real",
        "QDM/NV, CAD/Gerber/GDS, or external-solver validation.",
        "",
        "## Engineering run status",
        "",
        f"Engineering gates passed: `{eng_passed}`",
        "",
        "## Scientific status",
        "",
        f"Scientific gates passed: `{sci_passed}`",
        "",
        "## Claim affected",
        "",
        "- Primary: `C10_pdn_kcl_distribution_need`",
        "- Secondary: `C06_graph_hypothesis_system_identification`, `C02_single_plane_identifiability_boundary`, `C04_inverse_crime_and_operator_gap`",
        "",
        "## Evidence added",
        "",
        "E19.1 calibrated OBGHI posterior evidence with:",
        "- Split engineering/scientific gates",
        "- Block-diagonal group priors",
        "- Per-column observable normalization",
        "- Expanded H2 gap basis (registration derivatives, standoff laplacians, drift)",
        "- Split H1 via basis (vertical modes + sheet compensation)",
        "- Expanded H3 return basis (multi-position loops, edge modes, distributed)",
        "- Residual-conditioned case-specific via/gap diagnostic",
        "- Multi-tier decision rule with no-via false-positive guard",
        "",
        "## Metrics",
        "",
        f"- case_count: {obghi.get('case_count', 'N/A')}",
        f"- OBGHI top1_accuracy: {_f(obghi.get('top1_accuracy'))}",
        f"- OBGHI accepted_accuracy: {_f(obghi.get('accepted_accuracy'))}",
        f"- OBGHI accepted_risk: {_f(obghi.get('accepted_risk'))}",
        f"- OBGHI reject_rate: {_f(obghi.get('reject_rate'))}",
        f"- OBGHI need_next_measurement_rate: {_f(obghi.get('need_next_measurement_rate'))}",
        f"- OBGHI via_gap_ambiguous_reject_rate: {_f(obghi.get('via_gap_ambiguous_reject_rate'))}",
        f"- OBGHI h0_top1_accuracy: {_f(obghi.get('h0_top1_accuracy'))}",
        f"- OBGHI h2_mean_true_posterior: {_f(obghi.get('h2_mean_true_posterior'))}",
        f"- OBGHI h2_top1_accuracy: {_f(obghi.get('h2_top1_accuracy'))}",
        f"- OBGHI h3_top1_accuracy: {_f(obghi.get('h3_top1_accuracy'))}",
        f"- OBGHI h3_mean_true_posterior: {_f(obghi.get('h3_mean_true_posterior'))}",
        f"- OBGHI no_via_false_positive_guard_count: {obghi.get('no_via_false_positive_guard_count', 'N/A')}",
        f"- Ridge-map top1_accuracy: {_f(baseline_metrics.get('top1_accuracy'))}",
        "",
        "## Operator diagnostics",
        "",
        f"- A shape: `{operator_diag.get('shape', 'N/A')}`",
        f"- via_columns_nonzero: `{operator_diag.get('via_columns_nonzero', 'N/A')}`",
        f"- via_column_norm_min: `{_f(operator_diag.get('via_column_norm_min'))}`",
        f"- via_column_norm_mean: `{_f(operator_diag.get('via_column_norm_mean'))}`",
        "",
        "## Engineering Gates",
        "",
        "| gate | passed |",
        "|---|---:|",
    ]
    for k, v in metrics.get("engineering_gates", {}).items():
        lines.append(f"| {k} | {bool(v)} |")
    lines += [
        "",
        "## Scientific Gates",
        "",
        "| gate | passed |",
        "|---|---:|",
    ]
    for k, v in metrics.get("scientific_gates", {}).items():
        lines.append(f"| {k} | {bool(v)} |")
    lines += [
        "",
        f"Engineering gates passed: `{eng_passed}`",
        f"Scientific gates passed: `{sci_passed}`",
        "",
        "## Claim status change",
        "",
        "None. Do not upgrade any claim. If scientific gates fail, E19.1 is",
        "diagnostic/limiting evidence only. If they pass, E19.1 supports/motivates",
        "the generated-domain claims but does not prove real validation.",
        "",
        "## Failure modes",
        "",
        "See `FAILURE_CASES.md` and `SCIENTIFIC_GATES.md`.",
        "",
        "## Cannot claim",
        "",
        "- real QDM/NV validation",
        "- real CAD/Gerber/GDS validation",
        "- external FEM/FastHenry/COMSOL validation",
        "- real-board PDN/KCL robustness",
        "- mechanism-level explanation on real data",
        "- universal via detection",
        "- that generated-domain evidence transfers to real hardware",
        "",
        "## Next required evidence",
        "",
        "1. Multi-height observation for standoff discrimination",
        "2. Multi-state excitation for current-path discrimination",
        "3. Replace generated families with CAD/Gerber/GDS-derived graph candidates",
        "4. Validate against external solver (COMSOL/FastHenry/FEM) on small subset",
        "",
        "## Tests run",
        "",
        "See repository CI or run locally:",
        "`uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests`",
        "",
        "## Files changed",
        "",
        "- `experiments/evidence/E19_obghi_minimal_observable_topology_posterior/`",
        "- `research_graph/experiments.yml`",
        "- `research_graph/evidence_edges.yml`",
        "- `research_graph/update_log.md`",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(
    out_dir: Path,
    metrics: dict,
    results: list[OBGHIResult],
    gates: dict[str, bool],
    operator_diag: dict,
    baseline_metrics: dict,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (out_dir / "POSTERIOR_TABLE.md").write_text(posterior_table(results), encoding="utf-8")
    eng = metrics.get("engineering_gates", {})
    sci = metrics.get("scientific_gates", {})
    (out_dir / "ACCEPTANCE_GATES.md").write_text(gates_markdown(gates), encoding="utf-8")
    (out_dir / "SCIENTIFIC_GATES.md").write_text(scientific_gates_markdown(metrics), encoding="utf-8")
    (out_dir / "FAILURE_CASES.md").write_text(failure_cases(results), encoding="utf-8")
    (out_dir / "RUN_REPORT.md").write_text(run_report(metrics, gates, operator_diag, baseline_metrics), encoding="utf-8")
    (out_dir / "DIAGNOSTICS_SUMMARY.md").write_text(diagnostics_summary(metrics, results), encoding="utf-8")
    (out_dir / "BASIS_AUDIT.md").write_text(basis_audit(results), encoding="utf-8")
    rows = [result_to_row(r) for r in results]
    (out_dir / "posterior_rows.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
