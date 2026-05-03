from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from validate_real_case_metadata import validate_case


def load_field_array(case_json: Path) -> tuple[dict[str, object], np.ndarray]:
    payload = json.loads(case_json.read_text(encoding="utf-8"))
    errors = validate_case(payload, base_dir=case_json.parent, strict_paths=True)
    if errors:
        raise ValueError("; ".join(errors))
    field = payload["field"]
    path = Path(field["path"])
    if not path.is_absolute():
        path = case_json.parent / path
    data = np.load(path)
    key = field["array_key"]
    if key not in data:
        raise KeyError(f"array key `{key}` not found in {path}")
    arr = np.asarray(data[key], dtype=float)
    expected_shape = tuple(int(v) for v in field["shape"])
    if arr.shape != expected_shape:
        raise ValueError(f"field shape mismatch: expected {expected_shape}, got {arr.shape}")
    if arr.shape[-1] != len(field["component_order"]):
        raise ValueError("last field dimension must match component_order length")
    if not np.all(np.isfinite(arr)):
        raise ValueError("field contains non-finite values")
    summary = {
        "case_id": payload["case_id"],
        "shape": list(arr.shape),
        "component_order": field["component_order"],
        "units": field["units"],
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "rms": float(np.sqrt(np.mean(arr * arr))),
    }
    return summary, arr


def load_field(case_json: Path) -> dict[str, object]:
    summary, _ = load_field_array(case_json)
    return {
        **summary,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Load and sanity-check an Exp09 QDM/NV .npz field.")
    parser.add_argument("case_json", type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(load_field(args.case_json), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
