"""Centerline Biot-Savart forward model.

Uses the analytic finite-segment integral along the conductor centerline.
This is the A^{cl} operator from E25 §1.
"""
from __future__ import annotations

import numpy as np

try:
    from .constants import MU0_OVER_4PI, MIN_RHO
    from .geometry import RectConductor
except ImportError:
    from constants import MU0_OVER_4PI, MIN_RHO
    from geometry import RectConductor


def centerline_field(
    points: np.ndarray,           # (P, 3)
    conductor: RectConductor,
) -> np.ndarray:
    """B field at observation points from a single centerline segment.

    Uses the analytic integral for a finite straight wire segment.
    """
    pts = np.asarray(points, dtype=float)
    p0 = conductor.p0
    p1 = conductor.p1
    u = (p1 - p0) / (conductor.length + 1e-30)
    L = conductor.length
    I = conductor.current

    R = pts - p0                               # (P, 3)
    a = np.sum(R * u, axis=-1, keepdims=True)  # (P, 1)
    r_perp = R - a * u                         # (P, 3)
    rho2 = np.sum(r_perp * r_perp, axis=-1)    # (P,)
    rho2_safe = np.maximum(rho2, MIN_RHO ** 2)

    a_scalar = a[..., 0]
    term1 = (L - a_scalar) / (rho2_safe * np.sqrt(rho2_safe + (L - a_scalar) ** 2))
    term2 = a_scalar / (rho2_safe * np.sqrt(rho2_safe + a_scalar ** 2))
    integral = term1 + term2  # (P,)

    cross = np.cross(u, r_perp)  # (P, 3)
    B = MU0_OVER_4PI * I * cross * integral[..., None]
    return B


def centerline_field_from_conductors(
    points: np.ndarray,
    conductors: list[RectConductor],
) -> np.ndarray:
    """Total B field from a list of centerline conductors."""
    if not conductors:
        return np.zeros_like(points)
    B = np.zeros_like(points, dtype=float)
    for cond in conductors:
        B += centerline_field(points, cond)
    return B


def centerline_operator_matrix(
    points: np.ndarray,
    conductors: list[RectConductor],
) -> np.ndarray:
    """Build forward matrix A^{cl} of shape (3P, E).

    Each column is the B-field (3 components) from a unit-current conductor.
    """
    P = points.shape[0]
    E = len(conductors)
    A = np.zeros((3 * P, E), dtype=float)
    for e, cond in enumerate(conductors):
        unit_cond = type(cond)(
            p0=cond.p0, p1=cond.p1,
            width=cond.width, thickness=cond.thickness,
            current=1.0, layer=cond.layer, tag=cond.tag,
        )
        B = centerline_field(points, unit_cond)
        A[:, e] = B.ravel()
    return A
