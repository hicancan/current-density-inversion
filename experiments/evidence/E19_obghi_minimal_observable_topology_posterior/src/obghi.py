"""Minimal OBGHI posterior inference with block-diagonal group priors.

Requires HypothesisBasis to carry ``prior_var_vector`` (np.ndarray, length=k)
from build_hypothesis_basis.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import numpy as np

from basis import HYPOTHESES, HypothesisBasis, build_all_hypothesis_bases, subspace_principal_angle_deg, via_gap_angle
from operators import OperatorBundle


@dataclass
class HypothesisPosterior:
    hypothesis: str
    log_evidence: float
    log_prior: float
    log_joint: float
    posterior_probability: float
    coefficient_mean: np.ndarray
    coefficient_cov_diag: np.ndarray
    current_mean: np.ndarray
    predictive_mean: np.ndarray
    predictive_residual_norm: float
    kept_column_count: int
    dropped_column_count: int
    column_metadata: list[dict]
    per_block_column_counts: dict[str, int]
    current_basis_scales: np.ndarray


@dataclass
class OBGHIResult:
    case_id: str
    truth_hypothesis: str
    posteriors: dict[str, HypothesisPosterior]
    top_hypothesis: str
    top_probability: float
    decision: str
    via_gap_angle_deg: float
    logbf_via_gap: float
    posterior_entropy: float
    case_via_gap_angle_deg: float
    residual_alignment_via: float
    residual_alignment_gap: float
    residual_alignment_return: float
    logbf_via_vs_h0: float
    logbf_via_vs_return: float
    via_residual_improvement_over_h0: float
    no_via_false_positive_guard_triggered: bool


def _stable_logsumexp(vals: list[float]) -> float:
    m = max(vals)
    if not math.isfinite(m):
        return m
    return m + math.log(sum(math.exp(v - m) for v in vals))


def _residual_alignment(r: np.ndarray, B_extra: np.ndarray) -> float:
    """Cosine between residual and subspace spanned by extra basis columns."""
    if B_extra.shape[1] == 0 or np.linalg.norm(r) < 1e-18:
        return 0.0
    Q, _ = np.linalg.qr(B_extra)
    proj_norm = float(np.linalg.norm(Q @ (Q.T @ r)))
    r_norm = float(np.linalg.norm(r))
    return proj_norm / max(r_norm, 1e-18)


def _columns_orthogonal_to(B: np.ndarray, B_common: np.ndarray) -> np.ndarray:
    """Return columns of B projected orthogonal to column space of B_common."""
    if B.shape[1] == 0:
        return B
    if B_common.shape[1] == 0:
        return B.copy()
    Q, _ = np.linalg.qr(B_common)
    return B - Q @ (Q.T @ B)


def _prior_var_vector_from_basis(hb: HypothesisBasis) -> np.ndarray:
    """Extract prior_var_vector from HypothesisBasis, with fallback."""
    if hasattr(hb, "prior_var_vector") and hb.prior_var_vector is not None:
        return np.asarray(hb.prior_var_vector, dtype=float)
    return np.full(hb.B.shape[1], 1.0, dtype=float)


def _build_column_metadata(hb: HypothesisBasis) -> tuple[list[dict], dict[str, int]]:
    """Build per-column metadata and per-block-kind counts from kept columns."""
    col_meta: list[dict] = []
    for name in hb.kept_columns:
        parts = name.split(":")
        col_meta.append({
            "column_name": name,
            "block_kind": parts[0] if len(parts) > 0 else "unknown",
            "block_name": parts[1] if len(parts) > 1 else "unknown",
            "column_index": int(parts[2]) if len(parts) > 2 else -1,
        })
    per_block_counts: dict[str, int] = dict(
        Counter(d["block_kind"] for d in col_meta)
    )
    return col_meta, per_block_counts


def _current_basis_scales(hb: HypothesisBasis) -> np.ndarray:
    """Column norms of current basis (from basis construction)."""
    if hasattr(hb, "current_basis_scales") and hb.current_basis_scales is not None and len(hb.current_basis_scales) > 0:
        return np.asarray(hb.current_basis_scales, dtype=float)
    if hb.current_basis.shape[1] == 0:
        return np.zeros(0, dtype=float)
    return np.linalg.norm(hb.current_basis, axis=0)


def _gaussian_evidence_and_posterior(
    y: np.ndarray,
    B: np.ndarray,
    noise_sigma: float,
    prior_var_vector: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """Closed-form evidence for y ~ N(0, C) with block-diagonal prior.

    C = sigma^2 I + B diag(prior_var_vector) B^T

    Uses determinant lemma with B_scaled = B * sqrt(prior_var_vector):
      C = sigma^2 I + B_scaled B_scaled^T
      precision = B_scaled^T B_scaled / sigma^2 + I
    """
    m = y.size
    k = B.shape[1]
    sigma2 = float(noise_sigma) ** 2
    if k == 0:
        quad = float(y @ y / sigma2)
        logdet = m * math.log(sigma2)
        logev = -0.5 * (quad + logdet + m * math.log(2.0 * math.pi))
        return logev, np.zeros(0), np.zeros(0), np.zeros_like(y)

    sqrt_v = np.sqrt(np.maximum(prior_var_vector, 1e-30))
    B_scaled = B * sqrt_v[None, :]

    precision = (B_scaled.T @ B_scaled) / sigma2 + np.eye(k)
    rhs = (B_scaled.T @ y) / sigma2

    jitter = 1e-10
    for _ in range(6):
        try:
            L = np.linalg.cholesky(precision + jitter * np.eye(k))
            break
        except np.linalg.LinAlgError:
            jitter *= 10.0
    else:
        raise np.linalg.LinAlgError("Could not stabilize coefficient precision")

    tmp = np.linalg.solve(L, rhs)
    mean_scaled = np.linalg.solve(L.T, tmp)
    inv_precision = np.linalg.solve(L.T, np.linalg.solve(L, np.eye(k)))
    cov_diag_scaled = np.diag(inv_precision)

    mean = mean_scaled * sqrt_v
    cov_diag = cov_diag_scaled * prior_var_vector

    pred = B @ mean

    small = np.eye(k) + (B_scaled.T @ B_scaled) / sigma2
    sign, logdet_small = np.linalg.slogdet(small)
    if sign <= 0:
        evals = np.linalg.eigvalsh(small)
        logdet_small = float(np.sum(np.log(np.maximum(evals, 1e-18))))
    logdet = m * math.log(sigma2) + logdet_small

    cinv_y = y / sigma2 - (B_scaled @ (inv_precision @ (B_scaled.T @ y))) / (sigma2 * sigma2)
    quad = float(y @ cinv_y)
    logev = -0.5 * (quad + logdet + m * math.log(2.0 * math.pi))
    return float(logev), mean, cov_diag, pred


def _posterior_entropy(probs: list[float]) -> float:
    p = np.asarray(probs, dtype=float)
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)))


def _case_via_gap_angle(
    h0_basis: HypothesisBasis,
    h1_basis: HypothesisBasis,
    h2_basis: HypothesisBasis,
) -> float:
    """Case-specific via/gap principal angle on extra (beyond common) columns."""
    common_B = h0_basis.B
    via_extra = _columns_orthogonal_to(h1_basis.B, common_B)
    gap_extra = _columns_orthogonal_to(h2_basis.B, common_B)
    return subspace_principal_angle_deg(via_extra, gap_extra)


def _decision(
    cfg: dict,
    top_h: str,
    top_p: float,
    posteriors: dict[str, HypothesisPosterior],
    case_diagnostics: dict,
) -> str:
    dec = cfg["decision"]
    logbf_via_gap = posteriors["H1_via"].log_evidence - posteriors["H2_model_gap"].log_evidence

    logbf_via_vs_h0 = case_diagnostics.get("logbf_via_vs_h0", 0.0)
    residual_improvement = case_diagnostics.get("via_residual_improvement_over_h0", 0.0)
    case_angle = case_diagnostics.get("case_via_gap_angle_deg", 90.0)
    logbf_via_vs_return = case_diagnostics.get("logbf_via_vs_return", 0.0)

    logbf_threshold = float(dec.get("logbf_threshold", 2.0))
    improvement_threshold = float(dec.get("improvement_threshold", 0.05))
    min_angle = float(dec.get("via_gap_min_angle_deg", 10.0))
    logbf_eps = float(dec.get("via_gap_logbf_epsilon", 1.0))
    return_competition_threshold = float(dec.get("return_competition_threshold", 0.20))

    if top_h == "H1_via" and logbf_via_vs_h0 < logbf_threshold and residual_improvement < improvement_threshold:
        return "reject_no_via_false_positive_guard"

    if top_h in ("H1_via", "H2_model_gap") and (case_angle < min_angle or abs(logbf_via_gap) < logbf_eps):
        return "reject_via_gap_ambiguous"

    h3_posterior = posteriors["H3_return_path"].posterior_probability
    if top_h == "H1_via" and h3_posterior > return_competition_threshold:
        if logbf_via_vs_return < logbf_threshold:
            return "reject_return_ambiguous"
        return "need_next_measurement"

    accept_map = {
        "H0_no_via": float(dec.get("accept_threshold_h0", dec.get("accept_posterior_threshold", 0.80))),
        "H1_via": float(dec.get("accept_threshold_h1", dec.get("accept_posterior_threshold", 0.75))),
        "H2_model_gap": float(dec.get("accept_threshold_h2", dec.get("accept_posterior_threshold", 0.80))),
        "H3_return_path": float(dec.get("accept_threshold_h3", dec.get("accept_posterior_threshold", 0.80))),
    }
    class_accept_thr = accept_map.get(top_h, 0.80)
    global_reject_thr = float(dec.get("reject_posterior_threshold", 0.45))

    if top_p >= class_accept_thr:
        return "accept"
    if top_p < global_reject_thr:
        return "reject_low_posterior"
    return "need_next_measurement"


def infer_case(case, bundle: OperatorBundle, cfg: dict) -> OBGHIResult:
    y = case.field_observed
    bases = build_all_hypothesis_bases(bundle, cfg)
    log_priors = cfg["hypothesis_log_priors"]
    noise = float(cfg["noise_sigma"])
    noise_sq = noise ** 2

    # Step 1: fit common (H0) basis, compute residual evidence baseline.
    h0_basis = bases["H0_no_via"]
    logev_common, mu_common, cov_common, pred_common = _gaussian_evidence_and_posterior(
        y, h0_basis.B, noise, _prior_var_vector_from_basis(h0_basis),
    )
    residual = y - pred_common
    logev_residual_h0 = logev_common

    # Step 2: for each extra hypothesis, compute evidence as:
    # logev = logev_common + residual_logev(extra_columns)
    # This removes the common-basis complexity penalty.
    tmp: dict[str, dict] = {}
    joints: list[float] = []

    for h in HYPOTHESES:
        hb: HypothesisBasis = bases[h]
        logprior = float(log_priors[h])

        if h == "H0_no_via":
            logev_total = logev_common
        else:
            B_extra = _columns_orthogonal_to(hb.B, h0_basis.B)
            if B_extra.shape[1] > 0:
                extra_pv = np.ones(B_extra.shape[1], dtype=float)
                logev_extra, mu_extra, cov_extra, pred_extra = _gaussian_evidence_and_posterior(
                    residual, B_extra, noise, extra_pv,
                )
                logev_total = logev_common + logev_extra
            else:
                logev_total = logev_common

        joint = logev_total + logprior

        # Full model prediction for residual norm.
        B_full = hb.B
        pv_full = _prior_var_vector_from_basis(hb)
        _, mu_full, cov_full, pred_full = _gaussian_evidence_and_posterior(
            y, B_full, noise, pv_full,
        )
        if hb.current_basis.shape[1] > 0:
            k_c = hb.current_basis.shape[1]
            current_mean = hb.current_basis @ mu_full[:k_c]
        else:
            current_mean = np.zeros(bundle.A.shape[1])

        col_meta, per_block_counts = _build_column_metadata(hb)
        basis_scales = _current_basis_scales(hb)

        tmp[h] = {
            "logev": logev_total,
            "logprior": logprior,
            "joint": joint,
            "mu": mu_full,
            "cov_diag": cov_full,
            "pred": pred_full,
            "current_mean": current_mean,
            "col_meta": col_meta,
            "per_block_counts": per_block_counts,
            "current_basis_scales": basis_scales,
            "hb": hb,
        }
        joints.append(joint)

    lse = _stable_logsumexp(joints)
    posteriors: dict[str, HypothesisPosterior] = {}
    for h in HYPOTHESES:
        item = tmp[h]
        prob = math.exp(item["joint"] - lse)
        hb = item["hb"]
        posteriors[h] = HypothesisPosterior(
            hypothesis=h,
            log_evidence=float(item["logev"]),
            log_prior=float(item["logprior"]),
            log_joint=float(item["joint"]),
            posterior_probability=float(prob),
            coefficient_mean=item["mu"],
            coefficient_cov_diag=item["cov_diag"],
            current_mean=item["current_mean"],
            predictive_mean=item["pred"],
            predictive_residual_norm=float(
                np.linalg.norm(y - item["pred"]) / max(np.linalg.norm(y), 1e-18)
            ),
            kept_column_count=len(hb.kept_columns),
            dropped_column_count=len(hb.dropped_columns),
            column_metadata=item["col_meta"],
            per_block_column_counts=item["per_block_counts"],
            current_basis_scales=item["current_basis_scales"],
        )

    h1_basis = bases["H1_via"]
    h2_basis = bases["H2_model_gap"]
    h3_basis = bases["H3_return_path"]

    B_via_extra = _columns_orthogonal_to(h1_basis.B, h0_basis.B)
    B_gap_extra = _columns_orthogonal_to(h2_basis.B, h0_basis.B)
    B_return_extra = _columns_orthogonal_to(h3_basis.B, h0_basis.B)

    residual_alignment_via = _residual_alignment(residual, B_via_extra)
    residual_alignment_gap = _residual_alignment(residual, B_gap_extra)
    residual_alignment_return = _residual_alignment(residual, B_return_extra)

    case_via_gap_angle_deg_val = subspace_principal_angle_deg(B_via_extra, B_gap_extra)

    logbf_via_vs_h0 = posteriors["H1_via"].log_evidence - posteriors["H0_no_via"].log_evidence
    logbf_via_vs_return = posteriors["H1_via"].log_evidence - posteriors["H3_return_path"].log_evidence

    r_h0_norm = np.linalg.norm(y - posteriors["H0_no_via"].predictive_mean)
    r_h1_norm = np.linalg.norm(y - posteriors["H1_via"].predictive_mean)
    via_residual_improvement = float(
        (r_h0_norm - r_h1_norm) / max(r_h0_norm, 1e-18)
    )

    top_h = max(posteriors, key=lambda h: posteriors[h].posterior_probability)
    top_p = posteriors[top_h].posterior_probability
    logbf_via_gap = posteriors["H1_via"].log_evidence - posteriors["H2_model_gap"].log_evidence

    case_diagnostics = {
        "logbf_via_vs_h0": logbf_via_vs_h0,
        "logbf_via_vs_return": logbf_via_vs_return,
        "via_residual_improvement_over_h0": via_residual_improvement,
        "case_via_gap_angle_deg": case_via_gap_angle_deg_val,
    }

    decision = _decision(cfg, top_h, top_p, posteriors, case_diagnostics)
    entropy = _posterior_entropy([posteriors[h].posterior_probability for h in HYPOTHESES])
    global_angle = via_gap_angle(bundle, cfg)
    no_via_guard_triggered = decision == "reject_no_via_false_positive_guard"

    return OBGHIResult(
        case_id=case.case_id,
        truth_hypothesis=case.truth_hypothesis,
        posteriors=posteriors,
        top_hypothesis=top_h,
        top_probability=float(top_p),
        decision=decision,
        via_gap_angle_deg=float(global_angle),
        logbf_via_gap=float(logbf_via_gap),
        posterior_entropy=entropy,
        case_via_gap_angle_deg=float(case_via_gap_angle_deg_val),
        residual_alignment_via=float(residual_alignment_via),
        residual_alignment_gap=float(residual_alignment_gap),
        residual_alignment_return=float(residual_alignment_return),
        logbf_via_vs_h0=float(logbf_via_vs_h0),
        logbf_via_vs_return=float(logbf_via_vs_return),
        via_residual_improvement_over_h0=float(via_residual_improvement),
        no_via_false_positive_guard_triggered=no_via_guard_triggered,
    )


def result_to_row(result: OBGHIResult) -> dict:
    row = {
        "case_id": result.case_id,
        "truth": result.truth_hypothesis,
        "top": result.top_hypothesis,
        "top_probability": result.top_probability,
        "decision": result.decision,
        "via_gap_angle_deg": result.via_gap_angle_deg,
        "logbf_via_gap": result.logbf_via_gap,
        "posterior_entropy": result.posterior_entropy,
        "case_via_gap_angle_deg": result.case_via_gap_angle_deg,
        "residual_alignment_via": result.residual_alignment_via,
        "residual_alignment_gap": result.residual_alignment_gap,
        "residual_alignment_return": result.residual_alignment_return,
        "logbf_via_vs_h0": result.logbf_via_vs_h0,
        "logbf_via_vs_return": result.logbf_via_vs_return,
        "via_residual_improvement_over_h0": result.via_residual_improvement_over_h0,
        "no_via_false_positive_guard_triggered": result.no_via_false_positive_guard_triggered,
    }
    for h in HYPOTHESES:
        row[f"p_{h}"] = result.posteriors[h].posterior_probability
        row[f"logev_{h}"] = result.posteriors[h].log_evidence
        row[f"resid_{h}"] = result.posteriors[h].predictive_residual_norm
    return row
