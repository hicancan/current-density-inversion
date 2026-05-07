"""E23 round 5 — ensemble, robust margins, greedy excitation, adversarial stress."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from config import load_config
from layout_schema import validate_layout, parse_layout
from graph_builder import build_graph, graph_summary
from incidence import build_incidence_matrix, build_source_vector
from hodge_basis import assemble_hodge_basis, validate_basis
from forward import build_centerline_operator
from oqci_adapter import run_oqci
from layout_ensemble import generate_ensemble, portfolio_summary
from metrics import build_metrics
from reporting import write_outputs


def run_one_layout(layout: dict, config: dict, layout_name: str) -> dict:
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    summary = graph_summary(graph)
    D, node_order, edge_order = build_incidence_matrix(graph)
    q = build_source_vector(graph, node_order, config.get("source_current", 1.0))
    hodge_result = assemble_hodge_basis(graph, edge_order, D, q, config)
    validation = validate_basis(hodge_result, D, q, graph, config)
    grid_size = config.get("grid_size", 24)
    sensor_z = config.get("sensor_z", 0.35)
    A = build_centerline_operator(graph, edge_order, grid_size, sensor_z)
    oqci = run_oqci(graph, edge_order, D, hodge_result, A, config)
    return {
        "layout_name": layout_name, "graph": graph, "summary": summary,
        "valid": True, "D": D, "q": q, "node_order": node_order,
        "edge_order": edge_order, "hodge_result": hodge_result,
        "validation": validation, "oqci": oqci,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="E23 Round 5")
    parser.add_argument("--config", default=str(ROOT / "configs" / "default.json"))
    parser.add_argument("--out", default=str(ROOT / "outputs"))
    parser.add_argument("--data", default="")
    parser.add_argument("--examples-dir", default=str(ROOT / "examples"))
    args = parser.parse_args()

    config = load_config(args.config)
    np.random.seed(config.get("seed", 20260506))

    print(f"E23 Round 5 — Robust Observable-Quotient Certificate")
    print(f"Config: {args.config}")

    # Load ensemble (generate more to compensate for KCL-failing layouts)
    target = config.get("ensemble_count", 44)
    ensemble_n = max(target, int(target * 1.5))
    ensemble = generate_ensemble(n_layouts=ensemble_n, seed=config.get("seed", 20260506))
    port_summary = portfolio_summary(ensemble)
    print(f"Ensemble generated: {port_summary['total']} layouts, {port_summary['multiport']} multiport")
    print()

    # Load static examples too
    from layout_schema import load_layout
    examples_dir = Path(args.examples_dir)
    static_names = config.get("examples", [])
    static_layouts = []
    for name in static_names:
        path = examples_dir / name
        if path.exists():
            ly = load_layout(path)
            errors = validate_layout(ly)
            if not errors:
                static_layouts.append(ly)
    print(f"Static examples: {len(static_layouts)}")

    # Process: static examples first, then ensemble (cap valid results)
    max_valid = config.get("max_layouts", 999)
    all_layouts = static_layouts + ensemble
    total_generated = len(all_layouts)
    total_multiport_gen = port_summary["multiport"] + sum(
        1 for l in static_layouts if len(l.get("ports", [])) > 2)

    results = []
    for i, layout in enumerate(all_layouts):
        name = layout.get("description", f"layout_{i}")[:60] if isinstance(layout, dict) else f"layout_{i}"
        # Use ensemble meta if available
        meta = layout.get("_ensemble_meta", {})
        name_short = f"e{i}" if meta else f"l{i}"
        print(f"[{i+1}/{len(all_layouts)}] {name_short}  ", end="", flush=True)
        r = run_one_layout(layout, config, name_short)
        # Skip layouts with KCL failures (disconnected graphs)
        if not r["validation"].get("port_loop_kcl_pass", False):
            print(f"SKIP (KCL fail: {r['validation'].get('kcl_residual_port_loop', 0):.2e})")
            continue
        results.append(r)
        if len(results) >= max_valid:
            break
        h = r["hodge_result"]
        o = r["oqci"]
        rm = o.get("robust_margins", {})
        print(f"gamma_crit={rm.get('min_gamma_critical', 0):.4f} h1h2_g={o.get('h1_h2_gamma', 0):.4f}")

    # Build metrics
    layouts_processed = [
        {"layout_name": r["layout_name"], "summary": r["summary"],
         "graph": r["graph"], "valid": r["valid"]}
        for r in results
    ]
    hodge_results = [r["hodge_result"] for r in results]
    oqci_results = [r["oqci"] for r in results]
    validation_results = [r["validation"] for r in results]
    config["_total_generated"] = total_generated
    config["_total_multiport_gen"] = total_multiport_gen
    metrics = build_metrics(layouts_processed, config, hodge_results, oqci_results, validation_results)

    outputs_dir = Path(args.out)
    result_data = {"layouts_processed": layouts_processed, "hodge_results": hodge_results,
                   "oqci_results": oqci_results, "validation_results": validation_results}
    write_outputs(outputs_dir, metrics, result_data)

    print(f"\n{'='*60}")
    print("ACCEPTANCE GATES")
    print("=" * 60)
    for gate, passed in metrics["acceptance_gates"].items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {gate}")
    print(f"\nAll gates passed: {metrics['all_acceptance_gates_passed']}")
    print(f"Outputs written to: {outputs_dir}")
    return 0 if metrics["all_acceptance_gates_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
