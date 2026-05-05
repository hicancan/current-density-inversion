"""Output writers for E19.2 OQCI evidence package."""

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


def write_consistent_hypotheses(oqci_metrics: dict, out_dir: Path) -> None:
    lines = ["# Consistent Hypotheses", ""]
    lines.append("| case_id | truth | consistent_hypotheses | non_consistent |")
    lines.append("|---|---|---|---|")
    for row in oqci_metrics.get("per_case", []):
        consistent = ", ".join(row.get("consistent_hypotheses", []))
        non_consistent = ", ".join(row.get("non_consistent_hypotheses", []))
        lines.append(f"| {row['case_id']} | {row['truth']} | {consistent} | {non_consistent} |")
    (out_dir / "CONSISTENT_HYPOTHESES.md").write_text("\n".join(lines), encoding="utf-8")


def write_claim_intervals(interval_metrics: dict, out_dir: Path) -> None:
    lines = ["# Claim Intervals", ""]
    lines.append("| truth | claim | forced_false | forced_true | unidentifiable | count |")
    lines.append("|---|---:|---:|---:|---:|")
    matrix = interval_metrics.get("interval_matrix", {})
    for key in sorted(matrix.keys()):
        stats = matrix[key]
        if stats["count"] == 0:
            continue
        lines.append(
            f"| {stats['truth']} | {stats['claim']} | "
            f"{stats['forced_false']} | {stats['forced_true']} | "
            f"{stats['unidentifiable']} | {stats['count']} |"
        )
    lines.append("")
    lines.append(f"**Overall forced true rate**: {interval_metrics.get('overall_forced_true_rate', 0.0):.4f}")
    lines.append(f"**Overall unidentifiable rate**: {interval_metrics.get('overall_unidentifiable_rate', 0.0):.4f}")
    lines.append(f"**Overall mean width**: {interval_metrics.get('overall_mean_width', 0.0):.4f}")
    (out_dir / "CLAIM_INTERVALS.md").write_text("\n".join(lines), encoding="utf-8")


def write_pairwise_distances(dist_metrics: dict, epsilon: float, out_dir: Path) -> None:
    lines = ["# Pairwise Distinguishability Distances", ""]
    lines.append(f"Epsilon threshold: {epsilon:.4f}")
    lines.append("")
    lines.append("| pair | full_dist | extra_dist | angle_deg | dim_i | dim_j | distinguishable |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for pair_key, stats in dist_metrics.get("pairs", {}).items():
        ed = stats.get("extra_distance", stats.get("distance", 0))
        d = ed > epsilon
        lines.append(
            f"| {pair_key} | {stats.get('full_distance', stats.get('distance', 0)):.6f} | "
            f"{ed:.6f} | {stats['principal_angle_deg']:.2f} | "
            f"{stats['dim_i']} | {stats['dim_j']} | {'yes' if d else 'no'} |"
        )
    (out_dir / "PAIRWISE_DISTANCES.md").write_text("\n".join(lines), encoding="utf-8")


def write_near_null_modes(nullspace_metrics: dict, out_dir: Path) -> None:
    lines = ["# Near-Null Modes", ""]
    lines.append(f"Effective rank: {nullspace_metrics.get('effective_rank', 0)}")
    lines.append(f"Near-null count: {nullspace_metrics.get('near_null_count', 0)}")
    lines.append(f"Total rank: {nullspace_metrics.get('total_rank', 0)}")
    lines.append(f"Threshold: {nullspace_metrics.get('threshold', 0.0)}")
    lines.append("")
    lines.append("| index | singular_value | ratio | current_norm | field_norm |")
    lines.append("|---|---:|---:|---:|---:|")
    for mode in nullspace_metrics.get("modes", [])[:20]:
        lines.append(
            f"| {mode['index']} | {mode['singular_value']:.6e} | "
            f"{mode['singular_value_ratio']:.6e} | "
            f"{mode['current_norm']:.4e} | {mode['field_norm']:.4e} |"
        )
    (out_dir / "NEAR_NULL_MODES.md").write_text("\n".join(lines), encoding="utf-8")


def write_resolution_audit(resolution_metrics: dict, out_dir: Path) -> None:
    lines = ["# Resolution Audit", ""]
    lines.append(f"Dimension: {resolution_metrics.get('dimension', 0)}")
    lines.append(f"Trace ratio: {resolution_metrics.get('trace_ratio', 0.0):.4f}")
    lines.append(f"Resolution rank: {resolution_metrics.get('resolution_rank', 0)}")
    lines.append(f"Resolution rank ratio: {resolution_metrics.get('resolution_rank_ratio', 0.0):.4f}")
    lines.append(f"Condition number: {resolution_metrics.get('condition_number', 0.0):.2e}")
    lines.append("")
    lines.append("## PSF sample")
    lines.append("| index | diagonal | total_energy | diagonal_ratio |")
    lines.append("|---|---:|---:|---:|")
    for psf in resolution_metrics.get("psf_sample", [])[:10]:
        lines.append(
            f"| {psf['index']} | {psf['diagonal']:.4f} | "
            f"{psf['total_energy']:.4f} | {psf['diagonal_ratio']:.4f} |"
        )
    (out_dir / "RESOLUTION_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_next_measurement(next_metrics: dict, out_dir: Path) -> None:
    lines = ["# Next Measurement Recommendations", ""]
    lines.append(f"Top recommendation: **{next_metrics.get('top_recommendation', 'none')}**")
    lines.append(f"Recommendation score: {next_metrics.get('recommendation_score', 0.0):.4f}")
    lines.append("")
    lines.append("| candidate | score | predicted_nn_reduction | predicted_rank_increase |")
    lines.append("|---|---:|---:|---:|")
    for rec in next_metrics.get("all_recommendations", []):
        nn = rec.get("predicted_near_null_reduction", "?")
        ri = rec.get("predicted_rank_increase", "?")
        lines.append(
            f"| {rec['candidate']} | {rec['score']:.4f} | {nn} | {ri} |"
        )
    (out_dir / "NEXT_MEASUREMENT.md").write_text("\n".join(lines), encoding="utf-8")


def write_adversarial_pairs(adversarial_metrics: dict, out_dir: Path) -> None:
    lines = ["# Adversarial Pairs", ""]
    lines.append("| pair_id | label_a | label_b | forward_distance | ambiguous |")
    lines.append("|---|---:|---|---:|")
    for pair in adversarial_metrics.get("pairs", []):
        amb = "yes" if pair["forward_distance"] < adversarial_metrics.get("epsilon", 1.0) else "no"
        lines.append(
            f"| {pair.get('pair_id', '?')} | {pair.get('label_a', '?')} | "
            f"{pair.get('label_b', '?')} | {pair.get('forward_distance', 0.0):.6f} | {amb} |"
        )
    (out_dir / "ADVERSARIAL_PAIRS.md").write_text("\n".join(lines), encoding="utf-8")


def write_run_report(metrics: dict, out_dir: Path) -> None:
    status = metrics.get("status", "unknown")
    eng = metrics.get("engineering_gates", {})
    sci = metrics.get("scientific_gates", {})
    eng_passed = all(eng.values()) if eng else False
    sci_passed = all(sci.values()) if sci else False

    lines = [
        "# RUN REPORT - E19.2 OQCI Identifiability Audit",
        "",
        f"Status: **{status}**",
        f"Engineering gates passed: **{eng_passed}**",
        f"Scientific gates passed: **{sci_passed}**",
        "",
        "## Engineering Gates",
        "",
        "| gate | passed |",
        "|---|---:|---:|",
    ]
    for gate, passed in eng.items():
        lines.append(f"| {gate} | {passed} |")

    lines.extend([
        "",
        "## Scientific Gates",
        "",
        "| gate | passed |",
        "|---|---:|---:|",
    ])
    for gate, passed in sci.items():
        lines.append(f"| {gate} | {passed} |")

    oqci = metrics.get("oqci", {})
    lines.extend([
        "",
        "## OQCI Metrics",
        "",
        f"- case_count: {oqci.get('case_count', 0)}",
        f"- epsilon: {oqci.get('epsilon_primary', 0.0):.4f}",
        f"- consistent_set_nonempty_rate: {oqci.get('consistent_set_nonempty_rate', 0.0):.4f}",
        f"- ambiguity_rate: {oqci.get('ambiguity_rate', 0.0):.4f}",
        f"- mean_interval_width: {oqci.get('mean_interval_width', 0.0):.4f}",
        f"- near_null_count: {oqci.get('near_null_count', 0)}",
        f"- effective_rank: {oqci.get('effective_rank', 0)}",
        "",
        "## Decision Distribution",
        "",
    ])
    for dt, cnt in oqci.get("decision_distribution", {}).items():
        lines.append(f"- {dt}: {cnt}")

    lines.extend([
        "",
        "## Cannot Claim",
        "",
        "- Real QDM/NV validation",
        "- Real CAD/Gerber/GDS validation",
        "- External FEM/FastHenry/COMSOL validation",
        "- Universal via detection",
        "- Real-board PDN robustness",
        "- That generated-domain ambiguity holds for all real hardware",
    ])

    (out_dir / "RUN_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
