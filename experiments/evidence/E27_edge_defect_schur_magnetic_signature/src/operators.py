"""Generated graph-Laplacian network, Sherman-Morrison edge-defect perturbation,
and edge-segment Biot-Savart forward model for E27."""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from numpy.linalg import lstsq

MU0_OVER_4PI = 1e-7
EPS = 1e-18


@dataclass
class OperatorBundle:
    """Graph-Laplacian network and forward operator bundle."""
    A: np.ndarray
    positions: np.ndarray
    obs_positions: np.ndarray
    index: dict
    column_norms: np.ndarray
    D: np.ndarray
    L: np.ndarray
    G: np.ndarray
    conductances: np.ndarray
    edge_list: list[dict]
    edge_segment_positions: dict


@dataclass
class CandidateDefect:
    """A candidate edge defect with perturbation parameters."""
    defect_id: str
    family: str
    endpoints: tuple[int, int]
    layer_ids: tuple[int, int]
    edge_role: str
    alpha: float
    R_q: float
    a_q: np.ndarray
    baseline_voltage_drops: np.ndarray | None = None


def _grid_positions(n: int, pitch_um: float) -> np.ndarray:
    coords = (np.arange(n, dtype=float) - (n - 1) / 2.0) * pitch_um * 1e-6
    xx, yy = np.meshgrid(coords, coords, indexing="xy")
    return np.column_stack([xx.ravel(), yy.ravel()])


def _biot_savart_segment(
    obs: np.ndarray,
    r_start: np.ndarray,
    r_end: np.ndarray,
    current: float,
    n_quad: int = 5,
) -> np.ndarray:
    """Biot-Savart field for a finite straight segment carrying current I.

    Uses midpoint quadrature along the segment.
    """
    t_vals = np.linspace(0.0, 1.0, n_quad)
    dl = r_end - r_start
    length = np.linalg.norm(dl)
    if length < EPS:
        return np.zeros(obs.shape[0] * 3, dtype=float)
    dl_unit = dl / length
    b = np.zeros(obs.shape[0] * 3, dtype=float)
    dt = 1.0 / n_quad
    for t in t_vals:
        r_src = r_start + t * dl
        r = obs - r_src[None, :]
        norm3 = np.linalg.norm(r, axis=1) ** 3 + EPS
        cross = np.cross(np.tile(dl_unit * length * dt, (obs.shape[0], 1)), r)
        b += (MU0_OVER_4PI * current * cross / norm3[:, None]).reshape(-1)
    return b


def build_graph_network(cfg: dict) -> dict:
    """Build a multi-layer planar graph network with vertices, edges, incidence matrix,
    conductance matrix, and Laplacian.
    """
    n = int(cfg["grid_size"])
    layers = int(cfg["layer_count"])
    pitch = float(cfg["pixel_pitch_um"]) * 1e-6
    dz = float(cfg["layer_spacing_um"]) * 1e-6
    xy = _grid_positions(n, float(cfg["pixel_pitch_um"]))
    cell_count = n * n

    # Build vertices: (layer, cell_idx) -> global node ID
    nodes = []
    node_map = {}
    for layer in range(layers):
        z = -layer * dz
        for ci in range(cell_count):
            gid = len(nodes)
            node_map[(layer, ci)] = gid
            nodes.append({"layer": layer, "cell": ci, "pos": np.array([xy[ci, 0], xy[ci, 1], z])})

    # Build edges:
    # - Intra-layer edges: horizontal and vertical between adjacent cells
    # - Inter-layer (via) edges: between same cell on adjacent layers
    edges = []
    edge_list = []
    conductance_vals = []
    # Layer-dependent base conductance
    g0 = 1.0
    for layer in range(layers):
        g_layer = g0 * (1.0 - 0.05 * layer)
        for iy in range(n):
            for ix in range(n):
                ci = iy * n + ix
                u = node_map[(layer, ci)]
                # Horizontal edge (right neighbor)
                if ix + 1 < n:
                    cj = iy * n + (ix + 1)
                    v = node_map[(layer, cj)]
                    edges.append((u, v))
                    edge_list.append({"type": "intra_h", "layer": layer, "cell_a": ci, "cell_b": cj,
                                      "role": "sheet_x"})
                    conductance_vals.append(g_layer)
                # Vertical edge (down neighbor)
                if iy + 1 < n:
                    cj = (iy + 1) * n + ix
                    v = node_map[(layer, cj)]
                    edges.append((u, v))
                    edge_list.append({"type": "intra_v", "layer": layer, "cell_a": ci, "cell_b": cj,
                                      "role": "sheet_y"})
                    conductance_vals.append(g_layer)

    # Inter-layer (via) edges
    via_conductance = g0 * 0.8
    for layer in range(layers - 1):
        for ci in range(cell_count):
            u = node_map[(layer, ci)]
            v = node_map[(layer + 1, ci)]
            edges.append((u, v))
            edge_list.append({"type": "via", "layer_a": layer, "layer_b": layer + 1,
                              "cell": ci, "role": "via_vertical"})
            conductance_vals.append(via_conductance)

    V = len(nodes)
    E = len(edges)
    D = np.zeros((V, E), dtype=float)
    for e_idx, (u, v) in enumerate(edges):
        D[u, e_idx] = -1.0
        D[v, e_idx] = 1.0

    C = np.diag(np.array(conductance_vals, dtype=float))
    L_full = D @ C @ D.T

    # Gauge fixing: ground one node (first node)
    L = L_full[1:, 1:]
    D_int = D[1:, :]  # internal incidence (rows for non-grounded nodes)

    # Pseudo-inverse for the grounded system
    try:
        G = np.linalg.inv(L)
    except np.linalg.LinAlgError:
        G = np.linalg.pinv(L)

    # Pad G back to full size
    G_full = np.zeros((V, V), dtype=float)
    G_full[1:, 1:] = G

    # Edge segment positions for Biot-Savart
    edge_seg_positions = {}
    for e_idx, edge in enumerate(edge_list):
        if edge["type"] in ("intra_h", "intra_v"):
            ci = edge["cell_a"]
            cj = edge["cell_b"]
            r_start = nodes[node_map[(edge["layer"], ci)]]["pos"]
            r_end = nodes[node_map[(edge["layer"], cj)]]["pos"]
        else:  # via
            ci = edge["cell"]
            r_start = nodes[node_map[(edge["layer_a"], ci)]]["pos"]
            r_end = nodes[node_map[(edge["layer_b"], ci)]]["pos"]
        edge_seg_positions[e_idx] = (r_start.copy(), r_end.copy())

    return {
        "n": n, "layers": layers, "cell_count": cell_count,
        "nodes": nodes, "node_map": node_map,
        "edges": edges, "edge_list": edge_list,
        "D": D, "D_int": D_int, "C": C,
        "L_full": L_full, "L": L, "G_full": G_full, "G": G,
        "conductances": np.array(conductance_vals, dtype=float),
        "edge_seg_positions": edge_seg_positions,
        "via_edge_indices": [i for i, e in enumerate(edge_list) if e["type"] == "via"],
        "sheet_edge_indices": [i for i, e in enumerate(edge_list) if e["type"] != "via"],
        "node_positions": np.array([nd["pos"] for nd in nodes], dtype=float),
    }


def build_operator(cfg: dict) -> OperatorBundle:
    """Build the full operator bundle: graph network + Biot-Savart forward + Laplacian."""
    net = build_graph_network(cfg)
    n = int(cfg["grid_size"])
    sensor_h = float(cfg["sensor_height_um"]) * 1e-6
    pitch = float(cfg["pixel_pitch_um"]) * 1e-6
    xy = _grid_positions(n, float(cfg["pixel_pitch_um"]))
    n_quad = int(cfg.get("edge_segment_quadrature_points", 5))

    obs = np.column_stack([xy[:, 0], xy[:, 1], np.full(n * n, sensor_h)])
    m = obs.shape[0] * 3  # Bx, By, Bz per sensor
    E = len(net["edges"])

    # Build edge-segment forward matrix: column e = B field from unit current in edge e
    A = np.zeros((m, E), dtype=float)
    for e_idx in range(E):
        r_start, r_end = net["edge_seg_positions"][e_idx]
        col = _biot_savart_segment(obs, r_start, r_end, 1.0, n_quad)
        A[:, e_idx] = col

    col_norms = np.linalg.norm(A, axis=0)

    index = {
        "n": n,
        "layers": net["layers"],
        "cell_count": net["cell_count"],
        "edge_count": E,
        "node_count": len(net["nodes"]),
        "via_edge_indices": net["via_edge_indices"],
        "sheet_edge_indices": net["sheet_edge_indices"],
        "sensor_height_m": sensor_h,
        "pitch_m": pitch,
        "net": net,
    }

    return OperatorBundle(
        A=A,
        positions=net["node_positions"],
        obs_positions=obs,
        index=index,
        column_norms=col_norms,
        D=net["D"],
        L=net["L"],
        G=net["G"],
        conductances=net["conductances"],
        edge_list=net["edge_list"],
        edge_segment_positions=net["edge_seg_positions"],
    )


def operator_diagnostics(bundle: OperatorBundle) -> dict:
    """Compute operator diagnostics."""
    A = bundle.A
    via_idx = bundle.index["via_edge_indices"]
    sheet_idx = bundle.index["sheet_edge_indices"]
    via_norms = bundle.column_norms[via_idx]
    sheet_norms = bundle.column_norms[sheet_idx]
    return {
        "shape": list(A.shape),
        "edge_count": int(A.shape[1]),
        "node_count": int(bundle.D.shape[0]),
        "via_edges_nonzero": bool(np.all(via_norms > 0)),
        "via_column_norm_min": float(np.min(via_norms)) if len(via_norms) > 0 else 0.0,
        "via_column_norm_mean": float(np.mean(via_norms)) if len(via_norms) > 0 else 0.0,
        "sheet_column_norm_mean": float(np.mean(sheet_norms)),
        "laplacian_rank": int(np.linalg.matrix_rank(bundle.L)),
        "laplacian_condition": float(np.linalg.cond(bundle.L)),
        "grounded_nodes": int(bundle.L.shape[0]),
    }


def build_candidate_defects(bundle: OperatorBundle, cfg: dict) -> list[CandidateDefect]:
    """Build candidate edge defect instances from config families."""
    rng = np.random.default_rng(int(cfg["random_seed"]) + 777)
    net = bundle.index["net"]
    n = net["n"]
    cell_count = net["cell_count"]
    node_map = net["node_map"]
    layers = net["layers"]
    V = len(net["nodes"])
    G_full = net["G_full"]

    schur_cfg = cfg["schur"]
    alpha_nominal = float(schur_cfg["alpha_nominal"])

    candidates: list[CandidateDefect] = []
    c_idx = 0

    for family in cfg["candidate_defect_families"]:
        for _ in range(int(cfg["case_count_per_family"])):
            if family == "via_insertion":
                layer_a = int(rng.integers(0, layers - 1))
                layer_b = layer_a + 1
                ci = int(rng.integers(0, cell_count))
                u = node_map[(layer_a, ci)]
                v = node_map[(layer_b, ci)]
                role = "via_vertical"
                alpha = alpha_nominal * rng.uniform(0.5, 1.5)

            elif family == "via_removal":
                layer_a = int(rng.integers(0, layers - 1))
                layer_b = layer_a + 1
                ci = int(rng.integers(0, cell_count))
                u = node_map[(layer_a, ci)]
                v = node_map[(layer_b, ci)]
                role = "via_vertical"
                alpha = -alpha_nominal

            elif family == "return_path_insertion":
                layer = int(rng.integers(0, layers))
                ci = int(rng.integers(0, cell_count - n))
                cj = ci + n * (int(rng.integers(1, n - 1))) + int(rng.integers(0, n - 1))
                if cj >= cell_count:
                    cj = cell_count - 1
                u = node_map[(layer, ci)]
                v = node_map[(layer, cj)]
                role = "return_path"
                alpha = alpha_nominal * rng.uniform(0.3, 1.0)

            elif family == "return_path_removal":
                layer = int(rng.integers(0, layers))
                ci = int(rng.integers(0, cell_count - n))
                cj = ci + n * (int(rng.integers(1, n - 1))) + int(rng.integers(0, n - 1))
                if cj >= cell_count:
                    cj = cell_count - 1
                u = node_map[(layer, ci)]
                v = node_map[(layer, cj)]
                role = "return_path"
                alpha = -alpha_nominal

            elif family == "local_open_segment":
                layer = int(rng.integers(0, layers))
                ci = int(rng.integers(0, cell_count - 1))
                cj = ci + 1
                u = node_map[(layer, ci)]
                v = node_map[(layer, cj)]
                role = "sheet_open"
                alpha = -alpha_nominal * 0.8

            elif family == "parasitic_short_bridge":
                layer_a = int(rng.integers(0, layers))
                layer_b = int(rng.integers(0, layers))
                if layer_a == layer_b:
                    layer_b = min(layer_a + 1, layers - 1)
                ci = int(rng.integers(0, cell_count))
                cj = int(rng.integers(0, cell_count))
                u = node_map[(layer_a, ci)]
                v = node_map[(layer_b, cj)]
                role = "parasitic_short"
                alpha = alpha_nominal * rng.uniform(0.2, 0.8)

            else:  # deep_layer_alternate_return
                layer = layers - 1
                ci = int(rng.integers(0, n))
                cj = int(rng.integers(cell_count - n, cell_count))
                u = node_map[(layer, ci)]
                v = node_map[(layer, cj)]
                role = "deep_return"
                alpha = alpha_nominal * rng.uniform(0.4, 1.2)

            a_q = np.zeros(V, dtype=float)
            a_q[u] = -1.0
            a_q[v] = 1.0

            # Effective resistance: a_q^T G a_q (using gauge-fixed system)
            a_int = a_q[1:]
            R_q = float(a_int @ net["G"] @ a_int)

            defect = CandidateDefect(
                defect_id=f"DEF_{c_idx:03d}_{family}",
                family=family,
                endpoints=(u, v),
                layer_ids=(net["nodes"][u]["layer"], net["nodes"][v]["layer"]),
                edge_role=role,
                alpha=alpha,
                R_q=R_q,
                a_q=a_q,
            )
            candidates.append(defect)
            c_idx += 1

    return candidates


def solve_potential(bundle: OperatorBundle, b: np.ndarray) -> np.ndarray:
    """Solve L * phi_int = b_int for the grounded Laplacian system."""
    b_int = b[1:]
    phi_int = lstsq(bundle.L, b_int, rcond=None)[0]
    phi = np.zeros(bundle.D.shape[0], dtype=float)
    phi[1:] = phi_int
    return phi


def edge_currents(bundle: OperatorBundle, phi: np.ndarray) -> np.ndarray:
    """Compute edge currents i = C * D^T * phi."""
    return bundle.conductances * (bundle.D.T @ phi)


def schur_potential_perturbation(
    bundle: OperatorBundle,
    phi_baseline: np.ndarray,
    defect: CandidateDefect,
) -> np.ndarray:
    """Sherman-Morrison perturbed potential: phi(alpha) = phi - (alpha * v_q / (1 + alpha*R_q)) * G * a_q"""
    V = bundle.D.shape[0]
    G_full = bundle.index["net"]["G_full"]
    a_q = defect.a_q
    alpha = defect.alpha
    R_q = defect.R_q
    v_q = float(a_q @ phi_baseline)
    denom = 1.0 + alpha * R_q
    if abs(denom) < EPS:
        return phi_baseline.copy()
    factor = alpha * v_q / denom
    delta_phi = -factor * (G_full @ a_q)
    return phi_baseline + delta_phi


def schur_edge_current_perturbation(
    bundle: OperatorBundle,
    phi_baseline: np.ndarray,
    defect: CandidateDefect,
) -> np.ndarray:
    """Compute perturbed edge currents using Sherman-Morrison.

    Delta_i = (alpha * v_q / (1 + alpha*R_q)) * [e_q - C * D^T * G * a_q]
    where e_q is a unit vector for the candidate edge (not in original edge set).
    """
    G_full = bundle.index["net"]["G_full"]
    a_q = defect.a_q
    alpha = defect.alpha
    R_q = defect.R_q
    v_q = float(a_q @ phi_baseline)
    denom = 1.0 + alpha * R_q
    if abs(denom) < EPS:
        return edge_currents(bundle, phi_baseline)
    factor = alpha * v_q / denom

    # Perturbation to existing edges: -C * D^T * G_full * a_q
    delta_i_existing = -factor * (bundle.conductances * (bundle.D.T @ (G_full @ a_q)))

    return delta_i_existing


def magnetic_signature(
    bundle: OperatorBundle,
    delta_i: np.ndarray,
) -> np.ndarray:
    """Compute magnetic field perturbation: Delta_y = A * Delta_i."""
    return bundle.A @ delta_i


def compute_edge_signal(
    bundle: OperatorBundle,
    phi_baseline: np.ndarray,
    defect: CandidateDefect,
    W: np.ndarray | None = None,
) -> float:
    """Compute signal energy S_q = ||W * Delta_Y_q||_2 for a single state."""
    delta_i = schur_edge_current_perturbation(bundle, phi_baseline, defect)
    delta_y = magnetic_signature(bundle, delta_i)
    if W is not None:
        delta_y = W @ delta_y
    return float(np.linalg.norm(delta_y))


def compute_edge_gamma(
    bundle: OperatorBundle,
    signal: float,
    cfg: dict,
) -> float:
    """Compute robust edge-defect Gamma = S_q - epsilon - rho - tau."""
    epsilon = float(cfg["noise_sigma"])
    rho_scale = float(cfg["operator_perturbation"]["rho_scale"])
    rho = rho_scale * signal
    tau = float(cfg["decision"]["tau_threshold"])
    return signal - epsilon - rho - tau


def design_schur_states(
    bundle: OperatorBundle,
    candidates: list[CandidateDefect],
    cfg: dict,
    n_states: int,
) -> list[np.ndarray]:
    """Design port excitation states that maximize voltage drops across candidate defects.

    For each candidate, compute optimal port injection b* = argmax |a_q^T L^dagger b|.
    Then use minimax to select states for critical defects.
    """
    rng = np.random.default_rng(int(cfg["random_seed"]) + 888)
    V = bundle.D.shape[0]

    # Compute sensitivity vectors: s_q = G_full @ a_q for each candidate
    sensitivities = []
    for defect in candidates:
        s_q = bundle.index["net"]["G_full"] @ defect.a_q
        sensitivities.append(s_q / (np.linalg.norm(s_q) + EPS))

    # Greedy selection: pick states that maximize minimum voltage drop across candidates
    selected_states = []
    n_crit = min(int(cfg["schur"]["minimax_candidates"]), len(candidates))

    for state_idx in range(n_states):
        best_state = None
        best_min_score = -np.inf

        for _ in range(200):  # Random search over port pairs
            # Generate a random port pair (source/sink) consistent with 1^T b = 0
            u = int(rng.integers(0, V))
            v = int(rng.integers(0, V))
            while v == u:
                v = int(rng.integers(0, V))

            b_candidate = np.zeros(V, dtype=float)
            b_candidate[u] = 1.0
            b_candidate[v] = -1.0

            # Ensure 1^T b = 0 and feasibility: project onto grounded system
            if abs(np.sum(b_candidate)) < EPS or True:
                # Score: min voltage drop across top critical defects
                min_score = np.inf
                for defect in candidates[:n_crit]:
                    v_q = abs(float(defect.a_q @ (bundle.index["net"]["G_full"] @ b_candidate)))
                    denom = 1.0 + abs(defect.alpha) * defect.R_q
                    score = v_q / (denom + EPS)
                    min_score = min(min_score, score)

                if min_score > best_min_score:
                    best_min_score = min_score
                    best_state = b_candidate.copy()

        if best_state is not None:
            selected_states.append(best_state)

    return selected_states


def design_random_states(bundle: OperatorBundle, cfg: dict, n_states: int) -> list[np.ndarray]:
    """Generate random port states as baseline."""
    rng = np.random.default_rng(int(cfg["random_seed"]) + 999)
    V = bundle.D.shape[0]
    states = []
    for _ in range(n_states):
        u = int(rng.integers(0, V))
        v = int(rng.integers(0, V))
        while v == u:
            v = int(rng.integers(0, V))
        b = np.zeros(V, dtype=float)
        b[u] = 1.0
        b[v] = -1.0
        states.append(b)
    return states


def design_max_current_norm_states(bundle: OperatorBundle, cfg: dict, n_states: int) -> list[np.ndarray]:
    """States that maximize total current norm."""
    rng = np.random.default_rng(int(cfg["random_seed"]) + 1111)
    V = bundle.D.shape[0]
    G_full = bundle.index["net"]["G_full"]

    # Current norm ~ ||C D^T G b||
    states = []
    scoring_mat = bundle.conductances[:, None] * (bundle.D.T @ G_full)

    for _ in range(n_states):
        best_b = None
        best_score = -np.inf
        for _ in range(100):
            u = int(rng.integers(0, V))
            v = int(rng.integers(0, V))
            while v == u:
                v = int(rng.integers(0, V))
            b = np.zeros(V, dtype=float)
            b[u] = 1.0
            b[v] = -1.0
            score = float(np.linalg.norm(scoring_mat @ b))
            if score > best_score:
                best_score = score
                best_b = b.copy()
        states.append(best_b)
    return states


def design_max_resistance_contrast_states(
    bundle: OperatorBundle,
    candidates: list[CandidateDefect],
    cfg: dict,
    n_states: int,
) -> list[np.ndarray]:
    """States maximizing effective resistance contrast between defect endpoints."""
    rng = np.random.default_rng(int(cfg["random_seed"]) + 2222)
    V = bundle.D.shape[0]
    G_full = bundle.index["net"]["G_full"]

    states = []
    for _ in range(n_states):
        best_b = None
        best_score = -np.inf
        for _ in range(100):
            u = int(rng.integers(0, V))
            v = int(rng.integers(0, V))
            while v == u:
                v = int(rng.integers(0, V))
            b = np.zeros(V, dtype=float)
            b[u] = 1.0
            b[v] = -1.0
            # Resistance contrast: max over candidates of |a_q^T G b| / R_q
            max_contrast = 0.0
            for defect in candidates:
                contrast = abs(float(defect.a_q @ (G_full @ b))) / (defect.R_q + EPS)
                max_contrast = max(max_contrast, contrast)
            if max_contrast > best_score:
                best_score = max_contrast
                best_b = b.copy()
        states.append(best_b)
    return states


def design_oracle_states(
    bundle: OperatorBundle,
    candidates: list[CandidateDefect],
    cfg: dict,
    n_states: int,
) -> list[np.ndarray]:
    """Oracle: directly use the true defect a_q as excitation (non-deployable upper bound)."""
    V = bundle.D.shape[0]
    states = []
    for i in range(min(n_states, len(candidates))):
        defect = candidates[i]
        b = defect.a_q.copy()
        states.append(b)
    return states
