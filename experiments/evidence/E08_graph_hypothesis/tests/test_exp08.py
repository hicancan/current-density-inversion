from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sys

EXP_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = EXP_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from graph_id.forward import field_from_segments, make_observation_grid
from graph_id.generator import _make_case, generate_dataset
from graph_id.importers import case_record_from_json
from graph_id.solver import score_hypotheses, via_evidence
from graph_id.types import Segment


def load_cfg() -> dict:
    return json.loads((EXP_DIR / "configs" / "default.json").read_text(encoding="utf-8"))


def test_forward_superposition_linearity() -> None:
    grid = make_observation_grid(n=9, fov_m=1e-3)
    seg1 = Segment("a", "L1", "edge", (-3e-4, 0, -8e-5), (3e-4, 0, -8e-5))
    seg2 = Segment("b", "L2", "edge", (0, -3e-4, -1.2e-4), (0, 3e-4, -1.2e-4))
    b_sum = field_from_segments([seg1, seg2], {"a": 0.002, "b": -0.001}, grid)
    b_parts = field_from_segments([seg1], {"a": 0.002}, grid) + field_from_segments([seg2], {"b": -0.001}, grid)
    assert np.allclose(b_sum, b_parts, rtol=1e-12, atol=1e-18)


def test_dataset_contains_all_required_classes() -> None:
    cfg = load_cfg()
    records = generate_dataset(cfg)
    classes = {r.class_label for r in records}
    assert set(cfg["dataset"]["classes"]).issubset(classes)
    splits = {r.split for r in records}
    assert {"val", "test", "ood"}.issubset(splits)
    assert all(r.via_candidates for r in records)
    assert all(r.return_candidates for r in records)
    assert all(r.artifact_candidates for r in records)


def test_true_via_has_positive_h1_h0_evidence_in_low_noise_case() -> None:
    cfg = load_cfg()
    cfg["dataset"]["noise_std_relative_to_max_abs_b"]["val"] = 0.0
    grid = make_observation_grid(cfg["grid"]["n"], cfg["grid"]["fov_m"])
    rng = np.random.default_rng(123)
    rec = _make_case(0, "val", "true_via", rng, cfg)
    results = score_hypotheses(rec, grid, cfg, complexity_penalty=0.0)
    assert via_evidence(results) > -1e-8
    assert results["H1_sheet_via"].residual_rel_l2 <= results["H0_sheet_only"].residual_rel_l2 + 1e-8


def test_hypothesis_scores_are_finite() -> None:
    cfg = load_cfg()
    grid = make_observation_grid(cfg["grid"]["n"], cfg["grid"]["fov_m"])
    rec = generate_dataset(cfg)[0]
    results = score_hypotheses(rec, grid, cfg, complexity_penalty=0.001)
    assert set(results) == set(cfg["scoring"]["hypotheses"])
    for result in results.values():
        assert np.isfinite(result.score)
        assert np.isfinite(result.residual_rel_l2)
        assert result.n_basis >= 1


def test_graph_case_json_importer_accepts_minimal_external_case() -> None:
    payload = {
        "case_id": "json_schema_smoke",
        "split": "external",
        "class_label": "no_via",
        "hypothesis_label": "H0_sheet_only",
        "b_obs": np.zeros((3, 3, 3)).tolist(),
        "sheet_segments": [
            {
                "name": "edge",
                "layer": "L1",
                "kind": "edge",
                "prior_group": "sheet",
                "start": [-1e-4, 0.0, -5e-5],
                "end": [1e-4, 0.0, -5e-5],
            }
        ],
        "via_candidates": [],
        "return_candidates": [],
        "artifact_candidates": [],
    }
    rec = case_record_from_json(payload)
    assert rec.case_id == "json_schema_smoke"
    assert rec.b_obs.shape == (3, 3, 3)
    assert rec.sheet_segments[0].prior_group == "sheet"


def test_exp08_outputs_pass_scientific_gates() -> None:
    metrics_path = EXP_DIR / "outputs" / "metrics.json"
    assert metrics_path.exists()
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    gates = metrics["acceptance_gates"]
    assert gates["all_scientific_gates_passed"] is True
    assert gates["graph_ood_accuracy_is_material"] is True
    assert gates["graph_ood_no_via_accuracy_is_material"] is True
    assert gates["graph_ood_true_via_accuracy_is_material"] is True
    assert gates["graph_ood_return_path_accuracy_is_material"] is True
    assert gates["pypeec_graph_bridge_available"] is True
    assert gates["pypeec_bridge_exposes_solver_gap"] is True
    assert gates["hidden_mechanism_is_nontrivial"] is True
    assert gates["via_location_marginalization_is_evaluated"] is True
    assert gates["via_location_marginalization_improves_shifted_via"] is True
    assert gates["pypeec_aware_basis_bank_is_evaluated"] is True
    assert gates["model_selection_calibration_is_evaluated"] is True
    assert gates["pypeec_heldout_model_selection_is_evaluated"] is True
    assert gates["h0_h1_tradeoff_curve_is_evaluated"] is True
    assert gates["pypeec_model_selection_stability_is_evaluated"] is True
    assert gates["pypeec_class_specific_selective_is_evaluated"] is True
    assert gates["pypeec_stacked_evidence_calibrator_is_evaluated"] is True
    assert gates["pypeec_stacked_group_heldout_is_evaluated"] is True
    assert gates["pypeec_stacked_group_distance_refusal_is_evaluated"] is True
    assert gates["pypeec_family_fewshot_adaptation_is_evaluated"] is True
    assert gates["stacked_evidence_feature_ablation_is_evaluated"] is True
    assert gates["stacked_evidence_unknown_safety_is_evaluated"] is True
    assert gates["stacked_evidence_distance_ood_is_evaluated"] is True
    assert gates["stacked_evidence_near_boundary_hidden_is_evaluated"] is True
    assert gates["stacked_evidence_near_hidden_severity_is_evaluated"] is True
    assert gates["near_hidden_accepted_cases_are_audited"] is True
    assert gates["stacked_evidence_space_diagnostics_are_evaluated"] is True
    assert gates["pypeec_stacked_external_stress_is_evaluated"] is True
    assert gates["stacked_evidence_selective_risk_is_evaluated"] is True
    assert gates["pypeec_distribution_gap_is_evaluated"] is True
    assert gates["disciplined_model_bank_is_documented"] is True
    assert gates["global_registration_search_is_evaluated"] is True
    assert gates["unknown_rejection_catches_hidden_mechanisms"] is True
    assert gates["unknown_risk_coverage_is_evaluated"] is True
    assert gates["unknown_detector_ablation_is_evaluated"] is True
    assert gates["unknown_safety_benchmark_is_evaluated"] is True
    assert gates["unknown_accepted_hidden_risk_is_evaluated"] is True
    assert gates["unknown_physical_evidence_ablation_is_evaluated"] is True
    assert gates["h0_hard_negatives_are_evaluated"] is True
    assert gates["multistate_joint_not_worse_than_single"] is True
    assert gates["multistate_design_scan_is_evaluated"] is True
    assert gates["multistate_label_free_design_is_evaluated"] is True
    assert gates["active_design_objective_is_evaluated"] is True
    assert gates["active_design_constraints_are_evaluated"] is True
    assert gates["registration_stress_curve_is_evaluated"] is True
    assert gates["registration_standoff_tilt_stress_is_evaluated"] is True
    assert metrics["hypothesis_identification"]["ood"]["accuracy"] >= 0.70
    assert metrics["via_detection"]["graph_h1_h0"]["ood"]["auc"] >= metrics["via_detection"]["sheet_residual_template"]["ood"]["auc"] - 1e-9
    for rel in [
        "RUN_REPORT.md",
        "HYPOTHESIS_IDENTIFICATION_TABLE.md",
        "HYPOTHESIS_PER_CLASS_TABLE.md",
        "VIA_HYPOTHESIS_TEST_TABLE.md",
        "SELECTIVE_RISK_TABLE.md",
        "FAILURE_CASES_TABLE.md",
        "PYPEEC_GRAPH_BRIDGE_TABLE.md",
        "PYPEEC_GRAPH_BRIDGE_FAILURE_CASES.md",
        "PYPEEC_AWARE_BASIS_TABLE.md",
        "MODEL_EVIDENCE_SELECTION_TABLE.md",
        "PYPEEC_MODEL_BANK_EVIDENCE_TABLE.md",
        "MODEL_SELECTION_CALIBRATION_TABLE.md",
        "PYPEEC_MODEL_BANK_ALLOWED_BASIS_TABLE.md",
        "PYPEEC_HELDOUT_SPLIT_TABLE.md",
        "PYPEEC_HELDOUT_MODEL_SELECTION_TABLE.md",
        "H0_H1_MODEL_SELECTION_TRADEOFF_TABLE.md",
        "PYPEEC_MODEL_SELECTION_STABILITY_TABLE.md",
        "PYPEEC_CLASS_SPECIFIC_SELECTIVE_TABLE.md",
        "PYPEEC_STACKED_EVIDENCE_CALIBRATOR_TABLE.md",
        "PYPEEC_STACKED_EVIDENCE_GROUP_HELDOUT_TABLE.md",
        "PYPEEC_STACKED_EVIDENCE_GROUP_DISTANCE_REFUSAL_TABLE.md",
        "PYPEEC_FAMILY_FEWSHOT_ADAPTATION_TABLE.md",
        "STACKED_EVIDENCE_FEATURE_ABLATION_TABLE.md",
        "STACKED_EVIDENCE_UNKNOWN_SAFETY_TABLE.md",
        "STACKED_EVIDENCE_NEAR_BOUNDARY_HIDDEN_TABLE.md",
        "STACKED_EVIDENCE_NEAR_HIDDEN_SEVERITY_TABLE.md",
        "NEAR_HIDDEN_ACCEPTED_CASES.md",
        "STACKED_EVIDENCE_SPACE_DIAGNOSTICS_TABLE.md",
        "PYPEEC_STACKED_EVIDENCE_EXTERNAL_STRESS_TABLE.md",
        "STACKED_EVIDENCE_SELECTIVE_RISK_TABLE.md",
        "PYPEEC_DISTRIBUTION_GAP_TABLE.md",
        "H0_HARD_NEGATIVE_TABLE.md",
        "PYPEEC_BRIDGE_REGISTRATION_TABLE.md",
        "PYPEEC_BRIDGE_GLOBAL_REGISTRATION_TABLE.md",
        "HIDDEN_MECHANISM_STRESS_TABLE.md",
        "HIDDEN_MECHANISM_FAILURE_CASES.md",
        "REGISTRATION_MARGINALIZATION_TABLE.md",
        "UNKNOWN_REJECTION_TABLE.md",
        "UNKNOWN_RISK_COVERAGE_TABLE.md",
        "UNKNOWN_DETECTOR_ABLATION_TABLE.md",
        "UNKNOWN_SAFETY_BENCHMARK.md",
        "UNKNOWN_ACCEPTED_HIDDEN_RISK_TABLE.md",
        "UNKNOWN_PHYSICAL_EVIDENCE_ABLATION_TABLE.md",
        "MULTISTATE_IDENTIFICATION_TABLE.md",
        "MULTISTATE_DESIGN_TABLE.md",
        "MULTISTATE_EXPERIMENTAL_DESIGN_TABLE.md",
        "ACTIVE_DESIGN_OBJECTIVE_TABLE.md",
        "ACTIVE_DESIGN_CONSTRAINT_TABLE.md",
        "REGISTRATION_STRESS_CURVE.md",
    ]:
        assert (EXP_DIR / "outputs" / rel).exists()
    assert (EXP_DIR / "outputs" / "stacked_evidence_space_pca.png").exists()
