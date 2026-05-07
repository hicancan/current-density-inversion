"""Centerline vs multifilament vs volume forward comparison.

Computes the E25 §5 validation metrics for each canonical geometry family:

  field_rmse
  field_relative_l2
  max_component_error
  operator_frobenius_relative_error
  rho_relative_by_current_family
  quadrature_convergence_rate
"""
from __future__ import annotations

import numpy as np

try:
    from .centerline import centerline_field_from_conductors, centerline_operator_matrix
    from .multifilament import multifilament_field_from_conductors, multifilament_operator_matrix
    from .volume_forward import volume_forward_matrix, volume_forward_column
    from .geometry import RectConductor
    from .constants import MU0_OVER_4PI
except ImportError:
    from centerline import centerline_field_from_conductors, centerline_operator_matrix
    from multifilament import multifilament_field_from_conductors, multifilament_operator_matrix
    from volume_forward import volume_forward_matrix, volume_forward_column
    from geometry import RectConductor
    from constants import MU0_OVER_4PI


def _field_from_volume_matrix(
    points: np.ndarray,
    conductors: list[RectConductor],
    currents: np.ndarray,
    vol_kwargs: dict,
) -> np.ndarray:
    A = volume_forward_matrix(points, conductors, **vol_kwargs)
    B_flat = A @ currents
    return B_flat.reshape(-1, 3)


def compare_forward_models(
    points: np.ndarray,
    conductors: list[RectConductor],
    currents: np.ndarray | None = None,
    vol_kwargs: dict | None = None,
    mf_kwargs: dict | None = None,
) -> dict:
    """Compare centerline, multifilament, and volume forward on common grid.

    Args:
        points: (P, 3) observation points.
        conductors: list of RectConductor with assigned currents.
        currents: (E,) current vector. If None, uses conductor.current.
        vol_kwargs: quadrature kwargs for volume matrix.
        mf_kwargs: kwargs for multifilament.

    Returns:
        dict with comparison metrics.
    """
    if vol_kwargs is None:
        vol_kwargs = {"n_seg": 8, "n_w": 5, "n_t": 3}
    if mf_kwargs is None:
        mf_kwargs = {"n_w": 5, "n_t": 3}
    if currents is None:
        currents = np.array([c.current for c in conductors], dtype=float)

    E = len(conductors)

    # Compute fields
    B_cl = centerline_field_from_conductors(points, conductors)
    B_mf = multifilament_field_from_conductors(points, conductors, **mf_kwargs)
    B_vol = _field_from_volume_matrix(points, conductors, currents, vol_kwargs)

    # RMSE between models
    def rmse(B_a: np.ndarray, B_b: np.ndarray) -> float:
        return float(np.sqrt(np.mean(np.sum((B_a - B_b) ** 2, axis=-1))))

    def relative_l2(B_a: np.ndarray, B_ref: np.ndarray) -> float:
        num = float(np.sqrt(np.sum((B_a - B_ref) ** 2)))
        den = float(np.sqrt(np.sum(B_ref ** 2)))
        return num / den if den > 1e-30 else 0.0

    def max_component_error(B_a: np.ndarray, B_ref: np.ndarray) -> float:
        return float(np.max(np.abs(B_a - B_ref)))

    # Build operator matrices for Frobenius comparison
    A_cl = centerline_operator_matrix(points, conductors)
    A_mf = multifilament_operator_matrix(points, conductors, **mf_kwargs)
    A_vol = volume_forward_matrix(points, conductors, **vol_kwargs)

    def frob_rel(A_a: np.ndarray, A_ref: np.ndarray) -> float:
        num = float(np.linalg.norm(A_a - A_ref, 'fro'))
        den = float(np.linalg.norm(A_ref, 'fro'))
        return num / den if den > 1e-30 else 0.0

    # rho_relative by current family (using the given current vector)
    current_norm = float(np.linalg.norm(currents)) if E > 0 else 0.0
    B_vol_norm = float(np.sqrt(np.sum(B_vol ** 2)))

    def rho_current_family(A_star: np.ndarray, A0: np.ndarray) -> dict:
        diff = (A_star - A0) @ currents
        abs_val = float(np.linalg.norm(diff))
        rel_val = abs_val / B_vol_norm if B_vol_norm > 1e-30 else 0.0
        return {"absolute": abs_val, "relative": rel_val}

    return {
        "field_comparison": {
            "centerline_vs_volume": {
                "rmse": rmse(B_cl, B_vol),
                "relative_l2": relative_l2(B_cl, B_vol),
                "max_component_error": max_component_error(B_cl, B_vol),
            },
            "multifilament_vs_volume": {
                "rmse": rmse(B_mf, B_vol),
                "relative_l2": relative_l2(B_mf, B_vol),
                "max_component_error": max_component_error(B_mf, B_vol),
            },
            "centerline_vs_multifilament": {
                "rmse": rmse(B_cl, B_mf),
                "relative_l2": relative_l2(B_cl, B_mf),
                "max_component_error": max_component_error(B_cl, B_mf),
            },
        },
        "operator_frobenius_relative_error": {
            "centerline_vs_volume": frob_rel(A_cl, A_vol),
            "multifilament_vs_volume": frob_rel(A_mf, A_vol),
            "centerline_vs_multifilament": frob_rel(A_cl, A_mf),
        },
        "rho_by_current_family": {
            "centerline_vs_volume": rho_current_family(A_vol, A_cl),
            "multifilament_vs_volume": rho_current_family(A_vol, A_mf),
            "centerline_vs_multifilament": rho_current_family(A_mf, A_cl),
        },
        "signal_scale": B_vol_norm,
        "current_norm": current_norm,
        "num_conductors": E,
        "num_points": points.shape[0],
    }
