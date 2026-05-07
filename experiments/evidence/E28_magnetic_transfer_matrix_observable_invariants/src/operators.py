"""Forward operators and graph incidence matrix for E28.

Extends E19_2's Biot-Savart operator with graph incidence matrix construction
for the transfer-matrix pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

MU0_OVER_4PI = 1e-7
EPS = 1e-18


@dataclass(frozen=True)
class OperatorBundle:
    A: np.ndarray
    D: np.ndarray
    positions: np.ndarray
    obs_positions: np.ndarray
    index: dict
    column_norms: np.ndarray
    node_count: int
    edge_count: int
    heights: tuple[float, ...] | None = None


@dataclass
class PortExcitation:
    B: np.ndarray
    port_nodes: list[int]
    port_labels: list[str]
    n_states: int


def _grid_positions(n: int, pitch_um: float) -> np.ndarray:
    coords = (np.arange(n, dtype=float) - (n - 1) / 2.0) * pitch_um * 1e-6
    xx, yy = np.meshgrid(coords, coords, indexing="xy")
    return np.stack([xx.ravel(), yy.ravel()], axis=1)


def _biot_savart_columns(
    obs: np.ndarray,
    src: np.ndarray,
    direction: np.ndarray,
    length_m: float,
) -> np.ndarray:
    r = obs - src[None, :]
    norm = np.linalg.norm(r, axis=1)
    cross = np.cross(direction[None, :] * length_m, r)
    b = MU0_OVER_4PI * cross / (norm[:, None] ** 3 + EPS)
    return b.reshape(-1)


def build_operator_and_graph(
    n: int,
    layers: int,
    pitch_um: float,
    dz_um: float,
    sensor_h_um: float,
) -> OperatorBundle:
    """Build Biot-Savart operator A and graph incidence matrix D.

    The graph model:
    - Nodes: L * n^2 grid cell centers (indexed layer, row, col)
    - Edges: Jx (between cells horizontally), Jy (between cells vertically),
      Vz (between layers at same position)

    D maps edge currents to node KCL constraints.
    D[node, edge] = -1 if edge leaves node, +1 if edge enters node.
    """
    pitch_m = pitch_um * 1e-6
    dz_m = dz_um * 1e-6
    sensor_m = sensor_h_um * 1e-6

    xy = _grid_positions(n, pitch_um)
    cell_count = n * n
    z_layers = -np.arange(layers, dtype=float) * dz_m
    obs = np.column_stack([xy[:, 0], xy[:, 1], np.full(cell_count, sensor_m)])

    V = layers * cell_count  # total node count

    # Edge ordering: Jx(all layers), Jy(all layers), Vz(all interfaces)
    edge_types = []
    edge_src_dst = []

    # Jx edges: from (l, r, c) to (l, r, c+1)
    for layer in range(layers):
        for r in range(n):
            for c in range(n):
                src = (layer, r, c)
                if c < n - 1:
                    dst = (layer, r, c + 1)
                else:
                    dst = None  # boundary edge
                edge_src_dst.append((src, dst))
                edge_types.append("Jx")

    # Jy edges: from (l, r, c) to (l, r+1, c)
    for layer in range(layers):
        for r in range(n):
            for c in range(n):
                src = (layer, r, c)
                if r < n - 1:
                    dst = (layer, r + 1, c)
                else:
                    dst = None
                edge_src_dst.append((src, dst))
                edge_types.append("Jy")

    # Vz edges: from (l, r, c) to (l+1, r, c)
    for layer in range(layers - 1):
        for r in range(n):
            for c in range(n):
                src = (layer, r, c)
                dst = (layer + 1, r, c)
                edge_src_dst.append((src, dst))
                edge_types.append("Vz")

    E = len(edge_src_dst)
    D = np.zeros((V, E), dtype=float)

    for e, ((src_layer, src_r, src_c), dst) in enumerate(edge_src_dst):
        src_node = src_layer * cell_count + src_r * n + src_c
        D[src_node, e] = -1.0
        if dst is not None:
            dst_layer, dst_r, dst_c = dst
            dst_node = dst_layer * cell_count + dst_r * n + dst_c
            D[dst_node, e] = +1.0

    # Build Biot-Savart operator A (M_obs x E)
    # Each edge is treated as a current element at its midpoint
    columns: list[np.ndarray] = []
    names: list[str] = []
    sheet_slices: dict[tuple[int, str], slice] = {}
    via_slices: dict[tuple[int, int], slice] = {}

    jx_start = 0
    jx_count = layers * cell_count
    jy_start = jx_count
    jy_count = layers * cell_count
    vz_start = jx_count + jy_count
    vz_count = (layers - 1) * cell_count

    # Jx columns
    for layer in range(layers):
        start = len(columns)
        for r in range(n):
            for c in range(n):
                z = z_layers[layer]
                if c < n - 1:
                    cx = (xy[c * n + r, 0] + xy[(c + 1) * n + r, 0]) * 0.5
                    cy = (xy[c * n + r, 1] + xy[(c + 1) * n + r, 1]) * 0.5
                else:
                    cx = xy[c * n + r, 0] + pitch_m * 0.5
                    cy = xy[c * n + r, 1]
                src = np.array([cx, cy, z], dtype=float)
                columns.append(_biot_savart_columns(obs, src, np.array([1.0, 0.0, 0.0]), pitch_m))
                names.append(f"L{layer}_Jx_{r}_{c}")
        sheet_slices[(layer, "x")] = slice(start, len(columns))

    # Jy columns
    for layer in range(layers):
        start = len(columns)
        for r in range(n):
            for c in range(n):
                z = z_layers[layer]
                cx = xy[c * n + r, 0]
                if r < n - 1:
                    cy = (xy[c * n + r, 1] + xy[c * n + (r + 1), 1]) * 0.5
                else:
                    cy = xy[c * n + r, 1] + pitch_m * 0.5
                src = np.array([cx, cy, z], dtype=float)
                columns.append(_biot_savart_columns(obs, src, np.array([0.0, 1.0, 0.0]), pitch_m))
                names.append(f"L{layer}_Jy_{r}_{c}")
        sheet_slices[(layer, "y")] = slice(start, len(columns))

    # Vz columns
    for layer in range(layers - 1):
        start = len(columns)
        z_mid = 0.5 * (z_layers[layer] + z_layers[layer + 1])
        for r in range(n):
            for c in range(n):
                cx = xy[c * n + r, 0]
                cy = xy[c * n + r, 1]
                src = np.array([cx, cy, z_mid], dtype=float)
                columns.append(_biot_savart_columns(obs, src, np.array([0.0, 0.0, 1.0]), abs(dz_m)))
                names.append(f"V{layer}{layer+1}_{r}_{c}")
        via_slices[(layer, layer + 1)] = slice(start, len(columns))

    A = np.stack(columns, axis=1)
    col_norm = np.linalg.norm(A, axis=0)

    index = {
        "n": n,
        "layers": layers,
        "cell_count": cell_count,
        "node_count": V,
        "edge_count": E,
        "sheet_slices": sheet_slices,
        "via_slices": via_slices,
        "names": names,
        "z_layers_m": z_layers,
        "pitch_m": pitch_m,
        "edge_types": edge_types,
        "edge_src_dst": edge_src_dst,
        "jx_start": jx_start,
        "jx_count": jx_count,
        "jy_start": jy_start,
        "jy_count": jy_count,
        "vz_start": vz_start,
        "vz_count": vz_count,
    }

    positions = np.column_stack([xy[:, 0], xy[:, 1], np.zeros(cell_count)])

    return OperatorBundle(
        A=A,
        D=D,
        positions=positions,
        obs_positions=obs,
        index=index,
        column_norms=col_norm,
        node_count=V,
        edge_count=E,
        heights=(sensor_h_um,),
    )


def build_port_excitation(bundle: OperatorBundle, cfg: dict) -> PortExcitation:
    """Build port excitation matrix B (V x S).

    Each column is a balanced current injection/extraction at boundary nodes.
    """
    n = int(bundle.index["n"])
    layers = int(bundle.index["layers"])
    cell_count = int(bundle.index["cell_count"])
    S = int(cfg["n_port_states"])
    scheme = cfg["port_config"]["scheme"]
    amp = float(cfg["port_config"]["amplitude"])
    rng = np.random.default_rng(int(cfg["random_seed"]))

    V = bundle.node_count
    B_mat = np.zeros((V, S), dtype=float)
    port_nodes = []
    port_labels = []

    # Define boundary port locations
    def corner_nodes(layer):
        return [
            layer * cell_count + 0,                    # top-left
            layer * cell_count + (n - 1),               # top-right
            layer * cell_count + (n - 1) * n,           # bottom-left
            layer * cell_count + (n - 1) * n + (n - 1), # bottom-right
        ]

    def edge_center_nodes(layer):
        return [
            layer * cell_count + n // 2,                           # top edge center
            layer * cell_count + (n - 1) * n + n // 2,             # bottom edge center
            layer * cell_count + (n // 2) * n,                     # left edge center
            layer * cell_count + (n // 2) * n + (n - 1),           # right edge center
        ]

    top_layer = 0
    bot_layer = layers - 1

    top_corners = corner_nodes(top_layer)
    bot_corners = corner_nodes(bot_layer)
    top_centers = edge_center_nodes(top_layer)
    bot_centers = edge_center_nodes(bot_layer)

    all_ports = list(set(top_corners + bot_corners + top_centers + bot_centers))
    port_nodes = sorted(all_ports)
    port_labels = [f"node_{p}" for p in port_nodes]

    if scheme == "diagonal_pairs":
        # Create S diagonal injection pairs: inject at top layer corner, extract at bottom layer opposite corner
        pairs = [
            (top_corners[0], bot_corners[3]),  # TL → BR
            (top_corners[1], bot_corners[2]),  # TR → BL
            (top_corners[2], bot_corners[1]),  # BL → TR
            (top_corners[3], bot_corners[0]),  # BR → TL
            (top_centers[0], bot_centers[1]),  # Top → Bottom
            (top_centers[2], bot_centers[3]),  # Left → Right
        ]
        pairs = pairs[:S]
        for s, (src, dst) in enumerate(pairs):
            B_mat[src, s] = +amp
            B_mat[dst, s] = -amp

    elif scheme == "boundary_corners":
        # Inject at corners on top layer, extract on bottom layer
        for s in range(min(S, 4)):
            B_mat[top_corners[s], s] = +amp
            B_mat[bot_corners[s], s] = -amp

    elif scheme == "adjacent_pairs":
        # Inject at adjacent corners on top layer
        pairs = [(top_corners[0], top_corners[1]), (top_corners[2], top_corners[3]),
                  (bot_corners[0], bot_corners[1]), (bot_corners[2], bot_corners[3]),
                  (top_centers[0], top_centers[1]), (top_centers[2], top_centers[3])]
        pairs = pairs[:S]
        for s, (src, dst) in enumerate(pairs):
            B_mat[src, s] = +amp
            B_mat[dst, s] = -amp

    for _ in range(S - len(B_mat.nonzero()[0]) // 2):
        # Fill remaining states with random balanced pairs
        s = B_mat.shape[1]
        # This shouldn't happen if S <= len(pairs), but just in case

    actual_S = min(S, (B_mat != 0).any(axis=0).sum())
    if actual_S < S:
        B_mat = B_mat[:, :actual_S]

    return PortExcitation(
        B=B_mat,
        port_nodes=port_nodes,
        port_labels=port_labels,
        n_states=B_mat.shape[1],
    )


def operator_diagnostics(bundle: OperatorBundle) -> dict:
    A = bundle.A
    D = bundle.D
    idx = bundle.index

    via_norms = []
    sheet_norms = []
    for sl in idx["via_slices"].values():
        via_norms.extend(bundle.column_norms[sl].tolist())
    for sl in idx["sheet_slices"].values():
        sheet_norms.extend(bundle.column_norms[sl].tolist())

    via_norms_arr = np.asarray(via_norms, dtype=float)
    sheet_norms_arr = np.asarray(sheet_norms, dtype=float)

    return {
        "A_shape": list(A.shape),
        "D_shape": list(D.shape),
        "node_count": bundle.node_count,
        "edge_count": bundle.edge_count,
        "via_columns_nonzero": bool(np.all(via_norms_arr > 0)),
        "via_column_norm_min": float(np.min(via_norms_arr)),
        "via_column_norm_mean": float(np.mean(via_norms_arr)),
        "sheet_column_norm_mean": float(np.mean(sheet_norms_arr)),
        "obs_dim": int(A.shape[0]),
        "current_dim": int(A.shape[1]),
        "D_rank": int(np.linalg.matrix_rank(D)),
        "D_nullity": int(D.shape[1] - np.linalg.matrix_rank(D)),
    }
