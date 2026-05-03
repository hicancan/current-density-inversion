from __future__ import annotations

import hashlib
from typing import Any, Iterable


def _stable_unit_interval(text: str) -> float:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(16**12 - 1)


def family_from_case(case_name: str, case_type: str, is_exp03_like: bool) -> str:
    text = f"{case_name} {case_type}".lower()
    if "return_path" in text:
        return "return_path"
    if "dense_via" in text:
        return "dense_via"
    if "no_via" in text:
        return "no_via"
    if "multi_via" in text:
        return "multi_via"
    if "two_layer" in text or "via" in text:
        return "via_route"
    if is_exp03_like:
        return "exp03_like_other"
    return "canonical"


def build_pypeec_heldout_split_protocol(
    case_names: Iterable[str],
    case_types: Iterable[str],
    is_exp03_like: Iterable[bool],
    calibration_fraction: float = 0.30,
) -> dict[str, Any]:
    """Define a deterministic future PyPEEC calibration/test split.

    The returned split is a protocol artifact only. Current exp04 metrics must
    keep using the whole PyPEEC mini distribution as frozen test and must not
    select thresholds from these rows unless a future experiment explicitly
    changes the `used_for_current_*` flags.
    """
    rows: list[dict[str, Any]] = []
    for idx, (name, ctype, exp03_like) in enumerate(zip(case_names, case_types, is_exp03_like)):
        family = family_from_case(str(name), str(ctype), bool(exp03_like))
        score = _stable_unit_interval(f"{family}|{name}|{ctype}|v1")
        role = "future_calibration_candidate" if score < calibration_fraction else "future_heldout_test"
        rows.append(
            {
                "case_index": int(idx),
                "case_name": str(name),
                "case_type": str(ctype),
                "family": family,
                "is_exp03_like": bool(exp03_like),
                "split_score": float(score),
                "future_role": role,
                "used_for_current_training": False,
                "used_for_current_threshold_selection": False,
                "used_for_current_calibration": False,
            }
        )
    by_family: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_family.setdefault(str(row["family"]), []).append(row)
    for family_rows in by_family.values():
        if not any(row["future_role"] == "future_calibration_candidate" for row in family_rows):
            chosen = min(family_rows, key=lambda row: float(row["split_score"]))
            chosen["future_role"] = "future_calibration_candidate"
            chosen["role_adjustment"] = "promoted_lowest_hash_score_for_family_coverage"
        for row in family_rows:
            row.setdefault("role_adjustment", "none")
    family_summary: dict[str, dict[str, int]] = {}
    for row in rows:
        fam = str(row["family"])
        family_summary.setdefault(fam, {"total": 0, "future_calibration_candidate": 0, "future_heldout_test": 0})
        family_summary[fam]["total"] += 1
        family_summary[fam][str(row["future_role"])] += 1
    return {
        "enabled": True,
        "protocol_version": "sha256-family-balanced-v1",
        "current_protocol": "frozen_no_calibration",
        "calibration_fraction_target": float(calibration_fraction),
        "used_for_current_training": False,
        "used_for_current_threshold_selection": False,
        "used_for_current_calibration": False,
        "rows": rows,
        "family_summary": family_summary,
        "boundary": (
            "This split is reserved for a future PyPEEC calibration/held-out protocol. "
            "The current reported PyPEEC stress remains frozen evaluation only."
        ),
    }
