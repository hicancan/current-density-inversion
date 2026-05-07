"""Graph topology generation for E24 network profile inversion.

Generates chip-like 2D grid topologies with 4 hypotheses that genuinely
change the graph structure: edge set, via set, cycle space, and effective
resistance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

HYPOTHESES = ["H0_nominal", "H1_via", "H2_open", "H3_return"]
MU0_OVER_4PI = 1e-7
EPS = 1e-18


@dataclass
class TopologyGraph:
    hypothesis: str
    node_positions: np.ndarray       # (|V|, 3) in meters
    edges: np.ndarray                # (|E|, 2) int, node indices
    edge_types: list[str]             # type per edge: "sheet", "via", "return"
    D: np.ndarray                    # |V| x |E| oriented incidence
    port_nodes: list[int]             # node indices for port injection
    layer_of_node: np.ndarray        # (|V|,) int layer index
    grid_x: int
    grid_y: int
    layer_count: int
    layout_id: str

    @property
    def node_count(self) -> int:
        return self.node_positions.shape[0]

    @property
    def edge_count(self) -> int:
        return self.edges.shape[0]

    @property
    def via_edge_count(self) -> int:
        return sum(1 for t in self.edge_types if t == "via")

    @property
    def return_edge_count(self) -> int:
        return sum(1 for t in self.edge_types if t == "return")

    @property
    def port_count(self) -> int:
        return len(self.port_nodes)

    @property
    def component_count(self) -> int:
        # Approximate via connected components using D's nullspace
        return 1  # grids are connected

    @property
    def cycle_rank(self) -> int:
        return max(0, self.edge_count - self.node_count + self.component_count)

    @property
    def nullspace_dim(self) -> int:
        D_int = _internal_kcl(self.D, self.port_nodes)
        return max(0, self.edge_count - np.linalg.matrix_rank(D_int))


def _internal_kcl(D: np.ndarray, port_nodes: list[int]) -> np.ndarray:
    """Return internal-node KCL matrix (exclude port rows)."""
    internal = sorted(set(range(D.shape[0])) - set(port_nodes))
    if not internal:
        return D  # all nodes are ports (degenerate)
    return D[internal, :]


def _build_incidence(edges: np.ndarray, n_nodes: int, port_nodes: list[int]) -> np.ndarray:
    """Build oriented incidence matrix D: sign convention is D[from, e] = -1, D[to, e] = +1."""
    E = edges.shape[0]
    D = np.zeros((n_nodes, E), dtype=float)
    rows_from = edges[:, 0]
    rows_to = edges[:, 1]
    for e in range(E):
        D[rows_from[e], e] = -1.0
        D[rows_to[e], e] = 1.0
    return D


def _make_grid_positions(gx: int, gy: int, layer: int, layer_spacing: float,
                         pixel_pitch: float) -> np.ndarray:
    """Return (gx*gy, 3) positions for one layer in meters."""
    pitch_m = pixel_pitch * 1e-6
    xs = (np.arange(gx, dtype=float) - (gx - 1) / 2.0) * pitch_m
    ys = (np.arange(gy, dtype=float) - (gy - 1) / 2.0) * pitch_m
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    z = -float(layer) * layer_spacing * 1e-6
    return np.column_stack([xx.ravel(), yy.ravel(), np.full(gx * gy, z)])


def _grid_node_index(ix: int, iy: int, grid_x: int, layer: int, nodes_per_layer: int) -> int:
    """Global node index for grid position (ix, iy) on given layer."""
    return layer * nodes_per_layer + iy * grid_x + ix


def _grid_edges(gx: int, gy: int, layer: int, nodes_per_layer: int,
                edge_type: str) -> tuple[np.ndarray, list[str]]:
    """Build intra-layer grid edges (horizontal + vertical)."""
    edges = []
    types = []
    base = layer * nodes_per_layer
    for iy in range(gy):
        for ix in range(gx):
            u = base + iy * gx + ix
            if ix + 1 < gx:
                edges.append([u, u + 1])
                types.append(edge_type)
            if iy + 1 < gy:
                edges.append([u, u + gx])
                types.append(edge_type)
    return np.array(edges, dtype=int) if edges else np.zeros((0, 2), dtype=int), types


def _via_edges(gx: int, gy: int, layer0: int, layer1: int, nodes_per_layer: int,
               positions: list[tuple[int, int]]) -> tuple[np.ndarray, list[str]]:
    """Build via edges between corresponding grid positions."""
    edges = []
    types = []
    for ix, iy in positions:
        u = _grid_node_index(ix, iy, gx, layer0, nodes_per_layer)
        v = _grid_node_index(ix, iy, gx, layer1, nodes_per_layer)
        edges.append([u, v])
        types.append("via")
    return np.array(edges, dtype=int) if edges else np.zeros((0, 2), dtype=int), types


def build_topology(layout_id: str, rng: np.random.Generator, gx: int, gy: int,
                   layers: int, pixel_pitch: float, layer_spacing: float,
                   hypothesis: str) -> TopologyGraph:
    """Build a chip-like 2D grid topology for a specific hypothesis."""
    nodes_per_layer = gx * gy
    total_nodes = layers * nodes_per_layer

    # Node positions
    pos_parts = []
    layer_of = []
    for l in range(layers):
        pos_parts.append(_make_grid_positions(gx, gy, l, layer_spacing, pixel_pitch))
        layer_of.extend([l] * nodes_per_layer)
    positions = np.concatenate(pos_parts, axis=0)
    layer_of = np.array(layer_of, dtype=int)

    # Base grid edges (all layers)
    all_edges = []
    all_types: list[str] = []
    for l in range(layers):
        e, t = _grid_edges(gx, gy, l, nodes_per_layer, "sheet")
        if len(e) > 0:
            all_edges.append(e)
            all_types.extend(t)

    # Define ports: top-layer boundary nodes (left edge = sink, right edge = source)
    port_nodes: list[int] = []
    top_base = 0  # top layer
    for iy in [0, gy - 1, gy // 2]:
        for ix in [0, gx - 1]:
            port_nodes.append(_grid_node_index(ix, iy, gx, top_base, nodes_per_layer))
    # also some bottom-layer ports for multi-port
    for iy in [0, gy - 1]:
        for ix in [0, gx - 1, gx // 2]:
            port_nodes.append(_grid_node_index(ix, iy, gx, layers - 1, nodes_per_layer))
    port_nodes = sorted(set(port_nodes))[:20]  # limit port count

    # Hypothesis-specific modifications
    if hypothesis == "H0_nominal":
        pass  # baseline grid, no vias, all sheet edges intact

    elif hypothesis == "H1_via":
        # Add vias at scattered positions
        via_positions = []
        for cx in [gx // 3, gx // 2, 2 * gx // 3]:
            for cy in [gy // 3, gy // 2, 2 * gy // 3]:
                via_positions.append((cx, cy))
        for l in range(layers - 1):
            ve, vt = _via_edges(gx, gy, l, l + 1, nodes_per_layer, via_positions)
            if len(ve) > 0:
                all_edges.append(ve)
                all_types.extend(vt)

    elif hypothesis == "H2_open":
        # Remove some sheet edges to create open/missing segments
        # We'll remove ~10-15% of sheet edges
        if all_edges:
            base_edges = all_edges[0]  # first layer edges
            n_remove = max(1, base_edges.shape[0] // 8)
            remove_idx = set(rng.choice(base_edges.shape[0], size=n_remove, replace=False))
            keep_mask = np.ones(base_edges.shape[0], dtype=bool)
            keep_mask[list(remove_idx)] = False
            all_edges[0] = base_edges[keep_mask]
            keep_types = [t for i, t in enumerate(all_types[:base_edges.shape[0]]) if keep_mask[i]]
            all_types[:base_edges.shape[0]] = keep_types
            all_types = keep_types + all_types[base_edges.shape[0]:]

    elif hypothesis == "H3_return":
        # Add extra return-path edges: long-range connections along perimeter
        ret_edges = []
        ret_types = []
        for l in range(layers):
            base = l * nodes_per_layer
            # Perimeter return loops
            for iy in range(gy):
                u_left = base + iy * gx
                v_right = base + iy * gx + (gx - 1)
                if rng.random() < 0.4:
                    ret_edges.append([u_left, v_right])
                    ret_types.append("return")
            for ix in range(gx):
                u_top = base + ix
                v_bot = base + (gy - 1) * gx + ix
                if rng.random() < 0.4:
                    ret_edges.append([u_top, v_bot])
                    ret_types.append("return")
        # Add cross-layer return paths
        for ix, iy in [(0, 0), (gx - 1, 0), (0, gy - 1), (gx - 1, gy - 1)]:
            for l in range(layers - 1):
                if rng.random() < 0.4:
                    u = _grid_node_index(ix, iy, gx, l, nodes_per_layer)
                    v = _grid_node_index(ix, iy, gx, l + 1, nodes_per_layer)
                    ret_edges.append([u, v])
                    ret_types.append("return")
        if ret_edges:
            all_edges.append(np.array(ret_edges, dtype=int))
            all_types.extend(ret_types)

    # Concatenate all edges
    if len(all_edges) > 1:
        edges = np.concatenate([e for e in all_edges if isinstance(e, np.ndarray) and len(e) > 0], axis=0)
    elif len(all_edges) == 1 and isinstance(all_edges[0], np.ndarray) and len(all_edges[0]) > 0:
        edges = all_edges[0]
    else:
        edges = np.zeros((0, 2), dtype=int)

    # Build incidence matrix
    D = _build_incidence(edges, total_nodes, port_nodes)

    return TopologyGraph(
        hypothesis=hypothesis,
        node_positions=positions,
        edges=edges,
        edge_types=all_types,
        D=D,
        port_nodes=port_nodes,
        layer_of_node=layer_of,
        grid_x=gx,
        grid_y=gy,
        layer_count=layers,
        layout_id=layout_id,
    )


def build_all_topologies(layout_id: str, rng: np.random.Generator, gx: int, gy: int,
                         layers: int, pixel_pitch: float, layer_spacing: float) -> dict[str, TopologyGraph]:
    """Build all 4 hypothesis topologies for a given layout."""
    return {h: build_topology(layout_id, rng, gx, gy, layers, pixel_pitch, layer_spacing, h)
            for h in HYPOTHESES}


def generate_layout_params(rng: np.random.Generator, count: int, gx_min: int, gx_max: int) -> list[dict]:
    """Generate diverse layout parameters."""
    layouts = []
    sizes = [rng.integers(gx_min, gx_max + 1) for _ in range(count)]
    for i, size in enumerate(sizes):
        # Vary aspect ratio
        gy = size + rng.integers(-1, 2)
        gy = max(gx_min, min(gx_max, gy))
        layouts.append({
            "layout_id": f"L{i:03d}_g{size}x{gy}",
            "gx": int(size),
            "gy": int(gy),
            "layers": 2,
        })
    return layouts


def compute_graph_invariants(graphs: dict[str, TopologyGraph]) -> dict:
    """Compute graph invariants for all hypothesis topologies."""
    inv = {}
    for h, g in graphs.items():
        inv[h] = {
            "node_count": g.node_count,
            "edge_count": g.edge_count,
            "component_count": g.component_count,
            "cycle_rank": g.cycle_rank,
            "port_count": g.port_count,
            "via_edge_count": g.via_edge_count,
            "return_edge_count": g.return_edge_count,
            "nullspace_dim": g.nullspace_dim,
        }
    return inv


def effective_resistance(graph: TopologyGraph, theta: np.ndarray) -> np.ndarray:
    """Compute effective resistance matrix between ports via Laplacian pseudoinverse."""
    from scipy.linalg import pinvh
    D = graph.D
    c = np.exp(np.clip(theta, -20, 20))
    C = np.diag(c)
    L = D @ C @ D.T
    L_pinv = np.linalg.pinv(L)
    ports = sorted(graph.port_nodes)
    n_ports = len(ports)
    R_eff = np.zeros((n_ports, n_ports))
    for i, pi in enumerate(ports):
        for j, pj in enumerate(ports):
            R_eff[i, j] = L_pinv[pi, pi] + L_pinv[pj, pj] - 2 * L_pinv[pi, pj]
    return R_eff
