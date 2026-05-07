"""Test that run_all produces valid outputs in smoke mode."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def test_smoke_run_produces_outputs():
    sys.path.insert(0, SRC)
    from run_all import main

    out_dir = ROOT / "outputs" / "smoke_test"
    metrics = main(["--config", str(ROOT / "configs" / "smoke.json"), "--out", str(out_dir)])

    assert (out_dir / "metrics.json").exists()
    assert (out_dir / "RUN_REPORT.md").exists()
    assert (out_dir / "TRANSFER_MATRIX_DERIVATION.md").exists()
    assert (out_dir / "INVARIANT_DEFINITIONS.md").exists()
    assert (out_dir / "RAW_VS_INVARIANT_MARGIN_TABLE.md").exists()
    assert (out_dir / "PROJECTOR_GRAM_AUDIT.md").exists()
    assert (out_dir / "NUISANCE_INVARIANCE_AUDIT.md").exists()
    assert (out_dir / "OBSERVABLE_QUOTIENT_CERTIFICATE.md").exists()
    assert (out_dir / "HARDCASE_GAIN_SWEEP.md").exists()
    assert (out_dir / "CONSISTENT_SET_AUDIT.md").exists()
    assert (out_dir / "FAILURE_MODES.md").exists()

    m = json.loads((out_dir / "metrics.json").read_text(encoding="utf-8"))
    assert m["schema_version"] == "research-ssot-metrics-v1"
    assert m["evidence_id"] == "E28_magnetic_transfer_matrix_observable_invariants"
    assert "transfer_matrix" in m
    assert "invariants" in m
    assert "margins" in m
    assert "hardcase_gain_sweep" in m
    assert m["all_acceptance_gates_passed"] in (True, False)
    assert "leakage_audit" in m
    assert m["leakage_audit"]["generated_domain_only"] is True
