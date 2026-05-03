from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

EXP_DIR = Path(__file__).resolve().parents[1]
SRC = EXP_DIR / "src"
for module_name in [
    "geometry",
    "reference_biot_savart",
    "pypeec_adapter",
    "exp07_metrics",
]:
    sys.modules.pop(module_name, None)
sys.path.insert(0, str(SRC))

from exp07_metrics import via_bz_over_bxy
from geometry import make_case, make_sensor_grid
from pypeec_adapter import build_pypeec_model, detect_pypeec
from reference_biot_savart import field_from_segments, reshape_field


def load_cfg() -> dict:
    return json.loads((EXP_DIR / "configs" / "default.json").read_text())


def test_real_pypeec_api_is_required_and_available():
    detection = detect_pypeec()
    assert detection["python_module_available"] is True
    assert detection["python_package_version"]
    assert detection["api_functions_found"]["run_mesher_data"] is True
    assert detection["api_functions_found"]["run_solver_data"] is True


def test_pypeec_model_uses_real_api_contract():
    cfg = load_cfg()
    grid = make_sensor_grid(n=9, fov_m=0.6e-3, z_m=80e-6)
    case = make_case("straight_trace", cfg)
    model = build_pypeec_model(case, grid, cfg)
    assert model.geometry["mesh_type"] == "voxel"
    assert model.geometry["data_point"]["pts_cloud"]
    assert model.problem["source_def"]["src"]["source_type"] == "current"
    assert model.problem["source_val"]["src"]["I_re"] == cfg["currents"]["default_current_a"]
    assert model.problem["source_val"]["src"]["Y_re"] == 0.0
    assert model.index_counts["src"] == 1
    assert model.index_counts["sink"] == 1
    assert model.index_counts["wire"] > 0
    assert model.cross_section_fill is True
    assert model.n_centerline_voxel > 0


def test_finite_width_case_uses_more_pypeec_voxels():
    cfg = load_cfg()
    grid = make_sensor_grid(n=9, fov_m=0.6e-3, z_m=80e-6)
    straight = build_pypeec_model(make_case("straight_trace", cfg), grid, cfg)
    wide = build_pypeec_model(make_case("finite_width_trace", cfg), grid, cfg)
    n_straight = sum(straight.index_counts.values())
    n_wide = sum(wide.index_counts.values())
    assert n_wide > n_straight
    assert wide.n_centerline_voxel == straight.n_centerline_voxel


def test_exp03_like_cases_build_connected_pypeec_models():
    cfg = load_cfg()
    grid = make_sensor_grid(n=9, fov_m=0.6e-3, z_m=80e-6)
    exp03_like = cfg["exp03_like_subset"]["cases"]
    target_base_cases = {
        case_name
        for cases in cfg.get("pypeec_distribution_targets", {})
        .get("base_cases_by_hypothesis", {})
        .values()
        for case_name in cases
    }
    assert set(exp03_like).issubset(set(cfg["cases"]) | target_base_cases)
    for case_name in exp03_like:
        model = build_pypeec_model(make_case(case_name, cfg), grid, cfg)
        assert model.index_counts["src"] == 1
        assert model.index_counts["sink"] == 1
        assert model.index_counts["wire"] > 0
        assert model.n_centerline_voxel > 2
        assert model.cross_section_fill is True


def test_exp03_like_variant_case_preserves_connected_model_contract():
    cfg = load_cfg()
    grid = make_sensor_grid(n=9, fov_m=0.6e-3, z_m=80e-6)
    case = make_case("dense_via_background__v03", cfg)
    assert case.expected_physics["variant_of"] == "dense_via_background"
    assert case.expected_physics["exp03_like"] is True
    model = build_pypeec_model(case, grid, cfg)
    assert model.index_counts["src"] == 1
    assert model.index_counts["sink"] == 1
    assert model.index_counts["wire"] > 0
    assert model.cross_section_fill is True


def test_single_via_reference_has_near_zero_bz_over_bxy():
    cfg = load_cfg()
    grid = make_sensor_grid(n=21, fov_m=0.8e-3, z_m=80e-6)
    case = make_case("single_via", cfg)
    flat = field_from_segments(grid.points, case.segments, n_sub=12)
    B = reshape_field(flat, grid.shape)
    assert via_bz_over_bxy(B) <= 1e-10


def test_real_pypeec_outputs_pass_acceptance_gates():
    metrics_path = EXP_DIR / "outputs" / "metrics.json"
    assert metrics_path.exists()
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    cfg = load_cfg()
    assert metrics["all_acceptance_gates_passed"] is True
    assert metrics["backend_mode_executed"] == "real_pypeec_api"
    assert metrics["n_cases_completed"] == metrics["n_cases_requested"]
    assert metrics["n_cases_completed"] >= len(cfg["cases"])
    assert metrics["acceptance_gates"]["real_pypeec_backend_executed_for_all_cases"] is True
    assert metrics["acceptance_gates"]["source_current_matches_target"] is True
    assert metrics["acceptance_gates"]["finite_width_pypeec_geometry_is_wider"] is True
    assert metrics["acceptance_gates"]["voxel_convergence_sweep_completed"] is True
    assert metrics["acceptance_gates"]["voxel_convergence_finest_step_is_bounded"] is True
    assert metrics["acceptance_gates"]["exp03_like_pypeec_subset_completed"] is True
    assert metrics["acceptance_gates"]["exp03_like_shape_gap_is_finite_and_bounded"] is True
    assert metrics["acceptance_gates"]["pypeec_exp03_like_mini_dataset_written"] is True
    if cfg.get("pypeec_distribution_targets", {}).get("enabled", False):
        assert metrics["acceptance_gates"]["pypeec_distribution_targets_are_met"] is True
        counts = metrics["summary"]["pypeec_distribution_expansion"]["case_count_by_hypothesis"]
        targets = cfg["pypeec_distribution_targets"]["target_cases_per_hypothesis"]
        for hypothesis, target in targets.items():
            assert int(counts[hypothesis]) >= int(target)
    assert metrics["summary"]["exp03_like_case_count"] >= cfg["acceptance_thresholds"]["min_exp03_like_case_count"]
    assert metrics["summary"]["max_terminal_current_rel_error"] <= 0.02
    assert metrics["summary"]["finite_width_over_straight_voxel_ratio"] > 1.1
    assert metrics["summary"]["max_finest_step_convergence_shape_delta"] <= cfg["acceptance_thresholds"]["max_finest_step_convergence_shape_delta"]
    assert np.isfinite(metrics["summary"]["pypeec_centerline_shape_gap_median"])
    assert (EXP_DIR / "outputs" / "RUN_REPORT.md").exists()
    assert (EXP_DIR / "outputs" / "SOLVER_CROSS_VALIDATION_TABLE.md").exists()
    assert (EXP_DIR / "outputs" / "VOXEL_CONVERGENCE_TABLE.md").exists()
    assert (EXP_DIR / "outputs" / "01_case_pypeec_gap_summary.svg").exists()


def test_pypeec_exp03_like_mini_dataset_is_exp04_compatible():
    path = EXP_DIR / "data" / "pypeec_exp03_like_mini_dataset.npz"
    assert path.exists()
    data = np.load(path, allow_pickle=False)
    assert data["B_pypeec"].shape[-1] == 3
    assert data["B_centerline"].shape == data["B_pypeec"].shape
    assert data["truth"].shape[1] == 5
    assert data["truth"].shape[0] == data["B_pypeec"].shape[0]
    assert np.all(np.isfinite(data["B_pypeec"]))
    assert np.all(np.isfinite(data["truth"]))
    assert int(np.sum(data["is_exp03_like"])) >= load_cfg()["acceptance_thresholds"]["min_exp03_like_case_count"]
    assert set(data["split"].astype(str).tolist()) == {"pypeec_test"}
