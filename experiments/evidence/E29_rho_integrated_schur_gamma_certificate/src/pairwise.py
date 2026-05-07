"""Pairwise defect certificate.

For two candidate defects q and r:

    Gamma^{cons}_{qr} = ||Delta Y_q - Delta Y_r|| - epsilon - tau - rho_q - rho_r

Must be > 0 for pairwise distinguishability.
"""
from __future__ import annotations

import numpy as np


def compute_pairwise_delta(
    A_nominal: np.ndarray,
    A_defect_q: np.ndarray,
    A_defect_r: np.ndarray,
    current_samples: np.ndarray,
) -> dict:
    """Compute pairwise signal separation ||Delta Y_q - Delta Y_r||.

    Args:
        A_nominal: (M, E) nominal forward operator.
        A_defect_q: (M, E) operator for defect q.
        A_defect_r: (M, E) operator for defect r.
        current_samples: (E, K) sample current vectors.

    Returns dict with pairwise signal metrics.
    """
    if current_samples.ndim == 1:
        current_samples = current_samples[:, None]

    K = current_samples.shape[1]
    pair_deltas = []

    for k in range(K):
        i_k = current_samples[:, k]
        delta_q = (A_defect_q - A_nominal) @ i_k
        delta_r = (A_defect_r - A_nominal) @ i_k
        pair_delta = np.linalg.norm(delta_q - delta_r)
        pair_deltas.append(float(pair_delta))

    return {
        "pairwise_delta_max": max(pair_deltas),
        "pairwise_delta_mean": float(np.mean(pair_deltas)),
        "pairwise_delta_median": float(np.median(pair_deltas)),
        "pairwise_delta_min": min(pair_deltas),
    }


def compute_pairwise_gamma(
    A_nominal: np.ndarray,
    all_defect_operators: dict[str, np.ndarray],
    current_samples: np.ndarray,
    rho_components: dict,
    epsilon: float,
    tau: float,
) -> list[dict]:
    """Compute pairwise Gamma for all defect pairs.

    Gamma^{cons}_{qr} = ||Delta Y_q - Delta Y_r|| - epsilon - tau - rho_q - rho_r

    Uses the same rho for all defects (conservative bound) since all
    defects share the same nominal operator.
    """
    rho_cons = rho_components["rho_combined_conservative"]["absolute_radius"]
    rho_rss = rho_components["rho_combined_rss"]["absolute_radius"]

    defect_ids = sorted(all_defect_operators.keys())
    results = []

    for i, q in enumerate(defect_ids):
        for r in defect_ids[i + 1:]:
            A_q = all_defect_operators[q]
            A_r = all_defect_operators[r]

            pair_delta = compute_pairwise_delta(
                A_nominal, A_q, A_r, current_samples,
            )

            max_delta = pair_delta["pairwise_delta_max"]

            gamma_cons = max_delta - epsilon - tau - 2 * rho_cons
            gamma_rss = max_delta - epsilon - tau - 2 * rho_rss

            results.append({
                "defect_q": q,
                "defect_r": r,
                "pairwise_delta_max": max_delta,
                "pairwise_delta_median": pair_delta["pairwise_delta_median"],
                "gamma_conservative": gamma_cons,
                "gamma_rss": gamma_rss,
                "conservative_pass": gamma_cons > 0,
                "rss_pass": gamma_rss > 0,
                "epsilon": epsilon,
                "tau": tau,
                "rho_q": rho_cons,
                "rho_r": rho_cons,
            })

    return results


def compute_pairwise_rates(pairwise_results: list[dict]) -> dict:
    """Compute aggregate pairwise certificate rates."""
    n = max(len(pairwise_results), 1)
    n_cons_pass = sum(1 for p in pairwise_results if p["conservative_pass"])
    n_rss_pass = sum(1 for p in pairwise_results if p["rss_pass"])

    return {
        "pairwise_count": n,
        "pairwise_conservative_pass_count": n_cons_pass,
        "pairwise_rss_pass_count": n_rss_pass,
        "pairwise_conservative_gamma_rate": n_cons_pass / n,
        "pairwise_rss_gamma_rate": n_rss_pass / n,
    }
