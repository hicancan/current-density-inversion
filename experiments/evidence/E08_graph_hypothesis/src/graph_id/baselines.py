from __future__ import annotations

from typing import Mapping

import numpy as np

from .forward import basis_matrix, flatten_field
from .types import CaseRecord


def via_template_peak_score(record: CaseRecord, obs_xyz: np.ndarray, cfg: Mapping) -> float:
    """A deliberately simple pixel/residual-free baseline.

    It projects the full observed field onto the candidate via template without
    first explaining sheet/return/artifact currents. This mimics the failure mode
    of raw residual-via thresholding: bends and returns can look via-like.
    """

    a, _, _ = basis_matrix(
        list(record.via_candidates),
        obs_xyz,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )
    if a.shape[1] == 0:
        return 0.0
    y = flatten_field(record.b_obs)
    return float(abs(a[:, 0].T @ y) / (np.linalg.norm(y) + 1e-30))


def sheet_residual_via_score(record: CaseRecord, obs_xyz: np.ndarray, cfg: Mapping) -> float:
    """A stronger but still pixel-style residual baseline.

    It first fits sheet-only currents, then projects the residual onto the via
    template. This is close in spirit to exp04's residual-via detector, but it
    lacks return/artifact hypotheses and therefore tends to confuse such cases
    with true vias.
    """

    from .solver import fit_hypothesis

    h0 = fit_hypothesis(record, "H0_sheet_only", obs_xyz, cfg, complexity_penalty=0.0)
    # Rebuild sheet prediction from fitted physical coefficients.
    from .forward import field_from_segments

    pred = field_from_segments(
        record.sheet_segments,
        h0.coefficients,
        obs_xyz,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )
    residual = record.b_obs - pred
    a, _, _ = basis_matrix(
        list(record.via_candidates),
        obs_xyz,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )
    if a.shape[1] == 0:
        return 0.0
    y = flatten_field(residual)
    return float(abs(a[:, 0].T @ y) / (np.linalg.norm(flatten_field(record.b_obs)) + 1e-30))
