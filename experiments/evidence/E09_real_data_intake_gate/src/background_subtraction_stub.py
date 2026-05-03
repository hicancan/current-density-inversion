from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from load_qdm_npz_stub import load_field_array


def _resolve(path_text: str, base_dir: Path) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else base_dir / path


def subtract_background(case_json: Path, out_npz: Path, out_key: str = "B_subtracted") -> dict[str, object]:
    payload = json.loads(case_json.read_text(encoding="utf-8"))
    summary, arr = load_field_array(case_json)
    background = payload.get("background", {})
    if background.get("protocol") == "none" or not background.get("path"):
        raise ValueError("background protocol/path must be set before subtraction")
    bg_path = _resolve(str(background["path"]), case_json.parent)
    bg = np.load(bg_path)
    key = str(background.get("array_key", payload["field"]["array_key"]))
    if key not in bg:
        raise KeyError(f"background array key `{key}` not found in {bg_path}")
    bg_arr = np.asarray(bg[key], dtype=float)
    if bg_arr.shape != arr.shape:
        raise ValueError(f"background shape mismatch: expected {arr.shape}, got {bg_arr.shape}")
    if not np.all(np.isfinite(bg_arr)):
        raise ValueError("background contains non-finite values")
    out_npz.parent.mkdir(parents=True, exist_ok=True)
    result = arr - bg_arr
    np.savez_compressed(out_npz, **{out_key: result.astype(np.float32)})
    return {
        "case_id": summary["case_id"],
        "output": str(out_npz),
        "array_key": out_key,
        "input_rms": float(np.sqrt(np.mean(arr * arr))),
        "background_rms": float(np.sqrt(np.mean(bg_arr * bg_arr))),
        "subtracted_rms": float(np.sqrt(np.mean(result * result))),
        "claim_boundary": "background utility only; not a physical validation claim",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Subtract a reference/zero-current background from an Exp09 field case.")
    parser.add_argument("case_json", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--out-key", default="B_subtracted")
    args = parser.parse_args(argv)
    print(json.dumps(subtract_background(args.case_json, args.out, args.out_key), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
