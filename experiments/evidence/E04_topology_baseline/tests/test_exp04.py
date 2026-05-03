from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("exp04_run_all", ROOT / "src" / "run_all.py")
assert SPEC is not None and SPEC.loader is not None
RUN_ALL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RUN_ALL
SPEC.loader.exec_module(RUN_ALL)

UNetLite = RUN_ALL.UNetLite
load_config = RUN_ALL.load_config
resolve_dataset_path = RUN_ALL.resolve_dataset_path
load_dataset = RUN_ALL.load_dataset
posthoc_topology_projection = RUN_ALL.posthoc_topology_projection
topology_metrics = RUN_ALL.topology_metrics
build_physical_forward_kernels = RUN_ALL.build_physical_forward_kernels
raster_physical_forward = RUN_ALL.raster_physical_forward
build_finite_width_return_forward_kernels = RUN_ALL.build_finite_width_return_forward_kernels
dog_score_maps = RUN_ALL.dog_score_maps
load_pypeec_operator_stress_bridge = RUN_ALL.load_pypeec_operator_stress_bridge
load_pypeec_frozen_inference_dataset = RUN_ALL.load_pypeec_frozen_inference_dataset


def test_dataset_has_required_splits_and_channels():
    cfg = load_config(ROOT / "configs" / "default.json")
    data = load_dataset(resolve_dataset_path(cfg))
    assert data["B_obs"].shape[1] == 3
    assert data["truth"].shape[1] == 5
    counts = {s: int(np.sum(data["split"] == s)) for s in ["train", "val", "test", "ood"]}
    assert all(v > 0 for v in counts.values())


def test_unet_output_shape():
    model = UNetLite(base=8)
    x = torch.zeros(2, 3, 49, 49)
    y = model(x)
    assert tuple(y.shape) == (2, 5, 49, 49)


def test_posthoc_projection_reduces_topology_mse_on_random_prediction():
    rng = np.random.default_rng(0)
    pred = rng.normal(size=(4, 5, 21, 21)).astype(np.float32)
    before = topology_metrics(pred)[0]
    after = topology_metrics(posthoc_topology_projection(pred))[0]
    assert after < before


def test_raster_physical_forward_shape_and_finiteness():
    cfg = load_config(ROOT / "configs" / "default.json")
    data = load_dataset(resolve_dataset_path(cfg))
    forward = build_physical_forward_kernels(data["x"], data["y"], cfg)
    y = np.zeros((2, 5, 49, 49), dtype=np.float32)
    y[:, 0, 24, 10:20] = 1.0
    b = raster_physical_forward(y, forward)
    assert b.shape == (2, 3, 49, 49)
    assert np.all(np.isfinite(b))


def test_finite_width_return_forward_is_distinct_and_finite():
    cfg = load_config(ROOT / "configs" / "default.json")
    data = load_dataset(resolve_dataset_path(cfg))
    low = build_physical_forward_kernels(data["x"], data["y"], cfg)
    high = build_finite_width_return_forward_kernels(data["x"], data["y"], cfg)
    y = data["truth"][data["split"] == "test"][:3]
    b_low = raster_physical_forward(y, low)
    b_high = raster_physical_forward(y, high)
    assert b_high.shape == b_low.shape
    assert np.all(np.isfinite(b_high))
    assert np.linalg.norm(b_high - b_low) / (np.linalg.norm(b_low) + 1e-30) > 0.02


def test_dog_score_maps_suppresses_broad_background():
    broad = np.ones((2, 17, 17), dtype=np.float32)
    broad[:, 8, 8] = 2.0
    filtered = dog_score_maps(broad, sigma_px=2.0)
    assert filtered.shape == broad.shape
    assert np.all(filtered >= 0.0)
    assert float(np.median(filtered)) < float(np.max(filtered))


def test_pypeec_operator_stress_bridge_reads_exp07_artifact():
    cfg = load_config(ROOT / "configs" / "default.json")
    bridge = load_pypeec_operator_stress_bridge(cfg)
    assert bridge["enabled"] is True
    assert bridge["artifact_available"] is True
    assert bridge["used_for_training"] is False
    assert bridge["used_for_validation_thresholds"] is False
    assert bridge["exp07_all_gates_passed"] is True
    assert bridge["n_cases_completed"] >= cfg["pypeec_operator_stress_bridge"]["required_cases_completed"]
    assert bridge["exp03_like_shape_gap_median"] >= cfg["pypeec_operator_stress_bridge"]["min_exp03_like_shape_gap"]


def test_pypeec_frozen_inference_dataset_is_available_and_exp04_compatible():
    cfg = load_config(ROOT / "configs" / "default.json")
    data = load_pypeec_frozen_inference_dataset(cfg)
    assert data["enabled"] is True
    assert data["artifact_available"] is True
    assert data["B_pypeec"].shape[-1] == 3
    assert data["B_centerline"].shape == data["B_pypeec"].shape
    assert data["truth"].shape[0] == data["B_pypeec"].shape[0]
    assert data["truth"].shape[1] == 5
    assert data["truth"].shape[2:] == data["B_pypeec"].shape[1:3]
    assert int(data["B_pypeec"].shape[0]) >= cfg["pypeec_frozen_inference"]["min_cases"]
    assert set(data["split"].tolist()) == {"pypeec_test"}
    assert np.sum(data["is_exp03_like"]) >= cfg["pypeec_frozen_inference"]["min_exp03_like_cases"]
    assert np.all(np.isfinite(data["B_pypeec"]))
    assert np.all(np.isfinite(data["truth"]))


def test_reference_outputs_pass_acceptance_gates():
    metrics_path = ROOT / "outputs" / "metrics.json"
    assert metrics_path.exists()
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert metrics["all_acceptance_gates_passed"] is True
    assert metrics["acceptance_gates"]["lambda_sweep_finds_stronger_topology_tradeoff"]["pass"] is True
    assert metrics["acceptance_gates"]["multi_seed_topology_mse_reduction_is_stable"]["pass"] is True
    assert metrics["acceptance_gates"]["robust_channel_metrics_are_finite"]["pass"] is True
    assert metrics["acceptance_gates"]["stress_topology_mse_reduction_is_stable"]["pass"] is True
    assert metrics["acceptance_gates"]["physical_reforward_metrics_are_finite"]["pass"] is True
    assert metrics["acceptance_gates"]["physics_tikhonov_baseline_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["residual_via_detector_beats_raw_adjoint"]["pass"] is True
    assert metrics["acceptance_gates"]["oracle_residual_detector_is_upper_bound"]["pass"] is True
    assert metrics["acceptance_gates"]["fp_controlled_residual_detector_reduces_ood_false_positives"]["pass"] is True
    assert metrics["acceptance_gates"]["finite_width_return_operator_stress_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["finite_width_return_detail_metrics_are_finite"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_operator_stress_bridge_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_operator_stress_gap_is_material_and_bounded"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_frozen_inference_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_frozen_inference_metrics_are_finite"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_frozen_inference_subsets_are_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_null_via_diagnostics_are_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_return_path_diagnostics_are_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_failure_diagnostics_are_finite"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_mechanism_summaries_are_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["null_via_hypothesis_gate_is_calibrated_without_pypeec"]["pass"] is True
    assert metrics["acceptance_gates"]["null_via_hypothesis_gate_validation_metrics_are_finite"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_null_via_hypothesis_gate_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_null_via_hypothesis_gate_metrics_are_finite"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_null_via_gate_pareto_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_null_via_gate_case_studies_are_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_hypothesis_evidence_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_heldout_split_protocol_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_return_path_hypothesis_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_uncertainty_refusal_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_generative_hypothesis_scoring_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_selective_risk_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_return_current_generator_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_heldout_split_evaluation_is_reported"]["pass"] is True
    assert metrics["acceptance_gates"]["real_pypeec_frozen_inference_cost_is_bounded"]["pass"] is True
    assert metrics["acceptance_gates"]["two_stage_refinement_is_reported_and_bounded"]["pass"] is True
    assert metrics["via_detection_benchmark"]["calibration_split"] == "val"
    assert metrics["two_stage_refiner"]["calibration_split"] == "val"
    assert "unet_topology_soft_loss" in metrics["benchmark"]["test"]
    assert "unet_topology_two_stage_refined" in metrics["benchmark"]["test"]
    assert "physics_tikhonov" in metrics["benchmark"]["test"]
    assert "via_detection_benchmark" in metrics
    assert "finite_width_return" in metrics["stress_benchmark"]
    assert metrics["pypeec_operator_stress_bridge"]["exp07_all_gates_passed"] is True
    assert metrics["pypeec_operator_stress_bridge"]["used_for_training"] is False
    assert metrics["pypeec_frozen_inference"]["artifact_available"] is True
    assert metrics["pypeec_frozen_inference"]["used_for_training"] is False
    assert metrics["pypeec_frozen_inference"]["used_for_validation_thresholds"] is False
    assert metrics["pypeec_frozen_inference"]["used_for_calibration"] is False
    assert "unet_topology_soft_loss" in metrics["pypeec_frozen_inference"]["methods"]
    assert "exp03_like" in metrics["pypeec_frozen_inference"]["subsets"]
    assert metrics["pypeec_frozen_inference"]["subsets"]["exp03_like"]["n_cases"] >= 30
    null_diag = metrics["pypeec_frozen_inference"]["null_via_diagnostics"]
    return_diag = metrics["pypeec_frozen_inference"]["return_path_diagnostics"]
    assert null_diag["n_cases"] > 0
    assert return_diag["n_cases"] > 0
    assert set(null_diag["summary"]) >= {
        "unet_no_topology",
        "unet_topology_soft_loss",
        "unet_topology_two_stage_refined",
    }
    assert set(return_diag["summary"]) >= {
        "unet_no_topology",
        "unet_topology_soft_loss",
        "unet_topology_two_stage_refined",
    }
    assert len(null_diag["rows"]) >= 3 * null_diag["n_cases"]
    assert len(return_diag["rows"]) >= 3 * return_diag["n_cases"]
    assert "unet_topology_soft_loss" in null_diag["mechanism_summary"]
    assert "unet_topology_soft_loss" in return_diag["mechanism_summary"]
    assert len(null_diag.get("failure_figure_paths", [])) > 0
    assert null_diag["mechanism_summary"]["unet_topology_soft_loss"]["n_false_positives"] > 0
    assert return_diag["mechanism_summary"]["unet_topology_soft_loss"]["n_cases"] > 0
    gate = metrics["null_via_hypothesis_gate"]
    assert gate["enabled"] is True
    assert gate["calibration_split"] == "val_synthetic_null_via_stress"
    assert gate["used_for_pypeec_threshold_selection"] is False
    assert gate["used_for_pypeec_calibration"] is False
    families = {row["family"] for row in gate["validation_family_rows"]}
    assert {
        "synthetic_null_via_bend_corner_stress",
        "synthetic_null_via_strong_local_b_gap_stress",
        "synthetic_null_via_return_path_stress",
        "synthetic_null_via_operator_gap_stress",
        "synthetic_null_via_layer_allocation_stress",
        "true_via_near_bend_corner_strong_stress",
        "true_via_layer_allocation_stress",
    }.issubset(families)
    pypeec_gate = metrics["pypeec_frozen_inference"]["null_via_hypothesis_gate"]
    assert pypeec_gate["enabled"] is True
    assert pypeec_gate["calibration_split"] == "val_synthetic_null_via_stress"
    assert pypeec_gate["used_for_pypeec_threshold_selection"] is False
    assert pypeec_gate["used_for_pypeec_calibration"] is False
    assert set(pypeec_gate["models"]) >= {
        "unet_no_topology",
        "unet_topology_soft_loss",
        "unet_topology_two_stage_refined",
    }
    assert "topology_model_no_via_fp_before" in pypeec_gate["summary"]
    assert "topology_model_no_via_fp_after" in pypeec_gate["summary"]
    assert len(pypeec_gate["decision_rows"]) >= metrics["pypeec_frozen_inference"]["n_cases"] * 3
    assert len(pypeec_gate["pareto_rows"]) >= 5
    assert any(row["selected"] for row in pypeec_gate["pareto_rows"])
    assert pypeec_gate.get("pareto_plot_path")
    assert len(pypeec_gate.get("case_figure_paths", [])) > 0
    evidence = metrics["pypeec_frozen_inference"]["null_via_hypothesis_evidence"]
    assert evidence["enabled"] is True
    assert evidence["used_for_pypeec_threshold_selection"] is False
    assert len(evidence["rows"]) >= metrics["pypeec_frozen_inference"]["n_cases"] * 3
    assert "unet_topology_soft_loss" in evidence["summary"]
    assert "high_confidence_via_fraction" in evidence["summary"]["unet_topology_soft_loss"]
    generative = metrics["pypeec_frozen_inference"]["null_via_generative_hypothesis"]
    assert generative["enabled"] is True
    assert generative["used_for_pypeec_threshold_selection"] is False
    assert len(generative["rows"]) >= metrics["pypeec_frozen_inference"]["n_cases"] * 3
    assert len(generative["calibration_rows"]) >= 3
    assert "unet_topology_soft_loss" in generative["summary"]
    assert "auc_true_via_vs_no_via" in generative["summary"]["unet_topology_soft_loss"]
    assert generative.get("calibration_plot_path")
    selective = metrics["pypeec_frozen_inference"]["selective_risk"]
    assert selective["enabled"] is True
    assert "unet_topology_soft_loss" in selective["summary"]
    assert len(selective["rows"]) >= 15
    assert selective.get("plot_path")
    heldout = metrics["pypeec_frozen_inference"]["heldout_split_protocol"]
    assert heldout["current_protocol"] == "frozen_no_calibration"
    assert heldout["used_for_current_threshold_selection"] is False
    assert len(heldout["rows"]) == metrics["pypeec_frozen_inference"]["n_cases"]
    assert "no_via" in heldout["family_summary"]
    heldout_eval = metrics["pypeec_frozen_inference"]["heldout_split_evaluation"]
    assert heldout_eval["enabled"] is True
    assert heldout_eval["used_for_current_threshold_selection"] is False
    assert {"future_calibration_candidate", "future_heldout_test"}.issubset(set(heldout_eval["role_summary"]))
    assert "hypothesis_summary" in return_diag
    assert "unet_topology_soft_loss" in return_diag["hypothesis_summary"]
    return_gen = metrics["pypeec_frozen_inference"]["return_current_aware_generator"]
    assert return_gen["enabled"] is True
    assert return_gen["used_for_model_prediction"] is False
    assert return_gen["summary"]["n_cases"] > 0
    refusal = metrics["pypeec_frozen_inference"]["uncertainty_refusal"]
    assert refusal["enabled"] is True
    assert "unet_topology_soft_loss" in refusal["summary"]
    assert metrics["via_detection_benchmark"]["splits"]["test"]["raw_adjoint"]["via_hit_rate_within_2px"] < 0.1
    assert metrics["via_detection_benchmark"]["splits"]["test"]["unet_topology_soft_loss_sheet_residual"]["via_hit_rate_within_2px"] > 0.8
    assert (
        metrics["via_detection_benchmark"]["splits"]["ood"]["unet_topology_soft_loss_sheet_residual_dog_fp_controlled"]["via_false_positive_rate_no_via"]
        <= metrics["via_detection_benchmark"]["splits"]["ood"]["unet_topology_soft_loss_sheet_residual"]["via_false_positive_rate_no_via"]
    )
    ch = metrics["benchmark"]["test"]["unet_topology_soft_loss"]
    assert all(np.isfinite(v) for v in ch["per_channel_rmse_current_scale"])
    assert len(ch["per_channel_rel_l2"]) == 5
    assert metrics["lambda_sweep_summary"]["best_test_topology_ratio"] < 0.5
    assert metrics["multi_seed_summary"]["topology_mse_ratio_mean"] < 1.0
    assert metrics["stress_summary"]["topology_mse_ratio_mean"] < 1.0
    assert (ROOT / "outputs" / "RUN_REPORT.md").exists()
    assert (ROOT / "outputs" / "METRICS_TABLE.md").exists()
    assert (ROOT / "outputs" / "CHANNEL_METRICS_TABLE.md").exists()
    assert (ROOT / "outputs" / "STRESS_METRICS_TABLE.md").exists()
    assert (ROOT / "outputs" / "OPERATOR_STRESS_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_OPERATOR_STRESS_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_FROZEN_INFERENCE_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_FROZEN_INFERENCE_SUBSET_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_NULL_VIA_DIAGNOSTICS_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_NULL_VIA_MECHANISM_SUMMARY.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_NULL_VIA_FAILURE_CASES.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_RETURN_PATH_DIAGNOSTICS_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_RETURN_PATH_MECHANISM_SUMMARY.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_RETURN_PATH_FAILURE_MODES.md").exists()
    assert (ROOT / "outputs" / "NULL_VIA_VALIDATION_STRESS_TABLE.md").exists()
    assert (ROOT / "outputs" / "NULL_VIA_HYPOTHESIS_GATE_TABLE.md").exists()
    assert (ROOT / "outputs" / "NULL_VIA_GATE_PARETO_TABLE.md").exists()
    assert (ROOT / "outputs" / "NULL_VIA_HYPOTHESIS_EVIDENCE_TABLE.md").exists()
    assert (ROOT / "outputs" / "NULL_VIA_GENERATIVE_HYPOTHESIS_TABLE.md").exists()
    assert (ROOT / "outputs" / "NULL_VIA_SELECTIVE_RISK_TABLE.md").exists()
    assert (ROOT / "outputs" / "NULL_VIA_UNCERTAINTY_REFUSAL_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_HELDOUT_SPLIT_PROTOCOL.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_HELDOUT_SPLIT_EVALUATION_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_RETURN_PATH_HYPOTHESIS_TABLE.md").exists()
    assert (ROOT / "outputs" / "PYPEEC_RETURN_CURRENT_AWARE_GENERATOR_TABLE.md").exists()
    assert any((ROOT / "outputs" / path).exists() for path in null_diag["failure_figure_paths"])
    assert (ROOT / "outputs" / pypeec_gate["pareto_plot_path"]).exists()
    assert any((ROOT / "outputs" / path).exists() for path in pypeec_gate["case_figure_paths"])
    assert (ROOT / "outputs" / generative["calibration_plot_path"]).exists()
    assert (ROOT / "outputs" / selective["plot_path"]).exists()
    assert (ROOT / "outputs" / "VIA_DETECTOR_TABLE.md").exists()
    assert (ROOT / "STRICT_DETECTOR_NO_LEAKAGE_PROTOCOL.md").exists()
