"""Pairwise hypothesis distinguishability distances.

For each hypothesis pair (Gi, Gj):
  D(Gi, Gj) = min_{zi in Gi, zj in Gj} ||F(zi) - F(zj)||_2

This is the minimum noise-free forward distance between two hypothesis subspaces.
If D(Gi, Gj) <= epsilon at noise level, Gi and Gj are fundamentally indistinguishable.
"""

from __future__ import annotations

import numpy as np

from hypotheses import HYPOTHESES, HypothesisBasis, subspace_principal_angle_deg
from operators import OperatorBundle


def subspace_min_distance(B1: np.ndarray, B2: np.ndarray) -> float:
    """Compute minimum distance between two linear subspaces.

    Uses SVD of the concatenated basis difference:
    min_{z1, z2} ||B1*z1 - B2*z2||_2 = smallest singular value of [B1 | -B2]
    """
    if B1.shape[1] == 0 or B2.shape[1] == 0:
        return _rough_distance(B1, B2)

    C = np.concatenate([B1, -B2], axis=1)
    if C.size == 0:
        return 0.0
    s = np.linalg.svd(C, compute_uv=False)
    return float(s[-1]) if s.size > 0 else 0.0


def _rough_distance(B1: np.ndarray, B2: np.ndarray) -> float:
    """Fallback distance when subspace dims differ."""
    if B1.shape[1] == 0 and B2.shape[1] == 0:
        return 0.0
    if B1.shape[1] == 0:
        return float(np.linalg.norm(B2))
    if B2.shape[1] == 0:
        return float(np.linalg.norm(B1))
    return float(np.linalg.norm(B1 - B2))


def pairwise_distinguishability(
    bases: dict[str, HypothesisBasis],
    bundle: OperatorBundle,
) -> dict:
    """Compute all pairwise distinguishability distances among H0-H3.

    Reports two types of distance:
    - full_distance: minimum distance between full subspaces (always 0 if H0 shared)
    - extra_distance: minimum distance between subspaces projected orthogonal to H0
      (measures whether hypothesis-specific features are distinguishable)
    """
    pairs = [
        ("H0_no_via", "H1_via"),
        ("H0_no_via", "H2_model_gap"),
        ("H0_no_via", "H3_return_path"),
        ("H1_via", "H2_model_gap"),
        ("H1_via", "H3_return_path"),
        ("H2_model_gap", "H3_return_path"),
    ]

    # Common subspace = H0
    B_common = bases["H0_no_via"].B

    result = {"pairs": {}, "matrix": {}}

    for hi, hj in pairs:
        Bi_full = bases[hi].B
        Bj_full = bases[hj].B
        full_dist = subspace_min_distance(Bi_full, Bj_full)
        angle = subspace_principal_angle_deg(Bi_full, Bj_full)

        # Compute distance between orthogonal complements (beyond H0)
        if hi == "H0_no_via":
            Bi_extra = np.zeros((Bi_full.shape[0], 0))
        else:
            Bi_extra = Bi_full - B_common @ (np.linalg.pinv(B_common) @ Bi_full)
        if hj == "H0_no_via":
            Bj_extra = np.zeros((Bj_full.shape[0], 0))
        else:
            Bj_extra = Bj_full - B_common @ (np.linalg.pinv(B_common) @ Bj_full)
        extra_dist = subspace_min_distance(Bi_extra, Bj_extra)

        pair_key = f"{hi}__{hj}"
        result["pairs"][pair_key] = {
            "full_distance": full_dist,
            "extra_distance": extra_dist,
            "principal_angle_deg": angle,
            "dim_i": Bi_full.shape[1],
            "dim_j": Bj_full.shape[1],
        }
        result["matrix"].setdefault(hi, {})[hj] = extra_dist
        result["matrix"].setdefault(hj, {})[hi] = extra_dist

    return result


def per_family_distinguishability(
    bundles: dict[str, OperatorBundle],
    cfg: dict,
) -> dict:
    """Compute distinguishability for single-height vs multi-height configs.

    bundles: {"single": single_height_bundle, "multi": multi_height_bundle}
    """
    out = {}
    for name, bundle in bundles.items():
        # Build bases using the appropriate bundle A
        from hypotheses import build_all_hypothesis_bases
        bases = build_all_hypothesis_bases(bundle, cfg)
        out[name] = pairwise_distinguishability(bases, bundle)
    return out


def distinguishability_report(
    pairwise: dict,
    epsilon: float,
) -> dict:
    """Summarize pairwise results relative to an epsilon threshold."""
    distinguishable = []
    indistinguishable = []
    for pair_key, stats in pairwise["pairs"].items():
        if stats["extra_distance"] > epsilon:
            distinguishable.append(pair_key)
        else:
            indistinguishable.append(pair_key)

    return {
        "epsilon": epsilon,
        "distinguishable_pairs": distinguishable,
        "indistinguishable_pairs": indistinguishable,
        "distinguishable_count": len(distinguishable),
        "indistinguishable_count": len(indistinguishable),
        "pair_details": pairwise["pairs"],
    }
