"""Topology hypothesis conductance models for E28.

Each hypothesis defines a conductance matrix C_h (diagonal, E x E) that
determines how the graph Laplacian and transfer matrix differ between hypotheses.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from operators import OperatorBundle

HYPOTHESES = ["H0_no_via", "H1_via", "H2_model_gap", "H3_return_path"]


@dataclass
class ConductanceModel:
    hypothesis: str
    C: np.ndarray
    g_sheet: float
    g_via: float
    g_bottom_enhance: float
    label: str


def _edge_group_masks(bundle: OperatorBundle) -> dict[str, np.ndarray]:
    """Return boolean masks for each edge group."""
    idx = bundle.index
    E = bundle.edge_count
    masks = {}

    # Jx edges
    jx_mask = np.zeros(E, dtype=bool)
    jx_mask[idx["jx_start"]:idx["jx_start"] + idx["jx_count"]] = True
    masks["jx"] = jx_mask

    # Jy edges
    jy_mask = np.zeros(E, dtype=bool)
    jy_mask[idx["jy_start"]:idx["jy_start"] + idx["jy_count"]] = True
    masks["jy"] = jy_mask

    # Via edges
    vz_mask = np.zeros(E, dtype=bool)
    vz_mask[idx["vz_start"]:idx["vz_start"] + idx["vz_count"]] = True
    masks["vz"] = vz_mask

    # Sheet edges (Jx + Jy)
    masks["sheet"] = masks["jx"] | masks["jy"]

    # Bottom layer sheet edges
    n = int(idx["n"])
    cell_count = int(idx["cell_count"])
    layers = int(idx["layers"])
    bot_layer = layers - 1

    bot_mask = np.zeros(E, dtype=bool)
    for comp in ["x", "y"]:
        sl = idx["sheet_slices"][(bot_layer, comp)]
        bot_mask[sl] = True
    masks["bottom_sheet"] = bot_mask

    return masks


def build_conductance_model(
    bundle: OperatorBundle, cfg: dict, hypothesis: str
) -> ConductanceModel:
    """Build the conductance matrix C_h for a given hypothesis.

    C_h is a diagonal matrix where each entry is the conductance of an edge.
    Differences between hypotheses come from:
    - H0: via conductances are near-zero
    - H1: via conductances are nominal
    - H2: same as H1 (model gap is in observation, not topology)
    - H3: enhanced bottom-layer sheet conductances (return paths)
    """
    if hypothesis not in HYPOTHESES:
        raise ValueError(f"Unknown hypothesis: {hypothesis}")

    E = bundle.edge_count
    g_sheet = float(cfg["g_sheet"])
    g_via_nominal = float(cfg["g_via_nominal"])
    g_via_h0 = float(cfg["g_via_h0"])
    g_return_enhance = float(cfg["g_return_enhance"])
    g_return_suppress = float(cfg["g_return_suppress"])

    masks = _edge_group_masks(bundle)

    c_vec = np.full(E, g_sheet, dtype=float)
    via_mask = masks["vz"]
    bot_mask = masks["bottom_sheet"]

    if hypothesis == "H0_no_via":
        c_vec[via_mask] = g_via_h0
    elif hypothesis == "H1_via":
        c_vec[via_mask] = g_via_nominal
    elif hypothesis == "H2_model_gap":
        # Model gap perturbs inferred conductance: via conductance lowered
        # to simulate registration/standoff mismatch effects on apparent topology
        c_vec[via_mask] = g_via_nominal * 0.82
        # Add small perturbation to sheet conductances (drift)
        rng = np.random.default_rng(42)
        sheet_mask = masks["sheet"]
        c_vec[sheet_mask] = g_sheet * (1.0 + 0.03 * rng.normal(size=int(np.sum(sheet_mask))))
    elif hypothesis == "H3_return_path":
        c_vec[via_mask] = g_via_nominal * g_return_suppress
        c_vec[bot_mask] = g_sheet * g_return_enhance

    C = np.diag(c_vec)

    return ConductanceModel(
        hypothesis=hypothesis,
        C=C,
        g_sheet=g_sheet,
        g_via=float(c_vec[via_mask][0]) if np.any(via_mask) else 0.0,
        g_bottom_enhance=float(np.mean(c_vec[bot_mask]) / g_sheet) if np.any(bot_mask) else 1.0,
        label=hypothesis,
    )


def build_all_conductance_models(
    bundle: OperatorBundle, cfg: dict
) -> dict[str, ConductanceModel]:
    return {h: build_conductance_model(bundle, cfg, h) for h in HYPOTHESES}
