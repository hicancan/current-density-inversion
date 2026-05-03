from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_COMPONENTS = {"Bx", "By", "Bz"}
ALLOWED_FIELD_UNITS = {"tesla", "T"}
ALLOWED_ORIGINS = {"center", "top_left", "custom"}
ALLOWED_BACKGROUND_PROTOCOLS = {"none", "subtract_zero_current", "subtract_reference"}
ALLOWED_SAMPLE_TYPES = {"wire", "coupon", "fpc", "pcb", "chip", "unknown"}


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_positive_number(value: Any) -> bool:
    return _is_number(value) and float(value) > 0.0


def _is_unknown_or_number(value: Any, positive: bool = False) -> bool:
    if value == "unknown":
        return True
    return _is_positive_number(value) if positive else _is_number(value)


def _require_mapping(payload: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{key}` must be an object")
        return {}
    return value


def validate_case(payload: dict[str, Any], base_dir: Path | None = None, strict_paths: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload.get("case_id"), str) or not payload["case_id"]:
        errors.append("`case_id` must be a non-empty string")

    field = _require_mapping(payload, "field", errors)
    if field:
        path = field.get("path")
        if not isinstance(path, str) or not path.endswith(".npz"):
            errors.append("`field.path` must be a .npz path string")
        elif strict_paths and base_dir is not None and not (base_dir / path).exists() and not Path(path).exists():
            errors.append(f"`field.path` does not exist: {path}")
        if not isinstance(field.get("array_key"), str) or not field["array_key"]:
            errors.append("`field.array_key` must be a non-empty string")
        shape = field.get("shape")
        if not (isinstance(shape, list) and len(shape) == 3 and all(isinstance(v, int) and v > 0 for v in shape)):
            errors.append("`field.shape` must be [ny, nx, n_components] with positive integers")
        component_order = field.get("component_order")
        if not (
            isinstance(component_order, list)
            and len(component_order) == 3
            and set(component_order).issubset(ALLOWED_COMPONENTS)
            and len(set(component_order)) == 3
        ):
            errors.append("`field.component_order` must be a permutation/subset order of [Bx, By, Bz]")
        if field.get("units") not in ALLOWED_FIELD_UNITS:
            errors.append("`field.units` must be tesla/T before graph-identification evaluation")

    grid = _require_mapping(payload, "grid", errors)
    if grid:
        if not _is_positive_number(grid.get("pixel_size_m")):
            errors.append("`grid.pixel_size_m` must be positive")
        if grid.get("origin") not in ALLOWED_ORIGINS:
            errors.append("`grid.origin` must be center/top_left/custom")

    pose = _require_mapping(payload, "sensor_pose", errors)
    if pose:
        if not _is_unknown_or_number(pose.get("standoff_m"), positive=True):
            errors.append("`sensor_pose.standoff_m` must be positive or unknown")
        if not _is_unknown_or_number(pose.get("tilt_x_mrad")):
            errors.append("`sensor_pose.tilt_x_mrad` must be numeric or unknown")
        if not _is_unknown_or_number(pose.get("tilt_y_mrad")):
            errors.append("`sensor_pose.tilt_y_mrad` must be numeric or unknown")

    background = _require_mapping(payload, "background", errors)
    if background:
        if background.get("protocol") not in ALLOWED_BACKGROUND_PROTOCOLS:
            errors.append("`background.protocol` must be none/subtract_zero_current/subtract_reference")
        path = background.get("path")
        if path is not None and not isinstance(path, str):
            errors.append("`background.path` must be null or a path string")
        elif strict_paths and path and base_dir is not None and not (base_dir / path).exists() and not Path(path).exists():
            errors.append(f"`background.path` does not exist: {path}")

    sample = _require_mapping(payload, "sample", errors)
    if sample:
        if sample.get("type") not in ALLOWED_SAMPLE_TYPES:
            errors.append("`sample.type` must be wire/coupon/fpc/pcb/chip/unknown")
        geometry_path = sample.get("geometry_path")
        if geometry_path is not None and not isinstance(geometry_path, str):
            errors.append("`sample.geometry_path` must be null or a path string")
        elif strict_paths and geometry_path and base_dir is not None and not (base_dir / geometry_path).exists() and not Path(geometry_path).exists():
            errors.append(f"`sample.geometry_path` does not exist: {geometry_path}")

    excitation = _require_mapping(payload, "excitation", errors)
    if excitation:
        if not isinstance(excitation.get("state_id"), str) or not excitation["state_id"]:
            errors.append("`excitation.state_id` must be a non-empty string")
        current = excitation.get("current_a")
        if current != "unknown" and not _is_number(current):
            errors.append("`excitation.current_a` must be numeric or unknown")

    if payload.get("claim_boundary") != "real-data interface only":
        errors.append("`claim_boundary` must remain `real-data interface only` for this scaffold")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Exp09 real QDM/NV case metadata.")
    parser.add_argument("case_json", type=Path)
    parser.add_argument("--strict-paths", action="store_true")
    args = parser.parse_args(argv)

    payload = json.loads(args.case_json.read_text(encoding="utf-8"))
    errors = validate_case(payload, base_dir=args.case_json.parent, strict_paths=args.strict_paths)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
