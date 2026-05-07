"""Test OQCI core reuse: consistent sets, hypotheses, nullspace."""
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import numpy as np
import pytest

from config import load_config, component_mask
from operators import (
    multi_height_operator_stack, operator_diagnostics,
    empty_current, add_gaussian_sheet_mode, add_via_spot, add_return_loop,
    build_candidate_operator,
)
from hypotheses import (
    build_all_hypothesis_bases, HYPOTHESES,
    graph_basis, via_vertical_modes, multi_position_return_loops,
    registration_derivative_basis, subspace_principal_angle_deg,
)
from oqci_core import (
    fit_hypothesis, fit_hypothesis_ridge, fit_hypothesis_reduced_ridge,
    consistent_set_for_case, compute_epsilon_from_policy, _stable_lstsq,
    compute_epsilon_from_quantile,
)
from nullspace import near_null_modes
from distances import (
    unit_energy_principal_angle_distance,
    claim_activated_distance,
    pairwise_distinguishability,
)
from intervals import binary_claim_interval, aggregate_claim_intervals
from data_adapter import generate_cases


def _default_cfg(n=6):
    return {
        "schema_version": "e20-active-oqci-config-v1",
        "random_seed": 42,
        "grid_size": n,
        "layer_count": 4,
        "pixel_pitch_um": 1.0,
        "layer_spacing_um": 1.2,
        "sensor_height_um": 3.2,
        "sensor_heights_um": [3.2],
        "noise_sigma": 0.018,
        "case_count_per_family": 1,
        "families": ["no_via_clean"],
        "observable_energy_ratio_threshold": 0.015,
        "epsilon_policy": {"mode": "known_noise", "c": 1.5},
        "prior_variance": {
            "graph": 0.8, "via_vertical": 1.2, "via_compensation": 0.25,
            "gap_registration": 1.0, "gap_standoff": 1.0, "gap_drift": 0.4,
            "return_loop": 1.2, "return_edge": 0.6, "residual": 0.12,
        },
        "nullspace_threshold": 0.01,
        "baseline": {"ridge_alpha": 0.08},
        "adversarial_pair_count": 1,
        "candidate_pool": [],
        "utility_weights": {
            "interval_width": 1.0, "near_null": 1.0, "pairwise_distance": 0.5,
            "wrong_accept": 2.0, "cost": 0.1,
        },
    }


def test_operator_build():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    diag = operator_diagnostics(bundle)
    assert diag["shape"][0] > 0
    assert diag["shape"][1] > 0
    assert diag["obs_dim"] == 3 * 36  # 3 components * 36 pixels
    assert diag["current_dim"] > 0
    assert bundle.A_per_height is not None


def test_candidate_operator():
    bundle = build_candidate_operator(
        {"grid_size": 4, "layer_count": 4, "pixel_pitch_um": 1.0, "layer_spacing_um": 1.2},
        [3.2], 6.4, ["Bz"],
    )
    n_pix = 16
    assert bundle.A.shape[0] == 3 * n_pix + n_pix  # baseline full + candidate Bz only
    assert bundle.heights == (3.2, 6.4)


def test_hypothesis_bases():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    assert set(bases.keys()) == set(HYPOTHESES)
    for h in HYPOTHESES:
        assert bases[h].B.shape[0] == bundle.A.shape[0]
        assert bases[h].B.shape[1] > 0


def test_lstsq_stability():
    B = np.random.randn(50, 10)
    y = np.random.randn(50)
    coef, residual = _stable_lstsq(B, y)
    assert coef.shape == (10,)
    assert residual >= 0


def test_fit_hypothesis():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    y = np.random.randn(bundle.A.shape[0]) * 0.01
    fit = fit_hypothesis(y, bases["H0_no_via"], 1.0)
    assert fit.hypothesis == "H0_no_via"
    assert fit.residual >= 0
    assert fit.is_consistent  # with large epsilon


def test_consistent_set():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    cases = generate_cases(bundle, cfg)
    sigma = float(cfg["noise_sigma"])
    eps = compute_epsilon_from_policy(sigma, bundle.A.shape[0], cfg["epsilon_policy"])[0]
    result = consistent_set_for_case(cases[0], bundle, bases, eps)
    assert result.case_id
    assert len(result.consistent_hypotheses) >= 0
    assert len(result.non_consistent_hypotheses) >= 0


def test_near_null_modes():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    nn = near_null_modes(bundle, bases, 0.01)
    assert "near_null_count" in nn
    assert "effective_rank" in nn
    assert nn["total_rank"] > 0


def test_pairwise_distances():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    pw = pairwise_distinguishability(bases, bundle)
    assert len(pw["pairs"]) == 6
    for pair_key in pw["pairs"]:
        assert "unit_energy_distance" in pw["pairs"][pair_key]
        assert "claim_activated_distance" in pw["pairs"][pair_key]


def test_claim_intervals():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    cases = generate_cases(bundle, cfg)
    sigma = float(cfg["noise_sigma"])
    eps = compute_epsilon_from_policy(sigma, bundle.A.shape[0], cfg["epsilon_policy"])[0]
    results = [consistent_set_for_case(c, bundle, bases, eps) for c in cases]
    intervals = aggregate_claim_intervals(results)
    assert "interval_matrix" in intervals
    assert len(intervals["interval_matrix"]) == 16  # 4x4


def test_principal_angle():
    A = np.random.randn(100, 5)
    B = np.random.randn(100, 5)
    deg = subspace_principal_angle_deg(A, B)
    assert 0 <= deg <= 90


def test_claim_activated_distance():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    ca = claim_activated_distance("H1_via", "H3_return_path", bases)
    assert "distance" in ca
    assert ca["distance"] >= 0


def test_data_generation():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    cases = generate_cases(bundle, cfg)
    assert len(cases) == 1
    case = cases[0]
    assert case.truth_hypothesis == "H0_no_via"
    assert case.field_observed.shape == (bundle.A.shape[0],)


def test_current_primitives():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    x = empty_current(bundle)
    assert x.shape == (bundle.A.shape[1],)

    add_gaussian_sheet_mode(x, bundle, 0, "x", (3, 3), 2.0, 1.0)
    field = bundle.A @ x
    assert field.shape[0] == bundle.A.shape[0]

    x2 = empty_current(bundle)
    add_via_spot(x2, bundle, 0, 1, (3, 3), 1.0, radius=0)
    field2 = bundle.A @ x2
    assert field2.shape[0] == bundle.A.shape[0]

    x3 = empty_current(bundle)
    add_return_loop(x3, bundle, 3, 1.0)
    field3 = bundle.A @ x3
    assert field3.shape[0] == bundle.A.shape[0]


# ── Round 4 regularized fitting tests ─────────────────────────────────────

def test_ridge_fitting():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    y = np.random.randn(bundle.A.shape[0]) * 0.01
    fit = fit_hypothesis_ridge(y, bases["H0_no_via"], 1.0, lambda_reg=0.1)
    assert fit.hypothesis == "H0_no_via"
    assert fit.residual >= 0
    assert fit.fit_mode == "ridge"
    assert fit.lambda_reg == 0.1
    assert fit.effective_dof > 0


def test_reduced_ridge_fitting():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    y = np.random.randn(bundle.A.shape[0]) * 0.01
    fit = fit_hypothesis_reduced_ridge(y, bases["H1_via"], 1.0, lambda_reg=0.1)
    assert fit.hypothesis == "H1_via"
    assert fit.fit_mode == "reduced_ridge"
    assert fit.effective_dof <= bases["H1_via"].B.shape[1]  # reduced is smaller


def test_regularized_consistent_set():
    cfg = _default_cfg(6)
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    cases = generate_cases(bundle, cfg)
    sigma = float(cfg["noise_sigma"])
    eps = compute_epsilon_from_policy(sigma, bundle.A.shape[0], cfg["epsilon_policy"])[0]
    r = consistent_set_for_case(cases[0], bundle, bases, eps, fit_mode="ridge", lambda_reg=0.1)
    assert r.case_id
    assert len(r.fits) == 4
    for h in HYPOTHESES:
        assert r.fits[h].fit_mode == "ridge"


def test_epsilon_from_quantile():
    resids = np.array([0.1, 0.2, 0.3, 0.5, 1.0])
    eps90 = compute_epsilon_from_quantile(resids, 0.90)
    assert eps90 > 0.5
    eps95 = compute_epsilon_from_quantile(resids, 0.95)
    assert eps95 >= eps90
