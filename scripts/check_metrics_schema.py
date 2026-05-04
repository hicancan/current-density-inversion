from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph, metrics_gate_status


def _gate_values(metrics: dict[str, Any]) -> list[bool]:
    values: list[bool] = []
    if isinstance(metrics.get("all_acceptance_gates_passed"), bool):
        values.append(bool(metrics["all_acceptance_gates_passed"]))
    gates = metrics.get("acceptance_gates")
    if isinstance(gates, dict):
        for value in gates.values():
            if isinstance(value, bool):
                values.append(value)
            elif isinstance(value, dict) and isinstance(value.get("pass"), bool):
                values.append(bool(value["pass"]))
    return values


def main() -> int:
    graph = load_graph(ROOT)
    failures: list[str] = []
    checked = 0
    for evidence_id, evidence in graph.experiments.items():
        runtime = evidence.get("runtime") or {}
        package_dir = ROOT / runtime.get("package_dir", "") if runtime.get("package_dir") else None
        for rel_path in runtime.get("metrics_files", []) or []:
            checked += 1
            path = ROOT / rel_path
            status = metrics_gate_status(path)
            if not status.ok:
                failures.append(f"{evidence_id}: gate failed in {rel_path}: {status.gate}")
                continue
            metrics = json.loads(path.read_text(encoding="utf-8"))
            if metrics.get("schema_version") != "research-ssot-metrics-v1":
                failures.append(f"{evidence_id}: missing schema_version=research-ssot-metrics-v1")
            if not _gate_values(metrics):
                failures.append(f"{evidence_id}: no machine-readable boolean gate")
            if not isinstance(metrics.get("leakage_audit"), dict):
                failures.append(f"{evidence_id}: missing leakage_audit")
            run_audit = metrics.get("run_audit")
            if not isinstance(run_audit, dict):
                failures.append(f"{evidence_id}: missing run_audit")
            elif evidence.get("status") == "passed" and run_audit.get("fresh_full_run_completed") is not True:
                failures.append(f"{evidence_id}: passed evidence must record fresh_full_run_completed=true")
            elif evidence.get("status") == "passed_interface" and run_audit.get("mode") != "interface_scaffold":
                failures.append(f"{evidence_id}: passed_interface evidence must record interface_scaffold mode")
            if package_dir:
                report = package_dir / "outputs" / "RUN_REPORT.md"
                if not report.exists():
                    failures.append(f"{evidence_id}: missing RUN_REPORT.md")
                else:
                    text = report.read_text(encoding="utf-8", errors="ignore").lower()
                    if "metrics.json" not in text:
                        failures.append(f"{evidence_id}: RUN_REPORT.md does not reference metrics.json")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"Metrics schema check passed for {checked} metrics file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
