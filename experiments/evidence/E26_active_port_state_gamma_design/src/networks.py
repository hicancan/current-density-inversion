"""Generated port-network layouts for E26.

Each layout has:
- n_internal: internal nodes on a coarse grid
- ports: accessible port indices (subset of grid positions)
- Each hypothesis defines a different edge-resistance topology connecting the nodes.

For each hypothesis h and port state b, we solve for node potentials and edge currents
using a simple resistance-network model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np


@dataclass
class PortLayout:
    layout_id: str
    n_internal: int
    port_positions: np.ndarray        # shape (p, 2) coordinates in grid cells
    port_indices: np.ndarray           # shape (p,) internal node indices for each port
    p: int                             # number of ports
    boundary_nodes: np.ndarray         # boundary node indices (ground reference)
    internal_nodes: np.ndarray         # internal node indices
    all_positions: np.ndarray          # shape (n_internal + p, 2) positions of all nodes


@dataclass
class NetworkHypothesis:
    hypothesis: str
    label: str
    edges: list[tuple[int, int]]       # (u, v) node index pairs
    resistances: np.ndarray             # per-edge resistance
    description: str


@dataclass
class HypothesisBundle:
    layout: PortLayout
    hypotheses: dict[str, NetworkHypothesis]   # hypothesis name -> NetworkHypothesis
    incidence_matrices: dict[str, np.ndarray]  # hypothesis -> oriented incidence D
    resistance_diag: dict[str, np.ndarray]     # hypothesis -> diag(1/R_e)
    nullspace_bases: dict[str, np.ndarray]     # hypothesis -> nullspace of D_int


HYPOTHESIS_NAMES = ["H0_open", "H1_via", "H2_model_gap", "H3_return"]


def generate_port_layout(
    layout_index: int, n_internal: int, p: int, rng: np.random.Generator,
) -> PortLayout:
    """Generate a random port layout on a grid.

    Internal nodes are on a sqrt(n_internal) x sqrt(n_internal) grid.
    Ports are a random subset of internal nodes, plus one boundary reference.
    """
    side = max(2, int(np.ceil(np.sqrt(n_internal))))
    n_internal = side * side
    xs, ys = np.meshgrid(np.arange(side, dtype=float), np.arange(side, dtype=float))
    all_xy = np.stack([xs.ravel(), ys.ravel()], axis=1)

    # Select p port nodes (ensure p <= n_internal)
    p_actual = min(p, n_internal)
    port_choices = rng.choice(n_internal, size=p_actual, replace=False)
    port_indices = np.sort(port_choices)
    port_positions = all_xy[port_indices]

    internal_nodes = np.arange(n_internal)
    boundary_nodes = np.array([], dtype=int)

    return PortLayout(
        layout_id=f"L{layout_index:03d}_p{p_actual}",
        n_internal=n_internal,
        port_positions=port_positions,
        port_indices=port_indices,
        p=p_actual,
        boundary_nodes=boundary_nodes,
        internal_nodes=internal_nodes,
        all_positions=all_xy,
    )


def build_hypothesis_edges(
    layout: PortLayout, hypothesis: str, rng: np.random.Generator,
) -> NetworkHypothesis:
    """Build edge topology for a given hypothesis.

    All hypotheses share a base grid graph (4-neighbor adjacency).
    Hypothesis-specific edges are added for via, return, and model_gap.
    """
    side = max(2, int(np.round(np.sqrt(layout.n_internal))))
    n = layout.n_internal

    # Base grid edges: 4-neighbor adjacency
    base_edges: list[tuple[int, int]] = []
    for i in range(side):
        for j in range(side):
            u = i * side + j
            if j + 1 < side:
                base_edges.append((u, u + 1))
            if i + 1 < side:
                base_edges.append((u, u + side))

    if hypothesis == "H0_open":
        edges = list(base_edges)
        resistances = np.ones(len(edges)) * (1.0 + 0.05 * rng.normal(0, 1, len(edges)))
        return NetworkHypothesis(
            hypothesis="H0_open", label="open/no-via",
            edges=edges, resistances=np.abs(resistances),
            description="Base grid graph with no via connections",
        )

    elif hypothesis == "H1_via":
        edges = list(base_edges)
        # Add a via: connect center to its counterpart on a "lower layer" via low resistance
        center = side // 2 * side + side // 2
        ghost = n  # ghost node representing lower-layer connection
        n_actual = n + 1
        # Actually we'll model the via as an extra-path through existing nodes
        # Add low-resistance diagonal edges from center to nearby nodes + random
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = center // side + di
                nj = center % side + dj
                if 0 <= ni < side and 0 <= nj < side:
                    neighbors.append(ni * side + nj)
        for nb in neighbors[:3]:
            edges.append((center, nb))
        resistances = np.ones(len(edges)) * (1.0 + 0.05 * rng.normal(0, 1, len(edges)))
        # Via edges have lower resistance
        resistances[len(base_edges):] *= 0.3 + 0.1 * rng.random(len(edges) - len(base_edges))
        return NetworkHypothesis(
            hypothesis="H1_via", label="via_present",
            edges=edges, resistances=np.abs(resistances),
            description="Base grid + low-resistance via connection at center",
        )

    elif hypothesis == "H2_model_gap":
        edges = list(base_edges)
        # Model gap: perturbation in resistance of some edges + extra edge
        # Add a "gap" edge with anomalously high resistance between two nodes
        gap_u = rng.integers(0, n)
        gap_v = rng.integers(0, n)
        while gap_v == gap_u:
            gap_v = rng.integers(0, n)
        edges.append((gap_u, gap_v))
        resistances = np.ones(len(edges)) * (1.0 + 0.05 * rng.normal(0, 1, len(edges)))
        # The gap edge has high resistance
        resistances[-1] = 5.0 + 3.0 * rng.random()
        return NetworkHypothesis(
            hypothesis="H2_model_gap", label="model_gap",
            edges=edges, resistances=np.abs(resistances),
            description="Base grid + high-resistance model-gap edge",
        )

    elif hypothesis == "H3_return":
        edges = list(base_edges)
        # Return path: add a low-resistance path along the perimeter (bottom row)
        for y in [0, side - 1]:
            for x in range(side - 1):
                u = y * side + x
                v = y * side + x + 1
                if (u, v) not in edges and (v, u) not in edges:
                    edges.append((u, v))
        for x in [0, side - 1]:
            for y in range(side - 1):
                u = y * side + x
                v = (y + 1) * side + x
                if (u, v) not in edges and (v, u) not in edges:
                    edges.append((u, v))
        base_count = len(base_edges)
        resistances = np.ones(len(edges)) * (1.0 + 0.05 * rng.normal(0, 1, len(edges)))
        # Perimeter return edges have lower resistance
        resistances[base_count:] *= 0.2 + 0.15 * rng.random(len(edges) - base_count)
        return NetworkHypothesis(
            hypothesis="H3_return", label="return_path",
            edges=edges, resistances=np.abs(resistances),
            description="Base grid + low-resistance perimeter return path",
        )

    else:
        raise ValueError(f"Unknown hypothesis: {hypothesis}")


def build_incidence_matrix(n_nodes: int, edges: list[tuple[int, int]]) -> np.ndarray:
    """Build oriented incidence matrix D of shape (n_nodes, n_edges)."""
    D = np.zeros((n_nodes, len(edges)), dtype=float)
    for e_idx, (u, v) in enumerate(edges):
        D[u, e_idx] = 1.0
        D[v, e_idx] = -1.0
    return D


def solve_network(
    hypothesis: NetworkHypothesis,
    port_currents: np.ndarray,    # shape (p,) injected current at each port
    layout: PortLayout,
) -> np.ndarray:
    """Solve resistance network for edge currents given port injection.

    Solves: G V = b  where G = D * diag(1/R) * D^T is the Laplacian.
    Then edge currents: i_e = diag(1/R) * D^T * V.

    port_currents[b] is injected at port node layout.port_indices[b].
    Sum of port_currents must be zero (KCL).
    """
    n_nodes = layout.n_internal
    D = build_incidence_matrix(n_nodes, hypothesis.edges)
    R_inv = np.diag(1.0 / np.maximum(hypothesis.resistances, 1e-12))

    G = D @ R_inv @ D.T  # Laplacian (n_nodes, n_nodes)

    b = np.zeros(n_nodes)
    for p_idx, node in enumerate(layout.port_indices):
        b[node] = port_currents[p_idx]

    # Fix one node potential to zero for uniqueness (pick first port node)
    ref_node = int(layout.port_indices[0])
    keep = np.ones(n_nodes, dtype=bool)
    keep[ref_node] = False

    G_reduced = G[keep][:, keep]
    b_reduced = b[keep]

    try:
        V_reduced = np.linalg.solve(G_reduced + 1e-12 * np.eye(G_reduced.shape[0]), b_reduced)
    except np.linalg.LinAlgError:
        V_reduced = np.linalg.lstsq(G_reduced + 1e-12 * np.eye(G_reduced.shape[0]), b_reduced, rcond=None)[0]

    V = np.zeros(n_nodes)
    V[keep] = V_reduced
    V[ref_node] = 0.0

    i_edges = R_inv @ (D.T @ V)
    return i_edges


def compute_hypothesis_bundle(
    layout: PortLayout, rng: np.random.Generator,
) -> HypothesisBundle:
    """Build full hypothesis bundle for a layout."""
    hyp_dict: dict[str, NetworkHypothesis] = {}
    inc_dict: dict[str, np.ndarray] = {}
    res_dict: dict[str, np.ndarray] = {}
    null_dict: dict[str, np.ndarray] = {}

    for h_name in HYPOTHESIS_NAMES:
        hyp = build_hypothesis_edges(layout, h_name, rng)
        hyp_dict[h_name] = hyp
        D = build_incidence_matrix(layout.n_internal, hyp.edges)
        inc_dict[h_name] = D
        res_dict[h_name] = np.diag(1.0 / np.maximum(hyp.resistances, 1e-12))

        # Nullspace of D (cycle space): SVD on internal rows
        if D.shape[1] > 0:
            U, S, Vt = np.linalg.svd(D, full_matrices=False)
            rank = int(np.sum(S > 1e-10))
            null_mask = np.arange(S.size) >= rank
            if np.any(null_mask):
                null_dict[h_name] = Vt[null_mask, :].T
            else:
                null_dict[h_name] = np.zeros((D.shape[1], 0))
        else:
            null_dict[h_name] = np.zeros((0, 0))

    return HypothesisBundle(
        layout=layout,
        hypotheses=hyp_dict,
        incidence_matrices=inc_dict,
        resistance_diag=res_dict,
        nullspace_bases=null_dict,
    )
