"""Test pairwise distinguishability distances."""

from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def test_all_6_pairs_computed():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from hypotheses import build_all_hypothesis_bases
    from distances import pairwise_distinguishability

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    result = pairwise_distinguishability(bases, bundle)

    pairs = result["pairs"]
    assert len(pairs) == 6
    expected_pairs = [
        "H0_no_via__H1_via",
        "H0_no_via__H2_model_gap",
        "H0_no_via__H3_return_path",
        "H1_via__H2_model_gap",
        "H1_via__H3_return_path",
        "H2_model_gap__H3_return_path",
    ]
    for ep in expected_pairs:
        assert ep in pairs
        assert pairs[ep]["unit_energy_distance"] >= 0
        assert pairs[ep]["claim_activated_distance"] >= 0
        assert 0 <= pairs[ep]["principal_angle_deg"] <= 90


def test_subspace_distance_non_negative():
    import sys
    sys.path.insert(0, SRC)
    from distances import unit_energy_principal_angle_distance
    rng = np.random.default_rng(42)
    B1 = rng.normal(0, 1, (50, 5))
    B2 = rng.normal(0, 1, (50, 3))
    dist = unit_energy_principal_angle_distance(B1, B2)
    assert dist >= 0
