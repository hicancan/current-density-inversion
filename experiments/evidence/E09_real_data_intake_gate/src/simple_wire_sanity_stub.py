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


def simple_wire_sanity(case_json: Path) -> dict[str, object]:
    summary, arr = load_field_array(case_json)
    component_order = list(summary["component_order"])
    comp = {name: arr[:, :, idx] for idx, name in enumerate(component_order)}
    bx = comp.get("Bx")
    by = comp.get("By")
    bz = comp.get("Bz")
    bxy_rms = float(np.sqrt(np.mean((0.0 if bx is None else bx * bx) + (0.0 if by is None else by * by))))
    bz_rms = float("nan") if bz is None else float(np.sqrt(np.mean(bz * bz)))
    peak_idx = np.unravel_index(int(np.argmax(np.sqrt(np.sum(arr * arr, axis=-1)))), arr.shape[:2])
    center = ((arr.shape[0] - 1) / 2.0, (arr.shape[1] - 1) / 2.0)
    peak_offset_px = (float(peak_idx[0] - center[0]), float(peak_idx[1] - center[1]))
    symmetry_bx = float("nan") if bx is None else float(abs(np.mean(bx) / (np.sqrt(np.mean(bx * bx)) + 1e-30)))
    symmetry_by = float("nan") if by is None else float(abs(np.mean(by) / (np.sqrt(np.mean(by * by)) + 1e-30)))
    return {
        "case_id": summary["case_id"],
        "shape": summary["shape"],
        "component_order": component_order,
        "bxy_rms_t": bxy_rms,
        "bz_rms_t": bz_rms,
        "bz_over_bxy_rms": float(bz_rms / (bxy_rms + 1e-30)) if np.isfinite(bz_rms) else float("nan"),
        "peak_location_rc": [int(peak_idx[0]), int(peak_idx[1])],
        "peak_offset_px_from_center": list(peak_offset_px),
        "mean_over_rms_Bx": symmetry_bx,
        "mean_over_rms_By": symmetry_by,
        "claim_boundary": "simple-wire sanity only; inspect units, polarity, centering, and component order before exp08 inference",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute first-pass simple-wire sanity metrics for an Exp09 field case.")
    parser.add_argument("case_json", type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(simple_wire_sanity(args.case_json), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
