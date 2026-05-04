from pathlib import Path
import json
import sys

PKG = Path(__file__).resolve().parents[1]
SRC = PKG / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from config import load_config
from operators import build_operator, operator_diagnostics
from data import generate_cases
from basis import build_all_hypothesis_bases, HYPOTHESES
from obghi import infer_case


def test_config_loads():
    cfg = load_config(PKG / "configs" / "smoke.json")
    assert cfg["grid_size"] >= 6
    assert cfg["layer_count"] == 4


def test_operator_has_nonzero_via_columns():
    cfg = load_config(PKG / "configs" / "smoke.json")
    bundle = build_operator(cfg)
    diag = operator_diagnostics(bundle)
    assert diag["via_columns_nonzero"] is True
    assert diag["shape"][0] == 3 * cfg["grid_size"] * cfg["grid_size"]


def test_hypothesis_bases_have_columns():
    cfg = load_config(PKG / "configs" / "smoke.json")
    bundle = build_operator(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    assert set(bases) == set(HYPOTHESES)
    for h, b in bases.items():
        assert b.B.shape[0] == bundle.A.shape[0]
        assert b.B.shape[1] > 0


def test_single_case_inference_returns_posterior():
    cfg = load_config(PKG / "configs" / "smoke.json")
    bundle = build_operator(cfg)
    cases = generate_cases(bundle, cfg)
    result = infer_case(cases[0], bundle, cfg)
    probs = [p.posterior_probability for p in result.posteriors.values()]
    assert abs(sum(probs) - 1.0) < 1e-8
    assert result.top_hypothesis in HYPOTHESES
    assert result.decision in {
        "accept",
        "reject_low_posterior",
        "reject_via_gap_ambiguous",
        "need_next_measurement",
    }
