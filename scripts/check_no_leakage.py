from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph


def _as_set(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, list):
        return {str(item) for item in value}
    return {str(value)}


def main() -> int:
    graph = load_graph(ROOT)
    failures: list[str] = []
    checked = 0
    for evidence_id, evidence in graph.experiments.items():
        runtime = evidence.get("runtime") or {}
        package_dir = ROOT / runtime.get("package_dir", "") if runtime.get("package_dir") else None
        for rel_path in runtime.get("metrics_files", []) or []:
            checked += 1
            metrics = json.loads((ROOT / rel_path).read_text(encoding="utf-8"))
            audit = metrics.get("leakage_audit")
            if not isinstance(audit, dict):
                failures.append(f"{evidence_id}: missing leakage_audit")
                continue
            calibration = _as_set(audit.get("calibration_rows"))
            heldout = _as_set(audit.get("heldout_rows"))
            hidden = _as_set(audit.get("hidden_rows"))
            threshold_rows = _as_set(audit.get("threshold_selection_rows"))
            model_rows = _as_set(audit.get("model_selection_rows"))
            if calibration & heldout:
                failures.append(f"{evidence_id}: calibration and heldout rows overlap")
            if hidden & threshold_rows:
                failures.append(f"{evidence_id}: hidden rows used for threshold selection")
            if heldout & threshold_rows and not audit.get("heldout_rows_explicitly_calibration", False):
                failures.append(f"{evidence_id}: heldout rows used for threshold selection")
            if evidence_id in {"E04_topology_baseline_and_failures", "E08_graph_hypothesis_system_id"}:
                if audit.get("pypeec_stress_rows_used_for_training") is not False:
                    failures.append(f"{evidence_id}: PyPEEC stress rows must not be used for training")
                if not audit.get("thresholds_source"):
                    failures.append(f"{evidence_id}: thresholds_source is required")
                if not audit.get("model_selection_source"):
                    failures.append(f"{evidence_id}: model_selection_source is required")
            if evidence_id == "E07_pypeec_solver_bridge" and audit.get("proxy_fallback_used") is not False:
                failures.append("E07_pypeec_solver_bridge: proxy fallback must be false")
            if package_dir:
                report = package_dir / "outputs" / "RUN_REPORT.md"
                if report.exists():
                    text = report.read_text(encoding="utf-8", errors="ignore").lower()
                    if "calibration" not in text and "validation" not in text and audit.get("thresholds_source") not in {"none", "not_applicable"}:
                        failures.append(f"{evidence_id}: RUN_REPORT lacks calibration/validation source text")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"No-leakage check passed for {checked} metrics file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

