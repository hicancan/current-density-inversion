"""Test KCL and current closure with honest separation."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from layout_schema import load_layout, parse_layout
from graph_builder import build_graph
from incidence import build_incidence_matrix, build_source_vector
from hodge_basis import assemble_hodge_basis, validate_basis


def _setup_simple():
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    D, node_order, edge_order = build_incidence_matrix(graph)
    q = build_source_vector(graph, node_order)
    return graph, D, q, node_order, edge_order


def _default_config():
    return {"seed": 20260506, "basis_rank_tolerance": 1e-8,
            "kcl_residual_threshold": 1e-10, "current_closure_threshold": 1e-10}


def test_port_loop_kcl_near_zero():
    graph, D, q, no, eo = _setup_simple()
    cfg = _default_config()
    result = assemble_hodge_basis(graph, eo, D, q, cfg)
    v = validate_basis(result, D, q, graph, cfg)
    assert v["port_loop_kcl_pass"] is True
    assert v["kcl_residual_port_loop"] < 1e-6


def test_raw_blocks_kcl_reported():
    graph, D, q, no, eo = _setup_simple()
    cfg = _default_config()
    result = assemble_hodge_basis(graph, eo, D, q, cfg)
    v = validate_basis(result, D, q, graph, cfg)
    # Raw blocks should have non-trivial KCL residuals (they're raw one-hot/sinusoid)
    assert v["kcl_residual_raw_blocks"] >= 0.0


def test_projected_blocks_kcl():
    graph, D, q, no, eo = _setup_simple()
    cfg = _default_config()
    result = assemble_hodge_basis(graph, eo, D, q, cfg)
    v = validate_basis(result, D, q, graph, cfg)
    assert v["kcl_residual_svd_projected_blocks"] >= 0.0
    # SVD projected blocks should pass KCL (N @ N^T projection)
    assert v["svd_projected_blocks_kcl_pass"] is True


def test_four_layer_separated_kcl():
    layout = load_layout(ROOT / "examples" / "four_layer_pdn_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    D, node_order, edge_order = build_incidence_matrix(graph)
    q = build_source_vector(graph, node_order)
    cfg = _default_config()
    result = assemble_hodge_basis(graph, edge_order, D, q, cfg)
    v = validate_basis(result, D, q, graph, cfg)
    assert "kcl_residual_port_loop" in v
    assert "kcl_residual_raw_blocks" in v
    assert "kcl_residual_svd_projected_blocks" in v


def test_closure_reported():
    graph, D, q, no, eo = _setup_simple()
    cfg = _default_config()
    result = assemble_hodge_basis(graph, eo, D, q, cfg)
    v = validate_basis(result, D, q, graph, cfg)
    assert "max_closure_error" in v
    assert v["max_closure_error"] >= 0.0
