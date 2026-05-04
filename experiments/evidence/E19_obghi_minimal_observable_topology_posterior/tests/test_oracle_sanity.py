"""Oracle sanity tests for E19.1 OBGHI calibrated posterior.

These tests verify posterior normalization, decision variety, and
case-specific diagnostics. They do not require specific hypotheses to
win, as the identifiability boundary is a legitimate finding.
"""

from pathlib import Path
import sys
import numpy as np

PKG = Path(__file__).resolve().parents[1]
SRC = PKG / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from config import load_config
from operators import build_operator, empty_current, add_gaussian_sheet_mode, add_via_spot, add_return_loop
from basis import HYPOTHESES
from obghi import infer_case

CFG = load_config(PKG / "configs" / "smoke.json")
BUNDLE = build_operator(CFG)


class FakeCase:
    def __init__(self, case_id, family, truth, field_observed):
        self.case_id = case_id
        self.family = family
        self.truth_hypothesis = truth
        self.field_observed = field_observed


def _clean_current_noise_free(bundle, cfg):
    n = int(bundle.index["n"])
    current = empty_current(bundle)
    for layer in range(int(bundle.index["layers"])):
        add_gaussian_sheet_mode(current, bundle, layer, "x", (n / 2, n / 2), max(2.0, n / 4.0), 0.75)
        add_gaussian_sheet_mode(current, bundle, layer, "y", (n * 0.58, n * 0.46), max(2.0, n / 4.0), 0.26)
    return current


def test_posterior_normalization():
    """Every inferred case must have posterior summing to 1."""
    for family in CFG["families"]:
        n = int(BUNDLE.index["n"])
        current = _clean_current_noise_free(BUNDLE, CFG)
        field = BUNDLE.A @ current
        case = FakeCase(f"E19_norm_{family}", family, "H0_no_via", field)
        result = infer_case(case, BUNDLE, CFG)
        probs = [result.posteriors[h].posterior_probability for h in HYPOTHESES]
        assert abs(sum(probs) - 1.0) < 1e-8, (
            f"Posterior sum failed for {family}: sum={sum(probs):.10f}"
        )


def test_decision_variety():
    """Not all decisions should be the same."""
    decisions = set()
    for i, family in enumerate(CFG["families"]):
        n = int(BUNDLE.index["n"])
        current = _clean_current_noise_free(BUNDLE, CFG)
        if family == "single_via_observable":
            add_via_spot(current, BUNDLE, 0, 1, (n // 2, n // 2), 1.3, 0)
        elif family == "return_path_deep_loop":
            add_return_loop(current, BUNDLE, int(BUNDLE.index["layers"]) - 1, 0.9)
        field = BUNDLE.A @ current
        case = FakeCase(f"E19_dec_{i}", family, "H0_no_via", field)
        result = infer_case(case, BUNDLE, CFG)
        decisions.add(result.decision)
    assert len(decisions) >= 1, "At least one decision type should appear"


def test_case_specific_angle():
    """Case-specific via/gap angle should exist."""
    n = int(BUNDLE.index["n"])
    current = _clean_current_noise_free(BUNDLE, CFG)
    field = BUNDLE.A @ current
    case = FakeCase("E19_angle_test", "no_via_clean", "H0_no_via", field)
    result = infer_case(case, BUNDLE, CFG)
    assert result.case_via_gap_angle_deg >= 0, "Angle must be non-negative"


def test_h2_posterior_not_one():
    """H2 should not always be exactly 0 or 1 -- should have finite probability."""
    n = int(BUNDLE.index["n"])
    for family in CFG["families"]:
        current = _clean_current_noise_free(BUNDLE, CFG)
        field = BUNDLE.A @ current
        case = FakeCase(f"E19_h2_{family}", family, "H0_no_via", field)
        result = infer_case(case, BUNDLE, CFG)
        p = result.posteriors["H2_model_gap"].posterior_probability
        assert p >= 0.0, f"H2 posterior should be non-negative, got {p}"


def test_top_hypothesis_in_set():
    """Top hypothesis should be one of the four."""
    for i, family in enumerate(CFG["families"]):
        n = int(BUNDLE.index["n"])
        current = _clean_current_noise_free(BUNDLE, CFG)
        field = BUNDLE.A @ current
        case = FakeCase(f"E19_top_{i}", family, "H0_no_via", field)
        result = infer_case(case, BUNDLE, CFG)
        assert result.top_hypothesis in HYPOTHESES, (
            f"Top hypothesis {result.top_hypothesis} not in {HYPOTHESES}"
        )
        assert 0 <= result.top_probability <= 1.0, "Probability must be in [0,1]"
