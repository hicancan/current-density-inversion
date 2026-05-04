from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_all import (
    HYPOTHESES,
    build_graph,
    connected_components,
    count_return_candidates,
    count_via_candidates,
    generate_hypothesis_candidates,
    graph_is_connected,
    graph_summary,
    load_layout,
    parse_layout,
    run_one,
    validate_layout,
)


def _cfg() -> dict:
    return {"seed": 20260504}


def test_simple_two_layer_validates() -> None:
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    errors = validate_layout(layout)
    assert not errors, f"schema errors: {errors}"


def test_four_layer_validates() -> None:
    layout = load_layout(ROOT / "examples" / "four_layer_pdn_like_layout.json")
    errors = validate_layout(layout)
    assert not errors, f"schema errors: {errors}"


def test_no_via_hard_negative_validates() -> None:
    layout = load_layout(ROOT / "examples" / "no_via_hard_negative_layout.json")
    errors = validate_layout(layout)
    assert not errors, f"schema errors: {errors}"


def test_return_bottleneck_validates() -> None:
    layout = load_layout(ROOT / "examples" / "return_bottleneck_layout.json")
    errors = validate_layout(layout)
    assert not errors, f"schema errors: {errors}"


def test_simple_two_layer_graph_build() -> None:
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    assert len(graph["nodes"]) > 0
    assert len(graph["edges"]) > 0


def test_simple_two_layer_is_connected() -> None:
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    assert graph_is_connected(graph)


def test_four_layer_has_via_candidates() -> None:
    layout = load_layout(ROOT / "examples" / "four_layer_pdn_like_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    vias = count_via_candidates(graph)
    assert vias > 0


def test_no_via_layout_has_zero_vias() -> None:
    layout = load_layout(ROOT / "examples" / "no_via_hard_negative_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    vias = count_via_candidates(graph)
    assert vias == 0


def test_return_candidates_extracted() -> None:
    layout = load_layout(ROOT / "examples" / "return_bottleneck_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    rc = count_return_candidates(graph)
    assert rc > 0


def test_hypothesis_candidates_generated_for_simple() -> None:
    result = run_one(ROOT / "examples" / "simple_two_layer_layout.json", _cfg())
    candidates = result["hypothesis_candidates"]
    assert "H0_nominal" in candidates
    assert "H1_via_defect_or_extra_via" in candidates
    assert "H2_return_bottleneck" in candidates
    assert "H3_bend_width_artifact" in candidates


def test_hypothesis_candidates_generated_for_no_via() -> None:
    result = run_one(ROOT / "examples" / "no_via_hard_negative_layout.json", _cfg())
    candidates = result["hypothesis_candidates"]
    assert len(candidates) >= 4
    assert "H0_nominal" in candidates


def test_h1_perturbs_via_count() -> None:
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    candidates = generate_hypothesis_candidates(graph)
    h0 = candidates["H0_nominal"]
    h1 = candidates["H1_via_defect_or_extra_via"]
    assert count_via_candidates(h1) != count_via_candidates(h0)


def test_h2_modifies_return_path() -> None:
    layout = load_layout(ROOT / "examples" / "return_bottleneck_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    candidates = generate_hypothesis_candidates(graph)
    h2 = candidates["H2_return_bottleneck"]
    assert count_return_candidates(h2) == count_return_candidates(graph)


def test_h3_modifies_trace() -> None:
    layout = load_layout(ROOT / "examples" / "four_layer_pdn_like_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    candidates = generate_hypothesis_candidates(graph)
    h3 = candidates["H3_bend_width_artifact"]
    trace_edges_h3 = [e for e in h3["edges"].values() if e["kind"] == "trace"]
    trace_edges_original = [e for e in graph["edges"].values() if e["kind"] == "trace"]
    widths_h3 = [e.get("width_um", 0) for e in trace_edges_h3]
    widths_orig = [e.get("width_um", 0) for e in trace_edges_original]
    assert widths_h3[0] < widths_orig[0]


def test_layer_preservation() -> None:
    layout = load_layout(ROOT / "examples" / "four_layer_pdn_like_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    summary = graph_summary(graph)
    assert summary["layer_count"] == 4
    assert "TOP" in summary["layers_found"]
    assert "BOT" in summary["layers_found"]


def test_layer_preservation_simple() -> None:
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    summary = graph_summary(graph)
    assert summary["layer_count"] == 2


def test_graph_structure_has_required_node_kinds() -> None:
    for example_name in ["simple_two_layer_layout", "four_layer_pdn_like_layout", "no_via_hard_negative_layout", "return_bottleneck_layout"]:
        result = run_one(ROOT / "examples" / f"{example_name}.json", _cfg())
        kinds = set(result["summary"]["node_kinds"].keys())
        assert "port" in kinds, f"{example_name} missing port nodes"
        assert "layer" in kinds, f"{example_name} missing layer nodes"


def test_kcl_export_available() -> None:
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    from run_all import compute_kcl_residual
    kcl = compute_kcl_residual(graph)
    assert "max_kcl_residual" in kcl
    assert kcl["max_kcl_residual"] >= 0


def test_acceptance_gates_all_true() -> None:
    from run_all import run_experiment
    report = run_experiment(_cfg())
    assert report["all_acceptance_gates_passed"]
    assert all(report["acceptance_gates"].values())
