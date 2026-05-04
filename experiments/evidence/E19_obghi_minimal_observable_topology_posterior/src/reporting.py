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


def gates_markdown(gates: dict[str, bool]) -> str:
    lines = ["# E19 Acceptance Gates", "", "| gate | passed |", "|---|---:|"]
    for k, v in gates.items():
        lines.append(f"| {k} | {bool(v)} |")
    lines.append("")
    lines.append(f"All gates passed: {all(gates.values())}")
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
    lines = [
        "# RUN REPORT - E19 OBGHI Minimal Observable Topology Posterior",
        "",
        "## Claim affected",
        "",
        "- Primary: `C10_pdn_kcl_distribution_need`",
        "- Secondary: `C06_graph_hypothesis_system_identification`, `C02_single_plane_identifiability_boundary`, `C04_inverse_crime_and_operator_gap`",
        "",
        "## Evidence added",
        "",
        "Generated-domain minimal OBGHI evidence package implementing posterior topology inference over H0/H1/H2/H3 explanations.",
        "",
        "## Metrics",
        "",
        f"- case_count: {metrics['obghi']['case_count']}",
        f"- OBGHI top1_accuracy: {_f(metrics['obghi']['top1_accuracy'])}",
        f"- OBGHI accepted_accuracy: {_f(metrics['obghi']['accepted_accuracy'])}",
        f"- OBGHI accepted_risk: {_f(metrics['obghi']['accepted_risk'])}",
        f"- OBGHI reject_rate: {_f(metrics['obghi']['reject_rate'])}",
        f"- OBGHI need_next_measurement_rate: {_f(metrics['obghi']['need_next_measurement_rate'])}",
        f"- OBGHI via_gap_ambiguous_reject_rate: {_f(metrics['obghi']['via_gap_ambiguous_reject_rate'])}",
        f"- Ridge-map top1_accuracy: {_f(baseline_metrics['top1_accuracy'])}",
        "",
        "## Operator diagnostics",
        "",
        f"- A shape: `{operator_diag['shape']}`",
        f"- via_columns_nonzero: `{operator_diag['via_columns_nonzero']}`",
        f"- via_column_norm_min: `{_f(operator_diag['via_column_norm_min'])}`",
        f"- via_column_norm_mean: `{_f(operator_diag['via_column_norm_mean'])}`",
        "",
        "## Acceptance gates",
        "",
        "| gate | passed |",
        "|---|---:|",
    ]
    for k, v in gates.items():
        lines.append(f"| {k} | {bool(v)} |")

    lines += [
        "",
        f"All gates passed: `{all(gates.values())}`",
        "",
        "## Failure modes",
        "",
        "See `FAILURE_CASES.md`. Expected first-slice failure modes include accepted wrong topology, correct topology rejected under ambiguity, and need-next-measurement decisions.",
        "",
        "## Claim status change",
        "",
        "None in this ZIP. Do not upgrade any claim until the package is run locally and audited.",
        "",
        "## Cannot claim",
        "",
        "- real QDM/NV validation",
        "- real CAD/Gerber/GDS validation",
        "- external FEM/FastHenry/COMSOL validation",
        "- real-board PDN/KCL robustness",
        "- mechanism-level explanation on real data",
        "- universal via detection",
        "",
        "## Next required evidence",
        "",
        "1. Run E19 locally and audit metrics.",
        "2. Compare E19 failure slices against E18 physics-constrained inverse failure cases.",
        "3. If E19 passes, register it in the research graph as generated-domain evidence only.",
        "4. Add a follow-up multi-height / multi-state OBGHI information-gain evidence package.",
        "",
        "## Tests run",
        "",
        "Not run by this ZIP generator. Run locally with `uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests`.",
        "",
        "## Files changed",
        "",
        "This package only adds files under `experiments/evidence/E19_obghi_minimal_observable_topology_posterior/` unless you manually apply research graph snippets.",
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
    (out_dir / "ACCEPTANCE_GATES.md").write_text(gates_markdown(gates), encoding="utf-8")
    (out_dir / "FAILURE_CASES.md").write_text(failure_cases(results), encoding="utf-8")
    (out_dir / "RUN_REPORT.md").write_text(run_report(metrics, gates, operator_diag, baseline_metrics), encoding="utf-8")
    rows = [result_to_row(r) for r in results]
    (out_dir / "posterior_rows.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
