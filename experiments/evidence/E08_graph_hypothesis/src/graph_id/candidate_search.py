from __future__ import annotations

from dataclasses import replace
from typing import Mapping, Sequence

import numpy as np

from .solver import best_hypothesis, score_hypotheses, score_margin, via_evidence
from .types import CaseRecord, HypothesisResult, Segment


def offset_grid(radius_m: float, n_side: int) -> list[tuple[float, float]]:
    """Return a deterministic square xy-offset grid for candidate marginalization."""

    if n_side <= 1 or radius_m <= 0:
        return [(0.0, 0.0)]
    vals = np.linspace(-float(radius_m), float(radius_m), int(n_side))
    offsets = [(float(dx), float(dy)) for dx in vals for dy in vals]
    offsets.sort(key=lambda xy: (xy[0] * xy[0] + xy[1] * xy[1], xy[0], xy[1]))
    return offsets


def shift_segment_xy(segment: Segment, dx: float, dy: float) -> Segment:
    return Segment(
        name=f"{segment.name}__dx{dx:.3e}_dy{dy:.3e}",
        layer=segment.layer,
        kind=segment.kind,
        start=(segment.start[0] + dx, segment.start[1] + dy, segment.start[2]),
        end=(segment.end[0] + dx, segment.end[1] + dy, segment.end[2]),
        prior_group=segment.prior_group,
    )


def transform_grid(translation_radius_m: float, rotation_degrees: Sequence[float], scales: Sequence[float]) -> list[dict]:
    """Return a small deterministic global graph-registration search grid.

    The grid intentionally stays tiny because every transform re-fits all graph
    hypotheses.  It is a diagnostic for global CAD-to-sensor registration, not
    a full image-registration optimizer.
    """

    r = float(translation_radius_m)
    translations = [(0.0, 0.0)]
    if r > 0:
        translations += [(r, 0.0), (-r, 0.0), (0.0, r), (0.0, -r)]
    transforms: list[dict] = [{"dx_m": 0.0, "dy_m": 0.0, "rotation_deg": 0.0, "scale": 1.0}]
    transforms += [
        {"dx_m": float(dx), "dy_m": float(dy), "rotation_deg": 0.0, "scale": 1.0}
        for dx, dy in translations
        if abs(dx) + abs(dy) > 0
    ]
    transforms += [
        {"dx_m": 0.0, "dy_m": 0.0, "rotation_deg": float(deg), "scale": 1.0}
        for deg in rotation_degrees
        if abs(float(deg)) > 1e-12
    ]
    transforms += [
        {"dx_m": 0.0, "dy_m": 0.0, "rotation_deg": 0.0, "scale": float(scale)}
        for scale in scales
        if abs(float(scale) - 1.0) > 1e-12
    ]
    transforms.sort(
        key=lambda t: (
            abs(t["dx_m"]) + abs(t["dy_m"]) + abs(t["rotation_deg"]) * 1e-5 + abs(t["scale"] - 1.0) * 1e-3,
            t["dx_m"],
            t["dy_m"],
            t["rotation_deg"],
            t["scale"],
        )
    )
    return transforms


def transform_segment_xy(segment: Segment, dx: float, dy: float, rotation_rad: float, scale: float) -> Segment:
    """Apply a global xy transform around the field origin and keep z fixed."""

    c = float(np.cos(rotation_rad))
    s = float(np.sin(rotation_rad))

    def _xy(pt):
        x = float(pt[0]) * float(scale)
        y = float(pt[1]) * float(scale)
        return (c * x - s * y + float(dx), s * x + c * y + float(dy), float(pt[2]))

    return Segment(
        name=f"{segment.name}__gdx{dx:.2e}_gdy{dy:.2e}_rot{rotation_rad:.2e}_s{scale:.3f}",
        layer=segment.layer,
        kind=segment.kind,
        start=_xy(segment.start),
        end=_xy(segment.end),
        prior_group=segment.prior_group,
    )


def transform_record_geometry(record: CaseRecord, transform: Mapping[str, float]) -> CaseRecord:
    dx = float(transform.get("dx_m", 0.0))
    dy = float(transform.get("dy_m", 0.0))
    rotation_rad = np.deg2rad(float(transform.get("rotation_deg", 0.0)))
    scale = float(transform.get("scale", 1.0))
    return replace(
        record,
        sheet_segments=[transform_segment_xy(seg, dx, dy, rotation_rad, scale) for seg in record.sheet_segments],
        via_candidates=[transform_segment_xy(seg, dx, dy, rotation_rad, scale) for seg in record.via_candidates],
        return_candidates=[transform_segment_xy(seg, dx, dy, rotation_rad, scale) for seg in record.return_candidates],
        artifact_candidates=[transform_segment_xy(seg, dx, dy, rotation_rad, scale) for seg in record.artifact_candidates],
    )


def _with_shifted_vias(record: CaseRecord, dx: float, dy: float) -> CaseRecord:
    return replace(record, via_candidates=[shift_segment_xy(seg, dx, dy) for seg in record.via_candidates])


def score_with_via_location_marginalization(
    record: CaseRecord,
    obs_xyz: np.ndarray,
    cfg: Mapping,
    complexity_penalty: float,
    offsets: Sequence[tuple[float, float]],
) -> dict:
    """Score H0/H2/H3 once and H1 over an xy-offset candidate grid.

    This is a registration-uncertainty diagnostic. It does not tune offsets on
    PyPEEC labels; the offset grid is fixed by configuration and applied
    uniformly to validation, synthetic stress, and bridge datasets.
    """

    base_results = score_hypotheses(record, obs_xyz, cfg, complexity_penalty=complexity_penalty)
    best_h1: HypothesisResult = base_results["H1_sheet_via"]
    best_offset = (0.0, 0.0)
    for dx, dy in offsets:
        shifted = _with_shifted_vias(record, dx, dy)
        shifted_results = score_hypotheses(shifted, obs_xyz, cfg, complexity_penalty=complexity_penalty)
        candidate = shifted_results["H1_sheet_via"]
        if candidate.score < best_h1.score:
            best_h1 = candidate
            best_offset = (float(dx), float(dy))
    combined = dict(base_results)
    combined["H1_sheet_via"] = best_h1
    pred = best_hypothesis(combined)
    return {
        "pred_hypothesis": pred,
        "via_evidence": via_evidence(combined),
        "confidence_margin": score_margin(combined),
        "results": combined,
        "best_via_offset_m": best_offset,
        "best_via_offset_norm_m": float(np.hypot(best_offset[0], best_offset[1])),
    }


def score_with_global_registration_search(
    record: CaseRecord,
    obs_xyz: np.ndarray,
    cfg: Mapping,
    complexity_penalty: float,
    transforms: Sequence[Mapping[str, float]],
) -> dict:
    """Search a fixed global graph-registration bank and score the best fit."""

    best_results: dict[str, HypothesisResult] | None = None
    best_transform: Mapping[str, float] | None = None
    best_score = float("inf")
    for transform in transforms:
        transformed = transform_record_geometry(record, transform)
        results = score_hypotheses(transformed, obs_xyz, cfg, complexity_penalty=complexity_penalty)
        pred = best_hypothesis(results)
        score = float(results[pred].score)
        if score < best_score:
            best_score = score
            best_results = results
            best_transform = dict(transform)
    assert best_results is not None and best_transform is not None
    pred = best_hypothesis(best_results)
    return {
        "pred_hypothesis": pred,
        "via_evidence": via_evidence(best_results),
        "confidence_margin": score_margin(best_results),
        "results": best_results,
        "best_global_transform": dict(best_transform),
        "best_global_translation_norm_m": float(np.hypot(best_transform["dx_m"], best_transform["dy_m"])),
        "best_global_rotation_abs_deg": abs(float(best_transform["rotation_deg"])),
        "best_global_scale_delta": abs(float(best_transform["scale"]) - 1.0),
    }
