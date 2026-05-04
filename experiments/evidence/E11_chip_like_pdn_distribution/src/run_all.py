from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


EVIDENCE_ID = "E11_chip_like_pdn_distribution"
CLAIM_ID = "C10_pdn_kcl_distribution_need"
HYPOTHESES = [
    "H0_nominal",
    "H1_via_defect_or_extra",
    "H2_return_bottleneck",
    "H3_bend_width_artifact",
]
GENERATED_AT = "2026-05-04T00:00:00Z"
MU0_OVER_4PI = 1e-7
LAYERS = {
    "L3_top_power_straps": 0.0,
    "L2_intermediate_mesh": -0.08,
    "L1_lower_mesh": -0.16,
    "L0_return_grid": -0.26,
}


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _node(x: float, y: float, z: float, role: str, layer_id: str) -> dict[str, Any]:
    return {"xyz": [float(x), float(y), float(z)], "role": role, "layer_id": layer_id}


def _edge(edge_id: str, a: str, b: str, resistance: float, role: str, layer_id: str | None = None) -> dict[str, Any]:
    return {
        "id": edge_id,
        "a": a,
        "b": b,
        "resistance": float(resistance),
        "role": role,
        "kind": role,
        "layer_id": layer_id,
    }


def family_parameters(family: int, variant: int, hypothesis: str) -> dict[str, float]:
    y_offset = 0.035 * (family - 1.5)
    pitch_scale = 1.0 + 0.03 * family
    resistance_scale = 1.0 + 0.025 * variant + 0.035 * family
    return_shift = -0.045 if hypothesis == "H2_return_bottleneck" else 0.0
    bend_shift = 0.07 + 0.006 * variant if hypothesis == "H3_bend_width_artifact" else 0.0
    via_multiplier = 8.0 if hypothesis == "H1_via_defect_or_extra" else 1.0
    return_bottleneck = 6.0 if hypothesis == "H2_return_bottleneck" else 1.0
    return {
        "y_offset": y_offset,
        "pitch_scale": pitch_scale,
        "resistance_scale": resistance_scale,
        "return_shift": return_shift,
        "bend_shift": bend_shift,
        "via_multiplier": via_multiplier,
        "return_bottleneck": return_bottleneck,
    }


def _mesh_node_id(prefix: str, ix: int, iy: int) -> str:
    return f"{prefix}_{ix}_{iy}"


def build_graph(hypothesis: str, family: int, variant: int, cfg: dict[str, Any]) -> dict[str, Any]:
    if hypothesis not in HYPOTHESES:
        raise ValueError(f"unknown hypothesis {hypothesis}")
    params = family_parameters(family, variant, hypothesis)
    y0 = params["y_offset"]
    scale = params["resistance_scale"]
    pitch = params["pitch_scale"]
    xs = [0.12, 0.47 * pitch, 0.82 * pitch]
    ys = [-0.24 + y0, 0.0 + y0, 0.24 + y0]
    return_ys = [y + params["return_shift"] for y in ys]

    nodes: dict[str, dict[str, Any]] = {
        "vdd_bump": _node(-0.08, y0, LAYERS["L3_top_power_straps"], "VDD", "L3_top_power_straps"),
        "gnd_bump": _node(1.05 * pitch, y0 + params["return_shift"], LAYERS["L0_return_grid"], "GND", "L0_return_grid"),
    }

    top_rows = {"top_u": ys[2], "top_l": ys[0]}
    for prefix, y in top_rows.items():
        for ix, x in enumerate(xs):
            nodes[f"{prefix}_{ix}"] = _node(x, y, LAYERS["L3_top_power_straps"], "power_strap", "L3_top_power_straps")

    for prefix, layer_id in [
        ("m2", "L2_intermediate_mesh"),
        ("m1", "L1_lower_mesh"),
    ]:
        for ix, x in enumerate(xs):
            for iy, y in enumerate(ys):
                nodes[_mesh_node_id(prefix, ix, iy)] = _node(x, y, LAYERS[layer_id], "mesh_junction", layer_id)

    for ix, x in enumerate(xs):
        for iy, y in enumerate(return_ys):
            nodes[_mesh_node_id("ret", ix, iy)] = _node(x, y, LAYERS["L0_return_grid"], "return_grid", "L0_return_grid")

    edges: list[dict[str, Any]] = []
    edges.append(_edge("port_vdd_upper", "vdd_bump", "top_u_0", 0.18 * scale, "boundary_port", "L3_top_power_straps"))
    edges.append(_edge("port_vdd_lower", "vdd_bump", "top_l_0", 0.20 * scale, "boundary_port", "L3_top_power_straps"))
    edges.append(_edge("port_gnd", "ret_2_1", "gnd_bump", 0.16 * scale, "boundary_port", "L0_return_grid"))
    edges.append(_edge("port_gnd_upper", "ret_2_2", "gnd_bump", 0.24 * scale, "boundary_port", "L0_return_grid"))

    for prefix in ["top_u", "top_l"]:
        for ix in range(2):
            edges.append(_edge(f"{prefix}_strap_{ix}", f"{prefix}_{ix}", f"{prefix}_{ix + 1}", 0.42 * scale, "power_strap", "L3_top_power_straps"))
    for ix in range(3):
        edges.append(_edge(f"top_cross_{ix}", f"top_u_{ix}", f"top_l_{ix}", 1.15 * scale, "power_strap_crosslink", "L3_top_power_straps"))

    for prefix, layer_id, base_r in [
        ("m2", "L2_intermediate_mesh", 0.58),
        ("m1", "L1_lower_mesh", 0.72),
    ]:
        for iy in range(3):
            for ix in range(2):
                edges.append(_edge(f"{prefix}_h_{ix}_{iy}", _mesh_node_id(prefix, ix, iy), _mesh_node_id(prefix, ix + 1, iy), base_r * scale, "mesh_horizontal", layer_id))
        for ix in range(3):
            for iy in range(2):
                edges.append(_edge(f"{prefix}_v_{ix}_{iy}", _mesh_node_id(prefix, ix, iy), _mesh_node_id(prefix, ix, iy + 1), (base_r * 1.08) * scale, "mesh_vertical", layer_id))

    for iy in range(3):
        for ix in range(2):
            multiplier = params["return_bottleneck"] if (hypothesis == "H2_return_bottleneck" and ix == 1 and iy == 1) else 1.0
            edges.append(_edge(f"ret_h_{ix}_{iy}", _mesh_node_id("ret", ix, iy), _mesh_node_id("ret", ix + 1, iy), 0.46 * scale * multiplier, "return_grid", "L0_return_grid"))
    for ix in range(3):
        for iy in range(2):
            multiplier = params["return_bottleneck"] if (hypothesis == "H2_return_bottleneck" and ix == 1 and iy == 0) else 1.0
            edges.append(_edge(f"ret_v_{ix}_{iy}", _mesh_node_id("ret", ix, iy), _mesh_node_id("ret", ix, iy + 1), 0.50 * scale * multiplier, "return_grid", "L0_return_grid"))

    for ix in range(3):
        edges.append(_edge(f"top_u_to_m2_{ix}", f"top_u_{ix}", _mesh_node_id("m2", ix, 2), 0.19 * scale, "via_stack", None))
        edges.append(_edge(f"top_l_to_m2_{ix}", f"top_l_{ix}", _mesh_node_id("m2", ix, 0), 0.19 * scale, "via_stack", None))
    for ix in range(3):
        for iy in range(3):
            via_mult = params["via_multiplier"] if (hypothesis == "H1_via_defect_or_extra" and ix == 1 and iy == 1) else 1.0
            edges.append(_edge(f"via_m2_m1_{ix}_{iy}", _mesh_node_id("m2", ix, iy), _mesh_node_id("m1", ix, iy), 0.16 * scale * via_mult, "via_stack", None))

    load_sites = [(0, 0), (1, 1), (2, 2)]
    for idx, (ix, iy) in enumerate(load_sites):
        load_r = (0.62 + 0.04 * idx + 0.02 * variant) * scale
        if hypothesis == "H2_return_bottleneck" and idx == 1:
            load_r *= 0.80
        edges.append(_edge(f"distributed_load_{idx}", _mesh_node_id("m1", ix, iy), _mesh_node_id("ret", ix, iy), load_r, "distributed_load", None))

    if hypothesis == "H1_via_defect_or_extra":
        edges.append(_edge("diagnostic_extra_via_stack", "m2_0_1", "m1_2_1", 0.28 * scale, "via_hypothesis", None))
    if hypothesis == "H3_bend_width_artifact":
        nodes["artifact_bend_0"] = _node(0.42 * pitch, ys[2] + params["bend_shift"], LAYERS["L3_top_power_straps"], "artifact_candidate", "L3_top_power_straps")
        nodes["artifact_bend_1"] = _node(0.68 * pitch, ys[2] + params["bend_shift"], LAYERS["L3_top_power_straps"], "artifact_candidate", "L3_top_power_straps")
        edges.append(_edge("artifact_bend_leg_0", "top_u_1", "artifact_bend_0", 1.45 * scale, "bend_width_artifact", "L3_top_power_straps"))
        edges.append(_edge("artifact_bend_leg_1", "artifact_bend_0", "artifact_bend_1", 0.55 * scale, "bend_width_artifact", "L3_top_power_straps"))
        edges.append(_edge("artifact_bend_leg_2", "artifact_bend_1", "top_u_2", 1.25 * scale, "bend_width_artifact", "L3_top_power_straps"))

    return {
        "nodes": nodes,
        "edges": edges,
        "boundary_voltages": {"vdd_bump": float(cfg["source_voltage"]), "gnd_bump": float(cfg["ground_voltage"])},
        "hypothesis": hypothesis,
        "family": int(family),
        "variant": int(variant),
        "layer_ids": list(LAYERS),
    }


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

    solved_unknowns = np.linalg.solve(a_mat, b_vec) if unknowns else np.array([], dtype=float)
    voltages = dict(boundary)
    voltages.update({node: float(solved_unknowns[index[node]]) for node in unknowns})

    net_out = {node: 0.0 for node in nodes}
    solved_edges = []
    for edge in graph["edges"]:
        current = (voltages[edge["a"]] - voltages[edge["b"]]) / float(edge["resistance"])
        net_out[edge["a"]] += current
        net_out[edge["b"]] -= current
        solved_edge = dict(edge)
        solved_edge["current"] = float(current)
        solved_edges.append(solved_edge)

    interior = [abs(net_out[node]) for node in nodes if node not in boundary]
    source_current = net_out["vdd_bump"]
    sink_current = net_out["gnd_bump"]
    closure_error = abs(source_current + sink_current) / max(abs(source_current), abs(sink_current), 1e-30)
    return {
        "voltages": voltages,
        "edges": solved_edges,
        "node_kcl_residuals": {node: float(value) for node, value in net_out.items()},
        "max_interior_kcl_residual": float(max(interior) if interior else 0.0),
        "source_current": float(source_current),
        "sink_current": float(sink_current),
        "current_closure_error": float(closure_error),
    }


def sensor_grid(grid_size: int, z: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(-0.20, 1.12, grid_size)
    ys = np.linspace(-0.48, 0.48, grid_size)
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
        field += MU0_OVER_4PI * float(edge["current"]) * cross / np.maximum(norm[..., None] ** 3, 1e-18)
    return field


def divb_residual(graph: dict[str, Any], solved: dict[str, Any], cfg: dict[str, Any]) -> float:
    grid_size = int(cfg["grid_size"])
    z0 = float(cfg["sensor_z"])
    dz = 0.025
    b0 = forward_biot_savart(graph, solved, grid_size, z0)
    bp = forward_biot_savart(graph, solved, grid_size, z0 + dz)
    bm = forward_biot_savart(graph, solved, grid_size, z0 - dz)
    xs = np.linspace(-0.20, 1.12, grid_size)
    ys = np.linspace(-0.48, 0.48, grid_size)
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


def split_role(family: int, variant: int, cfg: dict[str, Any]) -> str:
    if family == int(cfg["families"]) - 1:
        return "family_hidden"
    if variant == 0:
        return "calibration"
    if variant in {1, 2}:
        return "heldout"
    return "train"


def field_features(field: np.ndarray) -> list[float]:
    features: list[float] = []
    flat = field.reshape(-1, 3)
    for component in range(3):
        values = flat[:, component]
        features.extend(
            [
                float(np.mean(values)),
                float(np.std(values)),
                float(np.max(values)),
                float(np.min(values)),
                float(np.mean(np.abs(values))),
            ]
        )
    bz = field[:, :, 2]
    mid_x = bz.shape[1] // 2
    mid_y = bz.shape[0] // 2
    quadrants = [bz[:mid_y, :mid_x], bz[:mid_y, mid_x:], bz[mid_y:, :mid_x], bz[mid_y:, mid_x:]]
    features.extend(float(np.mean(q)) for q in quadrants)
    features.extend(float(np.std(q)) for q in quadrants)
    features.append(float(np.sqrt(np.mean(field**2))))
    features.append(float(np.linalg.norm(field[:, :, 2]) / max(np.linalg.norm(field), 1e-30)))
    return features


def graph_adjacency(graph: dict[str, Any]) -> dict[str, set[str]]:
    adjacency = {node: set() for node in graph["nodes"]}
    for edge in graph["edges"]:
        adjacency[edge["a"]].add(edge["b"])
        adjacency[edge["b"]].add(edge["a"])
    return adjacency


def connected_components(graph: dict[str, Any]) -> list[set[str]]:
    adjacency = graph_adjacency(graph)
    remaining = set(adjacency)
    components = []
    while remaining:
        root = remaining.pop()
        stack = [root]
        component = {root}
        while stack:
            node = stack.pop()
            for other in adjacency[node]:
                if other in remaining:
                    remaining.remove(other)
                    component.add(other)
                    stack.append(other)
        components.append(component)
    return components


def has_explicit_return_path(graph: dict[str, Any]) -> bool:
    return any(edge["role"] in {"return_grid", "distributed_load"} for edge in graph["edges"])


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
                        "split_role": split_role(family, variant, cfg),
                        "true_hypothesis": hypothesis,
                        "graph": graph,
                        "solved": solved,
                        "field": field,
                        "field_features": field_features(field),
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
    values = sorted(scores.values())
    return {
        "scores": scores,
        "predicted_hypothesis": predicted,
        "correct": predicted == case["true_hypothesis"],
        "best_residual": values[0],
        "score_margin": values[1] - values[0] if len(values) > 1 else 0.0,
    }


def summarize(cases: list[dict[str, Any]], cfg: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows = []
    for case in cases:
        scored = score_hypotheses(case, cfg)
        rows.append(
            {
                "case_id": case["case_id"],
                "family": case["family"],
                "variant": case["variant"],
                "split_role": case["split_role"],
                "true_hypothesis": case["true_hypothesis"],
                "predicted_hypothesis": scored["predicted_hypothesis"],
                "correct": bool(scored["correct"]),
                "best_residual": float(scored["best_residual"]),
                "score_margin": float(scored["score_margin"]),
            }
        )

    split_roles = {role: sum(1 for row in rows if row["split_role"] == role) for role in sorted({row["split_role"] for row in rows})}
    by_hypothesis = {hypothesis: sum(1 for row in rows if row["true_hypothesis"] == hypothesis) for hypothesis in HYPOTHESES}
    by_family = {str(family): sum(1 for row in rows if row["family"] == family) for family in sorted({row["family"] for row in rows})}
    heldout_rows = [row for row in rows if row["split_role"] == "heldout"]
    family_hidden_rows = [row for row in rows if row["split_role"] == "family_hidden"]
    heldout_accuracy = sum(row["correct"] for row in heldout_rows) / max(len(heldout_rows), 1)
    family_hidden_accuracy = sum(row["correct"] for row in family_hidden_rows) / max(len(family_hidden_rows), 1)
    heldout_coverage = {}
    for family in sorted({row["family"] for row in heldout_rows}):
        family_rows = [row for row in heldout_rows if row["family"] == family]
        heldout_coverage[str(family)] = {
            hypothesis: sum(1 for row in family_rows if row["true_hypothesis"] == hypothesis) for hypothesis in HYPOTHESES
        }

    max_kcl = max(case["solved"]["max_interior_kcl_residual"] for case in cases)
    max_closure = max(case["solved"]["current_closure_error"] for case in cases)
    max_divb = max(case["divb_residual"] for case in cases)
    node_counts = [len(case["graph"]["nodes"]) for case in cases]
    edge_counts = [len(case["graph"]["edges"]) for case in cases]
    all_connected = all(len(connected_components(case["graph"])) == 1 for case in cases)
    all_return_paths = all(has_explicit_return_path(case["graph"]) for case in cases)
    balanced = min(by_hypothesis.values()) == max(by_hypothesis.values())
    per_family_heldout_coverage = all(
        all(count >= int(cfg["min_family_heldout_rows_per_hypothesis"]) for count in counts.values())
        for counts in heldout_coverage.values()
    )

    gates = {
        "graph_connected": all_connected,
        "explicit_return_paths_present": all_return_paths,
        "kcl_residual_below_threshold": max_kcl <= float(cfg["kcl_residual_threshold"]),
        "current_closure_below_threshold": max_closure <= float(cfg["current_closure_threshold"]),
        "divB_proxy_below_threshold": max_divb <= float(cfg["divB_residual_threshold"]),
        "per_family_heldout_coverage": per_family_heldout_coverage,
        "h0_h1_h2_h3_balance": balanced,
        "heldout_hypothesis_accuracy_material": heldout_accuracy >= float(cfg["heldout_accuracy_threshold"]),
        "family_hidden_accuracy_material": family_hidden_accuracy >= float(cfg["family_hidden_accuracy_threshold"]),
    }
    gates["all_acceptance_gates_passed"] = all(gates.values())

    metrics = {
        "evidence_id": EVIDENCE_ID,
        "claim_id": CLAIM_ID,
        "status": "passed" if gates["all_acceptance_gates_passed"] else "failed",
        "generated_at": GENERATED_AT,
        "case_count": len(cases),
        "family_count": int(cfg["families"]),
        "layer_count": len(LAYERS),
        "node_count": {"min": int(min(node_counts)), "max": int(max(node_counts))},
        "edge_count": {"min": int(min(edge_counts)), "max": int(max(edge_counts))},
        "dataset": {
            "case_count": len(cases),
            "family_count": int(cfg["families"]),
            "layer_count": len(LAYERS),
            "by_hypothesis": by_hypothesis,
            "by_family": by_family,
            "by_split_role": split_roles,
        },
        "split_roles": split_roles,
        "kcl": {
            "max_residual": float(max_kcl),
            "threshold": float(cfg["kcl_residual_threshold"]),
        },
        "closure": {
            "max_error": float(max_closure),
            "threshold": float(cfg["current_closure_threshold"]),
        },
        "divB": {
            "max_proxy_residual": float(max_divb),
            "threshold": float(cfg["divB_residual_threshold"]),
        },
        "hypothesis": {
            "balance": by_hypothesis,
            "heldout_accuracy": float(heldout_accuracy),
            "family_hidden_accuracy": float(family_hidden_accuracy),
            "per_family_heldout_coverage": heldout_coverage,
        },
        "acceptance_gates": gates,
        "all_acceptance_gates_passed": gates["all_acceptance_gates_passed"],
        "cannot_claim": [
            "real chip PDN realism",
            "real CAD/Gerber/GDS validation",
            "external FEM/FastHenry validation",
            "real QDM/NV validation",
            "inductive or frequency-dependent PDN behavior",
        ],
    }
    return metrics, rows


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")


def md_float(value: float) -> str:
    return f"{value:.3e}" if abs(value) < 1e-3 else f"{value:.3f}"


def write_tables(outputs: Path, metrics: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Chip-Like PDN Metrics Table\n\n",
        "| Metric | Value | Gate |\n",
        "|---|---:|---|\n",
        f"| case count | {metrics['case_count']} | - |\n",
        f"| family count | {metrics['family_count']} | - |\n",
        f"| layer count | {metrics['layer_count']} | - |\n",
        f"| node count range | {metrics['node_count']['min']} to {metrics['node_count']['max']} | - |\n",
        f"| edge count range | {metrics['edge_count']['min']} to {metrics['edge_count']['max']} | - |\n",
        f"| max KCL residual | {md_float(metrics['kcl']['max_residual'])} | {metrics['acceptance_gates']['kcl_residual_below_threshold']} |\n",
        f"| max closure error | {md_float(metrics['closure']['max_error'])} | {metrics['acceptance_gates']['current_closure_below_threshold']} |\n",
        f"| max divB proxy residual | {md_float(metrics['divB']['max_proxy_residual'])} | {metrics['acceptance_gates']['divB_proxy_below_threshold']} |\n",
        f"| heldout accuracy | {metrics['hypothesis']['heldout_accuracy']:.3f} | {metrics['acceptance_gates']['heldout_hypothesis_accuracy_material']} |\n",
        f"| family-hidden accuracy | {metrics['hypothesis']['family_hidden_accuracy']:.3f} | {metrics['acceptance_gates']['family_hidden_accuracy_material']} |\n",
    ]
    (outputs / "CHIP_LIKE_PDN_METRICS_TABLE.md").write_text("".join(lines), encoding="utf-8")

    case_lines = [
        "# Chip-Like PDN Case Table\n\n",
        "| Case | Family | Variant | Split | True | Predicted | Correct | Residual | Margin |\n",
        "|---|---:|---:|---|---|---|---:|---:|---:|\n",
    ]
    for row in rows[:40]:
        case_lines.append(
            f"| {row['case_id']} | {row['family']} | {row['variant']} | {row['split_role']} | "
            f"{row['true_hypothesis']} | {row['predicted_hypothesis']} | {row['correct']} | "
            f"{md_float(row['best_residual'])} | {md_float(row['score_margin'])} |\n"
        )
    case_lines.append("\nRows are generated-domain chip-like PDN hypotheses, not real layout validation.\n")
    (outputs / "CASE_TABLE.md").write_text("".join(case_lines), encoding="utf-8")

    field_manifest = {
        "field_array_file": "data/e11_fields.npz",
        "dataset_file": "data/e11_dataset.json",
        "field_key": "fields",
        "shape": [metrics["case_count"], "grid_size", "grid_size", 3],
        "units": "centerline Biot-Savart proxy units",
        "tracked": False,
        "reason_untracked": "large generated array artifact; reproducible from src/run_all.py and config",
    }
    write_json(outputs / "field_arrays_manifest.json", field_manifest)

    report = f"""# RUN_REPORT - E11 Chip-Like PDN Distribution

Claim: `{CLAIM_ID}`.

This run generated a four-layer artificial micro-PDN with top straps,
intermediate mesh, lower return grid, via stacks, distributed loads, VDD/GND
ports, edge resistance, solved KCL currents, current closure, and `Bxyz`
centerline Biot-Savart fields.

## Metrics

{(outputs / "CHIP_LIKE_PDN_METRICS_TABLE.md").read_text(encoding="utf-8")}

## Boundary

This is generated-domain evidence. It does not validate real chip layouts,
CAD/Gerber/GDS imports, external FEM/FastHenry solves, frequency-dependent PDN
effects, or real QDM/NV measurements.
"""
    (outputs / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def serializable_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    serialized = []
    for case in cases:
        serialized.append(
            {
                "case_id": case["case_id"],
                "family": int(case["family"]),
                "variant": int(case["variant"]),
                "split_role": case["split_role"],
                "true_hypothesis": case["true_hypothesis"],
                "graph": case["graph"],
                "solved": case["solved"],
                "field": np.asarray(case["field"]).round(12).tolist(),
                "field_features": [float(value) for value in case["field_features"]],
                "divb_residual": float(case["divb_residual"]),
            }
        )
    return serialized


def run_experiment(cfg: dict[str, Any], outputs: Path, data: Path) -> dict[str, Any]:
    outputs.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    cases = generate_cases(cfg)
    metrics, rows = summarize(cases, cfg)
    write_tables(outputs, metrics, rows)
    write_json(outputs / "metrics.json", metrics)
    write_json(outputs / "case_table.json", rows)
    write_json(data / "e11_dataset.json", serializable_cases(cases))
    np.savez_compressed(data / "e11_fields.npz", fields=np.stack([case["field"] for case in cases], axis=0))
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Run E11 generated chip-like PDN distribution evidence.")
    parser.add_argument("--config", type=Path, default=Path("configs/default.json"))
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    args = parser.parse_args()
    cfg = load_config(args.config)
    metrics = run_experiment(cfg, args.out, args.data)
    print(
        json.dumps(
            {
                "evidence_id": EVIDENCE_ID,
                "metrics_path": str(args.out / "metrics.json"),
                "passed": metrics["all_acceptance_gates_passed"],
            },
            sort_keys=True,
        )
    )
    return 0 if metrics["all_acceptance_gates_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
