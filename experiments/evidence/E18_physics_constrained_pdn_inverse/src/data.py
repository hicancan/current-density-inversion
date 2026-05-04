"""Data generation for E18 physics-constrained PDN inverse.

Reuses E15 four-layer via-chain benchmark generation with identical families
and channel layout (11 channels: J1x,J1y,J2x,J2y,J3x,J3y,J4x,J4y,s12,s23,s34).
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import numpy as np

LAYER_IDS = ["L1", "L2", "L3", "L4"]
CHANNEL_NAMES = [
    "J1x", "J1y", "J2x", "J2y", "J3x", "J3y", "J4x", "J4y",
    "s12", "s23", "s34",
]

def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rng(seed: int):
    return np.random.default_rng(seed)


def _grid_centers(cfg: dict):
    n = int(cfg["grid_size"])
    x0, x1, y0, y1 = cfg["in_plane_extent"]
    xs = np.linspace(x0 + (x1 - x0) / (2 * n), x1 - (x1 - x0) / (2 * n), n)
    ys = np.linspace(y0 + (y1 - y0) / (2 * n), y1 - (y1 - y0) / (2 * n), n)
    return xs, ys, xs[1] - xs[0], ys[1] - ys[0]


def _gauss(xs, ys, cx, cy, sx, sy):
    xm, ym = np.meshgrid(xs, ys, indexing="ij")
    return np.exp(-((xm - cx) ** 2) / (2 * sx ** 2) - ((ym - cy) ** 2) / (2 * sy ** 2))


def _loop(n, xs, ys, cx, cy, rx, ry, sign=1.0):
    xm, ym = np.meshgrid(xs, ys, indexing="ij")
    hx = ((ym - cy) / ry) * _gauss(xs, ys, cx + rx, cy, 0.25 * rx, 0.5 * ry)
    hy = -((xm - cx) / rx) * _gauss(xs, ys, cx, cy + ry, 0.5 * rx, 0.25 * ry)
    hx -= ((ym - (cy - ry)) / ry) * _gauss(xs, ys, cx + rx, cy - ry, 0.25 * rx, 0.5 * ry)
    hy += ((xm - (cx - rx)) / rx) * _gauss(xs, ys, cx - rx, cy, 0.5 * rx, 0.25 * ry)
    hx += ((ym - cy) / ry) * _gauss(xs, ys, cx - rx, cy, 0.25 * rx, 0.5 * ry)
    hy -= ((xm - cx) / rx) * _gauss(xs, ys, cx, cy - ry, 0.5 * rx, 0.25 * ry)
    sc = sign * 0.1 / max(np.sqrt(np.mean(hx ** 2 + hy ** 2)), 1e-30)
    return hx * sc, hy * sc


def _ss(n, xs, ys, cx, cy, sigma, amp):
    g = _gauss(xs, ys, cx, cy, sigma, sigma)
    t = np.sum(g)
    if t > 1e-30:
        g[n // 2, n // 2] -= t
    sc = amp / max(np.sqrt(np.mean(g ** 2)), 1e-30)
    return g * sc


def generate_case(family: str, variant: int, cfg: dict, rng, A_op: np.ndarray):
    """Generate a single four-layer benchmark case."""
    n = int(cfg["grid_size"])
    xs, ys, dx, dy = _grid_centers(cfg)
    ch = np.zeros((11, n, n))
    ext = cfg["in_plane_extent"]
    cx = float(rng.uniform(ext[0] + 0.08, ext[1] - 0.08))
    cy = float(rng.uniform(ext[2] + 0.08, ext[3] - 0.08))
    rx = float(rng.uniform(0.06, 0.14))
    ry = float(rng.uniform(0.06, 0.14))
    amp = float(rng.uniform(0.05, 0.15))

    if family == "deep_layer_only":
        al = [2, 3]
    elif family == "layer_misallocation_trap":
        al = [0, 3]
    else:
        al = [0, 1, 2, 3]

    for li in al:
        lx = cx + rng.uniform(-0.03, 0.03)
        ly = cy + rng.uniform(-0.03, 0.03)
        lrx = rx * (1 + 0.15 * li)
        lry = ry * (1 + 0.15 * li)
        sign = 1.0 if rng.uniform(0, 1) < 0.5 else -1.0
        jx, jy = _loop(n, xs, ys, lx, ly, lrx, lry, sign)
        ch[li * 2] = jx * amp * (1 + 0.2 * (3 - li))
        ch[li * 2 + 1] = jy * amp * (1 + 0.2 * (3 - li))

    vsig = (dx + dy) * 0.8
    vamp = amp * 0.3
    if family in {"nominal_via_chain", "dense_via_cluster", "return_grid_bottleneck"}:
        for vi in range(3):
            vx = cx + rng.uniform(-0.04, 0.04)
            vy = cy + rng.uniform(-0.04, 0.04)
            va = vamp * (1 - 0.1 * vi)
            ch[8 + vi] = _ss(n, xs, ys, vx, vy, vsig, va)
        if family == "dense_via_cluster":
            for _ in range(3):
                vx = cx + rng.uniform(-0.06, 0.06)
                vy = cy + rng.uniform(-0.06, 0.06)
                ch[9] += _ss(n, xs, ys, vx, vy, vsig * 0.7, vamp * 0.4)

    if family == "return_grid_bottleneck":
        ci = 6 if len(al) > 3 else (al[-1] * 2)
        cj = ci + 1
        mid = n // 2
        bw = max(1, n // 5)
        mask = np.ones(n)
        mask[mid - bw // 2:mid + bw // 2 + 1] = 0.3
        ch[cj] *= mask[None, :]

    if family == "no_via_hard_negative":
        ch[8] = 0.0
        ch[9] = 0.0
        ch[10] = 0.0

    flat = ch.reshape(-1)
    m = int(cfg["sensor_grid_size"])
    bf = A_op @ flat
    return {
        "family": family,
        "variant": int(variant),
        "channels": ch,
        "field": bf.reshape(m, m, 3),
        "flat_ground_truth": flat,
    }


def generate_all_cases(cfg: dict, A_op: np.ndarray) -> list[dict]:
    """Generate all benchmark cases from config."""
    cases = []
    fams = cfg["families"]
    vpf = int(cfg["variants_per_family"])
    seed = int(cfg["seed"])
    step = int(cfg["seed_per_variant_step"])
    for fi, fam in enumerate(fams):
        for vi in range(vpf):
            cs = seed + fi * 100 + vi * step
            rng = _rng(cs)
            case = generate_case(fam, vi, cfg, rng, A_op)
            case["case_id"] = f"{fam}_v{vi}"
            case["split_role"] = "heldout" if vi == vpf - 1 else "calibration"
            cases.append(case)
    return cases
