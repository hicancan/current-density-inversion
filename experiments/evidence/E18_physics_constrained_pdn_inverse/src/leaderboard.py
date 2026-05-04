"""Leaderboard generation for E18.1 unified comparison.

E18.1: Separates scientific leaderboard (no runtime) from runtime table.
Uses average rank across scientific metrics.
"""
from __future__ import annotations
import numpy as np


SCIENTIFIC_METRICS = [
    "current_relative_l2", "layer_misallocation", "via_f1", "no_via_fp",
    "b_residual_rel", "kcl_residual", "closure_error",
]

# lower is better, except via_f1 (higher is better)
HIGHER_IS_BETTER = {"via_f1"}

RUNTIME_METRICS = ["runtime_s"]


def _rank_by_metric(method_results: dict, metric: str) -> dict:
    """Rank methods by a single metric. Returns {method: rank}."""
    methods = list(method_results.keys())
    vals = [(m, method_results[m].get(metric, None)) for m in methods]
    vals = [(m, v) for m, v in vals if v is not None]
    reverse = metric in HIGHER_IS_BETTER
    vals.sort(key=lambda x: x[1], reverse=reverse)
    return {m: i + 1 for i, (m, _) in enumerate(vals)}


def build_scientific_leaderboard(method_results: dict) -> list[dict]:
    """Build leaderboard ranked by average rank across scientific metrics."""
    methods = list(method_results.keys())
    ranks_per_metric = {}
    for metric in SCIENTIFIC_METRICS:
        ranks_per_metric[metric] = _rank_by_metric(method_results, metric)

    rows = []
    for m in methods:
        row = {"method": m}
        metric_ranks = []
        for metric in SCIENTIFIC_METRICS:
            v = method_results[m].get(metric)
            row[metric] = v
            r = ranks_per_metric[metric].get(m)
            if r is not None:
                metric_ranks.append(r)
        row["avg_rank"] = float(np.mean(metric_ranks)) if metric_ranks else 999.0
        rows.append(row)

    rows.sort(key=lambda r: r["avg_rank"])
    for i, r in enumerate(rows):
        r["rank"] = i + 1
    return rows


def build_runtime_table(method_results: dict) -> list[dict]:
    """Build runtime-only table."""
    rows = []
    for m, metrics in method_results.items():
        rows.append({
            "method": m,
            "runtime_s": metrics.get("runtime_s", 0.0),
        })
    rows.sort(key=lambda r: r["runtime_s"])
    return rows


def win_loss_by_metric(new_method: str, method_results: dict, scientific_only: bool = True) -> dict:
    """Compute win/loss for new method vs each baseline."""
    new = method_results.get(new_method)
    if new is None:
        return {}

    metrics = SCIENTIFIC_METRICS if scientific_only else SCIENTIFIC_METRICS + RUNTIME_METRICS

    comparisons = {}
    for other_name, other_metrics in method_results.items():
        if other_name == new_method:
            continue
        wins = []
        losses = []
        ties = []
        for col in metrics:
            nv = new.get(col)
            ov = other_metrics.get(col)
            if nv is None or ov is None:
                continue
            if col in HIGHER_IS_BETTER:
                if nv > ov + 1e-10:
                    wins.append(col)
                elif nv < ov - 1e-10:
                    losses.append(col)
                else:
                    ties.append(col)
            else:
                if nv < ov - 1e-10:
                    wins.append(col)
                elif nv > ov + 1e-10:
                    losses.append(col)
                else:
                    ties.append(col)
        comparisons[other_name] = {
            "wins": wins, "losses": losses, "ties": ties,
            "win_count": len(wins), "loss_count": len(losses), "tie_count": len(ties),
        }
    return comparisons


def _f(v):
    if v is None:
        return "N/A"
    if isinstance(v, float):
        return f"{v:.6f}" if abs(v) >= 0.001 else f"{v:.3e}"
    return str(v)


def format_scientific_leaderboard_md(leaderboard: list[dict]) -> str:
    lines = [
        "# SCIENTIFIC LEADERBOARD",
        "",
        "Ranked by average rank across scientific metrics (no runtime).",
        "",
        "| Rank | Method | avg_rank | rel_l2 | misalloc | via_f1 | no_via_fp | b_res_rel | kcl_res | closure |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in leaderboard:
        lines.append(
            f"| {r['rank']} | {r['method']} "
            f"| {_f(r.get('avg_rank'))} "
            f"| {_f(r.get('current_relative_l2'))} "
            f"| {_f(r.get('layer_misallocation'))} "
            f"| {_f(r.get('via_f1'))} "
            f"| {_f(r.get('no_via_fp'))} "
            f"| {_f(r.get('b_residual_rel'))} "
            f"| {_f(r.get('kcl_residual'))} "
            f"| {_f(r.get('closure_error'))} |"
        )
    lines.append("")
    lines.append("Generated-domain benchmark only. Cannot claim real validation.")
    return "\n".join(lines)


def format_runtime_table_md(table: list[dict]) -> str:
    lines = [
        "# RUNTIME TABLE",
        "",
        "| Method | runtime_s |",
        "|---|---:|",
    ]
    for r in table:
        lines.append(f"| {r['method']} | {_f(r['runtime_s'])} |")
    return "\n".join(lines)


def format_win_loss_md(new_method: str, comparisons: dict) -> str:
    lines = [
        "# WIN/LOSS BY METRIC (Scientific Only)",
        "",
        f"New method: **{new_method}**",
        "",
        "| vs Baseline | Wins | Losses | Ties | Win Metrics | Loss Metrics |",
        "|---|---:|---:|---:|---|---|",
    ]
    for other, comp in comparisons.items():
        lines.append(
            f"| {other} | {comp['win_count']} | {comp['loss_count']} "
            f"| {comp['tie_count']} | {', '.join(comp['wins'])} "
            f"| {', '.join(comp['losses'])} |"
        )
    lines.append("")
    lines.append("Generated-domain benchmark only. Cannot claim real validation.")
    return "\n".join(lines)


def format_pareto_summary_md(new_method: str, method_results: dict) -> str:
    """Generate Pareto dominance summary."""
    new = method_results.get(new_method, {})
    lines = [
        "# PARETO SUMMARY",
        "",
        f"New method: **{new_method}**",
        "",
    ]

    key_baselines = ["ridge_scaled", "graph_kcl_aware_scaled"]
    for bl in key_baselines:
        bl_m = method_results.get(bl)
        if bl_m is None:
            continue
        lines.append(f"## vs {bl}")
        lines.append("")
        wins = []
        losses = []
        for metric in SCIENTIFIC_METRICS:
            nv = new.get(metric)
            ov = bl_m.get(metric)
            if nv is None or ov is None:
                continue
            if metric in HIGHER_IS_BETTER:
                better = nv > ov + 1e-10
                worse = nv < ov - 1e-10
            else:
                better = nv < ov - 1e-10
                worse = nv > ov + 1e-10
            if better:
                wins.append(f"  - ✅ {metric}: {_f(nv)} vs {_f(ov)}")
            elif worse:
                losses.append(f"  - ❌ {metric}: {_f(nv)} vs {_f(ov)}")
            else:
                wins.append(f"  - ➖ {metric}: {_f(nv)} ≈ {_f(ov)}")
        lines.extend(wins)
        lines.extend(losses)
        dominated = len(losses) == 0 and len(wins) > 0
        lines.append(f"  - **Dominates {bl}**: {'YES' if dominated else 'NO'}")
        lines.append("")

    lines.append("Generated-domain benchmark only. Cannot claim real validation.")
    return "\n".join(lines)


# Backward compat
def build_leaderboard(method_results):
    return build_scientific_leaderboard(method_results)

def format_leaderboard_md(leaderboard):
    return format_scientific_leaderboard_md(leaderboard)
