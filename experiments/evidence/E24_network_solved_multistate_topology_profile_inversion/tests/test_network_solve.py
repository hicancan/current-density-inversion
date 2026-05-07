"""Test network solver: Laplacian, conductance, KCL."""

import sys
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from graphs import build_topology
from network_solve import (
    solve_network, solve_network_multistate,
    build_excitation_states, compute_conductance_prior,
    build_free_kcl_nullspace,
)


def _make_test_graph():
    rng = np.random.default_rng(42)
    return build_topology("test", rng, 6, 6, 2, 1.0, 1.2, "H0_nominal")


def test_solve_network_basic():
    graph = _make_test_graph()
    theta = compute_conductance_prior(graph.edge_types, graph.edge_count)
    rng = np.random.default_rng(1)
    U = build_excitation_states(graph, 1, rng)
    phi, i_s, kcl = solve_network(graph, theta, U[:, 0])
    assert len(phi) == graph.node_count
    assert len(i_s) == graph.edge_count
    assert kcl < 0.2, f"KCL residual too high: {kcl}"


def test_solve_network_multistate():
    graph = _make_test_graph()
    theta = compute_conductance_prior(graph.edge_types, graph.edge_count)
    rng = np.random.default_rng(1)
    U = build_excitation_states(graph, 2, rng)
    I, kcl_vec, max_kcl = solve_network_multistate(graph, theta, U)
    assert I.shape == (graph.edge_count, 2)
    assert len(kcl_vec) == 2
    assert max_kcl < 0.2, f"Max KCL too high: {max_kcl}"


def test_excitation_states():
    graph = _make_test_graph()
    rng = np.random.default_rng(2)
    U = build_excitation_states(graph, 2, rng)
    assert U.shape == (graph.node_count, 2)
    # Each column should sum to (approximately) zero
    for s in range(2):
        col_sum = np.sum(U[:, s])
        assert abs(col_sum) < 1e-12, f"Column {s} does not sum to 0: {col_sum}"


def test_free_kcl_nullspace():
    graph = _make_test_graph()
    N = build_free_kcl_nullspace(graph)
    # Should have nullspace
    assert N.shape[0] == graph.edge_count
    # Check orthogonality: D_int @ N should be ~0
    internal = sorted(set(range(graph.node_count)) - set(graph.port_nodes))
    D_int = graph.D[internal, :] if internal else graph.D
    if N.shape[1] > 0:
        resid = np.linalg.norm(D_int @ N)
        assert resid < 1e-8, f"Nullspace not KCL-compatible: {resid}"


def test_conductance_positive():
    graph = _make_test_graph()
    theta = compute_conductance_prior(graph.edge_types, graph.edge_count)
    c = np.exp(theta)
    assert np.all(c > 0)
    assert len(theta) == graph.edge_count
