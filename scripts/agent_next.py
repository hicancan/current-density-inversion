from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph, next_agent_tasks


def main() -> int:
    graph = load_graph(ROOT)
    tasks = next_agent_tasks(graph)
    if not tasks:
        print("No active agent queue items.")
        return 0

    task = tasks[0]
    claim_id = task["affected_claim"]
    claim = graph.claims[claim_id]
    evidence_id = task.get("recommended_evidence_id", "-")
    print(f"Next task: {task['id']}")
    print(f"Priority: {task.get('priority')}")
    print(f"Status: {task.get('status')}")
    print(f"Affected claim: {claim_id} - {claim.get('title')}")
    print(f"Recommended evidence: {evidence_id}")
    print("Required nodes: " + ", ".join(task.get("required_nodes", []) or ["-"]))
    print("Acceptance gates: " + ", ".join(task.get("acceptance_gates", []) or ["-"]))
    print("Cannot claim: " + "; ".join(task.get("cannot_claim", []) or claim.get("cannot_claim", []) or ["-"]))
    if evidence_id in graph.experiments:
        runtime = graph.experiments[evidence_id].get("runtime") or {}
        for key in ["smoke_command", "test_command", "run_command"]:
            if runtime.get(key):
                print(f"{key}: {runtime[key]}")
        if runtime.get("package_dir"):
            print(f"cwd: {ROOT / runtime['package_dir']}")
    if task.get("blocked_by"):
        print("Blocked by: " + ", ".join(task["blocked_by"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
