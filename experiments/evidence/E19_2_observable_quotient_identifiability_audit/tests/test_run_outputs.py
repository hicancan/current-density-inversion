"""Test that run_all produces valid outputs in smoke mode."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def test_smoke_run_produces_outputs():
    import sys
    sys.path.insert(0, SRC)
    from run_all import main

    out_dir = ROOT / "outputs" / "smoke_test"
    metrics = main(["--config", str(ROOT / "configs" / "smoke.json"), "--out", str(out_dir)])

    assert (out_dir / "metrics.json").exists()
    assert (out_dir / "RUN_REPORT.md").exists()
    assert (out_dir / "CONSISTENT_HYPOTHESES.md").exists()
    assert (out_dir / "CLAIM_INTERVALS.md").exists()
    assert (out_dir / "PAIRWISE_DISTANCES.md").exists()
    assert (out_dir / "NEAR_NULL_MODES.md").exists()
    assert (out_dir / "RESOLUTION_AUDIT.md").exists()
    assert (out_dir / "NEXT_MEASUREMENT.md").exists()
    assert (out_dir / "ADVERSARIAL_PAIRS.md").exists()

    m = json.loads((out_dir / "metrics.json").read_text(encoding="utf-8"))
    assert m["schema_version"] == "research-ssot-metrics-v1"
    assert m["evidence_id"] == "E19_2_observable_quotient_identifiability_audit"
    assert "oqci" in m
    assert m["oqci"]["case_count"] > 0
    assert m["oqci"]["consistent_set_nonempty_rate"] >= 0.0
    assert m["all_acceptance_gates_passed"] in (True, False)
    assert "leakage_audit" in m
    assert m["leakage_audit"]["generated_domain_only"] is True
