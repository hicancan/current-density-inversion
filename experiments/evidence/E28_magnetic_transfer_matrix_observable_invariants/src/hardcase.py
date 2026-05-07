"""Hard-case nuisance sweeps for E28 quotient certificates."""

from __future__ import annotations

from copy import deepcopy

from margins import compute_robust_margins
from nuisance import nuisance_audit


def run_gain_hardcase_sweep(
    bundle,
    cfg: dict,
    cond_models: dict,
    ports,
    T_matrices: dict,
    pairwise_distances: dict,
    eps_invariant: dict[str, float],
    tau: float,
) -> dict:
    """Stress raw observations against gain nuisance and test Gram quotient survival.

    The hard case is deliberately not a new physical claim. It isolates the
    nuisance family for which a Gram invariant should matter most: per-channel
    observation gain. A useful E28 result must show a regime where raw quotient
    margins fail, Gram quotient margins remain positive, and the known H1/H2
    hard pair remains reported as unresolved.
    """
    magnitudes = cfg.get("hardcase_gain_magnitudes", [0.02, 0.05, 0.08, 0.12, 0.18])
    rows = []

    for magnitude in magnitudes:
        hard_cfg = deepcopy(cfg)
        hard_cfg["nuisance_types"] = ["gain_variation"]
        hard_cfg["nuisance_magnitudes"] = [float(magnitude)]

        nuisance_result = nuisance_audit(bundle, hard_cfg, cond_models, ports, T_matrices)
        margins = compute_robust_margins(
            pairwise_distances,
            nuisance_result,
            eps_invariant,
            tau,
        )
        quotient = margins.get("observable_quotient", {}).get("representations", {})
        raw = quotient.get("raw", {})
        gram = quotient.get("gram", {})
        summary = margins.get("summary", {})
        aggregate = nuisance_result.get("aggregate", {})

        rows.append({
            "gain_magnitude": float(magnitude),
            "raw_quotient_min_gamma": raw.get("quotient_min_gamma", float("-inf")),
            "gram_quotient_min_gamma": gram.get("quotient_min_gamma", float("-inf")),
            "raw_quotient_positive_rate": raw.get("quotient_positive_rate", 0.0),
            "gram_quotient_positive_rate": gram.get("quotient_positive_rate", 0.0),
            "raw_quotient_pass": bool(raw.get("quotient_all_positive", False)),
            "gram_quotient_pass": bool(gram.get("quotient_all_positive", False)),
            "raw_full_positive_rate": summary.get("positive_gamma_raw_rate", 0.0),
            "gram_full_positive_rate": summary.get("positive_gamma_gram_rate", 0.0),
            "raw_h1h2_gamma": raw.get("hard_h1_h2_gamma", float("-inf")),
            "gram_h1h2_gamma": gram.get("hard_h1_h2_gamma", float("-inf")),
            "raw_h1h2_unresolved": bool(raw.get("hard_h1_h2_unresolved", False)),
            "gram_h1h2_unresolved": bool(gram.get("hard_h1_h2_unresolved", False)),
            "rho_raw": aggregate.get("rho_raw", 0.0),
            "rho_gram": aggregate.get("rho_gram", 0.0),
            "raw_fails_gram_passes": (
                not bool(raw.get("quotient_all_positive", False))
                and bool(gram.get("quotient_all_positive", False))
            ),
        })

    raw_fails_gram_pass_rows = [r for r in rows if r["raw_fails_gram_passes"]]
    gram_pass_rows = [r for r in rows if r["gram_quotient_pass"]]
    max_gain_with_gram = max((r["gain_magnitude"] for r in gram_pass_rows), default=None)
    first_raw_fail_gram_pass = (
        raw_fails_gram_pass_rows[0]["gain_magnitude"]
        if raw_fails_gram_pass_rows else None
    )

    return {
        "description": (
            "Gain-only nuisance sweep: certificate is useful when raw quotient "
            "margins fail but Gram quotient margins remain positive."
        ),
        "rows": rows,
        "summary": {
            "sweep_count": len(rows),
            "raw_fails_gram_pass_count": len(raw_fails_gram_pass_rows),
            "first_raw_fail_gram_pass_gain": first_raw_fail_gram_pass,
            "gram_quotient_survival_rate": (
                len(gram_pass_rows) / max(len(rows), 1)
            ),
            "max_gain_with_gram_quotient_positive": max_gain_with_gram,
            "hard_h1_h2_still_unresolved_all": all(
                r["gram_h1h2_unresolved"] for r in rows
            ) if rows else False,
        },
    }
