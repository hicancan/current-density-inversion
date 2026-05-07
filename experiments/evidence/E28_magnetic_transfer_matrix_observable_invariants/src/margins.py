"""Robust invariant margins for E28.

For each invariant Phi and hypothesis pair (h, g):

    Gamma^Phi_hg = delta^Phi_hg - eps^Phi - rho^Phi_h - rho^Phi_g - tau^Phi

where:
- delta^Phi_hg = ||Phi(T_h) - Phi(T_g)|| (invariant distance)
- eps^Phi = invariant-specific noise floor (empirically estimated)
- rho^Phi_h = nuisance radius for hypothesis h under invariant Phi
- tau^Phi = invariant-specific acceptance threshold
"""

from __future__ import annotations

import numpy as np

from distances import HYP_PAIRS, CRITICAL_PAIRS
from invariants import (
    column_space_projector,
    whitened_gram,
    differential_matrix,
)

RAW_AND_INVARIANT_NAMES = ("raw", "projector", "gram", "differential")
INVARIANT_NAMES = ("projector", "gram", "differential")

OBSERVABLE_QUOTIENT_GROUPS = {
    "Q0_no_via": ("H0_no_via",),
    "Q12_via_or_model_gap": ("H1_via", "H2_model_gap"),
    "Q3_return_path": ("H3_return_path",),
}

HARD_UNRESOLVED_PAIR = ("H1_via", "H2_model_gap")


def _gamma_key(name: str) -> str:
    if name == "raw":
        return "gamma_raw"
    return f"gamma_{name}"


def _delta_key(name: str) -> str:
    if name == "raw":
        return "delta_raw_frobenius"
    if name == "projector":
        return "delta_projector"
    if name == "gram":
        return "delta_gram"
    if name == "differential":
        return "delta_differential"
    raise KeyError(name)


def _pair_key(hi: str, hj: str) -> str:
    pair = (hi, hj)
    if pair in HYP_PAIRS:
        return f"{hi}__{hj}"
    reverse = (hj, hi)
    if reverse in HYP_PAIRS:
        return f"{hj}__{hi}"
    return f"{hi}__{hj}"


def observable_quotient_pair_keys() -> list[str]:
    """Return hypothesis-pair keys that cross observable quotient groups.

    The quotient deliberately merges H1_via and H2_model_gap because current
    evidence shows that their transfer matrices are too close under the present
    synthetic generator. A valid quotient certificate therefore must separate
    Q0, Q12, and Q3, while explicitly reporting H1/H2 as unresolved.
    """
    pair_keys: list[str] = []
    groups = list(OBSERVABLE_QUOTIENT_GROUPS.values())
    for i, gi in enumerate(groups):
        for gj in groups[i + 1:]:
            for hi in gi:
                for hj in gj:
                    pair_keys.append(_pair_key(hi, hj))
    return pair_keys


def empirical_invariant_epsilon(
    T_ref: np.ndarray,
    noise_sigma: float,
    tau_mult: float,
    n_samples: int = 20,
) -> dict[str, float]:
    """Estimate noise floor epsilon for each invariant in its own units.

    Adds Gaussian noise to T_ref and measures the perturbation to each
    invariant representation. Returns epsilons scaled by tau_mult.
    """
    if T_ref.size == 0:
        return {"eps_raw": 0.0, "eps_projector": 0.0, "eps_gram": 0.0, "eps_differential": 0.0}

    rng = np.random.default_rng(42)
    M, S = T_ref.shape

    P_ref, _ = column_space_projector(T_ref)
    G_ref = whitened_gram(T_ref)
    D_ref = differential_matrix(T_ref)

    raw_deltas = []
    proj_deltas = []
    gram_deltas = []
    diff_deltas = []

    per_element_std = noise_sigma

    for _ in range(n_samples):
        noise = rng.normal(0.0, per_element_std, size=T_ref.shape)
        T_noisy = T_ref + noise

        # Raw: Frobenius norm (grows with sqrt(M*S), correct for sum-of-squares residual)
        raw_deltas.append(float(np.linalg.norm(noise, "fro")))

        P_noisy, _ = column_space_projector(T_noisy)
        if P_ref.shape == P_noisy.shape:
            proj_deltas.append(float(np.linalg.norm(P_noisy - P_ref, "fro") / np.sqrt(2.0)))

        G_noisy = whitened_gram(T_noisy)
        if G_ref.shape == G_noisy.shape:
            gram_deltas.append(float(np.linalg.norm(G_noisy - G_ref, "fro")))

        D_noisy = differential_matrix(T_noisy)
        if D_ref.shape == D_noisy.shape:
            diff_deltas.append(float(np.linalg.norm(D_noisy - D_ref, "fro")))

    return {
        "eps_raw": tau_mult * float(np.median(raw_deltas)) if raw_deltas else 0.0,
        "eps_projector": tau_mult * float(np.median(proj_deltas)) if proj_deltas else 0.0,
        "eps_gram": tau_mult * float(np.median(gram_deltas)) if gram_deltas else 0.0,
        "eps_differential": tau_mult * float(np.median(diff_deltas)) if diff_deltas else 0.0,
    }


def compute_robust_margins(
    pairwise_distances: dict,
    nuisance_audit_result: dict,
    eps_invariant: dict[str, float],
    tau: float,
) -> dict:
    """Compute robust invariant margins for all pairs.

    Uses invariant-specific epsilons for unit-consistent margin computation.

    Args:
        pairwise_distances: from distances.compute_all_pairwise_distances
        nuisance_audit_result: from nuisance.nuisance_audit
        eps_invariant: dict with eps_raw, eps_projector, eps_gram, eps_differential
        tau: acceptance threshold (invariant-specific)

    Returns margins for each distance family.
    """
    per_h = nuisance_audit_result["per_hypothesis"]
    agg = nuisance_audit_result["aggregate"]

    eps_raw = eps_invariant.get("eps_raw", 0.0)
    eps_proj = eps_invariant.get("eps_projector", 0.0)
    eps_gram = eps_invariant.get("eps_gram", 0.0)
    eps_diff = eps_invariant.get("eps_differential", 0.0)

    margins = {"pairs": {}, "summary": {}}

    for hi, hj in HYP_PAIRS:
        pair_key = f"{hi}__{hj}"
        pdist = pairwise_distances["pairs"].get(pair_key, {})

        rho_raw_h = per_h.get(hi, {}).get("rho_raw", 0.0)
        rho_raw_g = per_h.get(hj, {}).get("rho_raw", 0.0)
        rho_proj_h = per_h.get(hi, {}).get("rho_projector", 0.0)
        rho_proj_g = per_h.get(hj, {}).get("rho_projector", 0.0)
        rho_gram_h = per_h.get(hi, {}).get("rho_gram", 0.0)
        rho_gram_g = per_h.get(hj, {}).get("rho_gram", 0.0)
        rho_diff_h = per_h.get(hi, {}).get("rho_differential", 0.0)
        rho_diff_g = per_h.get(hj, {}).get("rho_differential", 0.0)

        margins["pairs"][pair_key] = {
            "gamma_raw": pdist.get("raw_frobenius", 0.0) - eps_raw - rho_raw_h - rho_raw_g - tau,
            "gamma_normalized": pdist.get("raw_normalized", 0.0) - eps_raw - rho_raw_h - rho_raw_g - tau,
            "gamma_differential": pdist.get("raw_differential", 0.0) - eps_diff - rho_diff_h - rho_diff_g - tau,
            "gamma_projector": pdist.get("projector_distance", 0.0) - eps_proj - rho_proj_h - rho_proj_g - tau,
            "gamma_gram": pdist.get("gram_distance", 0.0) - eps_gram - rho_gram_h - rho_gram_g - tau,
            "delta_raw_frobenius": pdist.get("raw_frobenius", 0.0),
            "delta_projector": pdist.get("projector_distance", 0.0),
            "delta_gram": pdist.get("gram_distance", 0.0),
            "delta_differential": pdist.get("raw_differential", 0.0),
            "eps_raw": eps_raw,
            "eps_projector": eps_proj,
            "eps_gram": eps_gram,
            "eps_differential": eps_diff,
            "tau": tau,
            "rho_raw_h": rho_raw_h,
            "rho_raw_g": rho_raw_g,
            "rho_projector_h": rho_proj_h,
            "rho_projector_g": rho_proj_g,
            "rho_gram_h": rho_gram_h,
            "rho_gram_g": rho_gram_g,
        }

    raw_pos = _positive_count(margins, "raw")
    proj_pos = _positive_count(margins, "projector")
    gram_pos = _positive_count(margins, "gram")
    diff_pos = _positive_count(margins, "differential")

    n = max(len(HYP_PAIRS), 1)

    crit_raw_pos = _critical_positive_count(margins, "raw")
    crit_proj_pos = _critical_positive_count(margins, "projector")
    crit_gram_pos = _critical_positive_count(margins, "gram")
    crit_diff_pos = _critical_positive_count(margins, "differential")
    n_crit = max(len(CRITICAL_PAIRS), 1)

    summary = {
        "n_pairs": len(HYP_PAIRS),
        "n_critical_pairs": len(CRITICAL_PAIRS),
        "positive_gamma_raw_rate": raw_pos / n,
        "positive_gamma_projector_rate": proj_pos / n,
        "positive_gamma_gram_rate": gram_pos / n,
        "positive_gamma_differential_rate": diff_pos / n,
        "critical_pair_positive_gamma_raw_rate": crit_raw_pos / n_crit,
        "critical_pair_positive_gamma_projector_rate": crit_proj_pos / n_crit,
        "critical_pair_positive_gamma_gram_rate": crit_gram_pos / n_crit,
        "critical_pair_positive_gamma_differential_rate": crit_diff_pos / n_crit,
        "mean_gamma_raw": float(np.mean([p["gamma_raw"] for p in margins["pairs"].values()])),
        "mean_gamma_projector": float(np.mean([p["gamma_projector"] for p in margins["pairs"].values()])),
        "mean_gamma_gram": float(np.mean([p["gamma_gram"] for p in margins["pairs"].values()])),
        "mean_gamma_differential": float(np.mean([p["gamma_differential"] for p in margins["pairs"].values()])),
        "min_gamma_raw": _min_gamma(margins, "raw"),
        "min_gamma_projector": _min_gamma(margins, "projector"),
        "min_gamma_gram": _min_gamma(margins, "gram"),
        "min_gamma_differential": _min_gamma(margins, "differential"),
    }
    summary["best_invariant"] = _best_invariant(summary)
    summary["best_invariant_gamma_key"] = _gamma_key(summary["best_invariant"])
    margins["summary"] = summary
    margins["observable_quotient"] = compute_observable_quotient_certificate(margins)

    return margins


def _positive_count(margins: dict, name: str) -> int:
    key = _gamma_key(name)
    return sum(1 for p in margins["pairs"].values() if p.get(key, -np.inf) > 0.0)


def _critical_positive_count(margins: dict, name: str) -> int:
    key = _gamma_key(name)
    return sum(
        1
        for hi, hj in CRITICAL_PAIRS
        if margins["pairs"].get(_pair_key(hi, hj), {}).get(key, -np.inf) > 0.0
    )


def _min_gamma(margins: dict, name: str) -> float:
    key = _gamma_key(name)
    values = [p.get(key, -np.inf) for p in margins["pairs"].values()]
    return float(np.min(values)) if values else float("-inf")


def _best_invariant(summary: dict) -> str:
    """Identify the best actual invariant, excluding raw observations.

    Selection is lexicographic and intentionally conservative: maximize the
    all-pair positive rate first, then critical-pair positive rate, then the
    worst robust margin, then the mean robust margin. This prevents mixing
    gates from different invariants or selecting raw as an "invariant".
    """
    def score(name: str) -> tuple[float, float, float, float]:
        return (
            float(summary.get(f"positive_gamma_{name}_rate", 0.0)),
            float(summary.get(f"critical_pair_positive_gamma_{name}_rate", 0.0)),
            float(summary.get(f"min_gamma_{name}", float("-inf"))),
            float(summary.get(f"mean_gamma_{name}", float("-inf"))),
        )

    return max(INVARIANT_NAMES, key=score)


def compute_observable_quotient_certificate(margins: dict) -> dict:
    """Compute a robust certificate on the observable quotient.

    The full four-hypothesis certificate is too strong for the current E28
    generator because H1_via and H2_model_gap remain within the nuisance/noise
    radius. The scientifically meaningful object is therefore a quotient:
    no-via vs via-or-model-gap vs return-path. This function reports both the
    quotient margins and the unresolved H1/H2 hard pair so that the claim
    boundary is explicit.
    """
    pairs = margins.get("pairs", {})
    quotient_keys = observable_quotient_pair_keys()
    hard_key = _pair_key(*HARD_UNRESOLVED_PAIR)
    selected = margins.get("summary", {}).get("best_invariant", "gram")

    reps = {}
    for name in RAW_AND_INVARIANT_NAMES:
        gkey = _gamma_key(name)
        pair_gammas = {
            key: float(pairs.get(key, {}).get(gkey, float("-inf")))
            for key in quotient_keys
        }
        finite_gammas = list(pair_gammas.values())
        positive_count = sum(1 for v in finite_gammas if v > 0.0)
        n = max(len(finite_gammas), 1)
        hard_gamma = float(pairs.get(hard_key, {}).get(gkey, float("-inf")))
        reps[name] = {
            "quotient_pair_gammas": pair_gammas,
            "quotient_min_gamma": float(np.min(finite_gammas)) if finite_gammas else float("-inf"),
            "quotient_mean_gamma": float(np.mean(finite_gammas)) if finite_gammas else float("-inf"),
            "quotient_positive_rate": positive_count / n,
            "quotient_all_positive": positive_count == len(finite_gammas),
            "hard_h1_h2_gamma": hard_gamma,
            "hard_h1_h2_unresolved": hard_gamma <= 0.0,
        }

    selected_rep = reps.get(selected, {})
    return {
        "groups": OBSERVABLE_QUOTIENT_GROUPS,
        "quotient_pair_keys": quotient_keys,
        "hard_unresolved_pair_key": hard_key,
        "selected_invariant": selected,
        "representations": reps,
        "selected_invariant_quotient_min_gamma": selected_rep.get("quotient_min_gamma", float("-inf")),
        "selected_invariant_quotient_positive_rate": selected_rep.get("quotient_positive_rate", 0.0),
        "selected_invariant_quotient_all_positive": bool(selected_rep.get("quotient_all_positive", False)),
        "selected_invariant_hard_h1_h2_gamma": selected_rep.get("hard_h1_h2_gamma", float("-inf")),
        "selected_invariant_hard_h1_h2_unresolved": bool(selected_rep.get("hard_h1_h2_unresolved", False)),
    }


def invariant_beats_raw(margins: dict) -> dict:
    """Check whether each invariant beats raw margin.

    Returns: {invariant: bool} where True means gamma_invariant > gamma_raw
    for at least one pair.
    """
    results = {"projector_beats_raw": False, "gram_beats_raw": False, "differential_beats_raw": False}

    for pair_data in margins["pairs"].values():
        if pair_data["gamma_projector"] > pair_data["gamma_raw"]:
            results["projector_beats_raw"] = True
        if pair_data["gamma_gram"] > pair_data["gamma_raw"]:
            results["gram_beats_raw"] = True
        if pair_data["gamma_differential"] > pair_data["gamma_raw"]:
            results["differential_beats_raw"] = True

    return results


def raw_vs_invariant_comparison(
    pairwise_distances: dict,
    nuisance_audit_result: dict,
    margins: dict,
) -> dict:
    """Consolidated raw vs invariant comparison table."""
    agg = nuisance_audit_result["aggregate"]
    beats = invariant_beats_raw(margins)
    reduction = __import__("nuisance", fromlist=["nuisance_reduction_factor"]).nuisance_reduction_factor(
        nuisance_audit_result
    )

    return {
        "raw_nuisance_radius": agg["rho_raw"],
        "projector_nuisance_radius": agg["rho_projector"],
        "gram_nuisance_radius": agg["rho_gram"],
        "differential_nuisance_radius": agg["rho_differential"],
        "nuisance_reduction": reduction,
        "invariant_beats_raw": beats,
        "pairwise_margins": margins["pairs"],
        "margin_summary": margins["summary"],
    }
