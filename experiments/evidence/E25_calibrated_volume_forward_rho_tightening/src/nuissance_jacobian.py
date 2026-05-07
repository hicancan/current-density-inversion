"""Nuisance Jacobian radius computation.

Implements the first-order perturbation analysis from E25 §3.

For nuisance parameters psi = (z_sensor, dx, dy, dz_layer, w, t, sigma_psf, ...)
with bounded box uncertainty |Delta psi_j| <= a_j:

    rho^{box}_h <= sum_j a_j * sup_{i in I_h} ||dA/dpsi_j * i||_2

Uses finite differences to approximate dA/dpsi_j.
"""
from __future__ import annotations

import numpy as np

try:
    from .volume_forward import volume_forward_matrix
    from .geometry import RectConductor
    from .constants import MU0_OVER_4PI
except ImportError:
    from volume_forward import volume_forward_matrix
    from geometry import RectConductor
    from constants import MU0_OVER_4PI


def perturbed_operator(
    points: np.ndarray,
    conductors: list[RectConductor],
    param_name: str,
    delta: float,
    vol_kwargs: dict | None = None,
) -> np.ndarray:
    """Build volume forward matrix with one parameter perturbed.

    Args:
        points: observation points, (P, 3).
        conductors: list of RectConductor.
        param_name: 'sensor_z', 'sensor_dx', 'sensor_dy', 'layer_z', 'width', 'thickness'.
        delta: perturbation amount in SI units.
        vol_kwargs: kwargs for volume_forward_matrix.

    Returns:
        Forward matrix A(psi + delta).
    """
    if vol_kwargs is None:
        vol_kwargs = {"n_seg": 8, "n_w": 5, "n_t": 3}

    pts_perturbed = np.asarray(points, dtype=float).copy()
    conds_perturbed = [_perturb_conductor(c, param_name, delta) for c in conductors]

    if param_name == "sensor_z":
        pts_perturbed[:, 2] += delta
    elif param_name == "sensor_dx":
        pts_perturbed[:, 0] += delta
    elif param_name == "sensor_dy":
        pts_perturbed[:, 1] += delta

    return volume_forward_matrix(pts_perturbed, conds_perturbed, **vol_kwargs)


def _perturb_conductor(
    conductor: RectConductor,
    param_name: str,
    delta: float,
) -> RectConductor:
    """Return a copy of conductor with parameter perturbed."""
    p0 = np.asarray(conductor.p0, dtype=float).copy()
    p1 = np.asarray(conductor.p1, dtype=float).copy()
    width = conductor.width
    thickness = conductor.thickness

    if param_name == "layer_z":
        p0[2] += delta
        p1[2] += delta
    elif param_name == "width":
        width = max(width + delta, 1e-8)
    elif param_name == "thickness":
        thickness = max(thickness + delta, 1e-8)

    return RectConductor(
        p0=p0, p1=p1,
        width=width, thickness=thickness,
        current=conductor.current,
        layer=conductor.layer, tag=conductor.tag,
    )


def nuisance_jacobian_radius(
    points: np.ndarray,
    conductors: list[RectConductor],
    nuisance_specs: list[dict],
    current_samples: np.ndarray | None = None,
    R_h: float = 1.0,
    vol_kwargs: dict | None = None,
) -> dict:
    """Compute nuisance Jacobian radius for each nuisance parameter.

    Args:
        points: observation points, (P, 3).
        conductors: list of RectConductor.
        nuisance_specs: list of dicts with keys:
            - name: parameter name
            - delta: finite-difference step size
            - bound: box uncertainty bound a_j
        current_samples: (E,) or (E, K).
        R_h: current norm bound.
        vol_kwargs: quadrature kwargs.

    Returns:
        dict with per-parameter and combined radii.
    """
    if vol_kwargs is None:
        vol_kwargs = {"n_seg": 6, "n_w": 3, "n_t": 2}

    E = len(conductors)
    rng = np.random.RandomState(42)
    if current_samples is None:
        K = 20
        samples = rng.randn(E, K)
        norms = np.linalg.norm(samples, axis=0)
        samples = R_h * samples / (norms + 1e-30)
    else:
        samples = np.asarray(current_samples, dtype=float)
        if samples.ndim == 1:
            samples = samples[:, None]

    A_nominal = volume_forward_matrix(points, conductors, **vol_kwargs)
    signal_scale = 0.0
    for k in range(samples.shape[1]):
        signal_scale = max(signal_scale,
                           float(np.linalg.norm(A_nominal @ samples[:, k])))
    signal_scale = max(signal_scale, 1e-30)

    results = {}
    total_abs = 0.0
    total_rel = 0.0

    for spec in nuisance_specs:
        name = spec["name"]
        step = spec.get("delta", 1e-6)
        bound = spec.get("bound", 1e-5)

        # Finite-difference Jacobian: dA/dpsi ≈ (A(psi+step) - A(psi-step)) / (2*step)
        A_plus = perturbed_operator(points, conductors, name, step, vol_kwargs)
        A_minus = perturbed_operator(points, conductors, name, -step, vol_kwargs)
        dA_dpsi = (A_plus - A_minus) / (2.0 * step) if step > 1e-30 else np.zeros_like(A_plus)

        # Worst-case over current samples: a_j * max_k ||(dA/dpsi_j) i_k||_2
        worst = 0.0
        for k in range(samples.shape[1]):
            diff = dA_dpsi @ samples[:, k]
            worst = max(worst, float(np.linalg.norm(diff)))

        abs_radius = bound * worst
        rel_radius = abs_radius / signal_scale

        results[f"rho_{name}"] = {
            "name": name,
            "absolute_radius": abs_radius,
            "relative_radius": rel_radius,
            "bound": bound,
            "finite_difference_step": step,
            "signal_scale": signal_scale,
        }
        total_abs += abs_radius
        total_rel += rel_radius

    results["rho_nuisance_combined_box"] = {
        "name": "nuisance_combined_box",
        "absolute_radius": total_abs,
        "relative_radius": total_rel,
        "bound": None,
        "finite_difference_step": None,
        "signal_scale": signal_scale,
    }
    results["rho_nuisance_combined_rss"] = {
        "name": "nuisance_combined_rss",
        "absolute_radius": float(np.sqrt(sum(
            results[k]["absolute_radius"] ** 2
            for k in results if k.startswith("rho_") and k != "rho_nuisance_combined_box"
        ))),
        "relative_radius": float(np.sqrt(sum(
            results[k]["relative_radius"] ** 2
            for k in results if k.startswith("rho_") and k != "rho_nuisance_combined_box"
        ))),
        "bound": None,
        "finite_difference_step": None,
        "signal_scale": signal_scale,
    }

    return results
