from __future__ import annotations

from dataclasses import replace
from typing import Mapping

import numpy as np

from .types import CaseRecord, Segment


def _parallel_offset_segment(segment: Segment, offset_m: float, suffix: str, prior_group: str | None = None) -> Segment:
    start = np.asarray(segment.start, dtype=float)
    end = np.asarray(segment.end, dtype=float)
    d = end[:2] - start[:2]
    n = float(np.linalg.norm(d))
    if n < 1e-15:
        perp = np.asarray([1.0, 0.0])
    else:
        perp = np.asarray([-d[1], d[0]]) / n
    delta = float(offset_m) * perp
    return Segment(
        name=f"{segment.name}__{suffix}",
        layer=segment.layer,
        kind=segment.kind,
        start=(float(start[0] + delta[0]), float(start[1] + delta[1]), float(start[2])),
        end=(float(end[0] + delta[0]), float(end[1] + delta[1]), float(end[2])),
        prior_group=prior_group or segment.prior_group,
    )


def _shift_segment_xy(segment: Segment, dx: float, dy: float, suffix: str) -> Segment:
    return Segment(
        name=f"{segment.name}__{suffix}",
        layer=segment.layer,
        kind=segment.kind,
        start=(float(segment.start[0] + dx), float(segment.start[1] + dy), float(segment.start[2])),
        end=(float(segment.end[0] + dx), float(segment.end[1] + dy), float(segment.end[2])),
        prior_group=segment.prior_group,
    )


def _local_artifact_at(point_xy: tuple[float, float], z: float, length_m: float, idx: int) -> Segment:
    half = 0.5 * float(length_m)
    return Segment(
        name=f"pypeec_local_artifact_{idx:03d}",
        layer="PYPEEC_ARTIFACT",
        kind="artifact",
        start=(float(point_xy[0] - half), float(point_xy[1] - half), float(z)),
        end=(float(point_xy[0] + half), float(point_xy[1] + half), float(z)),
        prior_group="artifact",
    )


def augment_record_for_pypeec_basis(record: CaseRecord, cfg: Mapping, mode: str) -> CaseRecord:
    """Return a fixed PyPEEC-aware graph-basis variant.

    These are intentionally simple graph-level basis-bank diagnostics.  They do
    not import CAD geometry and do not use PyPEEC labels for selection.
    """

    basis_cfg = cfg.get("pypeec_aware_basis", {})
    trace_half_width = float(basis_cfg.get("trace_half_width_m", 30e-6))
    return_offset = float(basis_cfg.get("return_offset_m", 120e-6))
    via_spread = float(basis_cfg.get("via_spread_m", 60e-6))
    artifact_length = float(basis_cfg.get("artifact_length_m", 80e-6))

    sheet = list(record.sheet_segments)
    vias = list(record.via_candidates)
    returns = list(record.return_candidates)
    artifacts = list(record.artifact_candidates)

    if mode in {"finite_width_sheet", "combined_pypeec_aware"}:
        for seg in record.sheet_segments:
            sheet.append(_parallel_offset_segment(seg, trace_half_width, "fw_pos"))
            sheet.append(_parallel_offset_segment(seg, -trace_half_width, "fw_neg"))

    if mode in {"return_bank", "combined_pypeec_aware"}:
        for seg in record.return_candidates:
            returns.append(_parallel_offset_segment(seg, return_offset, "ret_pos"))
            returns.append(_parallel_offset_segment(seg, -return_offset, "ret_neg"))

    if mode in {"distributed_via", "combined_pypeec_aware"}:
        offsets = [(via_spread, 0.0), (-via_spread, 0.0), (0.0, via_spread), (0.0, -via_spread)]
        for seg in record.via_candidates:
            for idx, (dx, dy) in enumerate(offsets):
                vias.append(_shift_segment_xy(seg, dx, dy, f"spread_{idx}"))

    if mode in {"artifact_bank", "combined_pypeec_aware"}:
        idx = 0
        for seg in record.sheet_segments:
            for pt in [seg.start, seg.end]:
                artifacts.append(_local_artifact_at((float(pt[0]), float(pt[1])), float(pt[2]) - 20e-6, artifact_length, idx))
                idx += 1

    return replace(
        record,
        sheet_segments=sheet,
        via_candidates=vias,
        return_candidates=returns,
        artifact_candidates=artifacts,
    )

