from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph


def _select_command(runtime: dict, mode: str) -> str:
    keys = {
        "run": ["run_command"],
        "smoke": ["smoke_command", "run_command"],
        "test": ["test_command"],
    }[mode]
    for key in keys:
        command = runtime.get(key)
        if command:
            return str(command)
    raise KeyError(f"no {mode} command for runtime package")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a claim-graph evidence package.")
    parser.add_argument("evidence", nargs="*", help="Evidence ids such as E01_canonical_forward_sanity.")
    parser.add_argument("--all", action="store_true", help="Run every registered evidence package.")
    parser.add_argument("--mode", choices=["run", "smoke", "test"], default="smoke")
    parser.add_argument("--continue-on-fail", action="store_true")
    args = parser.parse_args()

    graph = load_graph(ROOT)
    if args.all:
        evidence_ids = list(graph.experiments)
    else:
        evidence_ids = args.evidence
    if not evidence_ids:
        parser.error("provide evidence ids or --all")

    failures: list[str] = []
    for evidence_id in evidence_ids:
        if evidence_id not in graph.experiments:
            print(f"Unknown evidence id: {evidence_id}", file=sys.stderr)
            return 2
        runtime = graph.experiments[evidence_id].get("runtime")
        if not runtime:
            print(f"{evidence_id}: no runtime command registered")
            continue
        package_dir = ROOT / runtime["package_dir"]
        command = _select_command(runtime, args.mode)
        print(f"\n== {evidence_id} [{args.mode}] ==")
        print(f"cwd: {package_dir}")
        print(f"$ {command}")
        result = subprocess.run(command, cwd=package_dir, shell=True)
        if result.returncode != 0:
            failures.append(evidence_id)
            print(f"{evidence_id}: failed with exit code {result.returncode}", file=sys.stderr)
            if not args.continue_on_fail:
                return result.returncode

    if failures:
        print(f"Failed evidence packages: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

