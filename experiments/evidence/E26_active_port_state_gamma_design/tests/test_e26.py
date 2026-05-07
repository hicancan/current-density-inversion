"""Tests for E26 Active Port-State Gamma Design."""

from __future__ import annotations

import json
import numpy as np
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from config import load_config
from operators import build_default_operator, grid_positions, build_operator
from networks import (
    generate_port_layout, build_hypothesis_edges,
    compute_hypothesis_bundle, solve_network,
    HYPOTHESIS_NAMES,
)
from port_states import generate_feasible_states, PortState
from gamma import (
    compute_state_current, map_edge_currents_to_field,
    compute_gamma, compute_all_gammas, min_gamma,
    greedy_gamma_selection, two_step_lookahead_selection,
    compute_current_path_overlap, compute_effective_resistance,
    CRITICAL_PAIRS,
)
from baselines import run_all_baselines
from refusal import (
    run_refusal_policy, compute_observation,
    compute_residuals, consistent_set_from_residuals,
)
from diagnostics import state_impact_diagnostics, gamma_trajectory, failure_mode_analysis
from metrics import engineering_gates, scientific_gates, aggregate_run_metrics


RNG = np.random.default_rng(42)
CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "smoke.json"


def test_config_load():
    cfg = load_config(str(CONFIG_PATH))
    assert cfg["schema_version"] == "e26-active-port-gamma-config-v1"
    assert cfg["layout_count"] == 6
    assert cfg["port_count_min"] == 3


def test_operator_build():
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    assert op.A.shape[0] > 0
    assert op.A.shape[1] > 0
    assert op.sensor_height_um == 3.2


def test_grid_positions():
    pos = grid_positions(4, 5.0)
    assert pos.shape == (16, 2)


def test_layout_generation():
    layout = generate_port_layout(0, 9, 4, RNG)
    assert 3 <= layout.p <= 4
    assert layout.n_internal == 9
    assert len(layout.port_indices) == layout.p


def test_hypothesis_building():
    layout = generate_port_layout(0, 9, 4, RNG)
    for h_name in HYPOTHESIS_NAMES:
        hyp = build_hypothesis_edges(layout, h_name, RNG)
        assert hyp.hypothesis == h_name
        assert len(hyp.edges) > 0
        assert len(hyp.resistances) == len(hyp.edges)


def test_hypothesis_bundle():
    layout = generate_port_layout(0, 9, 4, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    assert len(bundle.hypotheses) == 4
    for h_name in HYPOTHESIS_NAMES:
        assert h_name in bundle.hypotheses
        assert h_name in bundle.incidence_matrices
        assert h_name in bundle.nullspace_bases


def test_network_solve():
    layout = generate_port_layout(0, 9, 4, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    b = np.zeros(layout.p)
    b[0] = 1.0
    b[1] = -1.0
    i_edges = solve_network(bundle.hypotheses["H0_open"], b, layout)
    assert len(i_edges) == len(bundle.hypotheses["H0_open"].edges)


def test_port_state_generation():
    layout = generate_port_layout(0, 9, 4, RNG)
    states = generate_feasible_states(layout, RNG, max_states=24)
    assert len(states) >= 4  # at minimum some single-pair states

    # Check constraints
    for s in states:
        assert abs(float(np.sum(s.b))) < 1e-10  # KCL
        assert float(np.sum(np.abs(s.b))) > 0  # non-trivial


def test_gamma_computation():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    gamma = compute_gamma(
        bundle, op, states[:2], "H1_via", "H3_return",
        noise_sigma=1e-11, operator_rho=1e-13,
    )
    assert hasattr(gamma, "delta")
    assert hasattr(gamma, "gamma")
    assert hasattr(gamma, "is_separable")


def test_greedy_selection():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    selected, trace = greedy_gamma_selection(
        bundle, op, states, noise_sigma=1e-11, operator_rho=1e-13,
        max_states=2,
    )
    assert len(selected) >= 1
    assert len(trace) == len(selected)


def test_two_step_selection():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    selected, trace = two_step_lookahead_selection(
        bundle, op, states, noise_sigma=1e-11, operator_rho=1e-13,
        max_states=2,
    )
    assert len(selected) >= 1


def test_baselines():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    baselines = run_all_baselines(
        states, bundle, op, noise_sigma=1e-11, operator_rho=1e-13,
        max_states=2, rng=RNG,
    )
    assert "single_default" in baselines
    assert "random" in baselines
    assert "all_pairwise" in baselines
    assert "max_current_norm" in baselines
    assert "max_eff_resistance_contrast" in baselines
    assert "oracle_truth_margin" in baselines
    assert not baselines["oracle_truth_margin"].is_deployable


def test_refusal_policy():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    selected, _ = greedy_gamma_selection(
        bundle, op, states, noise_sigma=1e-11, operator_rho=1e-13,
        max_states=2,
    )

    trace = run_refusal_policy(
        bundle, op, selected, "H1_via",
        noise_sigma=1e-11, operator_rho=1e-13,
        rng=RNG, S_max=2,
    )
    assert len(trace.steps) > 0
    assert trace.final_decision in ("identified", "refused", "max_states_reached")


def test_observation_generation():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    y = compute_observation(
        bundle, op, states[0], "H1_via",
        noise_sigma=1e-11, rng=RNG,
    )
    assert y.shape == (op.A.shape[0],)


def test_residuals():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    y0 = compute_observation(bundle, op, states[0], "H0_open", noise_sigma=1e-11, rng=RNG)
    residuals = compute_residuals(bundle, op, [(states[0], y0)])
    assert len(residuals) == 4
    consistent = consistent_set_from_residuals(residuals, tau=1e-8)
    assert len(consistent) >= 1


def test_diagnostics():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    diag = state_impact_diagnostics(
        bundle, op, states[0], noise_sigma=1e-11, operator_rho=1e-13,
    )
    assert "gamma_by_pair" in diag
    assert "current_path_overlap" in diag
    assert "effective_resistance" in diag


def test_gamma_trajectory():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    selected, _ = greedy_gamma_selection(
        bundle, op, states, noise_sigma=1e-11, operator_rho=1e-13,
        max_states=2,
    )
    traj = gamma_trajectory(
        bundle, op, selected, noise_sigma=1e-11, operator_rho=1e-13,
    )
    assert "trajectory" in traj
    assert len(traj["trajectory"]) == len(selected) + 1


def test_overlap_computation():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    states = generate_feasible_states(layout, RNG, max_states=12)

    overlap = compute_current_path_overlap(bundle, states[0], "H1_via", "H3_return")
    assert 0.0 <= overlap <= 1.0


def test_effective_resistance():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    states = generate_feasible_states(layout, RNG, max_states=12)

    reff = compute_effective_resistance(bundle, "H0_open", states[0])
    assert reff >= 0


def test_failure_mode_analysis():
    layout = generate_port_layout(0, 9, 3, RNG)
    bundle = compute_hypothesis_bundle(layout, RNG)
    cfg = load_config(str(CONFIG_PATH))
    op = build_default_operator(cfg)
    states = generate_feasible_states(layout, RNG, max_states=12)

    selected, _ = greedy_gamma_selection(
        bundle, op, states, noise_sigma=2.0, operator_rho=1e-13,
        max_states=2,
    )
    baselines = run_all_baselines(
        states, bundle, op, noise_sigma=2.0, operator_rho=1e-13,
        max_states=2, rng=RNG,
    )
    fm = failure_mode_analysis(
        bundle, op, selected, 2.0, 1e-13, baselines,
    )
    assert "min_gamma" in fm
    assert "failure_modes" in fm


def test_aggregate_metrics():
    cfg = load_config(str(CONFIG_PATH))
    results = [
        {
            "layout_id": f"L{i:03d}", "greedy_min_gamma": 0.1 * i,
            "two_step_min_gamma": 0.15 * i, "random_min_gamma": 0.05 * i,
            "single_default_min_gamma": -0.1, "truth_missing_rate": 0.05,
            "wrong_accept_rate": 0.1, "mean_states_used": 2.0,
        }
        for i in range(1, 5)
    ]
    agg = aggregate_run_metrics(results, cfg)
    assert agg["layout_count"] == 4
    assert "positive_gamma_rate" in agg
    assert "greedy_gamma_min_gamma" in agg


def test_main_smoke_run():
    """End-to-end smoke test: run with smoke config and check outputs."""
    from run_all import main
    import tempfile
    import os

    cfg_path = str(CONFIG_PATH)
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "outputs_smoke_test"
        result = main(["--config", cfg_path, "--out", str(out)])
        assert result["status"] in ("passed", "passed_with_limitations", "failed_sanity")
        assert (out / "metrics.json").exists()
        assert (out / "RUN_REPORT.md").exists()
        assert (out / "PORT_STATE_FEASIBILITY_AUDIT.md").exists()
        assert (out / "GREEDY_GAMMA_SELECTION.md").exists()
        assert (out / "TWO_STEP_LOOKAHEAD_AUDIT.md").exists()
        assert (out / "STATE_BASELINE_COMPARISON.md").exists()
        assert (out / "SEQUENTIAL_REFUSAL_POLICY.md").exists()
        assert (out / "CRITICAL_PAIR_STATE_DIAGNOSTICS.md").exists()
        assert (out / "FAILURE_MODES.md").exists()
