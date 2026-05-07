"""Report generation for E29 evidence package.

Writes all required output files per the E29 algorithm blueprint §6.
"""
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_metrics_json(
    output_dir: Path,
    gates: dict,
    aggregate_rates: dict,
    split_audit: dict,
    pairwise_rates: dict,
) -> None:
    """Write outputs/metrics.json."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "evidence_id": "E29_rho_integrated_schur_gamma_certificate",
        "claim_ids": [
            "C04_inverse_crime_and_operator_gap",
            "C06_graph_hypothesis_system_identification",
            "C10_pdn_kcl_distribution_need",
            "C13_calibration_protocol_reality",
        ],
        "status": "partial",
        "acceptance_gates": gates,
        "aggregate_rates": aggregate_rates,
        "calibration_evaluation_split": split_audit,
        "pairwise_rates": pairwise_rates,
        "cannot_claim": [
            "All results are generated-domain only; no real QDM/NV sensor data is used.",
            "No external solver (PyPEEC, FastHenry, COMSOL) is used for cross-validation.",
            "Schur defect signatures are synthetic and not validated against E27 edge-Schur artifacts.",
            "Rho estimates are locally computed (E25 artifacts not available in E29 worktree); marked as local generated calibration.",
            "Operator matrices use simplified geometry (canonical straight segments); no CAD/GDS import.",
            "No real via/return diagnosis; all defects are synthetic perturbations on generated geometries.",
            "Calibration/evaluation split is geometric (defect-based), not layout-family-based.",
            "Pairwise certificate uses shared rho; per-defect rho not available without E27 artifacts.",
        ],
        "generated_at": _now_iso(),
    }
    (output_dir / "metrics.json").write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )


def write_run_report(
    output_dir: Path,
    context: dict,
) -> None:
    """Write outputs/RUN_REPORT.md."""
    gates = context.get("gates", {})
    rates = context.get("aggregate_rates", {})
    rho = context.get("rho_components", {})
    split_info = context.get("split_audit", {})
    pairwise_r = context.get("pairwise_rates", {})
    e23_e24_analysis = context.get("e23_e24_impact", "")

    lines = [
        "# E29 RUN REPORT",
        "",
        f"Generated: {_now_iso()}",
        "",
        "## Execution Summary",
        "",
        f"- Config: {context.get('config', 'unknown')}",
        f"- Smoke mode: {context.get('smoke', False)}",
        f"- Calibration defects: {split_info.get('calibration_count', 0)}",
        f"- Evaluation defects: {split_info.get('evaluation_count', 0)}",
        "",
        "## Rho Sources and Split Discipline",
        "",
    ]

    rho_comp = rho.get("components", {})
    for key, comp in rho_comp.items():
        lines.append(
            f"- **{comp['name']}**: abs={comp['absolute_radius']:.4e}, "
            f"rel={comp['relative_radius']:.4e} [{comp.get('calibration_status', 'N/A')}]"
        )
    lines.append("")
    lines.append(f"- Rho calibration note: {rho.get('calibration_note', 'N/A')}")
    lines.append(f"- Split discipline enforced: {split_info.get('discipline_enforced', False)}")
    lines.append(f"- Split violations: {split_info.get('violations', [])}")
    lines.append("")

    lines.append("## Acceptance Gates")
    lines.append("")
    lines.append("### Engineering Gates")
    for gate_name in sorted(gates):
        if gate_name.startswith("all_"):
            continue
        val = gates[gate_name]
        icon = "PASS" if val else "FAIL"
        lines.append(f"- **{gate_name}**: {icon}")
    lines.append("")
    lines.append(f"- **all_engineering_gates_passed**: {'PASS' if gates.get('all_engineering_gates_passed') else 'FAIL'}")
    lines.append(f"- **all_scientific_gates_passed**: {'PASS' if gates.get('all_scientific_gates_passed') else 'FAIL'}")
    lines.append(f"- **all_acceptance_gates_passed**: {'PASS' if gates.get('all_acceptance_gates_passed') else 'FAIL'}")
    lines.append("")

    lines.append("## Aggregate Rates")
    lines.append("")
    for key, val in rates.items():
        if isinstance(val, float):
            lines.append(f"- **{key}**: {val:.4f}")
        else:
            lines.append(f"- **{key}**: {val}")
    lines.append("")

    lines.append("## Pairwise Defect Certificate")
    lines.append("")
    for key, val in pairwise_r.items():
        if isinstance(val, float):
            lines.append(f"- **{key}**: {val:.4f}")
        else:
            lines.append(f"- **{key}**: {val}")
    lines.append("")

    lines.append("## E25 Rho Impact on E23/E24 Conclusions")
    lines.append("")
    lines.append(e23_e24_analysis)
    lines.append("")

    lines.append("## Failure Modes")
    failures = context.get("failure_modes", [])
    for fm in failures:
        lines.append(f"- **{fm['name']}** [{fm['severity']}]: {fm['description']}")
    lines.append("")

    lines.append("## Cannot Claim")
    for cc in context.get("cannot_claim", []):
        lines.append(f"- {cc}")
    lines.append("")

    lines.append("## Next Required Evidence")
    lines.append("- E27: Edge Schur signatures for real (non-synthetic) defect perturbations")
    lines.append("- External solver cross-validation (PyPEEC, FastHenry) for rho components")
    lines.append("- Real CAD/GDS layout import for defect-defect distinguishability")
    lines.append("- Layout-ensemble scaling (multiple layout families, not single geometry)")
    lines.append("- Real QDM/NV measurement for truth-containing consistent sets")
    lines.append("")

    (output_dir / "RUN_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def write_rho_input_audit(
    output_dir: Path,
    rho_components: dict,
    loaded_from_e25: bool,
) -> None:
    """Write outputs/RHO_INPUT_AUDIT.md."""
    comps = rho_components.get("components", {})
    lines = [
        "# Rho Input Audit",
        "",
        f"## Source: {'E25 artifacts' if loaded_from_e25 else 'Local generated calibration'}",
        "",
        f"- E: {rho_components.get('E', 'N/A')}",
        f"- P: {rho_components.get('P', 'N/A')}",
        f"- Signal scale: {rho_components.get('signal_scale', 0):.4e}",
        "",
        "## Component Breakdown",
        "",
        "| Component | Absolute Rho | Relative Rho | Status |",
        "|---|---|---|---|",
    ]
    for key, comp in comps.items():
        lines.append(
            f"| {comp['name']} | {comp['absolute_radius']:.4e} "
            f"| {comp['relative_radius']:.4e} "
            f"| {comp.get('calibration_status', 'N/A')} |"
        )
    lines.append("")
    lines.append("## Conservative vs RSS")
    cons = comps.get("rho_combined_conservative", {})
    rss = comps.get("rho_combined_rss", {})
    lines.append(f"- Conservative (sum): {cons.get('absolute_radius', 0):.4e}")
    lines.append(f"- RSS: {rss.get('absolute_radius', 0):.4e}")
    lines.append(f"- Ratio RSS/Conservative: {rss.get('absolute_radius', 0) / max(cons.get('absolute_radius', 1), 1e-30):.4f}")
    lines.append("")

    if not loaded_from_e25:
        lines.append("## Local Calibration Note")
        lines.append("")
        lines.append(
            "E25 artifacts (rho_calibration_table.json, operator_error_budget.json) "
            "were not available in the E29 worktree. Rho estimates are locally "
            "computed following E25 methodology with volume quadrature vs centerline "
            "comparison. This is marked as local generated calibration per §1 of "
            "the E29 blueprint."
        )
        lines.append("")

    (output_dir / "RHO_INPUT_AUDIT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_gamma_ablation_table(
    output_dir: Path,
    gamma_results: list[dict],
    aggregate_rates: dict,
) -> None:
    """Write outputs/GAMMA_ABLATION_TABLE.md."""
    lines = [
        "# Gamma Ablation Table",
        "",
        "## Ablation Variants",
        "",
        "Each defect is evaluated under 5 Gamma definitions:",
        "",
        "1. **no_rho**: Gamma = S - epsilon - tau (no operator penalty)",
        "2. **rss_rho**: Gamma = S - epsilon - tau - rho_rss",
        "3. **conservative_rho**: Gamma = S - epsilon - tau - rho_cons (sum)",
        "4. **e23_old_rho**: Gamma = S - epsilon - tau - rho_e23_old",
        "5. **e25_calibrated**: Gamma = S - epsilon - tau - rho_e25 (same as conservative)",
        "",
        "Conservative gamma governs claims per §3 of the E29 blueprint.",
        "",
        "## Aggregate Rates",
        "",
    ]
    for key, val in aggregate_rates.items():
        if isinstance(val, float):
            lines.append(f"- **{key}**: {val:.4f}")
        else:
            lines.append(f"- **{key}**: {val}")
    lines.append("")

    lines.append("## Per-Defect Gamma Table")
    lines.append("")
    lines.append(
        "| Defect ID | Type | S | G_no_rho | G_rss | G_cons | G_e23_old | G_e25 | "
        "cons_pass | rss_pass |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for g in gamma_results:
        lines.append(
            f"| {g['defect_id']} | {g['defect_type']} "
            f"| {g['schur_signal']:.4e} "
            f"| {g['gamma_no_rho']:+.4e} "
            f"| {g['gamma_rss_rho']:+.4e} "
            f"| {g['gamma_conservative_rho']:+.4e} "
            f"| {g['gamma_e23_old_rho']:+.4e} "
            f"| {g['gamma_e25_calibrated_rho']:+.4e} "
            f"| {'YES' if g['conservative_pass'] else 'NO'} "
            f"| {'YES' if g['rss_pass'] else 'NO'} |"
        )
    lines.append("")

    (output_dir / "GAMMA_ABLATION_TABLE.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_conservative_gamma_certificate(
    output_dir: Path,
    gamma_results: list[dict],
    aggregate_rates: dict,
    gates: dict,
) -> None:
    """Write outputs/CONSERVATIVE_GAMMA_CERTIFICATE.md."""
    n_total = len(gamma_results)
    n_pass = sum(1 for g in gamma_results if g.get("conservative_pass", False))
    rate = aggregate_rates.get("positive_conservative_rho_rate", 0.0)

    lines = [
        "# Conservative Gamma Certificate",
        "",
        f"## Result: {n_pass}/{n_total} defects pass (rate={rate:.4f})",
        "",
        "## Definition",
        "",
        "```math",
        "Gamma^{cons}_q = S_q - epsilon - tau - rho^{cons}_q",
        "```",
        "",
        "where rho^{cons} is the sum of all independently bounded operator-radius",
        "components (finite width, height, registration, layer z, background).",
        "",
        "## Decision Rule",
        "",
        "Accept defect q only if Gamma^{cons}_q > 0.",
        "",
        "Otherwise refuse: insufficient robust magnetic information.",
        "",
        "## Gate Status",
        "",
        f"- positive_conservative_gamma_rate >= 0.30: "
        f"{'PASS' if rate >= 0.30 else 'FAIL'} (rate={rate:.4f})",
        f"- truth_in_consistent_set_rate >= 0.90: "
        f"{'PASS' if aggregate_rates.get('truth_missing_rate', 1) <= 0.10 else 'FAIL'}",
        f"- wrong_accept_rate <= 0.10: "
        f"{'PASS' if aggregate_rates.get('wrong_accept_rate_conservative', 1) <= 0.10 else 'FAIL'}",
        f"- empty_rate <= 0.10: "
        f"{'PASS' if aggregate_rates.get('empty_rate', 1) <= 0.10 else 'FAIL'}",
        "",
        "## Overall",
        "",
        f"- Certificate: {'GRANTED' if gates.get('all_scientific_gates_passed') else 'NOT GRANTED'}",
        "",
    ]
    (output_dir / "CONSERVATIVE_GAMMA_CERTIFICATE.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_rss_gamma_upper_bound(
    output_dir: Path,
    gamma_results: list[dict],
    aggregate_rates: dict,
) -> None:
    """Write outputs/RSS_GAMMA_UPPER_BOUND.md."""
    n_total = len(gamma_results)
    n_pass = sum(1 for g in gamma_results if g.get("rss_pass", False))
    rate = aggregate_rates.get("positive_rss_rho_rate", 0.0)

    lines = [
        "# RSS Gamma Upper Bound",
        "",
        f"## Result: {n_pass}/{n_total} defects pass (rate={rate:.4f})",
        "",
        "## Definition",
        "",
        "```math",
        "Gamma^{rss}_q = S_q - epsilon - tau - rho^{rss}_q",
        "```",
        "",
        "where rho^{rss} = sqrt(sum_j rho_{q,j}^2) assumes independent nuisance sources.",
        "",
        "## Status",
        "",
        "This is an UPPER BOUND on Gamma. Claims MUST be governed by the",
        "conservative (sum) estimate per §3 of the E29 blueprint.",
        "",
        "If conservative gates fail but RSS gates pass, report as promising",
        "but not claim-supporting per §5 of the E29 blueprint.",
        "",
        "## Gate Status",
        "",
        f"- positive_rss_gamma_rate >= 0.50: "
        f"{'PASS' if rate >= 0.50 else 'FAIL'} (rate={rate:.4f})",
        f"- Negative rho impact on gamma (cons - rss): "
        f"{aggregate_rates.get('positive_conservative_rho_rate', 0) - rate:+.4f}",
        "",
    ]
    (output_dir / "RSS_GAMMA_UPPER_BOUND.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_pairwise_defect_certificate(
    output_dir: Path,
    pairwise_results: list[dict],
    pairwise_rates: dict,
) -> None:
    """Write outputs/PAIRWISE_DEFECT_CERTIFICATE.md."""
    n_total = pairwise_rates.get("pairwise_count", 0)
    n_pass = pairwise_rates.get("pairwise_conservative_pass_count", 0)
    rate = pairwise_rates.get("pairwise_conservative_gamma_rate", 0.0)

    lines = [
        "# Pairwise Defect Certificate",
        "",
        f"## Result: {n_pass}/{n_total} pairs distinguishable (rate={rate:.4f})",
        "",
        "## Definition",
        "",
        "```math",
        "Gamma^{cons}_{qr} = ||Delta Y_q - Delta Y_r|| - epsilon - tau - rho_q - rho_r",
        "```",
        "",
        "A pair (q, r) is distinguishable only if Gamma^{cons}_{qr} > 0.",
        "",
        "## Gate Status",
        "",
        f"- pairwise_conservative_gamma_rate >= 0.20: "
        f"{'PASS' if rate >= 0.20 else 'FAIL'} (rate={rate:.4f})",
        "",
        "## Per-Pair Details",
        "",
        "| Defect Q | Defect R | Delta_max | Gamma_cons | Pass |",
        "|---|---|---|---|---|",
    ]
    for p in pairwise_results[:50]:  # Cap at 50 rows
        lines.append(
            f"| {p['defect_q']} | {p['defect_r']} "
            f"| {p['pairwise_delta_max']:.4e} "
            f"| {p['gamma_conservative']:+.4e} "
            f"| {'YES' if p['conservative_pass'] else 'NO'} |"
        )
    if len(pairwise_results) > 50:
        lines.append(f"| ... | ... | ... | ... | ... |")
        lines.append(f"| ({len(pairwise_results) - 50} more rows omitted) |")
    lines.append("")

    (output_dir / "PAIRWISE_DEFECT_CERTIFICATE.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_calibration_evaluation_split_audit(
    output_dir: Path,
    split_info: dict,
    split_audit: dict,
) -> None:
    """Write outputs/CALIBRATION_EVALUATION_SPLIT_AUDIT.md."""
    lines = [
        "# Calibration/Evaluation Split Audit",
        "",
        "## Split Configuration",
        "",
        f"- Calibration fraction: {split_info.get('calibration_fraction', 0):.2f}",
        f"- Seed: {split_info.get('seed', 'N/A')}",
        "",
        "## Split Sizes",
        "",
        f"- Calibration defects: {split_audit.get('calibration_count', 0)}",
        f"- Evaluation defects: {split_audit.get('evaluation_count', 0)}",
        f"- Total: {split_audit.get('total_count', 0)}",
        "",
        "## Discipline Enforcement",
        "",
        f"- Discipline enforced: {split_audit.get('discipline_enforced', False)}",
        f"- Violations: {split_audit.get('violations', ['none'])}",
        "",
        "## Defect Type Coverage",
        "",
        f"- Calibration types: {split_audit.get('calibration_defect_types', [])}",
        f"- Evaluation types: {split_audit.get('evaluation_defect_types', [])}",
        f"- Types missing from calibration: {split_audit.get('types_missing_from_calibration', [])}",
        f"- Types missing from evaluation: {split_audit.get('types_missing_from_evaluation', [])}",
        "",
        "## Rules",
        "",
        "- epsilon and tau are computed exclusively from calibration geometries.",
        "- Evaluation geometries report rates only.",
        "- No threshold is chosen from evaluation rows.",
        "",
    ]
    (output_dir / "CALIBRATION_EVALUATION_SPLIT_AUDIT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_failure_modes(
    output_dir: Path,
    failure_modes: list[dict],
) -> None:
    """Write outputs/FAILURE_MODES.md."""
    lines = [
        "# Failure Modes",
        "",
        "Documented operator-boundary findings from E29.",
        "",
    ]
    for fm in failure_modes:
        lines.append(f"## {fm.get('name', 'Unknown')}")
        lines.append(f"- Severity: {fm.get('severity', 'unknown')}")
        lines.append(f"- Description: {fm.get('description', 'N/A')}")
        lines.append(f"- Gate passed: {fm.get('gate_passed', 'N/A')}")
        lines.append("")
    (output_dir / "FAILURE_MODES.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
