from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph, validate_graph


def main() -> int:
    graph = load_graph(ROOT)
    issues = validate_graph(graph)
    failures: list[str] = []

    incoming = {}
    for edge in graph.evidence_edges:
        incoming.setdefault((edge["from"], edge["to"]), set()).add(edge["relation"])

    for claim_id, claim in graph.claims.items():
        status = claim.get("status")
        supported_by = claim.get("supported_by", []) or []
        if status in {"supported", "supported_generated", "limited"} and not supported_by:
            failures.append(f"{claim_id}: status {status} requires supporting evidence")
        if status == "supported_generated":
            if not claim.get("cannot_claim"):
                failures.append(f"{claim_id}: supported_generated requires cannot_claim")
            if not claim.get("limitations"):
                failures.append(f"{claim_id}: supported_generated requires limitations")
        if claim_id == "C12_real_qdm_nv_validation" and status != "blocked":
            failures.append("C12_real_qdm_nv_validation must remain blocked until measured rows exist")
        for evidence_id in supported_by:
            if (evidence_id, claim_id) not in incoming:
                failures.append(f"{claim_id}: supported_by {evidence_id} has no evidence edge")
        for evidence_id in claim.get("limited_by", []) or []:
            if "limits" not in incoming.get((evidence_id, claim_id), set()):
                failures.append(f"{claim_id}: limited_by {evidence_id} lacks limits edge")
        for evidence_id in claim.get("contradicted_by", []) or []:
            if "contradicts" not in incoming.get((evidence_id, claim_id), set()):
                failures.append(f"{claim_id}: contradicted_by {evidence_id} lacks contradicts edge")

    failures.extend(f"{issue.location}: {issue.message}" for issue in issues if issue.severity == "error")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Claim gate check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

