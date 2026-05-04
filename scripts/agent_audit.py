from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import inspect_evidence_packages, load_graph, metrics_gate_status, next_agent_tasks, validate_graph


def _ids_by_status(items: dict[str, dict], status: str) -> list[str]:
    return [item_id for item_id, item in items.items() if item.get("status") == status]


def main() -> int:
    graph = load_graph(ROOT)
    issues = validate_graph(graph)
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    print("# Agent Research Audit")
    print("")
    print(f"Claims: {len(graph.claims)}")
    print(f"Evidence packages: {len(graph.experiments)}")
    print(f"Artifacts: {len(graph.artifacts)}")
    print(f"Graph validation: {len(errors)} error(s), {len(warnings)} warning(s)")
    print("")

    print("## Claim Risk")
    print("- Blocked claims: " + ", ".join(_ids_by_status(graph.claims, "blocked") or ["-"]))
    print("- Proposed claims: " + ", ".join(_ids_by_status(graph.claims, "proposed") or ["-"]))
    print("- Missing nodes: " + ", ".join(_ids_by_status(graph.nodes, "missing") or ["-"]))
    print("")

    print("## Next Agent Task")
    tasks = next_agent_tasks(graph)
    if tasks:
        task = tasks[0]
        print(f"- {task['id']} -> {task.get('recommended_evidence_id')} ({task.get('affected_claim')})")
    else:
        print("- none")
    print("")

    print("## Evidence Package Contract")
    for inspection in inspect_evidence_packages(graph):
        gaps = ", ".join(inspection.missing_standard_files) or "-"
        print(
            f"- {inspection.evidence_id}: exists={inspection.exists} config={inspection.has_config} "
            f"tests={inspection.has_tests} metrics={inspection.has_metrics} missing={gaps}"
        )
    print("")

    print("## Metrics Gates")
    for evidence_id, evidence in graph.experiments.items():
        for rel_path in (evidence.get("runtime") or {}).get("metrics_files", []) or []:
            status = metrics_gate_status(ROOT / rel_path)
            print(f"- {evidence_id}: {status.gate}={status.ok}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
