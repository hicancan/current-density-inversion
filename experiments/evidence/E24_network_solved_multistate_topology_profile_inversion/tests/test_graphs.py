"""Test graph generation and topology invariants."""

import sys
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from graphs import (
    HYPOTHESES, build_all_topologies, generate_layout_params,
    compute_graph_invariants,
)


def test_hypothesis_list():
    assert len(HYPOTHESES) >= 4
    assert "H0_nominal" in HYPOTHESES
    assert "H1_via" in HYPOTHESES
    assert "H2_open" in HYPOTHESES
    assert "H3_return" in HYPOTHESES


def test_build_topology():
    rng = np.random.default_rng(42)
    graphs = build_all_topologies("test_L0", rng, 6, 6, 2, 1.0, 1.2)
    assert len(graphs) == 4
    for h, g in graphs.items():
        assert g.node_count > 0
        assert g.edge_count > 0
        assert g.D.shape == (g.node_count, g.edge_count)
        assert g.port_count > 0


def test_topology_differences():
    """Verify that hypotheses produce different graph structures."""
    rng = np.random.default_rng(42)
    graphs = build_all_topologies("test_diff", rng, 6, 6, 2, 1.0, 1.2)
    inv = compute_graph_invariants(graphs)

    edge_counts = set(v["edge_count"] for v in inv.values())
    assert len(edge_counts) >= 2, f"All hypotheses have same edge count: {edge_counts}"

    cycle_ranks = set(v["cycle_rank"] for v in inv.values())
    assert len(cycle_ranks) >= 2, f"All hypotheses have same cycle rank: {cycle_ranks}"


def test_layout_generation():
    rng = np.random.default_rng(42)
    layouts = generate_layout_params(rng, 24, 5, 10)
    assert len(layouts) == 24
    for lp in layouts:
        assert "layout_id" in lp
        assert lp["gx"] >= 5
        assert lp["gy"] >= 4


def test_graph_invariants():
    rng = np.random.default_rng(42)
    g0 = list(build_all_topologies("test_inv", rng, 6, 6, 2, 1.0, 1.2).values())[0]
    inv = compute_graph_invariants({"test": g0})
    d = inv["test"]
    assert d["node_count"] > 0
    assert d["edge_count"] > 0
    assert d["cycle_rank"] >= 0
    assert d["port_count"] > 0
    assert d["nullspace_dim"] >= 0
