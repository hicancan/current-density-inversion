"""Directional statistical certificates for E28 transfer matrices.

E28's original robust margin subtracts a full feature-space noise ball. That is
deliberately conservative, but binary hypothesis testing is controlled by the
noise and nuisance projected onto the hypothesis-separation direction. This
module computes that matched-filter style certificate for raw transfer matrices
and for the whitened Gram invariant.
"""

from __future__ import annotations

import numpy as np

from distances import HYP_PAIRS
from hypotheses import build_conductance_model
from invariants import whitened_gram
from margins import observable_quotient_pair_keys
from nuisance import _PERTURBATION_SEED_OFFSETS, _build_perturbed_bundle
from transfer_matrix import compute_transfer_matrix

FEATURE_NAMES = ("raw", "gram")
HARD_H1_H2_KEY = "H1_via__H2_model_gap"


def _feature(T: np.ndarray, name: str) -> np.ndarray:
    if name == "raw":
        return T.reshape(-1)
    if name == "gram":
        return whitened_gram(T).reshape(-1)
    raise ValueError(f"Unknown directional feature: {name}")


def _pair_key(hi: str, hj: str) -> str:
    pair = (hi, hj)
    if pair in HYP_PAIRS:
        return f"{hi}__{hj}"
    reverse = (hj, hi)
    if reverse in HYP_PAIRS:
        return f"{hj}__{hi}"
    return f"{hi}__{hj}"


def _configured_list(cfg: dict, key: str, default: list[float]) -> list[float]:
    values = cfg.get(key, default)
    if not isinstance(values, list) or not values:
        return default
    return [float(v) for v in values]


def _direction_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"std": 0.0, "max_abs": 0.0}
    arr = np.asarray(values, dtype=float)
    return {
        "std": float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0,
        "max_abs": float(np.max(np.abs(arr))),
    }


def _noise_feature_deltas(
    T_base: np.ndarray,
    feature_name: str,
    sigma: float,
    n_samples: int,
    seed: int,
) -> list[np.ndarray]:
    if feature_name == "raw":
        return []

    rng = np.random.default_rng(seed)
    f0 = _feature(T_base, feature_name)
    deltas = []
    for _ in range(n_samples):
        T_noisy = T_base + rng.normal(0.0, sigma, size=T_base.shape)
        deltas.append(_feature(T_noisy, feature_name) - f0)
    return deltas


def _precompute_noise_deltas(
    T_matrices: dict[str, np.ndarray],
    cfg: dict,
) -> dict[str, dict[str, list[np.ndarray]]]:
    sigma = float(cfg["noise_sigma"])
    n_samples = int(cfg.get("directional_noise_samples", 200))
    seed = int(cfg.get("random_seed", 0)) + 7801

    result: dict[str, dict[str, list[np.ndarray]]] = {name: {} for name in FEATURE_NAMES}
    for name in FEATURE_NAMES:
        for offset, (h, T) in enumerate(T_matrices.items()):
            result[name][h] = _noise_feature_deltas(
                T, name, sigma, n_samples, seed + 97 * offset
            )
    return result


def _precompute_nuisance_deltas(
    bundle,
    cfg: dict,
    ports,
    T_matrices: dict[str, np.ndarray],
) -> dict[str, dict[str, list[np.ndarray]]]:
    perturbation_types = cfg.get(
        "directional_nuisance_types",
        cfg.get("nuisance_types", []),
    )
    magnitudes = _configured_list(
        cfg,
        "directional_nuisance_magnitudes",
        _configured_list(cfg, "nuisance_magnitudes", [0.02]),
    )
    n_samples = int(cfg.get("directional_nuisance_samples", 5))

    result: dict[str, dict[str, list[np.ndarray]]] = {
        name: {h: [] for h in T_matrices}
        for name in FEATURE_NAMES
    }
    base_features = {
        name: {h: _feature(T, name) for h, T in T_matrices.items()}
        for name in FEATURE_NAMES
    }

    for hypothesis, T_base in T_matrices.items():
        for perturbation_type in perturbation_types:
            seed_offset = _PERTURBATION_SEED_OFFSETS.get(str(perturbation_type), 999)
            for magnitude in magnitudes:
                rng = np.random.default_rng(int(cfg["random_seed"]) + seed_offset)
                for _ in range(n_samples):
                    pert_bundle = _build_perturbed_bundle(
                        bundle,
                        cfg,
                        str(perturbation_type),
                        float(magnitude),
                        rng,
                    )
                    pert_cond = build_conductance_model(pert_bundle, cfg, hypothesis)
                    T_pert = compute_transfer_matrix(pert_bundle, pert_cond, ports)
                    for name in FEATURE_NAMES:
                        result[name][hypothesis].append(
                            _feature(T_pert, name) - base_features[name][hypothesis]
                        )

    return result


def _noise_radius_along_direction(
    feature_name: str,
    noise_deltas: dict[str, dict[str, list[np.ndarray]]],
    hi: str,
    hj: str,
    direction: np.ndarray,
    cfg: dict,
) -> dict:
    z = float(cfg.get("directional_z_threshold", 3.0))
    if feature_name == "raw":
        std = float(cfg["noise_sigma"])
        return {
            "std_hi": std,
            "std_hj": std,
            "std": std,
            "z": z,
            "z_noise_radius": z * std,
            "estimator": "exact_raw_unit_direction",
        }

    vals_i = [float(np.dot(d, direction)) for d in noise_deltas[feature_name][hi]]
    vals_j = [float(np.dot(d, direction)) for d in noise_deltas[feature_name][hj]]
    stats_i = _direction_stats(vals_i)
    stats_j = _direction_stats(vals_j)
    std = max(stats_i["std"], stats_j["std"])
    return {
        "std_hi": stats_i["std"],
        "std_hj": stats_j["std"],
        "std": std,
        "z": z,
        "z_noise_radius": z * std,
        "estimator": "empirical_directional_projection_std",
    }


def _nuisance_radius_along_direction(
    feature_name: str,
    nuisance_deltas: dict[str, dict[str, list[np.ndarray]]],
    hypothesis: str,
    direction: np.ndarray,
) -> float:
    values = [
        float(np.dot(delta, direction))
        for delta in nuisance_deltas[feature_name][hypothesis]
    ]
    return _direction_stats(values)["max_abs"]


def _feature_rows(
    feature_name: str,
    T_matrices: dict[str, np.ndarray],
    noise_deltas: dict[str, dict[str, list[np.ndarray]]],
    nuisance_deltas: dict[str, dict[str, list[np.ndarray]]],
    cfg: dict,
) -> list[dict]:
    tau = float(cfg.get("directional_tau", cfg.get("invariant_eps_threshold", 0.01)))
    features = {h: _feature(T, feature_name) for h, T in T_matrices.items()}
    rows = []

    for hi, hj in HYP_PAIRS:
        pair_key = _pair_key(hi, hj)
        delta_vec = features[hi] - features[hj]
        delta = float(np.linalg.norm(delta_vec))
        direction = delta_vec / max(delta, 1e-30)
        noise = _noise_radius_along_direction(
            feature_name, noise_deltas, hi, hj, direction, cfg
        )
        rho_i = _nuisance_radius_along_direction(
            feature_name, nuisance_deltas, hi, direction
        )
        rho_j = _nuisance_radius_along_direction(
            feature_name, nuisance_deltas, hj, direction
        )
        gamma = delta - noise["z_noise_radius"] - rho_i - rho_j - tau
        rows.append({
            "pair": pair_key,
            "hypotheses": [hi, hj],
            "feature": feature_name,
            "delta_directional": delta,
            "noise_radius_directional": noise["z_noise_radius"],
            "noise_std_directional": noise["std"],
            "noise_estimator": noise["estimator"],
            "z_threshold": noise["z"],
            "rho_directional_hi": rho_i,
            "rho_directional_hj": rho_j,
            "tau": tau,
            "gamma_directional": float(gamma),
            "positive": bool(gamma > 0.0),
        })
    return rows


def _feature_summary(rows: list[dict]) -> dict:
    quotient_keys = observable_quotient_pair_keys()
    quotient_rows = [r for r in rows if r["pair"] in quotient_keys]
    gammas = [float(r["gamma_directional"]) for r in rows]
    quotient_gammas = [float(r["gamma_directional"]) for r in quotient_rows]
    hard = next((r for r in rows if r["pair"] == HARD_H1_H2_KEY), None)

    return {
        "pair_count": len(rows),
        "positive_count": sum(1 for r in rows if r["positive"]),
        "positive_rate": sum(1 for r in rows if r["positive"]) / max(len(rows), 1),
        "min_gamma": float(np.min(gammas)) if gammas else float("-inf"),
        "mean_gamma": float(np.mean(gammas)) if gammas else float("-inf"),
        "quotient_pair_count": len(quotient_rows),
        "quotient_positive_count": sum(1 for r in quotient_rows if r["positive"]),
        "quotient_positive_rate": (
            sum(1 for r in quotient_rows if r["positive"]) / max(len(quotient_rows), 1)
        ),
        "quotient_min_gamma": (
            float(np.min(quotient_gammas)) if quotient_gammas else float("-inf")
        ),
        "quotient_all_positive": all(r["positive"] for r in quotient_rows),
        "hard_h1_h2_gamma": (
            float(hard["gamma_directional"]) if hard else float("-inf")
        ),
        "hard_h1_h2_positive": bool(hard["positive"]) if hard else False,
    }


def run_directional_statistical_certificate(
    bundle,
    cfg: dict,
    ports,
    T_matrices: dict[str, np.ndarray],
    baseline_margins: dict,
) -> dict:
    """Compute directional matched-filter certificates for raw and Gram features."""
    noise_deltas = _precompute_noise_deltas(T_matrices, cfg)
    nuisance_deltas = _precompute_nuisance_deltas(bundle, cfg, ports, T_matrices)

    feature_results = {}
    for feature_name in FEATURE_NAMES:
        rows = _feature_rows(
            feature_name,
            T_matrices,
            noise_deltas,
            nuisance_deltas,
            cfg,
        )
        feature_results[feature_name] = {
            "rows": rows,
            "summary": _feature_summary(rows),
        }

    baseline_quotient = baseline_margins.get("observable_quotient", {})
    baseline_min = float(
        baseline_quotient.get("selected_invariant_quotient_min_gamma", float("-inf"))
    )
    gram_min = feature_results["gram"]["summary"]["quotient_min_gamma"]
    gram_hard = feature_results["gram"]["summary"]["hard_h1_h2_gamma"]

    return {
        "description": (
            "Directional matched-filter certificate: subtract noise and nuisance "
            "only along each hypothesis-separation direction, rather than using "
            "a full feature-space noise ball."
        ),
        "features": feature_results,
        "summary": {
            "z_threshold": float(cfg.get("directional_z_threshold", 3.0)),
            "directional_tau": float(
                cfg.get("directional_tau", cfg.get("invariant_eps_threshold", 0.01))
            ),
            "baseline_selected_quotient_min_gamma": baseline_min,
            "directional_gram_quotient_min_gamma": gram_min,
            "directional_gram_quotient_improvement": gram_min - baseline_min,
            "directional_gram_quotient_all_positive": bool(
                feature_results["gram"]["summary"]["quotient_all_positive"]
            ),
            "directional_gram_h1_h2_gamma": gram_hard,
            "directional_gram_h1_h2_positive": bool(
                feature_results["gram"]["summary"]["hard_h1_h2_positive"]
            ),
            "directional_raw_h1_h2_gamma": feature_results["raw"]["summary"][
                "hard_h1_h2_gamma"
            ],
            "directional_raw_h1_h2_positive": bool(
                feature_results["raw"]["summary"]["hard_h1_h2_positive"]
            ),
        },
        "cannot_claim": [
            "full H1_via versus H2_model_gap separation unless hard-pair gamma is positive",
            "real-chip detection risk control",
            "replacement for external-solver or real-data validation",
            "that directional Gaussian assumptions cover all structured noise",
        ],
    }
