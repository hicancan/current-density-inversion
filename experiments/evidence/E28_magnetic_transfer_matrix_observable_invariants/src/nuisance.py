"""Nuisance perturbation ladder for E28.

Applies structured perturbations to the forward operator to estimate
the empirical nuisance radius rho for each invariant representation.

Perturbation types:
- height_jitter: random sensor height variation
- grid_shift: sub-pixel grid registration error
- gain_variation: per-channel sensitivity variation
"""

from __future__ import annotations

import numpy as np

from operators import OperatorBundle, build_operator_and_graph, PortExcitation
from hypotheses import build_conductance_model, ConductanceModel
from transfer_matrix import compute_transfer_matrix
from invariants import (
    column_space_projector,
    whitened_gram,
    differential_matrix,
)

_PERTURBATION_SEED_OFFSETS = {
    "height_jitter": 101,
    "grid_shift": 202,
    "gain_variation": 303,
}


def _build_perturbed_bundle(
    base_bundle: OperatorBundle,
    cfg: dict,
    perturbation_type: str,
    magnitude: float,
    rng: np.random.Generator,
) -> OperatorBundle:
    """Build a perturbed OperatorBundle."""
    n = int(cfg["grid_size"])
    layers = int(cfg["layer_count"])
    pitch = float(cfg["pixel_pitch_um"])
    dz = float(cfg["layer_spacing_um"])
    sensor_h = float(cfg["sensor_heights_um"][0])

    if perturbation_type == "height_jitter":
        h_perturbed = sensor_h * (1.0 + magnitude * rng.normal())
        return build_operator_and_graph(n, layers, pitch, dz, max(h_perturbed, 0.1))

    elif perturbation_type == "grid_shift":
        shift = magnitude * rng.normal(size=2)
        pitch_shifted = pitch * (1.0 + shift[0])
        dz_shifted = dz * (1.0 + shift[1])
        return build_operator_and_graph(n, layers, max(pitch_shifted, 0.1), max(dz_shifted, 0.01), sensor_h)

    elif perturbation_type == "gain_variation":
        # Apply gain perturbation to A, keep D the same
        A_pert = base_bundle.A.copy()
        gain = 1.0 + magnitude * rng.normal(size=(A_pert.shape[0], 1))
        A_pert = A_pert * gain
        return __import__("dataclasses").replace(base_bundle, A=A_pert)

    else:
        return base_bundle


def compute_nuisance_radius(
    bundle: OperatorBundle,
    cfg: dict,
    hypothesis: str,
    cond_model: ConductanceModel,
    ports: PortExcitation,
    T_base: np.ndarray,
    perturbation_type: str,
    magnitude: float,
    n_samples: int = 8,
) -> dict:
    """Estimate rho for one perturbation type and magnitude.

    rho = max ||Phi(T_perturbed) - Phi(T_base)||

    Returns max norm across samples for each invariant.
    """
    seed_offset = _PERTURBATION_SEED_OFFSETS.get(perturbation_type, 999)
    rng = np.random.default_rng(int(cfg["random_seed"]) + seed_offset)

    max_proj = 0.0
    max_gram = 0.0
    max_diff = 0.0
    max_raw = 0.0

    P_base, _ = column_space_projector(T_base)
    G_base = whitened_gram(T_base)
    D_base = differential_matrix(T_base)

    for _ in range(n_samples):
        pert_bundle = _build_perturbed_bundle(bundle, cfg, perturbation_type, magnitude, rng)
        pert_cond = build_conductance_model(pert_bundle, cfg, hypothesis)
        T_pert = compute_transfer_matrix(pert_bundle, pert_cond, ports)

        # Raw perturbation
        delta_raw = float(np.linalg.norm(T_pert - T_base, "fro"))
        max_raw = max(max_raw, delta_raw)

        # Projector perturbation
        P_pert, _ = column_space_projector(T_pert)
        if P_base.shape == P_pert.shape:
            delta_proj = float(np.linalg.norm(P_pert - P_base, "fro") / np.sqrt(2.0))
            max_proj = max(max_proj, delta_proj)

        # Gram perturbation
        G_pert = whitened_gram(T_pert)
        if G_base.shape == G_pert.shape:
            delta_gram = float(np.linalg.norm(G_pert - G_base, "fro"))
            max_gram = max(max_gram, delta_gram)

        # Differential perturbation
        D_pert = differential_matrix(T_pert)
        if D_base.shape == D_pert.shape:
            delta_diff = float(np.linalg.norm(D_pert - D_base, "fro"))
            max_diff = max(max_diff, delta_diff)

    return {
        "perturbation_type": perturbation_type,
        "magnitude": magnitude,
        "rho_raw": max_raw,
        "rho_projector": max_proj,
        "rho_gram": max_gram,
        "rho_differential": max_diff,
    }


def nuisance_audit(
    bundle: OperatorBundle,
    cfg: dict,
    cond_models: dict[str, ConductanceModel],
    ports: PortExcitation,
    T_matrices: dict[str, np.ndarray],
) -> dict:
    """Run full nuisance perturbation ladder for all hypotheses and perturbation types.

    Returns per-hypothesis and aggregate nuisance radii.
    """
    pert_types = cfg["nuisance_types"]
    magnitudes = cfg["nuisance_magnitudes"]
    n_samples = 5  # fewer for speed

    all_results = {}
    per_h = {h: {"rho_raw": 0.0, "rho_projector": 0.0, "rho_gram": 0.0, "rho_differential": 0.0}
             for h in cond_models}

    for h, T_base in T_matrices.items():
        h_results = []
        for ptype in pert_types:
            for mag in magnitudes:
                r = compute_nuisance_radius(
                    bundle, cfg, h, cond_models[h], ports, T_base,
                    ptype, mag, n_samples=n_samples,
                )
                h_results.append(r)
                per_h[h]["rho_raw"] = max(per_h[h]["rho_raw"], r["rho_raw"])
                per_h[h]["rho_projector"] = max(per_h[h]["rho_projector"], r["rho_projector"])
                per_h[h]["rho_gram"] = max(per_h[h]["rho_gram"], r["rho_gram"])
                per_h[h]["rho_differential"] = max(per_h[h]["rho_differential"], r["rho_differential"])
        all_results[h] = h_results

    # Aggregate: max across hypotheses
    aggregate = {
        "rho_raw": max(per_h[h]["rho_raw"] for h in per_h),
        "rho_projector": max(per_h[h]["rho_projector"] for h in per_h),
        "rho_gram": max(per_h[h]["rho_gram"] for h in per_h),
        "rho_differential": max(per_h[h]["rho_differential"] for h in per_h),
    }

    return {
        "per_hypothesis": per_h,
        "per_perturbation": all_results,
        "aggregate": aggregate,
        "perturbation_types": pert_types,
        "magnitudes": magnitudes,
        "n_samples_per": n_samples,
    }


def nuisance_reduction_factor(nuisance_audit_result: dict) -> dict:
    """Compute reduction factors: rho_invariant / rho_raw.

    Values < 1 indicate the invariant reduces nuisance sensitivity.
    """
    agg = nuisance_audit_result["aggregate"]
    rho_raw = max(agg["rho_raw"], 1e-14)
    return {
        "projector_reduction": agg["rho_projector"] / rho_raw,
        "gram_reduction": agg["rho_gram"] / rho_raw,
        "differential_reduction": agg["rho_differential"] / rho_raw,
    }
