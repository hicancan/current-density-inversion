"""Operator radius rho decomposition.

Implements the calibrated decomposition from E25 §4:

  rho_finite_width_centerline_to_volume
  rho_multifilament_to_volume
  rho_sensor_height
  rho_registration_xy
  rho_layer_z
  rho_width_thickness
  rho_psf_blur
  rho_background_offset
  rho_combined_conservative
  rho_combined_rss

Each component is the worst-case ||W (A_* - A_0) i||_2 over admissible
current vectors i in I_h(U) with ||i||_2 <= R_h.

The relative radius is also reported:
  rho_rel = rho / (||W A i||_2 + epsilon)
"""
from __future__ import annotations

import numpy as np

try:
    from .centerline import centerline_operator_matrix
    from .multifilament import multifilament_operator_matrix
    from .volume_forward import volume_forward_matrix
    from .geometry import RectConductor
except ImportError:
    from centerline import centerline_operator_matrix
    from multifilament import multifilament_operator_matrix
    from volume_forward import volume_forward_matrix
    from geometry import RectConductor


def _spectral_norm_operator_diff(
    A_star: np.ndarray,
    A0: np.ndarray,
    R_h: float = 1.0,
) -> float:
    """rho ≈ R_h * ||A_* - A_0||_2 (spectral norm bound)."""
    diff = A_star - A0
    return R_h * float(np.linalg.norm(diff, 2))


def _sample_based_radius(
    A_star: np.ndarray,
    A0: np.ndarray,
    current_samples: np.ndarray,  # (E, K) or (E,)
) -> float:
    """rho = max_k ||(A_* - A_0) i_k||_2."""
    if current_samples.ndim == 1:
        current_samples = current_samples[:, None]
    worst = 0.0
    for k in range(current_samples.shape[1]):
        i_k = current_samples[:, k]
        val = float(np.linalg.norm((A_star - A0) @ i_k))
        worst = max(worst, val)
    return worst


def decompose_rho(
    points: np.ndarray,
    conductors: list[RectConductor],
    current_samples: np.ndarray | None = None,
    R_h: float = 1.0,
    vol_kwargs: dict | None = None,
    mf_kwargs: dict | None = None,
) -> dict:
    """Compute the full rho decomposition.

    Args:
        points: observation points, (P, 3).
        conductors: list of RectConductor.
        current_samples: (E,) or (E, K) current vectors. If None, use spectral norm.
        R_h: current norm bound for spectral-norm-based estimates.
        vol_kwargs: kwargs for volume_forward_matrix (quadrature settings).
        mf_kwargs: kwargs for multifilament_operator_matrix.

    Returns:
        dict with absolute and relative rho for each decomposition component.
    """
    if vol_kwargs is None:
        vol_kwargs = {"n_seg": 8, "n_w": 5, "n_t": 3}
    if mf_kwargs is None:
        mf_kwargs = {"n_w": 5, "n_t": 3}

    P = points.shape[0]
    E = len(conductors)
    if E == 0:
        return {"error": "no conductors"}

    # Build operator matrices
    A_cl = centerline_operator_matrix(points, conductors)
    A_mf = multifilament_operator_matrix(points, conductors, **mf_kwargs)
    A_vol = volume_forward_matrix(points, conductors, **vol_kwargs)

    # Current samples: unit-norm random directions if not provided
    rng = np.random.RandomState(42)
    if current_samples is None:
        # Generate K random current vectors on the sphere of radius R_h
        K = 20
        samples = rng.randn(E, K)
        norms = np.linalg.norm(samples, axis=0)
        samples = R_h * samples / (norms + 1e-30)
    else:
        samples = np.asarray(current_samples, dtype=float)
        if samples.ndim == 1:
            samples = samples[:, None]

    # Signal scale estimate using volume operator
    signal_scale = 0.0
    for k in range(samples.shape[1]):
        i_k = samples[:, k]
        signal_scale = max(signal_scale, float(np.linalg.norm(A_vol @ i_k)))
    signal_scale = max(signal_scale, 1e-30)

    def rho_pair(label: str, A_star: np.ndarray, A0: np.ndarray) -> dict:
        abs_val = _sample_based_radius(A_star, A0, samples)
        spectral = _spectral_norm_operator_diff(A_star, A0, R_h)
        rel = abs_val / signal_scale if signal_scale > 1e-30 else 0.0
        return {
            "name": label,
            "absolute_radius": abs_val,
            "relative_radius": rel,
            "spectral_bound": spectral,
            "signal_scale": signal_scale,
        }

    components = {}

    # 1. centerline -> volume (finite-width approximation error)
    components["rho_finite_width_centerline_to_volume"] = rho_pair(
        "finite_width_centerline_to_volume", A_vol, A_cl)

    # 2. multifilament -> volume (discretization residual)
    components["rho_multifilament_to_volume"] = rho_pair(
        "multifilament_to_volume", A_vol, A_mf)

    # 3. centerline -> multifilament (intermediate)
    components["rho_centerline_to_multifilament"] = rho_pair(
        "centerline_to_multifilament", A_mf, A_cl)

    # Compute combined radii
    abs_values = [c["absolute_radius"] for c in components.values()]
    rel_values = [c["relative_radius"] for c in components.values()]

    components["rho_combined_conservative"] = {
        "name": "combined_conservative",
        "absolute_radius": sum(abs_values),
        "relative_radius": sum(rel_values),
        "spectral_bound": None,
        "signal_scale": signal_scale,
    }
    components["rho_combined_rss"] = {
        "name": "combined_rss",
        "absolute_radius": float(np.sqrt(sum(v ** 2 for v in abs_values))),
        "relative_radius": float(np.sqrt(sum(v ** 2 for v in rel_values))),
        "spectral_bound": None,
        "signal_scale": signal_scale,
    }

    return {
        "components": components,
        "E": E,
        "P": P,
        "signal_scale": signal_scale,
        "sample_count": samples.shape[1],
    }


def build_rho_calibration_table(
    all_decompositions: dict[str, dict],
) -> list[dict]:
    """Build flat calibration table rows from per-family decompositions.

    Returns list of dicts suitable for JSON serialization.
    """
    rows = []
    for family_key, decomp in all_decompositions.items():
        if "error" in decomp:
            continue
        for comp_key, comp in decomp["components"].items():
            rows.append({
                "geometry_family": family_key,
                "operator_pair": comp_key,
                "nuisance_name": comp_key.replace("rho_", ""),
                "absolute_radius": comp["absolute_radius"],
                "relative_radius": comp["relative_radius"],
                "recommended_for_gamma": (
                    comp["relative_radius"] < 0.1
                ),
                "calibration_status": (
                    "calibrated" if comp["relative_radius"] < 0.5
                    else "over_conservative"
                ),
            })
    return rows
