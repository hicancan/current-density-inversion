from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from .types import CaseRecord, Segment


def segment_from_json(payload: Mapping[str, Any]) -> Segment:
    """Parse one graph-current segment from the lightweight exp08 JSON schema."""

    required = ["name", "layer", "kind", "start", "end"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"segment is missing required keys: {missing}")
    prior_group = str(payload.get("prior_group", payload.get("kind", "sheet")))
    return Segment(
        name=str(payload["name"]),
        layer=str(payload["layer"]),
        kind=str(payload["kind"]),
        start=tuple(float(x) for x in payload["start"]),
        end=tuple(float(x) for x in payload["end"]),
        prior_group=prior_group,
    )


def case_record_from_json(payload: Mapping[str, Any], b_obs: np.ndarray | None = None) -> CaseRecord:
    """Build a `CaseRecord` from a simple graph/candidate JSON document.

    This is not a Gerber/GDS parser. It is the stable interchange layer that a
    future layout parser can target: nodes/edges may be converted upstream, and
    exp08 only needs sheet, via, return, and artifact candidate segments.
    """

    if "case_id" not in payload:
        raise ValueError("case JSON must include `case_id`")
    if b_obs is None:
        if "b_obs" not in payload:
            raise ValueError("case JSON must include `b_obs` when no array is supplied")
        b_obs = np.asarray(payload["b_obs"], dtype=float)
    else:
        b_obs = np.asarray(b_obs, dtype=float)
    b_clean = np.asarray(payload.get("b_clean", b_obs), dtype=float)
    if b_obs.ndim != 3 or b_obs.shape[-1] != 3:
        raise ValueError(f"b_obs must have shape (H, W, 3); got {b_obs.shape}")

    def parse_many(key: str) -> list[Segment]:
        return [segment_from_json(item) for item in payload.get(key, [])]

    return CaseRecord(
        case_id=str(payload["case_id"]),
        split=str(payload.get("split", "external")),
        class_label=str(payload.get("class_label", "unknown")),
        hypothesis_label=str(payload.get("hypothesis_label", "unknown")),
        b_clean=b_clean,
        b_obs=b_obs,
        sheet_segments=parse_many("sheet_segments"),
        via_candidates=parse_many("via_candidates"),
        return_candidates=parse_many("return_candidates"),
        artifact_candidates=parse_many("artifact_candidates"),
        truth_currents={str(k): float(v) for k, v in payload.get("truth_currents", {}).items()},
        metadata=dict(payload.get("metadata", {})),
    )


def load_case_record_json(path: Path, b_obs: np.ndarray | None = None) -> CaseRecord:
    return case_record_from_json(json.loads(path.read_text(encoding="utf-8")), b_obs=b_obs)
