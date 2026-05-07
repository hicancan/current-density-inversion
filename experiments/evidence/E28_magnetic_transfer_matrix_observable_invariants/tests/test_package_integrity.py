"""E28 package integrity tests."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def test_standard_files_exist():
    assert (ROOT / "README.md").exists()
    assert (ROOT / "REPRODUCE.md").exists()
    assert (ROOT / "METRICS_SCHEMA.md").exists()
    assert (ROOT / "FAILURE_MODES.md").exists()
    assert (ROOT / "requirements.txt").exists()
    assert (ROOT / "configs" / "smoke.json").exists()
    assert (ROOT / "configs" / "default.json").exists()
    assert (ROOT / "src" / "__init__.py").exists()
    assert (ROOT / "tests").exists()


def test_configs_are_valid_json():
    for name in ["smoke", "default"]:
        cfg = json.loads((ROOT / "configs" / f"{name}.json").read_text(encoding="utf-8"))
        assert cfg["schema_version"] == "e28-transfer-invariants-config-v1"
        assert len(cfg["sensor_heights_um"]) >= 1
        assert cfg["n_port_states"] >= 2
        assert cfg["port_config"]["scheme"] in ("diagonal_pairs", "boundary_corners", "adjacent_pairs")


def test_imports():
    from src.config import load_config, validate_config
    from src.operators import build_operator_and_graph, build_port_excitation, operator_diagnostics
    from src.hypotheses import HYPOTHESES, build_conductance_model, build_all_conductance_models
    from src.transfer_matrix import compute_transfer_matrix, compute_all_transfer_matrices
    from src.invariants import (
        column_space_projector, whitened_gram, differential_matrix,
        compute_all_invariants, invariant_sanity_checks,
    )
    from src.distances import compute_all_pairwise_distances, HYP_PAIRS, CRITICAL_PAIRS
    from src.nuisance import nuisance_audit, nuisance_reduction_factor
    from src.margins import compute_robust_margins, invariant_beats_raw
    from src.data import generate_transfer_cases, consistent_set_analysis
    from src.metrics import engineering_gates, scientific_gates
    import src.run_all
    assert len(HYPOTHESES) == 4
