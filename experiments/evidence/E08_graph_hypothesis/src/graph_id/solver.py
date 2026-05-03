from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Tuple

import numpy as np

from .forward import basis_matrix, flatten_field
from .types import CaseRecord, HypothesisResult, Segment


HYPOTHESIS_SEGMENTS = {
    "H0_sheet_only": ("sheet",),
    "H1_sheet_via": ("sheet", "via"),
    "H2_sheet_return": ("sheet", "return"),
    "H3_sheet_artifact": ("sheet", "artifact"),
}

EXTRA_GROUPS = {"via", "return", "artifact"}


def _segments_for(record: CaseRecord, hypothesis_name: str) -> List[Segment]:
    groups = HYPOTHESIS_SEGMENTS[hypothesis_name]
    out: List[Segment] = []
    if "sheet" in groups:
        out += list(record.sheet_segments)
    if "via" in groups:
        out += list(record.via_candidates)
    if "return" in groups:
        out += list(record.return_candidates)
    if "artifact" in groups:
        out += list(record.artifact_candidates)
    return out


def _ridge_fit(a: np.ndarray, y: np.ndarray, ridge_alpha: float) -> np.ndarray:
    if a.size == 0:
        return np.zeros((0,), dtype=float)
    lhs = a.T @ a + float(ridge_alpha) * np.eye(a.shape[1])
    rhs = a.T @ y
    return np.linalg.solve(lhs, rhs)


def fit_hypothesis(
    record: CaseRecord,
    hypothesis_name: str,
    obs_xyz: np.ndarray,
    cfg: Mapping,
    complexity_penalty: float,
) -> HypothesisResult:
    segments = _segments_for(record, hypothesis_name)
    a_norm, names, norms = basis_matrix(
        segments,
        obs_xyz,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )
    y = flatten_field(record.b_obs)
    coef_norm = _ridge_fit(a_norm, y, ridge_alpha=float(cfg["scoring"]["ridge_alpha"]))
    pred = a_norm @ coef_norm if len(coef_norm) else np.zeros_like(y)
    residual = y - pred
    residual_norm = float(np.linalg.norm(residual))
    y_norm = float(np.linalg.norm(y)) + 1e-30
    residual_rel = residual_norm / y_norm

    coefficients: Dict[str, float] = {}
    name_to_segment = {s.name: s for s in segments}
    n_extra = 0
    l1_extra = 0.0
    for name, c, norm in zip(names, coef_norm, norms):
        # Convert normalized coefficient back to current amplitude in amperes.
        physical_current = float(c / norm)
        coefficients[name] = physical_current
        seg = name_to_segment[name]
        if seg.prior_group in EXTRA_GROUPS:
            n_extra += 1
            l1_extra += abs(float(c))

    l1_penalty = float(cfg["scoring"]["extra_basis_l1_penalty"]) * l1_extra / (y_norm + 1e-30)
    complexity = float(complexity_penalty) * float(n_extra)
    score = residual_rel + complexity + l1_penalty
    return HypothesisResult(
        name=hypothesis_name,
        score=float(score),
        residual_rel_l2=float(residual_rel),
        coefficients=coefficients,
        n_basis=len(names),
        n_extra_basis=n_extra,
        residual_norm=residual_norm,
        complexity_penalty=complexity,
        l1_penalty=l1_penalty,
    )


def score_hypotheses(
    record: CaseRecord,
    obs_xyz: np.ndarray,
    cfg: Mapping,
    complexity_penalty: float,
) -> Dict[str, HypothesisResult]:
    return {
        h: fit_hypothesis(record, h, obs_xyz, cfg, complexity_penalty=complexity_penalty)
        for h in cfg["scoring"]["hypotheses"]
    }


def best_hypothesis(results: Mapping[str, HypothesisResult]) -> str:
    return min(results.values(), key=lambda r: r.score).name


def via_evidence(results: Mapping[str, HypothesisResult]) -> float:
    """Positive values indicate H1 explains the field better than H0."""

    return float(results["H0_sheet_only"].score - results["H1_sheet_via"].score)


def return_evidence(results: Mapping[str, HypothesisResult]) -> float:
    return float(results["H0_sheet_only"].score - results["H2_sheet_return"].score)


def artifact_evidence(results: Mapping[str, HypothesisResult]) -> float:
    return float(results["H0_sheet_only"].score - results["H3_sheet_artifact"].score)


def score_margin(results: Mapping[str, HypothesisResult]) -> float:
    ordered = sorted((r.score for r in results.values()))
    if len(ordered) < 2:
        return 0.0
    return float(ordered[1] - ordered[0])
