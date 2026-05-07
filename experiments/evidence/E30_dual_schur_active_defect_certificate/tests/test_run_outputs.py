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

    metrics_path = tmp_path / "metrics.json"
    assert metrics_path.exists()
    loaded = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert loaded["evidence_id"] == "E30_dual_schur_active_defect_certificate"
    assert loaded["engineering_gates_passed"] is True
    assert metrics["dual_schur_certificate"]["summary"]["pair_count"] >= 1
    assert (tmp_path / "DUAL_SCHUR_DERIVATION.md").exists()
    assert (tmp_path / "DEFECT_SIGNATURE_CERTIFICATE.md").exists()

