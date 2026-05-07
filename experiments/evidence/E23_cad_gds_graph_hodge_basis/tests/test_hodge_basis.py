"""Test Hodge basis with SVD nullspace projection."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from layout_schema import load_layout, parse_layout
from graph_builder import build_graph
from incidence import build_incidence_matrix, build_source_vector
from hodge_basis import (
    assemble_hodge_basis, validate_basis,
    build_port_basis, build_loop_basis,
    build_svd_nullspace, project_via_modes_svd,
)


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


def test_svd_nullspace_built():
    graph, D, q, no, eo = _setup_simple()
    cfg = _default_config()
    result = assemble_hodge_basis(graph, eo, D, q, cfg)
    assert "svd_nullspace" in result
    svd = result["svd_nullspace"]
    assert svd["projection_method"] == "SVD"
    assert svd["nullspace_dim"] >= 0
    assert "via_retained_energy" in svd
    assert "return_retained_energy" in svd
    assert "via_collapsed_count" in svd
    assert "return_collapsed_count" in svd


def test_svd_nullspace_satisfies_DN_zero():
    graph, D, q, no, eo = _setup_simple()
    from hodge_basis import _interior_mask
    interior = _interior_mask(D, q)
    N, ndim, sv = build_svd_nullspace(D, interior)
    if ndim > 0:
        D_int = D[interior, :]
        residual = np.max(np.abs(D_int @ N))
        assert residual < 1e-6


def test_svd_projected_blocks_kcl():
    graph, D, q, no, eo = _setup_simple()
    cfg = _default_config()
    result = assemble_hodge_basis(graph, eo, D, q, cfg)
    v = validate_basis(result, D, q, graph, cfg)
    assert "kcl_residual_svd_projected_blocks" in v
    assert "svd_projected_blocks_kcl_pass" in v
    assert v["svd_projected_blocks_kcl_pass"] is True


def test_svd_via_projection():
    graph, D, q, no, eo = _setup_simple()
    from hodge_basis import _interior_mask
    interior = _interior_mask(D, q)
    N, ndim, sv = build_svd_nullspace(D, interior)
    # Create a raw one-hot via vector
    H_raw = np.zeros((D.shape[1], 1))
    for j, eid in enumerate(eo):
        if graph["edges"][eid]["kind"] == "via_edge":
            H_raw[j, 0] = 1.0
            break
    H_proj, res, energy, collapsed = project_via_modes_svd(H_raw, N, ndim)
    assert H_proj.shape == H_raw.shape
    assert len(res) == 1
    assert len(energy) == 1
    # SVD projected should satisfy D_int @ v_proj = 0
    if ndim > 0 and H_proj.shape[1] > 0:
        D_int = D[interior, :]
        r = np.max(np.abs(D_int @ H_proj[:, 0]))
        assert r < 1e-6
