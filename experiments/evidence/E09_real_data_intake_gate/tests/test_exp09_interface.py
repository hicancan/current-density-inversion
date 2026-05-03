from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

EXP_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = EXP_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from load_qdm_npz_stub import load_field
from background_subtraction_stub import subtract_background
from simple_wire_sanity_stub import simple_wire_sanity
from validate_real_case_metadata import validate_case


def test_template_metadata_validates_without_requiring_paths() -> None:
    payload = json.loads((EXP_DIR / "examples" / "example_case_template.json").read_text(encoding="utf-8"))
    assert validate_case(payload, base_dir=EXP_DIR / "examples", strict_paths=False) == []


def test_validator_rejects_missing_component_order() -> None:
    payload = json.loads((EXP_DIR / "examples" / "example_case_template.json").read_text(encoding="utf-8"))
    payload["field"]["component_order"] = ["Bx", "Bx", "Bz"]
    errors = validate_case(payload, base_dir=EXP_DIR / "examples", strict_paths=False)
    assert any("component_order" in e for e in errors)


def test_npz_loader_checks_shape_and_finiteness(tmp_path: Path) -> None:
    arr = np.zeros((4, 5, 3), dtype=float)
    npz = tmp_path / "field.npz"
    np.savez_compressed(npz, B_meas=arr)
    payload = json.loads((EXP_DIR / "examples" / "example_case_template.json").read_text(encoding="utf-8"))
    payload["field"]["path"] = "field.npz"
    payload["field"]["shape"] = [4, 5, 3]
    case_json = tmp_path / "case.json"
    case_json.write_text(json.dumps(payload), encoding="utf-8")
    summary = load_field(case_json)
    assert summary["shape"] == [4, 5, 3]
    assert summary["rms"] == 0.0


def test_background_subtraction_stub_writes_npz(tmp_path: Path) -> None:
    arr = np.ones((4, 5, 3), dtype=float)
    bg = 0.25 * np.ones((4, 5, 3), dtype=float)
    np.savez_compressed(tmp_path / "field.npz", B_meas=arr)
    np.savez_compressed(tmp_path / "bg.npz", B_meas=bg)
    payload = json.loads((EXP_DIR / "examples" / "example_case_template.json").read_text(encoding="utf-8"))
    payload["field"]["path"] = "field.npz"
    payload["field"]["shape"] = [4, 5, 3]
    payload["background"] = {"path": "bg.npz", "array_key": "B_meas", "protocol": "subtract_reference"}
    case_json = tmp_path / "case.json"
    case_json.write_text(json.dumps(payload), encoding="utf-8")
    out = tmp_path / "sub.npz"
    summary = subtract_background(case_json, out)
    assert summary["subtracted_rms"] == 0.75
    assert "B_subtracted" in np.load(out)


def test_simple_wire_sanity_reports_component_ratios(tmp_path: Path) -> None:
    arr = np.zeros((4, 5, 3), dtype=float)
    arr[:, :, 0] = 2.0
    arr[:, :, 2] = 1.0
    np.savez_compressed(tmp_path / "field.npz", B_meas=arr)
    payload = json.loads((EXP_DIR / "examples" / "example_case_template.json").read_text(encoding="utf-8"))
    payload["field"]["path"] = "field.npz"
    payload["field"]["shape"] = [4, 5, 3]
    case_json = tmp_path / "case.json"
    case_json.write_text(json.dumps(payload), encoding="utf-8")
    summary = simple_wire_sanity(case_json)
    assert summary["bz_over_bxy_rms"] == 0.5
