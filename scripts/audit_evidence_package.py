from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import inspect_evidence_packages, load_graph, metrics_gate_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit evidence package contract.")
    parser.add_argument("evidence", nargs="*", help="Evidence ids to inspect; defaults to all.")
    args = parser.parse_args()

    graph = load_graph(ROOT)
    wanted = set(args.evidence) if args.evidence else set(graph.experiments)
    failures: list[str] = []
    for item in inspect_evidence_packages(graph):
        if item.evidence_id not in wanted:
            continue
        evidence = graph.experiments[item.evidence_id]
        print(f"{item.evidence_id}: {item.package_dir}")
        if not item.exists:
            failures.append(f"{item.evidence_id}: package missing")
        if item.missing_standard_files:
            failures.append(f"{item.evidence_id}: missing {', '.join(item.missing_standard_files)}")
        if not item.has_tests:
            failures.append(f"{item.evidence_id}: tests directory missing")
        status = evidence.get("status")
        if status not in {"planned", "blocked", "blocked_by_dependency", "obsolete"}:
            if not item.has_config:
                failures.append(f"{item.evidence_id}: configs/default.json missing")
            if not item.has_metrics:
                failures.append(f"{item.evidence_id}: metrics file missing")
        for rel_path in (evidence.get("runtime") or {}).get("metrics_files", []) or []:
            gate = metrics_gate_status(ROOT / rel_path)
            print(f"  metrics {rel_path}: {gate.gate}={gate.ok}")
            if not gate.ok:
                failures.append(f"{item.evidence_id}: metrics gate failed")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Evidence package audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

