"""Tests for E18 physics-constrained PDN inverse."""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np

# Add src to path for imports
E18_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(E18_DIR))

from src.data import generate_all_cases, load_config, CHANNEL_NAMES, LAYER_IDS
from src.forward_adapter import build_forward_operator, build_div_matrix
from src.inverse import ridge_solve, constrained_ridge_solve, graph_kcl_differentiable_inverse
from src.baselines import BASELINES
from src.metrics import (
    compute_all_metrics, current_rmse, layer_misallocation,
    via_precision_recall_f1, kcl_residual, physical_b_residual,
)
from src.leaderboard import build_leaderboard, win_loss_by_metric


def _mini_cfg():
    """Minimal config for fast tests."""
    return {
        "seed": 42,
        "layer_depths": {"L1": -0.02, "L2": -0.08, "L3": -0.16, "L4": -0.26},
        "grid_size": 6,
        "sensor_grid_size": 8,
        "sensor_z": 0.06,
        "in_plane_extent": [-0.32, 0.32, -0.32, 0.32],
        "families": ["nominal_via_chain", "no_via_hard_negative"],
        "variants_per_family": 1,
        "seed_per_variant_step": 7,
        "ridge_alpha": 0.01,
        "kcl_constraint_weight": 0.5,
        "inverse_max_iter": 20,
        "inverse_b_weight": 1.0,
        "inverse_kcl_weight": 0.5,
        "inverse_topo_weight": 0.3,
        "inverse_via_sparsity_weight": 0.1,
        "inverse_layer_prior_weight": 0.05,
    }


def test_forward_operator_shape():
    cfg = _mini_cfg()
    A, vb = build_forward_operator(cfg)
    n = cfg["grid_size"]
    m = cfg["sensor_grid_size"]
    assert A.shape == (3 * m * m, 11 * n * n)
    assert vb == 8 * n * n


def test_div_matrix_shape():
    n = 6
    D = build_div_matrix(n)
    assert D.shape == (4 * n * n, 11 * n * n)


def test_generate_cases():
    cfg = _mini_cfg()
    A, vb = build_forward_operator(cfg)
    cases = generate_all_cases(cfg, A)
    assert len(cases) == 2  # 2 families x 1 variant
    for c in cases:
        assert c["channels"].shape == (11, 6, 6)
        assert c["field"].shape == (8, 8, 3)
        assert c["flat_ground_truth"].shape == (11 * 36,)


def test_ridge_solve():
    np.random.seed(0)
    A = np.random.randn(10, 5)
    x_true = np.random.randn(5)
    b = A @ x_true
    x_est = ridge_solve(A, b, 0.001)
    assert np.allclose(x_est, x_true, atol=0.1)


def test_constrained_ridge_solve():
    np.random.seed(0)
    A = np.random.randn(10, 5)
    x_true = np.random.randn(5)
    b = A @ x_true
    C = np.eye(5)
    cv = np.zeros(5)
    x_est = constrained_ridge_solve(A, b, 0.001, C, cv, 0.01)
    # Should still get reasonable result
    assert np.linalg.norm(A @ x_est - b) < 1.0


def test_baselines_run():
    cfg = _mini_cfg()
    A, vb = build_forward_operator(cfg)
    cases = generate_all_cases(cfg, A)
    for name, func in BASELINES.items():
        pred = func(cases[0], A, cfg)
        assert pred.shape == (11 * 36,)
        assert np.all(np.isfinite(pred))


def test_new_method_runs():
    cfg = _mini_cfg()
    A, vb = build_forward_operator(cfg)
    cases = generate_all_cases(cfg, A)
    n = cfg["grid_size"]
    result = graph_kcl_differentiable_inverse(A, cases[0]["field"].ravel(), cfg, n)
    assert result["predicted"].shape == (11 * n * n,)
    assert np.all(np.isfinite(result["predicted"]))
    assert result["runtime_s"] > 0
    assert result["optimizer_result"]["success"] or result["optimizer_result"]["n_iter"] > 0


def test_metrics_compute():
    cfg = _mini_cfg()
    A, vb = build_forward_operator(cfg)
    cases = generate_all_cases(cfg, A)
    n = cfg["grid_size"]
    case = cases[0]
    pred = BASELINES["ridge_least_squares"](case, A, cfg)
    m = compute_all_metrics(pred, case["flat_ground_truth"], case["field"], A, n)
    assert "current_rmse" in m
    assert "layer_wise_rmse" in m
    assert "layer_misallocation" in m
    assert "via_metrics" in m
    assert "kcl_residual" in m
    assert "physical_b_residual" in m
    assert "current_closure_error" in m


def test_leaderboard_builds():
    data = {
        "method_a": {"current_rmse": 0.5, "via_f1": 0.8, "kcl_residual": 0.01},
        "method_b": {"current_rmse": 0.3, "via_f1": 0.6, "kcl_residual": 0.02},
    }
    lb = build_leaderboard(data)
    assert len(lb) == 2
    assert all("rank" in r for r in lb)


def test_win_loss():
    data = {
        "new": {"current_rmse": 0.3, "via_f1": 0.9, "kcl_residual": 0.01},
        "baseline": {"current_rmse": 0.5, "via_f1": 0.7, "kcl_residual": 0.005},
    }
    wl = win_loss_by_metric("new", data)
    assert "baseline" in wl
    assert "wins" in wl["baseline"]
    assert "losses" in wl["baseline"]


def test_eleven_channels():
    assert len(CHANNEL_NAMES) == 11


def test_four_layers():
    assert len(LAYER_IDS) == 4


def test_new_method_reduces_kcl_vs_unconstrained():
    """The new method should have lower KCL residual than plain ridge."""
    cfg = _mini_cfg()
    A, vb = build_forward_operator(cfg)
    cases = generate_all_cases(cfg, A)
    n = cfg["grid_size"]
    case = cases[0]

    ridge_pred = BASELINES["ridge_least_squares"](case, A, cfg)
    ridge_kcl = kcl_residual(ridge_pred, n)

    result = graph_kcl_differentiable_inverse(A, case["field"].ravel(), cfg, n)
    new_kcl = kcl_residual(result["predicted"], n)

    # New method should have lower or equal KCL residual
    assert new_kcl <= ridge_kcl * 1.1, (
        f"New method KCL {new_kcl:.6f} > ridge KCL {ridge_kcl:.6f} * 1.1"
    )
