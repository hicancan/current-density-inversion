"""Graph-Hodge-inspired basis construction for minimal OBGHI.

This is not a full discrete exterior calculus implementation. It is a minimal
basis compiler that gives each topology a physically interpretable low-rank
subspace:

- graph modes: smooth sheet/net currents;
- via modes: candidate vertical source/sink currents;
- gap modes: direct observation residuals for calibration/model mismatch;
- return modes: deep return-loop currents.

The observable compression step follows the OBGHI blueprint principle: keep only
modes with enough magnetic observation energy relative to the strongest mode.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from operators import OperatorBundle, empty_current, add_gaussian_sheet_mode, add_via_spot, add_return_loop


HYPOTHESES = ["H0_no_via", "H1_via", "H2_model_gap", "H3_return_path"]


@dataclass
class BasisBlock:
    name: str
    kind: str
    matrix: np.ndarray
    prior_variance: float
    is_current_basis: bool


@dataclass
class HypothesisBasis:
    hypothesis: str
    B: np.ndarray
    blocks: list[BasisBlock]
    kept_columns: list[str]
    dropped_columns: list[str]
    current_basis: np.ndarray
    current_column_names: list[str]


def _candidate_centers(n: int) -> list[tuple[int, int]]:
    q1 = n // 3
    q2 = (2 * n) // 3
    c = n // 2
    return [(c, c), (q1, q1), (q2, q1), (q1, q2), (q2, q2)]


def graph_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for layer in range(int(bundle.index["layers"])):
        for comp in ["x", "y"]:
            for cx, cy in [(n / 2, n / 2), (n / 3, n / 3), (2 * n / 3, n / 3), (n / 3, 2 * n / 3)]:
                x = empty_current(bundle)
                add_gaussian_sheet_mode(x, bundle, layer, comp, (cx, cy), max(1.8, n / 5.0), 1.0)
                cols.append(x)
    H = np.stack(cols, axis=1)
    return BasisBlock("graph_smooth_sheet_modes", "graph", H, prior_var, True)


def via_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for layer in range(int(bundle.index["layers"]) - 1):
        for center in _candidate_centers(n):
            x = empty_current(bundle)
            add_via_spot(x, bundle, layer, layer + 1, center, 1.0, radius=0)
            # Soft source/sink compensation modes on adjacent sheet layers.
            add_gaussian_sheet_mode(x, bundle, layer, "x", center, max(1.5, n / 7.0), 0.25)
            add_gaussian_sheet_mode(x, bundle, layer + 1, "x", center, max(1.5, n / 7.0), -0.25)
            cols.append(x)
    H = np.stack(cols, axis=1)
    return BasisBlock("candidate_via_source_sink_modes", "via", H, prior_var, True)


def return_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    cols = []
    for layer in [int(bundle.index["layers"]) - 1, max(0, int(bundle.index["layers"]) - 2)]:
        x = empty_current(bundle)
        add_return_loop(x, bundle, layer, 1.0)
        cols.append(x)
        x2 = empty_current(bundle)
        add_return_loop(x2, bundle, layer, -1.0)
        cols.append(x2)
    H = np.stack(cols, axis=1)
    return BasisBlock("deep_return_loop_modes", "return", H, prior_var, True)


def residual_current_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for layer in [0, int(bundle.index["layers"]) - 1]:
        for comp in ["x", "y"]:
            x = empty_current(bundle)
            add_gaussian_sheet_mode(x, bundle, layer, comp, (n / 2, n / 2), max(1.0, n / 8.0), 1.0)
            cols.append(x)
    H = np.stack(cols, axis=1)
    return BasisBlock("small_residual_current_modes", "residual", H, prior_var, True)


def _gaussian_field_pattern(bundle: OperatorBundle, center: tuple[float, float], sigma_cells: float, channel: int) -> np.ndarray:
    n = int(bundle.index["n"])
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    g -= np.mean(g)
    out = np.zeros((3, n, n), dtype=float)
    out[channel] = g
    return out.reshape(-1)


def gap_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    centers = [(n / 2, n / 2), (n / 3, n / 2), (2 * n / 3, n / 2), (n / 2, n / 3), (n / 2, 2 * n / 3)]
    cols = []
    for channel in [0, 1, 2]:
        for center in centers:
            cols.append(_gaussian_field_pattern(bundle, center, max(1.5, n / 6.0), channel))
    U = np.stack(cols, axis=1)
    return BasisBlock("direct_model_gap_field_modes", "gap", U, prior_var, False)


def _forward_block(bundle: OperatorBundle, block: BasisBlock) -> np.ndarray:
    if block.is_current_basis:
        return bundle.A @ block.matrix
    return block.matrix


def _observable_filter(B: np.ndarray, names: list[str], threshold_ratio: float) -> tuple[np.ndarray, list[str], list[str]]:
    norms = np.linalg.norm(B, axis=0)
    if B.shape[1] == 0:
        return B, [], []
    max_norm = float(np.max(norms))
    if max_norm <= 0:
        return B[:, :0], [], names
    keep = norms >= threshold_ratio * max_norm
    kept_names = [name for name, k in zip(names, keep) if k]
    dropped_names = [name for name, k in zip(names, keep) if not k]
    return B[:, keep], kept_names, dropped_names


def build_hypothesis_basis(bundle: OperatorBundle, cfg: dict, hypothesis: str) -> HypothesisBasis:
    if hypothesis not in HYPOTHESES:
        raise ValueError(f"Unknown hypothesis: {hypothesis}")
    pv = cfg["prior_variance"]
    threshold_ratio = float(cfg["observable_energy_ratio_threshold"])

    blocks: list[BasisBlock] = [
        graph_basis(bundle, float(pv["graph"])),
        residual_current_basis(bundle, float(pv["residual"])),
    ]
    if hypothesis == "H1_via":
        blocks.append(via_basis(bundle, float(pv["via"])))
    elif hypothesis == "H2_model_gap":
        blocks.append(gap_basis(bundle, float(pv["gap"])))
    elif hypothesis == "H3_return_path":
        blocks.append(return_basis(bundle, float(pv["return"])))

    B_parts: list[np.ndarray] = []
    kept: list[str] = []
    dropped: list[str] = []
    current_parts: list[np.ndarray] = []
    current_names: list[str] = []

    for block in blocks:
        raw = _forward_block(bundle, block)
        names = [f"{block.kind}:{block.name}:{i}" for i in range(raw.shape[1])]
        B_keep, kept_names, dropped_names = _observable_filter(raw, names, threshold_ratio)
        B_parts.append(B_keep)
        kept.extend(kept_names)
        dropped.extend(dropped_names)
        if block.is_current_basis:
            # Keep the same columns in current basis as survived in observation space.
            raw_norms = np.linalg.norm(raw, axis=0)
            if raw_norms.size:
                keep_mask = raw_norms >= threshold_ratio * max(float(np.max(raw_norms)), 1e-30)
                current_parts.append(block.matrix[:, keep_mask])
                current_names.extend([n for n, k in zip(names, keep_mask) if k])

    B = np.concatenate(B_parts, axis=1) if B_parts else np.zeros((bundle.A.shape[0], 0))
    current_basis = np.concatenate(current_parts, axis=1) if current_parts else np.zeros((bundle.A.shape[1], 0))
    return HypothesisBasis(
        hypothesis=hypothesis,
        B=B,
        blocks=blocks,
        kept_columns=kept,
        dropped_columns=dropped,
        current_basis=current_basis,
        current_column_names=current_names,
    )


def build_all_hypothesis_bases(bundle: OperatorBundle, cfg: dict) -> dict[str, HypothesisBasis]:
    return {h: build_hypothesis_basis(bundle, cfg, h) for h in HYPOTHESES}


def subspace_principal_angle_deg(A: np.ndarray, B: np.ndarray, eps: float = 1e-12) -> float:
    """Return smallest principal angle in degrees between column spaces."""
    if A.size == 0 or B.size == 0 or A.shape[1] == 0 or B.shape[1] == 0:
        return 90.0
    qa, _ = np.linalg.qr(A)
    qb, _ = np.linalg.qr(B)
    s = np.linalg.svd(qa.T @ qb, compute_uv=False)
    if s.size == 0:
        return 90.0
    c = float(np.clip(np.max(s), -1.0, 1.0))
    return float(np.degrees(np.arccos(c + 0.0)))


def via_gap_angle(bundle: OperatorBundle, cfg: dict) -> float:
    via = via_basis(bundle, float(cfg["prior_variance"]["via"]))
    gap = gap_basis(bundle, float(cfg["prior_variance"]["gap"]))
    B_via = bundle.A @ via.matrix
    B_gap = gap.matrix
    return subspace_principal_angle_deg(B_via, B_gap)
