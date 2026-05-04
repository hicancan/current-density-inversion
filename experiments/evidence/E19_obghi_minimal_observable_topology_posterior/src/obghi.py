"""Minimal OBGHI posterior inference."""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

from basis import HYPOTHESES, HypothesisBasis, build_all_hypothesis_bases, via_gap_angle
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


def _stable_logsumexp(vals: list[float]) -> float:
    m = max(vals)
    if not math.isfinite(m):
        return m
    return m + math.log(sum(math.exp(v - m) for v in vals))


def _gaussian_evidence_and_posterior(
    y: np.ndarray,
    B: np.ndarray,
    noise_sigma: float,
    prior_var: float,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """Closed-form evidence for y ~ N(0, sigma^2 I + prior_var B B^T).

    Uses Woodbury identity in coefficient space for numerical stability.
    """
    m = y.size
    k = B.shape[1]
    sigma2 = float(noise_sigma) ** 2
    if k == 0:
        quad = float(y @ y / sigma2)
        logdet = m * math.log(sigma2)
        logev = -0.5 * (quad + logdet + m * math.log(2.0 * math.pi))
        return logev, np.zeros(0), np.zeros(0), np.zeros_like(y)

    # Posterior over coefficients:
    # S = (B^T B / sigma^2 + I/prior_var)^-1
    BtB = (B.T @ B) / sigma2
    precision = BtB + np.eye(k) / float(prior_var)
    jitter = 1e-10
    for _ in range(6):
        try:
            L = np.linalg.cholesky(precision + jitter * np.eye(k))
            break
        except np.linalg.LinAlgError:
            jitter *= 10.0
    else:
        raise np.linalg.LinAlgError("Could not stabilize coefficient precision")

    rhs = (B.T @ y) / sigma2
    tmp = np.linalg.solve(L, rhs)
    mean = np.linalg.solve(L.T, tmp)

    inv_precision = np.linalg.solve(L.T, np.linalg.solve(L, np.eye(k)))
    pred = B @ mean

    # Marginal likelihood via determinant lemma:
    # C = sigma^2 I + v B B^T
    # log|C| = m log sigma^2 + log|I + v/sigma^2 B^T B|
    small = np.eye(k) + (float(prior_var) / sigma2) * (B.T @ B)
    sign, logdet_small = np.linalg.slogdet(small)
    if sign <= 0:
        # Conservative fallback.
        evals = np.linalg.eigvalsh(small)
        logdet_small = float(np.sum(np.log(np.maximum(evals, 1e-18))))
    logdet = m * math.log(sigma2) + logdet_small

    # C^-1 y = y/sigma2 - B (precision^-1 B^T y) / sigma2^2
    cinv_y = y / sigma2 - B @ (inv_precision @ (B.T @ y)) / (sigma2 * sigma2)
    quad = float(y @ cinv_y)
    logev = -0.5 * (quad + logdet + m * math.log(2.0 * math.pi))
    return float(logev), mean, np.diag(inv_precision), pred


def _prior_variance_for_hypothesis(cfg: dict, hypothesis: str) -> float:
    pv = cfg["prior_variance"]
    if hypothesis == "H1_via":
        return float(pv["via"])
    if hypothesis == "H2_model_gap":
        return float(pv["gap"])
    if hypothesis == "H3_return_path":
        return float(pv["return"])
    return float(pv["graph"])


def _posterior_entropy(probs: list[float]) -> float:
    p = np.asarray(probs, dtype=float)
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)))


def _decision(cfg: dict, top_h: str, top_p: float, logbf_via_gap: float, angle_deg: float) -> str:
    dec = cfg["decision"]
    accept_thr = float(dec["accept_posterior_threshold"])
    reject_thr = float(dec["reject_posterior_threshold"])
    min_angle = float(dec["via_gap_min_angle_deg"])
    logbf_eps = float(dec["via_gap_logbf_epsilon"])

    if top_p < reject_thr:
        return "reject_low_posterior"
    if top_h in ("H1_via", "H2_model_gap") and (angle_deg < min_angle or abs(logbf_via_gap) < logbf_eps):
        return "reject_via_gap_ambiguous"
    if top_p >= accept_thr:
        return "accept"
    return "need_next_measurement"


def infer_case(case, bundle: OperatorBundle, cfg: dict) -> OBGHIResult:
    y = case.field_observed
    bases = build_all_hypothesis_bases(bundle, cfg)
    log_priors = cfg["hypothesis_log_priors"]
    noise = float(cfg["noise_sigma"])

    tmp: dict[str, dict] = {}
    joints: list[float] = []

    for h in HYPOTHESES:
        hb: HypothesisBasis = bases[h]
        prior_var = _prior_variance_for_hypothesis(cfg, h)
        logev, mu, cov_diag, pred = _gaussian_evidence_and_posterior(y, hb.B, noise, prior_var)
        logprior = float(log_priors[h])
        joint = logev + logprior
        current_mean = hb.current_basis @ mu[: hb.current_basis.shape[1]] if hb.current_basis.shape[1] else np.zeros(bundle.A.shape[1])
        tmp[h] = {
            "basis": hb,
            "logev": logev,
            "logprior": logprior,
            "joint": joint,
            "mu": mu,
            "cov_diag": cov_diag,
            "pred": pred,
            "current_mean": current_mean,
        }
        joints.append(joint)

    lse = _stable_logsumexp(joints)
    posteriors: dict[str, HypothesisPosterior] = {}
    for h in HYPOTHESES:
        item = tmp[h]
        prob = math.exp(item["joint"] - lse)
        hb = item["basis"]
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
            predictive_residual_norm=float(np.linalg.norm(y - item["pred"]) / max(np.linalg.norm(y), 1e-18)),
            kept_column_count=len(hb.kept_columns),
            dropped_column_count=len(hb.dropped_columns),
        )

    top_h = max(posteriors, key=lambda h: posteriors[h].posterior_probability)
    top_p = posteriors[top_h].posterior_probability
    logbf_via_gap = posteriors["H1_via"].log_evidence - posteriors["H2_model_gap"].log_evidence
    angle = via_gap_angle(bundle, cfg)
    decision = _decision(cfg, top_h, top_p, logbf_via_gap, angle)
    entropy = _posterior_entropy([posteriors[h].posterior_probability for h in HYPOTHESES])

    return OBGHIResult(
        case_id=case.case_id,
        truth_hypothesis=case.truth_hypothesis,
        posteriors=posteriors,
        top_hypothesis=top_h,
        top_probability=float(top_p),
        decision=decision,
        via_gap_angle_deg=float(angle),
        logbf_via_gap=float(logbf_via_gap),
        posterior_entropy=entropy,
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
    }
    for h in HYPOTHESES:
        row[f"p_{h}"] = result.posteriors[h].posterior_probability
        row[f"logev_{h}"] = result.posteriors[h].log_evidence
        row[f"resid_{h}"] = result.posteriors[h].predictive_residual_norm
    return row
