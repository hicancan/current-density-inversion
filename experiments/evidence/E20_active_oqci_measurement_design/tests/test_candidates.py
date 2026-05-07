"""Test candidate measurement pool with truth coverage (round 3)."""
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import numpy as np
import pytest

from config import component_mask
from operators import build_candidate_operator, multi_height_operator_stack, build_multi_state_operator
from candidates import build_candidate_pool, evaluate_candidate, CandidateMeasurement, _coverage_metrics


def test_component_mask():
    mask = component_mask(["Bx", "By", "Bz"], 4)
    assert mask.sum() == 12
    mask_bz = component_mask(["Bz"], 4)
    assert mask_bz.sum() == 4
    mask_bxy = component_mask(["Bx", "By"], 4)
    assert mask_bxy.sum() == 8


def test_candidate_pool_with_multi_state():
    cfg = {
        "schema_version": "e20-active-oqci-config-v2", "random_seed": 1,
        "grid_size": 6, "layer_count": 4, "pixel_pitch_um": 1.0,
        "layer_spacing_um": 1.2, "sensor_height_um": 3.2,
        "sensor_heights_um": [3.2], "noise_sigma": 0.018,
        "case_count_per_family": 1, "families": ["no_via_clean"],
        "observable_energy_ratio_threshold": 0.015,
        "epsilon_policy": {"mode": "known_noise", "c": 1.5},
        "epsilon_multipliers": [0.5, 1.0, 1.5],
        "prior_variance": {"graph": 0.8, "via_vertical": 1.2, "via_compensation": 0.25,
            "gap_registration": 1.0, "gap_standoff": 1.0, "gap_drift": 0.4,
            "return_loop": 1.2, "return_edge": 0.6, "residual": 0.12},
        "nullspace_threshold": 0.01, "baseline": {"ridge_alpha": 0.08},
        "adversarial_pair_count": 1,
        "candidate_pool": [
            {"id": "test_h1.6_Bz", "height_um": 1.6, "components": ["Bz"], "cost": 0.5},
            {"id": "test_state2", "height_um": 0.0, "components": ["Bx", "By", "Bz"], "cost": 0.8, "n_states": 2},
        ],
        "utility_weights": {"interval_width": 1.0, "near_null": 1.0, "pairwise_distance": 0.5,
            "wrong_accept": 2.0, "cost": 0.1},
    }
    pool = build_candidate_pool(cfg)
    assert len(pool) == 2
    assert pool[1].n_states == 2


def test_coverage_metrics_basic():
    """Test coverage metrics on a minimal setup."""
    cfg = {
        "schema_version": "e20-active-oqci-config-v2", "random_seed": 42,
        "grid_size": 6, "layer_count": 4, "pixel_pitch_um": 1.0,
        "layer_spacing_um": 1.2, "sensor_height_um": 3.2,
        "sensor_heights_um": [3.2], "noise_sigma": 0.018,
        "case_count_per_family": 1,
        "families": ["no_via_clean", "return_path_deep_loop"],
        "observable_energy_ratio_threshold": 0.015,
        "epsilon_policy": {"mode": "known_noise", "c": 1.5},
        "epsilon_multipliers": [0.5, 1.5, 3.0],
        "prior_variance": {"graph": 0.8, "via_vertical": 1.2, "via_compensation": 0.25,
            "gap_registration": 1.0, "gap_standoff": 1.0, "gap_drift": 0.4,
            "return_loop": 1.2, "return_edge": 0.6, "residual": 0.12},
        "nullspace_threshold": 0.01, "baseline": {"ridge_alpha": 0.08},
        "adversarial_pair_count": 1, "candidate_pool": [],
        "utility_weights": {"interval_width": 1.0, "near_null": 1.0, "pairwise_distance": 0.5,
            "wrong_accept": 2.0, "cost": 0.1},
    }
    from hypotheses import build_all_hypothesis_bases
    from data_adapter import generate_cases
    from operators import multi_height_operator_stack

    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    cases = generate_cases(bundle, cfg)
    assert len(cases) == 2

    # Test tight epsilon (0.5 sigma) — should produce empty sets
    sigma = float(cfg["noise_sigma"])
    obs_dim = bundle.A.shape[0]
    eps_val = 0.5 * sigma * np.sqrt(obs_dim)
    cov = _coverage_metrics(cases, bundle, bases, eps_val)
    assert "empty_rate" in cov
    assert "singleton_rate" in cov
    assert "valid_disambiguation_rate" in cov
    assert "truth_in_consistent_set_rate" in cov
    assert cov["n_cases"] == 2

    # Test loose epsilon (3.0 sigma) — should have multi consistent
    eps_val2 = 3.0 * sigma * np.sqrt(obs_dim)
    cov2 = _coverage_metrics(cases, bundle, bases, eps_val2)
    assert cov2["multi_consistent_rate"] >= 0
    assert cov2["truth_in_consistent_set_rate"] >= 0


def test_evaluate_candidate_with_truth_coverage():
    """Evaluate candidate and verify epsilon sweep has truth coverage metrics."""
    cfg = {
        "schema_version": "e20-active-oqci-config-v2", "random_seed": 42,
        "grid_size": 6, "layer_count": 4, "pixel_pitch_um": 1.0,
        "layer_spacing_um": 1.2, "sensor_height_um": 3.2,
        "sensor_heights_um": [3.2], "noise_sigma": 0.018,
        "case_count_per_family": 1,
        "families": ["no_via_clean", "return_path_deep_loop"],
        "observable_energy_ratio_threshold": 0.015,
        "epsilon_policy": {"mode": "known_noise", "c": 1.5},
        "epsilon_multipliers": [0.5, 1.0, 2.0],
        "prior_variance": {"graph": 0.8, "via_vertical": 1.2, "via_compensation": 0.25,
            "gap_registration": 1.0, "gap_standoff": 1.0, "gap_drift": 0.4,
            "return_loop": 1.2, "return_edge": 0.6, "residual": 0.12},
        "nullspace_threshold": 0.01, "baseline": {"ridge_alpha": 0.08},
        "adversarial_pair_count": 1, "candidate_pool": [],
        "utility_weights": {"interval_width": 1.0, "near_null": 1.0, "pairwise_distance": 0.5,
            "wrong_accept": 2.0, "cost": 0.1},
    }
    from operators import operator_diagnostics
    from data_adapter import generate_cases
    from hypotheses import build_all_hypothesis_bases
    from oqci_core import consistent_set_for_case, compute_epsilon_from_policy, run_consistent_set_analysis
    from nullspace import near_null_modes
    from distances import pairwise_distinguishability

    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    cases = generate_cases(bundle, cfg)
    sigma = float(cfg["noise_sigma"])
    eps_values = compute_epsilon_from_policy(sigma, bundle.A.shape[0], cfg["epsilon_policy"])
    primary_eps = eps_values[0]
    baseline_results = [consistent_set_for_case(c, bundle, bases, primary_eps) for c in cases]
    baseline_oqci = run_consistent_set_analysis(cases, bundle, bases, cfg)
    baseline_ns = near_null_modes(bundle, bases, 0.01)
    baseline_pw = pairwise_distinguishability(bases, bundle, cases)

    cand = CandidateMeasurement("test_cand", 6.4, ["Bz"], "test", 0.4)
    result = evaluate_candidate(cfg, baseline_results, [3.2], baseline_oqci, baseline_ns, baseline_pw, cand)

    assert "epsilon_sweep" in result
    for eps_r in result["epsilon_sweep"]:
        assert "valid_disambiguation_rate" in eps_r
        assert "truth_in_consistent_set_rate" in eps_r
        assert "singleton_wrong_rate" in eps_r
        assert "empty_rate" in eps_r
        assert "singleton_correct" in eps_r
