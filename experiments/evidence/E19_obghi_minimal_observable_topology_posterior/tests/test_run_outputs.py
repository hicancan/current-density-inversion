from pathlib import Path
import json
import sys

PKG = Path(__file__).resolve().parents[1]
SRC = PKG / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from run_all import main


def test_smoke_run_writes_outputs(tmp_path):
    out = tmp_path / "outputs"
    metrics = main(["--config", str(PKG / "configs" / "smoke.json"), "--out", str(out)])
    assert (out / "metrics.json").exists()
    assert (out / "RUN_REPORT.md").exists()
    assert (out / "POSTERIOR_TABLE.md").exists()
    loaded = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert loaded["evidence_id"] == "E19_obghi_minimal_observable_topology_posterior"
    assert "acceptance_gates" in loaded
    assert metrics["obghi"]["case_count"] > 0
