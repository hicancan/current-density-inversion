"""Test run output file generation (round 2)."""
import sys
import json
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import numpy as np
import pytest

from reporting import (
    write_metrics_json, write_run_report, write_candidate_ranking,
    write_epsilon_sweep, write_epsilon_candidate_matrix,
    write_ambiguity_reduction, write_claim_intervals_before_after,
    write_near_null_before_after, write_next_measurement_policy,
    write_failure_modes,
)


def test_write_metrics_json(tmp_path):
    metrics = {"test": 1, "nested": {"a": np.float64(1.0), "b": np.int64(2)}}
    write_metrics_json(metrics, tmp_path)
    assert (tmp_path / "metrics.json").exists()
    loaded = json.loads((tmp_path / "metrics.json").read_text())
    assert loaded["test"] == 1


def test_write_run_report_with_breakthrough(tmp_path):
    metrics = {
        "status": "passed_with_limitations",
        "engineering_gates": {"a": True, "epsilon_sweep_present": True},
        "scientific_gates": {
            "any_epsilon_any_candidate_interval_width_reduction_ge_0_20": False,
            "ambiguity_rate_reduction_gt_0": False,
        },
        "engineering_gates_passed": True, "scientific_gates_passed": False,
        "case_count": 24, "candidate_count": 11,
        "baseline_ambiguity_rate": 1.0, "baseline_mean_interval_width": 1.0,
        "baseline_near_null_count": 50, "baseline_effective_rank": 23,
        "best_candidate": "add_h1.6_Bz",
        "best_by_epsilon": {"1.0": {"candidate_id": "A"}, "2.0": {"candidate_id": "B"}},
        "run_audit": {"runtime_s": 5.0},
    }
    write_run_report(metrics, tmp_path)
    assert (tmp_path / "RUN_REPORT.md").exists()


def test_write_epsilon_sweep(tmp_path):
    cand_results = [
        {
            "candidate_id": "c1",
            "epsilon_sweep": [
                {"epsilon_multiplier": 0.5, "epsilon": 0.05, "ambiguity_rate": 0.0, "nonempty_rate": 0.0, "empty_rate": 1.0, "mean_interval_width": 0.0, "wrong_accept_count": 0},
                {"epsilon_multiplier": 1.5, "epsilon": 0.15, "ambiguity_rate": 0.8, "nonempty_rate": 1.0, "empty_rate": 0.0, "mean_interval_width": 0.8, "wrong_accept_count": 0},
            ],
        },
        {
            "candidate_id": "c2",
            "epsilon_sweep": [
                {"epsilon_multiplier": 0.5, "epsilon": 0.05, "ambiguity_rate": 0.0, "nonempty_rate": 0.0, "empty_rate": 1.0, "mean_interval_width": 0.0, "wrong_accept_count": 0},
                {"epsilon_multiplier": 1.5, "epsilon": 0.15, "ambiguity_rate": 0.6, "nonempty_rate": 1.0, "empty_rate": 0.0, "mean_interval_width": 0.6, "wrong_accept_count": 0},
            ],
        },
    ]
    write_epsilon_sweep(cand_results, tmp_path)
    assert (tmp_path / "EPSILON_SWEEP.md").exists()
    content = (tmp_path / "EPSILON_SWEEP.md").read_text(encoding="utf-8")
    assert "epsilon_mult" in content or "Epsilon" in content


def test_write_epsilon_candidate_matrix(tmp_path):
    cand_results = [
        {
            "candidate_id": "c1",
            "epsilon_sweep": [
                {"epsilon_multiplier": 0.5, "mean_interval_width": 0.0, "ambiguity_rate": 0.0},
                {"epsilon_multiplier": 1.5, "mean_interval_width": 0.8, "ambiguity_rate": 0.8},
            ],
        },
        {
            "candidate_id": "c2",
            "epsilon_sweep": [
                {"epsilon_multiplier": 0.5, "mean_interval_width": 0.0, "ambiguity_rate": 0.0},
                {"epsilon_multiplier": 1.5, "mean_interval_width": 0.6, "ambiguity_rate": 0.6},
            ],
        },
    ]
    write_epsilon_candidate_matrix(cand_results, tmp_path)
    assert (tmp_path / "EPSILON_CANDIDATE_MATRIX.md").exists()
    content = (tmp_path / "EPSILON_CANDIDATE_MATRIX.md").read_text(encoding="utf-8")
    assert "c1" in content


def test_write_candidate_ranking_round2(tmp_path):
    ranking = {
        "ranking": [
            {
                "candidate_id": "best_ms", "height_um": 0.0, "components": ["Bz"], "n_states": 2,
                "utility": 0.3,
                "utility_detail": {
                    "utility": 0.3, "method": "median_over_epsilons",
                    "per_epsilon_utilities": {"1.0": 0.2, "2.0": 0.4},
                    "per_epsilon_interval_widths": {"1.0": 0.7, "2.0": 0.9},
                },
            },
        ],
        "best_global": "best_ms", "best_utility": 0.3, "candidate_count": 1, "any_improved": True,
        "best_per_epsilon": {"1.0": {"candidate_id": "best_ms", "utility": 0.2}},
    }
    write_candidate_ranking(ranking, tmp_path)
    assert (tmp_path / "CANDIDATE_RANKING.md").exists()
    content = (tmp_path / "CANDIDATE_RANKING.md").read_text(encoding="utf-8")
    assert "best_ms" in content


def test_write_failure_modes_round2(tmp_path):
    metrics = {
        "status": "passed_with_limitations",
        "scientific_gates": {
            "any_epsilon_any_candidate_interval_width_reduction_ge_0_20": False,
        },
    }
    ranking = {
        "ranking": [
            {"candidate_id": "ok", "utility": 0.1},
            {"candidate_id": "bad", "utility": -0.2},
        ],
    }
    write_failure_modes(metrics, ranking, tmp_path)
    assert (tmp_path / "FAILURE_MODES.md").exists()
    content = (tmp_path / "FAILURE_MODES.md").read_text(encoding="utf-8")
    assert "Breakthrough" in content
