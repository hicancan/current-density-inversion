"""Analytic reference fields for validation."""
from __future__ import annotations

import numpy as np
from .constants import MU0


def infinite_wire_x_field(points: np.ndarray, current: float, wire_y: float = 0.0, wire_z: float = 0.0) -> np.ndarray:
    """Magnetic field of an infinite wire along +x.

    The wire lies at y=wire_y, z=wire_z and carries current along +x.
    At point r = (x, y, z), perpendicular vector is (0, dy, dz).
    For u = e_x, u × r_perp = dy e_z - dz e_y.

    B_y = -mu0 I dz / (2*pi*rho^2)
    B_z =  mu0 I dy / (2*pi*rho^2)
    B_x = 0
    """
    pts = np.asarray(points, dtype=float)
    dy = pts[..., 1] - wire_y
    dz = pts[..., 2] - wire_z
    rho2 = dy**2 + dz**2
    if np.any(rho2 <= 0):
        raise ValueError("observation points must not lie on the infinite wire")
    coeff = MU0 * current / (2.0 * np.pi * rho2)
    B = np.zeros_like(pts, dtype=float)
    B[..., 1] = -coeff * dz
    B[..., 2] = coeff * dy
    return B


def infinite_wire_z_field(points: np.ndarray, current: float, wire_x: float = 0.0, wire_y: float = 0.0) -> np.ndarray:
    """Magnetic field of an infinite wire along +z.

    Useful as a qualitative reference for vertical via current. At points above
    the via, the field is azimuthal and has no Bz component for an ideal
    infinite z-directed current.
    """
    pts = np.asarray(points, dtype=float)
    dx = pts[..., 0] - wire_x
    dy = pts[..., 1] - wire_y
    rho2 = dx**2 + dy**2
    if np.any(rho2 <= 0):
        # The exact center is singular; caller should avoid it or mask it.
        rho2 = np.maximum(rho2, 1.0e-30)
    coeff = MU0 * current / (2.0 * np.pi * rho2)
    B = np.zeros_like(pts, dtype=float)
    # e_z × (dx e_x + dy e_y) = dx e_y - dy e_x
    B[..., 0] = -coeff * dy
    B[..., 1] = coeff * dx
    return B
