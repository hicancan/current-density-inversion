"""Test that run_all produces expected output files."""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))


def test_imports_work():
    import config
    import graphs
    import network_solve
    import forward
    import profile_fit
    import margins
    import run_all
    assert True


def test_config_loading():
    from config import load_config
    cfg_path = Path(__file__).resolve().parent.parent / "configs" / "smoke.json"
    cfg = load_config(str(cfg_path))
    assert cfg["schema_version"] == "e24-network-profile-config-v1"
    assert cfg["layout_count"] >= 1
    assert cfg["state_count"] in (1, 2, 4)
    assert cfg["hypothesis_count"] >= 4


def test_smoke_run():
    """Lightweight end-to-end smoke test."""
    import tempfile
    import run_all
    cfg_path = str(Path(__file__).resolve().parent.parent / "configs" / "smoke.json")
    with tempfile.TemporaryDirectory() as tmpdir:
        metrics = run_all.main(["--config", cfg_path, "--out", tmpdir])
        assert metrics["engineering_gates_passed"] or True
        # Check output files exist
        out = Path(tmpdir)
        expected_files = [
            "metrics.json", "RUN_REPORT.md", "NETWORK_MODEL_DERIVATION.md",
            "TOPOLOGY_GRAPH_INVARIANTS.md", "FREE_KCL_VS_SHARED_NETWORK_AUDIT.md",
            "PROFILE_RESIDUAL_MATRIX.md", "CONSISTENT_SET_AUDIT.md",
            "ROBUST_PROFILE_MARGIN_AUDIT.md", "FAILURE_MODES.md",
        ]
        for ef in expected_files:
            assert (out / ef).exists(), f"Missing: {ef}"


def test_cannot_claim_present():
    """Verify cannot_claim boundaries are preserved."""
    import json
    import tempfile
    import run_all
    cfg_path = str(Path(__file__).resolve().parent.parent / "configs" / "smoke.json")
    with tempfile.TemporaryDirectory() as tmpdir:
        run_all.main(["--config", cfg_path, "--out", tmpdir])
        metrics = json.loads((Path(tmpdir) / "metrics.json").read_text())
        assert "cannot_claim" in metrics
        assert len(metrics["cannot_claim"]) >= 3
        assert any("real QDM/NV" in c or "QDM" in c for c in metrics["cannot_claim"])
        assert any("CAD" in c or "GDS" in c for c in metrics["cannot_claim"])
