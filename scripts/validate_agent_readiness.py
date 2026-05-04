from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph, readiness_score


MIN_READINESS_SCORE = 90


def main() -> int:
    graph = load_graph(ROOT)
    score, notes = readiness_score(graph)
    print(f"Agent readiness score: {score}/100")
    for note in notes:
        print(f"- {note}")
    if score < MIN_READINESS_SCORE:
        print(f"Agent readiness failed below threshold {MIN_READINESS_SCORE}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
