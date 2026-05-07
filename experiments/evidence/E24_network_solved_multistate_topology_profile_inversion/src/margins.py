"""Robust profile margins and operator stress for E24.

Computes:
- Pairwise profile separability delta^{profile}_{h,g}
- Operator perturbation radius rho_h
- Robust margin Gamma_{h,g} = delta - tau - noise - rho_h - rho_g
"""

from __future__ import annotations

import numpy as np

from graphs import TopologyGraph
from network_solve import solve_network
from forward import ForwardBundle


def compute_noise_threshold(sigma: float, obs_dim: int, multiplier: float = 2.5) -> float:
    """Noise epsilon = c * sigma * sqrt(obs_dim)."""
    return float(multiplier * sigma * np.sqrt(max(1, obs_dim)))


def compute_profile_residual_gap(
    truth_graph: TopologyGraph,
    wrong_graph: TopologyGraph,
    truth_bundle: ForwardBundle,
    wrong_bundle: ForwardBundle,
    U: np.ndarray,
    truth_theta: np.ndarray,
    wrong_theta: np.ndarray,
    noise_sigma: float,
    rng: np.random.Generator,
) -> dict:
    """Compute residual gap when fitting a wrong topology to truth data.

    Generates data Y from truth_graph with truth_theta, then fits
    wrong_graph to Y and reports the residual gap.

    This is the surrogate profile margin:
        Gamma_tilde = r_g(Y_h) - r_h(Y_h) - noise - rho_h - rho_g
    """
    from network_solve import solve_network_multistate
    from forward import forward_multistate

    S = U.shape[1]
    obs_per_state = truth_bundle.A.shape[0]

    # Generate truth data
    I_truth, kcl_truth, _ = solve_network_multistate(truth_graph, truth_theta, U)
    Y = forward_multistate(truth_bundle, I_truth, noise_sigma, rng)

    # Fit truth to itself (shared network fit)
    from profile_fit import shared_network_fit
    from network_solve import compute_conductance_prior

    theta0_truth = compute_conductance_prior(truth_graph.edge_types, truth_graph.edge_count)
    fit_truth = shared_network_fit(truth_graph, truth_bundle, Y, U, theta0_truth, lam=0.01, max_iter=50)
    r_h = fit_truth["residual"]

    # Fit wrong topology to truth data
    theta0_wrong = compute_conductance_prior(wrong_graph.edge_types, wrong_graph.edge_count)
    fit_wrong = shared_network_fit(wrong_graph, wrong_bundle, Y, U, theta0_wrong, lam=0.01, max_iter=50)
    r_g = fit_wrong["residual"]

    # Normalized ratio
    eps_safe = 0.001 * noise_sigma * np.sqrt(obs_per_state)
    ratio = (r_g + eps_safe) / max(r_h + eps_safe, 1e-15)

    return {
        "r_truth_self": float(r_h),
        "r_wrong_fit": float(r_g),
        "residual_gap": float(r_g - r_h),
        "ratio": float(ratio),
        "r_h_kcl": float(fit_truth["max_kcl_residual"]),
        "r_g_kcl": float(fit_wrong["max_kcl_residual"]),
    }


def estimate_operator_radius(
    graph: TopologyGraph, bundle: ForwardBundle, U: np.ndarray,
    theta: np.ndarray, stress_class: str, magnitude: float,
) -> float:
    """Estimate operator perturbation radius rho_h for one stress class.

    Returns ||W(F_h(theta, stress) - F_h(theta, 0))||_2.
    """
    from network_solve import solve_network_multistate

    I_nom, _, _ = solve_network_multistate(graph, theta, U)
    A_nom = bundle.A

    # Apply perturbation
    if stress_class == "sensor_height_error":
        # Shift sensor height
        A_pert = _perturb_height(bundle, magnitude)
    elif stress_class == "registration_gap":
        # Shift sensor lateral positions
        A_pert = _perturb_registration(bundle, magnitude)
    elif stress_class == "finite_width":
        # Smear edge currents (Gaussian blur along sensor)
        A_pert = _perturb_finite_width(bundle, magnitude)
    elif stress_class == "deep_layer_shift":
        # Shift deep-layer node z-positions
        A_pert = _perturb_deep_layer(graph, bundle, magnitude)
    else:
        A_pert = A_nom

    S = U.shape[1]
    obs_per_state = bundle.A.shape[0]
    F_nom = np.zeros(obs_per_state * S)
    F_pert = np.zeros(obs_per_state * S)
    for s in range(S):
        F_nom[s * obs_per_state:(s + 1) * obs_per_state] = A_nom @ I_nom[:, s]
        F_pert[s * obs_per_state:(s + 1) * obs_per_state] = A_pert @ I_nom[:, s]

    return float(np.linalg.norm(F_pert - F_nom))


def _perturb_height(bundle: ForwardBundle, delta_m: float) -> np.ndarray:
    """Shift sensor height by delta_m meters (approximate)."""
    # Simplification: scale operator columns based on height change ratio
    # More accurate would rebuild A, but this approximates the radius
    h0 = bundle.heights[0] * 1e-6
    factor = np.exp(-abs(delta_m) / h0) if h0 > 0 else 1.0
    return bundle.A * factor


def _perturb_registration(bundle: ForwardBundle, delta_m: float) -> np.ndarray:
    """Lateral shift (registration error). Approximate via gradient."""
    # Approximate: small lateral shift reduces column norms
    factor = max(0.9, 1.0 - abs(delta_m) * 50)
    return bundle.A * factor


def _perturb_finite_width(bundle: ForwardBundle, sigma_m: float) -> np.ndarray:
    """Finite width blur. Approximate via Gaussian attenuation."""
    # Each edge's field is spread; approximate as attenuation
    factor = max(0.85, 1.0 - sigma_m * 30)
    return bundle.A * factor


def _perturb_deep_layer(graph: TopologyGraph, bundle: ForwardBundle, delta_z: float) -> np.ndarray:
    """Shift deep-layer nodes deeper."""
    # Rebuild operator with shifted deep nodes (simplified)
    max_z = float(np.max(np.abs(graph.node_positions[:, 2])))
    factor = max(0.9, max_z / (max_z + abs(delta_z)))
    return bundle.A * factor


def compute_all_stress_radii(
    graph: TopologyGraph, bundle: ForwardBundle, U: np.ndarray,
    theta: np.ndarray, stress_configs: list[dict],
) -> dict:
    """Compute operator perturbation radii for all stress classes."""
    radii = {}
    for sc in stress_configs:
        name = sc["class"]
        mag = float(sc.get("magnitude", 1e-6))
        radii[name] = estimate_operator_radius(graph, bundle, U, theta, name, mag)
    radii["max_rho"] = max(radii.values()) if radii else 0.0
    return radii


def compute_robust_profile_margin(
    residual_gap: float, noise_eps: float,
    rho_h: float, rho_g: float, tau_g: float = 0.0,
) -> float:
    """Compute robust profile margin.

    Gamma_{h,g} = residual_gap - noise_eps - rho_h - rho_g - tau_g
    """
    return float(residual_gap - noise_eps - rho_h - rho_g - tau_g)


def compute_all_pairwise_margins(
    all_graphs: dict[str, TopologyGraph],
    all_bundles: dict[str, ForwardBundle],
    truth_graph: TopologyGraph,
    truth_bundle: ForwardBundle,
    truth_theta: np.ndarray,
    U: np.ndarray,
    noise_sigma: float,
    obs_dim: int,
    stress_radii: dict[str, dict],
    rng: np.random.Generator,
) -> dict:
    """Compute pairwise profile margins for all (truth, wrong) pairs."""
    noise_eps = compute_noise_threshold(noise_sigma, obs_dim, 2.5)
    margins = {}

    for wrong_h, wrong_graph in all_graphs.items():
        if wrong_h == truth_graph.hypothesis:
            continue
        wrong_bundle = all_bundles[wrong_h]

        gap_info = compute_profile_residual_gap(
            truth_graph, wrong_graph, truth_bundle, wrong_bundle,
            U, truth_theta, np.zeros(wrong_graph.edge_count),
            noise_sigma, rng,
        )

        rho_h = stress_radii.get(truth_graph.hypothesis, {}).get("max_rho", 0.0)
        rho_g = stress_radii.get(wrong_h, {}).get("max_rho", 0.0)

        gamma = compute_robust_profile_margin(
            gap_info["residual_gap"], noise_eps, rho_h, rho_g,
        )

        margins[f"{truth_graph.hypothesis}__{wrong_h}"] = {
            **gap_info,
            "noise_eps": noise_eps,
            "rho_truth": rho_h,
            "rho_wrong": rho_g,
            "gamma": gamma,
            "gamma_positive": gamma > 0,
        }

    return margins
