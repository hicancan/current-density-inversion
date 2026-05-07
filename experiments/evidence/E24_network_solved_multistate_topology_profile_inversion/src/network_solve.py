"""Network solver for conductance-based current distribution.

Solves L(theta) * phi = b_s for node potentials, then derives edge
currents as i_s = C(theta) * D^T * phi_s.

All conductances are shared across excitation states.
"""

from __future__ import annotations

import numpy as np
from graphs import TopologyGraph, EPS


def solve_network(graph: TopologyGraph, theta: np.ndarray, b_s: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Solve the conductance network for one excitation state.

    Args:
        graph: topology with incidence matrix D
        theta: log-conductance vector (|E|,) — shared across states
        b_s: port injection vector (|V|,) — must satisfy sum(b_s) = 0

    Returns:
        phi: node potentials (|V|,)
        i_s: edge currents (|E|,)
        kcl_residual: ||D i_s - b_s||_2
    """
    c = np.exp(np.clip(theta, -20.0, 20.0))
    C = np.diag(c)
    D = graph.D
    L = D @ C @ D.T  # weighted graph Laplacian

    # Solve L phi = b_s with gauge-fixing (sum phi = 0)
    # Use regularized solve: (L + eps*ones) phi = b_s
    # Or pinv
    try:
        phi = np.linalg.lstsq(L, b_s, rcond=None)[0]
    except np.linalg.LinAlgError:
        phi = np.linalg.pinv(L) @ b_s

    # Gauge fix: remove mean
    phi = phi - np.mean(phi)

    # Edge currents
    i_s = c * (D.T @ phi)

    # KCL residual
    kcl_res = float(np.linalg.norm(D @ i_s - b_s))

    return phi, i_s, kcl_res


def solve_network_multistate(
    graph: TopologyGraph, theta: np.ndarray, U: np.ndarray
) -> tuple[np.ndarray, np.ndarray, float]:
    """Solve network for all excitation states with shared conductances.

    Args:
        graph: topology
        theta: shared log-conductance vector
        U: excitation matrix (|V|, S), each column is a b_s vector

    Returns:
        I: edge currents (|E|, S), column s = i_s
        kcl_residuals: list of per-state KCL residuals
        max_kcl_residual: worst-case KCL residual
    """
    S = U.shape[1]
    E = theta.shape[0]
    I = np.zeros((E, S), dtype=float)
    kcl_residuals = []
    for s in range(S):
        _, I[:, s], kcl = solve_network(graph, theta, U[:, s])
        kcl_residuals.append(kcl)
    return I, np.array(kcl_residuals), max(kcl_residuals)


def build_excitation_states(graph: TopologyGraph, state_count: int,
                            rng: np.random.Generator, current_scale: float = 0.1) -> np.ndarray:
    """Build port excitation vectors.

    Each state injects current at one subset of ports and extracts at another,
    ensuring sum(b_s) = 0.
    """
    V = graph.node_count
    ports = sorted(set(graph.port_nodes))
    if not ports:
        # Fallback: use boundary nodes
        rows = graph.layer_of_node == 0
        ports = list(np.where(rows)[0][:min(8, np.sum(rows))])

    U = np.zeros((V, state_count), dtype=float)
    n_ports = len(ports)
    for s in range(state_count):
        # Select source and sink port subsets
        half = max(1, n_ports // 2)
        perm = rng.permutation(n_ports)
        sources = [ports[perm[i]] for i in range(half)]
        sinks = [ports[perm[i]] for i in range(half, min(2 * half, n_ports))]
        amp = current_scale * rng.uniform(0.8, 1.2)
        for src in sources:
            U[src, s] = amp
        for snk in sinks:
            U[snk, s] = -amp * len(sources) / max(len(sinks), 1)

    return U


def build_free_kcl_nullspace(graph: TopologyGraph) -> np.ndarray:
    """Compute SVD nullspace basis N_h for internal KCL.

    Returns N_h such that D_int @ N_h = 0.
    """
    D_int = _internal_kcl_matrix(graph)
    if D_int.shape[0] == 0 or D_int.shape[1] == 0:
        return np.zeros((graph.edge_count, 0))
    _, S, Vt = np.linalg.svd(D_int, full_matrices=False)
    tol = 1e-10 * max(S[0], 1.0) if S.size > 0 else 1e-10
    rank = np.sum(S > tol)
    N = Vt[rank:, :].T  # nullspace basis
    return N


def _internal_kcl_matrix(graph: TopologyGraph) -> np.ndarray:
    """Internal-node KCL matrix."""
    internal = sorted(set(range(graph.node_count)) - set(graph.port_nodes))
    if not internal:
        return graph.D  # all nodes are ports
    return graph.D[internal, :]


def compute_free_kcl_current(graph: TopologyGraph, b_s: np.ndarray,
                              N: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, float]:
    """Compute a free KCL-compatible current for state s.

    Finds particular solution i^0 then adds nullspace component: i = i^0 + N @ z.
    """
    D_int = _internal_kcl_matrix(graph)
    internal = sorted(set(range(graph.node_count)) - set(graph.port_nodes))

    if D_int.shape[0] > 0 and D_int.shape[1] > 0:
        b_int = b_s[internal]
        # Find particular solution via least squares
        i0 = np.linalg.lstsq(D_int, b_int, rcond=None)[0]
    else:
        i0 = np.zeros(graph.edge_count)

    i = i0 + N @ z
    kcl = float(np.linalg.norm(graph.D @ i - b_s))
    return i, kcl


def fit_free_kcl_multistate(
    graph: TopologyGraph, U: np.ndarray, A: np.ndarray,
    Y: np.ndarray, N: np.ndarray, lam: float = 0.0
) -> tuple[float, list[np.ndarray]]:
    """Fit free KCL currents independently per state.

    For each state s, solve:
        min_z || W(y_s - A (i^0_s + N z)) ||^2 + lam ||z||^2

    Returns total residual and per-state current vectors.
    """
    S = U.shape[1]
    D_int = _internal_kcl_matrix(graph)
    internal = sorted(set(range(graph.node_count)) - set(graph.port_nodes))
    obs_per_state = Y.shape[0] // S
    currents = []
    total_r2 = 0.0

    for s in range(S):
        # Particular solution
        if D_int.shape[0] > 0 and D_int.shape[1] > 0:
            b_int = U[internal, s]
            i0 = np.linalg.lstsq(D_int, b_int, rcond=None)[0]
        else:
            i0 = np.zeros(graph.edge_count)

        y_s = Y[s * obs_per_state:(s + 1) * obs_per_state]
        A_s = A[s * obs_per_state:(s + 1) * obs_per_state, :]

        if N.shape[1] > 0:
            Aeff = A_s @ N
            lhs = Aeff.T @ Aeff + lam * np.eye(N.shape[1])
            rhs = Aeff.T @ (y_s - A_s @ i0)
            try:
                z = np.linalg.solve(lhs, rhs)
            except np.linalg.LinAlgError:
                z = np.linalg.lstsq(lhs, rhs, rcond=None)[0]
            i_s = i0 + N @ z
        else:
            i_s = i0

        currents.append(i_s)
        resid = np.linalg.norm(y_s - A_s @ i_s)
        total_r2 += resid ** 2

    return np.sqrt(total_r2), currents


def compute_conductance_prior(edge_types: list[str], edge_count: int) -> np.ndarray:
    """Default log-conductance prior: sheet=0.5, via=0.8, return=0.3."""
    theta0 = np.zeros(edge_count, dtype=float)
    for i, t in enumerate(edge_types):
        if t == "via":
            theta0[i] = 0.8
        elif t == "return":
            theta0[i] = 0.3
        else:  # sheet
            theta0[i] = 0.5
    return theta0
