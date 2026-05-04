"""Leaderboard generation for E18 unified comparison."""
from __future__ import annotations
from typing import Any


METRIC_COLS = [
    "current_rmse", "layer_misallocation", "via_f1", "no_via_fp",
    "b_residual_rel", "kcl_residual", "closure_error", "runtime_s",
]


def build_leaderboard(method_results: dict[str, dict]) -> list[dict]:
    """Build a ranked leaderboard from method results.

    Args:
        method_results: {method_name: {metric_name: value, ...}, ...}

    Returns:
        Sorted list of leaderboard rows.
    """
    rows = []
    for name, metrics in method_results.items():
        row = {"method": name}
        for col in METRIC_COLS:
            row[col] = metrics.get(col, None)
        rows.append(row)

    # Rank by composite score: lower is better for all metrics except via_f1
    def score(r):
        s = 0.0
        for col in METRIC_COLS:
            v = r.get(col)
            if v is None:
                continue
            if col == "via_f1":
                s -= v  # higher is better
            else:
                s += v  # lower is better
        return s

    rows.sort(key=score)
    for i, r in enumerate(rows):
        r["rank"] = i + 1
    return rows


def win_loss_by_metric(
    new_method: str, method_results: dict[str, dict]
) -> dict:
    """Compute win/loss table for new method vs each baseline per metric."""
    new = method_results.get(new_method)
    if new is None:
        return {}

    comparisons = {}
    for other_name, other_metrics in method_results.items():
        if other_name == new_method:
            continue
        wins = []
        losses = []
        ties = []
        for col in METRIC_COLS:
            nv = new.get(col)
            ov = other_metrics.get(col)
            if nv is None or ov is None:
                continue
            if col == "via_f1":
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
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "win_count": len(wins),
            "loss_count": len(losses),
            "tie_count": len(ties),
        }
    return comparisons


def format_leaderboard_md(leaderboard: list[dict]) -> str:
    """Format leaderboard as markdown table."""
    lines = [
        "# UNIFIED LEADERBOARD",
        "",
        "| Rank | Method | current_rmse | layer_misalloc | via_f1 | no_via_fp | b_residual | kcl_residual | closure_error | runtime_s |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in leaderboard:
        def _f(v):
            if v is None:
                return "N/A"
            if isinstance(v, float):
                return f"{v:.6f}" if abs(v) >= 0.001 else f"{v:.3e}"
            return str(v)

        lines.append(
            f"| {r['rank']} | {r['method']} "
            f"| {_f(r.get('current_rmse'))} "
            f"| {_f(r.get('layer_misallocation'))} "
            f"| {_f(r.get('via_f1'))} "
            f"| {_f(r.get('no_via_fp'))} "
            f"| {_f(r.get('b_residual_rel'))} "
            f"| {_f(r.get('kcl_residual'))} "
            f"| {_f(r.get('closure_error'))} "
            f"| {_f(r.get('runtime_s'))} |"
        )
    lines.append("")
    lines.append("Lower is better for all metrics except via_f1 (higher is better).")
    lines.append("")
    lines.append("Generated-domain benchmark only. Cannot claim real validation.")
    return "\n".join(lines)


def format_win_loss_md(
    new_method: str, comparisons: dict
) -> str:
    """Format win/loss table as markdown."""
    lines = [
        "# WIN/LOSS BY METRIC",
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
