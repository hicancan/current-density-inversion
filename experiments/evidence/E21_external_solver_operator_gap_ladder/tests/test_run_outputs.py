"""Test that smoke run produces expected outputs."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_smoke_run_completes():
    """Run the smoke config and verify outputs exist."""
    result = subprocess.run(
        [
            sys.executable, str(ROOT / "src" / "run_all.py"),
            "--config", str(ROOT / "configs" / "smoke.json"),
            "--out", str(ROOT / "outputs_smoke"),
        ],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        timeout=120,
    )
    assert result.returncode == 0, f"Smoke run failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    outputs = ROOT / "outputs_smoke"
    assert (outputs / "metrics.json").exists()
    assert (outputs / "RUN_REPORT.md").exists()
    assert (outputs / "OPERATOR_GAP_TABLE.md").exists()
    assert (outputs / "SPECTRAL_GAP.md").exists()
    assert (outputs / "EXTERNAL_ARTIFACT_CONTRACT.md").exists()
    assert (outputs / "FAILURE_MODES.md").exists()


def test_metrics_json_schema():
    """Verify metrics.json has required keys after smoke run."""
    metrics_path = ROOT / "outputs_smoke" / "metrics.json"
    if not metrics_path.exists():
        # Run smoke first if needed
        subprocess.run(
            [sys.executable, str(ROOT / "src" / "run_all.py"),
             "--config", str(ROOT / "configs" / "smoke.json"),
             "--out", str(ROOT / "outputs_smoke")],
            capture_output=True, text=True, cwd=str(ROOT), timeout=120,
        )

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    required_keys = [
        "experiment", "case_count", "available_operator_count",
        "external_solver_artifacts_present", "unit_sanity_passed",
        "operator_gap_summary", "acceptance_gates",
    ]
    for key in required_keys:
        assert key in metrics, f"Missing key: {key}"

    assert metrics["unit_sanity_passed"] is True
    assert metrics["external_solver_artifacts_present"] is False
    assert metrics["acceptance_gates"]["no_fake_external_validation"]["pass"] is True


def test_acceptance_gates():
    """Verify all acceptance gates are present in metrics."""
    metrics_path = ROOT / "outputs_smoke" / "metrics.json"
    if not metrics_path.exists():
        subprocess.run(
            [sys.executable, str(ROOT / "src" / "run_all.py"),
             "--config", str(ROOT / "configs" / "smoke.json"),
             "--out", str(ROOT / "outputs_smoke")],
            capture_output=True, text=True, cwd=str(ROOT), timeout=120,
        )

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    gates = metrics["acceptance_gates"]
    expected_gates = [
        "package_runs_to_completion",
        "all_operators_same_shape",
        "operator_gaps_nonzero",
        "decision_stress_executed",
        "external_artifact_contract_written",
        "reports_written",
        "no_fake_external_validation",
        "generated_domain_boundary_explicit",
    ]
    for gate in expected_gates:
        assert gate in gates, f"Missing gate: {gate}"


def test_operator_gap_table_content():
    """Verify OPERATOR_GAP_TABLE.md has actual data."""
    table_path = ROOT / "outputs_smoke" / "OPERATOR_GAP_TABLE.md"
    if not table_path.exists():
        subprocess.run(
            [sys.executable, str(ROOT / "src" / "run_all.py"),
             "--config", str(ROOT / "configs" / "smoke.json"),
             "--out", str(ROOT / "outputs_smoke")],
            capture_output=True, text=True, cwd=str(ROOT), timeout=120,
        )

    content = table_path.read_text(encoding="utf-8")
    assert "Operator Gap" in content
    assert "Rel RMSE" in content
    # Should have at least one data row (with numeric entry)
    assert "centerline" in content.lower()
