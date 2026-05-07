"""Incidence matrix construction for E23 Graph-Hodge basis."""
from __future__ import annotations

from typing import Any

import numpy as np


def build_incidence_matrix(
    graph: dict[str, Any],
    node_order: list[str] | None = None,
    edge_order: list[str] | None = None,
) -> tuple[np.ndarray, list[str], list[str]]:
    """Build the node-edge incidence matrix D.

    D has shape (n_nodes, n_edges). D[i, j] = +1 if edge j leaves node i,
    -1 if edge j enters node i.

    Returns (D, node_order, edge_order).
    """
    if node_order is None:
        node_order = sorted(graph["nodes"].keys())
    if edge_order is None:
        edge_order = sorted(graph["edges"].keys())

    node_index = {nid: i for i, nid in enumerate(node_order)}

    n = len(node_order)
    m = len(edge_order)
    D = np.zeros((n, m), dtype=float)

    for j, eid in enumerate(edge_order):
        ed = graph["edges"][eid]
        src = ed["src"]
        dst = ed["dst"]
        if src in node_index:
            D[node_index[src], j] = 1.0
        if dst in node_index:
            D[node_index[dst], j] = -1.0

    return D, node_order, edge_order


def build_source_vector(
    graph: dict[str, Any],
    node_order: list[str],
    source_current: float = 1.0,
) -> np.ndarray:
    """Build the source/sink injection vector q for KCL.

    D i = q where q has +source_current at source ports and -source_current
    at sink ports, distributed among all source/sink ports.
    """
    node_index = {nid: i for i, nid in enumerate(node_order)}
    n = len(node_order)
    q = np.zeros(n, dtype=float)

    source_ports = []
    sink_ports = []
    for nid, nd in graph["nodes"].items():
        if nd["kind"] == "port":
            if nd.get("role") == "source":
                source_ports.append(nid)
            elif nd.get("role") == "sink":
                sink_ports.append(nid)

    n_src = max(len(source_ports), 1)
    n_snk = max(len(sink_ports), 1)

    for sp in source_ports:
        q[node_index[sp]] = source_current / n_src

    for sp in sink_ports:
        q[node_index[sp]] = -source_current / n_snk

    return q


def check_kcl_residual(
    D: np.ndarray, i: np.ndarray, q: np.ndarray | None = None
) -> float:
    """Compute max absolute KCL residual: max|D i - q|."""
    residual = D @ i
    if q is not None:
        residual = residual - q
    return float(np.max(np.abs(residual)))


def check_current_closure(
    D: np.ndarray, i: np.ndarray, q: np.ndarray
) -> float:
    """Compute current closure error: sum of D i vs sum of q."""
    di_sum = float(np.sum(D @ i))
    q_sum = float(np.sum(q))
    if abs(q_sum) < 1e-15:
        return abs(di_sum)
    return abs(di_sum - q_sum) / abs(q_sum)
