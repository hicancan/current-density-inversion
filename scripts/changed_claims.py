from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph


def main() -> int:
    graph = load_graph(ROOT)
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "research_graph", "experiments/evidence", "outputs/by_claim"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    changed = set(result.stdout.splitlines())
    claims = set()
    if any(path.startswith("research_graph/claims.yml") for path in changed):
        claims.update(graph.claims)
    for evidence_id, evidence in graph.experiments.items():
        package = (evidence.get("runtime") or {}).get("package_dir")
        outputs = evidence.get("outputs", []) or []
        if package and any(path.startswith(package.replace("\\", "/")) for path in changed):
            claims.add(evidence["claim"])
            claims.update(evidence.get("secondary_claims", []) or [])
        if any(output in changed for output in outputs):
            claims.add(evidence["claim"])
            claims.update(evidence.get("secondary_claims", []) or [])
    for claim_id in sorted(claims):
        print(claim_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

