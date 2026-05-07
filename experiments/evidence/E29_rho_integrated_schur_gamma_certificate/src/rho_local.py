"""Local rho estimates following E25 methodology.

Since E25 artifacts are not available in this worktree, this module
implements a small local copy of E25-style operator-radius calibration.

Rho decomposition:
  rho_finite_width   — centerline-to-volume operator gap
  rho_height         — sensor height uncertainty radius
  rho_registration   — lateral registration error radius
  rho_layer_z        — conductor layer z-position uncertainty
  rho_background     — background field offset

Combined:
  rho_combined_conservative = sum_j rho_j
  rho_combined_rss          = sqrt(sum_j rho_j^2)
"""
from __future__ import annotations

import numpy as np

# Physical constants
MU0_OVER_4PI = 1e-7


def _centerline_field_single(
    obs: np.ndarray, p0: np.ndarray, p1: np.ndarray, current: float,
) -> np.ndarray:
    """Biot-Savart for a straight current segment (centerline approximation)."""
    r0 = obs - p0
    r1 = obs - p1
    dl = p1 - p0
    cross_r0_r1 = np.cross(r0, r1)
    norm_cross_sq = np.sum(cross_r0_r1 ** 2, axis=-1)
    r0_norm = np.linalg.norm(r0, axis=-1)
    r1_norm = np.linalg.norm(r1, axis=-1)
    dot_term = np.sum(r0 * dl, axis=-1) / (r0_norm + 1e-30) - np.sum(
        r1 * dl, axis=-1
    ) / (r1_norm + 1e-30)
    safe = np.maximum(norm_cross_sq, 1e-30)
    B = MU0_OVER_4PI * current * cross_r0_r1 / safe[:, None] * dot_term[:, None]
    return B


def centerline_operator(points: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """Build centerline Biot-Savart operator matrix A_cl.

    Args:
        points: (P, 3) observation points.
        edges: (E, 2, 3) edge endpoints (start, end) in meters.

    Returns:
        A_cl: (3*P, E) operator matrix.
    """
    P = points.shape[0]
    E = edges.shape[0]
    A = np.zeros((3 * P, E))
    for e in range(E):
        B = _centerline_field_single(
            points, edges[e, 0], edges[e, 1], current=1.0
        )
        A[:, e] = B.ravel()
    return A


def volume_operator(
    points: np.ndarray, edges: np.ndarray, widths: np.ndarray,
    thicknesses: np.ndarray, n_w: int = 5, n_t: int = 3, n_seg: int = 8,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Build volume-quadrature Biot-Savart operator A_vol.

    Approximates rectangular cross-section by distributing n_w*n_t filaments
    across the width and thickness, and n_seg segments along length.
    """
    if rng is None:
        rng = np.random.default_rng(42)

    P = points.shape[0]
    E = edges.shape[0]
    A = np.zeros((3 * P, E))

    for e in range(E):
        p0 = edges[e, 0]
        p1 = edges[e, 1]
        dl = p1 - p0
        length = np.linalg.norm(dl)
        t = dl / (length + 1e-30)

        # Cross-section axes (perpendicular to t)
        if abs(t[2]) < 0.99:
            n1 = np.cross(t, np.array([0.0, 0.0, 1.0]))
        else:
            n1 = np.cross(t, np.array([1.0, 0.0, 0.0]))
        n1 = n1 / (np.linalg.norm(n1) + 1e-30)
        n2 = np.cross(t, n1)
        n2 = n2 / (np.linalg.norm(n2) + 1e-30)

        w = widths[e] if e < len(widths) else widths[0]
        th = thicknesses[e] if e < len(thicknesses) else thicknesses[0]

        B_sum = np.zeros((P, 3))
        total_filaments = n_seg * n_w * n_t

        # Gauss-Legendre-like uniform spacing (simplified from true GL quadrature)
        for si in range(n_seg):
            alpha_s = (si + 0.5) / n_seg
            for wi in range(n_w):
                beta_w = (wi + 0.5 - n_w / 2) / n_w
                for ti in range(n_t):
                    gamma_t = (ti + 0.5 - n_t / 2) / n_t

                    offset = beta_w * w * n1 + gamma_t * th * n2
                    seg_p0 = p0 + alpha_s * dl + offset
                    seg_p1 = p1 + alpha_s * dl + offset

                    B = _centerline_field_single(
                        points, seg_p0, seg_p1, current=1.0 / total_filaments
                    )
                    B_sum += B

        A[:, e] = B_sum.ravel()

    return A


def finite_width_rho(
    points: np.ndarray, edges: np.ndarray,
    widths: np.ndarray, thicknesses: np.ndarray,
    n_w: int = 5, n_t: int = 3, n_seg: int = 8,
) -> tuple[float, float]:
    """Compute rho for finite-width operator gap (centerline vs volume)."""
    A_cl = centerline_operator(points, edges)
    A_vol = volume_operator(points, edges, widths, thicknesses, n_w, n_t, n_seg)

    # Spectral norm bound
    diff = A_vol - A_cl
    abs_rho = float(np.linalg.norm(diff, 2))

    signal_scale = float(np.linalg.norm(A_vol, 2))
    rel_rho = abs_rho / max(signal_scale, 1e-30)

    return abs_rho, rel_rho


def height_uncertainty_rho(
    points: np.ndarray, edges: np.ndarray,
    widths: np.ndarray, thicknesses: np.ndarray,
    delta_z: float = 1e-5,
) -> tuple[float, float]:
    """Compute rho for sensor height uncertainty (delta_z in meters).

    Approximates as exp(-|k|*delta_z) attenuation of high spatial frequencies.
    Simplified: use worst-case scaling factor.
    """
    z0 = float(np.mean(points[:, 2]))
    # Exponential attenuation ratio for shifting height by delta_z
    attenuation = np.exp(-abs(delta_z) / max(abs(z0), 1e-30))
    factor = abs(1.0 - attenuation)

    A_nom = volume_operator(points, edges, widths, thicknesses)
    signal_scale = float(np.linalg.norm(A_nom, 2))
    abs_rho = factor * signal_scale
    rel_rho = factor

    return abs_rho, rel_rho


def registration_uncertainty_rho(
    points: np.ndarray, edges: np.ndarray,
    widths: np.ndarray, thicknesses: np.ndarray,
    delta_xy: float = 1e-6,
) -> tuple[float, float]:
    """Compute rho for lateral registration uncertainty.

    Approximate as gradient of A w.r.t lateral shift.
    """
    # Perturb observation points laterally
    perturbed = points.copy()
    perturbed[:, 0] += delta_xy
    perturbed[:, 1] += delta_xy

    A_nom = volume_operator(points, edges, widths, thicknesses)
    A_pert = volume_operator(perturbed, edges, widths, thicknesses)

    diff = A_pert - A_nom
    abs_rho = float(np.linalg.norm(diff, 2))
    signal_scale = float(np.linalg.norm(A_nom, 2))
    rel_rho = abs_rho / max(signal_scale, 1e-30)

    return abs_rho, rel_rho


def layer_z_uncertainty_rho(
    points: np.ndarray, edges: np.ndarray,
    widths: np.ndarray, thicknesses: np.ndarray,
    delta_layer_z: float = 1e-5,
) -> tuple[float, float]:
    """Compute rho for conductor layer z-position uncertainty."""
    perturbed_edges = edges.copy()
    perturbed_edges[:, :, 2] += delta_layer_z

    A_nom = volume_operator(points, edges, widths, thicknesses)
    A_pert = volume_operator(points, perturbed_edges, widths, thicknesses)

    diff = A_pert - A_nom
    abs_rho = float(np.linalg.norm(diff, 2))
    signal_scale = float(np.linalg.norm(A_nom, 2))
    rel_rho = abs_rho / max(signal_scale, 1e-30)

    return abs_rho, rel_rho


def background_offset_rho(
    typical_signal: float, background_fraction: float = 1e-4,
) -> tuple[float, float]:
    """Compute rho for background field offset."""
    abs_rho = background_fraction * typical_signal
    rel_rho = background_fraction
    return abs_rho, rel_rho


def compute_full_rho_decomposition(
    points: np.ndarray,
    edges: np.ndarray,
    widths: np.ndarray,
    thicknesses: np.ndarray,
    delta_z: float = 1e-5,
    delta_xy: float = 1e-6,
    delta_layer_z: float = 5e-6,
    background_fraction: float = 1e-4,
) -> dict:
    """Compute full rho decomposition using local E25-style estimates.

    Returns dict with all components and combined values.
    """
    A_vol = volume_operator(points, edges, widths, thicknesses)
    signal_scale = float(np.linalg.norm(A_vol, 2))

    components = {}

    abs_fw, rel_fw = finite_width_rho(points, edges, widths, thicknesses)
    components["rho_finite_width"] = {
        "name": "finite_width",
        "description": "Centerline-to-volume operator gap",
        "absolute_radius": abs_fw,
        "relative_radius": rel_fw,
        "calibration_status": "calibrated" if rel_fw < 0.5 else "over_conservative",
    }

    abs_h, rel_h = height_uncertainty_rho(
        points, edges, widths, thicknesses, delta_z,
    )
    components["rho_height"] = {
        "name": "height",
        "description": "Sensor height uncertainty",
        "absolute_radius": abs_h,
        "relative_radius": rel_h,
        "calibration_status": "calibrated" if rel_h < 0.5 else "over_conservative",
    }

    abs_r, rel_r = registration_uncertainty_rho(
        points, edges, widths, thicknesses, delta_xy,
    )
    components["rho_registration"] = {
        "name": "registration",
        "description": "Lateral registration error",
        "absolute_radius": abs_r,
        "relative_radius": rel_r,
        "calibration_status": "calibrated" if rel_r < 0.5 else "over_conservative",
    }

    abs_l, rel_l = layer_z_uncertainty_rho(
        points, edges, widths, thicknesses, delta_layer_z,
    )
    components["rho_layer_z"] = {
        "name": "layer_z",
        "description": "Conductor layer z-position uncertainty",
        "absolute_radius": abs_l,
        "relative_radius": rel_l,
        "calibration_status": "calibrated" if rel_l < 0.5 else "over_conservative",
    }

    abs_b, rel_b = background_offset_rho(signal_scale, background_fraction)
    components["rho_background"] = {
        "name": "background",
        "description": "Background field offset",
        "absolute_radius": abs_b,
        "relative_radius": rel_b,
        "calibration_status": "calibrated" if rel_b < 0.5 else "over_conservative",
    }

    abs_vals = [c["absolute_radius"] for c in components.values()]
    rel_vals = [c["relative_radius"] for c in components.values()]

    combined_conservative = {
        "name": "combined_conservative",
        "description": "Sum of all rho components (conservative bound)",
        "absolute_radius": sum(abs_vals),
        "relative_radius": sum(rel_vals),
        "calibration_status": "conservative_upper_bound",
    }

    combined_rss = {
        "name": "combined_rss",
        "description": "RSS of all rho components (independence assumed)",
        "absolute_radius": float(np.sqrt(sum(v ** 2 for v in abs_vals))),
        "relative_radius": float(np.sqrt(sum(v ** 2 for v in rel_vals))),
        "calibration_status": "rss_upper_bound",
    }

    # E23-style old surrogate (centerline-only, inflated)
    e23_old_factor = 2.5  # E23's conservative multiplier
    combined_e23_old = {
        "name": "combined_e23_old",
        "description": "E23-style inflated surrogate (centerline-only, 2.5x multiplier)",
        "absolute_radius": e23_old_factor * abs_fw,
        "relative_radius": e23_old_factor * rel_fw,
        "calibration_status": "old_surrogate_deprecated",
    }

    components["rho_combined_conservative"] = combined_conservative
    components["rho_combined_rss"] = combined_rss
    components["rho_combined_e23_old"] = combined_e23_old

    return {
        "components": components,
        "signal_scale": signal_scale,
        "E": edges.shape[0],
        "P": points.shape[0],
        "calibration_note": (
            "Local generated calibration. E25 artifacts were not available "
            "in the E29 worktree. Values follow E25 methodology with volume "
            "quadrature vs centerline comparison."
        ),
    }
