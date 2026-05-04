from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare minimal agent context for a claim or evidence package.")
    parser.add_argument("--claim")
    parser.add_argument("--evidence")
    args = parser.parse_args()

    graph = load_graph(ROOT)
    if not args.claim and not args.evidence:
        parser.error("provide --claim or --evidence")

    claims = set()
    evidence_ids = set()
    if args.claim:
        if args.claim not in graph.claims:
            print(f"Unknown claim: {args.claim}", file=sys.stderr)
            return 2
        claims.add(args.claim)
        evidence_ids.update(graph.claims[args.claim].get("supported_by", []) or [])
        evidence_ids.update(edge["from"] for edge in graph.evidence_edges if edge.get("to") == args.claim)
    if args.evidence:
        if args.evidence not in graph.experiments:
            print(f"Unknown evidence: {args.evidence}", file=sys.stderr)
            return 2
        evidence_ids.add(args.evidence)
        claims.add(graph.experiments[args.evidence]["claim"])
        claims.update(graph.experiments[args.evidence].get("secondary_claims", []) or [])

    print("# Agent Context")
    print("## Claims")
    for claim_id in sorted(claims):
        claim = graph.claims[claim_id]
        print(f"- {claim_id}: {claim['status']} - {claim['title']}")
        print(f"  cannot_claim: {claim.get('cannot_claim', [])}")
        print(f"  next_required_evidence: {claim.get('next_required_evidence', [])}")
    print("## Evidence")
    for evidence_id in sorted(evidence_ids):
        evidence = graph.experiments[evidence_id]
        runtime = evidence.get("runtime") or {}
        print(f"- {evidence_id}: {evidence.get('status')} - {evidence.get('title')}")
        print(f"  package: {runtime.get('package_dir')}")
        print(f"  run: {runtime.get('run_command')}")
        print(f"  test: {runtime.get('test_command')}")
        print(f"  metrics: {runtime.get('metrics_files', [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

