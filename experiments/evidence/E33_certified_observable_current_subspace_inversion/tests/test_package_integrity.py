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


def test_readme_states_observable_current_subspace():
    text = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
    assert "J_observable" in text
    assert "J_dark" in text
    assert "lambda_q" in text
