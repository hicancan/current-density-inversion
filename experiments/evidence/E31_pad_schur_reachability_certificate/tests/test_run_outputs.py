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
    assert loaded["evidence_id"] == "E31_pad_schur_reachability_certificate"
    assert metrics["engineering_gates_passed"] is True
    assert "pad_reachability" in loaded
    assert (tmp_path / "PAD_SCHUR_REACHABILITY_THEOREM.md").exists()
    assert (tmp_path / "PAD_ACCESS_CERTIFICATE.md").exists()

