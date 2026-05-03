from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot.graph import claim_matrix_markdown, evidence_edge_table_markdown, load_graph


def main() -> int:
    graph = load_graph(ROOT)
    output_dir = ROOT / "outputs" / "by_claim"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "CLAIM_MATRIX.md").write_text(claim_matrix_markdown(graph), encoding="utf-8")
    (output_dir / "EVIDENCE_EDGE_TABLE.md").write_text(evidence_edge_table_markdown(graph), encoding="utf-8")
    print("Rendered outputs/by_claim/CLAIM_MATRIX.md")
    print("Rendered outputs/by_claim/EVIDENCE_EDGE_TABLE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
