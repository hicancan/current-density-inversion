from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_all import (
    _build_forward_matrix,
    _effective_rank,
    _condition_number_proxy,
    _separability_margin,
    _layer_misallocation_error,
    _return_confusion_rate,
    _via_auc,
    _obs_dim,
    generate_case,
    load_config,
    run_experiment,
)
import numpy as np


def _cfg() -> dict:
    return {
        "seed": 20260504,
        "grid_size": 10,
        "sensor_fov": 1.4,
        "heights": [0.35, 0.55, 0.75],
        "n_states_list": [1, 2],
        "component_modes": ["Bz", "Bxyz"],
        "layer_z": {"L1_route": -0.1, "L2_route": -0.2, "L0_return": -0.3},
        "effective_rank_threshold": 1e-6,
        "n_segments_per_case": 8,
        "n_cases": 12,
        "test_split_ratio": 0.5,
        "separability_margin_threshold": 0.05,
        "via_auc_threshold": 0.85,
        "layer_misallocation_threshold": 0.20,
        "return_confusion_threshold": 0.15,
        "condition_number_improvement_ratio": 0.9,
        "margin_improvement_ratio": 0.8,
        "rank_not_worse_tolerance": 0.95,
    }


def test_case_generation_produces_segments() -> None:
    rng = np.random.Generator(np.random.PCG64(20260504))
    case = generate_case(0, _cfg(), rng)
    assert len(case["segments"]) > 0
    assert case["n_segments"] == len(case["segments"])
    assert "case_id" in case


def test_case_has_via_and_return_flags() -> None:
    rng = np.random.Generator(np.random.PCG64(20260504))
    via_count = 0
    for i in range(20):
        case = generate_case(i, _cfg(), rng)
        if case["has_via"]:
            via_count += 1
            assert case["n_l2"] > 0
        if case["has_return"]:
            assert case["has_via"]
    assert via_count > 0


def test_forward_matrix_dimensions() -> None:
    cfg = _cfg()
    rng = np.random.Generator(np.random.PCG64(20260504))
    case = generate_case(0, cfg, rng)
    segments = case["segments"]
    G = _build_forward_matrix(segments, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35], "Bz")
    assert G.shape[0] == _obs_dim(int(cfg["grid_size"]), "Bz")
    assert G.shape[1] == len(segments)


def test_forward_matrix_multi_height() -> None:
    cfg = _cfg()
    rng = np.random.Generator(np.random.PCG64(20260504))
    case = generate_case(0, cfg, rng)
    segments = case["segments"]
    G_single = _build_forward_matrix(segments, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35], "Bz")
    G_dual = _build_forward_matrix(segments, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35, 0.55], "Bz")
    assert G_dual.shape[0] == 2 * G_single.shape[0]
    assert G_dual.shape[1] == G_single.shape[1]


def test_effective_rank_positive() -> None:
    sv = np.array([10.0, 5.0, 2.0, 0.5, 1e-8, 1e-10])
    rank = _effective_rank(sv, 1e-6)
    assert rank >= 3


def test_condition_number_proxy_finite() -> None:
    sv = np.array([10.0, 5.0, 2.0, 0.5])
    cond = _condition_number_proxy(sv, 4)
    assert cond > 0
    assert cond < float("inf")


def test_separability_margin_positive() -> None:
    cfg = _cfg()
    rng = np.random.Generator(np.random.PCG64(20260504))
    case = generate_case(0, cfg, rng)
    segments = case["segments"]
    G = _build_forward_matrix(segments, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35], "Bz")
    margin = _separability_margin(segments, G)
    assert margin >= 0.0


def test_layer_misallocation_with_prior() -> None:
    cfg = _cfg()
    rng = np.random.Generator(np.random.PCG64(20260504))
    case = generate_case(0, cfg, rng)
    segments = case["segments"]
    err_np = _layer_misallocation_error(segments, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35], "Bz", False)
    err_wp = _layer_misallocation_error(segments, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35], "Bz", True)
    assert err_np >= 0.0
    assert err_wp >= 0.0


def test_return_confusion_rate_non_negative() -> None:
    cfg = _cfg()
    rng = np.random.Generator(np.random.PCG64(20260504))
    case = generate_case(0, cfg, rng)
    segments = case["segments"]
    rate = _return_confusion_rate(segments, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35], "Bz")
    assert rate >= 0.0


def test_via_auc_computable() -> None:
    cfg = _cfg()
    rng = np.random.Generator(np.random.PCG64(20260504))
    cases = [generate_case(i, cfg, rng) for i in range(6)]
    segs_list = [c["segments"] for c in cases if c["segments"]]
    labels = [1 if c["has_via"] else 0 for c in cases if c["segments"]]
    G_list = [_build_forward_matrix(s, int(cfg["grid_size"]), float(cfg["sensor_fov"]), [0.35], "Bz") for s in segs_list]
    auc = _via_auc(segs_list, G_list, labels)
    assert 0.0 <= auc <= 1.0


def test_run_experiment_writes_passing_metrics(tmp_path: Path) -> None:
    cfg = _cfg()
    outputs = tmp_path / "outputs"
    metrics = run_experiment(cfg, outputs)
    assert metrics["all_acceptance_gates_passed"] is True
    assert (outputs / "metrics.json").exists()
    assert (outputs / "RUN_REPORT.md").exists()
    assert (outputs / "OBSERVABILITY_TABLE.md").exists()
    assert (outputs / "IDENTIFIABILITY_GAIN_TABLE.md").exists()
    assert metrics["case_count"] == cfg["n_cases"]
    assert metrics["n_configurations"] > 0


