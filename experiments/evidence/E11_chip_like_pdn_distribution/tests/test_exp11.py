from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_all import HYPOTHESES, build_graph, connected_components, generate_cases, has_explicit_return_path, run_experiment, solve_kcl


def _cfg() -> dict:
    return {
        "seed": 20260504,
        "families": 3,
        "variants_per_hypothesis": 4,
        "grid_size": 12,
        "sensor_z": 0.42,
        "source_voltage": 1.0,
        "ground_voltage": 0.0,
        "kcl_residual_threshold": 1e-10,
        "current_closure_threshold": 1e-10,
        "divB_residual_threshold": 2.0,
        "heldout_accuracy_threshold": 0.95,
        "family_hidden_accuracy_threshold": 0.90,
        "min_family_heldout_rows_per_hypothesis": 1,
    }


def test_graph_connectivity_and_no_floating_nodes() -> None:
    graph = build_graph("H3_bend_width_artifact", family=1, variant=2, cfg=_cfg())
    components = connected_components(graph)
    assert len(components) == 1
    assert set(graph["nodes"]) == components[0]


def test_kcl_solve_and_current_closure() -> None:
    graph = build_graph("H1_via_defect_or_extra", family=0, variant=1, cfg=_cfg())
    solved = solve_kcl(graph)
    assert solved["max_interior_kcl_residual"] < 1e-12
    assert solved["current_closure_error"] < 1e-12
    assert solved["source_current"] > 0
    assert solved["sink_current"] < 0
    assert abs(solved["source_current"] + solved["sink_current"]) < 1e-12


def test_every_case_has_explicit_return_path() -> None:
    cases = generate_cases(_cfg())
    assert cases
    assert all(has_explicit_return_path(case["graph"]) for case in cases)


def test_hypothesis_rows_are_balanced_across_families() -> None:
    cases = generate_cases(_cfg())
    for family in {case["family"] for case in cases}:
        counts = {
            hypothesis: sum(1 for case in cases if case["family"] == family and case["true_hypothesis"] == hypothesis)
            for hypothesis in HYPOTHESES
        }
        assert min(counts.values()) == max(counts.values())


def test_run_experiment_writes_passing_metrics(tmp_path: Path) -> None:
    metrics = run_experiment(_cfg(), tmp_path / "outputs", tmp_path / "data")
    assert metrics["all_acceptance_gates_passed"] is True
    assert metrics["kcl"]["max_residual"] < 1e-10
    assert metrics["closure"]["max_error"] < 1e-10
    assert (tmp_path / "outputs" / "metrics.json").exists()
    assert (tmp_path / "data" / "e11_dataset.json").exists()

