from pathlib import Path


def test_standard_files_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "README.md",
        "REPRODUCE.md",
        "METRICS_SCHEMA.md",
        "FAILURE_MODES.md",
        "requirements.txt",
        "configs/default.json",
        "configs/smoke.json",
        "src/run_all.py",
    ]:
        assert (root / rel).exists(), rel


def test_default_config_mentions_dual_schur():
    text = (Path(__file__).resolve().parents[1] / "configs/default.json").read_text(encoding="utf-8")
    assert "active_drive_amplitude" in text
    assert "defect_open_factor" in text

