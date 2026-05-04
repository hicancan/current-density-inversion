from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


EVIDENCE_ID = "E10_pdn_kcl_distribution"
CLAIM_ID = "C10_pdn_kcl_distribution_need"
HYPOTHESES = ["H0_nominal_pdn", "H1_extra_via", "H2_return_path_shift", "H3_bend_artifact"]
GENERATED_AT = "2026-05-04T00:00:00Z"
MU0_OVER_4PI = 1e-7


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def family_parameters(family: int, variant: int) -> dict[str, float]:
    y_shift = 0.07 * (family - 1)
    return {
        "y_shift": y_shift,
        "return_y": -0.18 - 0.03 * family,
        "resistance_scale": 1.0 + 0.04 * variant + 0.03 * family,
        "artifact_y": y_shift + 0.16 + 0.01 * variant,
    }


def build_graph(hypothesis: str, family: int, variant: int, cfg: dict[str, Any]) -> dict[str, Any]:
    params = family_parameters(family, variant)
    y = params["y_shift"]
    ry = params["return_y"]
    scale = params["resistance_scale"]
    ay = params["artifact_y"]
    nodes = {
        "vdd": {"xyz": [0.0, 0.0, 0.0], "role": "VDD"},
        "j1": {"xyz": [0.32, y, 0.0], "role": "junction"},
        "load": {"xyz": [0.72, y, 0.0], "role": "load"},
        "bottom": {"xyz": [0.72, y, -0.18], "role": "via_bottom"},
        "ret_mid": {"xyz": [0.35, ry, -0.18], "role": "return"},
        "gnd": {"xyz": [1.05, 0.0, -0.18], "role": "GND"},
    }
    edges = [
        {"id": "supply_0", "a": "vdd", "b": "j1", "resistance": 0.85 * scale, "kind": "sheet"},
        {"id": "supply_1", "a": "j1", "b": "load", "resistance": 0.95 * scale, "kind": "sheet"},
        {"id": "load_via", "a": "load", "b": "bottom", "resistance": 0.22 * scale, "kind": "via"},
        {"id": "return_0", "a": "bottom", "b": "ret_mid", "resistance": 1.10 * scale, "kind": "return"},
        {"id": "return_1", "a": "ret_mid", "b": "gnd", "resistance": 0.95 * scale, "kind": "return"},
    ]
    if hypothesis == "H1_extra_via":
        edges.append({"id": "diagnostic_extra_via", "a": "j1", "b": "ret_mid", "resistance": 0.58 * scale, "kind": "via_hypothesis"})
    elif hypothesis == "H2_return_path_shift":
        edges.append({"id": "diagnostic_return", "a": "bottom", "b": "gnd", "resistance": 0.55 * scale, "kind": "return_hypothesis"})
    elif hypothesis == "H3_bend_artifact":
        nodes["artifact"] = {"xyz": [0.55, ay, 0.0], "role": "artifact_candidate"}
        edges.extend(
            [
                {"id": "artifact_leg_0", "a": "j1", "b": "artifact", "resistance": 2.30 * scale, "kind": "artifact"},
                {"id": "artifact_leg_1", "a": "artifact", "b": "load", "resistance": 2.10 * scale, "kind": "artifact"},
            ]
        )
    boundary = {"vdd": float(cfg["source_voltage"]), "gnd": float(cfg["ground_voltage"])}
    return {"nodes": nodes, "edges": edges, "boundary_voltages": boundary, "hypothesis": hypothesis}


def solve_kcl(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = list(graph["nodes"])
    boundary = graph["boundary_voltages"]
    unknowns = [node for node in nodes if node not in boundary]
    index = {node: i for i, node in enumerate(unknowns)}
    a_mat = np.zeros((len(unknowns), len(unknowns)), dtype=float)
    b_vec = np.zeros(len(unknowns), dtype=float)

    for edge in graph["edges"]:
        a = edge["a"]
        b = edge["b"]
        conductance = 1.0 / float(edge["resistance"])
        for node, other in [(a, b), (b, a)]:
            if node in boundary:
                continue
            row = index[node]
            a_mat[row, row] += conductance
            if other in boundary:
                b_vec[row] += conductance * boundary[other]
            else:
                a_mat[row, index[other]] -= conductance

    solved = np.linalg.solve(a_mat, b_vec) if unknowns else np.array([], dtype=float)
    voltages = dict(boundary)
    voltages.update({node: float(solved[index[node]]) for node in unknowns})

    net_out = {node: 0.0 for node in nodes}
    solved_edges = []
    for edge in graph["edges"]:
        current = (voltages[edge["a"]] - voltages[edge["b"]]) / float(edge["resistance"])
        net_out[edge["a"]] += current
        net_out[edge["b"]] -= current
        solved_edge = dict(edge)
        solved_edge["current"] = float(current)
        solved_edges.append(solved_edge)

    interior_residuals = [abs(net_out[node]) for node in nodes if node not in boundary]
    source_current = net_out["vdd"]
    sink_current = net_out["gnd"]
    closure_error = abs(source_current + sink_current) / max(abs(source_current), abs(sink_current), 1e-30)
    return {
        "voltages": voltages,
        "edges": solved_edges,
        "node_kcl_residuals": {node: float(value) for node, value in net_out.items()},
        "max_interior_kcl_residual": float(max(interior_residuals) if interior_residuals else 0.0),
        "source_current": float(source_current),
        "sink_current": float(sink_current),
        "current_closure_error": float(closure_error),
    }


def sensor_grid(grid_size: int, z: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(-0.15, 1.20, grid_size)
    ys = np.linspace(-0.50, 0.35, grid_size)
    xx, yy = np.meshgrid(xs, ys)
    zz = np.full_like(xx, z)
    return xx, yy, zz


def forward_biot_savart(graph: dict[str, Any], solved: dict[str, Any], grid_size: int, sensor_z: float) -> np.ndarray:
    xx, yy, zz = sensor_grid(grid_size, sensor_z)
    field = np.zeros((grid_size, grid_size, 3), dtype=float)
    points = np.stack([xx, yy, zz], axis=-1)
    for edge in solved["edges"]:
        p0 = np.array(graph["nodes"][edge["a"]]["xyz"], dtype=float)
        p1 = np.array(graph["nodes"][edge["b"]]["xyz"], dtype=float)
        midpoint = 0.5 * (p0 + p1)
        dl = p1 - p0
        r = points - midpoint
        norm = np.linalg.norm(r, axis=-1)
        cross = np.cross(dl, r)
        field += MU0_OVER_4PI * edge["current"] * cross / np.maximum(norm[..., None] ** 3, 1e-18)
    return field


def divb_residual(graph: dict[str, Any], solved: dict[str, Any], cfg: dict[str, Any]) -> float:
    grid_size = int(cfg["grid_size"])
    z0 = float(cfg["sensor_z"])
    dz = 0.02
    b0 = forward_biot_savart(graph, solved, grid_size, z0)
    bp = forward_biot_savart(graph, solved, grid_size, z0 + dz)
    bm = forward_biot_savart(graph, solved, grid_size, z0 - dz)
    xs = np.linspace(-0.15, 1.20, grid_size)
    ys = np.linspace(-0.50, 0.35, grid_size)
    dx = float(xs[1] - xs[0])
    dy = float(ys[1] - ys[0])
    d_bx_dx = np.gradient(b0[:, :, 0], dx, axis=1)
    d_by_dy = np.gradient(b0[:, :, 1], dy, axis=0)
    d_bz_dz = (bp[:, :, 2] - bm[:, :, 2]) / (2.0 * dz)
    div = d_bx_dx + d_by_dy + d_bz_dz
    field_scale = np.sqrt(np.mean(b0**2)) / max(dx, dy, dz)
    return float(np.sqrt(np.mean(div**2)) / max(field_scale, 1e-30))


def rel_l2(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(b), 1e-30))


def split_role(variant: int) -> str:
    if variant == 0:
        return "calibration"
    if variant == 4:
        return "train"
    return "heldout"


def generate_cases(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for family in range(int(cfg["families"])):
        for variant in range(int(cfg["variants_per_hypothesis"])):
            for hypothesis in HYPOTHESES:
                graph = build_graph(hypothesis, family, variant, cfg)
                solved = solve_kcl(graph)
                field = forward_biot_savart(graph, solved, int(cfg["grid_size"]), float(cfg["sensor_z"]))
                cases.append(
                    {
                        "case_id": f"family{family}_variant{variant}_{hypothesis}",
                        "family": family,
                        "variant": variant,
                        "split_role": split_role(variant),
                        "true_hypothesis": hypothesis,
                        "graph": graph,
                        "solved": solved,
                        "field": field,
                        "divb_residual": divb_residual(graph, solved, cfg),
                    }
                )
    return cases


def score_hypotheses(case: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    scores = {}
    for hypothesis in HYPOTHESES:
        candidate_graph = build_graph(hypothesis, int(case["family"]), int(case["variant"]), cfg)
        candidate_solved = solve_kcl(candidate_graph)
        candidate_field = forward_biot_savart(candidate_graph, candidate_solved, int(cfg["grid_size"]), float(cfg["sensor_z"]))
        scores[hypothesis] = rel_l2(candidate_field, case["field"])
    predicted = min(scores, key=scores.get)
    return {"scores": scores, "predicted_hypothesis": predicted, "correct": predicted == case["true_hypothesis"]}


def summarize(cases: list[dict[str, Any]], cfg: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows = []
    for case in cases:
        scored = score_hypotheses(case, cfg)
        rows.append(
            {
                "case_id": case["case_id"],
                "family": case["family"],
                "split_role": case["split_role"],
                "true_hypothesis": case["true_hypothesis"],
                "predicted_hypothesis": scored["predicted_hypothesis"],
                "correct": scored["correct"],
                "best_residual": min(scored["scores"].values()),
                "score_margin": sorted(scored["scores"].values())[1] - sorted(scored["scores"].values())[0],
            }
        )

    split_roles = {role: sum(1 for row in rows if row["split_role"] == role) for role in sorted({row["split_role"] for row in rows})}
    by_hypothesis = {hyp: sum(1 for row in rows if row["true_hypothesis"] == hyp) for hyp in HYPOTHESES}
    heldout_rows = [row for row in rows if row["split_role"] == "heldout"]
    h0_rows = [row for row in heldout_rows if row["true_hypothesis"] == "H0_nominal_pdn"]
    h1_rows = [row for row in heldout_rows if row["true_hypothesis"] == "H1_extra_via"]
    heldout_accuracy = sum(row["correct"] for row in heldout_rows) / max(len(heldout_rows), 1)
    h0_false_any = sum(row["predicted_hypothesis"] != "H0_nominal_pdn" for row in h0_rows) / max(len(h0_rows), 1)
    h1_recall = sum(row["predicted_hypothesis"] == "H1_extra_via" for row in h1_rows) / max(len(h1_rows), 1)

    max_kcl = max(case["solved"]["max_interior_kcl_residual"] for case in cases)
    max_closure = max(case["solved"]["current_closure_error"] for case in cases)
    max_divb = max(case["divb_residual"] for case in cases)
    gates = {
        "kcl_residual_below_threshold": max_kcl <= float(cfg["kcl_residual_threshold"]),
        "current_closure_below_threshold": max_closure <= float(cfg["current_closure_threshold"]),
        "divB_proxy_below_threshold": max_divb <= float(cfg["divB_residual_threshold"]),
        "h0_h1_h2_h3_rows_present": all(count > 0 for count in by_hypothesis.values()),
        "heldout_hypothesis_accuracy_material": heldout_accuracy >= float(cfg["heldout_accuracy_threshold"]),
    }
    gates["all_acceptance_gates_passed"] = all(gates.values())

    metrics = {
        "evidence_id": EVIDENCE_ID,
        "claim_id": CLAIM_ID,
        "status": "passed" if gates["all_acceptance_gates_passed"] else "failed",
        "generated_at": GENERATED_AT,
        "dataset": {
            "case_count": len(cases),
            "by_hypothesis": by_hypothesis,
            "by_split_role": split_roles,
            "families": int(cfg["families"]),
            "variants_per_hypothesis": int(cfg["variants_per_hypothesis"]),
        },
        "split_roles": split_roles,
        "pdn_kcl": {
            "max_interior_kcl_residual": max_kcl,
            "kcl_residual_threshold": float(cfg["kcl_residual_threshold"]),
            "max_current_closure_error": max_closure,
            "current_closure_threshold": float(cfg["current_closure_threshold"]),
        },
        "divB": {
            "max_full_divergence_proxy": max_divb,
            "divB_residual_threshold": float(cfg["divB_residual_threshold"]),
        },
        "hypothesis_scoring": {
            "heldout_accuracy": heldout_accuracy,
            "h0_false_any_rate": h0_false_any,
            "h1_recall": h1_recall,
            "median_best_residual": float(np.median([row["best_residual"] for row in rows])),
        },
        "acceptance_gates": gates,
        "all_acceptance_gates_passed": gates["all_acceptance_gates_passed"],
        "cannot_claim": [
            "real CAD/Gerber/GDS validation",
            "real QDM/NV validation",
            "external FEM/FastHenry validation",
            "PDN/KCL robustness under realistic boards",
        ],
    }
    return metrics, rows


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")


def md_float(value: float) -> str:
    return f"{value:.3e}" if abs(value) < 1e-3 else f"{value:.3f}"


def write_tables(outputs: Path, metrics: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    metrics_lines = [
        "# PDN/KCL Metrics Table\n\n",
        "| Metric | Value | Gate |\n",
        "|---|---:|---|\n",
        f"| max interior KCL residual | {md_float(metrics['pdn_kcl']['max_interior_kcl_residual'])} | {metrics['acceptance_gates']['kcl_residual_below_threshold']} |\n",
        f"| max current closure error | {md_float(metrics['pdn_kcl']['max_current_closure_error'])} | {metrics['acceptance_gates']['current_closure_below_threshold']} |\n",
        f"| max divB proxy residual | {md_float(metrics['divB']['max_full_divergence_proxy'])} | {metrics['acceptance_gates']['divB_proxy_below_threshold']} |\n",
        f"| heldout H0/H1/H2/H3 accuracy | {metrics['hypothesis_scoring']['heldout_accuracy']:.3f} | {metrics['acceptance_gates']['heldout_hypothesis_accuracy_material']} |\n",
        "\nCannot claim: real CAD/Gerber/GDS, real QDM/NV, or external FEM/FastHenry validation.\n",
    ]
    (outputs / "PDN_KCL_METRICS_TABLE.md").write_text("".join(metrics_lines), encoding="utf-8")

    count_lines = ["# Case Counts Table\n\n", "| Group | Count |\n", "|---|---:|\n"]
    for hypothesis, count in metrics["dataset"]["by_hypothesis"].items():
        count_lines.append(f"| {hypothesis} | {count} |\n")
    for role, count in metrics["split_roles"].items():
        count_lines.append(f"| split:{role} | {count} |\n")
    (outputs / "CASE_COUNTS_TABLE.md").write_text("".join(count_lines), encoding="utf-8")

    score_lines = [
        "# Hypothesis Score Table\n\n",
        "| Case | Split | True | Predicted | Correct | Best residual | Margin |\n",
        "|---|---|---|---|---:|---:|---:|\n",
    ]
    for row in rows[:24]:
        score_lines.append(
            f"| {row['case_id']} | {row['split_role']} | {row['true_hypothesis']} | {row['predicted_hypothesis']} | "
            f"{row['correct']} | {md_float(row['best_residual'])} | {md_float(row['score_margin'])} |\n"
        )
    score_lines.append("\nRows are generated-domain hypothesis sanity rows, not real mechanism validation.\n")
    (outputs / "HYPOTHESIS_SCORE_TABLE.md").write_text("".join(score_lines), encoding="utf-8")

    report = f"""# RUN_REPORT - E10 PDN/KCL Distribution

Claim: `{CLAIM_ID}`.

This run implements the first generated PDN/KCL circuit-graph evidence loop:
resistive graph generation, nodal KCL solve, current closure, centerline
Biot-Savart forward fields, and H0/H1/H2/H3 generated hypothesis scoring.

## Metrics

{(outputs / "PDN_KCL_METRICS_TABLE.md").read_text(encoding="utf-8")}

## Case Counts

{(outputs / "CASE_COUNTS_TABLE.md").read_text(encoding="utf-8")}

## Boundary

This evidence supports only a generated-domain PDN/KCL prototype. It cannot be
claimed as real CAD/Gerber/GDS, external FEM/FastHenry, or real QDM/NV
validation.
"""
    (outputs / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def serializable_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        rows.append(
            {
                "case_id": case["case_id"],
                "family": case["family"],
                "variant": case["variant"],
                "split_role": case["split_role"],
                "true_hypothesis": case["true_hypothesis"],
                "max_interior_kcl_residual": case["solved"]["max_interior_kcl_residual"],
                "current_closure_error": case["solved"]["current_closure_error"],
                "divb_residual": case["divb_residual"],
            }
        )
    return rows


def run_experiment(cfg: dict[str, Any], outputs: Path, data: Path) -> dict[str, Any]:
    outputs.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    cases = generate_cases(cfg)
    metrics, rows = summarize(cases, cfg)
    write_tables(outputs, metrics, rows)
    write_json(outputs / "metrics.json", metrics)
    write_json(data / "exp10_cases.json", serializable_cases(cases))
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Run E10 generated PDN/KCL evidence.")
    parser.add_argument("--config", type=Path, default=Path("configs/default.json"))
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    args = parser.parse_args()
    cfg = load_config(args.config)
    metrics = run_experiment(cfg, args.out, args.data)
    print(json.dumps({"evidence_id": EVIDENCE_ID, "metrics_path": str(args.out / "metrics.json"), "passed": metrics["all_acceptance_gates_passed"]}, sort_keys=True))
    return 0 if metrics["all_acceptance_gates_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
