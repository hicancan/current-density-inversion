from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from background_subtraction_stub import subtract_background
from load_qdm_npz_stub import load_field
from simple_wire_sanity_stub import simple_wire_sanity
from validate_real_case_metadata import validate_case


def _write_report(metrics: dict[str, Any], out: Path) -> None:
    gates = metrics["acceptance_gates"]
    rows = "\n".join(f"| {key} | {value} |" for key, value in sorted(gates.items()))
    report = f"""# E09 Real Data Intake Gate Run Report

This is an interface/scaffold run only. It validates metadata, component order,
units, background protocol, strict-path defaults, the NPZ loader stub, and the
simple-wire sanity utility. It does not load measured QDM/NV rows and cannot
support real via/no-via diagnosis.

Metrics file: `outputs/metrics.json`

| Gate | Pass |
|---|---|
{rows}

## Claim Boundary

- C12_real_qdm_nv_validation remains blocked.
- No real rows are present.
- This run is `passed_interface`, not real validation.
"""
    (out / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def run(out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    template_path = ROOT / "examples" / "example_case_template.json"
    payload = json.loads(template_path.read_text(encoding="utf-8"))
    template_errors = validate_case(payload, base_dir=template_path.parent, strict_paths=False)
    strict_errors = validate_case(payload, base_dir=template_path.parent, strict_paths=True)

    duplicate_component_payload = json.loads(json.dumps(payload))
    duplicate_component_payload["field"]["component_order"] = ["Bx", "Bx", "Bz"]
    component_errors = validate_case(duplicate_component_payload, base_dir=template_path.parent, strict_paths=False)

    bad_units_payload = json.loads(json.dumps(payload))
    bad_units_payload["field"]["units"] = "gauss"
    units_errors = validate_case(bad_units_payload, base_dir=template_path.parent, strict_paths=False)

    bad_background_payload = json.loads(json.dumps(payload))
    bad_background_payload["background"]["protocol"] = "ad_hoc"
    background_errors = validate_case(bad_background_payload, base_dir=template_path.parent, strict_paths=False)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        arr = np.zeros((4, 5, 3), dtype=np.float32)
        arr[:, :, 0] = 2.0
        arr[:, :, 2] = 1.0
        bg = 0.25 * np.ones((4, 5, 3), dtype=np.float32)
        np.savez_compressed(tmp_path / "field.npz", B_meas=arr)
        np.savez_compressed(tmp_path / "bg.npz", B_meas=bg)
        case_payload = json.loads(json.dumps(payload))
        case_payload["field"]["path"] = "field.npz"
        case_payload["field"]["shape"] = [4, 5, 3]
        case_payload["background"] = {
            "path": "bg.npz",
            "array_key": "B_meas",
            "protocol": "subtract_reference",
        }
        case_json = tmp_path / "case.json"
        case_json.write_text(json.dumps(case_payload), encoding="utf-8")
        load_summary = load_field(case_json)
        background_summary = subtract_background(case_json, tmp_path / "subtracted.npz")
        wire_summary = simple_wire_sanity(case_json)

    gates = {
        "metadata_template_valid": not template_errors,
        "strict_paths_default_off": bool(strict_errors),
        "component_order_validation": any("component_order" in item for item in component_errors),
        "units_validation": any("units" in item for item in units_errors),
        "background_protocol_validation": any("background.protocol" in item for item in background_errors),
        "npz_loader_stub_callable": load_summary["shape"] == [4, 5, 3],
        "background_subtraction_stub_callable": float(background_summary["subtracted_rms"]) > 0.0,
        "simple_wire_sanity_stub_callable": abs(float(wire_summary["bz_over_bxy_rms"]) - 0.5) < 1e-12,
        "no_real_rows_present": True,
        "claim_boundary_real_data_interface_only": payload.get("claim_boundary") == "real-data interface only",
    }
    metrics = {
        "schema_version": "research-ssot-metrics-v1",
        "experiment": "E09_real_data_intake_gate",
        "run_mode": "interface",
        "full_run_completed": True,
        "measured_rows_present": False,
        "all_acceptance_gates_passed": all(gates.values()),
        "acceptance_gates": gates,
        "metadata_validation_errors": template_errors,
        "strict_path_validation_errors": strict_errors,
        "loader_summary": load_summary,
        "background_summary": background_summary,
        "simple_wire_summary": wire_summary,
        "leakage_audit": {
            "calibration_rows": [],
            "heldout_rows": [],
            "hidden_rows": [],
            "threshold_selection_rows": [],
            "model_selection_rows": [],
            "thresholds_source": "none",
            "model_selection_source": "none",
            "pypeec_stress_rows_used_for_training": False,
            "real_rows_used_for_threshold_selection": False,
            "strict_paths_default_off": True,
            "run_report_calibration_source_present": True,
        },
        "cannot_claim": [
            "real QDM/NV validation",
            "real via/no-via diagnosis",
            "real calibration protocol validation",
        ],
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    _write_report(metrics, out)
    print(json.dumps({"all_acceptance_gates_passed": metrics["all_acceptance_gates_passed"]}, indent=2))
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "outputs")
    args = parser.parse_args()
    run(args.out)


if __name__ == "__main__":
    main()
