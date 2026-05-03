from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph, validate_graph


def main() -> int:
    graph = load_graph(ROOT)
    issues = validate_graph(graph)
    for issue in issues:
        print(f"{issue.severity.upper()}: {issue.location}: {issue.message}")
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        print(f"Graph validation failed with {len(errors)} error(s).")
        return 1
    print(f"Graph validation passed with {len(issues)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
