"""Output writers for E20 Active OQCI evidence package (round 2)."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)): return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
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
        "# RUN REPORT - E20 Active OQCI Measurement Design (Round 2)",
        "",
        f"Status: **{status}**",
        f"Engineering gates passed: **{eng_passed}**",
        f"Scientific gates passed: **{sci_passed}**",
        "",
        "## Engineering Gates", "", "| gate | passed |", "|---|---|",
    ]
    for gate, passed in eng.items():
        lines.append(f"| {gate} | {passed} |")

    lines.extend(["", "## Scientific Gates", "", "| gate | passed |", "|---|---|"])
    for gate, passed in sci.items():
        lines.append(f"| {gate} | {passed} |")

    lines.extend([
        "", "## Summary Metrics", "",
        f"- case_count: {metrics.get('case_count', 0)}",
        f"- candidate_count: {metrics.get('candidate_count', 0)}",
        f"- baseline_ambiguity_rate: {metrics.get('baseline_ambiguity_rate', 0.0):.4f}",
        f"- baseline_mean_interval_width: {metrics.get('baseline_mean_interval_width', 0.0):.4f}",
        f"- baseline_near_null_count: {metrics.get('baseline_near_null_count', 0)}",
        f"- baseline_effective_rank: {metrics.get('baseline_effective_rank', 0)}",
        f"- best_candidate: {metrics.get('best_candidate', 'none')}",
        f"- runtime_s: {metrics.get('run_audit', {}).get('runtime_s', 0.0):.1f}",
        "",
        "## Best Candidate by Epsilon",
        "",
        "| epsilon_mult | best_candidate |",
        "|---|---:|",
    ])
    for eps_str, info in sorted(metrics.get("best_by_epsilon", {}).items()):
        lines.append(f"| {eps_str} | {info.get('candidate_id', '?')} |")
    lines.extend([
        "",
        "## Scope & Limitations",
        "",
        "Generated-domain OQCI with epsilon sweep, multi-height, multi-component,",
        "and multi-state excitation candidates. No real QDM/NV, CAD/GDS, or",
        "external solver validation.",
        "",
        "## Cannot Claim",
        "",
        "- real QDM/NV validation",
        "- real CAD/GDS validation",
        "- hardware feasibility of active measurement",
        "- universal multilayer recovery",
        "- that generated multi-height improvements transfer to real devices",
        "- that no improvement means all physical measurement protocols are useless",
    ])
    (out_dir / "RUN_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def write_candidate_ranking(ranking: dict, out_dir: Path) -> None:
    lines = [
        "# Candidate Measurement Ranking (Robust Utility)", "",
        f"Best global candidate: **{ranking.get('best_global', 'none')}**",
        f"Best utility: {ranking.get('best_utility', 0.0):.6f}",
        f"Candidates evaluated: {ranking.get('candidate_count', 0)}",
        f"Any improved over baseline: {ranking.get('any_improved', False)}",
        "",
        "| rank | candidate | height_um | components | n_states | utility |",
        "|---|---:|---:|---:|---:|",
    ]
    for i, entry in enumerate(ranking.get("ranking", [])):
        lines.append(
            f"| {i + 1} | {entry['candidate_id']} | {entry['height_um']:.1f} | "
            f"{', '.join(entry.get('components', []))} | {entry.get('n_states', 1)} | "
            f"{entry['utility']:.6f} |"
        )
    lines.append("")

    # Per-epsilon utility detail for each candidate
    for entry in ranking.get("ranking", []):
        det = entry.get("utility_detail", {})
        per_eps = det.get("per_epsilon_utilities", {})
        per_widths = det.get("per_epsilon_interval_widths", {})
        lines.extend([
            f"## {entry['candidate_id']} (states={entry.get('n_states', 1)})",
            "", "| epsilon | utility | interval_width |",
            "|---|---:|---:|",
        ])
        for eps_str in sorted(per_eps.keys(), key=float):
            lines.append(
                f"| {eps_str} | {per_eps[eps_str]:.6f} | "
                f"{per_widths.get(eps_str, 0.0):.4f} |"
            )
        lines.append(f"\n**Robust utility (median): {entry['utility']:.6f}**\n")
    (out_dir / "CANDIDATE_RANKING.md").write_text("\n".join(lines), encoding="utf-8")


def write_epsilon_sweep(candidate_results: list[dict], out_dir: Path) -> None:
    """Write EPSILON_SWEEP.md: summary of epsilon sensitivity across all candidates."""
    # Collect all epsilon multipliers
    all_eps = set()
    for cr in candidate_results:
        for eps_r in cr.get("epsilon_sweep", []):
            all_eps.add(eps_r["epsilon_multiplier"])
    eps_sorted = sorted(all_eps)

    lines = [
        "# Epsilon Sensitivity Sweep", "",
        "## Per-Epsilon Summary (across all candidates)", "",
        "| epsilon_mult | epsilon | min_ambiguity_rate | max_nonempty_rate | min_empty_rate |",
        "|---|---:|---:|---:|---:|",
    ]
    for eps_mult in eps_sorted:
        eps_val = None
        amb_rates = []; nonempty_rates = []; empty_rates = []
        for cr in candidate_results:
            for eps_r in cr.get("epsilon_sweep", []):
                if abs(eps_r["epsilon_multiplier"] - eps_mult) < 1e-9:
                    eps_val = eps_r["epsilon"]
                    amb_rates.append(eps_r["ambiguity_rate"])
                    nonempty_rates.append(eps_r["nonempty_rate"])
                    empty_rates.append(eps_r["empty_rate"])
        lines.append(
            f"| {eps_mult:.1f} | {eps_val:.4f} | {min(amb_rates):.4f} | "
            f"{max(nonempty_rates):.4f} | {min(empty_rates):.4f} |"
        )
    lines.append("")

    # Best candidate per epsilon (by interval width)
    lines.extend([
        "## Best Candidate by Epsilon (lowest interval width)", "",
        "| epsilon_mult | best_candidate | interval_width | ambiguity_rate | wrong_accept |",
        "|---|---:|---:|---:|---:|",
    ])
    for eps_mult in eps_sorted:
        best_cid = None; best_width = 2.0; best_amb = 2.0; best_wrong = 999
        for cr in candidate_results:
            for eps_r in cr.get("epsilon_sweep", []):
                if abs(eps_r["epsilon_multiplier"] - eps_mult) < 1e-9:
                    if eps_r["mean_interval_width"] < best_width:
                        best_width = eps_r["mean_interval_width"]
                        best_cid = cr["candidate_id"]
                        best_amb = eps_r["ambiguity_rate"]
                        best_wrong = eps_r["wrong_accept_count"]
        lines.append(
            f"| {eps_mult:.1f} | {best_cid} | {best_width:.4f} | "
            f"{best_amb:.4f} | {best_wrong} |"
        )
    lines.append("")
    (out_dir / "EPSILON_SWEEP.md").write_text("\n".join(lines), encoding="utf-8")


def write_epsilon_candidate_matrix(candidate_results: list[dict], out_dir: Path) -> None:
    """Write EPSILON_CANDIDATE_MATRIX.md: full candidate x epsilon matrix."""
    all_eps = set()
    for cr in candidate_results:
        for eps_r in cr.get("epsilon_sweep", []):
            all_eps.add(eps_r["epsilon_multiplier"])
    eps_sorted = sorted(all_eps)

    lines = [
        "# Epsilon-Candidate Matrix", "",
        "Interval width for each candidate at each epsilon multiplier.",
        "",
    ]

    # Interval width matrix
    header = "| candidate | " + " | ".join(f"eps={e:.1f}" for e in eps_sorted) + " | min |"
    sep = "|---:|---:" * (len(eps_sorted) + 2) + "|"
    lines.append(header); lines.append(sep)
    for cr in candidate_results:
        widths = {}
        min_w = 1.0
        for eps_r in cr.get("epsilon_sweep", []):
            em = eps_r["epsilon_multiplier"]
            widths[em] = eps_r["mean_interval_width"]
            if eps_r["mean_interval_width"] < min_w:
                min_w = eps_r["mean_interval_width"]
        row = f"| {cr['candidate_id']} | " + " | ".join(f"{widths.get(e, 1.0):.4f}" for e in eps_sorted) + f" | {min_w:.4f} |"
        lines.append(row)
    lines.append("")

    # Ambiguity rate matrix
    lines.extend([
        "## Ambiguity Rate Matrix", "",
        "Ambiguity rate (fraction of cases with >1 consistent hypothesis).",
        "",
    ])
    header2 = "| candidate | " + " | ".join(f"eps={e:.1f}" for e in eps_sorted) + " | min |"
    lines.append(header2); lines.append(sep)
    for cr in candidate_results:
        rates = {}
        min_r = 1.0
        for eps_r in cr.get("epsilon_sweep", []):
            em = eps_r["epsilon_multiplier"]
            rates[em] = eps_r["ambiguity_rate"]
            if eps_r["ambiguity_rate"] < min_r:
                min_r = eps_r["ambiguity_rate"]
        row = f"| {cr['candidate_id']} | " + " | ".join(f"{rates.get(e, 1.0):.4f}" for e in eps_sorted) + f" | {min_r:.4f} |"
        lines.append(row)
    lines.append("")

    (out_dir / "EPSILON_CANDIDATE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")


def write_ambiguity_reduction(baseline_oqci: dict, ranking: dict, out_dir: Path) -> None:
    lines = [
        "# Ambiguity Reduction: Before/After", "",
        "## Baseline (single-height E0)", "",
        f"- ambiguity_rate: {baseline_oqci.get('ambiguity_rate', 0.0):.4f}",
        f"- mean_interval_width: {baseline_oqci.get('mean_interval_width', 0.0):.4f}",
        f"- wrong_accept_count: {baseline_oqci.get('wrong_high_confidence_accept_count', 0)}",
        "", "## Best Candidate", "",
    ]
    best = ranking.get("ranking", [{}])[0] if ranking.get("ranking") else {}
    lines.append(f"- candidate: {best.get('candidate_id', 'none')}")
    lines.append(f"- utility: {best.get('utility', 0.0):.6f}")

    per_widths = best.get("utility_detail", {}).get("per_epsilon_interval_widths", {})
    if per_widths:
        lines.append("")
        lines.append("| epsilon | interval_width |")
        lines.append("|---|---:|")
        for eps_str in sorted(per_widths.keys(), key=float):
            lines.append(f"| {eps_str} | {per_widths[eps_str]:.4f} |")
    lines.append("")
    (out_dir / "AMBIGUITY_REDUCTION.md").write_text("\n".join(lines), encoding="utf-8")


def write_claim_intervals_before_after(baseline_intervals: dict, candidate_results: list[dict], ranking: dict, out_dir: Path) -> None:
    lines = [
        "# Claim Intervals Before/After", "",
        "## Baseline (E0)", "",
        f"overall_forced_true_rate: {baseline_intervals.get('overall_forced_true_rate', 0.0):.4f}",
        f"overall_unidentifiable_rate: {baseline_intervals.get('overall_unidentifiable_rate', 0.0):.4f}",
        f"overall_mean_width: {baseline_intervals.get('overall_mean_width', 0.0):.4f}",
        "",
    ]
    if ranking.get("ranking"):
        best_id = ranking["ranking"][0]["candidate_id"]
        for cr in candidate_results:
            if cr["candidate_id"] == best_id:
                intervals = cr.get("intervals", {})
                lines.extend([
                    f"## Best Candidate ({best_id})", "",
                    f"overall_forced_true_rate: {intervals.get('overall_forced_true_rate', 0.0):.4f}",
                    f"overall_unidentifiable_rate: {intervals.get('overall_unidentifiable_rate', 0.0):.4f}",
                    f"overall_mean_width: {intervals.get('overall_mean_width', 0.0):.4f}",
                    "",
                ])
                break
    (out_dir / "CLAIM_INTERVALS_BEFORE_AFTER.md").write_text("\n".join(lines), encoding="utf-8")


def write_near_null_before_after(baseline_nullspace: dict, candidate_results: list[dict], ranking: dict, out_dir: Path) -> None:
    lines = [
        "# Near-Null Modes Before/After", "",
        "## Baseline (E0)", "",
        f"- near_null_count: {baseline_nullspace.get('near_null_count', 0)}",
        f"- effective_rank: {baseline_nullspace.get('effective_rank', 0)}",
        f"- total_rank: {baseline_nullspace.get('total_rank', 0)}",
        "", "## Per Candidate", "",
        "| candidate | near_null_count | effective_rank | total_rank |",
        "|---|---:|---:|---:|",
    ]
    for cr in candidate_results:
        ns = cr.get("nullspace", {})
        lines.append(
            f"| {cr['candidate_id']} | {ns.get('near_null_count', 0)} | "
            f"{ns.get('effective_rank', 0)} | {ns.get('total_rank', 0)} |"
        )
    lines.append("")
    (out_dir / "NEAR_NULL_BEFORE_AFTER.md").write_text("\n".join(lines), encoding="utf-8")


def write_next_measurement_policy(ranking: dict, out_dir: Path) -> None:
    if not ranking.get("ranking"):
        lines = ["# Next Measurement Policy", "", "No candidates evaluated."]
    else:
        best = ranking["ranking"][0]
        lines = [
            "# Next Measurement Policy", "",
            f"Recommended next measurement: **{best['candidate_id']}**",
            f"  - height: {best.get('height_um', 0.0):.1f} um",
            f"  - components: {', '.join(best.get('components', []))}",
            f"  - n_states: {best.get('n_states', 1)}",
            f"  - robust utility: {best['utility']:.6f}",
            "",
            "Best candidates by epsilon:",
            "",
        ]
        for eps_str, info in sorted(ranking.get("best_per_epsilon", {}).items()):
            lines.append(f"  - eps={eps_str}: {info['candidate_id']} (u={info['utility']:.6f})")
    (out_dir / "NEXT_MEASUREMENT_POLICY.md").write_text("\n".join(lines), encoding="utf-8")


def write_failure_modes(metrics: dict, ranking: dict, out_dir: Path) -> None:
    lines = [
        "# Failure Modes - E20 Active OQCI (Round 3)",
        "",
        "## Valid Disambiguation Utility <= 0",
        "",
    ]
    no_improve = [e for e in ranking.get("ranking", []) if e["utility"] <= 0]
    if no_improve:
        for e in no_improve:
            lines.append(f"- {e['candidate_id']}: utility_valid={e['utility']:.6f}")
    else:
        lines.append("(none — all candidates showed positive valid-disambiguation utility)")
    lines.extend([
        "",
        "## Breakthrough Gates",
        "",
    ])
    for gate, val in metrics.get("scientific_gates", {}).items():
        if gate.startswith(("valid_", "truth_", "singleton_", "empty_", "any_")):
            lines.append(f"- {gate}: **{val}**")

    lines.extend([
        "",
        "## Best Coverage Pair",
        "",
    ])
    bc = metrics.get("best_coverage", {})
    if bc:
        lines.append(f"- candidate: {bc.get('candidate_id', '?')} @ epsilon_mult={bc.get('epsilon_multiplier', 0.0):.1f}")
        lines.append(f"- valid_disambiguation_rate: {bc.get('valid_disambiguation_rate', 0.0):.4f}")
        lines.append(f"- singleton_correct: {bc.get('singleton_correct', 0)}/{bc.get('n_cases', 1)}")
        lines.append(f"- singleton_wrong: {bc.get('singleton_wrong', 0)}")
        lines.append(f"- empty_rate: {bc.get('empty_rate', 0.0):.4f}")
        lines.append(f"- truth_in_consistent_set_rate: {bc.get('truth_in_consistent_set_rate', 0.0):.4f}")
    else:
        lines.append("(no valid coverage pair found)")

    lines.extend([
        "",
        "## Cannot Claim Boundaries",
        "",
        "- This evidence is generated-domain only",
        "- No real QDM/NV, CAD/GDS, or external solver validation",
        "- Multi-height/multi-state improvement does not transfer to real devices",
        "- Hardware feasibility of active measurement is not assessed",
        "- Empty-set discrimination is not treated as disambiguation",
        "",
        "## Next Required Evidence",
        "",
        "- Validate candidate recommendations on real QDM/NV multi-height data",
        "- Cross-validate with external solver (COMSOL/FastHenry) held-out rows",
        "- Test with imported CAD/GDS graph families",
        "- If any candidate passes all 4 breakthrough gates, audit per-case at that epsilon",
        "",
    ])
    (out_dir / "FAILURE_MODES.md").write_text("\n".join(lines), encoding="utf-8")


# ── Round 3 new reports ────────────────────────────────────────────────────

def write_truth_coverage_audit(candidate_results: list[dict], out_dir: Path) -> None:
    """Write TRUTH_COVERAGE_AUDIT.md: per-candidate per-epsilon truth coverage."""

    # Find all epsilon multipliers
    all_eps = set()
    for cr in candidate_results:
        for eps_r in cr.get("epsilon_sweep", []):
            all_eps.add(eps_r["epsilon_multiplier"])
    eps_sorted = sorted(all_eps)

    lines = [
        "# Truth Coverage Audit",
        "",
        "Coverage metrics for each candidate at each epsilon multiplier.",
        "Valid disambiguation = consistent set is singleton AND equals truth hypothesis.",
        "",
    ]

    for cr in candidate_results:
        lines.extend([
            f"## {cr['candidate_id']} (h={cr['height_um']:.1f}, states={cr.get('n_states', 1)})",
            "",
            "| eps | empty | sing_correct | sing_wrong | multi | truth_in_set | vdr | acc |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for eps_r in cr.get("epsilon_sweep", []):
            em = eps_r.get("epsilon_multiplier", 0.0)
            lines.append(
                f"| {em:.1f} | {eps_r.get('empty_count', 0)} | "
                f"{eps_r.get('singleton_correct', 0)} | {eps_r.get('singleton_wrong', 0)} | "
                f"{eps_r.get('multi_count', 0)} | {eps_r.get('truth_in_set_count', 0)} | "
                f"{eps_r.get('valid_disambiguation_rate', 0.0):.4f} | "
                f"{eps_r.get('accepted_accuracy', 0.0):.4f} |"
            )
        lines.append("")

    (out_dir / "TRUTH_COVERAGE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_valid_disambiguation_matrix(candidate_results: list[dict], out_dir: Path) -> None:
    """Write VALID_DISAMBIGUATION_MATRIX.md: VDR matrix + best pair."""

    all_eps = set()
    for cr in candidate_results:
        for eps_r in cr.get("epsilon_sweep", []):
            all_eps.add(eps_r["epsilon_multiplier"])
    eps_sorted = sorted(all_eps)

    lines = [
        "# Valid Disambiguation Matrix",
        "",
        "Valid disambiguation rate (VDR) = fraction of cases where consistent set",
        "is a singleton AND that singleton equals truth.",
        "Higher is better. Empty sets score 0.",
        "",
        "| candidate | " + " | ".join(f"eps={e:.1f}" for e in eps_sorted) + " | best |",
        "|---:|---:" * (len(eps_sorted) + 2) + "|",
    ]
    best_overall = ("none", -1.0, 0.0)
    for cr in candidate_results:
        vdrs = {}
        best_vdr = -1.0; best_eps = 0.0
        for eps_r in cr.get("epsilon_sweep", []):
            em = eps_r["epsilon_multiplier"]
            vdr = eps_r.get("valid_disambiguation_rate", 0.0)
            vdrs[em] = vdr
            if vdr > best_vdr:
                best_vdr = vdr; best_eps = em
        row = f"| {cr['candidate_id']} | " + " | ".join(f"{vdrs.get(e, 0.0):.4f}" for e in eps_sorted) + f" | {best_vdr:.4f} |"
        lines.append(row)
        if best_vdr > best_overall[1]:
            best_overall = (cr["candidate_id"], best_vdr, best_eps)
    lines.append("")

    lines.extend([
        f"**Best overall**: {best_overall[0]} at epsilon={best_overall[2]:.1f} (VDR={best_overall[1]:.4f})",
        "",
    ])
    (out_dir / "VALID_DISAMBIGUATION_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")


def write_breakthrough_gate_audit(candidate_results: list[dict], metrics: dict, out_dir: Path) -> None:
    """Write BREAKTHROUGH_GATE_AUDIT.md: per-gate analysis."""
    sci = metrics.get("scientific_gates", {})
    all_four = sci.get("any_candidate_passes_all_four", False)
    bc = metrics.get("best_coverage", {})

    lines = [
        "# Breakthrough Gate Audit",
        "",
        f"All four breakthrough gates passed: **{all_four}**",
        "",
        "## Gate Requirements",
        "",
        "| gate | requirement | current best | passed |",
        "|---|---:|---:|",
    ]

    def _yn(v): return "yes" if v else "no"

    if bc:
        lines.append(f"| valid_disambiguation_rate >= 0.50 | >="
                     f" 0.50 | {bc.get('valid_disambiguation_rate', 0.0):.4f} | {_yn(sci.get('valid_disambiguation_rate_ge_0_50', False))} |")
        lines.append(f"| truth_in_consistent_set_rate >= 0.90 | >="
                     f" 0.90 | {bc.get('truth_in_consistent_set_rate', 0.0):.4f} | {_yn(sci.get('truth_in_consistent_set_rate_ge_0_90', False))} |")
        lines.append(f"| singleton_wrong_rate == 0 | ="
                     f" 0.00 | {bc.get('singleton_wrong_rate', 0.0):.4f} | {_yn(sci.get('singleton_wrong_rate_eq_0', False))} |")
        lines.append(f"| empty_rate <= 0.10 | <="
                     f" 0.10 | {bc.get('empty_rate', 0.0):.4f} | {_yn(sci.get('empty_rate_le_0_10', False))} |")
    else:
        for gate in ["valid_disambiguation_rate_ge_0_50", "truth_in_consistent_set_rate_ge_0_90",
                      "singleton_wrong_rate_eq_0", "empty_rate_le_0_10"]:
            lines.append(f"| {gate} | — | — | no |")

    lines.extend([
        "",
        "## Interpretation",
        "",
    ])
    if all_four:
        lines.append("BREAKTHROUGH: at least one (candidate, epsilon) pair passes all four gates.")
        lines.append("This constitutes generated-domain evidence that active OQCI measurement")
        lines.append("selection can produce valid, nonempty, singleton, truth-containing")
        lines.append("consistent sets.")
    else:
        lines.append("No (candidate, epsilon) pair passes all four breakthrough gates.")
        lines.append("The current generated-domain OQCI framework does not yet produce")
        lines.append("reliable valid disambiguation. The observed signal at tight epsilon")
        lines.append("is dominated by empty sets or singleton-wrong classifications.")
        lines.append("")
        lines.append("This is a stronger negative result: even with epsilon sweep and")
        lines.append("multi-state excitation, the generated basis family cannot produce")
        lines.append("valid disambiguation at a level meeting all breakthrough criteria.")
    lines.append("")
    (out_dir / "BREAKTHROUGH_GATE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


# ── Round 4 new reports ────────────────────────────────────────────────────

def write_regularized_consistent_set_audit(candidate_results: list[dict], out_dir: Path) -> None:
    """Write REGULARIZED_CONSISTENT_SET_AUDIT.md: per-candidate regularized sweep."""
    lines = [
        "# Regularized Consistent Set Audit",
        "",
        "Lambda sweep across fitting modes. Best per-mode selected by VDR.",
        "",
    ]
    for cr in candidate_results:
        rs = cr.get("regularized_sweep", {})
        fmr = rs.get("fit_mode_results", {})
        lines.extend([
            f"## {cr['candidate_id']}",
            "",
            "| fit_mode | lambda | VDR | ticr | SWR | ER | nonempty | acc |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for key, cov in sorted(fmr.items()):
            if key in ("ridge_best", "reduced_ridge_best"):
                continue
            lines.append(
                f"| {cov.get('fit_mode', key)} | {cov.get('lambda', 0.0):.0e} | "
                f"{cov.get('valid_disambiguation_rate', 0.0):.4f} | "
                f"{cov.get('truth_in_consistent_set_rate', 0.0):.4f} | "
                f"{cov.get('singleton_wrong_rate', 0.0):.4f} | "
                f"{cov.get('empty_rate', 0.0):.4f} | "
                f"{cov.get('nonempty_rate', 0.0):.4f} | "
                f"{cov.get('accepted_accuracy', 0.0):.4f} |"
            )
        # Summary
        ols = fmr.get("ols", {})
        br = fmr.get("ridge_best", {})
        brr = fmr.get("reduced_ridge_best", {})
        lines.extend([
            "",
            "**Summary**",
            f"- OLS VDR: {ols.get('valid_disambiguation_rate', 0.0):.4f}",
            f"- Best ridge VDR: {br.get('valid_disambiguation_rate', 0.0):.4f} (lambda={br.get('lambda', 0.0):.0e})",
            f"- Best reduced-ridge VDR: {brr.get('valid_disambiguation_rate', 0.0):.4f} (lambda={brr.get('lambda', 0.0):.0e})",
            f"- Regularization beats OLS: {cr.get('regularization_beats_ols', False)}",
            "",
        ])
    (out_dir / "REGULARIZED_CONSISTENT_SET_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_epsilon_calibration_audit(candidate_results: list[dict], out_dir: Path) -> None:
    """Write EPSILON_CALIBRATION_AUDIT.md: calibration split and evaluation."""
    lines = [
        "# Epsilon Calibration Audit",
        "",
        "Epsilon calibrated from truth residual quantiles on calibration split,",
        "evaluated on held-out evaluation split.",
        "",
    ]
    for cr in candidate_results:
        ce = cr.get("calibrated_evaluation", {})
        calib = ce.get("calibration", {})
        eval_results = ce.get("evaluation", {})

        lines.extend([
            f"## {cr['candidate_id']}",
            f"  - fit_mode: {calib.get('fit_mode', 'none')}",
            f"  - lambda: {calib.get('lambda', 0.0):.0e}",
            f"  - calibration cases: {ce.get('calibration_case_count', 0)}",
            f"  - evaluation cases: {ce.get('evaluation_case_count', 0)}",
            "",
            "### Calibration",
            "",
            f"  - truth_residual_mean: {calib.get('truth_residual_mean', 0.0):.4f}",
            f"  - truth_residual_median: {calib.get('truth_residual_median', 0.0):.4f}",
            "",
            "| quantile | epsilon | VDR | ticr | SWR | ER |",
            "|---|---:|---:|---:|---:|---:|",
        ])
        for q_key in sorted(eval_results.keys()):
            edata = eval_results[q_key]
            cd = calib.get(f"coverage_{q_key}", {})
            lines.append(
                f"| {q_key} | {edata.get('epsilon', 0.0):.4f} | "
                f"{cd.get('valid_disambiguation_rate', 0.0):.4f} | "
                f"{cd.get('truth_in_consistent_set_rate', 0.0):.4f} | "
                f"{cd.get('singleton_wrong_rate', 0.0):.4f} | "
                f"{cd.get('empty_rate', 0.0):.4f} |"
            )
        lines.extend([
            "",
            "### Evaluation",
            "",
            "| quantile | epsilon | VDR | ticr | SWR | ER |",
            "|---|---:|---:|---:|---:|---:|",
        ])
        for q_key in sorted(eval_results.keys()):
            edata = eval_results[q_key]
            lines.append(
                f"| {q_key} | {edata.get('epsilon', 0.0):.4f} | "
                f"{edata.get('valid_disambiguation_rate', 0.0):.4f} | "
                f"{edata.get('truth_in_consistent_set_rate', 0.0):.4f} | "
                f"{edata.get('singleton_wrong_rate', 0.0):.4f} | "
                f"{edata.get('empty_rate', 0.0):.4f} |"
            )
        lines.append("")
    (out_dir / "EPSILON_CALIBRATION_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_regularization_breakthrough_gate_audit(metrics: dict, candidate_results: list[dict], out_dir: Path) -> None:
    """Write REGULARIZATION_BREAKTHROUGH_GATE_AUDIT.md."""
    sci = metrics.get("scientific_gates", {})
    reg = metrics.get("best_regularized_coverage", {})

    lines = [
        "# Regularization Breakthrough Gate Audit",
        "",
        f"All regularized gates passed: **{sci.get('all_regularized_gates_pass', False)}**",
        "",
        "## Gate Requirements",
        "",
        "| gate | requirement | current | passed |",
        "|---|---:|---:|",
    ]

    def _yn(v): return "yes" if v else "no"

    lines.append(f"| regularized VDR >= 0.50 | >= 0.50 | "
                 f"{metrics.get('best_regularized_valid_disambiguation_rate', 0.0):.4f} | "
                 f"{_yn(sci.get('regularized_valid_disambiguation_rate_ge_0_50', False))} |")
    lines.append(f"| regularized ticr >= 0.90 | >= 0.90 | "
                 f"{metrics.get('best_regularized_truth_in_consistent_set_rate', 0.0):.4f} | "
                 f"{_yn(sci.get('regularized_truth_in_consistent_set_rate_ge_0_90', False))} |")
    lines.append(f"| regularized SWR == 0 | == 0.00 | "
                 f"{metrics.get('best_regularized_singleton_wrong_rate', 0.0):.4f} | "
                 f"{_yn(sci.get('regularized_singleton_wrong_rate_eq_0', False))} |")
    lines.append(f"| regularized ER <= 0.10 | <= 0.10 | "
                 f"{metrics.get('best_regularized_empty_rate', 0.0):.4f} | "
                 f"{_yn(sci.get('regularized_empty_rate_le_0_10', False))} |")
    lines.append(f"| regularization beats OLS by 0.20 | >= 0.20 | — | "
                 f"{_yn(sci.get('regularization_beats_ols_by_0_20', False))} |")

    lines.extend([
        "",
        "## Calibration Evaluation Gate",
        "",
        f"calibration_eval_vdr_nondegenerate (VDR > 0 on eval split): "
        f"**{sci.get('calibration_eval_vdr_nondegenerate', False)}**",
        "",
    ])

    # Best regularized details
    if reg:
        lines.extend([
            "## Best Regularized Coverage",
            "",
            f"- candidate: {reg.get('candidate_id', '?')}",
            f"- fit_mode: {reg.get('fit_mode', '?')}",
            f"- lambda: {reg.get('lambda', 0.0):.0e}",
            f"- VDR: {reg.get('valid_disambiguation_rate', 0.0):.4f}",
            f"- OLS VDR: {reg.get('ols_vdr', 0.0):.4f}",
            f"- ridge VDR: {reg.get('ridge_vdr', 0.0):.4f}",
            f"- reduced_ridge VDR: {reg.get('reduced_ridge_vdr', 0.0):.4f}",
            f"- regularization beats OLS: {reg.get('beats_ols', False)}",
            f"- singleton_wrong_rate: {reg.get('singleton_wrong_rate', 0.0):.4f}",
            f"- empty_rate: {reg.get('empty_rate', 0.0):.4f}",
            "",
        ])
    else:
        lines.extend(["", "No regularized coverage data available.", ""])

    lines.extend([
        "## Interpretation",
        "",
    ])
    if sci.get("all_regularized_gates_pass", False):
        lines.append("BREAKTHROUGH: regularized fitting passes all gates.")
    else:
        lines.append("Regularized fitting does not yet pass all breakthrough gates.")
    lines.append("")
    (out_dir / "REGULARIZATION_BREAKTHROUGH_GATE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


# ── Round 5 new reports ────────────────────────────────────────────────────

def write_pairwise_margin_matrix_report(baseline_margins: dict, candidate_results: list[dict], out_dir: Path) -> None:
    """Write PAIRWISE_MARGIN_MATRIX.md: before/after pairwise margins."""
    lines = [
        "# Pairwise Margin Matrix",
        "",
        "## Baseline (E0)",
        "",
        "| pair | delta | gamma | angle_deg | intersection_rank |",
        "|---|---:|---:|---:|---:|",
    ]
    for pk, pd in baseline_margins.get("pairs", {}).items():
        lines.append(
            f"| {pk} | {pd['delta']:.6f} | {pd['gamma']:.6f} | "
            f"{pd['principal_angle_deg']:.2f} | {pd['intersection_rank']} |"
        )
    lines.extend([
        "",
        f"**Baseline min_gamma**: {baseline_margins['summary']['min_gamma']:.6f}",
        f"**Critical pairs**: {', '.join(baseline_margins['summary'].get('critical_pairs', []))}",
        "",
        "## Per-Candidate (after adding measurement)",
        "",
        "| candidate | pair | delta_before | delta_after | gamma_before | gamma_after | gamma_gain |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for cr in candidate_results:
        pm = cr.get("pairwise_margin", {})
        for pk, pd in pm.get("pairs", {}).items():
            lines.append(
                f"| {cr['candidate_id']} | {pk} | "
                f"{pd.get('delta_before', 0.0):.6f} | {pd.get('delta_after', 0.0):.6f} | "
                f"{pd.get('gamma_before', 0.0):.6f} | {pd.get('gamma_after', 0.0):.6f} | "
                f"{pd.get('gamma_gain', 0.0):.6f} |"
            )
    lines.append("")
    (out_dir / "PAIRWISE_MARGIN_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")


def write_active_policy_comparison(policy_comparison: dict, out_dir: Path) -> None:
    """Write ACTIVE_POLICY_COMPARISON.md."""
    policies = policy_comparison.get("policies", {})
    lines = [
        "# Active Policy Comparison",
        "",
        f"Pairwise-min-gamma differs from VDR utility: "
        f"**{policy_comparison.get('pairwise_differs_from_vdr', False)}**",
        f"Pairwise-min-gamma differs from interval width: "
        f"**{policy_comparison.get('pairwise_differs_from_interval_width', False)}**",
        "",
        "| policy | selected candidate | metric |",
        "|---|---:|",
    ]
    for pname, pdata in policies.items():
        lines.append(
            f"| {pname} | {pdata.get('selected', 'none')} | "
            f"{pdata.get('metric_value', 0.0):.4f} |"
        )
    lines.append("")
    (out_dir / "ACTIVE_POLICY_COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")


def write_two_step_active_design_audit(two_step: dict, candidate_results: list[dict], out_dir: Path) -> None:
    """Write TWO_STEP_ACTIVE_DESIGN_AUDIT.md."""
    lines = [
        "# Two-Step Active Design Audit",
        "",
        "| metric | value |",
        "|---|---|",
        f"| best_1step_candidate | {two_step.get('best_1step_candidate', 'none')} |",
        f"| best_2step_sequence | {', '.join(two_step.get('best_2step_sequence', []))} |",
        f"| baseline_min_gamma | {two_step.get('baseline_min_gamma', 0.0):.6f} |",
        f"| min_gamma_after_1step | {two_step.get('min_gamma_after_1step', 0.0):.6f} |",
        f"| min_gamma_after_2step | {two_step.get('min_gamma_after_2step', 0.0):.6f} |",
        f"| critical_gamma_after_1step | {two_step.get('critical_gamma_after_1step', 0.0):.6f} |",
        f"| critical_gamma_after_2step | {two_step.get('critical_gamma_after_2step', 0.0):.6f} |",
        f"| step1_cost | {two_step.get('step1_cost', 0.0):.2f} |",
        f"| step2_cost | {two_step.get('step2_cost', 0.0):.2f} |",
        "",
    ]
    (out_dir / "TWO_STEP_ACTIVE_DESIGN_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_round5_pairwise_margin_gate_audit(
    metrics: dict, two_step: dict, policy_comparison: dict, out_dir: Path,
) -> None:
    """Write ROUND5_PAIRWISE_MARGIN_GATE_AUDIT.md."""
    sci = metrics.get("scientific_gates", {})

    lines = [
        "# Round 5 Pairwise-Margin Gate Audit",
        "",
        "| gate | passed |",
        "|---|---|",
    ]
    gate_keys = [
        "pairwise_margin_policy_improves_min_gamma",
        "pairwise_margin_policy_improves_vdr_by_0_20",
        "two_step_policy_min_gamma_positive",
        "two_step_policy_truth_coverage_ge_0_90",
        "two_step_policy_singleton_wrong_rate_eq_0",
        "two_step_policy_empty_rate_le_0_10",
        "critical_h1_h2_gamma_positive",
    ]
    for gk in gate_keys:
        lines.append(f"| {gk} | {sci.get(gk, False)} |")

    lines.extend([
        "",
        f"All round-5 gates pass: **{all(sci.get(gk, False) for gk in gate_keys)}**",
        "",
        "## Summary",
        "",
        f"- pairwise_differs_from_old_policy: {policy_comparison.get('pairwise_differs_from_vdr', False)}",
        f"- baseline_min_gamma: {metrics.get('baseline_pairwise_margins', {}).get('summary', {}).get('min_gamma', 0.0):.6f}",
        f"- min_gamma_after_1step: {two_step.get('min_gamma_after_1step', 0.0):.6f}",
        f"- min_gamma_after_2step: {two_step.get('min_gamma_after_2step', 0.0):.6f}",
        "",
    ])
    (out_dir / "ROUND5_PAIRWISE_MARGIN_GATE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
