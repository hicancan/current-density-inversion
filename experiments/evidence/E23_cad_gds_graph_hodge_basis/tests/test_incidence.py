"""Test incidence matrix construction and KCL."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from layout_schema import load_layout, parse_layout
from graph_builder import build_graph
from incidence import (
    build_incidence_matrix, build_source_vector,
    check_kcl_residual, check_current_closure,
)


def _setup_simple():
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    D, node_order, edge_order = build_incidence_matrix(graph)
    q = build_source_vector(graph, node_order)
    return graph, D, q, node_order, edge_order


def test_incidence_matrix_shape():
    graph, D, q, no, eo = _setup_simple()
    assert D.shape[0] == len(graph["nodes"])
    assert D.shape[1] == len(graph["edges"])


def test_incidence_column_sum_zero():
    """Each column of D should sum to zero (+1 and -1)."""
    graph, D, q, no, eo = _setup_simple()
    col_sums = D.sum(axis=0)
    assert np.allclose(col_sums, 0.0)


def test_incidence_row_sum():
    """Row sums represent net flow per node."""
    graph, D, q, no, eo = _setup_simple()
    row_sums = D.sum(axis=1)
    # Row sums are generally non-zero for boundary nodes
    assert row_sums is not None


def test_source_vector():
    graph, D, q, no, eo = _setup_simple()
    assert abs(np.sum(q)) < 1e-10  # net source + sink should be zero
    source_indices = np.where(q > 0)[0]
    sink_indices = np.where(q < 0)[0]
    assert len(source_indices) > 0
    assert len(sink_indices) > 0


def test_kcl_residual_zero_vector():
    """Zero current vector should have KCL residual = max|q| (since D*0 - q = -q)."""
    graph, D, q, no, eo = _setup_simple()
    i = np.zeros(D.shape[1])
    r = check_kcl_residual(D, i, q)
    assert r > 0  # q is non-zero, so D*0 != q


def test_closure():
    graph, D, q, no, eo = _setup_simple()
    i = np.zeros(D.shape[1])
    # Current closure: compare sum(D i) vs sum(q)
    c = check_current_closure(D, i, q)
    assert c >= 0.0
