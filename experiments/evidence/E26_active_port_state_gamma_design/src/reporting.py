"""Output writers for E26 Active Port-State Gamma Design."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np


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


def write_port_state_feasibility_audit(
    all_states: list, out_dir: Path,
) -> None:
    lines = [
        "# Port State Feasibility Audit",
        "",
        f"Total feasible states generated: {len(all_states)}",
        "",
        "| layout_id | port_count | candidate_states | constraints_check |",
        "|---|---:|---:|:---:|",
    ]
    for entry in all_states:
        lines.append(
            f"| {entry['layout_id']} | {entry['port_count']} | "
            f"{entry['candidate_count']} | {entry['constraints_ok']} |"
        )
    lines.append("")
    (out_dir / "PORT_STATE_FEASIBILITY_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_greedy_gamma_selection(
    layout_results: list[dict], out_dir: Path,
) -> None:
    lines = [
        "# Greedy Gamma State Selection",
        "",
        "| layout_id | states_selected | min_gamma_final | cost |",
        "|---|---:|---:|---:|",
    ]
    for r in layout_results:
        greedy = r.get("greedy", {})
        lines.append(
            f"| {r['layout_id']} | {greedy.get('n_states', 0)} | "
            f"{greedy.get('final_min_gamma', -np.inf):.6f} | "
            f"{greedy.get('total_cost', 0.0):.4f} |"
        )
    lines.append("")
    (out_dir / "GREEDY_GAMMA_SELECTION.md").write_text("\n".join(lines), encoding="utf-8")


def write_two_step_lookahead_audit(
    layout_results: list[dict], out_dir: Path,
) -> None:
    lines = [
        "# Two-Step Lookahead Audit",
        "",
        "| layout_id | states_selected | min_gamma_final | cost | beats_greedy |",
        "|---|---:|---:|---:|:---:|",
    ]
    for r in layout_results:
        ts = r.get("two_step", {})
        greedy_mg = r.get("greedy", {}).get("final_min_gamma", -np.inf)
        ts_mg = ts.get("final_min_gamma", -np.inf)
        beats = "yes" if ts_mg >= greedy_mg else "no"
        lines.append(
            f"| {r['layout_id']} | {ts.get('n_states', 0)} | "
            f"{ts_mg:.6f} | {ts.get('total_cost', 0.0):.4f} | {beats} |"
        )
    lines.append("")
    (out_dir / "TWO_STEP_LOOKAHEAD_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_state_baseline_comparison(
    layout_results: list[dict], out_dir: Path,
) -> None:
    lines = [
        "# State Baseline Comparison",
        "",
        "Strategy ranking by mean min Gamma across all layouts:",
        "",
        "| strategy | mean_min_gamma | median_min_gamma | deployable |",
        "|---|---:|---:|:---:|",
    ]

    # Aggregate across layouts
    strategies = {}
    for r in layout_results:
        baselines = r.get("baselines", {})
        for name, bl in baselines.items():
            if name not in strategies:
                strategies[name] = []
            strategies[name].append(bl.get("min_gamma", -np.inf))

    sorted_strategies = sorted(
        strategies.items(), key=lambda x: np.mean(x[1]), reverse=True,
    )

    for name, values in sorted_strategies:
        mean_val = float(np.mean(values))
        median_val = float(np.median(values))
        dep = "yes" if name != "oracle_truth_margin" else "no (nondeployable)"
        lines.append(f"| {name} | {mean_val:.6f} | {median_val:.6f} | {dep} |")

    lines.append("")
    lines.append("## Per-Layout Breakdown")
    lines.append("")
    lines.append("| layout_id | greedy | two_step | random | default | pairwise | max_norm | max_res | oracle |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    for r in layout_results:
        bl = r.get("baselines", {})
        greedy_mg = r.get("greedy", {}).get("final_min_gamma", -np.inf)
        ts_mg = r.get("two_step", {}).get("final_min_gamma", -np.inf)
        vals = [str(r["layout_id"]),
                f"{greedy_mg:.4f}", f"{ts_mg:.4f}"]
        for key in ["random_best_of_n", "single_default", "all_pairwise",
                     "max_current_norm", "max_eff_resistance_contrast",
                     "oracle_truth_margin"]:
            v = bl.get(key, {}).get("min_gamma", -np.inf)
            vals.append(f"{v:.4f}")
        lines.append("| " + " | ".join(vals) + " |")

    lines.append("")
    (out_dir / "STATE_BASELINE_COMPARISON.md").write_text("\n".join(lines), encoding="utf-8")


def write_sequential_refusal_policy(
    refusal_results: list[dict], out_dir: Path,
) -> None:
    lines = [
        "# Sequential Refusal Policy",
        "",
        "| layout_id | true_hypothesis | final_decision | identified | states_used | truth_missing |",
        "|---|---|:---:|---:|---:|:---:|",
    ]
    for r in refusal_results:
        truth_missing = "yes" if r.get("truth_missing", False) else "no"
        lines.append(
            f"| {r['layout_id']} | {r['true_hypothesis']} | "
            f"{r['final_decision']} | {r.get('identified_hypothesis', '-')} | "
            f"{r['states_used']} | {truth_missing} |"
        )

    lines.append("")
    # Aggregate
    n = len(refusal_results)
    identified = sum(1 for r in refusal_results if r["final_decision"] == "identified")
    refused = sum(1 for r in refusal_results if r["final_decision"] == "refused")
    maxed = sum(1 for r in refusal_results if r["final_decision"] == "max_states_reached")
    wrong = sum(1 for r in refusal_results if r.get("wrong_accept", False))
    missing = sum(1 for r in refusal_results if r.get("truth_missing", False))
    mean_states = float(np.mean([r["states_used"] for r in refusal_results])) if refusal_results else 0

    lines.extend([
        "",
        "## Aggregate",
        "",
        f"- Total runs: {n}",
        f"- Identified (|C|=1, Gamma>0): {identified}",
        f"- Refused (S=Smax, Gamma<=0): {refused}",
        f"- Max states reached: {maxed}",
        f"- Wrong accept rate: {wrong / max(n, 1):.4f}",
        f"- Truth missing rate: {missing / max(n, 1):.4f}",
        f"- Mean states used: {mean_states:.2f}",
    ])

    (out_dir / "SEQUENTIAL_REFUSAL_POLICY.md").write_text("\n".join(lines), encoding="utf-8")


def write_critical_pair_diagnostics(
    layout_results: list[dict], out_dir: Path,
) -> None:
    lines = [
        "# Critical Pair State Diagnostics",
        "",
        "## Gamma by Critical Pair (mean across layouts)",
        "",
        "| pair | mean_gamma | mean_delta | separable_rate |",
        "|---|---:|---:|---:|",
    ]

    # Aggregate pair metrics across layouts
    pair_gammas: dict[str, list[float]] = {}
    pair_deltas: dict[str, list[float]] = {}
    pair_sep: dict[str, list[bool]] = {}

    for r in layout_results:
        pairs = r.get("critical_pair_gammas", {})
        for pair_name, data in pairs.items():
            if pair_name not in pair_gammas:
                pair_gammas[pair_name] = []
                pair_deltas[pair_name] = []
                pair_sep[pair_name] = []
            pair_gammas[pair_name].append(data.get("gamma", -np.inf))
            pair_deltas[pair_name].append(data.get("delta", 0.0))
            pair_sep[pair_name].append(data.get("is_separable", False))

    for pair_name in sorted(pair_gammas.keys()):
        mg = float(np.mean(pair_gammas[pair_name]))
        md = float(np.mean(pair_deltas[pair_name]))
        sr = float(np.mean(pair_sep[pair_name]))
        lines.append(f"| {pair_name} | {mg:.6f} | {md:.6f} | {sr:.4f} |")

    lines.extend([
        "",
        "## Gamma Trajectory (first layout as example)",
        "",
    ])
    if layout_results:
        first_traj = layout_results[0].get("gamma_trajectory", [])
        if first_traj:
            lines.append("| step | min_gamma | separable_pairs | total_pairs |")
            lines.append("|---:|---:|---:|---:|")
            for entry in first_traj[:10]:
                lines.append(
                    f"| {entry['step']} | {entry['min_gamma']:.6f} | "
                    f"{entry['separable_pairs']} | {entry['total_pairs']} |"
                )
        lines.append("")

    (out_dir / "CRITICAL_PAIR_STATE_DIAGNOSTICS.md").write_text("\n".join(lines), encoding="utf-8")


def write_failure_modes(
    failure_results: list[dict], out_dir: Path,
) -> None:
    lines = [
        "# Failure Modes",
        "",
        "## When positive Gamma cannot be achieved, the limiter is identified:",
        "",
    ]

    # Aggregate failure modes across layouts
    mode_counts: dict[str, int] = {}
    for r in failure_results:
        for mode in r.get("failure_modes", []):
            mode_name = mode.get("mode", "unknown")
            mode_counts[mode_name] = mode_counts.get(mode_name, 0) + 1

    if mode_counts:
        lines.append("| failure_mode | count |")
        lines.append("|---|---:|")
        for mode, count in sorted(mode_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"| {mode} | {count} |")
        lines.append("")

    lines.append("## Per-Layout Details")
    lines.append("")
    for r in failure_results:
        lines.append(f"### {r['layout_id']}")
        lines.append(f"- Min Gamma: {r.get('min_gamma', -np.inf):.6f}")
        lines.append(f"- Positive Gamma: {r.get('positive_gamma_achieved', False)}")
        lines.append(f"- Worst pair: {r.get('worst_pair', 'none')} "
                      f"(Gamma={r.get('worst_pair_gamma', 0.0):.6f})")
        modes = r.get("failure_modes", [])
        if modes:
            lines.append("- Failure modes:")
            for mode in modes:
                lines.append(f"  - **{mode['mode']}**: {mode['detail']}")
        lines.append("")

    (out_dir / "FAILURE_MODES.md").write_text("\n".join(lines), encoding="utf-8")


def write_run_report(
    metrics: dict, out_dir: Path,
) -> None:
    status = metrics.get("status", "unknown")
    eng = metrics.get("engineering_gates", {})
    sci = metrics.get("scientific_gates", {})
    eng_passed = all(eng.values()) if eng else False
    sci_passed = all(sci.values()) if sci else False

    lines = [
        "# RUN REPORT - E26 Active Port-State Gamma Design",
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

    agg = metrics.get("aggregate_metrics", {})
    lines.extend([
        "",
        "## Aggregate Metrics",
        "",
        f"- Layout count: {agg.get('layout_count', 0)}",
        f"- Greedy min Gamma (mean): {agg.get('greedy_gamma_min_gamma', -np.inf):.6f}",
        f"- Two-step min Gamma (mean): {agg.get('two_step_min_gamma', -np.inf):.6f}",
        f"- Random min Gamma (mean): {agg.get('random_min_gamma', -np.inf):.6f}",
        f"- Single default min Gamma (mean): {agg.get('single_default_min_gamma', -np.inf):.6f}",
        f"- Truth missing rate: {agg.get('truth_missing_rate', 0):.4f}",
        f"- Wrong accept rate: {agg.get('wrong_accept_rate', 0):.4f}",
        f"- Mean states used: {agg.get('mean_states_used', 0):.2f}",
        f"- Positive Gamma rate: {agg.get('positive_gamma_rate', 0):.4f}",
        f"- Gamma improves with states: {agg.get('gamma_improves_with_states', False)}",
        f"- Wrong accept decreases: {agg.get('wrong_accept_decreases', False)}",
        "",
        "## Scope & Limitations",
        "",
        "This evidence is scoped to generated-domain port-network layouts",
        "with simplified resistance-network models. The state design strategy",
        "is demonstrated on these generated layouts only.",
        "",
        "## Cannot Claim",
        "",
        "- Real QDM/NV validation",
        "- Real CAD/Gerber/GDS validation",
        "- External FEM/FastHenry/COMSOL validation",
        "- Universal via detection",
        "- Real-board PDN robustness",
        "- That generated-domain port-state optimality transfers to real hardware",
        "- Real-world port excitation hardware feasibility",
        "",
        "## Next Required Evidence",
        "",
        "- E24 shared-network profile topology separability results",
        "- Real port-state hardware constraints from QDM/NV testbed",
        "- Validation against E23 multi-state excitation measurements on same layouts",
    ])

    (out_dir / "RUN_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
