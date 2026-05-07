"""Volume-integrated Biot-Savart forward model.

Implements A^{vol} via numerical quadrature over the conductor volume V_e.
For a rectangular cross-section conductor with uniform current density:

    J_e(r') = (i_e / a_e) * t_e,    r' in V_e
    A^{vol}_{m,e} = mu0/(4*pi*a_e) * int_{V_e} [t_e x (r_m - r')] / |r_m - r'|^3 dr'

The volume integral decomposes into:
1. An integral along the segment (0 to L) using Gauss-Legendre quadrature.
2. An integral over the cross-section (w x t rectangle) using tensor-product
   Gauss-Legendre quadrature.

Quadrature order is configurable; convergence is tested by doubling.
"""
from __future__ import annotations

import numpy as np

try:
    from .constants import MU0_OVER_4PI
    from .geometry import RectConductor
except ImportError:
    from constants import MU0_OVER_4PI
    from geometry import RectConductor


# Precomputed Gauss-Legendre nodes and weights for orders 1-16
_GL_CACHE: dict[int, tuple[np.ndarray, np.ndarray]] = {}


def _gauss_legendre(n: int) -> tuple[np.ndarray, np.ndarray]:
    """Return (nodes, weights) for n-point Gauss-Legendre on [-1, 1]."""
    if n in _GL_CACHE:
        return _GL_CACHE[n]
    nodes, weights = np.polynomial.legendre.leggauss(n)
    _GL_CACHE[n] = (nodes, weights)
    return nodes, weights


def volume_forward_column(
    points: np.ndarray,          # (P, 3) observation points [m]
    conductor: RectConductor,
    n_seg: int = 8,              # quadrature points along segment
    n_w: int = 5,                # quadrature points across width
    n_t: int = 3,                # quadrature points across thickness
) -> np.ndarray:
    """Compute A^{vol} column: B field at points for unit current.

    The conductor carries 1 A for the purpose of building the forward matrix.
    For actual current i_e, scale by i_e.

    Args:
        points: observation points, shape (P, 3).
        conductor: RectConductor defining geometry.
        n_seg: Gauss-Legendre order along segment.
        n_w: Gauss-Legendre order across width.
        n_t: Gauss-Legendre order across thickness.

    Returns:
        B field array, shape (P, 3), for 1 A current.
    """
    pts = np.asarray(points, dtype=float)
    P = pts.shape[0]

    p0 = conductor.p0
    p1 = conductor.p1
    t = conductor.tangent
    L = conductor.length
    area = conductor.cross_section_area
    u, v = conductor.cross_section_axes()
    hw = conductor.width / 2.0
    ht = conductor.thickness / 2.0

    # Gauss-Legendre nodes
    s_nodes, s_weights = _gauss_legendre(n_seg)   # segment [-1,1] -> [0,L]
    w_nodes, w_weights = _gauss_legendre(n_w)      # width [-1,1] -> [-hw, hw]
    t_nodes, t_weights = _gauss_legendre(n_t)      # thickness [-1,1] -> [-ht, ht]

    # Precompute all quadrature points in the conductor volume
    # Total Q = n_seg * n_w * n_t
    B_total = np.zeros((P, 3), dtype=float)
    j_density = 1.0 / area  # current density for unit current

    for si in range(n_seg):
        s_param = (s_nodes[si] + 1.0) / 2.0  # map to [0, 1]
        sw = s_weights[si] * 0.5 * L  # dV Jacobian: (L/2)*w_s * hw*w_w * ht*w_t
        r_centerline = p0 + s_param * (p1 - p0)

        for wi in range(n_w):
            w_offset = w_nodes[wi] * hw
            for ti in range(n_t):
                t_offset = t_nodes[ti] * ht
                r_prime = r_centerline + w_offset * u + t_offset * v

                # Quadrature weight
                weight = sw * w_weights[wi] * t_weights[ti] * hw * ht

                # Biot-Savart: dB = mu0/(4pi) * J x (r - r') / |r - r'|^3 * dV
                # with J = j_density * t
                R = pts - r_prime              # (P, 3)
                R_norm = np.linalg.norm(R, axis=-1)  # (P,)
                R_norm_safe = np.maximum(R_norm, 1e-15)
                R_norm3 = R_norm_safe ** 3

                cross_t_R = np.cross(t, R)     # (P, 3)
                dB = MU0_OVER_4PI * j_density * cross_t_R / R_norm3[..., None] * weight
                B_total += dB

    return B_total


def volume_forward_matrix(
    points: np.ndarray,
    conductors: list[RectConductor],
    n_seg: int = 8,
    n_w: int = 5,
    n_t: int = 3,
) -> np.ndarray:
    """Build the volume forward matrix A^{vol} of shape (3P, E).

    Each column is the B-field from a unit-current conductor.
    """
    P = points.shape[0]
    E = len(conductors)
    A = np.zeros((3 * P, E), dtype=float)
    for e, cond in enumerate(conductors):
        B = volume_forward_column(points, cond, n_seg=n_seg, n_w=n_w, n_t=n_t)
        A[:, e] = B.ravel()
    return A


def volume_forward_matrix_quadrature_pair(
    points: np.ndarray,
    conductors: list[RectConductor],
    n_seg: int = 8,
    n_w: int = 5,
    n_t: int = 3,
) -> tuple[np.ndarray, np.ndarray]:
    """Build A^{quad}_Q and A^{quad}_{2Q} for convergence testing.

    Returns (A_coarse, A_fine) where fine uses doubled quadrature.
    """
    A_coarse = volume_forward_matrix(points, conductors,
                                     n_seg=n_seg, n_w=n_w, n_t=n_t)
    A_fine = volume_forward_matrix(points, conductors,
                                   n_seg=2 * n_seg, n_w=2 * n_w, n_t=2 * n_t)
    return A_coarse, A_fine


def apply_forward(
    A_matrix: np.ndarray,
    currents: np.ndarray,
) -> np.ndarray:
    """Apply forward matrix to current vector.

    Args:
        A_matrix: shape (3P, E)
        currents: shape (E,) or (E, S) for S excitation states.

    Returns:
        B field, shape (3P,) or (3P, S).
    """
    if currents.ndim == 1:
        return A_matrix @ currents
    return A_matrix @ currents
