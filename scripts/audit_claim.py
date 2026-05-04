from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph, metrics_gate_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Print a claim-centered audit package.")
    parser.add_argument("claim_id")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    graph = load_graph(ROOT)
    if args.claim_id not in graph.claims:
        print(f"Unknown claim: {args.claim_id}", file=sys.stderr)
        return 2
    claim = graph.claims[args.claim_id]
    edges = [edge for edge in graph.evidence_edges if edge.get("to") == args.claim_id]
    evidence_ids = sorted({edge["from"] for edge in edges} | set(claim.get("supported_by", []) or []))
    evidence = {}
    for evidence_id in evidence_ids:
        exp = graph.experiments.get(evidence_id, {})
        metrics = []
        for rel_path in (exp.get("runtime") or {}).get("metrics_files", []) or []:
            gate = metrics_gate_status(ROOT / rel_path)
            metrics.append({"path": rel_path, "gate": gate.gate, "ok": gate.ok})
        evidence[evidence_id] = {
            "status": exp.get("status"),
            "package_dir": (exp.get("runtime") or {}).get("package_dir"),
            "metrics": metrics,
            "summary": exp.get("result_summary"),
        }
    payload = {
        "claim": args.claim_id,
        "status": claim.get("status"),
        "supported_by": claim.get("supported_by", []),
        "limited_by": claim.get("limited_by", []),
        "cannot_claim": claim.get("cannot_claim", []),
        "limitations": claim.get("limitations", []),
        "next_required_evidence": claim.get("next_required_evidence", []),
        "edges": edges,
        "evidence": evidence,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"# Claim Audit: {args.claim_id}")
        print(f"status: {payload['status']}")
        print(f"supported_by: {', '.join(payload['supported_by']) or '-'}")
        print(f"limited_by: {', '.join(payload['limited_by']) or '-'}")
        print("cannot_claim:")
        for item in payload["cannot_claim"]:
            print(f"- {item}")
        print("next_required_evidence:")
        for item in payload["next_required_evidence"]:
            print(f"- {item}")
        print("evidence:")
        for evidence_id, item in evidence.items():
            metric_text = "; ".join(f"{m['path']} {m['gate']}={m['ok']}" for m in item["metrics"]) or "no metrics"
            print(f"- {evidence_id}: {item['status']} ({metric_text})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

