"""Tests for E18.1 physics-constrained PDN inverse."""
import sys
from pathlib import Path
import numpy as np
import pytest

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from src.data import load_config, generate_case, _rng
from src.forward_adapter import (
    build_forward_operator, build_kcl_matrix,
    operator_diagnostics, kcl_diagnostics, scale_operator, unscale_solution,
)
from src.inverse import ridge_solve_scaled, graph_kcl_differentiable_inverse
from src.baselines import ALL_METHODS
from src.metrics import compute_all_metrics

CFG_PATH = _PKG / "configs" / "default.json"

@pytest.fixture(scope="module")
def setup():
    cfg = load_config(CFG_PATH)
    A, vb = build_forward_operator(cfg)
    n = int(cfg["grid_size"])
    D = build_kcl_matrix(n, cfg)
    rng = _rng(42)
    case = generate_case("nominal_via_chain", 0, cfg, rng, A)
    return cfg, A, D, n, case


def test_forward_operator_has_nonzero_via_columns(setup):
    cfg, A, D, n, case = setup
    diag = operator_diagnostics(A, cfg)
    assert diag["via_columns_nonzero"], "Via columns in A must be nonzero"
    assert diag["via_column_norm_min"] > 1e-15


def test_kcl_matrix_couples_via_channels(setup):
    cfg, A, D, n, case = setup
    diag = kcl_diagnostics(D, n)
    assert diag["via_coupling_nonzero"], "KCL matrix must couple via channels"
    for vn in ["s12", "s23", "s34"]:
        assert diag["via_coupling_column_norms"][vn] > 0


def test_oracle_predictor_has_near_zero_b_residual(setup):
    cfg, A, D, n, case = setup
    truth = case["flat_ground_truth"]
    b_pred = A @ truth
    b_obs = case["field"].ravel()
    rel = np.linalg.norm(b_pred - b_obs) / max(np.linalg.norm(b_obs), 1e-30)
    assert rel < 1e-4, f"Oracle b_residual_rel={rel} should be near zero"


def test_zero_predictor_has_near_unit_b_residual(setup):
    cfg, A, D, n, case = setup
    zero = np.zeros(11 * n * n)
    b_obs = case["field"].ravel()
    b_pred = A @ zero
    rel = np.linalg.norm(b_pred - b_obs) / max(np.linalg.norm(b_obs), 1e-30)
    assert rel > 0.5, f"Zero b_residual_rel={rel} should be near 1.0"


def test_scaled_ridge_not_all_zero(setup):
    cfg, A, D, n, case = setup
    pred = ridge_solve_scaled(A, case["field"].ravel(), 1e-3)
    assert np.linalg.norm(pred) > 1e-10, "Scaled ridge should produce nonzero solution"
    b_res = np.linalg.norm(A @ pred - case["field"].ravel()) / max(np.linalg.norm(case["field"].ravel()), 1e-30)
    assert b_res < 1.0, f"Scaled ridge b_res_rel={b_res} should beat zero"


def test_graph_kcl_differentiable_inverse_runs(setup):
    cfg, A, D, n, case = setup
    result = graph_kcl_differentiable_inverse(A, case["field"].ravel(), cfg, n)
    pred = result["predicted"]
    assert pred.shape == (11 * n * n,)
    assert np.linalg.norm(pred) > 1e-10


def test_leaderboard_separates_runtime(setup):
    from src.leaderboard import build_scientific_leaderboard, SCIENTIFIC_METRICS
    # Scientific metrics should not include runtime_s
    assert "runtime_s" not in SCIENTIFIC_METRICS


def test_metrics_detect_via_collapse(setup):
    cfg, A, D, n, case = setup
    zero = np.zeros(11 * n * n)
    m = compute_all_metrics(zero, case["flat_ground_truth"], case["field"], A, n, cfg)
    via = m["via_metrics"]
    # Zero prediction should be detected as collapse if truth has vias
    if via["truth_has_vias"]:
        assert via["via_collapse_to_zero"] is True


def test_scale_operator_roundtrip(setup):
    cfg, A, D, n, case = setup
    b = case["field"].ravel()
    A_s, b_s, cn, bs = scale_operator(A, b)
    # After column normalization, before b_scale: col norms = 1
    # After b_scale division: col norms = 1/bs
    # Check roundtrip: unscale(y, cn) = y / cn
    y = np.ones(A.shape[1])
    x = unscale_solution(y, cn)
    y2 = x * cn
    np.testing.assert_allclose(y, y2, atol=1e-12)
    # Check col_norms are positive
    assert np.all(cn > 0)


def test_kcl_consistent_truth(setup):
    cfg, A, D, n, case = setup
    truth = case["flat_ground_truth"]
    kcl_res = np.sqrt(np.mean((D @ truth) ** 2))
    # With projection, KCL residual should be reduced
    assert kcl_res < 1.0, f"KCL-projected truth should have low KCL residual, got {kcl_res}"


def test_via_forward_affects_field(setup):
    cfg, A, D, n, case = setup
    pl = n * n
    # Create a via-only signal
    x_via = np.zeros(11 * pl)
    x_via[8 * pl:9 * pl] = 1.0  # s12 channel
    b_via = A @ x_via
    assert np.linalg.norm(b_via) > 1e-15, "Via channel should produce nonzero B field"
