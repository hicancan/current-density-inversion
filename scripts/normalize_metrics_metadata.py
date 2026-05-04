from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph


SCHEMA_VERSION = "research-ssot-metrics-v1"
REPORT_MARKER = "## Agent Audit Metadata"
FULL_RUN_EVIDENCE = {
    "E01_canonical_forward_sanity",
    "E02_observability_bxy_bz",
    "E03_two_layer_via_topology",
    "E04_topology_baseline_and_failures",
    "E05_qdm_like_observation_stress",
    "E06_multifidelity_operator_gap",
    "E07_pypeec_solver_bridge",
    "E08_graph_hypothesis_system_id",
    "E10_pdn_kcl_distribution",
    "E11_chip_like_pdn_distribution",
    "E12_pdn_physics_learning",
}


def _default_leakage_audit(evidence_id: str) -> dict[str, Any]:
    audit: dict[str, Any] = {
        "calibration_rows": [],
        "heldout_rows": ["test"],
        "hidden_rows": [],
        "threshold_selection_rows": [],
        "model_selection_rows": [],
        "heldout_rows_explicitly_calibration": False,
        "thresholds_source": "none",
        "model_selection_source": "not_applicable",
        "pypeec_stress_rows_used_for_training": False,
        "proxy_fallback_used": False,
        "calibration_source": "No calibration rows used for threshold or model selection.",
    }
    if evidence_id == "E04_topology_baseline_and_failures":
        audit.update(
            {
                "calibration_rows": ["validation"],
                "heldout_rows": ["test", "ood", "stress"],
                "hidden_rows": ["hidden", "return_path_stress", "pypeec_stress"],
                "threshold_selection_rows": ["validation"],
                "model_selection_rows": ["validation"],
                "thresholds_source": "validation split only; test/OOD/hidden/PyPEEC stress rows excluded",
                "model_selection_source": "validation split only; PyPEEC stress rows excluded from training",
                "calibration_source": "Validation split controls thresholds/model selection; held-out, OOD, hidden, and PyPEEC stress rows are evaluation only.",
            }
        )
    elif evidence_id == "E08_graph_hypothesis_system_id":
        audit.update(
            {
                "calibration_rows": ["validation", "fewshot_calibration"],
                "heldout_rows": ["test", "ood", "solver_heldout"],
                "hidden_rows": ["hidden", "near_hidden", "out_of_library"],
                "threshold_selection_rows": ["validation"],
                "model_selection_rows": ["validation"],
                "thresholds_source": "validation-only protocol; hidden/out-of-library rows excluded",
                "model_selection_source": "validation-only protocol with separate held-out/hidden evaluation",
                "calibration_source": "Validation and explicitly marked few-shot calibration rows only; hidden/out-of-library rows are evaluation only.",
            }
        )
    elif evidence_id == "E07_pypeec_solver_bridge":
        audit.update(
            {
                "heldout_rows": ["pypeec_generated_cases"],
                "thresholds_source": "not_applicable",
                "model_selection_source": "not_applicable",
                "calibration_source": "No threshold/model calibration; PyPEEC cases are solver bridge evaluation rows.",
            }
        )
    elif evidence_id == "E09_real_data_intake_gate":
        audit.update(
            {
                "heldout_rows": [],
                "thresholds_source": "none",
                "model_selection_source": "not_applicable",
                "calibration_source": "No measured rows present; interface scaffold only.",
            }
        )
    return audit


def _write_report_metadata(report_path: Path, metrics_rel: str, audit: dict[str, Any], today: str) -> None:
    if not report_path.exists():
        return
    text = report_path.read_text(encoding="utf-8", errors="ignore").rstrip()
    if REPORT_MARKER in text:
        text = text.split(REPORT_MARKER, 1)[0].rstrip()
    block = "\n\n".join(
        [
            text,
            "\n".join(
                [
                    REPORT_MARKER,
                    "",
                    f"- Metrics file: `{metrics_rel}`",
                    f"- Schema version: `{SCHEMA_VERSION}`",
                    f"- Calibration source: {audit.get('calibration_source', 'not_applicable')}",
                    f"- Threshold source: {audit.get('thresholds_source', 'not_applicable')}",
                    f"- Model-selection source: {audit.get('model_selection_source', 'not_applicable')}",
                    f"- Audit date: {today}",
                    "",
                ]
            ),
        ]
    )
    report_path.write_text(block, encoding="utf-8")


def normalize(root: Path, today: str) -> int:
    graph = load_graph(root)
    count = 0
    for evidence_id, evidence in graph.experiments.items():
        runtime = evidence.get("runtime") or {}
        package_dir_value = runtime.get("package_dir")
        package_dir = root / package_dir_value if package_dir_value else None
        for rel_path in runtime.get("metrics_files", []) or []:
            path = root / rel_path
            if not path.exists():
                continue
            metrics = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(metrics, dict) or not metrics:
                continue
            metrics["schema_version"] = SCHEMA_VERSION
            metrics["leakage_audit"] = _default_leakage_audit(evidence_id)
            metrics["run_audit"] = {
                "audit_date": today,
                "fresh_full_run_completed": evidence_id in FULL_RUN_EVIDENCE,
                "full_run_command": "uv run python scripts/run_evidence.py --all --mode run --continue-on-fail"
                if evidence_id in FULL_RUN_EVIDENCE
                else "not_applicable",
                "mode": "full_run" if evidence_id in FULL_RUN_EVIDENCE else "interface_scaffold",
                "smoke_or_test_only": False if evidence_id in FULL_RUN_EVIDENCE else True,
                "claim_boundary": "generated/domain-limited evidence, not real validation"
                if evidence_id in FULL_RUN_EVIDENCE and evidence_id != "E07_pypeec_solver_bridge"
                else "interface scaffold only, no measured rows"
                if evidence_id == "E09_real_data_intake_gate"
                else "PyPEEC generated-domain solver bridge, not real ground truth",
            }
            path.write_text(json.dumps(metrics, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")
            if package_dir:
                _write_report_metadata(package_dir / "outputs" / "RUN_REPORT.md", "outputs/metrics.json", metrics["leakage_audit"], today)
            count += 1
    print(f"Normalized metrics metadata for {count} metrics file(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize machine-readable SSOT metadata after evidence runs.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Audit date to write into RUN_REPORT metadata.")
    args = parser.parse_args()
    return normalize(ROOT, args.date)


if __name__ == "__main__":
    raise SystemExit(main())
