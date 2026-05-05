"""Test near-null mode extraction."""

from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def test_near_null_modes_produce_valid_svd():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from hypotheses import build_all_hypothesis_bases
    from nullspace import near_null_modes

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    result = near_null_modes(bundle, bases, threshold=0.01)

    assert result["near_null_count"] >= 0
    assert result["effective_rank"] > 0
    assert len(result["singular_values"]) > 0
    assert result["max_singular_value"] > 0
    assert result["min_singular_value"] >= 0


def test_effective_rank_nonzero():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from hypotheses import build_all_hypothesis_bases
    from nullspace import near_null_modes

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    result = near_null_modes(bundle, bases, threshold=0.01)
    assert result["effective_rank"] >= 1, "Effective rank should be at least 1"
    assert result["effective_rank"] <= result["total_rank"]
