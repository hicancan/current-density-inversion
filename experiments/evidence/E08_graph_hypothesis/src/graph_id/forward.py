from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np

from .types import Segment

MU0_OVER_4PI = 1e-7
_EPS = 1e-18


def make_observation_grid(n: int, fov_m: float, obs_z_m: float = 0.0) -> np.ndarray:
    """Return an ``(n, n, 3)`` observation grid centered at the origin."""

    xs = np.linspace(-fov_m / 2.0, fov_m / 2.0, n)
    ys = np.linspace(-fov_m / 2.0, fov_m / 2.0, n)
    xg, yg = np.meshgrid(xs, ys, indexing="xy")
    zg = np.full_like(xg, obs_z_m, dtype=float)
    return np.stack([xg, yg, zg], axis=-1)


def _segment_field_unit_current(segment: Segment, obs_xyz: np.ndarray, n_steps: int) -> np.ndarray:
    """Discretized Biot-Savart field for one ampere through one segment.

    The segment is represented by midpoint current elements. This is not a FEM
    solver; it is a controlled graph-level forward model whose role is to test
    whether a proposed current-flow graph can explain an observed magnetic field.
    """

    start = np.asarray(segment.start, dtype=float)
    end = np.asarray(segment.end, dtype=float)
    dl_total = end - start
    if np.linalg.norm(dl_total) < 1e-15:
        return np.zeros_like(obs_xyz, dtype=float)

    # Midpoint rule: each current element has vector length dl_total / n_steps.
    t = (np.arange(n_steps, dtype=float) + 0.5) / float(n_steps)
    points = start[None, :] + t[:, None] * dl_total[None, :]
    dl = dl_total / float(n_steps)

    out = np.zeros_like(obs_xyz, dtype=float)
    obs_flat = obs_xyz.reshape(-1, 3)
    out_flat = out.reshape(-1, 3)
    for p in points:
        r = obs_flat - p[None, :]
        r_norm = np.linalg.norm(r, axis=1)
        denom = np.maximum(r_norm**3, _EPS)
        contrib = np.cross(dl[None, :], r) / denom[:, None]
        out_flat += MU0_OVER_4PI * contrib
    return out


def field_from_segments(
    segments: Iterable[Segment],
    currents: dict[str, float],
    obs_xyz: np.ndarray,
    edge_steps: int = 22,
    via_steps: int = 14,
) -> np.ndarray:
    """Superpose fields from named graph segments with given current amplitudes."""

    b = np.zeros_like(obs_xyz, dtype=float)
    for seg in segments:
        current = float(currents.get(seg.name, 0.0))
        if current == 0.0:
            continue
        n_steps = via_steps if seg.kind == "via" else edge_steps
        b += current * _segment_field_unit_current(seg, obs_xyz, n_steps=n_steps)
    return b


def basis_matrix(
    segments: list[Segment],
    obs_xyz: np.ndarray,
    edge_steps: int = 22,
    via_steps: int = 14,
) -> Tuple[np.ndarray, list[str], np.ndarray]:
    """Build a column-normalized forward matrix for graph current bases.

    Returns ``A_norm, names, column_norms`` where columns of ``A_norm`` map
    normalized coefficients to flattened ``Bxyz`` observations. Physical current
    coefficients can be recovered by dividing normalized coefficients by norms.
    """

    cols = []
    names = []
    norms = []
    for seg in segments:
        n_steps = via_steps if seg.kind == "via" else edge_steps
        col = _segment_field_unit_current(seg, obs_xyz, n_steps=n_steps).reshape(-1)
        norm = float(np.linalg.norm(col))
        if norm < 1e-30:
            continue
        cols.append(col / norm)
        names.append(seg.name)
        norms.append(norm)
    if not cols:
        return np.zeros((obs_xyz.size, 0), dtype=float), [], np.zeros((0,), dtype=float)
    return np.stack(cols, axis=1), names, np.asarray(norms, dtype=float)


def flatten_field(b_xyz: np.ndarray) -> np.ndarray:
    return np.asarray(b_xyz, dtype=float).reshape(-1)


def relative_l2(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(b.reshape(-1))) + 1e-30
    return float(np.linalg.norm((a - b).reshape(-1)) / denom)
