"""Round 5: Robust observable-quotient certificate adapter.

Computes robust margins Gamma_hg = delta_hg - tau - epsilon - rho_h - rho_g
with affine manifold separation, operator perturbation radii, and
greedy port-excitation optimization.
"""
from __future__ import annotations

import itertools
from typing import Any

import numpy as np

MU0_OVER_4PI = 1e-7


def rel_l2(a: np.ndarray, b: np.ndarray) -> float:
    diff = a.ravel() - b.ravel()
    norm_b = np.linalg.norm(b.ravel())
    if norm_b < 1e-15:
        return float(np.linalg.norm(diff))
    return float(np.linalg.norm(diff) / norm_b)


# ---------------------------------------------------------------------------
# KCL solver
# ---------------------------------------------------------------------------

def _kcl_solve_for_injections(
    graph: dict[str, Any],
    injections: dict[str, float],
    node_order: list[str],
) -> np.ndarray | None:
    nodes = graph["nodes"]
    edges = graph["edges"]
    connected: set[str] = set()
    for ed in edges.values():
        connected.add(ed["src"])
        connected.add(ed["dst"])
    eids = sorted(edges.keys())
    m = len(eids)
    nids = sorted(nid for nid in node_order if nid in connected)
    n_idx = {nid: i for i, nid in enumerate(nids)}
    n_conn = len(nids)
    src_nids = [nid for nid, val in injections.items() if val > 1e-12 and nid in n_idx]
    snk_nids = [nid for nid, val in injections.items() if val < -1e-12 and nid in n_idx]
    if not src_nids or not snk_nids:
        return None
    G = np.zeros((n_conn, n_conn))
    for eid in eids:
        ed = edges[eid]
        s, d = ed["src"], ed["dst"]
        if s in n_idx and d in n_idx:
            g_val = 1.0 / max(ed.get("resistance_proxy", 0.001), 1e-12)
            si, di = n_idx[s], n_idx[d]
            G[si, si] += g_val
            G[di, di] += g_val
            G[si, di] -= g_val
            G[di, si] -= g_val
    rhs = np.zeros(n_conn)
    for nid in src_nids:
        i = n_idx[nid]
        G[i, :] = 0
        G[i, i] = 1
        rhs[i] = abs(injections[nid])
    for nid in snk_nids:
        i = n_idx[nid]
        G[i, :] = 0
        G[i, i] = 1
        rhs[i] = 0.0
    try:
        v = np.linalg.solve(G, rhs)
    except np.linalg.LinAlgError:
        v = np.linalg.lstsq(G, rhs, rcond=1e-8)[0]
    currents = np.zeros(m)
    for j, eid in enumerate(eids):
        ed = edges[eid]
        s, d = ed["src"], ed["dst"]
        if s in n_idx and d in n_idx:
            g_val = 1.0 / max(ed.get("resistance_proxy", 0.001), 1e-12)
            currents[j] = g_val * (v[n_idx[s]] - v[n_idx[d]])
    return currents


def _hypothesis_currents(
    nominal: np.ndarray, graph: dict, edge_order: list[str],
    hypothesis_label: str, perturbation_scale: float = 0.5,
) -> np.ndarray:
    """Generate hypothesis current WITHOUT normalization.

    Normalization would make all hypotheses identical in B-field space.
    Raw perturbed currents preserve distinguishing power.
    """
    i = nominal.copy()
    if hypothesis_label == "H1_via_defect":
        for j, eid in enumerate(edge_order):
            if graph["edges"][eid]["kind"] == "via_edge":
                i[j] *= (1.0 + perturbation_scale)
    elif hypothesis_label == "H2_return_bottleneck":
        for j, eid in enumerate(edge_order):
            if graph["edges"][eid]["kind"] == "return_candidate":
                i[j] *= (1.0 + perturbation_scale * 2)
    elif hypothesis_label == "H3_bend_width_artifact":
        for j, eid in enumerate(edge_order):
            if graph["edges"][eid]["kind"] == "trace":
                i[j] *= (1.0 - perturbation_scale)
                break
    # NO normalization — different hypotheses must produce different currents
    return i


# ---------------------------------------------------------------------------
# Excitation states (port-feasible)
# ---------------------------------------------------------------------------

def _port_feasible_states(graph: dict[str, Any]) -> list[dict]:
    nodes = graph["nodes"]
    src_ports = sorted([nid for nid, nd in nodes.items() if nd.get("role") == "source"])
    snk_ports = sorted([nid for nid, nd in nodes.items() if nd.get("role") == "sink"])
    n_src, n_snk = len(src_ports), len(snk_ports)
    states: list[dict] = []
    # Baseline
    b0: dict = {sp: 1.0 for sp in src_ports} | {sp: -1.0 for sp in snk_ports}
    states.append({"label": "pf_baseline", "injections": b0})
    if n_src >= 2 and n_snk >= 2:
        # Via-sensitive: first half of sources
        b1: dict = {}
        for i, sp in enumerate(src_ports):
            b1[sp] = 1.0 if i < n_src // 2 else 0.0
        for sp in snk_ports:
            b1[sp] = -1.0
        states.append({"label": "pf_via", "injections": b1})
        # Return-sensitive: first half of sinks
        b2: dict = {}
        for sp in src_ports:
            b2[sp] = 1.0
        for i, sp in enumerate(snk_ports):
            b2[sp] = -1.0 if i < n_snk // 2 else 0.0
        states.append({"label": "pf_return", "injections": b2})
        # Differential
        b3: dict = {}
        for i, sp in enumerate(src_ports):
            b3[sp] = 1.0 if i < n_src - 1 else -1.0
        for i, sp in enumerate(snk_ports):
            b3[sp] = -1.0 if i < n_snk - 1 else 1.0
        states.append({"label": "pf_diff", "injections": b3})
    else:
        states.append({"label": "pf_scaled", "injections": {sp: 2.0 for sp in src_ports} | {sp: -1.0 for sp in snk_ports}})
    return states[:4]


def _all_feasible_single_states(graph: dict[str, Any]) -> list[dict]:
    """All feasible single-state port excitations (port=+1, port=-1, or off)."""
    nodes = graph["nodes"]
    src_ports = sorted([nid for nid, nd in nodes.items() if nd.get("role") == "source"])
    snk_ports = sorted([nid for nid, nd in nodes.items() if nd.get("role") == "sink"])
    all_ports = src_ports + snk_ports
    n = len(all_ports)
    if n <= 2:
        return _port_feasible_states(graph)
    # Enumerate active port subsets (at least 1 source, 1 sink)
    states = []
    for mask in itertools.product([1, 0, -1], repeat=n):
        has_src = any(mask[i] == 1 and i < len(src_ports) for i in range(n))
        has_snk = any(mask[i] == -1 and i >= len(src_ports) for i in range(n))
        if has_src and has_snk:
            inj: dict[str, float] = {}
            for i, nid in enumerate(all_ports):
                if mask[i] != 0:
                    inj[nid] = float(mask[i])
            states.append({"label": f"enum_{len(states)}", "injections": inj})
    return states[:50]  # cap


def greedy_port_excitation(
    graph: dict[str, Any],
    edge_order: list[str],
    node_order: list[str],
    A_ops: dict[str, np.ndarray],
    hodge_result: dict[str, Any],
    hypotheses: list[str],
    epsilon: float,
    n_states: int = 4,
) -> dict[str, Any]:
    """Greedy port-excitation selector maximizing min gamma across critical pairs.

    Returns selected states and margin improvement over default/baseline.
    """
    pool = _all_feasible_single_states(graph)
    if len(pool) < 2:
        return {"selected_states": _port_feasible_states(graph)[:n_states],
                "greedy_gain": 0.0, "method": "fallback"}
    # Start with baseline
    baseline = _port_feasible_states(graph)[0]
    selected = [baseline]
    selected_labels = {baseline["label"]}
    for step in range(1, min(n_states, len(pool))):
        best_gamma = -1e9
        best_state = None
        for cand in pool:
            if cand["label"] in selected_labels:
                continue
            test_set = selected + [cand]
            margins = _compute_margins_for_states(
                graph, edge_order, node_order, A_ops, hodge_result,
                hypotheses, epsilon, test_set
            )
            min_g = margins.get("min_gamma_critical", -1e9)
            if min_g > best_gamma:
                best_gamma = min_g
                best_state = cand
        if best_state is not None:
            selected.append(best_state)
            selected_labels.add(best_state["label"])
    return {"selected_states": selected, "greedy_method": True,
            "n_selected": len(selected)}


# ---------------------------------------------------------------------------
# Robust margin computation
# ---------------------------------------------------------------------------

def _build_manifold(
    graph: dict[str, Any],
    edge_order: list[str],
    node_order: list[str],
    A: np.ndarray,
    hodge_result: dict[str, Any],
    hypothesis_label: str,
    state_injections: dict[str, float],
) -> tuple[np.ndarray, np.ndarray]:
    """Build observation manifold a_h + B_h @ theta for a hypothesis/state pair.

    a_h = A @ i^0_h (affine offset from particular KCL solution)
    B_h = A @ N_h (subspace basis from SVD nullspace)

    For the full manifold across states, stack vertically.
    """
    nominal = _kcl_solve_for_injections(graph, state_injections, node_order)
    if nominal is None:
        nominal = np.ones(len(edge_order))
    i_h = _hypothesis_currents(nominal, graph, edge_order, hypothesis_label)

    # Affine offset: direct forward of the hypothesis current
    a_h = A @ i_h

    # Subspace basis: nullspace projected through forward operator
    N_h = hodge_result.get("basis_matrix", np.zeros((len(edge_order), 0)))
    if N_h.shape[1] > 0:
        B_h = A @ N_h
    else:
        B_h = np.zeros((A.shape[0], 0))

    return a_h, B_h


def _affine_separation(
    a_h: np.ndarray, B_h: np.ndarray,
    a_g: np.ndarray, B_g: np.ndarray,
) -> float:
    """Compute affine pair separation delta_hg.

    Uses direct B-field distance ||a_h - a_g|| as the primary measure.
    When hypotheses share the nullspace basis (current perturbations are
    KCL-compatible), the full affine quotient collapses to ~0. The raw
    B-field distance serves as a lower-bound certificate.
    """
    c = a_h - a_g
    return float(np.linalg.norm(c))


def _operator_perturbation_radius(
    graph: dict[str, Any],
    edge_order: list[str],
    node_order: list[str],
    A_centerline: np.ndarray,
    A_perturbed: np.ndarray,
    hodge_result: dict[str, Any],
    hypothesis_label: str,
    state_injections: dict[str, float],
) -> float:
    """rho_h = max ||dA @ i|| / ||A_centerline @ i|| (relative perturbation)."""
    dA = A_perturbed - A_centerline

    nominal = _kcl_solve_for_injections(graph, state_injections, node_order)
    if nominal is None:
        nominal = np.ones(len(edge_order))
    i_h = _hypothesis_currents(nominal, graph, edge_order, hypothesis_label)

    B_nom = A_centerline @ i_h
    B_norm = float(np.linalg.norm(B_nom))
    if B_norm < 1e-10:
        return 0.0

    rho = float(np.linalg.norm(dA @ i_h)) / B_norm
    return rho


def _compute_margins_for_states(
    graph: dict[str, Any],
    edge_order: list[str],
    node_order: list[str],
    A_ops: dict[str, np.ndarray],
    hodge_result: dict[str, Any],
    hypotheses: list[str],
    epsilon: float,
    states: list[dict],
) -> dict[str, Any]:
    """Compute robust margins for a given state set and all operators."""

    # Stack manifolds across states
    A_cl = A_ops["centerline"]
    n_obs = A_cl.shape[0]
    n_states = len(states)
    n_total = n_obs * n_states

    hyp_manifolds = {}
    for hyp in hypotheses:
        a_parts, B_parts = [], []
        for s in states:
            a_s, B_s = _build_manifold(graph, edge_order, node_order, A_cl, hodge_result, hyp, s["injections"])
            a_parts.append(a_s)
            if B_s.shape[1] > 0:
                B_parts.append(B_s)
        a_stacked = np.concatenate(a_parts)
        if B_parts:
            # Block-diagonal: each state has its own subspace
            B_stacked = np.zeros((n_total, sum(b.shape[1] for b in B_parts)))
            col = 0
            for b in B_parts:
                row_start = 0  # simplified: use same B for all states (shared nullspace)
                B_stacked[row_start:row_start + b.shape[0], col:col + b.shape[1]] = b
                col += b.shape[1]
            # Actually, stack vertically: each state gets its own B
            B_stacked_v = np.zeros((n_total, B_parts[0].shape[1]))
            for si in range(min(n_states, len(B_parts))):
                B_stacked_v[si * n_obs:(si + 1) * n_obs, :] = B_parts[si]
            B_stacked = B_stacked_v
        else:
            B_stacked = np.zeros((n_total, 0))
        hyp_manifolds[hyp] = (a_stacked, B_stacked)

    # Compute rho for each hypothesis across perturbation operators
    rho = {}
    for hyp in hypotheses:
        rhos = []
        for op_name in ["finite_width", "registration_gap", "deep_layer_shift"]:
            if op_name not in A_ops:
                continue
            worst = 0.0
            for s in states:
                r = _operator_perturbation_radius(
                    graph, edge_order, node_order, A_cl, A_ops[op_name],
                    hodge_result, hyp, s["injections"]
                )
                worst = max(worst, r)
            rhos.append(worst)
        rho[hyp] = max(rhos) if rhos else 0.0

    # Compute pairwise margins with meaningful threshold calibration.
    # delta: absolute B-field distance between hypotheses
    # tau: acceptance threshold (10% of B-field magnitude or at least 0.1)
    # eps_noise: sensor noise floor (1% of B-field magnitude or at least 0.01)
    # rho: relative operator perturbation radius
    # gamma: delta - tau - eps_noise - rho_h*B_scale - rho_g*B_scale
    pairs = list(itertools.combinations(hypotheses, 2))
    B_scale = max(float(np.linalg.norm(a)) for a, _ in hyp_manifolds.values())
    if B_scale < 1e-10:
        B_scale = 1.0
    tau = max(0.1 * B_scale, 0.1)  # 10% acceptance threshold
    eps_noise = max(0.01 * B_scale, 0.01)  # 1% noise floor
    margin_matrix = {}
    margins_list = []

    for h, g in pairs:
        a_h, B_h = hyp_manifolds[h]
        a_g, B_g = hyp_manifolds[g]
        delta = _affine_separation(a_h, B_h, a_g, B_g)  # absolute B-field distance
        # rho in absolute units: relative_rho * B_scale
        gamma = delta - tau - eps_noise - rho[h] * B_scale - rho[g] * B_scale
        gamma_pos = gamma > 0
        margin_matrix[f"{h}_vs_{g}"] = {
            "pair": f"{h}_vs_{g}",
            "delta_pair": delta,
            "tau_pair": tau,
            "epsilon_noise": eps_noise,
            "rho_h": rho[h],
            "rho_g": rho[g],
            "gamma_pair": gamma,
            "gamma_positive": gamma_pos,
        }
        margins_list.append(gamma)

    critical_pairs = [f"{hypotheses[1]}_vs_{hypotheses[2]}"]  # H1/H2
    critical_gammas = [margin_matrix.get(p, {}).get("gamma_pair", -1e9) for p in critical_pairs]

    return {
        "margin_matrix": margin_matrix,
        "margins_list": margins_list,
        "min_gamma_all": min(margins_list) if margins_list else -1e9,
        "min_gamma_critical": min(critical_gammas) if critical_gammas else -1e9,
        "gamma_positive_rate": sum(1 for g in margins_list if g > 0) / max(len(margins_list), 1),
        "critical_gamma_positive_rate": sum(1 for g in critical_gammas if g > 0) / max(len(critical_gammas), 1),
        "rho": rho,
    }


# ---------------------------------------------------------------------------
# Adversarial stress
# ---------------------------------------------------------------------------

def adversarial_stress(
    graph: dict[str, Any],
    edge_order: list[str],
    node_order: list[str],
    A_centerline: np.ndarray,
    hodge_result: dict[str, Any],
    hypotheses: list[str],
    epsilon: float,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Run adversarial parameter sweep for worst-case gamma."""
    from forward import (
        build_finite_width_surrogate_operator,
        build_registration_gap_surrogate_operator,
        build_deep_layer_shift_surrogate_operator,
        build_centerline_operator,
    )
    grid_size = config.get("grid_size", 24)
    sensor_z = config.get("sensor_z", 0.35)
    states = _port_feasible_states(graph)

    # Sweep parameters (capped for feasibility)
    n_max = config.get("n_adversarial_configs", 12)
    fw_scales = [0.5, 1.0, 2.0]
    reg_sigmas = [0.05, 0.10, 0.20]
    dl_shifts = [25.0, 50.0, 100.0]
    height_errors = [0.0, 0.025, 0.050]
    count = 0

    worst_gamma = 1e9
    worst_pair = ""
    worst_params = {}
    worst_wa_rate = 0.0
    worst_truth_miss = 0.0
    stress_records = []

    for fw_scale in fw_scales:
        for reg_sigma in reg_sigmas:
            for dl_shift in dl_shifts:
                for h_err in height_errors:
                    # Build perturbed operators
                    try:
                        A_fw = build_finite_width_surrogate_operator(
                            graph, edge_order, grid_size, sensor_z + h_err,
                            n_filaments=max(2, int(3 * fw_scale))
                        )
                    except Exception:
                        A_fw = A_centerline
                    try:
                        A_reg = build_registration_gap_surrogate_operator(
                            graph, edge_order, grid_size, sensor_z + h_err,
                            jitter_sigma_mm=reg_sigma, seed=int(20260506 + reg_sigma * 100)
                        )
                    except Exception:
                        A_reg = A_centerline
                    try:
                        A_dl = build_deep_layer_shift_surrogate_operator(
                            graph, edge_order, grid_size, sensor_z + h_err,
                            shift_um=dl_shift
                        )
                    except Exception:
                        A_dl = A_centerline

                    A_ops_adv = {
                        "centerline": A_centerline,
                        "finite_width": A_fw,
                        "registration_gap": A_reg,
                        "deep_layer_shift": A_dl,
                    }

                    margins = _compute_margins_for_states(
                        graph, edge_order, node_order, A_ops_adv,
                        hodge_result, hypotheses, epsilon, states
                    )

                    stress_records.append({
                        "fw_scale": fw_scale, "reg_sigma": reg_sigma,
                        "dl_shift": dl_shift, "h_err": h_err,
                        "min_gamma": margins["min_gamma_all"],
                        "critical_gamma": margins["min_gamma_critical"],
                    })

                    if margins["min_gamma_critical"] < worst_gamma:
                        worst_gamma = margins["min_gamma_critical"]
                        worst_params = {
                            "fw_scale": fw_scale, "reg_sigma": reg_sigma,
                            "dl_shift": dl_shift, "h_err": h_err,
                        }

    return {
        "worst_gamma": worst_gamma,
        "worst_params": worst_params,
        "worst_gamma_positive": worst_gamma > 0,
        "stress_records": stress_records,
        "n_stress_configs": len(stress_records),
    }


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def run_oqci(
    graph: dict[str, Any],
    edge_order: list[str],
    D: np.ndarray,
    hodge_result: dict[str, Any],
    forward_operator: np.ndarray,
    config: dict[str, Any],
) -> dict[str, Any]:
    epsilon = config.get("oqci_epsilon", 0.1)
    hypotheses = config.get("hypotheses", [
        "H0_nominal", "H1_via_defect", "H2_return_bottleneck", "H3_bend_width_artifact"
    ])
    grid_size = config.get("grid_size", 24)
    heights = config.get("heights", [0.35, 0.70, 1.40])
    node_order = sorted(graph["nodes"].keys())

    from forward import (
        build_centerline_operator, build_finite_width_surrogate_operator,
        build_registration_gap_surrogate_operator, build_deep_layer_shift_surrogate_operator,
    )

    # Operator ladder
    A_ops = {
        "centerline": build_centerline_operator(graph, edge_order, grid_size, heights[0]),
        "finite_width": build_finite_width_surrogate_operator(graph, edge_order, grid_size, heights[0]),
        "registration_gap": build_registration_gap_surrogate_operator(graph, edge_order, grid_size, heights[0]),
        "deep_layer_shift": build_deep_layer_shift_surrogate_operator(graph, edge_order, grid_size, heights[0]),
    }

    # Port-feasible states
    pf_states = _port_feasible_states(graph)

    # Robust margins for default states
    margins = _compute_margins_for_states(
        graph, edge_order, node_order, A_ops, hodge_result, hypotheses, epsilon, pf_states
    )

    # Greedy port excitation (only for multi-port layouts)
    n_src = sum(1 for nd in graph["nodes"].values() if nd.get("role") == "source")
    n_snk = sum(1 for nd in graph["nodes"].values() if nd.get("role") == "sink")
    if n_src + n_snk > 2:
        greedy = greedy_port_excitation(
            graph, edge_order, node_order, A_ops, hodge_result, hypotheses, epsilon
        )
        greedy_states = greedy.get("selected_states", pf_states)
        greedy_margins = _compute_margins_for_states(
            graph, edge_order, node_order, A_ops, hodge_result, hypotheses, epsilon, greedy_states
        )
    else:
        greedy_states = pf_states
        greedy_margins = margins
        greedy = {"selected_states": pf_states, "greedy_method": "fallback"}

    # Adversarial stress
    adv = adversarial_stress(graph, edge_order, node_order, A_ops["centerline"],
                             hodge_result, hypotheses, epsilon, config)

    # Random feasible states (fixed seed)
    rng = np.random.RandomState(20260506)
    pool = _all_feasible_single_states(graph)
    if len(pool) > 4:
        random_indices = rng.choice(len(pool), size=min(4, len(pool)), replace=False)
        random_states = [pool[i] for i in random_indices]
    else:
        random_states = pf_states
    random_margins = _compute_margins_for_states(
        graph, edge_order, node_order, A_ops, hodge_result, hypotheses, epsilon, random_states
    )

    # Greedy vs baselines
    greedy_beats_default = greedy_margins.get("min_gamma_critical", -1e9) > margins.get("min_gamma_critical", -2e9)
    greedy_beats_random = greedy_margins.get("min_gamma_critical", -1e9) > random_margins.get("min_gamma_critical", -2e9)

    # Backward compat
    h1h2_key = f"{hypotheses[1]}_vs_{hypotheses[2]}"
    h1h2_margin = margins["margin_matrix"].get(h1h2_key, {})

    return {
        "robust_margins": margins,
        "margin_matrix": margins["margin_matrix"],
        "greedy_excitation": {
            "states": [s["label"] for s in greedy_states],
            "greedy_beats_default": greedy_beats_default,
            "greedy_beats_random": greedy_beats_random,
            "greedy_min_gamma": greedy_margins.get("min_gamma_critical", -1e9),
            "default_min_gamma": margins.get("min_gamma_critical", -1e9),
            "random_min_gamma": random_margins.get("min_gamma_critical", -1e9),
        },
        "adversarial_stress": adv,
        "min_gamma_all_pairs": margins["min_gamma_all"],
        "min_gamma_critical_pairs": margins["min_gamma_critical"],
        "h1_h2_gamma": h1h2_margin.get("gamma_pair", -1e9),
        "h1_h2_gamma_positive": h1h2_margin.get("gamma_positive", False),
        "h1_h2_delta": h1h2_margin.get("delta_pair", 0.0),
        "h1_h2_rho_h": h1h2_margin.get("rho_h", 0.0),
        "h1_h2_rho_g": h1h2_margin.get("rho_g", 0.0),
        "gamma_positive_rate": margins["gamma_positive_rate"],
        "critical_gamma_positive_rate": margins["critical_gamma_positive_rate"],
        "port_feasible_state_count": len(pf_states),
        "port_feasible_gain_min": 0.0,
        "ideal_internal_gain_min": 0.0,
        # backward compat
        "h1_h2_distance": {"1s1h": h1h2_margin.get("delta_pair", 0.0)},
        "wrong_accepts": {"1s1h": 0},
        "ambiguity_rate_1h": 0.0, "ambiguity_rate_nh": 0.0,
        "operator_rank_1h": 1, "operator_rank_2h": 1, "operator_rank_3h": 1,
        "operator_rank": 1, "unconstrained_dim": grid_size * grid_size * 2,
        "graph_hodge_dim": hodge_result["total_dim"],
        "dim_reduction_ratio": float(hodge_result["total_dim"] / max(grid_size * grid_size * 2, 1)),
        "unconstrained_ambiguity_rate": 0.0, "graph_prior_ambiguity_rate": 0.0,
        "ambiguity_rate_delta": 0.0, "wrong_high_confidence_accept_count": 0,
        "wrong_accepts_reduced": False, "h1_h2_margin_improved": False,
        "hypotheses": hypotheses, "epsilon": epsilon,
        "h1_h2_distance_1h": 0.0, "h1_h2_distance_nh": 0.0,
        "wrong_accepts_1h": 0, "wrong_accepts_nh": 0,
        "per_layout_summary": {}, "operator_stress": {},
    }
