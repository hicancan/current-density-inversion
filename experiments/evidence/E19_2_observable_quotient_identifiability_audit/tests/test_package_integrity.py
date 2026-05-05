"""E19.2 package integrity tests."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_standard_files_exist():
    eid = "E19_2_observable_quotient_identifiability_audit"
    assert (ROOT / "README.md").exists()
    assert (ROOT / "REPRODUCE.md").exists()
    assert (ROOT / "METRICS_SCHEMA.md").exists()
    assert (ROOT / "FAILURE_MODES.md").exists()
    assert (ROOT / "requirements.txt").exists()
    assert (ROOT / "configs" / "smoke.json").exists()
    assert (ROOT / "configs" / "default.json").exists()
    assert (ROOT / "configs" / "multi_height.json").exists()
    assert (ROOT / "src" / "__init__.py").exists()
    assert (ROOT / "tests").exists()


def test_configs_are_valid_json():
    for name in ["smoke", "default", "multi_height"]:
        cfg = json.loads((ROOT / "configs" / f"{name}.json").read_text(encoding="utf-8"))
        assert cfg["schema_version"] == "e19_2-oqci-config-v1"
        assert len(cfg["sensor_heights_um"]) >= 1
        assert cfg["epsilon_policy"]["mode"] in ("known_noise", "sensitivity")


def test_imports():
    from src.config import load_config, validate_config, compute_epsilon
    from src.operators import multi_height_operator_stack, operator_diagnostics
    from src.hypotheses import HYPOTHESES, build_hypothesis_basis
    from src.data import generate_cases, generate_adversarial_pairs
    from src.quotient import consistent_set_for_case, fit_hypothesis
    from src.intervals import binary_claim_interval, aggregate_claim_intervals
    from src.distances import unit_energy_principal_angle_distance, pairwise_distinguishability
    from src.nullspace import near_null_modes
    from src.resolution import resolution_diagnostics
    from src.metrics import engineering_gates, scientific_gates
    import src.run_all
    assert len(HYPOTHESES) == 4
