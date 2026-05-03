from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from .types import CaseRecord, Segment


def _is_vertical(seg: dict[str, Any]) -> bool:
    start = np.asarray(seg["start"], dtype=float)
    end = np.asarray(seg["end"], dtype=float)
    delta = np.abs(end - start)
    return bool(delta[2] > max(float(delta[0]), float(delta[1]), 1e-15))


def _as_segment(seg: dict[str, Any], prior_group: str, idx: int) -> Segment:
    kind = "via" if _is_vertical(seg) else ("return" if prior_group == "return" else ("artifact" if prior_group == "artifact" else "edge"))
    return Segment(
        name=f"{prior_group}_{idx}_{seg.get('tag', 'segment')}",
        layer=str(seg.get("layer", "")),
        kind=kind,
        start=tuple(float(x) for x in seg["start"]),
        end=tuple(float(x) for x in seg["end"]),
        prior_group=prior_group,
    )


def _classify_exp07_case(meta: dict[str, Any]) -> tuple[str, str]:
    physics = meta.get("expected_physics", {})
    route_kind = str(physics.get("route_kind", ""))
    if bool(physics.get("artifact_like", False)) or route_kind in {"bend_artifact", "corner_artifact"}:
        return "bend_artifact", "H3_sheet_artifact"
    if bool(physics.get("return_path", False)) or route_kind == "return_path":
        return "return_path", "H2_sheet_return"
    if physics.get("has_via") is False or route_kind == "no_via_background":
        return "no_via", "H0_sheet_only"
    if any(_is_vertical(seg) for seg in meta.get("segments", [])):
        return "true_via", "H1_sheet_via"
    return "no_via", "H0_sheet_only"


def _fallback_via_candidate(meta: dict[str, Any]) -> Segment:
    pts = np.asarray([p for seg in meta["segments"] for p in [seg["start"], seg["end"]]], dtype=float)
    xy = pts[:, :2].mean(axis=0)
    z_top = float(np.max(pts[:, 2]))
    z_bot = float(np.min(pts[:, 2]))
    if abs(z_top - z_bot) < 1e-9:
        z_bot = z_top - 50e-6
    return Segment(
        name="candidate_via_fallback",
        layer="L1-L2",
        kind="via",
        start=(float(xy[0]), float(xy[1]), z_top),
        end=(float(xy[0]), float(xy[1]), z_bot),
        prior_group="via",
    )


def _fallback_return_candidate(meta: dict[str, Any]) -> Segment:
    pts = np.asarray([p for seg in meta["segments"] for p in [seg["start"], seg["end"]]], dtype=float)
    x0 = float(np.min(pts[:, 0]))
    x1 = float(np.max(pts[:, 0]))
    y = float(np.mean(pts[:, 1]) - 150e-6)
    z = float(np.min(pts[:, 2]) - 70e-6)
    return Segment(
        name="candidate_return_fallback",
        layer="RETURN",
        kind="return",
        start=(x1, y, z),
        end=(x0, y, z),
        prior_group="return",
    )


def _artifact_candidate(meta: dict[str, Any]) -> Segment:
    pts = np.asarray([p for seg in meta["segments"] for p in [seg["start"], seg["end"]]], dtype=float)
    xy = pts[:, :2].mean(axis=0)
    z = float(np.median(pts[:, 2]) - 25e-6)
    length = 80e-6
    return Segment(
        name="candidate_artifact_local",
        layer="ARTIFACT",
        kind="artifact",
        start=(float(xy[0] - 0.5 * length), float(xy[1] - 0.5 * length), z),
        end=(float(xy[0] + 0.5 * length), float(xy[1] + 0.5 * length), z),
        prior_group="artifact",
    )


def _split_segments(meta: dict[str, Any], hypothesis_label: str) -> tuple[list[Segment], list[Segment], list[Segment], list[Segment]]:
    sheet: list[Segment] = []
    via: list[Segment] = []
    ret: list[Segment] = []
    artifact: list[Segment] = []
    is_return_case = hypothesis_label == "H2_sheet_return"
    is_artifact_case = hypothesis_label == "H3_sheet_artifact"
    for idx, seg in enumerate(meta.get("segments", [])):
        tag = str(seg.get("tag", ""))
        if is_return_case and ("return" in tag or "lower" in tag or tag.startswith("right_via")):
            ret.append(_as_segment(seg, "return", idx))
        elif is_artifact_case and ("artifact" in tag or "corner" in tag or "bend" in tag):
            artifact.append(_as_segment(seg, "artifact", idx))
        elif _is_vertical(seg):
            via.append(_as_segment(seg, "via", idx))
        else:
            sheet.append(_as_segment(seg, "sheet", idx))
    if not via:
        via.append(_fallback_via_candidate(meta))
    if not ret:
        ret.append(_fallback_return_candidate(meta))
    if not artifact:
        artifact.append(_artifact_candidate(meta))
    return sheet, via, ret, artifact


def load_exp07_graph_bridge_records(npz_path: Path, field_key: str) -> tuple[list[CaseRecord], np.ndarray]:
    """Convert the tracked exp07 mini PyPEEC dataset into exp08 graph records.

    `field_key` is usually `B_centerline` or `B_pypeec`. The graph candidates are
    reconstructed from exp07 metadata and are intentionally approximate; this is
    a bridge diagnostic, not a real layout parser.
    """

    data = np.load(npz_path, allow_pickle=True)
    metadata = json.loads(str(data["metadata_json"]))
    exp07_cfg = json.loads(str(data["config_json"]))
    x = np.asarray(data["x"], dtype=float)
    y = np.asarray(data["y"], dtype=float)
    xg, yg = np.meshgrid(x, y, indexing="xy")
    zg = np.full_like(xg, float(exp07_cfg["sensor_grid"]["z_m"]))
    obs_grid = np.stack([xg, yg, zg], axis=-1)
    records: list[CaseRecord] = []
    for idx, meta in enumerate(metadata):
        class_label, hypothesis_label = _classify_exp07_case(meta)
        sheet, via, ret, artifact = _split_segments(meta, hypothesis_label)
        b_obs = np.asarray(data[field_key][idx], dtype=float)
        records.append(
            CaseRecord(
                case_id=str(meta["name"]),
                split="exp07_bridge",
                class_label=class_label,
                hypothesis_label=hypothesis_label,
                b_clean=np.asarray(data["B_centerline"][idx], dtype=float),
                b_obs=b_obs,
                sheet_segments=sheet,
                via_candidates=via,
                return_candidates=ret,
                artifact_candidates=artifact,
                truth_currents={
                    str(seg.get("tag", f"segment_{j}")): float(seg.get("current_a", 0.0))
                    for j, seg in enumerate(meta.get("segments", []))
                },
                metadata={
                    "source": "exp07-pypeec-solver-cross-validation",
                    "field_key": field_key,
                    "case_type": str(data["case_type"][idx]),
                    "is_exp03_like": bool(data["is_exp03_like"][idx]),
                    "claim_boundary": "Approximate graph reconstruction from exp07 metadata; not real CAD import.",
                },
            )
        )
    return records, obs_grid
