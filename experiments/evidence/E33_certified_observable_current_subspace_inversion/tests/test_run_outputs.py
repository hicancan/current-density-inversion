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
    assert loaded["evidence_id"] == "E33_certified_observable_current_subspace_inversion"
    assert metrics["engineering_gates_passed"] is True
    assert "single_height" in loaded["protocols"]
    assert loaded["protocols"]["single_height"]["stable_mode_count"] > 0
    assert (tmp_path / "CERTIFIED_OBSERVABLE_CURRENT_SUBSPACE.md").exists()
    assert (tmp_path / "DARK_MODE_CERTIFICATE.md").exists()
