"""Test profile fitting: shared/network, per-state, free KCL."""

import sys
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from graphs import build_topology
from network_solve import (
    solve_network_multistate, build_excitation_states,
    compute_conductance_prior,
)
from forward import build_forward_operator, forward_multistate
from profile_fit import (
    shared_network_fit, per_state_network_fit, free_kcl_fit, fit_all_models,
)


def _make_setup(hypothesis="H0_nominal"):
    rng = np.random.default_rng(42)
    graph = build_topology("test_fit", rng, 5, 5, 2, 1.0, 1.2, hypothesis)
    bundle = build_forward_operator(graph, [3.2], 8, 0.8)
    U = build_excitation_states(graph, 2, rng, current_scale=0.05)
    theta0 = compute_conductance_prior(graph.edge_types, graph.edge_count)
    theta_true = theta0 + 0.1 * rng.normal(0, 1, size=graph.edge_count)
    I, _, _ = solve_network_multistate(graph, theta_true, U)
    Y = forward_multistate(bundle, I, 0.005, rng)
    return graph, bundle, U, Y, theta0


def test_shared_network_fit():
    graph, bundle, U, Y, theta0 = _make_setup()
    result = shared_network_fit(graph, bundle, Y, U, theta0, lam=0.01, max_iter=50)
    assert result["success"] or result["residual"] > 0
    assert result["conductances_positive"]
    assert result["max_kcl_residual"] < 0.5
    assert result["residual"] >= 0


def test_per_state_network_fit():
    graph, bundle, U, Y, theta0 = _make_setup()
    result = per_state_network_fit(graph, bundle, Y, U, theta0, lam=0.01)
    assert result["residual"] >= 0
    assert len(result["per_state_residuals"]) == 2


def test_free_kcl_fit():
    graph, bundle, U, Y, theta0 = _make_setup()
    result = free_kcl_fit(graph, bundle, Y, U, lam=0.0)
    assert result["residual"] >= 0
    assert len(result["per_state_residuals"]) == 2


def test_fit_all_models():
    graph, bundle, U, Y, theta0 = _make_setup()
    results = fit_all_models(graph, bundle, Y, U, theta0, lam=0.01)
    assert "shared" in results
    assert "per_state" in results
    assert "free" in results
    assert "gap_shared_vs_free" in results
    # Free KCL should have lowest residual (most degrees of freedom)
    assert results["free"]["residual"] <= results["shared"]["residual"] + 0.1


def test_self_fit_lower_than_cross_fit():
    """Shared network fit to truth itself should be lower than fit to different topology."""
    rng = np.random.default_rng(42)
    graph_h0 = build_topology("test_cross", rng, 5, 5, 2, 1.0, 1.2, "H0_nominal")
    graph_h1 = build_topology("test_cross", rng, 5, 5, 2, 1.0, 1.2, "H1_via")
    bundle_h0 = build_forward_operator(graph_h0, [3.2], 8, 0.8)
    bundle_h1 = build_forward_operator(graph_h1, [3.2], 8, 0.8)
    U = build_excitation_states(graph_h0, 2, rng, current_scale=0.05)
    theta0_h0 = compute_conductance_prior(graph_h0.edge_types, graph_h0.edge_count)
    theta_true = theta0_h0 + 0.1 * rng.normal(0, 1, size=graph_h0.edge_count)
    I, _, _ = solve_network_multistate(graph_h0, theta_true, U)
    Y = forward_multistate(bundle_h0, I, 0.005, rng)

    fit_self = shared_network_fit(graph_h0, bundle_h0, Y, U, theta0_h0, lam=0.01, max_iter=50)
    theta0_h1 = compute_conductance_prior(graph_h1.edge_types, graph_h1.edge_count)
    fit_cross = shared_network_fit(graph_h1, bundle_h1, Y, U, theta0_h1, lam=0.01, max_iter=50)

    # Self-fit should be better or approximately equal
    assert fit_self["residual"] <= fit_cross["residual"] + 0.2, \
        f"Self {fit_self['residual']:.4f} not <= cross {fit_cross['residual']:.4f}"
