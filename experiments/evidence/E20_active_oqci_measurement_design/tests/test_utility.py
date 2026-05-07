"""Test valid disambiguation utility scoring (round 3)."""
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import numpy as np
import pytest

from utility import compute_valid_utility, rank_candidates


def test_valid_utility_perfect():
    """All cases validly disambiguated."""
    cr = {
        "candidate_id": "perfect",
        "cost": 1.0,
        "epsilon_sweep": [
            {"epsilon_multiplier": 1.5, "valid_disambiguation_rate": 1.0,
             "truth_in_consistent_set_rate": 1.0, "singleton_wrong_rate": 0.0,
             "empty_rate": 0.0},
        ],
    }
    util = compute_valid_utility(cr)
    # 1.0 + 0.5*1.0 - 2.0*0 - 1.0*0 - 1.0 = 0.5
    assert abs(util["utility"] - 0.5) < 0.001
    assert util["method"] == "valid_disambiguation"


def test_valid_utility_empty():
    """All cases empty consistent sets."""
    cr = {
        "candidate_id": "empty",
        "cost": 1.0,
        "epsilon_sweep": [
            {"epsilon_multiplier": 0.5, "valid_disambiguation_rate": 0.0,
             "truth_in_consistent_set_rate": 0.0, "singleton_wrong_rate": 0.0,
             "empty_rate": 1.0},
        ],
    }
    util = compute_valid_utility(cr)
    # 0 + 0.5*0 - 2.0*0 - 1.0*1.0 - 1.0 = -2.0
    assert abs(util["utility"] - (-2.0)) < 0.001


def test_valid_utility_singleton_wrong():
    """Singleton but wrong hypothesis."""
    cr = {
        "candidate_id": "wrong",
        "cost": 0.4,
        "epsilon_sweep": [
            {"epsilon_multiplier": 2.0, "valid_disambiguation_rate": 0.0,
             "truth_in_consistent_set_rate": 0.0, "singleton_wrong_rate": 0.5,
             "empty_rate": 0.0},
        ],
    }
    util = compute_valid_utility(cr)
    # 0 + 0.5*0 - 2.0*0.5 - 1.0*0 - 0.4 = -1.4
    assert abs(util["utility"] - (-1.4)) < 0.001


def test_valid_utility_partial():
    """Partial disambiguation with some truth coverage."""
    cr = {
        "candidate_id": "partial",
        "cost": 0.8,
        "epsilon_sweep": [
            {"epsilon_multiplier": 1.0, "valid_disambiguation_rate": 0.3,
             "truth_in_consistent_set_rate": 0.8, "singleton_wrong_rate": 0.0,
             "empty_rate": 0.0},
        ],
    }
    util = compute_valid_utility(cr)
    # 0.3 + 0.5*0.8 - 2.0*0 - 1.0*0 - 0.8 = 0.3 + 0.4 + 0 + 0 - 0.8 = -0.1
    assert abs(util["utility"] - (-0.1)) < 0.001


def test_valid_utility_best_epsilon():
    """Selects best epsilon by utility."""
    cr = {
        "candidate_id": "multi_eps",
        "cost": 0.5,
        "epsilon_sweep": [
            {"epsilon_multiplier": 0.5, "valid_disambiguation_rate": 0.0,
             "truth_in_consistent_set_rate": 0.0, "singleton_wrong_rate": 0.0,
             "empty_rate": 1.0},
            {"epsilon_multiplier": 1.0, "valid_disambiguation_rate": 0.4,
             "truth_in_consistent_set_rate": 0.9, "singleton_wrong_rate": 0.0,
             "empty_rate": 0.0},
            {"epsilon_multiplier": 2.0, "valid_disambiguation_rate": 0.1,
             "truth_in_consistent_set_rate": 1.0, "singleton_wrong_rate": 0.0,
             "empty_rate": 0.0},
        ],
    }
    util = compute_valid_utility(cr)
    # eps=0.5: 0 + 0 - 0 - 1.0 - 0.5 = -1.5
    # eps=1.0: 0.4 + 0.45 - 0 - 0 - 0.5 = 0.35  <-- best
    # eps=2.0: 0.1 + 0.5 - 0 - 0 - 0.5 = 0.1
    assert abs(util["utility"] - 0.35) < 0.001
    assert abs(util["best_epsilon_multiplier"] - 1.0) < 0.001


def test_valid_utility_no_sweep():
    """Fallback when no epsilon sweep data."""
    cr = {"candidate_id": "nosweep", "cost": 1.0, "epsilon_sweep": []}
    util = compute_valid_utility(cr)
    assert util["utility"] == -1.0


def test_rank_candidates_valid():
    baseline_oqci = {}; baseline_ns = {}; baseline_pw = {}
    cand_results = [
        {"candidate_id": "bad", "height_um": 1.6, "components": ["Bz"], "n_states": 1, "cost": 0.4,
         "epsilon_sweep": [
             {"epsilon_multiplier": 1.0, "valid_disambiguation_rate": 0.0,
              "truth_in_consistent_set_rate": 0.0, "singleton_wrong_rate": 0.0, "empty_rate": 1.0},
         ]},
        {"candidate_id": "good", "height_um": 6.4, "components": ["Bx", "By", "Bz"], "n_states": 4, "cost": 1.5,
         "epsilon_sweep": [
             {"epsilon_multiplier": 1.5, "valid_disambiguation_rate": 0.5,
              "truth_in_consistent_set_rate": 0.9, "singleton_wrong_rate": 0.0, "empty_rate": 0.0},
         ]},
    ]
    ranking = rank_candidates(baseline_oqci, baseline_ns, baseline_pw, cand_results, {})
    assert ranking["candidate_count"] == 2
    assert ranking["best_global"] == "good"
    # good utility = 0.5 + 0.45 - 1.5 = -0.55 (cost dominates at low VDR)
    assert ranking["best_utility"] > -1.0
    # both utilities negative, so no "improvement" over baseline 0
