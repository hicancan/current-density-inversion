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


def test_readme_states_pad_pitch_barrier():
    text = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
    assert "eta_e(P)" in text
    assert "pitch" in text.lower()
