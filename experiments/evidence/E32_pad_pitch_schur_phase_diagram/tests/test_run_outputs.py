import json
import sys
from pathlib import Path


def test_smoke_run_outputs(tmp_path):
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    from run_all import main

    metrics = main([
        "--config",
        str(root / "configs" / "smoke.json"),
        "--out",
        str(tmp_path),
    ])

    loaded = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert loaded["evidence_id"] == "E32_pad_pitch_schur_phase_diagram"
    assert metrics["engineering_gates_passed"] is True
    assert "phase_diagram" in loaded
    assert loaded["barrier_certificate"]["candidate_exact_min_ratio"] > 0.0
    assert (tmp_path / "PAD_PITCH_PHASE_DIAGRAM.md").exists()
    assert (tmp_path / "LOCALITY_BARRIER_DERIVATION.md").exists()
