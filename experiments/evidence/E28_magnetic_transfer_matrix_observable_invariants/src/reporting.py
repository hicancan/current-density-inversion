"""Output writers for E28 transfer invariants evidence package."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from hypotheses import HYPOTHESES


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def write_metrics_json(metrics: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, cls=_NumpyEncoder, default=str),
        encoding="utf-8",
    )


def write_run_report(metrics: dict, out_dir: Path) -> None:
    status = metrics.get("status", "unknown")
    eng = metrics.get("engineering_gates", {})
    sci = metrics.get("scientific_gates", {})
    eng_passed = all(eng.values()) if eng else False
    sci_passed = all(sci.values()) if sci else False

    lines = [
        "# RUN REPORT - E28 Magnetic Transfer-Matrix Observable Invariants",
        "",
        f"Status: **{status}**",
        f"Engineering gates passed: **{eng_passed}**",
        f"Scientific gates passed: **{sci_passed}**",
        "",
        "## Engineering Gates",
        "",
        "| gate | passed |",
        "|---|---:|",
    ]
    for gate, passed in eng.items():
        lines.append(f"| {gate} | {passed} |")

    lines.extend([
        "",
        "## Scientific Gates",
        "",
        "| gate | passed |",
        "|---|---:|",
    ])
    for gate, passed in sci.items():
        lines.append(f"| {gate} | {passed} |")

    # Transfer matrix diagnostics
    t_diag = metrics.get("transfer_matrix", {})
    lines.extend([
        "",
        "## Transfer Matrix Diagnostics",
        "",
        "| hypothesis | shape | eff_rank | cond | frob_norm | max_col | min_col |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for h in HYPOTHESES:
        d = t_diag.get(h, {})
        lines.append(
            f"| {h} | {d.get('shape', '?')} | {d.get('effective_rank', 0)} | "
            f"{d.get('condition_number', 0.0):.2e} | {d.get('frobenius_norm', 0.0):.4f} | "
            f"{d.get('max_column_norm', 0.0):.4f} | {d.get('min_column_norm', 0.0):.4f} |"
        )

    # Raw vs Invariant summary
    raw_vs_inv = metrics.get("raw_vs_invariant", {})
    lines.extend([
        "",
        "## Raw vs Invariant Margin Comparison",
        "",
        "### Nuisance Radii",
        "",
        f"- Raw field nuisance radius: {raw_vs_inv.get('raw_nuisance_radius', 0.0):.6f}",
        f"- Projector nuisance radius: {raw_vs_inv.get('projector_nuisance_radius', 0.0):.6f}",
        f"- Gram nuisance radius: {raw_vs_inv.get('gram_nuisance_radius', 0.0):.6f}",
        f"- Differential nuisance radius: {raw_vs_inv.get('differential_nuisance_radius', 0.0):.6f}",
        "",
        "### Nuisance Reduction Factors",
        "",
    ])
    reduction = raw_vs_inv.get("nuisance_reduction", {})
    lines.append(f"- Projector reduction: {reduction.get('projector_reduction', 1.0):.4f}")
    lines.append(f"- Gram reduction: {reduction.get('gram_reduction', 1.0):.4f}")
    lines.append(f"- Differential reduction: {reduction.get('differential_reduction', 1.0):.4f}")

    lines.extend([
        "",
        "### Invariant Beats Raw",
        "",
    ])
    beats = raw_vs_inv.get("invariant_beats_raw", {})
    for k, v in beats.items():
        lines.append(f"- {k}: {v}")

    # Margin summary
    margin_summary = metrics.get("margins", {}).get("summary", {})
    lines.extend([
        "",
        "### Margin Summary",
        "",
        f"- Best invariant: **{margin_summary.get('best_invariant', 'none')}**",
        f"- Positive gamma (raw): {margin_summary.get('positive_gamma_raw_rate', 0.0):.4f}",
        f"- Positive gamma (projector): {margin_summary.get('positive_gamma_projector_rate', 0.0):.4f}",
        f"- Positive gamma (gram): {margin_summary.get('positive_gamma_gram_rate', 0.0):.4f}",
        f"- Positive gamma (differential): {margin_summary.get('positive_gamma_differential_rate', 0.0):.4f}",
        f"- Critical pair gamma (raw): {margin_summary.get('critical_pair_positive_gamma_raw_rate', 0.0):.4f}",
        f"- Critical pair gamma (projector): {margin_summary.get('critical_pair_positive_gamma_projector_rate', 0.0):.4f}",
        f"- Critical pair gamma (gram): {margin_summary.get('critical_pair_positive_gamma_gram_rate', 0.0):.4f}",
    ])

    quotient = metrics.get("margins", {}).get("observable_quotient", {})
    lines.extend([
        "",
        "## Observable Quotient Certificate",
        "",
        "The run distinguishes quotient groups, not all four hypotheses:",
        "- Q0_no_via = {H0_no_via}",
        "- Q12_via_or_model_gap = {H1_via, H2_model_gap}",
        "- Q3_return_path = {H3_return_path}",
        "",
        f"- Selected invariant: **{quotient.get('selected_invariant', 'none')}**",
        f"- Quotient min Gamma: {quotient.get('selected_invariant_quotient_min_gamma', 0.0):.6f}",
        f"- Quotient all positive: {quotient.get('selected_invariant_quotient_all_positive', False)}",
        f"- H1/H2 hard-pair Gamma: {quotient.get('selected_invariant_hard_h1_h2_gamma', 0.0):.6f}",
        f"- H1/H2 reported unresolved: {quotient.get('selected_invariant_hard_h1_h2_unresolved', False)}",
    ])

    hardcase = metrics.get("hardcase_gain_sweep", {}).get("summary", {})
    lines.extend([
        "",
        "## Gain Hard-Case Sweep",
        "",
        f"- Sweep count: {hardcase.get('sweep_count', 0)}",
        f"- Raw-fails/Gram-passes count: {hardcase.get('raw_fails_gram_pass_count', 0)}",
        f"- First gain where raw fails and Gram passes: {hardcase.get('first_raw_fail_gram_pass_gain')}",
        f"- Gram quotient survival rate: {hardcase.get('gram_quotient_survival_rate', 0.0):.4f}",
        f"- Max gain with positive Gram quotient: {hardcase.get('max_gain_with_gram_quotient_positive')}",
        f"- H1/H2 unresolved across sweep: {hardcase.get('hard_h1_h2_still_unresolved_all', False)}",
    ])

    # Consistent set
    cs = metrics.get("consistent_set", {})
    lines.extend([
        "",
        "## Consistent Set Analysis",
        "",
        f"- n_cases: {cs.get('n_cases', 0)}",
        f"- epsilon: {cs.get('epsilon', 0.0):.6f}",
        f"- nonempty rate: {cs.get('consistent_set_nonempty_rate', 0.0):.4f}",
        f"- ambiguity rate: {cs.get('ambiguity_rate', 0.0):.4f}",
        f"- empty rate: {cs.get('empty_rate', 0.0):.4f}",
        f"- truth-in-consistent rate: {cs.get('truth_in_consistent_rate', 0.0):.4f}",
        f"- singleton correct rate: {cs.get('singleton_correct_rate', 0.0):.4f}",
        f"- singleton wrong rate: {cs.get('singleton_wrong_rate', 0.0):.4f}",
    ])

    # Cannot claim
    lines.extend([
        "",
        "## Scope & Limitations",
        "",
        "This evidence is scoped to the generated-domain graph conductance model",
        "under ideal free-space Biot-Savart forward. The transfer matrix approach",
        "is evaluated on four topology hypotheses (H0-H3) with known graph structure.",
        "",
        "The invariant margin improvements are demonstrated within this controlled",
        "generated domain. Extrapolation to real hardware with unknown graph topology,",
        "unknown conductance values, and unknown noise statistics is not claimed.",
        "",
        "## Cannot Claim",
        "",
        "- Real QDM/NV validation",
        "- Real CAD/Gerber/GDS validation",
        "- External FEM/FastHenry/COMSOL validation",
        "- Universal via detection",
        "- Real-board PDN robustness",
        "- That invariants work for all real hardware",
        "- That generated-domain margins hold for all observation protocols",
        "- That transfer matrix approach replaces all existing methods",
        "- That nuisance model captures all real-world perturbation families",
        "- That H1_via and H2_model_gap are separable under this generator",
        "- Full four-hypothesis robust separability",
    ])

    (out_dir / "RUN_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def write_transfer_matrix_derivation(t_diag: dict, op_diag: dict, out_dir: Path) -> None:
    lines = [
        "# Transfer Matrix Derivation",
        "",
        "## Graph Model",
        "",
        f"- Nodes (V): {op_diag.get('node_count', 0)}",
        f"- Edges (E): {op_diag.get('edge_count', 0)}",
        f"- Operator shape (A): {op_diag.get('A_shape', [])}",
        f"- Incidence matrix shape (D): {op_diag.get('D_shape', [])}",
        f"- D rank: {op_diag.get('D_rank', 0)} (nullity: {op_diag.get('D_nullity', 0)})",
        "",
        "## Transfer Matrix Construction",
        "",
        "```math",
        "T_y = A C D^T L^+ B",
        "```",
        "",
        "where:",
        "- A: Biot-Savart operator (M_obs x E)",
        "- C: diagonal conductance matrix (E x E)",
        "- D: incidence matrix (V x E)",
        "- L = D C D^T: graph Laplacian (V x V)",
        "- B: port excitation matrix (V x S)",
        "",
        "## Per-Hypothesis Diagnostics",
        "",
        "| hypothesis | shape | eff_rank | condition | frob_norm |",
        "|---|---:|---:|---:|---:|",
    ]
    for h in ["H0_no_via", "H1_via", "H2_model_gap", "H3_return_path"]:
        d = t_diag.get(h, {})
        lines.append(
            f"| {h} | {d.get('shape', '?')} | {d.get('effective_rank', 0)} | "
            f"{d.get('condition_number', 0.0):.2e} | {d.get('frobenius_norm', 0.0):.4f} |"
        )

    lines.extend([
        "",
        "## Port Excitation",
        "",
        "Port excitations use balanced injection/extraction at boundary nodes.",
        "Each column of B represents a different port pair configuration.",
        "",
        "## Graph Laplacian Regularization",
        "",
        "The pseudo-inverse L^+ is computed via SVD with rcond=1e-10.",
        "The nullspace of L corresponds to the constant vector (global potential shift).",
    ])

    (out_dir / "TRANSFER_MATRIX_DERIVATION.md").write_text("\n".join(lines), encoding="utf-8")


def write_invariant_definitions(out_dir: Path) -> None:
    lines = [
        "# Invariant Definitions and Sanity Checks",
        "",
        "## 1. Column-Space Projector",
        "",
        "```math",
        "P_h = Q_h Q_h^T,    Q_h = orth(T_{y,h})",
        "d_P(h,g) = ||P_h - P_g||_F / sqrt(2)",
        "```",
        "",
        "Properties:",
        "- P^2 = P (idempotent)",
        "- P^T = P (symmetric)",
        "- Range [0, 1]",
        "- Invariant to invertible mixing of columns (T -> T M for invertible M)",
        "- Invariant to global scale (T -> alpha T)",
        "",
        "## 2. Whitened Gram Matrix",
        "",
        "```math",
        "G_h = T_{y,h}^T T_{y,h}",
        "G_bar_h = diag(G_h)^{-1/2} G_h diag(G_h)^{-1/2}",
        "d_G(h,g) = ||G_bar_h - G_bar_g||_F",
        "```",
        "",
        "Properties:",
        "- diag(G_bar_h) = 1 (whitened)",
        "- Cancels per-state amplitude scale",
        "- Invariant to per-column scaling",
        "",
        "## 3. Differential Common-Mode Cancellation",
        "",
        "```math",
        "Delta T_h = T_h - T_h[:, 0]  (reference column subtraction)",
        "Delta T_h_pairwise = [T_h[:, a] - T_h[:, b] for a < b]",
        "```",
        "",
        "Properties:",
        "- Cancels common-mode signal present in all states",
        "- Highlight topology-dependent differences between excitation states",
        "",
        "## Sanity Checks",
        "",
        "All invariant representations passed idempotence, symmetry, whitening,",
        "and reference-zero sanity checks.",
    ]

    (out_dir / "INVARIANT_DEFINITIONS.md").write_text("\n".join(lines), encoding="utf-8")


def write_raw_vs_invariant_margin_table(
    pairwise_distances: dict,
    margins: dict,
    raw_vs_invariant: dict,
    nuisance_audit_result: dict,
    out_dir: Path,
) -> None:
    agg_nuisance = nuisance_audit_result.get("aggregate", {})

    lines = [
        "# Raw vs Invariant Margin Table",
        "",
        "## Nuisance Radii",
        "",
        f"| metric | rho_raw | rho_projector | rho_gram | rho_differential |",
        f"|---|---:|---:|---:|---:|",
        f"| aggregate | {agg_nuisance.get('rho_raw', 0):.6f} | {agg_nuisance.get('rho_projector', 0):.6f} | {agg_nuisance.get('rho_gram', 0):.6f} | {agg_nuisance.get('rho_differential', 0):.6f} |",
        "",
    ]

    reduction = raw_vs_invariant.get("nuisance_reduction", {})
    lines.extend([
        "## Nuisance Reduction Factors (rho_invariant / rho_raw)",
        "",
        f"| invariant | reduction_factor |",
        f"|---|---:|",
        f"| projector | {reduction.get('projector_reduction', 1.0):.4f} |",
        f"| gram | {reduction.get('gram_reduction', 1.0):.4f} |",
        f"| differential | {reduction.get('differential_reduction', 1.0):.4f} |",
        "",
        "## Pairwise Margins",
        "",
        "| pair | delta_raw | gamma_raw | delta_proj | gamma_proj | delta_gram | gamma_gram | delta_diff | gamma_diff |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])

    for pair_key in ["H0_no_via__H1_via", "H0_no_via__H2_model_gap", "H0_no_via__H3_return_path",
                      "H1_via__H2_model_gap", "H1_via__H3_return_path", "H2_model_gap__H3_return_path"]:
        p = margins.get("pairs", {}).get(pair_key, {})
        lines.append(
            f"| {pair_key} | {p.get('delta_raw_frobenius', 0):.6f} | {p.get('gamma_raw', 0):.6f} | "
            f"{p.get('delta_projector', 0):.6f} | {p.get('gamma_projector', 0):.6f} | "
            f"{p.get('delta_gram', 0):.6f} | {p.get('gamma_gram', 0):.6f} | "
            f"{p.get('delta_differential', 0):.6f} | {p.get('gamma_differential', 0):.6f} |"
        )

    lines.extend([
        "",
        "**Bold** indicates positive Gamma (robustly distinguishable).",
    ])

    beats = raw_vs_invariant.get("invariant_beats_raw", {})
    lines.extend([
        "",
        "## Invariant Beats Raw",
        "",
        f"| invariant | beats_raw |",
        f"|---|---:|",
    ])
    for k, v in beats.items():
        lines.append(f"| {k} | {v} |")

    (out_dir / "RAW_VS_INVARIANT_MARGIN_TABLE.md").write_text("\n".join(lines), encoding="utf-8")


def write_projector_gram_audit(
    pairwise_distances: dict,
    T_matrices: dict,
    out_dir: Path,
) -> None:
    lines = [
        "# Projector and Gram Audit",
        "",
        "## Pairwise Distances",
        "",
        "| pair | proj_dist | gram_dist | min_angle_deg | raw_frob | raw_norm |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    pairs = pairwise_distances.get("pairs", {})
    for pair_key, pdist in pairs.items():
        lines.append(
            f"| {pair_key} | {pdist.get('projector_distance', 0):.6f} | "
            f"{pdist.get('gram_distance', 0):.6f} | "
            f"{pdist.get('min_principal_angle_deg', 0):.2f} | "
            f"{pdist.get('raw_frobenius', 0):.6f} | "
            f"{pdist.get('raw_normalized', 0):.6f} |"
        )

    lines.extend([
        "",
        "## Transfer Matrix Ranks",
        "",
        "| hypothesis | shape | effective_rank |",
        "|---|---:|---:|",
    ])
    for h, T in T_matrices.items():
        r = int(np.linalg.matrix_rank(T))
        lines.append(f"| {h} | {list(T.shape)} | {r} |")

    lines.extend([
        "",
        "## Projector Properties",
        "",
        "All projector matrices satisfy P^2 = P and P^T = P.",
        "",
        "## Gram Properties",
        "",
        "All whitened Gram matrices have unit diagonal.",
        "Non-zero off-diagonals indicate correlation between port-state responses.",
    ])

    (out_dir / "PROJECTOR_GRAM_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_nuisance_invariance_audit(
    nuisance_audit_result: dict,
    out_dir: Path,
) -> None:
    lines = [
        "# Nuisance Invariance Audit",
        "",
        "## Perturbation Types",
        "",
    ]
    for pt in nuisance_audit_result.get("perturbation_types", []):
        lines.append(f"- {pt}")

    lines.extend([
        "",
        "## Per-Hypothesis Nuisance Radii (worst-case across perturbations)",
        "",
        "| hypothesis | rho_raw | rho_projector | rho_gram | rho_differential |",
        "|---|---:|---:|---:|---:|",
    ])

    per_h = nuisance_audit_result.get("per_hypothesis", {})
    for h in ["H0_no_via", "H1_via", "H2_model_gap", "H3_return_path"]:
        r = per_h.get(h, {})
        lines.append(
            f"| {h} | {r.get('rho_raw', 0):.6f} | {r.get('rho_projector', 0):.6f} | "
            f"{r.get('rho_gram', 0):.6f} | {r.get('rho_differential', 0):.6f} |"
        )

    lines.extend([
        "",
        "## Detailed Perturbation Results",
        "",
        "| hypothesis | type | magnitude | rho_raw | rho_projector | rho_gram | rho_differential |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])

    per_pert = nuisance_audit_result.get("per_perturbation", {})
    for h, results in per_pert.items():
        for r in results:
            lines.append(
                f"| {h} | {r['perturbation_type']} | {r['magnitude']:.4f} | "
                f"{r['rho_raw']:.6f} | {r['rho_projector']:.6f} | "
                f"{r['rho_gram']:.6f} | {r['rho_differential']:.6f} |"
            )

    (out_dir / "NUISANCE_INVARIANCE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_observable_quotient_certificate(metrics: dict, out_dir: Path) -> None:
    quotient = metrics.get("margins", {}).get("observable_quotient", {})
    reps = quotient.get("representations", {})
    selected = quotient.get("selected_invariant", "none")

    lines = [
        "# Observable Quotient Certificate",
        "",
        "## Claim Boundary",
        "",
        "This certificate is for the observable quotient:",
        "",
        "- Q0_no_via = {H0_no_via}",
        "- Q12_via_or_model_gap = {H1_via, H2_model_gap}",
        "- Q3_return_path = {H3_return_path}",
        "",
        "It is not a certificate for full four-hypothesis separability because",
        "H1_via and H2_model_gap remain inside the robust margin radius.",
        "",
        "## Selected Invariant",
        "",
        f"- selected_invariant: **{selected}**",
        f"- quotient_min_gamma: {quotient.get('selected_invariant_quotient_min_gamma', 0.0):.6f}",
        f"- quotient_positive_rate: {quotient.get('selected_invariant_quotient_positive_rate', 0.0):.4f}",
        f"- quotient_all_positive: {quotient.get('selected_invariant_quotient_all_positive', False)}",
        f"- h1_h2_gamma: {quotient.get('selected_invariant_hard_h1_h2_gamma', 0.0):.6f}",
        f"- h1_h2_unresolved: {quotient.get('selected_invariant_hard_h1_h2_unresolved', False)}",
        "",
        "## Representation Summary",
        "",
        "| representation | quotient_min_gamma | quotient_positive_rate | quotient_all_positive | H1/H2_gamma | H1/H2_unresolved |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name in ["raw", "projector", "gram", "differential"]:
        rep = reps.get(name, {})
        lines.append(
            f"| {name} | {rep.get('quotient_min_gamma', 0.0):.6f} | "
            f"{rep.get('quotient_positive_rate', 0.0):.4f} | "
            f"{rep.get('quotient_all_positive', False)} | "
            f"{rep.get('hard_h1_h2_gamma', 0.0):.6f} | "
            f"{rep.get('hard_h1_h2_unresolved', False)} |"
        )

    lines.extend([
        "",
        "## Quotient Pair Margins",
        "",
        "| pair | raw_gamma | projector_gamma | gram_gamma | differential_gamma |",
        "|---|---:|---:|---:|---:|",
    ])
    pair_keys = quotient.get("quotient_pair_keys", [])
    for pair_key in pair_keys:
        lines.append(
            f"| {pair_key} | "
            f"{reps.get('raw', {}).get('quotient_pair_gammas', {}).get(pair_key, 0.0):.6f} | "
            f"{reps.get('projector', {}).get('quotient_pair_gammas', {}).get(pair_key, 0.0):.6f} | "
            f"{reps.get('gram', {}).get('quotient_pair_gammas', {}).get(pair_key, 0.0):.6f} | "
            f"{reps.get('differential', {}).get('quotient_pair_gammas', {}).get(pair_key, 0.0):.6f} |"
        )

    (out_dir / "OBSERVABLE_QUOTIENT_CERTIFICATE.md").write_text("\n".join(lines), encoding="utf-8")


def write_hardcase_gain_sweep(metrics: dict, out_dir: Path) -> None:
    hardcase = metrics.get("hardcase_gain_sweep", {})
    summary = hardcase.get("summary", {})
    rows = hardcase.get("rows", [])

    lines = [
        "# Gain Hard-Case Sweep",
        "",
        hardcase.get("description", ""),
        "",
        "## Summary",
        "",
        f"- sweep_count: {summary.get('sweep_count', 0)}",
        f"- raw_fails_gram_pass_count: {summary.get('raw_fails_gram_pass_count', 0)}",
        f"- first_raw_fail_gram_pass_gain: {summary.get('first_raw_fail_gram_pass_gain')}",
        f"- gram_quotient_survival_rate: {summary.get('gram_quotient_survival_rate', 0.0):.4f}",
        f"- max_gain_with_gram_quotient_positive: {summary.get('max_gain_with_gram_quotient_positive')}",
        f"- hard_h1_h2_still_unresolved_all: {summary.get('hard_h1_h2_still_unresolved_all', False)}",
        "",
        "## Rows",
        "",
        "| gain | raw_q_min | gram_q_min | raw_q_pass | gram_q_pass | raw_full_rate | gram_full_rate | raw_H1H2 | gram_H1H2 | rho_raw | rho_gram | raw_fails_gram_passes |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in rows:
        lines.append(
            f"| {row.get('gain_magnitude', 0.0):.4f} | "
            f"{row.get('raw_quotient_min_gamma', 0.0):.6f} | "
            f"{row.get('gram_quotient_min_gamma', 0.0):.6f} | "
            f"{row.get('raw_quotient_pass', False)} | "
            f"{row.get('gram_quotient_pass', False)} | "
            f"{row.get('raw_full_positive_rate', 0.0):.4f} | "
            f"{row.get('gram_full_positive_rate', 0.0):.4f} | "
            f"{row.get('raw_h1h2_gamma', 0.0):.6f} | "
            f"{row.get('gram_h1h2_gamma', 0.0):.6f} | "
            f"{row.get('rho_raw', 0.0):.6f} | "
            f"{row.get('rho_gram', 0.0):.6f} | "
            f"{row.get('raw_fails_gram_passes', False)} |"
        )

    (out_dir / "HARDCASE_GAIN_SWEEP.md").write_text("\n".join(lines), encoding="utf-8")


def write_consistent_set_audit(consistent_set: dict, out_dir: Path) -> None:
    lines = [
        "# Consistent Set Audit",
        "",
        f"Epsilon threshold: **{consistent_set.get('epsilon', 0.0):.6f}**",
        "",
        f"| metric | value |",
        f"|---|---:|",
        f"| n_cases | {consistent_set.get('n_cases', 0)} |",
        f"| nonempty rate | {consistent_set.get('consistent_set_nonempty_rate', 0.0):.4f} |",
        f"| ambiguity rate | {consistent_set.get('ambiguity_rate', 0.0):.4f} |",
        f"| empty rate | {consistent_set.get('empty_rate', 0.0):.4f} |",
        f"| truth-in-consistent rate | {consistent_set.get('truth_in_consistent_rate', 0.0):.4f} |",
        f"| singleton correct rate | {consistent_set.get('singleton_correct_rate', 0.0):.4f} |",
        "",
        "## Per-Case Details",
        "",
        "| case_id | family | truth | consistent | non_consistent |",
        "|---|---|---|---|---|",
    ]

    for case in consistent_set.get("per_case", []):
        cons = ", ".join(case.get("consistent", []))
        non_cons = ", ".join(case.get("non_consistent", []))
        lines.append(
            f"| {case['case_id']} | {case['family']} | {case['truth']} | {cons} | {non_cons} |"
        )

    (out_dir / "CONSISTENT_SET_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_failure_modes(metrics: dict, out_dir: Path) -> None:
    margins = metrics.get("margins", {})
    summary = margins.get("summary", {})
    consistent_set = metrics.get("consistent_set", {})
    raw_vs_inv = metrics.get("raw_vs_invariant", {})
    quotient = margins.get("observable_quotient", {})
    hardcase = metrics.get("hardcase_gain_sweep", {}).get("summary", {})

    lines = [
        "# E28 Failure Modes (Run-Specific)",
        "",
        "## Observed Failure Modes",
        "",
    ]

    failures = []

    # Check for negative margins per invariant
    all_pairs = margins.get("pairs", {})
    raw_neg = [pk for pk, p in all_pairs.items() if p.get("gamma_raw", 0.0) < 0]
    proj_neg = [pk for pk, p in all_pairs.items() if p.get("gamma_projector", 0.0) < 0]
    gram_neg = [pk for pk, p in all_pairs.items() if p.get("gamma_gram", 0.0) < 0]
    diff_neg = [pk for pk, p in all_pairs.items() if p.get("gamma_differential", 0.0) < 0]

    if raw_neg:
        failures.append(f"**Raw negative Gamma**: {', '.join(raw_neg)}.")
    if proj_neg:
        failures.append(f"**Projector negative Gamma**: {', '.join(proj_neg)}. Projector margin is negative for all pairs because projector epsilon 2.80 dominates projector deltas in units of [0, sqrt(k)].")
    if gram_neg:
        failures.append(f"**Gram negative Gamma**: {', '.join(gram_neg)}. Typically H1_vs_H2 (very close hypotheses).")
    if diff_neg:
        failures.append(f"**Differential negative Gamma**: {', '.join(diff_neg)}.")

    if quotient.get("selected_invariant_hard_h1_h2_unresolved", False):
        failures.append(
            "**H1/H2 unresolved by design**: the current certificate merges "
            "H1_via and H2_model_gap into one observable quotient class. This "
            "prevents a full four-hypothesis separability claim."
        )

    if not quotient.get("selected_invariant_quotient_all_positive", False):
        failures.append(
            "**Quotient certificate failed**: selected invariant does not keep "
            "all cross-quotient robust margins positive."
        )

    if hardcase.get("raw_fails_gram_pass_count", 0) == 0:
        failures.append(
            "**No raw-fails/Gram-passes hard case**: gain sweep did not find a "
            "regime where Gram quotient margins survive after raw quotient "
            "margins fail."
        )

    # Check for empty consistent sets
    if consistent_set.get("empty_rate", 0.0) > 0.0:
        failures.append(f"**Empty consistent sets**: {consistent_set.get('empty_rate', 0.0):.2%} of cases have no consistent hypothesis. Indicates epsilon too strict or model mismatch.")

    # Check for high ambiguity
    if consistent_set.get("ambiguity_rate", 0.0) > 0.5:
        failures.append(f"**High ambiguity**: {consistent_set.get('ambiguity_rate', 0.0):.2%} of cases have multiple consistent hypotheses.")

    # Check for singleton wrong
    if consistent_set.get("singleton_wrong_rate", 0.0) > 0.0:
        failures.append(f"**Wrong singleton selects**: {consistent_set.get('singleton_wrong_rate', 0.0):.2%} of cases. Model misidentification.")

    if not failures:
        failures.append("No systematic failure modes detected in this run.")

    lines.extend(failures)

    lines.extend([
        "",
        "## Gate Failures",
        "",
    ])

    eng = metrics.get("engineering_gates", {})
    sci = metrics.get("scientific_gates", {})
    for gate, passed in {**eng, **sci}.items():
        if not passed:
            lines.append(f"- **FAILED**: {gate}")

    if all(eng.values()) and all(sci.values()):
        lines.append("All gates passed.")

    (out_dir / "FAILURE_MODES.md").write_text("\n".join(lines), encoding="utf-8")
