"""Report generation for E25 evidence package.

Writes all required output files in outputs/.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from datetime import datetime, timezone


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_metrics_json(
    output_dir: Path,
    gates: dict,
    metadata: dict | None = None,
) -> None:
    """Write outputs/metrics.json with acceptance gates."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "evidence_id": "E25_calibrated_volume_forward_rho_tightening",
        "claim_id": "C04_inverse_crime_and_operator_gap",
        "secondary_claims": ["C10_pdn_kcl_distribution_need", "C13_calibration_protocol_reality"],
        "status": "partial",
        "acceptance_gates": gates,
        "cannot_claim": [
            "All results are generated-domain only; no real QDM/NV sensor data is used.",
            "No external solver (PyPEEC, FastHenry, COMSOL) is used for cross-validation.",
            "Volume quadrature is numerical; no analytic volume integral for rectangular prisms is implemented.",
            "Multifilament approximation uses uniform filament spacing; no adaptive refinement.",
            "Nuisance Jacobian uses first-order finite differences; higher-order effects are not quantified.",
            "No real CAD/GDS layouts are used; all geometries are canonical generated families.",
        ],
        "generated_at": _now_iso(),
    }
    if metadata:
        payload.update(metadata)
    (output_dir / "metrics.json").write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )


def write_rho_calibration_table(
    output_dir: Path,
    rows: list[dict],
) -> None:
    """Write outputs/rho_calibration_table.json."""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "rho_calibration_table.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )


def write_operator_error_budget(
    output_dir: Path,
    rho_decompositions: dict,
    nuisance_results: dict,
    comparison_results: dict,
) -> None:
    """Write outputs/operator_error_budget.json."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "evidence_id": "E25_calibrated_volume_forward_rho_tightening",
        "generated_at": _now_iso(),
        "rho_decomposition_by_family": {
            k: {
                "components": {ck: {
                    "absolute_radius": cv["absolute_radius"],
                    "relative_radius": cv["relative_radius"],
                } for ck, cv in v.get("components", {}).items()},
                "signal_scale": v.get("signal_scale", 0),
            }
            for k, v in rho_decompositions.items()
            if "error" not in v
        },
        "nuisance_jacobian_radii": {
            k: {
                "absolute_radius": v["absolute_radius"],
                "relative_radius": v["relative_radius"],
                "bound": v.get("bound"),
            }
            for k, v in nuisance_results.items()
        },
        "comparison_summary": {
            family: {
                "operator_frobenius": comp.get("operator_frobenius_relative_error", {}),
                "rho_current_family": comp.get("rho_by_current_family", {}),
            }
            for family, comp in comparison_results.items()
        },
    }
    (output_dir / "operator_error_budget.json").write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )


def write_run_report(
    output_dir: Path,
    context: dict,
) -> None:
    """Write outputs/RUN_REPORT.md."""
    lines = [
        "# E25 RUN REPORT",
        "",
        f"Generated: {_now_iso()}",
        "",
        "## Execution Summary",
        "",
        f"- Config: {context.get('config', 'unknown')}",
        f"- Smoke mode: {context.get('smoke', False)}",
        f"- Families tested: {context.get('families_tested', 0)}",
        f"- Quadrature levels tested: {context.get('quadrature_levels', 0)}",
        "",
    ]

    gates = context.get("gates", {})
    lines.append("## Acceptance Gates")
    lines.append("")
    for gate_name, gate_val in gates.items():
        icon = "PASS" if gate_val else "FAIL"
        lines.append(f"- **{gate_name}**: {icon}")
    lines.append("")

    lines.append("## Quadrature Convergence")
    qc = context.get("quadrature_convergence", {})
    lines.append(f"- Best relative change: {qc.get('best_relative_change', 'N/A')}")
    lines.append(f"- Median relative change: {qc.get('median_relative_change', 'N/A')}")
    lines.append(f"- Gate (<=0.05): {'PASS' if qc.get('passed') else 'FAIL'}")
    lines.append("")

    lines.append("## Dominant Rho Source")
    lines.append(f"- {context.get('dominant_rho_source', 'N/A')}")
    lines.append("")

    lines.append("## Cannot Claim")
    for cc in context.get("cannot_claim", []):
        lines.append(f"- {cc}")
    lines.append("")

    lines.append("## Next Required Evidence")
    lines.append("- E24/E26: integrate calibrated rho into robust Gamma certificates")
    lines.append("- External solver cross-validation (PyPEEC, FastHenry)")
    lines.append("- Real CAD/GDS layout import")
    lines.append("")

    (output_dir / "RUN_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def write_volume_forward_derivation(
    output_dir: Path,
) -> None:
    """Write outputs/VOLUME_FORWARD_DERIVATION.md."""
    text = """# Volume Forward Derivation

## Continuous Model

For a conductor volume V_e with uniform current density J_e = (i_e / a_e) * t_e:

    B_e(r_m) = mu0/(4*pi) * int_{V_e} [J_e x (r_m - r')] / |r_m - r'|^3  dr'

## Discretization

The volume integral is factorized as:

1. **Along-segment integral** (0 to L): Gauss-Legendre quadrature, order n_seg.
2. **Cross-section integral** (width x thickness): Tensor-product Gauss-Legendre, orders n_w x n_t.

Total quadrature points per conductor: n_seg * n_w * n_t.

## Forward Matrix

    A^{vol}_{m,e} = mu0/(4*pi*a_e) * int_{V_e} [t_e x (r_m - r')] / |r_m - r'|^3  dr'

Each column is computed with unit current (i_e = 1 A) for linearity.

## Convergence

Convergence is verified by doubling all quadrature orders:

    ||A_Q - A_{{2Q}}||_F / ||A_{{2Q}}||_F  <=  0.05

The 0.05 threshold is the E25 scientific gate.
"""
    (output_dir / "VOLUME_FORWARD_DERIVATION.md").write_text(text, encoding="utf-8")


def write_quadrature_convergence_audit(
    output_dir: Path,
    convergence_results: list[dict],
    gate_result: dict,
) -> None:
    """Write outputs/QUADRATURE_CONVERGENCE_AUDIT.md."""
    lines = [
        "# Quadrature Convergence Audit",
        "",
        "## Gate Result",
        "",
        f"- Gate: ||A_Q - A_{{2Q}}||_F / ||A_{{2Q}}||_F <= 0.05",
        f"- Passed: {gate_result.get('passed', False)}",
        f"- Best relative change: {gate_result.get('best_relative_change', 'N/A'):.6e}",
        f"- Worst relative change: {gate_result.get('worst_relative_change', 'N/A'):.6e}",
        f"- Median relative change: {gate_result.get('median_relative_change', 'N/A'):.6e}",
        f"- Levels tested: {gate_result.get('num_levels_tested', 0)}",
        "",
        "## Convergence Table",
        "",
        "| Family | n_seg | n_w | n_t | Rel Change | Frobenius(A_Q) | Frobenius(A_2Q) |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in convergence_results:
        lines.append(
            f"| {r.get('family', '?')} | {r.get('n_seg', '?')} | {r.get('n_w', '?')} "
            f"| {r.get('n_t', '?')} | {r.get('relative_change', 0):.6e} "
            f"| {r.get('frob_AQ', 0):.6e} | {r.get('frob_A2Q', 0):.6e} |"
        )
    lines.append("")
    (output_dir / "QUADRATURE_CONVERGENCE_AUDIT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_centerline_multifilament_volume_comparison(
    output_dir: Path,
    comparison_results: dict,
) -> None:
    """Write outputs/CENTERLINE_MULTIFILAMENT_VOLUME_COMPARISON.md."""
    lines = [
        "# Centerline vs Multifilament vs Volume Comparison",
        "",
        "## Per-Family Metrics",
        "",
    ]
    for family, comp in comparison_results.items():
        lines.append(f"### {family}")
        lines.append("")
        fc = comp.get("field_comparison", {})
        ofe = comp.get("operator_frobenius_relative_error", {})
        rho_cf = comp.get("rho_by_current_family", {})

        lines.append("| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |")
        lines.append("|---|---|---|---|---|---|---|")

        for pair_name in ["centerline_vs_volume", "multifilament_vs_volume", "centerline_vs_multifilament"]:
            fmetrics = fc.get(pair_name, {})
            om = ofe.get(pair_name, "N/A")
            rm = rho_cf.get(pair_name, {})
            lines.append(
                f"| {pair_name} | {fmetrics.get('rmse', 0):.4e} "
                f"| {fmetrics.get('relative_l2', 0):.4e} "
                f"| {fmetrics.get('max_component_error', 0):.4e} "
                f"| {om:.4e} "
                f"| {rm.get('absolute', 0):.4e} "
                f"| {rm.get('relative', 0):.4e} |"
            )
        lines.append("")
        lines.append(f"- Signal scale (||B_vol||_2): {comp.get('signal_scale', 'N/A'):.4e}")
        lines.append(f"- Current norm: {comp.get('current_norm', 'N/A'):.4e}")
        lines.append("")

    lines.append("## Key Finding")
    lines.append("")
    lines.append("Multifilament should substantially outperform centerline, confirming")
    lines.append("that finite-width effects are the dominant operator gap for traces.")
    lines.append("")
    (output_dir / "CENTERLINE_MULTIFILAMENT_VOLUME_COMPARISON.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_rho_decomposition_table(
    output_dir: Path,
    rho_decompositions: dict,
) -> None:
    """Write outputs/RHO_DECOMPOSITION_TABLE.md."""
    lines = [
        "# Rho Decomposition Table",
        "",
        "## Per-Family Decomposition",
        "",
    ]
    for family, decomp in rho_decompositions.items():
        if "error" in decomp:
            continue
        lines.append(f"### {family}")
        lines.append(f"- Signal scale: {decomp.get('signal_scale', 0):.4e}")
        lines.append(f"- Current samples: {decomp.get('sample_count', 0)}")
        lines.append("")
        lines.append("| Component | Absolute Rho | Relative Rho | Spectral Bound |")
        lines.append("|---|---|---|---|")
        for comp_key, comp in decomp.get("components", {}).items():
            lines.append(
                f"| {comp_key} | {comp['absolute_radius']:.4e} "
                f"| {comp['relative_radius']:.4e} "
                f"| {comp.get('spectral_bound', 'N/A')} |"
            )
        lines.append("")
    (output_dir / "RHO_DECOMPOSITION_TABLE.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_nuisance_jacobian_audit(
    output_dir: Path,
    nuisance_results: dict,
) -> None:
    """Write outputs/NUISANCE_JACOBIAN_RADIUS_AUDIT.md."""
    lines = [
        "# Nuisance Jacobian Radius Audit",
        "",
        "| Parameter | Abs Radius | Rel Radius | Bound | FD Step |",
        "|---|---|---|---|---|",
    ]
    for key, val in nuisance_results.items():
        lines.append(
            f"| {key} | {val.get('absolute_radius', 0):.4e} "
            f"| {val.get('relative_radius', 0):.4e} "
            f"| {val.get('bound', 'N/A')} "
            f"| {val.get('finite_difference_step', 'N/A')} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("Parameters with relative radius > 0.1 dominate the calibration budget.")
    lines.append("These must be bounded through external measurement or included in Gamma.")
    lines.append("")
    (output_dir / "NUISANCE_JACOBIAN_RADIUS_AUDIT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_gamma_rho_recommendation(
    output_dir: Path,
    dominant_source: str,
    recommended_rho: float,
    recommended_rho_rel: float,
    e23_verdict: str,
) -> None:
    """Write outputs/GAMMA_RHO_RECOMMENDATION.md."""
    lines = [
        "# Gamma Rho Recommendation",
        "",
        "## E23 Rho Assessment",
        "",
        f"- Verdict: {e23_verdict}",
        "",
        "## Recommended Rho for Future Gamma Certificates",
        "",
        f"- Recommended absolute rho: {recommended_rho:.4e}",
        f"- Recommended relative rho: {recommended_rho_rel:.4e}",
        f"- Dominant source: {dominant_source}",
        "",
        "## Usage",
        "",
        "Future rounds (E24, E26) should use these calibrated rho values as the",
        "operator perturbation term in the robust Gamma margin:",
        "",
        "    Gamma = delta - tau - epsilon - rho_h - rho_g",
        "",
        "The conservative (sum) estimate provides a safe upper bound.",
        "The RSS estimate is appropriate if nuisance sources are independent.",
        "",
        "## Rationale",
        "",
        "E25 decomposes rho into physically justified components with numerical",
        "convergence verification. This replaces the black-box E23 finite-width",
        "surrogate with calibrated, auditable operator radii.",
        "",
    ]
    (output_dir / "GAMMA_RHO_RECOMMENDATION.md").write_text(
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
        "Documented operator-boundary findings from E25.",
        "",
    ]
    for fm in failure_modes:
        lines.append(f"## {fm.get('name', 'Unknown')}")
        lines.append(f"- Severity: {fm.get('severity', 'unknown')}")
        lines.append(f"- Description: {fm.get('description', 'N/A')}")
        lines.append(f"- Gate status: {fm.get('gate_passed', 'N/A')}")
        lines.append("")
    (output_dir / "FAILURE_MODES.md").write_text("\n".join(lines), encoding="utf-8")
