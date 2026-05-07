"""H1/H2 robust-separability phase diagram for E28.

The original E28 run finds a positive observable quotient certificate while
leaving H1_via vs H2_model_gap unresolved. This module asks whether that
boundary is a single hard-coded accident or a stable phase boundary under
controlled H2 model-gap severity.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Iterable

import numpy as np

from distances import compute_all_pairwise_distances
from hypotheses import (
    HYPOTHESES,
    ConductanceModel,
    build_all_conductance_models,
)
from margins import compute_robust_margins
from nuisance import compute_nuisance_radius
from transfer_matrix import compute_all_transfer_matrices

H1_H2_PAIR_KEY = "H1_via__H2_model_gap"


def _float_list(values: Iterable[float]) -> list[float]:
    return [float(v) for v in values]


def _configured_list(cfg: dict, key: str, default: list[float]) -> list[float]:
    values = cfg.get(key, default)
    if not isinstance(values, list) or not values:
        return default
    return _float_list(values)


def _max_radii(rows: list[dict]) -> dict[str, float]:
    keys = ("rho_raw", "rho_projector", "rho_gram", "rho_differential")
    return {k: max((float(r.get(k, 0.0)) for r in rows), default=0.0) for k in keys}


def _aggregate_radii(per_hypothesis: dict[str, dict[str, float]]) -> dict[str, float]:
    keys = ("rho_raw", "rho_projector", "rho_gram", "rho_differential")
    return {
        k: max((float(v.get(k, 0.0)) for v in per_hypothesis.values()), default=0.0)
        for k in keys
    }


def _phase_nuisance_rows(
    bundle,
    cfg: dict,
    hypothesis: str,
    cond_model: ConductanceModel,
    ports,
    T_base: np.ndarray,
) -> list[dict]:
    perturbation_types = cfg.get("phase_nuisance_types", cfg.get("nuisance_types", []))
    magnitudes = _configured_list(
        cfg,
        "phase_nuisance_magnitudes",
        [max(_configured_list(cfg, "nuisance_magnitudes", [0.02]))],
    )
    n_samples = int(cfg.get("phase_nuisance_samples", 2))

    rows: list[dict] = []
    for perturbation_type in perturbation_types:
        for magnitude in magnitudes:
            rows.append(
                compute_nuisance_radius(
                    bundle,
                    cfg,
                    hypothesis,
                    cond_model,
                    ports,
                    T_base,
                    str(perturbation_type),
                    float(magnitude),
                    n_samples=n_samples,
                )
            )
    return rows


def _base_phase_radii(bundle, cfg: dict, ports, T_matrices: dict) -> tuple[dict, dict]:
    cond_models = build_all_conductance_models(bundle, cfg)
    per_hypothesis: dict[str, dict[str, float]] = {}
    per_perturbation: dict[str, list[dict]] = {}

    for hypothesis in ("H0_no_via", "H1_via", "H3_return_path"):
        rows = _phase_nuisance_rows(
            bundle,
            cfg,
            hypothesis,
            cond_models[hypothesis],
            ports,
            T_matrices[hypothesis],
        )
        per_hypothesis[hypothesis] = _max_radii(rows)
        per_perturbation[hypothesis] = rows

    return per_hypothesis, per_perturbation


def _make_nuisance_result(
    cfg: dict,
    per_hypothesis: dict[str, dict[str, float]],
    per_perturbation: dict[str, list[dict]],
) -> dict:
    return {
        "per_hypothesis": per_hypothesis,
        "per_perturbation": per_perturbation,
        "aggregate": _aggregate_radii(per_hypothesis),
        "perturbation_types": cfg.get("phase_nuisance_types", cfg.get("nuisance_types", [])),
        "magnitudes": cfg.get(
            "phase_nuisance_magnitudes",
            [max(_configured_list(cfg, "nuisance_magnitudes", [0.02]))],
        ),
        "n_samples_per": int(cfg.get("phase_nuisance_samples", 2)),
    }


def _frontier_by_jitter(rows: list[dict]) -> list[dict]:
    jitters = sorted({float(r["h2_sheet_jitter"]) for r in rows})
    frontier = []
    for jitter in jitters:
        subset = [r for r in rows if float(r["h2_sheet_jitter"]) == jitter]
        positive = [r for r in subset if bool(r["h1_h2_gram_positive"])]
        frontier.append(
            {
                "h2_sheet_jitter": jitter,
                "max_h2_via_factor_with_positive_gram_gamma": (
                    max(float(r["h2_via_factor"]) for r in positive)
                    if positive else None
                ),
                "min_via_contrast_with_positive_gram_gamma": (
                    min(abs(1.0 - float(r["h2_via_factor"])) for r in positive)
                    if positive else None
                ),
                "positive_count": len(positive),
                "row_count": len(subset),
            }
        )
    return frontier


def _closest_default_row(rows: list[dict], cfg: dict) -> dict:
    default_factor = float(cfg.get("h2_via_factor", 0.82))
    default_jitter = float(cfg.get("h2_sheet_jitter", 0.03))
    return min(
        rows,
        key=lambda r: (
            abs(float(r["h2_via_factor"]) - default_factor),
            abs(float(r["h2_sheet_jitter"]) - default_jitter),
        ),
    )


def _summarize(rows: list[dict], cfg: dict) -> dict:
    gram_gammas = [float(r["h1_h2_gamma_gram"]) for r in rows]
    raw_gammas = [float(r["h1_h2_gamma_raw"]) for r in rows]
    positive = [r for r in rows if bool(r["h1_h2_gram_positive"])]
    zero_noise_positive = [r for r in rows if bool(r["h1_h2_zero_noise_gram_positive"])]
    quotient_positive = [r for r in rows if bool(r["gram_quotient_pass"])]
    default_row = _closest_default_row(rows, cfg) if rows else {}

    min_via_contrast = (
        min(abs(1.0 - float(r["h2_via_factor"])) for r in positive)
        if positive else None
    )
    max_factor_positive = (
        max(float(r["h2_via_factor"]) for r in positive)
        if positive else None
    )

    return {
        "row_count": len(rows),
        "h1_h2_gram_positive_count": len(positive),
        "h1_h2_gram_positive_rate": len(positive) / max(len(rows), 1),
        "h1_h2_raw_positive_count": sum(1 for v in raw_gammas if v > 0.0),
        "h1_h2_raw_positive_rate": sum(1 for v in raw_gammas if v > 0.0) / max(len(rows), 1),
        "h1_h2_gram_max_gamma": float(np.max(gram_gammas)) if gram_gammas else float("-inf"),
        "h1_h2_gram_min_gamma": float(np.min(gram_gammas)) if gram_gammas else float("-inf"),
        "h1_h2_raw_max_gamma": float(np.max(raw_gammas)) if raw_gammas else float("-inf"),
        "h1_h2_raw_min_gamma": float(np.min(raw_gammas)) if raw_gammas else float("-inf"),
        "max_h2_via_factor_with_h1_h2_gram_positive": max_factor_positive,
        "min_via_contrast_with_h1_h2_gram_positive": min_via_contrast,
        "default_h2_via_factor": float(cfg.get("h2_via_factor", 0.82)),
        "default_h2_sheet_jitter": float(cfg.get("h2_sheet_jitter", 0.03)),
        "nearest_default_row": default_row,
        "default_h1_h2_gram_positive": bool(default_row.get("h1_h2_gram_positive", False)),
        "default_h1_h2_gamma_gram": float(default_row.get("h1_h2_gamma_gram", float("-inf"))),
        "default_h1_h2_zero_noise_gamma_gram": float(
            default_row.get("h1_h2_zero_noise_gamma_gram", float("-inf"))
        ),
        "default_h1_h2_actual_eps_plus_rho_gram": float(
            default_row.get("h1_h2_actual_eps_plus_rho_gram", float("inf"))
        ),
        "default_h1_h2_required_eps_plus_rho_gram": float(
            default_row.get("h1_h2_required_eps_plus_rho_gram", float("inf"))
        ),
        "default_h1_h2_budget_gap_gram": float(
            default_row.get("h1_h2_budget_gap_gram", float("inf"))
        ),
        "h1_h2_zero_noise_gram_positive_count": len(zero_noise_positive),
        "h1_h2_zero_noise_gram_positive_rate": (
            len(zero_noise_positive) / max(len(rows), 1)
        ),
        "gram_quotient_survival_rate": len(quotient_positive) / max(len(rows), 1),
        "frontier_by_sheet_jitter": _frontier_by_jitter(rows),
        "phase_boundary_explicit": len(rows) > 0,
        "conditional_h1_h2_separation_region_found": len(positive) > 0,
    }


def run_h1_h2_phase_diagram(
    bundle,
    cfg: dict,
    ports,
    base_T_matrices: dict[str, np.ndarray],
    eps_invariant: dict[str, float],
    tau: float,
) -> dict:
    """Sweep H2 severity and report robust H1/H2 separability.

    The diagram varies two interpretable H2 controls:
    - h2_via_factor: apparent via conductance relative to H1 nominal via.
    - h2_sheet_jitter: random sheet-conductance drift magnitude.

    Each row recomputes transfer matrices and a reduced, explicit nuisance
    budget. A positive H1/H2 Gamma is therefore a conditional separability
    result under that row's H2 severity, not a full real-chip claim.
    """
    factors = _configured_list(
        cfg,
        "phase_h2_via_factors",
        [0.2, 0.35, 0.5, 0.65, 0.75, 0.82, 0.9, 0.97],
    )
    jitters = _configured_list(
        cfg,
        "phase_h2_sheet_jitters",
        [0.0, 0.01, 0.03, 0.06],
    )

    fixed_radii, fixed_perturbations = _base_phase_radii(
        bundle, cfg, ports, base_T_matrices
    )

    rows: list[dict] = []
    for h2_via_factor in factors:
        for h2_sheet_jitter in jitters:
            row_cfg = deepcopy(cfg)
            row_cfg["h2_via_factor"] = float(h2_via_factor)
            row_cfg["h2_sheet_jitter"] = float(h2_sheet_jitter)

            cond_models = build_all_conductance_models(bundle, row_cfg)
            T_matrices = compute_all_transfer_matrices(bundle, cond_models, ports)
            distances = compute_all_pairwise_distances(T_matrices)

            h2_perturbations = _phase_nuisance_rows(
                bundle,
                row_cfg,
                "H2_model_gap",
                cond_models["H2_model_gap"],
                ports,
                T_matrices["H2_model_gap"],
            )
            per_hypothesis = dict(fixed_radii)
            per_hypothesis["H2_model_gap"] = _max_radii(h2_perturbations)
            per_perturbation = dict(fixed_perturbations)
            per_perturbation["H2_model_gap"] = h2_perturbations

            nuisance_result = _make_nuisance_result(
                row_cfg, per_hypothesis, per_perturbation
            )
            margins = compute_robust_margins(
                distances,
                nuisance_result,
                eps_invariant,
                tau,
            )

            h1_h2 = margins["pairs"][H1_H2_PAIR_KEY]
            quotient = margins.get("observable_quotient", {}).get("representations", {})
            raw_q = quotient.get("raw", {})
            gram_q = quotient.get("gram", {})
            summary = margins.get("summary", {})
            gram_delta = float(h1_h2.get("delta_gram", 0.0))
            gram_eps = float(h1_h2.get("eps_gram", 0.0))
            gram_rho_h1 = float(per_hypothesis["H1_via"]["rho_gram"])
            gram_rho_h2 = float(per_hypothesis["H2_model_gap"]["rho_gram"])
            gram_tau = float(h1_h2.get("tau", tau))
            required_eps_plus_rho = max(gram_delta - gram_tau, 0.0)
            actual_eps_plus_rho = gram_eps + gram_rho_h1 + gram_rho_h2
            zero_noise_gamma = gram_delta - gram_rho_h1 - gram_rho_h2 - gram_tau

            rows.append(
                {
                    "h2_via_factor": float(h2_via_factor),
                    "h2_sheet_jitter": float(h2_sheet_jitter),
                    "h1_h2_delta_raw": float(h1_h2.get("delta_raw_frobenius", 0.0)),
                    "h1_h2_delta_gram": gram_delta,
                    "h1_h2_delta_projector": float(h1_h2.get("delta_projector", 0.0)),
                    "h1_h2_delta_differential": float(h1_h2.get("delta_differential", 0.0)),
                    "h1_h2_gamma_raw": float(h1_h2.get("gamma_raw", float("-inf"))),
                    "h1_h2_gamma_gram": float(h1_h2.get("gamma_gram", float("-inf"))),
                    "h1_h2_gamma_projector": float(
                        h1_h2.get("gamma_projector", float("-inf"))
                    ),
                    "h1_h2_gamma_differential": float(
                        h1_h2.get("gamma_differential", float("-inf"))
                    ),
                    "h1_h2_gram_positive": bool(h1_h2.get("gamma_gram", 0.0) > 0.0),
                    "h1_h2_zero_noise_gamma_gram": float(zero_noise_gamma),
                    "h1_h2_zero_noise_gram_positive": bool(zero_noise_gamma > 0.0),
                    "h1_h2_required_eps_plus_rho_gram": float(required_eps_plus_rho),
                    "h1_h2_actual_eps_plus_rho_gram": float(actual_eps_plus_rho),
                    "h1_h2_budget_gap_gram": float(
                        actual_eps_plus_rho - required_eps_plus_rho
                    ),
                    "raw_quotient_min_gamma": float(
                        raw_q.get("quotient_min_gamma", float("-inf"))
                    ),
                    "gram_quotient_min_gamma": float(
                        gram_q.get("quotient_min_gamma", float("-inf"))
                    ),
                    "raw_quotient_pass": bool(raw_q.get("quotient_all_positive", False)),
                    "gram_quotient_pass": bool(gram_q.get("quotient_all_positive", False)),
                    "best_invariant": summary.get("best_invariant", "none"),
                    "positive_gamma_gram_rate": float(
                        summary.get("positive_gamma_gram_rate", 0.0)
                    ),
                    "phase_rho_h1_gram": gram_rho_h1,
                    "phase_rho_h2_gram": gram_rho_h2,
                    "phase_rho_h1_raw": float(per_hypothesis["H1_via"]["rho_raw"]),
                    "phase_rho_h2_raw": float(per_hypothesis["H2_model_gap"]["rho_raw"]),
                }
            )

    summary = _summarize(rows, cfg)
    return {
        "description": (
            "H1/H2 phase diagram over H2 via-conductance severity and sheet drift. "
            "Rows use the same robust Gamma definition with an explicit reduced "
            "phase nuisance budget."
        ),
        "hypotheses": HYPOTHESES,
        "sweep_axes": {
            "h2_via_factors": factors,
            "h2_sheet_jitters": jitters,
            "phase_nuisance_types": cfg.get(
                "phase_nuisance_types", cfg.get("nuisance_types", [])
            ),
            "phase_nuisance_magnitudes": cfg.get(
                "phase_nuisance_magnitudes",
                [max(_configured_list(cfg, "nuisance_magnitudes", [0.02]))],
            ),
            "phase_nuisance_samples": int(cfg.get("phase_nuisance_samples", 2)),
        },
        "rows": rows,
        "summary": summary,
        "cannot_claim": [
            "default H1_via versus H2_model_gap separability unless the default row has positive Gamma",
            "real-chip H1/H2 separation",
            "external-solver or real-data validation",
            "that sheet-drift and via-factor axes span all real model-gap mechanisms",
        ],
    }
