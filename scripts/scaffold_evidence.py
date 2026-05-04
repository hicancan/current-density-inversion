from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph


def _write_new(path: Path, text: str) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a standard claim-graph evidence package skeleton.")
    parser.add_argument("--claim", required=True, help="Existing claim id, for example C10_pdn_kcl_distribution_need.")
    parser.add_argument("--evidence", required=True, help="New evidence id, for example E10_pdn_kcl_distribution.")
    parser.add_argument("--package-dir", help="Package directory under experiments/evidence. Defaults to evidence id.")
    args = parser.parse_args()

    graph = load_graph(ROOT)
    if args.claim not in graph.claims:
        raise SystemExit(f"Unknown claim id: {args.claim}")
    if args.evidence in graph.experiments:
        raise SystemExit(f"Evidence already registered: {args.evidence}")

    package_name = args.package_dir or args.evidence
    package_dir = ROOT / "experiments" / "evidence" / package_name
    if package_dir.exists():
        raise SystemExit(f"Package directory already exists: {package_dir}")

    _write_new(package_dir / "README.md", f"# {args.evidence}\n\nClaim: `{args.claim}`.\n")
    _write_new(package_dir / "REPRODUCE.md", "# Reproduce\n\n```powershell\nuv run python src/run_all.py\n```\n")
    _write_new(package_dir / "METRICS_SCHEMA.md", "# Metrics Schema\n\n`outputs/metrics.json` must include acceptance gates.\n")
    _write_new(package_dir / "FAILURE_MODES.md", "# Failure Modes\n\nDocument failures as claim boundaries.\n")
    _write_new(package_dir / "requirements.txt", "")
    _write_new(package_dir / "configs" / "default.json", "{\n  \"seed\": 0\n}\n")
    _write_new(package_dir / "tests" / "test_interface.py", "def test_placeholder() -> None:\n    assert True\n")
    _write_new(package_dir / "src" / "run_all.py", "from __future__ import annotations\n\n\nif __name__ == \"__main__\":\n    print(\"scaffold only\")\n")
    _write_new(package_dir / "GRAPH_UPDATE_CHECKLIST.md", f"""# Graph Update Checklist\n\n- Register `{args.evidence}` in `research_graph/experiments.yml`.\n- Add evidence edge(s) in `research_graph/evidence_edges.yml`.\n- Update claim `{args.claim}` only if evidence changes status or boundaries.\n- Register outputs in `research_graph/artifacts.yml` when generated.\n- Run `uv run python scripts/validate_graph.py`.\n""")
    print(f"Created evidence scaffold: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
