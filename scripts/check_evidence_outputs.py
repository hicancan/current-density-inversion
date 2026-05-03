from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph


def _metrics_pass(metrics: dict) -> tuple[bool, str]:
    if "all_acceptance_gates_passed" in metrics:
        return bool(metrics["all_acceptance_gates_passed"]), "all_acceptance_gates_passed"
    gates = metrics.get("acceptance_gates")
    if isinstance(gates, dict) and "all_scientific_gates_passed" in gates:
        return bool(gates["all_scientific_gates_passed"]), "acceptance_gates.all_scientific_gates_passed"
    if isinstance(gates, dict) and gates:
        bool_values = [value for value in gates.values() if isinstance(value, bool)]
        if bool_values:
            return all(bool_values), "all boolean acceptance_gates"
    return False, "no recognized gate field"


def main() -> int:
    graph = load_graph(ROOT)
    failures: list[str] = []
    checked = 0
    for evidence_id, evidence in graph.experiments.items():
        runtime = evidence.get("runtime") or {}
        metrics_files = runtime.get("metrics_files") or []
        if not metrics_files:
            package_dir = runtime.get("package_dir")
            if package_dir and not (ROOT / package_dir).exists():
                failures.append(f"{evidence_id}: runtime package missing")
            continue
        for rel_path in metrics_files:
            checked += 1
            path = ROOT / rel_path
            if not path.exists():
                failures.append(f"{evidence_id}: missing metrics file {rel_path}")
                continue
            metrics = json.loads(path.read_text(encoding="utf-8"))
            ok, gate = _metrics_pass(metrics)
            print(f"{evidence_id}: {gate}={ok}")
            if not ok:
                failures.append(f"{evidence_id}: metrics gate failed via {gate}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"Evidence output check passed for {checked} metrics file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

