"""Profile fitting: shared-conductance optimization and free KCL baseline.

Core diagnostic: shared_network_fit vs free_kcl_fit vs per_state_network_fit.

The key E24 hypothesis: wrong topologies cannot use ONE shared conductance
vector to fit all states simultaneously, even when free KCL fits succeed.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from graphs import TopologyGraph
from network_solve import (
    solve_network, solve_network_multistate,
    build_free_kcl_nullspace, fit_free_kcl_multistate,
    compute_conductance_prior,
)
from forward import ForwardBundle


def _build_stack_operators(
    bundles: dict[str, ForwardBundle], U: np.ndarray
) -> np.ndarray:
    """Stack observation operators for all states."""
    S = U.shape[1]
    parts = []
    for h in bundles:
        A = bundles[h].A
        parts.extend([A] * S)
    return parts


def shared_network_fit(
    graph: TopologyGraph, bundle: ForwardBundle, Y: np.ndarray, U: np.ndarray,
    theta0: np.ndarray, lam: float = 0.01, max_iter: int = 200,
) -> dict:
    """Optimize shared theta across all states.

    Minimizes:
        J(theta) = sum_s ||y_s - A i_s(theta)||^2 + lam ||theta - theta0||^2

    where i_s(theta) = C(theta) D^T L(theta)^dagger b_s.

    Returns fit results including residual and optimized theta.
    """
    S = U.shape[1]
    obs_per_state = bundle.A.shape[0]
    A = bundle.A

    def objective(theta_np: np.ndarray) -> float:
        theta_np = theta_np.copy()
        val = 0.0
        for s in range(S):
            b_s = U[:, s]
            _, i_s, _ = solve_network(graph, theta_np, b_s)
            y_s = Y[s * obs_per_state:(s + 1) * obs_per_state]
            resid = y_s - A @ i_s
            val += float(np.sum(resid ** 2))
        val += lam * float(np.sum((theta_np - theta0) ** 2))
        return val

    # Use L-BFGS-B with bounds to prevent extreme log-conductances
    result = minimize(
        objective, theta0.copy(),
        method="L-BFGS-B",
        bounds=[(-20, 20)] * len(theta0),
        options={"maxiter": max_iter, "ftol": 1e-12},
    )

    theta_opt = result.x
    residual = np.sqrt(objective(theta_opt))

    # Compute per-state currents and residuals
    per_state_residuals = []
    I_opt = np.zeros((graph.edge_count, S))
    for s in range(S):
        _, I_opt[:, s], _ = solve_network(graph, theta_opt, U[:, s])
        y_s = Y[s * obs_per_state:(s + 1) * obs_per_state]
        per_state_residuals.append(float(np.linalg.norm(y_s - A @ I_opt[:, s])))

    # KCL check
    _, _, max_kcl = solve_network_multistate(graph, theta_opt, U)

    return {
        "residual": float(residual),
        "theta_opt": theta_opt,
        "I_opt": I_opt,
        "per_state_residuals": per_state_residuals,
        "max_kcl_residual": float(max_kcl),
        "success": bool(result.success),
        "n_iter": int(result.nit),
        "conductances_positive": bool(np.all(np.exp(theta_opt) > 0)),
    }


def per_state_network_fit(
    graph: TopologyGraph, bundle: ForwardBundle, Y: np.ndarray, U: np.ndarray,
    theta0: np.ndarray, lam: float = 0.01,
) -> dict:
    """Fit independent theta_s per state (not shared).

    This is an intermediate: each state gets its own conductance vector.
    Should be better than shared but worse than free KCL.
    """
    S = U.shape[1]
    obs_per_state = bundle.A.shape[0]
    A = bundle.A

    thetas = []
    residuals = []
    I_all = np.zeros((graph.edge_count, S))

    for s in range(S):
        def obj_s(theta_np: np.ndarray) -> float:
            _, i_s, _ = solve_network(graph, theta_np, U[:, s])
            y_s = Y[s * obs_per_state:(s + 1) * obs_per_state]
            resid = y_s - A @ i_s
            return float(np.sum(resid ** 2)) + lam * float(np.sum((theta_np - theta0) ** 2))

        result = minimize(
            obj_s, theta0.copy(),
            method="L-BFGS-B",
            bounds=[(-20, 20)] * len(theta0),
            options={"maxiter": 100, "ftol": 1e-10},
        )
        thetas.append(result.x)
        residuals.append(float(np.sqrt(obj_s(result.x) - lam * float(np.sum((result.x - theta0) ** 2)))))
        _, I_all[:, s], _ = solve_network(graph, result.x, U[:, s])

    total_residual = np.sqrt(sum(r ** 2 for r in residuals))
    return {
        "residual": float(total_residual),
        "per_state_residuals": residuals,
        "thetas": thetas,
        "I": I_all,
    }


def free_kcl_fit(
    graph: TopologyGraph, bundle: ForwardBundle, Y: np.ndarray, U: np.ndarray,
    lam: float = 0.0,
) -> dict:
    """Fit free KCL currents (independent per state, full nullspace freedom).

    This should always achieve the lowest residual, as each state can
    independently pick its nullspace current components.
    """
    N = build_free_kcl_nullspace(graph)
    if N.shape[1] == 0:
        # No nullspace — just fit particular solutions
        S = U.shape[1]
        obs_per_state = bundle.A.shape[0]
        residuals = []
        I_all = np.zeros((graph.edge_count, S))
        for s in range(S):
            _, i_s, _ = solve_network(graph, np.zeros(graph.edge_count), U[:, s])
            I_all[:, s] = i_s
            y_s = Y[s * obs_per_state:(s + 1) * obs_per_state]
            residuals.append(float(np.linalg.norm(y_s - bundle.A @ i_s)))
        total = np.sqrt(sum(r ** 2 for r in residuals))
        return {
            "residual": float(total),
            "per_state_residuals": residuals,
            "I": I_all,
            "nullspace_dim": 0,
        }

    residual, currents = fit_free_kcl_multistate(graph, U, bundle.A, Y, N, lam)

    S = U.shape[1]
    obs_per_state = bundle.A.shape[0]
    per_state_residuals = []
    I_all = np.zeros((graph.edge_count, S))
    for s, i_s in enumerate(currents):
        I_all[:, s] = i_s
        y_s = Y[s * obs_per_state:(s + 1) * obs_per_state]
        per_state_residuals.append(float(np.linalg.norm(y_s - bundle.A @ i_s)))

    return {
        "residual": float(residual),
        "per_state_residuals": per_state_residuals,
        "I": I_all,
        "nullspace_dim": N.shape[1],
    }


def fit_all_models(
    graph: TopologyGraph, bundle: ForwardBundle, Y: np.ndarray, U: np.ndarray,
    theta0: np.ndarray, lam: float = 0.01, max_iter: int = 80,
) -> dict:
    """Run shared, per-state, and free KCL fits. Return all residuals."""
    shared = shared_network_fit(graph, bundle, Y, U, theta0, lam, max_iter=max_iter)
    per_state = per_state_network_fit(graph, bundle, Y, U, theta0, lam)
    free = free_kcl_fit(graph, bundle, Y, U, lam=0.0)

    return {
        "shared": shared,
        "per_state": per_state,
        "free": free,
        "gap_shared_vs_free": float(shared["residual"] - free["residual"]),
        "gap_shared_vs_per_state": float(shared["residual"] - per_state["residual"]),
    }
