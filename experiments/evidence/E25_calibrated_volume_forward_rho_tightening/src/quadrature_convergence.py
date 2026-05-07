"""Quadrature convergence audit.

Tests that A^{quad}_Q converges to A^{quad}_{2Q} as quadrature order
increases, satisfying the E25 scientific gate:

    ||A_Q - A_{2Q}||_F / ||A_{2Q}||_F <= 0.05

This is run in smoke (low-resolution) and default (convergence-sweep) modes.
"""
from __future__ import annotations

import numpy as np

try:
    from .volume_forward import volume_forward_matrix
    from .geometry import (RectConductor, make_straight_strip,
                            make_parallel_strips, make_rectangular_loop,
                            make_two_layer_trace_with_return)
except ImportError:
    from volume_forward import volume_forward_matrix
    from geometry import (RectConductor, make_straight_strip,
                           make_parallel_strips, make_rectangular_loop,
                           make_two_layer_trace_with_return)


def quadrature_relative_change(
    points: np.ndarray,
    conductors: list[RectConductor],
    n_seg: int = 4,
    n_w: int = 3,
    n_t: int = 2,
) -> dict:
    """Compute relative Frobenius change when doubling quadrature.

    Returns dict with keys: relative_change, frob_AQ, frob_A2Q, n_seg, n_w, n_t.
    """
    A_Q = volume_forward_matrix(points, conductors,
                                n_seg=n_seg, n_w=n_w, n_t=n_t)
    A_2Q = volume_forward_matrix(points, conductors,
                                 n_seg=2 * n_seg, n_w=2 * n_w, n_t=2 * n_t)

    frob_AQ = float(np.linalg.norm(A_Q, 'fro'))
    frob_A2Q = float(np.linalg.norm(A_2Q, 'fro'))
    delta = float(np.linalg.norm(A_Q - A_2Q, 'fro'))

    rel_change = delta / frob_A2Q if frob_A2Q > 1e-30 else 0.0
    return {
        "relative_change": rel_change,
        "frob_AQ": frob_AQ,
        "frob_A2Q": frob_A2Q,
        "delta_frob": delta,
        "n_seg": n_seg,
        "n_w": n_w,
        "n_t": n_t,
    }


def quadrature_convergence_sweep(
    points: np.ndarray,
    conductors: list[RectConductor],
    family_label: str,
    seg_levels: list[int] | None = None,
    w_levels: list[int] | None = None,
    t_levels: list[int] | None = None,
) -> list[dict]:
    """Sweep quadrature levels and report convergence.

    Returns list of dicts, one per level.
    """
    if seg_levels is None:
        seg_levels = [2, 4, 8]
    if w_levels is None:
        w_levels = [2, 3, 5]
    if t_levels is None:
        t_levels = [1, 2, 3]

    results = []
    for n_seg in seg_levels:
        for n_w in w_levels:
            for n_t in t_levels:
                entry = quadrature_relative_change(
                    points, conductors,
                    n_seg=n_seg, n_w=n_w, n_t=n_t,
                )
                entry["family"] = family_label
                results.append(entry)
    return results


def check_convergence_gate(results: list[dict], gate: float = 0.05) -> dict:
    """Check if quadrature convergence satisfies the scientific gate.

    Returns dict with: passed, best_relative_change, worst_relative_change,
    median_relative_change, gate_value.
    """
    if not results:
        return {"passed": False, "reason": "no results", "gate_value": gate}

    rel_changes = [r["relative_change"] for r in results]
    best = min(rel_changes)
    worst = max(rel_changes)
    median_val = float(np.median(rel_changes))

    return {
        "passed": best <= gate,
        "best_relative_change": best,
        "worst_relative_change": worst,
        "median_relative_change": median_val,
        "gate_value": gate,
        "num_levels_tested": len(results),
    }
