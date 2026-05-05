"""Near-null mode extraction via SVD.

Computes the SVD of A_E * H_all (stacked forward operator times all admissible
current modes) and extracts near-null modes — current patterns that produce
almost zero magnetic field at the sensor.

These are the "invisible" current patterns that cannot be recovered from magnetic
observations regardless of algorithm choice.
"""

from __future__ import annotations

import numpy as np

from hypotheses import HYPOTHESES, HypothesisBasis
from operators import OperatorBundle


def near_null_modes(
    bundle: OperatorBundle,
    bases: dict[str, HypothesisBasis],
    threshold: float = 0.01,
    max_null_modes: int = 50,
) -> dict:
    """Extract near-null modes from the forward operator.

    1. Stack all hypothesis bases into H_all
    2. Compute SVD of H_all (current-space basis)
    3. Forward each mode through A to get singular values
    4. Identify modes with singular value <= threshold * max_singular_value
    """
    # Stack all current bases
    parts = []
    for h in HYPOTHESES:
        if bases[h].current_basis.shape[1] > 0:
            parts.append(bases[h].current_basis)
    if not parts:
        return {"near_null_count": 0, "effective_rank": 0, "singular_values": [], "modes": []}

    H_all = np.concatenate(parts, axis=1)
    # SVD of A @ H_all gives the true observable singular values
    A_H_all = bundle.A @ H_all
    _, S, Vt = np.linalg.svd(A_H_all, full_matrices=False)

    s_max = S[0] if S.size > 0 else 1.0
    threshold_abs = threshold * s_max

    near_null_indices = [i for i, s in enumerate(S) if s <= threshold_abs]
    effective_rank = sum(1 for s in S if s > threshold_abs)

    modes = []
    for idx in near_null_indices[:max_null_modes]:
        v = Vt[idx, :]  # left singular vector in coefficient space
        current_mode = H_all @ v  # project to current space
        field_mode = bundle.A @ current_mode  # forward to field space

        # Decompose by block contribution
        block_energy = {}
        col_start = 0
        for h in HYPOTHESES:
            k = bases[h].current_basis.shape[1]
            if k > 0:
                block_energy[h] = float(np.linalg.norm(v[col_start:col_start + k]) ** 2)
                col_start += k

        modes.append({
            "index": idx,
            "singular_value": float(S[idx]),
            "singular_value_ratio": float(S[idx] / s_max) if s_max > 0 else 0.0,
            "current_norm": float(np.linalg.norm(current_mode)),
            "field_norm": float(np.linalg.norm(field_mode)),
            "block_energy": block_energy,
        })

    return {
        "near_null_count": len(modes),
        "effective_rank": effective_rank,
        "total_rank": int(S.size),
        "singular_values": S.tolist()[:200],
        "singular_value_ratios": (S / max(s_max, 1e-30)).tolist()[:200],
        "threshold": threshold,
        "modes": modes,
        "max_singular_value": float(s_max),
        "min_singular_value": float(S[-1]) if S.size > 0 else 0.0,
    }
