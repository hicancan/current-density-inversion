from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np


def write_json(path: Path, payload: Mapping) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out) + "\n"


def fmt_float(x: float) -> str:
    if x != x:
        return "nan"
    if abs(x) >= 1000 or (abs(x) > 0 and abs(x) < 1e-3):
        return f"{x:.3e}"
    return f"{x:.4f}"


def save_confusion_matrix(path: Path, cm: np.ndarray, labels: Sequence[str], title: str) -> None:
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation="nearest")
    ax.set_title(title)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("predicted")
    ax.set_ylabel("true")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(int(cm[i, j])), ha="center", va="center")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_score_histogram(path: Path, scores_pos, scores_neg, threshold: float, title: str) -> None:
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(scores_neg, bins=24, alpha=0.65, label="no true via")
    ax.hist(scores_pos, bins=24, alpha=0.65, label="true via")
    ax.axvline(threshold, linestyle="--", linewidth=1.5, label="validation threshold")
    ax.set_title(title)
    ax.set_xlabel("via evidence score")
    ax.set_ylabel("case count")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_example_case(path: Path, record, results) -> None:
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    b = record.b_obs
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
    names = ["Bx", "By", "Bz"]
    for k, ax in enumerate(axes):
        im = ax.imshow(b[..., k], origin="lower")
        ax.set_title(f"{record.class_label}: {names[k]}")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    scores = ", ".join(f"{name.replace('H', 'H')}: {res.score:.3f}" for name, res in results.items())
    fig.suptitle(f"{record.case_id}\n{scores}", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
