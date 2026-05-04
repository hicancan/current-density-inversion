from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_all import acceptance_gates_from_metrics, run_experiment


def _cfg() -> dict:
    return {
        "seed": 20260504,
        "e11_package_dir": "../E11_chip_like_pdn_distribution",
        "e11_config": "../E11_chip_like_pdn_distribution/configs/default.json",
        "e11_dataset_json": "../E11_chip_like_pdn_distribution/data/e11_dataset.json",
        "ridge_lambda": 0.001,
        "train_roles": ["train"],
        "eval_roles": ["heldout", "family_hidden"],
        "heldout_accuracy_threshold": 0.70,
        "accuracy_gain_vs_majority_threshold": 0.10,
        "family_generalization_gap_threshold": 0.50,
        "kcl_improvement_ratio_threshold": 0.50,
        "closure_improvement_ratio_threshold": 0.50,
        "field_reconstruction_rmse_threshold": 0.50,
    }


def test_run_experiment_writes_physics_learning_metrics(tmp_path: Path) -> None:
    metrics = run_experiment(_cfg(), tmp_path / "outputs", ROOT)
    assert metrics["all_acceptance_gates_passed"] is True
    assert metrics["heldout_accuracy"] > metrics["models"]["majority_baseline"]["heldout_accuracy"]
    assert metrics["predicted_kcl_residual"] < metrics["physics_learning_gain_vs_unconstrained"]["unconstrained_max_kcl_residual"]
    assert metrics["predicted_current_closure_error"] < metrics["physics_learning_gain_vs_unconstrained"]["unconstrained_max_current_closure_error"]
    assert (tmp_path / "outputs" / "metrics.json").exists()


def test_acceptance_fails_when_predicted_kcl_and_closure_fail(tmp_path: Path) -> None:
    metrics = run_experiment(_cfg(), tmp_path / "outputs", ROOT)
    broken = copy.deepcopy(metrics)
    broken["physics_learning_gain_vs_unconstrained"]["kcl_residual_reduction_ratio"] = 0.0
    broken["physics_learning_gain_vs_unconstrained"]["closure_error_reduction_ratio"] = 0.0
    gates = acceptance_gates_from_metrics(broken, _cfg())
    assert gates["all_acceptance_gates_passed"] is False
    assert gates["predicted_kcl_improves_over_unconstrained"] is False
    assert gates["predicted_closure_improves_over_unconstrained"] is False

