from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from load_qdm_npz_stub import load_field_array


def plot_components(case_json: Path, out_path: Path) -> dict[str, object]:
    summary, arr = load_field_array(case_json)
    component_order = list(summary["component_order"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, arr.shape[-1], figsize=(3.2 * arr.shape[-1], 3.2), constrained_layout=True)
    if arr.shape[-1] == 1:
        axes = [axes]
    vmax = float(np.max(np.abs(arr)))
    vmax = vmax if vmax > 0 else 1.0
    for idx, ax in enumerate(axes):
        im = ax.imshow(arr[:, :, idx], cmap="coolwarm", vmin=-vmax, vmax=vmax, origin="lower")
        ax.set_title(str(component_order[idx]))
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle(str(summary["case_id"]))
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return {"case_id": summary["case_id"], "output": str(out_path), "shape": summary["shape"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plot Exp09 QDM/NV B-field components from a validated case JSON.")
    parser.add_argument("case_json", type=Path)
    parser.add_argument("--out", type=Path, default=Path("B_components.png"))
    args = parser.parse_args(argv)
    print(plot_components(args.case_json, args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
