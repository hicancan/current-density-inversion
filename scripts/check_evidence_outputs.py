from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import inspect_evidence_packages, load_graph, metrics_gate_status


def main() -> int:
    graph = load_graph(ROOT)
    failures: list[str] = []
    checked = 0
    for inspection in inspect_evidence_packages(graph):
        evidence = graph.experiments[inspection.evidence_id]
        status = evidence.get("status")
        if not inspection.exists:
            failures.append(f"{inspection.evidence_id}: runtime package missing")
            continue
        if inspection.missing_standard_files:
            failures.append(
                f"{inspection.evidence_id}: missing standard files {', '.join(inspection.missing_standard_files)}"
            )
        if not inspection.has_tests:
            failures.append(f"{inspection.evidence_id}: tests directory missing")
        if status not in {"planned", "blocked", "blocked_by_dependency", "obsolete"}:
            if not inspection.has_config:
                failures.append(f"{inspection.evidence_id}: configs/default.json missing")
            if not (inspection.package_dir / "outputs" / "RUN_REPORT.md").exists():
                failures.append(f"{inspection.evidence_id}: outputs/RUN_REPORT.md missing")
            if not (inspection.package_dir / "requirements.txt").exists() and not (inspection.package_dir / "pyproject.toml").exists():
                failures.append(f"{inspection.evidence_id}: requirements.txt or pyproject.toml missing")
    for evidence_id, evidence in graph.experiments.items():
        runtime = evidence.get("runtime") or {}
        metrics_files = runtime.get("metrics_files") or []
        if not metrics_files:
            package_dir = runtime.get("package_dir")
            if evidence.get("status") not in {"planned", "blocked", "blocked_by_dependency", "obsolete"}:
                failures.append(f"{evidence_id}: non-planned evidence has no metrics_files")
            elif package_dir and not (ROOT / package_dir).exists():
                failures.append(f"{evidence_id}: runtime package missing")
            continue
        for rel_path in metrics_files:
            checked += 1
            path = ROOT / rel_path
            status = metrics_gate_status(path)
            print(f"{evidence_id}: {status.gate}={status.ok}")
            if not status.ok:
                if evidence.get("status") == "partial" and status.gate == "all_acceptance_gates_passed":
                    pass  # partial evidence may legitimately have gates not passed
                else:
                    failures.append(f"{evidence_id}: metrics gate failed via {status.gate}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"Evidence output check passed for {checked} metrics file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
