from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_all import build_graph, generate_cases, run_experiment, solve_kcl


def _cfg() -> dict:
    return {
        "seed": 20260504,
        "families": 2,
        "variants_per_hypothesis": 3,
        "grid_size": 16,
        "sensor_z": 0.35,
        "source_voltage": 1.0,
        "ground_voltage": 0.0,
        "kcl_residual_threshold": 1e-10,
        "current_closure_threshold": 1e-10,
        "divB_residual_threshold": 2.0,
        "heldout_accuracy_threshold": 0.95,
    }


def test_kcl_solve_conserves_current() -> None:
    graph = build_graph("H1_extra_via", family=0, variant=0, cfg=_cfg())
    solved = solve_kcl(graph)
    assert solved["max_interior_kcl_residual"] < 1e-12
    assert solved["current_closure_error"] < 1e-12
    assert solved["source_current"] > 0
    assert solved["sink_current"] < 0


def test_generated_cases_cover_hypotheses_and_splits() -> None:
    cases = generate_cases(_cfg())
    labels = {case["true_hypothesis"] for case in cases}
    roles = {case["split_role"] for case in cases}
    assert labels == {"H0_nominal_pdn", "H1_extra_via", "H2_return_path_shift", "H3_bend_artifact"}
    assert {"calibration", "heldout"}.issubset(roles)


def test_run_experiment_writes_passing_metrics(tmp_path: Path) -> None:
    metrics = run_experiment(_cfg(), tmp_path / "outputs", tmp_path / "data")
    assert metrics["all_acceptance_gates_passed"] is True
    assert (tmp_path / "outputs" / "metrics.json").exists()
    assert (tmp_path / "outputs" / "RUN_REPORT.md").exists()


def test_gate_fails_when_kcl_threshold_is_impossible(tmp_path: Path) -> None:
    cfg = _cfg()
    cfg["kcl_residual_threshold"] = -1.0
    metrics = run_experiment(cfg, tmp_path / "outputs", tmp_path / "data")
    assert metrics["all_acceptance_gates_passed"] is False
    assert metrics["acceptance_gates"]["kcl_residual_below_threshold"] is False

