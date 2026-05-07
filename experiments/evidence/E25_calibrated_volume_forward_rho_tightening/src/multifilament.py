"""Multifilament forward model.

Approximates a finite-width conductor by N_fil parallel centerline filaments
distributed across the cross-section. Each filament carries i_e / N_fil current.

This is the intermediate operator between centerline and volume quadrature,
used to quantify the discretization error of centerline-only approximation.
"""
from __future__ import annotations

import numpy as np

try:
    from .centerline import centerline_field
    from .geometry import RectConductor
except ImportError:
    from centerline import centerline_field
    from geometry import RectConductor


def multifilament_field(
    points: np.ndarray,
    conductor: RectConductor,
    n_w: int = 5,
    n_t: int = 3,
) -> np.ndarray:
    """B field from a single conductor discretized as n_w * n_t filaments.

    Filaments are uniformly distributed across the cross-section.
    Each filament carries i_e / (n_w * n_t) current.

    Args:
        points: observation points, shape (P, 3).
        conductor: RectConductor.
        n_w: number of filaments across width.
        n_t: number of filaments across thickness.

    Returns:
        B field array, shape (P, 3).
    """
    pts = np.asarray(points, dtype=float)
    n_w = max(1, int(n_w))
    n_t = max(1, int(n_t))
    n_total = n_w * n_t

    u, v = conductor.cross_section_axes()
    hw = conductor.width / 2.0
    ht = conductor.thickness / 2.0

    # Uniform filament positions across cross-section
    w_offsets = np.linspace(-hw, hw, n_w) if n_w > 1 else np.array([0.0])
    t_offsets = np.linspace(-ht, ht, n_t) if n_t > 1 else np.array([0.0])

    filament_current = conductor.current / n_total

    B_total = np.zeros_like(pts, dtype=float)
    for wo in w_offsets:
        for to in t_offsets:
            offset = wo * u + to * v
            filament_cond = RectConductor(
                p0=conductor.p0 + offset,
                p1=conductor.p1 + offset,
                width=0.0, thickness=0.0,
                current=filament_current,
                layer=conductor.layer,
                tag=f"{conductor.tag}_fw_{wo:.1e}_{to:.1e}",
            )
            B_total += centerline_field(pts, filament_cond)
    return B_total


def multifilament_field_from_conductors(
    points: np.ndarray,
    conductors: list[RectConductor],
    n_w: int = 5,
    n_t: int = 3,
) -> np.ndarray:
    """Total B field from multifilament approximation of all conductors."""
    if not conductors:
        return np.zeros_like(points)
    B = np.zeros_like(points, dtype=float)
    for cond in conductors:
        B += multifilament_field(points, cond, n_w=n_w, n_t=n_t)
    return B


def multifilament_operator_matrix(
    points: np.ndarray,
    conductors: list[RectConductor],
    n_w: int = 5,
    n_t: int = 3,
) -> np.ndarray:
    """Build multifilament forward matrix of shape (3P, E).

    Each column is the B-field from a unit-current conductor.
    """
    P = points.shape[0]
    E = len(conductors)
    A = np.zeros((3 * P, E), dtype=float)
    for e, cond in enumerate(conductors):
        unit_cond = RectConductor(
            p0=cond.p0, p1=cond.p1,
            width=cond.width, thickness=cond.thickness,
            current=1.0, layer=cond.layer, tag=cond.tag,
        )
        B = multifilament_field(points, unit_cond, n_w=n_w, n_t=n_t)
        A[:, e] = B.ravel()
    return A
