from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

# Allow running as ``python src/run_all.py`` without package installation.
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from graph_id.baselines import sheet_residual_via_score, via_template_peak_score
from graph_id.basis_library import augment_record_for_pypeec_basis
from graph_id.candidate_search import (
    offset_grid,
    score_with_global_registration_search,
    score_with_via_location_marginalization,
    transform_grid,
    transform_segment_xy,
)
from graph_id.exp07_bridge import load_exp07_graph_bridge_records
from graph_id.forward import field_from_segments, make_observation_grid
from graph_id.generator import generate_dataset, write_dataset_artifacts
from graph_id.hidden_stress import (
    generate_hidden_mechanism_records,
    generate_near_boundary_hidden_records,
    generate_near_boundary_hidden_severity_records,
)
from graph_id.metrics import (
    auc_pairwise,
    binary_metrics,
    confusion_matrix,
    hypothesis_accuracy,
    per_class_accuracy,
    select_threshold_with_fp_cap,
    selective_risk,
)
from graph_id.multistate import best_joint_hypothesis, joint_hypothesis_scores, make_second_excitation_state
from graph_id.reporting import (
    fmt_float,
    markdown_table,
    save_confusion_matrix,
    save_example_case,
    save_score_histogram,
    write_json,
)
from graph_id.solver import best_hypothesis, score_hypotheses, score_margin, via_evidence


EXP_DIR = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_records(records, obs_grid, cfg, complexity_penalty: float) -> List[dict]:
    rows = []
    for rec in records:
        results = score_hypotheses(rec, obs_grid, cfg, complexity_penalty=complexity_penalty)
        pred_h = best_hypothesis(results)
        rows.append(
            {
                "case_id": rec.case_id,
                "split": rec.split,
                "class_label": rec.class_label,
                "true_hypothesis": rec.hypothesis_label,
                "pred_hypothesis": pred_h,
                "confidence_margin": score_margin(results),
                "via_evidence": via_evidence(results),
                "raw_via_score": via_template_peak_score(rec, obs_grid, cfg),
                "sheet_residual_via_score": sheet_residual_via_score(rec, obs_grid, cfg),
                "scores": {k: v.score for k, v in results.items()},
                "residuals": {k: v.residual_rel_l2 for k, v in results.items()},
                "results": results,
                "record": rec,
            }
        )
    return rows


def tune_complexity(records_val, obs_grid, cfg) -> Tuple[float, List[dict]]:
    labels = list(cfg["scoring"]["hypotheses"])
    best = None
    best_rows: List[dict] = []
    for penalty in cfg["scoring"]["complexity_penalty_grid"]:
        rows = evaluate_records(records_val, obs_grid, cfg, complexity_penalty=float(penalty))
        true = [r["true_hypothesis"] for r in rows]
        pred = [r["pred_hypothesis"] for r in rows]
        acc = hypothesis_accuracy(true, pred)
        y_true_via = [1 if r["class_label"] == "true_via" else 0 for r in rows]
        y_score_via = [r["via_evidence"] for r in rows]
        threshold, via_m = select_threshold_with_fp_cap(
            y_true_via,
            y_score_via,
            max_fp_rate=float(cfg["scoring"]["max_allowed_no_via_fp_for_threshold_selection"]),
        )
        no_via_fp = via_m.get("false_positive_rate", 1.0)
        # The selected penalty should improve multi-hypothesis accuracy while
        # not simply over-selecting the extra-basis hypotheses.
        objective = acc + 0.30 * via_m.get("f1", 0.0) - 0.20 * no_via_fp
        key = (objective, acc, via_m.get("f1", 0.0), -float(penalty))
        if best is None or key > best[0]:
            best = (key, float(penalty), threshold, via_m)
            best_rows = rows
    return best[1], best_rows


def split_rows(rows, split: str) -> List[dict]:
    return [r for r in rows if r["split"] == split]


def via_eval(rows: List[dict], threshold: float, score_key: str) -> Dict[str, float]:
    y_true = [1 if r["class_label"] == "true_via" else 0 for r in rows]
    y_score = [float(r[score_key]) for r in rows]
    out = binary_metrics(y_true, y_score, threshold=threshold)
    out["auc"] = auc_pairwise(y_true, y_score)
    out["threshold"] = float(threshold)
    return out


def tune_threshold(rows_val: List[dict], cfg: dict, score_key: str) -> Tuple[float, Dict[str, float]]:
    y_true = [1 if r["class_label"] == "true_via" else 0 for r in rows_val]
    y_score = [float(r[score_key]) for r in rows_val]
    return select_threshold_with_fp_cap(
        y_true,
        y_score,
        max_fp_rate=float(cfg["scoring"]["max_allowed_no_via_fp_for_threshold_selection"]),
    )


def summarize_hypothesis(rows: List[dict], labels: List[str]) -> Dict[str, object]:
    true = [r["true_hypothesis"] for r in rows]
    pred = [r["pred_hypothesis"] for r in rows]
    return {
        "accuracy": hypothesis_accuracy(true, pred),
        "per_class_accuracy": per_class_accuracy(true, pred),
        "confusion_matrix": confusion_matrix(true, pred, labels).tolist(),
        "selective_risk": selective_risk(true, pred, [r["confidence_margin"] for r in rows]),
        "median_best_residual_rel_l2": float(np.median([r["results"][r["pred_hypothesis"]].residual_rel_l2 for r in rows])),
    }


def per_class_rows(metrics: dict) -> List[List[object]]:
    out: List[List[object]] = []
    for split in ["val", "test", "ood"]:
        h = metrics["hypothesis_identification"][split]
        for label, acc in h["per_class_accuracy"].items():
            out.append([split, label, fmt_float(acc)])
    return out


def selective_rows(metrics: dict) -> List[List[object]]:
    out: List[List[object]] = []
    for split in ["val", "test", "ood"]:
        sr = metrics["hypothesis_identification"][split]["selective_risk"]
        for pct in [20, 50, 80, 100]:
            acc = sr[f"accuracy_at_{pct}pct_coverage"]
            n_selected = sr[f"coverage_{pct}pct_n"]
            out.append([split, f"{pct}%", int(n_selected), fmt_float(acc), fmt_float(1.0 - acc)])
    return out


def failure_rows(rows_all: List[dict]) -> List[List[object]]:
    records: List[Tuple[float, List[object]]] = []
    for row in rows_all:
        if row["true_hypothesis"] == row["pred_hypothesis"]:
            continue
        pred = row["pred_hypothesis"]
        true = row["true_hypothesis"]
        results = row["results"]
        records.append((float(row["confidence_margin"]), [
            row["split"],
            row["case_id"],
            row["class_label"],
            true,
            pred,
            fmt_float(row["confidence_margin"]),
            fmt_float(row["via_evidence"]),
            fmt_float(results[true].residual_rel_l2),
            fmt_float(results[pred].residual_rel_l2),
            fmt_float(row["raw_via_score"]),
            fmt_float(row["sheet_residual_via_score"]),
        ]))
    records.sort(key=lambda item: (item[1][0] == "ood", item[0]), reverse=True)
    return [row for _, row in records]


def _via_metrics_from_rows(rows: List[dict], threshold: float) -> Dict[str, float]:
    y_true = [1 if r["class_label"] == "true_via" else 0 for r in rows]
    y_score = [float(r["via_evidence"]) for r in rows]
    out = binary_metrics(y_true, y_score, threshold=threshold)
    out["auc"] = auc_pairwise(y_true, y_score)
    return out


def _summary_for_rows(rows: List[dict], labels: List[str], threshold: float) -> dict:
    hyp = summarize_hypothesis(rows, labels)
    via = _via_metrics_from_rows(rows, threshold)
    return {
        "n": len(rows),
        "accuracy": hyp["accuracy"],
        "per_class_accuracy": hyp["per_class_accuracy"],
        "selective_risk": hyp["selective_risk"],
        "via_detection": via,
        "median_margin": float(np.median([r["confidence_margin"] for r in rows])) if rows else float("nan"),
        "median_best_residual_rel_l2": hyp["median_best_residual_rel_l2"],
    }


def _summary_table_row(name: str, summary: dict) -> List[object]:
    via = summary["via_detection"]
    pc = summary["per_class_accuracy"]
    return [
        name,
        int(summary["n"]),
        fmt_float(summary["accuracy"]),
        fmt_float(pc.get("H0_sheet_only", float("nan"))),
        fmt_float(pc.get("H1_sheet_via", float("nan"))),
        fmt_float(pc.get("H2_sheet_return", float("nan"))),
        fmt_float(pc.get("H3_sheet_artifact", float("nan"))),
        fmt_float(via["auc"]),
        fmt_float(via["recall"]),
        fmt_float(via["f1"]),
        fmt_float(via["false_positive_rate"]),
        fmt_float(summary["median_margin"]),
        fmt_float(summary["median_best_residual_rel_l2"]),
    ]


def _evidence_score(result, mode: str, cfg: dict, n_obs: int) -> float:
    ev_cfg = cfg.get("model_evidence", {})
    residual = float(result.residual_rel_l2)
    if mode == "residual_only":
        return residual
    if mode == "default_score":
        return float(result.score)
    if mode == "parameter_count":
        return residual + float(ev_cfg.get("parameter_count_penalty", 0.0)) * float(result.n_basis)
    if mode == "extra_count":
        return residual + float(ev_cfg.get("extra_count_penalty", 0.0)) * float(result.n_extra_basis)
    if mode == "bic_like":
        return residual + float(ev_cfg.get("bic_weight", 0.0)) * float(result.n_basis) * float(np.log(max(n_obs, 2))) / float(n_obs)
    if mode == "h0_conservative":
        prior = 0.0 if result.name == "H0_sheet_only" else float(ev_cfg.get("h0_prior_penalty", 0.0))
        return residual + prior + float(ev_cfg.get("extra_count_penalty", 0.0)) * float(result.n_extra_basis)
    raise ValueError(f"unknown evidence mode: {mode}")


def _summary_for_evidence_mode(rows: List[dict], labels: List[str], cfg: dict, mode: str) -> dict:
    n_obs = int(rows[0]["record"].b_obs.size) if rows else 1
    pred = [
        min(labels, key=lambda label: _evidence_score(r["results"][label], mode, cfg, n_obs))
        for r in rows
    ]
    true = [r["true_hypothesis"] for r in rows]
    h0_idx = [i for i, r in enumerate(rows) if r["true_hypothesis"] == "H0_sheet_only"]
    false_h1 = float(np.mean([pred[i] == "H1_sheet_via" for i in h0_idx])) if h0_idx else float("nan")
    false_h2 = float(np.mean([pred[i] == "H2_sheet_return" for i in h0_idx])) if h0_idx else float("nan")
    false_h3 = float(np.mean([pred[i] == "H3_sheet_artifact" for i in h0_idx])) if h0_idx else float("nan")
    residuals = [r["results"][p].residual_rel_l2 for r, p in zip(rows, pred)]
    counts = [r["results"][p].n_basis for r, p in zip(rows, pred)]
    return {
        "n": len(rows),
        "accuracy": hypothesis_accuracy(true, pred),
        "per_class_accuracy": per_class_accuracy(true, pred),
        "false_h1_rate": false_h1,
        "false_h2_rate": false_h2,
        "false_h3_rate": false_h3,
        "median_residual": float(np.median(residuals)) if residuals else float("nan"),
        "median_parameter_count": float(np.median(counts)) if counts else float("nan"),
        "pred": pred,
    }


def _model_evidence_table_row(dataset: str, basis_mode: str, evidence_mode: str, summary: dict) -> List[object]:
    pc = summary["per_class_accuracy"]
    return [
        dataset,
        basis_mode,
        evidence_mode,
        int(summary["n"]),
        fmt_float(summary["accuracy"]),
        fmt_float(pc.get("H0_sheet_only", float("nan"))),
        fmt_float(pc.get("H1_sheet_via", float("nan"))),
        fmt_float(pc.get("H2_sheet_return", float("nan"))),
        fmt_float(pc.get("H3_sheet_artifact", float("nan"))),
        fmt_float(summary["false_h1_rate"]),
        fmt_float(summary["false_h2_rate"]),
        fmt_float(summary["false_h3_rate"]),
        fmt_float(summary["median_residual"]),
        fmt_float(summary["median_parameter_count"]),
    ]


def _h0_hard_row(dataset: str, mode: str, summary: dict) -> List[object]:
    pc = summary["per_class_accuracy"]
    return [
        dataset,
        mode,
        int(summary["n"]),
        fmt_float(pc.get("H0_sheet_only", float("nan"))),
        fmt_float(summary["false_h1_rate"]),
        fmt_float(summary["false_h2_rate"]),
        fmt_float(summary["false_h3_rate"]),
        fmt_float(summary["accuracy"]),
        fmt_float(summary["median_residual"]),
    ]


def _best_residual(row: dict) -> float:
    return float(row["results"][row["pred_hypothesis"]].residual_rel_l2)


def _evaluate_via_marginalized_records(
    records,
    obs_grid,
    cfg: dict,
    complexity_penalty: float,
    offsets: list[tuple[float, float]],
) -> List[dict]:
    rows = []
    for rec in records:
        out = score_with_via_location_marginalization(
            rec, obs_grid, cfg, complexity_penalty=complexity_penalty, offsets=offsets
        )
        rows.append(
            {
                "case_id": rec.case_id,
                "split": rec.split,
                "class_label": rec.class_label,
                "true_hypothesis": rec.hypothesis_label,
                "pred_hypothesis": out["pred_hypothesis"],
                "confidence_margin": out["confidence_margin"],
                "via_evidence": out["via_evidence"],
                "scores": {k: v.score for k, v in out["results"].items()},
                "residuals": {k: v.residual_rel_l2 for k, v in out["results"].items()},
                "results": out["results"],
                "record": rec,
                "best_via_offset_m": out["best_via_offset_m"],
                "best_via_offset_norm_m": out["best_via_offset_norm_m"],
            }
        )
    return rows


def _evaluate_global_registration_records(
    records,
    obs_grid,
    cfg: dict,
    complexity_penalty: float,
    transforms: list[dict],
) -> List[dict]:
    rows = []
    for rec in records:
        out = score_with_global_registration_search(
            rec, obs_grid, cfg, complexity_penalty=complexity_penalty, transforms=transforms
        )
        transform = out["best_global_transform"]
        rows.append(
            {
                "case_id": rec.case_id,
                "split": rec.split,
                "class_label": rec.class_label,
                "true_hypothesis": rec.hypothesis_label,
                "pred_hypothesis": out["pred_hypothesis"],
                "confidence_margin": out["confidence_margin"],
                "via_evidence": out["via_evidence"],
                "scores": {k: v.score for k, v in out["results"].items()},
                "residuals": {k: v.residual_rel_l2 for k, v in out["results"].items()},
                "results": out["results"],
                "record": rec,
                "best_global_transform": transform,
                "best_global_translation_norm_m": out["best_global_translation_norm_m"],
                "best_global_rotation_abs_deg": out["best_global_rotation_abs_deg"],
                "best_global_scale_delta": out["best_global_scale_delta"],
            }
        )
    return rows


def _unknown_thresholds(rows_val: List[dict], cfg: dict) -> dict:
    unk_cfg = cfg.get("unknown_rejection", {})
    margin_q = float(unk_cfg.get("margin_quantile", 0.05))
    residual_q = float(unk_cfg.get("residual_quantile", 0.95))
    residual_multiplier = float(unk_cfg.get("residual_multiplier", 1.5))
    margins = np.asarray([float(r["confidence_margin"]) for r in rows_val], dtype=float)
    residuals = np.asarray([_best_residual(r) for r in rows_val], dtype=float)
    return {
        "min_margin": float(np.quantile(margins, margin_q)),
        "max_residual": float(np.quantile(residuals, residual_q) * residual_multiplier),
        "margin_quantile": margin_q,
        "residual_quantile": residual_q,
        "residual_multiplier": residual_multiplier,
    }


def _unknown_summary(rows: List[dict], thresholds: dict) -> dict:
    accepted = [
        r for r in rows
        if float(r["confidence_margin"]) >= thresholds["min_margin"] and _best_residual(r) <= thresholds["max_residual"]
    ]
    rejected = len(rows) - len(accepted)
    acc_all = hypothesis_accuracy([r["true_hypothesis"] for r in rows], [r["pred_hypothesis"] for r in rows]) if rows else float("nan")
    acc_acc = hypothesis_accuracy(
        [r["true_hypothesis"] for r in accepted], [r["pred_hypothesis"] for r in accepted]
    ) if accepted else float("nan")
    return {
        "n": len(rows),
        "accepted": len(accepted),
        "rejected": rejected,
        "unknown_rate": rejected / max(len(rows), 1),
        "full_accuracy": acc_all,
        "accepted_accuracy": acc_acc,
        "median_margin": float(np.median([r["confidence_margin"] for r in rows])) if rows else float("nan"),
        "median_best_residual": float(np.median([_best_residual(r) for r in rows])) if rows else float("nan"),
    }


def _unknown_table_row(name: str, summary: dict) -> List[object]:
    return [
        name,
        int(summary["n"]),
        int(summary["accepted"]),
        int(summary["rejected"]),
        fmt_float(summary["unknown_rate"]),
        fmt_float(summary["full_accuracy"]),
        fmt_float(summary["accepted_accuracy"]),
        fmt_float(summary["median_margin"]),
        fmt_float(summary["median_best_residual"]),
    ]


def _selective_unknown_rows(name: str, rows: List[dict], coverages=(0.2, 0.4, 0.6, 0.8, 1.0)) -> List[List[object]]:
    if not rows:
        return []
    confidence = np.asarray(
        [float(r["confidence_margin"]) / (_best_residual(r) + 1e-12) for r in rows],
        dtype=float,
    )
    order = np.argsort(-confidence)
    out: List[List[object]] = []
    for cov in coverages:
        k = max(1, int(round(float(cov) * len(rows))))
        idx = order[:k]
        selected = [rows[int(i)] for i in idx]
        acc = hypothesis_accuracy(
            [r["true_hypothesis"] for r in selected],
            [r["pred_hypothesis"] for r in selected],
        )
        out.append([
            name,
            f"{int(cov * 100)}%",
            int(k),
            int(len(rows) - k),
            fmt_float(acc),
            fmt_float(1.0 - acc),
            fmt_float(float(np.median(confidence[idx]))),
        ])
    return out


def _safe_zscore(values: np.ndarray, center: float, scale: float) -> np.ndarray:
    return (values - center) / max(float(scale), 1e-12)


def _score_entropy(row: dict) -> float:
    vals = np.asarray(list(row["scores"].values()), dtype=float)
    if len(vals) <= 1:
        return 0.0
    shifted = vals - float(np.min(vals))
    scale = float(np.std(shifted)) + 1e-12
    weights = np.exp(-shifted / scale)
    probs = weights / max(float(np.sum(weights)), 1e-12)
    entropy = -float(np.sum(probs * np.log(probs + 1e-12)))
    return entropy / float(np.log(len(vals)))


def _residual_gap(row: dict) -> float:
    vals = sorted(float(v) for v in row["residuals"].values())
    if len(vals) < 2:
        return 0.0
    return vals[1] - vals[0]


def _residual_only_prediction(row: dict) -> str:
    return min(row["residuals"], key=lambda k: float(row["residuals"][k]))


def _unknown_detector_ablation_rows(
    clean_rows: List[dict],
    hidden_rows: List[dict],
    clean_marg_rows: List[dict],
    hidden_marg_rows: List[dict],
    cfg: dict,
) -> List[List[object]]:
    clean_by_id = {r["case_id"]: r for r in clean_marg_rows}
    hidden_by_id = {r["case_id"]: r for r in hidden_marg_rows}

    def _arrays(rows: List[dict], marg_by_id: dict[str, dict]) -> dict[str, np.ndarray]:
        residual = np.asarray([_best_residual(r) for r in rows], dtype=float)
        margin = np.asarray([float(r["confidence_margin"]) for r in rows], dtype=float)
        margin_ratio = margin / (residual + 1e-12)
        instability = np.asarray(
            [float(marg_by_id.get(r["case_id"], {}).get("best_via_offset_norm_m", 0.0)) for r in rows],
            dtype=float,
        )
        disagreement = np.asarray(
            [
                float(marg_by_id.get(r["case_id"], {}).get("pred_hypothesis", r["pred_hypothesis"]) != r["pred_hypothesis"])
                for r in rows
            ],
            dtype=float,
        )
        evidence_entropy = np.asarray([_score_entropy(r) for r in rows], dtype=float)
        residual_gap = np.asarray([_residual_gap(r) for r in rows], dtype=float)
        h0_h1_ambiguity = np.asarray(
            [-abs(float(r["scores"]["H1_sheet_via"]) - float(r["scores"]["H0_sheet_only"])) for r in rows],
            dtype=float,
        )
        residual_score_disagreement = np.asarray(
            [float(_residual_only_prediction(r) != r["pred_hypothesis"]) for r in rows],
            dtype=float,
        )
        return {
            "margin_only": -margin,
            "residual_only": residual,
            "margin_over_residual": -margin_ratio,
            "registration_instability": instability,
            "prediction_disagreement": disagreement,
            "evidence_entropy": evidence_entropy,
            "residual_gap_ambiguity": 1.0 / (residual_gap + 1e-12),
            "h0_h1_score_ambiguity": h0_h1_ambiguity,
            "residual_score_disagreement": residual_score_disagreement,
        }

    clean_scores = _arrays(clean_rows, clean_by_id)
    hidden_scores = _arrays(hidden_rows, hidden_by_id)
    combined_clean = np.zeros(len(clean_rows), dtype=float)
    combined_hidden = np.zeros(len(hidden_rows), dtype=float)
    for key in ["margin_only", "residual_only", "margin_over_residual", "registration_instability", "prediction_disagreement"]:
        c = clean_scores[key]
        center = float(np.median(c))
        scale = float(np.std(c)) + 1e-12
        combined_clean += _safe_zscore(c, center, scale)
        combined_hidden += _safe_zscore(hidden_scores[key], center, scale)
    clean_scores["combined_unknown_score"] = combined_clean
    hidden_scores["combined_unknown_score"] = combined_hidden
    physical_clean = np.zeros(len(clean_rows), dtype=float)
    physical_hidden = np.zeros(len(hidden_rows), dtype=float)
    for key in [
        "evidence_entropy",
        "residual_gap_ambiguity",
        "h0_h1_score_ambiguity",
        "residual_score_disagreement",
        "registration_instability",
    ]:
        c = clean_scores[key]
        center = float(np.median(c))
        scale = float(np.std(c)) + 1e-12
        physical_clean += _safe_zscore(c, center, scale)
        physical_hidden += _safe_zscore(hidden_scores[key], center, scale)
    clean_scores["combined_physical_unknown_score"] = physical_clean
    hidden_scores["combined_physical_unknown_score"] = physical_hidden

    false_reject = float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20))
    rows_out: List[List[object]] = []
    clean_true = [r["true_hypothesis"] for r in clean_rows]
    clean_pred = [r["pred_hypothesis"] for r in clean_rows]
    hidden_true = [r["true_hypothesis"] for r in hidden_rows]
    hidden_pred = [r["pred_hypothesis"] for r in hidden_rows]
    for name in [
        "margin_only",
        "residual_only",
        "margin_over_residual",
        "registration_instability",
        "prediction_disagreement",
        "evidence_entropy",
        "residual_gap_ambiguity",
        "h0_h1_score_ambiguity",
        "residual_score_disagreement",
        "combined_unknown_score",
        "combined_physical_unknown_score",
    ]:
        c = clean_scores[name]
        h = hidden_scores[name]
        threshold = float(np.quantile(c, max(0.0, min(1.0, 1.0 - false_reject))))
        clean_reject = c >= threshold
        hidden_reject = h >= threshold
        clean_accept_idx = np.where(~clean_reject)[0]
        hidden_accept_idx = np.where(~hidden_reject)[0]
        clean_acc = hypothesis_accuracy(
            [clean_true[int(i)] for i in clean_accept_idx],
            [clean_pred[int(i)] for i in clean_accept_idx],
        ) if len(clean_accept_idx) else float("nan")
        hidden_acc = hypothesis_accuracy(
            [hidden_true[int(i)] for i in hidden_accept_idx],
            [hidden_pred[int(i)] for i in hidden_accept_idx],
        ) if len(hidden_accept_idx) else float("nan")
        rows_out.append([
            name,
            fmt_float(threshold),
            fmt_float(float(np.mean(clean_reject))),
            fmt_float(float(np.mean(hidden_reject))),
            int(len(clean_accept_idx)),
            int(len(hidden_accept_idx)),
            fmt_float(clean_acc),
            fmt_float(hidden_acc),
        ])
    return rows_out


def _to_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def _model_selection_calibration_rows(evidence_rows: List[List[object]], cfg: dict) -> List[List[object]]:
    """Rank PyPEEC model-bank entries by a fixed audit objective.

    This is deliberately not used to change the current frozen predictions. It
    makes the H0/H1/model-complexity trade-off explicit instead of hiding it in
    a single residual column.
    """
    cal_cfg = cfg.get("model_selection_calibration", {})
    weights = cal_cfg.get("objective_weights", {})
    w_acc = float(weights.get("accuracy", 0.40))
    w_h0 = float(weights.get("h0_accuracy", 0.30))
    w_h1 = float(weights.get("h1_accuracy", 0.20))
    w_h2 = float(weights.get("h2_accuracy", 0.10))
    w_fp = float(weights.get("false_positive", 0.10))
    w_param = float(weights.get("parameter_count", 0.02))
    min_h1 = float(cal_cfg.get("min_h1_accuracy", 0.65))

    ranked = []
    for row in evidence_rows:
        if row[0] != "B_pypeec":
            continue
        acc = _to_float(row[4])
        h0 = _to_float(row[5])
        h1 = _to_float(row[6])
        h2 = _to_float(row[7])
        false_h1 = _to_float(row[9])
        false_h2 = _to_float(row[10])
        false_h3 = _to_float(row[11])
        residual = _to_float(row[12])
        params = _to_float(row[13])
        fp_sum = np.nansum([false_h1, false_h2, false_h3])
        objective = (
            w_acc * acc
            + w_h0 * h0
            + w_h1 * h1
            + w_h2 * h2
            - w_fp * fp_sum
            - w_param * params
        )
        ranked.append([
            row[1],
            row[2],
            fmt_float(objective),
            fmt_float(acc),
            fmt_float(h0),
            fmt_float(h1),
            fmt_float(h2),
            fmt_float(false_h1),
            fmt_float(false_h2),
            fmt_float(false_h3),
            fmt_float(residual),
            fmt_float(params),
            bool(h1 >= min_h1),
        ])
    ranked.sort(key=lambda r: _to_float(r[2]), reverse=True)
    return ranked


def _model_selection_objective(summary: dict, cfg: dict) -> float:
    cal_cfg = cfg.get("model_selection_calibration", {})
    weights = cal_cfg.get("objective_weights", {})
    pc = summary["per_class_accuracy"]
    # For model selection safety, the false-explanation penalty should be
    # measured on true H0/no-via rows when that stricter endpoint is available.
    # Return-current H2 rows are not H0 false positives.
    fp_prefix = "h0_false" if "h0_false_h1_rate" in summary else "false"
    fp_sum = np.nansum([
        float(summary.get(f"{fp_prefix}_h1_rate", 0.0)),
        float(summary.get(f"{fp_prefix}_h2_rate", 0.0)),
        float(summary.get(f"{fp_prefix}_h3_rate", 0.0)),
    ])
    return (
        float(weights.get("accuracy", 0.40)) * float(summary["accuracy"])
        + float(weights.get("h0_accuracy", 0.30)) * float(pc.get("H0_sheet_only", 0.0))
        + float(weights.get("h1_accuracy", 0.20)) * float(pc.get("H1_sheet_via", 0.0))
        + float(weights.get("h2_accuracy", 0.10)) * float(pc.get("H2_sheet_return", 0.0))
        - float(weights.get("false_positive", 0.10)) * float(fp_sum)
        - float(weights.get("parameter_count", 0.02)) * float(summary.get("median_parameter_count", 0.0))
    )


def _evidence_detail_rows(
    field_key: str,
    basis_mode: str,
    evidence_mode: str,
    rows: List[dict],
    labels: List[str],
    cfg: dict,
) -> List[dict]:
    n_obs = int(rows[0]["record"].b_obs.size) if rows else 1
    details = []
    for row in rows:
        evidence_scores = {
            label: _evidence_score(row["results"][label], evidence_mode, cfg, n_obs)
            for label in labels
        }
        ordered = sorted(labels, key=lambda label: evidence_scores[label])
        pred = ordered[0]
        margin = float(evidence_scores[ordered[1]] - evidence_scores[ordered[0]]) if len(ordered) > 1 else 0.0
        rec = row["record"]
        details.append({
            "field": field_key,
            "basis_mode": basis_mode,
            "evidence_mode": evidence_mode,
            "case_id": row["case_id"],
            "class_label": row["class_label"],
            "true_hypothesis": row["true_hypothesis"],
            "pred_hypothesis": pred,
            "family": str(
                rec.metadata.get(
                    "hidden_mechanism_family",
                    rec.metadata.get("case_type", rec.metadata.get("route_family", row["class_label"])),
                )
            ),
            "residual": float(row["results"][pred].residual_rel_l2),
            "n_basis": float(row["results"][pred].n_basis),
            "margin": margin,
            "evidence_scores": evidence_scores,
        })
    return details


def _details_summary(details: List[dict], labels: List[str]) -> dict:
    true = [d["true_hypothesis"] for d in details]
    pred = [d["pred_hypothesis"] for d in details]
    no_via = [i for i, d in enumerate(details) if d["class_label"] != "true_via"]
    false_h1 = float(np.mean([pred[i] == "H1_sheet_via" for i in no_via])) if no_via else float("nan")
    false_h2 = float(np.mean([pred[i] == "H2_sheet_return" for i in no_via])) if no_via else float("nan")
    false_h3 = float(np.mean([pred[i] == "H3_sheet_artifact" for i in no_via])) if no_via else float("nan")
    h0_idx = [i for i, d in enumerate(details) if d["true_hypothesis"] == "H0_sheet_only"]
    h0_false_h1 = float(np.mean([pred[i] == "H1_sheet_via" for i in h0_idx])) if h0_idx else float("nan")
    h0_false_h2 = float(np.mean([pred[i] == "H2_sheet_return" for i in h0_idx])) if h0_idx else float("nan")
    h0_false_h3 = float(np.mean([pred[i] == "H3_sheet_artifact" for i in h0_idx])) if h0_idx else float("nan")
    return {
        "n": len(details),
        "accuracy": hypothesis_accuracy(true, pred),
        "per_class_accuracy": per_class_accuracy(true, pred),
        "false_h1_rate": false_h1,
        "false_h2_rate": false_h2,
        "false_h3_rate": false_h3,
        "h0_false_h1_rate": h0_false_h1,
        "h0_false_h2_rate": h0_false_h2,
        "h0_false_h3_rate": h0_false_h3,
        "median_residual": float(np.median([d["residual"] for d in details])) if details else float("nan"),
        "median_parameter_count": float(np.median([d["n_basis"] for d in details])) if details else float("nan"),
    }


def _pypeec_split_map(details: List[dict], cfg: dict) -> dict[str, str]:
    fraction = float(cfg.get("model_selection_calibration", {}).get("pypeec_calibration_fraction", 0.5))
    fraction = min(max(fraction, 0.25), 0.75)
    by_true: dict[str, list[str]] = defaultdict(list)
    for d in details:
        by_true[d["true_hypothesis"]].append(d["case_id"])
    split = {}
    for _, case_ids in sorted(by_true.items()):
        unique = sorted(set(case_ids))
        n_cal = max(1, min(len(unique) - 1, int(round(len(unique) * fraction)))) if len(unique) > 1 else len(unique)
        for idx, case_id in enumerate(unique):
            split[case_id] = "calibration" if idx < n_cal else "heldout"
    return split


def _pypeec_repeated_split_map(details: List[dict], cfg: dict, repeat_index: int) -> dict[str, str]:
    cal_cfg = cfg.get("model_selection_calibration", {})
    fraction = float(cal_cfg.get("pypeec_calibration_fraction", 0.5))
    fraction = min(max(fraction, 0.25), 0.75)
    seed = int(cal_cfg.get("repeated_split_seed", cfg.get("seed", 0)))
    rng = np.random.default_rng(seed + 1009 * int(repeat_index))
    by_true: dict[str, list[str]] = defaultdict(list)
    for d in details:
        by_true[d["true_hypothesis"]].append(d["case_id"])
    split = {}
    for true_h, case_ids in sorted(by_true.items()):
        unique = np.asarray(sorted(set(case_ids)), dtype=object)
        if len(unique) > 1:
            perm = rng.permutation(len(unique))
            unique = unique[perm]
        n_cal = max(1, min(len(unique) - 1, int(round(len(unique) * fraction)))) if len(unique) > 1 else len(unique)
        for idx, case_id in enumerate(unique.tolist()):
            split[str(case_id)] = "calibration" if idx < n_cal else "heldout"
    return split


def _pypeec_heldout_model_selection_rows(details: List[dict], labels: List[str], cfg: dict) -> tuple[List[List[object]], List[List[object]]]:
    split = _pypeec_split_map(details, cfg)
    keys = sorted({(d["basis_mode"], d["evidence_mode"]) for d in details})
    ranked = []
    tradeoff = []
    for basis_mode, evidence_mode in keys:
        combo = [d for d in details if d["basis_mode"] == basis_mode and d["evidence_mode"] == evidence_mode]
        cal = [d for d in combo if split.get(d["case_id"]) == "calibration"]
        held = [d for d in combo if split.get(d["case_id"]) == "heldout"]
        cal_summary = _details_summary(cal, labels)
        held_summary = _details_summary(held, labels)
        cal_obj = _model_selection_objective(cal_summary, cfg)
        held_obj = _model_selection_objective(held_summary, cfg)
        cal_pc = cal_summary["per_class_accuracy"]
        held_pc = held_summary["per_class_accuracy"]
        ranked.append([
            basis_mode,
            evidence_mode,
            fmt_float(cal_obj),
            fmt_float(held_obj),
            int(cal_summary["n"]),
            int(held_summary["n"]),
            fmt_float(cal_summary["accuracy"]),
            fmt_float(held_summary["accuracy"]),
            fmt_float(cal_pc.get("H0_sheet_only", float("nan"))),
            fmt_float(held_pc.get("H0_sheet_only", float("nan"))),
            fmt_float(cal_pc.get("H1_sheet_via", float("nan"))),
            fmt_float(held_pc.get("H1_sheet_via", float("nan"))),
            fmt_float(held_pc.get("H2_sheet_return", float("nan"))),
            fmt_float(held_summary["h0_false_h1_rate"]),
            fmt_float(held_summary["h0_false_h2_rate"]),
            fmt_float(held_summary["h0_false_h3_rate"]),
        ])
        tradeoff.append([
            basis_mode,
            evidence_mode,
            fmt_float(held_pc.get("H0_sheet_only", float("nan"))),
            fmt_float(held_pc.get("H1_sheet_via", float("nan"))),
            fmt_float(held_summary["accuracy"]),
            fmt_float(held_summary["h0_false_h1_rate"]),
            fmt_float(held_summary["h0_false_h2_rate"]),
            fmt_float(held_summary["h0_false_h3_rate"]),
            fmt_float(held_summary["median_residual"]),
            fmt_float(held_summary["median_parameter_count"]),
        ])
    ranked.sort(key=lambda r: _to_float(r[2]), reverse=True)
    tradeoff.sort(key=lambda r: (_to_float(r[2]), _to_float(r[3]), _to_float(r[4])), reverse=True)
    return ranked, tradeoff


def _mean_std(values: list[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return float("nan"), float("nan")
    return float(np.mean(arr)), float(np.std(arr))


def _ci(values: list[float], level: float) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return float("nan"), float("nan")
    alpha = max(0.0, min(0.49, (1.0 - float(level)) / 2.0))
    return float(np.quantile(arr, alpha)), float(np.quantile(arr, 1.0 - alpha))


def _pypeec_model_selection_stability_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    """Repeated stratified split audit for PyPEEC model selection.

    The current PyPEEC mini set is still too small for a final model-selection
    claim. This repeated split table estimates ranking stability and held-out
    variance without changing any frozen bridge predictions.
    """
    cal_cfg = cfg.get("model_selection_calibration", {})
    n_repeats = int(cal_cfg.get("repeated_split_count", 25))
    ci_level = float(cal_cfg.get("bootstrap_ci_level", 0.90))
    keys = sorted({(d["basis_mode"], d["evidence_mode"]) for d in details})
    stats = {
        key: {
            "selected": 0,
            "held_obj": [],
            "held_acc": [],
            "held_h0": [],
            "held_h1": [],
            "held_h2": [],
            "held_h0_false_any": [],
            "held_params": [],
        }
        for key in keys
    }
    for repeat_idx in range(n_repeats):
        split = _pypeec_repeated_split_map(details, cfg, repeat_idx)
        cal_rank: list[tuple[float, tuple[str, str]]] = []
        for key in keys:
            basis_mode, evidence_mode = key
            combo = [d for d in details if d["basis_mode"] == basis_mode and d["evidence_mode"] == evidence_mode]
            cal = [d for d in combo if split.get(d["case_id"]) == "calibration"]
            held = [d for d in combo if split.get(d["case_id"]) == "heldout"]
            cal_summary = _details_summary(cal, labels)
            held_summary = _details_summary(held, labels)
            cal_obj = _model_selection_objective(cal_summary, cfg)
            held_obj = _model_selection_objective(held_summary, cfg)
            cal_rank.append((cal_obj, key))
            pc = held_summary["per_class_accuracy"]
            stats[key]["held_obj"].append(float(held_obj))
            stats[key]["held_acc"].append(float(held_summary["accuracy"]))
            stats[key]["held_h0"].append(float(pc.get("H0_sheet_only", float("nan"))))
            stats[key]["held_h1"].append(float(pc.get("H1_sheet_via", float("nan"))))
            stats[key]["held_h2"].append(float(pc.get("H2_sheet_return", float("nan"))))
            h0_false_any = np.nansum([
                float(held_summary.get("h0_false_h1_rate", 0.0)),
                float(held_summary.get("h0_false_h2_rate", 0.0)),
                float(held_summary.get("h0_false_h3_rate", 0.0)),
            ])
            stats[key]["held_h0_false_any"].append(float(h0_false_any))
            stats[key]["held_params"].append(float(held_summary.get("median_parameter_count", float("nan"))))
        cal_rank.sort(key=lambda item: item[0], reverse=True)
        if cal_rank:
            stats[cal_rank[0][1]]["selected"] += 1
    rows = []
    for basis_mode, evidence_mode in keys:
        s = stats[(basis_mode, evidence_mode)]
        obj_mean, obj_std = _mean_std(s["held_obj"])
        obj_lo, obj_hi = _ci(s["held_obj"], ci_level)
        acc_mean, acc_std = _mean_std(s["held_acc"])
        h0_mean, h0_std = _mean_std(s["held_h0"])
        h1_mean, h1_std = _mean_std(s["held_h1"])
        h2_mean, _ = _mean_std(s["held_h2"])
        h0_false_mean, _ = _mean_std(s["held_h0_false_any"])
        params_mean, _ = _mean_std(s["held_params"])
        rows.append([
            basis_mode,
            evidence_mode,
            int(n_repeats),
            int(s["selected"]),
            fmt_float(float(s["selected"]) / max(n_repeats, 1)),
            fmt_float(obj_mean),
            fmt_float(obj_std),
            fmt_float(obj_lo),
            fmt_float(obj_hi),
            fmt_float(acc_mean),
            fmt_float(acc_std),
            fmt_float(h0_mean),
            fmt_float(h0_std),
            fmt_float(h1_mean),
            fmt_float(h1_std),
            fmt_float(h2_mean),
            fmt_float(h0_false_mean),
            fmt_float(params_mean),
        ])
    rows.sort(key=lambda r: (_to_float(r[4]), _to_float(r[5]), _to_float(r[11]), _to_float(r[13])), reverse=True)
    return rows


def _margin_threshold_grid(details: List[dict], labels: List[str]) -> dict[str, list[float]]:
    grids: dict[str, list[float]] = {}
    base = [0.0, 1e-4, 5e-4, 1e-3, 3e-3, 5e-3, 1e-2, 2e-2, 5e-2]
    for label in labels:
        margins = np.asarray(
            [float(d.get("margin", 0.0)) for d in details if d.get("pred_hypothesis") == label],
            dtype=float,
        )
        margins = margins[np.isfinite(margins)]
        vals = list(base)
        if len(margins):
            vals += [float(np.quantile(margins, q)) for q in [0.10, 0.25, 0.50, 0.75, 0.90]]
        vals = sorted({float(max(0.0, v)) for v in vals if np.isfinite(v)})
        grids[label] = vals[:]
    return grids


def _apply_class_specific_margin_refusal(details: List[dict], thresholds: dict[str, float]) -> list[str]:
    pred: list[str] = []
    for d in details:
        label = str(d["pred_hypothesis"])
        margin = float(d.get("margin", 0.0))
        pred.append(label if margin >= float(thresholds.get(label, 0.0)) else "UNKNOWN")
    return pred


def _selective_prediction_summary(details: List[dict], pred: list[str], labels: List[str]) -> dict:
    true = [str(d["true_hypothesis"]) for d in details]
    accepted_idx = [i for i, p in enumerate(pred) if p != "UNKNOWN"]
    accepted_true = [true[i] for i in accepted_idx]
    accepted_pred = [pred[i] for i in accepted_idx]
    all_true_count = {label: sum(1 for t in true if t == label) for label in labels}
    per_class_accept = {
        label: float(sum(1 for i, t in enumerate(true) if t == label and pred[i] != "UNKNOWN") / max(all_true_count[label], 1))
        for label in labels
    }
    per_class_correct = {}
    for label in labels:
        accepted_label = [i for i in accepted_idx if true[i] == label]
        per_class_correct[label] = (
            float(np.mean([pred[i] == true[i] for i in accepted_label])) if accepted_label else float("nan")
        )
    h0_idx = [i for i, t in enumerate(true) if t == "H0_sheet_only"]
    h0_false_any = (
        float(np.mean([pred[i] not in {"H0_sheet_only", "UNKNOWN"} for i in h0_idx])) if h0_idx else float("nan")
    )
    return {
        "n": len(details),
        "coverage": float(len(accepted_idx) / max(len(details), 1)),
        "unknown_rate": float(1.0 - len(accepted_idx) / max(len(details), 1)),
        "accepted_accuracy": hypothesis_accuracy(accepted_true, accepted_pred) if accepted_idx else float("nan"),
        "per_class_accept": per_class_accept,
        "per_class_correct": per_class_correct,
        "h0_false_any": h0_false_any,
    }


def _select_class_specific_thresholds(cal: List[dict], labels: List[str]) -> tuple[dict[str, float], dict]:
    grids = _margin_threshold_grid(cal, labels)
    best_thresholds = {label: 0.0 for label in labels}
    best_summary: dict | None = None
    best_obj = -float("inf")
    grid_values = [grids.get(label, [0.0]) for label in labels]
    for combo in itertools.product(*grid_values):
        thresholds = {label: float(value) for label, value in zip(labels, combo)}
        pred = _apply_class_specific_margin_refusal(cal, thresholds)
        summary = _selective_prediction_summary(cal, pred, labels)
        pc = summary["per_class_correct"]
        coverage = float(summary["coverage"])
        acc = float(summary["accepted_accuracy"])
        h0_false = float(summary["h0_false_any"])
        if not np.isfinite(acc):
            continue
        # The objective is intentionally conservative on H0 false alarms while
        # still rewarding accepted true-via correctness. It is an audit policy,
        # not a PyPEEC test-set tuned detector.
        obj = (
            2.50 * acc
            + 0.60 * float(pc.get("H0_sheet_only", 0.0))
            + 0.60 * float(pc.get("H1_sheet_via", 0.0))
            + 0.25 * float(pc.get("H2_sheet_return", 0.0))
            + 0.25 * float(pc.get("H3_sheet_artifact", 0.0))
            + 0.25 * coverage
            - 4.00 * h0_false
        )
        if coverage < 0.50:
            obj -= 1.0
        if obj > best_obj:
            best_obj = float(obj)
            best_thresholds = thresholds
            best_summary = summary
    return best_thresholds, (best_summary or {})


def _pypeec_class_specific_selective_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    """Audit class-specific refusal margins under repeated PyPEEC splits.

    This formalizes the main bottleneck discovered after the one-point null-via
    gate: a single operating point can protect H0/no-via only by damaging
    true-via recall. The table asks whether class-specific margins produce a
    stable, auditable trusted-output region without changing frozen predictions.
    """
    cal_cfg = cfg.get("model_selection_calibration", {})
    n_repeats = int(cal_cfg.get("repeated_split_count", 25))
    target = [
        d
        for d in details
        if d["field"] == "B_pypeec"
        and d["basis_mode"] == "finite_width_sheet"
        and d["evidence_mode"] == "h0_conservative"
    ]
    if not target:
        return [[
            "class_specific_margin_refusal",
            "B_pypeec",
            "finite_width_sheet",
            "h0_conservative",
            0,
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "nan",
            "no_rows",
        ]]
    metrics = {
        "coverage": [],
        "unknown": [],
        "accepted_acc": [],
        "h0_false_any": [],
        "h0_correct": [],
        "h1_correct": [],
        "h2_correct": [],
        "h3_correct": [],
        "h0_accept": [],
        "h1_accept": [],
        "h2_accept": [],
        "h3_accept": [],
    }
    for repeat_idx in range(n_repeats):
        split = _pypeec_repeated_split_map(target, cfg, repeat_idx)
        cal = [d for d in target if split.get(d["case_id"]) == "calibration"]
        held = [d for d in target if split.get(d["case_id"]) == "heldout"]
        thresholds, _ = _select_class_specific_thresholds(cal, labels)
        held_pred = _apply_class_specific_margin_refusal(held, thresholds)
        summary = _selective_prediction_summary(held, held_pred, labels)
        pc = summary["per_class_correct"]
        pa = summary["per_class_accept"]
        metrics["coverage"].append(float(summary["coverage"]))
        metrics["unknown"].append(float(summary["unknown_rate"]))
        metrics["accepted_acc"].append(float(summary["accepted_accuracy"]))
        metrics["h0_false_any"].append(float(summary["h0_false_any"]))
        metrics["h0_correct"].append(float(pc.get("H0_sheet_only", float("nan"))))
        metrics["h1_correct"].append(float(pc.get("H1_sheet_via", float("nan"))))
        metrics["h2_correct"].append(float(pc.get("H2_sheet_return", float("nan"))))
        metrics["h3_correct"].append(float(pc.get("H3_sheet_artifact", float("nan"))))
        metrics["h0_accept"].append(float(pa.get("H0_sheet_only", float("nan"))))
        metrics["h1_accept"].append(float(pa.get("H1_sheet_via", float("nan"))))
        metrics["h2_accept"].append(float(pa.get("H2_sheet_return", float("nan"))))
        metrics["h3_accept"].append(float(pa.get("H3_sheet_artifact", float("nan"))))
    def _q(values: list[float], q: float) -> float:
        arr = np.asarray(values, dtype=float)
        arr = arr[np.isfinite(arr)]
        return float(np.quantile(arr, q)) if len(arr) else float("nan")

    status = "h0_safe_but_h1_recall_limited"
    h0_false_mean, _ = _mean_std(metrics["h0_false_any"])
    h1_accept_mean, _ = _mean_std(metrics["h1_accept"])
    h1_correct_mean, _ = _mean_std(metrics["h1_correct"])
    if h0_false_mean <= 0.05 and h1_accept_mean >= 0.80 and h1_correct_mean >= 0.85:
        status = "balanced_candidate"
    elif h0_false_mean > 0.10:
        status = "h0_safety_insufficient"
    rows = [[
        "class_specific_margin_refusal",
        "B_pypeec",
        "finite_width_sheet",
        "h0_conservative",
        int(n_repeats),
        fmt_float(_mean_std(metrics["coverage"])[0]),
        fmt_float(_mean_std(metrics["coverage"])[1]),
        fmt_float(_q(metrics["coverage"], 0.10)),
        fmt_float(_q(metrics["coverage"], 0.90)),
        fmt_float(_mean_std(metrics["accepted_acc"])[0]),
        fmt_float(_mean_std(metrics["accepted_acc"])[1]),
        fmt_float(_mean_std(metrics["h0_false_any"])[0]),
        fmt_float(_q(metrics["h0_false_any"], 0.50)),
        fmt_float(_mean_std(metrics["h0_correct"])[0]),
        fmt_float(_mean_std(metrics["h1_correct"])[0]),
        fmt_float(_mean_std(metrics["h1_accept"])[0]),
        fmt_float(_mean_std(metrics["unknown"])[0]),
        status,
    ]]
    return rows


def _stacked_evidence_dataset(
    details: List[dict],
    labels: List[str],
    field_key: str = "B_pypeec",
) -> tuple[list[str], np.ndarray, np.ndarray, list[dict], dict[str, dict]]:
    target = [d for d in details if d["field"] == field_key]
    case_ids = sorted({str(d["case_id"]) for d in target})
    combos = sorted({(str(d["basis_mode"]), str(d["evidence_mode"])) for d in target})
    by_case_combo = {(str(d["case_id"]), str(d["basis_mode"]), str(d["evidence_mode"])): d for d in target}
    true_by_case = {str(d["case_id"]): str(d["true_hypothesis"]) for d in target}
    meta_by_case = {
        str(d["case_id"]): {
            "true_hypothesis": str(d["true_hypothesis"]),
            "class_label": str(d["class_label"]),
            "family": str(d.get("family", "unknown")),
        }
        for d in target
    }
    features = []
    feature_tags: list[dict] = []
    for basis_mode, evidence_mode in combos:
        for label in labels:
            feature_tags.append({"basis": basis_mode, "evidence": evidence_mode, "kind": "score", "label": label})
        for label in labels:
            feature_tags.append({"basis": basis_mode, "evidence": evidence_mode, "kind": "pred_one_hot", "label": label})
        for kind in ["margin", "residual", "n_basis"]:
            feature_tags.append({"basis": basis_mode, "evidence": evidence_mode, "kind": kind, "label": ""})
    for case_id in case_ids:
        row_features: list[float] = []
        for basis_mode, evidence_mode in combos:
            d = by_case_combo[(case_id, basis_mode, evidence_mode)]
            scores = np.asarray([float(d["evidence_scores"][label]) for label in labels], dtype=float)
            if not np.all(np.isfinite(scores)):
                scores = np.nan_to_num(scores, nan=0.0, posinf=0.0, neginf=0.0)
            rel_scores = scores - float(np.min(scores))
            pred_idx = labels.index(str(d["pred_hypothesis"]))
            pred_one_hot = np.zeros(len(labels), dtype=float)
            pred_one_hot[pred_idx] = 1.0
            row_features.extend(rel_scores.tolist())
            row_features.extend(pred_one_hot.tolist())
            row_features.extend([
                float(d.get("margin", 0.0)),
                float(d.get("residual", 0.0)),
                float(d.get("n_basis", 0.0)),
            ])
        features.append(row_features)
    x = np.asarray(features, dtype=float)
    x[~np.isfinite(x)] = 0.0
    y = np.asarray([labels.index(true_by_case[case_id]) for case_id in case_ids], dtype=int)
    return case_ids, x, y, feature_tags, meta_by_case


def _stacked_evidence_feature_matrix(details: List[dict], labels: List[str]) -> tuple[list[str], np.ndarray, np.ndarray]:
    case_ids, x, y, _, _ = _stacked_evidence_dataset(details, labels)
    return case_ids, x, y


def _fit_ridge_evidence_calibrator(x_train: np.ndarray, y_train: np.ndarray, n_labels: int, alpha: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = np.mean(x_train, axis=0)
    std = np.std(x_train, axis=0)
    std[std < 1e-9] = 1.0
    xz = (x_train - mean) / std
    design = np.c_[np.ones(len(xz)), xz]
    target = np.zeros((len(y_train), n_labels), dtype=float)
    target[np.arange(len(y_train)), y_train] = 1.0
    reg = np.eye(design.shape[1], dtype=float)
    reg[0, 0] = 0.0
    weights = np.linalg.solve(design.T @ design + float(alpha) * reg, design.T @ target)
    return mean, std, weights


def _predict_ridge_evidence_calibrator(x: np.ndarray, mean: np.ndarray, std: np.ndarray, weights: np.ndarray) -> np.ndarray:
    xz = (x - mean) / std
    design = np.c_[np.ones(len(xz)), xz]
    return np.asarray(design @ weights, dtype=float)


def _stacked_prediction_summary(y_true: np.ndarray, y_pred: np.ndarray, labels: List[str]) -> dict:
    summary = {
        "accuracy": float(np.mean(y_true == y_pred)) if len(y_true) else float("nan"),
        "per_class": {},
        "h0_false_any": float("nan"),
    }
    for idx, label in enumerate(labels):
        mask = y_true == idx
        summary["per_class"][label] = float(np.mean(y_pred[mask] == y_true[mask])) if np.any(mask) else float("nan")
    h0 = y_true == labels.index("H0_sheet_only")
    summary["h0_false_any"] = float(np.mean(y_pred[h0] != y_true[h0])) if np.any(h0) else float("nan")
    return summary


def _stacked_eval_run(
    x: np.ndarray,
    y: np.ndarray,
    train_mask: np.ndarray,
    eval_mask: np.ndarray,
    labels: List[str],
    alpha: float,
    feature_idx: np.ndarray | None = None,
) -> tuple[dict, np.ndarray, np.ndarray]:
    if feature_idx is None:
        feature_idx = np.arange(x.shape[1])
    x_sub = x[:, feature_idx]
    mean, std, weights = _fit_ridge_evidence_calibrator(x_sub[train_mask], y[train_mask], len(labels), alpha)
    scores = _predict_ridge_evidence_calibrator(x_sub[eval_mask], mean, std, weights)
    pred = np.argmax(scores, axis=1)
    summary = _stacked_prediction_summary(y[eval_mask], pred, labels)
    summary["objective"] = _stacked_evidence_objective(summary)
    confidence = np.sort(scores, axis=1)[:, -1] - np.sort(scores, axis=1)[:, -2]
    return summary, pred, confidence


def _stacked_evidence_objective(summary: dict) -> float:
    pc = summary["per_class"]
    return float(
        2.0 * summary["accuracy"]
        + 0.70 * pc.get("H0_sheet_only", 0.0)
        + 0.70 * pc.get("H1_sheet_via", 0.0)
        + 0.20 * pc.get("H2_sheet_return", 0.0)
        + 0.20 * pc.get("H3_sheet_artifact", 0.0)
        - 4.0 * summary.get("h0_false_any", 0.0)
    )


def _stacked_run_to_flat(run: dict, labels: List[str]) -> dict:
    flat = {
        "accuracy": float(run["accuracy"]),
        "h0_false_any": float(run["h0_false_any"]),
        "objective": float(run.get("objective", _stacked_evidence_objective(run))),
    }
    for label in labels:
        flat[label] = float(run["per_class"].get(label, float("nan")))
    return flat


def _summarize_stacked_runs(runs: list[dict], labels: List[str], alpha_label: str, alpha_counts: dict[float, int] | None = None) -> List[object]:
    def vals(key: str) -> list[float]:
        return [float(run[key]) for run in runs]

    acc_mean, acc_std = _mean_std(vals("accuracy"))
    h0_mean, _ = _mean_std(vals("H0_sheet_only"))
    h1_mean, _ = _mean_std(vals("H1_sheet_via"))
    h2_mean, _ = _mean_std(vals("H2_sheet_return"))
    h3_mean, _ = _mean_std(vals("H3_sheet_artifact"))
    h0_false_mean, _ = _mean_std(vals("h0_false_any"))
    obj_mean, obj_std = _mean_std(vals("objective"))
    counts = ""
    if alpha_counts:
        counts = ", ".join(f"{alpha:g}:{count}" for alpha, count in sorted(alpha_counts.items()) if count)
    status = "breakthrough_candidate"
    if h0_false_mean > 0.05:
        status = "h0_safety_watch"
    if h1_mean < 0.90:
        status = "h1_recall_limited"
    return [
        alpha_label,
        int(len(runs)),
        fmt_float(acc_mean),
        fmt_float(acc_std),
        fmt_float(h0_mean),
        fmt_float(h1_mean),
        fmt_float(h2_mean),
        fmt_float(h3_mean),
        fmt_float(h0_false_mean),
        fmt_float(obj_mean),
        fmt_float(obj_std),
        counts,
        status,
    ]


def _pypeec_repeated_stacked_runs(
    case_ids: list[str],
    x: np.ndarray,
    y: np.ndarray,
    labels: List[str],
    cfg: dict,
    alpha: float,
    feature_idx: np.ndarray | None = None,
) -> list[dict]:
    fake = [{"case_id": case_id, "true_hypothesis": labels[int(y_idx)]} for case_id, y_idx in zip(case_ids, y)]
    n_repeats = int(cfg.get("model_selection_calibration", {}).get("repeated_split_count", 25))
    runs: list[dict] = []
    for repeat_idx in range(n_repeats):
        split = _pypeec_repeated_split_map(fake, cfg, repeat_idx)
        train_mask = np.asarray([split.get(case_id) == "calibration" for case_id in case_ids], dtype=bool)
        eval_mask = ~train_mask
        summary, _, _ = _stacked_eval_run(x, y, train_mask, eval_mask, labels, alpha, feature_idx)
        runs.append(_stacked_run_to_flat(summary, labels))
    return runs


def _feature_indices_for_policy(feature_tags: list[dict], policy: str) -> np.ndarray:
    def keep(tag: dict) -> bool:
        basis = str(tag["basis"])
        evidence = str(tag["evidence"])
        kind = str(tag["kind"])
        if policy == "all_features":
            return True
        if policy == "scores_only":
            return kind == "score"
        if policy == "scores_plus_margin":
            return kind in {"score", "margin"}
        if policy == "scores_plus_residual":
            return kind in {"score", "residual"}
        if policy == "pred_one_hot_only":
            return kind == "pred_one_hot"
        if policy == "margin_residual_nbasis_only":
            return kind in {"margin", "residual", "n_basis"}
        if policy == "no_finite_width_sheet":
            return basis != "finite_width_sheet"
        if policy == "no_artifact_bank":
            return basis != "artifact_bank"
        if policy == "no_return_bank":
            return basis != "return_bank"
        if policy == "no_distributed_via":
            return basis != "distributed_via"
        if policy == "finite_width_h0_conservative_only":
            return basis == "finite_width_sheet" and evidence == "h0_conservative"
        if policy == "finite_width_all_evidence":
            return basis == "finite_width_sheet"
        if policy == "h0_conservative_all_basis":
            return evidence == "h0_conservative"
        return True

    idx = [i for i, tag in enumerate(feature_tags) if keep(tag)]
    if not idx:
        idx = list(range(len(feature_tags)))
    return np.asarray(idx, dtype=int)


def _pypeec_stacked_evidence_calibrator_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    """Learn a simple calibration/held-out evidence fusion model over basis banks.

    Unlike frozen model-bank tables, this is an explicit PyPEEC calibration
    experiment. It does not alter the frozen bridge claims. Its purpose is to
    test whether the existing evidence bank contains enough information if a
    held-out protocol is allowed.
    """
    case_ids, x, y = _stacked_evidence_feature_matrix(details, labels)
    if len(case_ids) == 0:
        return []
    cal_cfg = cfg.get("model_selection_calibration", {})
    n_repeats = int(cal_cfg.get("repeated_split_count", 25))
    alpha_grid = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 300.0, 1000.0]
    fake = [{"case_id": case_id, "true_hypothesis": labels[int(y_idx)]} for case_id, y_idx in zip(case_ids, y)]
    rows = []
    for alpha in alpha_grid:
        runs = []
        for repeat_idx in range(n_repeats):
            split = _pypeec_repeated_split_map(fake, cfg, repeat_idx)
            cal_mask = np.asarray([split.get(case_id) == "calibration" for case_id in case_ids], dtype=bool)
            held_mask = ~cal_mask
            mean, std, weights = _fit_ridge_evidence_calibrator(x[cal_mask], y[cal_mask], len(labels), alpha)
            scores = _predict_ridge_evidence_calibrator(x[held_mask], mean, std, weights)
            pred = np.argmax(scores, axis=1)
            summary = _stacked_prediction_summary(y[held_mask], pred, labels)
            run = {
                "accuracy": summary["accuracy"],
                "h0_false_any": summary["h0_false_any"],
                "objective": _stacked_evidence_objective(summary),
            }
            run.update(summary["per_class"])
            runs.append(run)
        rows.append(_summarize_stacked_runs(runs, labels, f"fixed_alpha={alpha:g}"))

    nested_runs = []
    alpha_counts = {alpha: 0 for alpha in alpha_grid}
    for repeat_idx in range(n_repeats):
        split = _pypeec_repeated_split_map(fake, cfg, repeat_idx)
        cal_ids = [case_id for case_id in case_ids if split.get(case_id) == "calibration"]
        held_mask = np.asarray([split.get(case_id) == "heldout" for case_id in case_ids], dtype=bool)
        inner_train_ids: set[str] = set()
        inner_val_ids: set[str] = set()
        for label in labels:
            ids = sorted([case_id for case_id in cal_ids if labels[int(y[case_ids.index(case_id)])] == label])
            for local_idx, case_id in enumerate(ids):
                if local_idx % 3 == repeat_idx % 3:
                    inner_val_ids.add(case_id)
                else:
                    inner_train_ids.add(case_id)
        train_mask = np.asarray([case_id in inner_train_ids for case_id in case_ids], dtype=bool)
        val_mask = np.asarray([case_id in inner_val_ids for case_id in case_ids], dtype=bool)
        best_alpha = alpha_grid[0]
        best_obj = -float("inf")
        for alpha in alpha_grid:
            mean, std, weights = _fit_ridge_evidence_calibrator(x[train_mask], y[train_mask], len(labels), alpha)
            scores = _predict_ridge_evidence_calibrator(x[val_mask], mean, std, weights)
            pred = np.argmax(scores, axis=1)
            summary = _stacked_prediction_summary(y[val_mask], pred, labels)
            obj = _stacked_evidence_objective(summary)
            if obj > best_obj:
                best_obj = obj
                best_alpha = alpha
        alpha_counts[best_alpha] += 1
        cal_mask = np.asarray([split.get(case_id) == "calibration" for case_id in case_ids], dtype=bool)
        mean, std, weights = _fit_ridge_evidence_calibrator(x[cal_mask], y[cal_mask], len(labels), best_alpha)
        scores = _predict_ridge_evidence_calibrator(x[held_mask], mean, std, weights)
        pred = np.argmax(scores, axis=1)
        summary = _stacked_prediction_summary(y[held_mask], pred, labels)
        run = {
            "accuracy": summary["accuracy"],
            "h0_false_any": summary["h0_false_any"],
            "objective": _stacked_evidence_objective(summary),
        }
        run.update(summary["per_class"])
        nested_runs.append(run)
    rows.append(_summarize_stacked_runs(nested_runs, labels, "inner_split_selected_alpha", alpha_counts))
    rows.sort(key=lambda r: (_to_float(r[10]), _to_float(r[3]), _to_float(r[5]), _to_float(r[6]), -_to_float(r[9])), reverse=True)
    return rows


def _pypeec_stacked_feature_ablation_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    case_ids, x, y, feature_tags, _ = _stacked_evidence_dataset(details, labels)
    policies = [
        "all_features",
        "scores_only",
        "scores_plus_margin",
        "scores_plus_residual",
        "pred_one_hot_only",
        "margin_residual_nbasis_only",
        "finite_width_h0_conservative_only",
        "finite_width_all_evidence",
        "h0_conservative_all_basis",
        "no_finite_width_sheet",
        "no_return_bank",
        "no_artifact_bank",
        "no_distributed_via",
    ]
    rows = []
    alpha = 100.0
    for policy in policies:
        idx = _feature_indices_for_policy(feature_tags, policy)
        runs = _pypeec_repeated_stacked_runs(case_ids, x, y, labels, cfg, alpha, idx)
        row = _summarize_stacked_runs(runs, labels, f"{policy}/fixed_alpha=100")
        rows.append([policy, int(len(idx)), *row[1:]])
    rows.sort(key=lambda r: (_to_float(r[10]), _to_float(r[3]), _to_float(r[5]), _to_float(r[6]), -_to_float(r[9])), reverse=True)
    return rows


def _variant_bucket(case_id: str, n_buckets: int = 5) -> str:
    if "__v" in case_id:
        try:
            idx = int(case_id.rsplit("__v", 1)[1].split("_", 1)[0])
            return f"variant_mod_{idx % n_buckets}"
        except ValueError:
            pass
    return "canonical"


def _pypeec_stacked_group_heldout_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    case_ids, x, y, _, meta = _stacked_evidence_dataset(details, labels)
    alpha = 100.0
    rows: list[list[object]] = []
    groups = {
        "variant_mod5": {case_id: _variant_bucket(case_id, 5) for case_id in case_ids},
        "case_family": {case_id: str(meta[case_id].get("family", "unknown")) for case_id in case_ids},
    }
    for group_policy, mapping in groups.items():
        fold_runs: list[dict] = []
        for group_name in sorted(set(mapping.values())):
            eval_mask = np.asarray([mapping[case_id] == group_name for case_id in case_ids], dtype=bool)
            if not np.any(eval_mask):
                continue
            train_mask = ~eval_mask
            train_labels = set(int(v) for v in y[train_mask])
            eval_labels = set(int(v) for v in y[eval_mask])
            if not eval_labels.issubset(train_labels):
                rows.append([
                    group_policy,
                    group_name,
                    int(np.sum(eval_mask)),
                    int(np.sum(train_mask)),
                    "nan",
                    "nan",
                    "nan",
                    "nan",
                    "nan",
                    "nan",
                    "skipped_train_missing_eval_class",
                ])
                continue
            summary, _, _ = _stacked_eval_run(x, y, train_mask, eval_mask, labels, alpha)
            flat = _stacked_run_to_flat(summary, labels)
            fold_runs.append(flat)
            rows.append([
                group_policy,
                group_name,
                int(np.sum(eval_mask)),
                int(np.sum(train_mask)),
                fmt_float(flat["accuracy"]),
                fmt_float(flat["H0_sheet_only"]),
                fmt_float(flat["H1_sheet_via"]),
                fmt_float(flat["H2_sheet_return"]),
                fmt_float(flat["H3_sheet_artifact"]),
                fmt_float(flat["h0_false_any"]),
                "evaluated",
            ])
        if fold_runs:
            acc_mean, acc_std = _mean_std([r["accuracy"] for r in fold_runs])
            h0_mean, _ = _mean_std([r["H0_sheet_only"] for r in fold_runs])
            h1_mean, _ = _mean_std([r["H1_sheet_via"] for r in fold_runs])
            h2_mean, _ = _mean_std([r["H2_sheet_return"] for r in fold_runs])
            h3_mean, _ = _mean_std([r["H3_sheet_artifact"] for r in fold_runs])
            h0_false_mean, _ = _mean_std([r["h0_false_any"] for r in fold_runs])
            rows.append([
                group_policy,
                "AGGREGATE_EVALUATED_FOLDS",
                int(sum(1 for v in set(mapping.values()))),
                int(len(fold_runs)),
                fmt_float(acc_mean),
                fmt_float(h0_mean),
                fmt_float(h1_mean),
                fmt_float(h2_mean),
                fmt_float(h3_mean),
                fmt_float(h0_false_mean),
                f"std_acc={fmt_float(acc_std)}",
            ])
    return rows


def _distance_gate_for_train_mask(
    x: np.ndarray,
    y: np.ndarray,
    train_mask: np.ndarray,
    labels: List[str],
    reject_target: float,
) -> tuple[float, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    inner_train_mask, inner_val_mask = _inner_train_val_masks(y, train_mask)
    if not np.any(inner_train_mask) or not np.any(inner_val_mask):
        model = _fit_feature_distance_ood_model(x[train_mask], y[train_mask], len(labels))
        return float("inf"), model
    inner_model = _fit_feature_distance_ood_model(x[inner_train_mask], y[inner_train_mask], len(labels))
    inner_signal = _feature_distance_ood_score(x[inner_val_mask], *inner_model)
    threshold = float(np.quantile(inner_signal, 1.0 - reject_target))
    full_model = _fit_feature_distance_ood_model(x[train_mask], y[train_mask], len(labels))
    return threshold, full_model


def _pypeec_stacked_group_distance_refusal_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    case_ids, x, y, _, meta = _stacked_evidence_dataset(details, labels)
    alpha = 100.0
    reject_target = float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20))
    rows: list[list[object]] = []
    groups = {
        "variant_mod5": {case_id: _variant_bucket(case_id, 5) for case_id in case_ids},
        "case_family": {case_id: str(meta[case_id].get("family", "unknown")) for case_id in case_ids},
    }
    for group_policy, mapping in groups.items():
        fold_runs: list[dict[str, float]] = []
        for group_name in sorted(set(mapping.values())):
            eval_mask = np.asarray([mapping[case_id] == group_name for case_id in case_ids], dtype=bool)
            if not np.any(eval_mask):
                continue
            train_mask = ~eval_mask
            train_labels = set(int(v) for v in y[train_mask])
            eval_labels = set(int(v) for v in y[eval_mask])
            mean, std, weights = _fit_ridge_evidence_calibrator(x[train_mask], y[train_mask], len(labels), alpha)
            scores = _predict_ridge_evidence_calibrator(x[eval_mask], mean, std, weights)
            pred = np.argmax(scores, axis=1)
            raw_summary = _stacked_prediction_summary(y[eval_mask], pred, labels)
            threshold, distance_model = _distance_gate_for_train_mask(x, y, train_mask, labels, reject_target)
            distance = _feature_distance_ood_score(x[eval_mask], *distance_model)
            accept = distance <= threshold
            y_eval = y[eval_mask]
            accepted_acc = float(np.mean(pred[accept] == y_eval[accept])) if np.any(accept) else float("nan")
            h0_mask = y_eval == labels.index("H0_sheet_only")
            h0_false_any = (
                float(np.mean((pred[h0_mask & accept] != labels.index("H0_sheet_only"))))
                if np.any(h0_mask & accept)
                else float("nan")
            )
            flat = {
                "raw_accuracy": raw_summary["accuracy"],
                "raw_h0_false_any": raw_summary["h0_false_any"],
                "reject_rate": float(1.0 - np.mean(accept)),
                "accepted_accuracy": accepted_acc,
                "accepted_risk": float(1.0 - accepted_acc) if np.isfinite(accepted_acc) else float("nan"),
                "accepted_h0_false_any": h0_false_any,
            }
            fold_runs.append(flat)
            if eval_labels.issubset(train_labels):
                status = "evaluated_in_class_family"
            elif not np.any(accept):
                status = "train_missing_eval_class_rejected"
            else:
                status = "train_missing_eval_class_some_accepted"
            rows.append([
                group_policy,
                group_name,
                int(np.sum(eval_mask)),
                int(np.sum(train_mask)),
                fmt_float(flat["raw_accuracy"]),
                fmt_float(flat["raw_h0_false_any"]),
                fmt_float(flat["reject_rate"]),
                fmt_float(flat["accepted_accuracy"]),
                fmt_float(flat["accepted_risk"]),
                fmt_float(flat["accepted_h0_false_any"]),
                status,
            ])
        if fold_runs:
            rows.append([
                group_policy,
                "AGGREGATE_EVALUATED_FOLDS",
                int(len(fold_runs)),
                int(len(fold_runs)),
                fmt_float(_mean_std([r["raw_accuracy"] for r in fold_runs])[0]),
                fmt_float(_mean_std([r["raw_h0_false_any"] for r in fold_runs])[0]),
                fmt_float(_mean_std([r["reject_rate"] for r in fold_runs])[0]),
                fmt_float(_mean_std([r["accepted_accuracy"] for r in fold_runs])[0]),
                fmt_float(_mean_std([r["accepted_risk"] for r in fold_runs])[0]),
                fmt_float(_mean_std([r["accepted_h0_false_any"] for r in fold_runs])[0]),
                "distance_refusal_aggregate",
            ])
    return rows


def _fewshot_indices_for_family(fam_indices: np.ndarray, y: np.ndarray, k: int) -> list[int]:
    if k <= 0:
        return []
    by_label: dict[int, list[int]] = defaultdict(list)
    for idx in sorted(int(v) for v in fam_indices):
        by_label[int(y[idx])].append(idx)
    selected: list[int] = []
    cursor = 0
    while len(selected) < min(k, max(len(fam_indices) - 1, 0)):
        progressed = False
        for label in sorted(by_label):
            ids = by_label[label]
            if cursor < len(ids):
                selected.append(ids[cursor])
                progressed = True
                if len(selected) >= min(k, max(len(fam_indices) - 1, 0)):
                    break
        if not progressed:
            break
        cursor += 1
    return selected


def _pypeec_family_fewshot_adaptation_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    case_ids, x, y, _, meta = _stacked_evidence_dataset(details, labels)
    alpha = 100.0
    reject_target = float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20))
    shot_counts = [0, 2, 5, 10]
    family_by_case = {case_id: str(meta[case_id].get("family", "unknown")) for case_id in case_ids}
    rows: list[list[object]] = []
    aggregate: dict[int, list[dict[str, float]]] = {k: [] for k in shot_counts}
    for family in sorted(set(family_by_case.values())):
        fam_mask = np.asarray([family_by_case[case_id] == family for case_id in case_ids], dtype=bool)
        fam_indices = np.flatnonzero(fam_mask)
        if len(fam_indices) <= 1:
            continue
        for shots in shot_counts:
            shot_indices = _fewshot_indices_for_family(fam_indices, y, shots)
            shot_mask = np.zeros(len(case_ids), dtype=bool)
            shot_mask[shot_indices] = True
            eval_mask = fam_mask & ~shot_mask
            if not np.any(eval_mask):
                continue
            train_mask = (~fam_mask) | shot_mask
            mean, std, weights = _fit_ridge_evidence_calibrator(x[train_mask], y[train_mask], len(labels), alpha)
            scores = _predict_ridge_evidence_calibrator(x[eval_mask], mean, std, weights)
            pred = np.argmax(scores, axis=1)
            y_eval = y[eval_mask]
            raw_summary = _stacked_prediction_summary(y_eval, pred, labels)
            threshold, dist_model = _distance_gate_for_train_mask(x, y, train_mask, labels, reject_target)
            distance = _feature_distance_ood_score(x[eval_mask], *dist_model)
            accept = distance <= threshold
            accepted_acc = float(np.mean(pred[accept] == y_eval[accept])) if np.any(accept) else float("nan")
            h0_mask = y_eval == labels.index("H0_sheet_only")
            accepted_h0_false = (
                float(np.mean(pred[h0_mask & accept] != labels.index("H0_sheet_only")))
                if np.any(h0_mask & accept)
                else float("nan")
            )
            flat = {
                "raw_accuracy": raw_summary["accuracy"],
                "reject_rate": float(1.0 - np.mean(accept)),
                "accepted_accuracy": accepted_acc,
                "accepted_risk": float(1.0 - accepted_acc) if np.isfinite(accepted_acc) else float("nan"),
                "accepted_h0_false_any": accepted_h0_false,
            }
            aggregate[shots].append(flat)
            if shots == 0:
                status = "zero_shot_family_refusal_baseline"
            elif np.isfinite(accepted_acc) and accepted_acc >= 0.95 and flat["reject_rate"] <= 0.50:
                status = "fewshot_adaptation_candidate"
            elif flat["reject_rate"] > 0.80:
                status = "still_mostly_refusal"
            else:
                status = "diagnostic_only"
            rows.append([
                family,
                int(shots),
                int(np.sum(train_mask)),
                int(np.sum(eval_mask)),
                fmt_float(raw_summary["accuracy"]),
                fmt_float(raw_summary["h0_false_any"]),
                fmt_float(flat["reject_rate"]),
                fmt_float(accepted_acc),
                fmt_float(flat["accepted_risk"]),
                fmt_float(accepted_h0_false),
                status,
            ])
    for shots in shot_counts:
        runs = aggregate[shots]
        if not runs:
            continue
        rows.append([
            "AGGREGATE_FAMILIES",
            int(shots),
            int(len(runs)),
            int(len(runs)),
            fmt_float(_mean_std([r["raw_accuracy"] for r in runs])[0]),
            "nan",
            fmt_float(_mean_std([r["reject_rate"] for r in runs])[0]),
            fmt_float(_mean_std([r["accepted_accuracy"] for r in runs])[0]),
            fmt_float(_mean_std([r["accepted_risk"] for r in runs])[0]),
            fmt_float(_mean_std([r["accepted_h0_false_any"] for r in runs])[0]),
            "fewshot_aggregate",
        ])
    return rows


def _stacked_evidence_details_for_records(
    records: list,
    obs_grid: np.ndarray,
    cfg: dict,
    complexity_penalty: float,
    labels: List[str],
    field_key: str,
) -> list[dict]:
    evidence_modes = list(cfg.get("model_evidence", {}).get("modes", ["default_score"]))
    basis_modes = ["base"] + list(cfg.get("pypeec_aware_basis", {}).get("modes", []))
    details: list[dict] = []
    for basis_mode in basis_modes:
        variant = records if basis_mode == "base" else [augment_record_for_pypeec_basis(rec, cfg, basis_mode) for rec in records]
        rows = evaluate_records(variant, obs_grid, cfg, complexity_penalty=complexity_penalty)
        for evidence_mode in evidence_modes:
            details.extend(_evidence_detail_rows(field_key, basis_mode, evidence_mode, rows, labels, cfg))
    return details


def _fit_stacked_on_split(
    case_ids: list[str],
    x: np.ndarray,
    y: np.ndarray,
    split: dict[str, str],
    labels: List[str],
    alpha: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    train_mask = np.asarray([split.get(case_id) == "calibration" for case_id in case_ids], dtype=bool)
    mean, std, weights = _fit_ridge_evidence_calibrator(x[train_mask], y[train_mask], len(labels), alpha)
    return train_mask, mean, std, weights


def _calibration_confidence_threshold(
    x: np.ndarray,
    y: np.ndarray,
    train_mask: np.ndarray,
    labels: List[str],
    alpha: float,
    reject_target: float,
) -> float:
    train_indices = np.flatnonzero(train_mask)
    inner_train: list[int] = []
    inner_val: list[int] = []
    for label_idx in range(len(labels)):
        ids = train_indices[y[train_indices] == label_idx]
        for j, idx in enumerate(ids):
            if j % 3 == 0:
                inner_val.append(int(idx))
            else:
                inner_train.append(int(idx))
    if not inner_val or not inner_train:
        return -float("inf")
    inner_train_mask = np.zeros(len(y), dtype=bool)
    inner_val_mask = np.zeros(len(y), dtype=bool)
    inner_train_mask[inner_train] = True
    inner_val_mask[inner_val] = True
    mean, std, weights = _fit_ridge_evidence_calibrator(x[inner_train_mask], y[inner_train_mask], len(labels), alpha)
    scores = _predict_ridge_evidence_calibrator(x[inner_val_mask], mean, std, weights)
    conf = np.sort(scores, axis=1)[:, -1] - np.sort(scores, axis=1)[:, -2]
    return float(np.quantile(conf, max(0.0, min(0.95, float(reject_target)))))


def _inner_train_val_masks(y: np.ndarray, train_mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    train_indices = np.flatnonzero(train_mask)
    inner_train: list[int] = []
    inner_val: list[int] = []
    for label_idx in sorted(set(int(v) for v in y[train_indices])):
        ids = train_indices[y[train_indices] == label_idx]
        for j, idx in enumerate(ids):
            if j % 3 == 0:
                inner_val.append(int(idx))
            else:
                inner_train.append(int(idx))
    inner_train_mask = np.zeros(len(y), dtype=bool)
    inner_val_mask = np.zeros(len(y), dtype=bool)
    inner_train_mask[inner_train] = True
    inner_val_mask[inner_val] = True
    return inner_train_mask, inner_val_mask


def _fit_feature_distance_ood_model(
    x_train: np.ndarray,
    y_train: np.ndarray,
    n_classes: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Fit a class-conditional feature-distance model over stacked evidence.

    This is intentionally simple: it measures whether a new stacked-evidence
    vector looks close to any calibrated in-library class. It is not a new
    hypothesis classifier; it is an unknown/out-of-library rejection signal.
    """
    mean = np.mean(x_train, axis=0)
    std = np.std(x_train, axis=0) + 1e-6
    z = (x_train - mean) / std
    global_var = np.var(z, axis=0) + 1e-2
    centroids = []
    invvars = []
    for label_idx in range(n_classes):
        class_z = z[y_train == label_idx]
        if len(class_z) == 0:
            centroids.append(np.mean(z, axis=0))
            invvars.append(1.0 / global_var)
            continue
        centroids.append(np.mean(class_z, axis=0))
        class_var = np.var(class_z, axis=0) + 1e-2
        invvars.append(1.0 / (0.5 * class_var + 0.5 * global_var))
    return mean, std, np.asarray(centroids), np.asarray(invvars)


def _feature_distance_ood_score(
    x_eval: np.ndarray,
    mean: np.ndarray,
    std: np.ndarray,
    centroids: np.ndarray,
    invvars: np.ndarray,
) -> np.ndarray:
    z = (x_eval - mean) / std
    distances = []
    for centroid, invvar in zip(centroids, invvars):
        distances.append(np.mean(((z - centroid) ** 2) * invvar, axis=1))
    return np.min(np.asarray(distances), axis=0)


def _confidence_unknown_score(scores: np.ndarray) -> np.ndarray:
    sorted_scores = np.sort(scores, axis=1)
    confidence = sorted_scores[:, -1] - sorted_scores[:, -2]
    return -confidence


def _safe_standardized(values: np.ndarray, reference: np.ndarray) -> np.ndarray:
    return (values - float(np.mean(reference))) / (float(np.std(reference)) + 1e-9)


def _pypeec_stacked_selective_risk_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    case_ids, x, y, _, _ = _stacked_evidence_dataset(details, labels)
    fake = [{"case_id": case_id, "true_hypothesis": labels[int(y_idx)]} for case_id, y_idx in zip(case_ids, y)]
    n_repeats = int(cfg.get("model_selection_calibration", {}).get("repeated_split_count", 25))
    alpha = 100.0
    coverages = [0.20, 0.50, 0.80, 1.00]
    buckets = {cov: [] for cov in coverages}
    for repeat_idx in range(n_repeats):
        split = _pypeec_repeated_split_map(fake, cfg, repeat_idx)
        train_mask, mean, std, weights = _fit_stacked_on_split(case_ids, x, y, split, labels, alpha)
        eval_mask = ~train_mask
        scores = _predict_ridge_evidence_calibrator(x[eval_mask], mean, std, weights)
        pred = np.argmax(scores, axis=1)
        conf = np.sort(scores, axis=1)[:, -1] - np.sort(scores, axis=1)[:, -2]
        y_eval = y[eval_mask]
        order = np.argsort(-conf)
        for cov in coverages:
            k = max(1, int(round(float(cov) * len(order))))
            idx = order[:k]
            summary = _stacked_prediction_summary(y_eval[idx], pred[idx], labels)
            flat = _stacked_run_to_flat(summary, labels)
            h1_total = max(int(np.sum(y_eval == labels.index("H1_sheet_via"))), 1)
            h1_accepted = int(np.sum(y_eval[idx] == labels.index("H1_sheet_via")))
            flat["h1_acceptance"] = float(h1_accepted / h1_total)
            flat["coverage"] = float(k / max(len(order), 1))
            buckets[cov].append(flat)
    rows = []
    for cov in coverages:
        runs = buckets[cov]
        rows.append([
            "fixed_alpha=100_confidence_margin",
            fmt_float(cov),
            int(n_repeats),
            fmt_float(_mean_std([r["accuracy"] for r in runs])[0]),
            fmt_float(_mean_std([r["H0_sheet_only"] for r in runs])[0]),
            fmt_float(_mean_std([r["H1_sheet_via"] for r in runs])[0]),
            fmt_float(_mean_std([r["h0_false_any"] for r in runs])[0]),
            fmt_float(_mean_std([r["h1_acceptance"] for r in runs])[0]),
            fmt_float(1.0 - _mean_std([r["coverage"] for r in runs])[0]),
        ])
    return rows


def _pypeec_stacked_unknown_safety_rows(
    pypeec_details: List[dict],
    hidden_details: List[dict],
    labels: List[str],
    cfg: dict,
    hidden_field_key: str = "hidden_mechanism",
) -> List[List[object]]:
    case_ids, x, y, _, _ = _stacked_evidence_dataset(pypeec_details, labels)
    hidden_ids, x_hidden, y_hidden, _, _ = _stacked_evidence_dataset(hidden_details, labels, field_key=hidden_field_key)
    fake = [{"case_id": case_id, "true_hypothesis": labels[int(y_idx)]} for case_id, y_idx in zip(case_ids, y)]
    n_repeats = int(cfg.get("model_selection_calibration", {}).get("repeated_split_count", 25))
    alpha = 100.0
    reject_target = float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20))
    policies = ["confidence_margin", "feature_distance", "confidence_plus_distance"]
    rows_by_policy: dict[str, list[dict[str, float]]] = {policy: [] for policy in policies}
    for repeat_idx in range(n_repeats):
        split = _pypeec_repeated_split_map(fake, cfg, repeat_idx)
        train_mask, mean, std, weights = _fit_stacked_on_split(case_ids, x, y, split, labels, alpha)
        inner_train_mask, inner_val_mask = _inner_train_val_masks(y, train_mask)
        if not np.any(inner_train_mask) or not np.any(inner_val_mask):
            continue

        inner_mean, inner_std, inner_weights = _fit_ridge_evidence_calibrator(
            x[inner_train_mask], y[inner_train_mask], len(labels), alpha
        )
        inner_scores = _predict_ridge_evidence_calibrator(x[inner_val_mask], inner_mean, inner_std, inner_weights)
        inner_conf_signal = _confidence_unknown_score(inner_scores)
        inner_dist_model = _fit_feature_distance_ood_model(x[inner_train_mask], y[inner_train_mask], len(labels))
        inner_dist_signal = _feature_distance_ood_score(x[inner_val_mask], *inner_dist_model)
        inner_combined_signal = _safe_standardized(inner_dist_signal, inner_dist_signal) + _safe_standardized(
            inner_conf_signal, inner_conf_signal
        )
        thresholds = {
            "confidence_margin": float(np.quantile(inner_conf_signal, 1.0 - reject_target)),
            "feature_distance": float(np.quantile(inner_dist_signal, 1.0 - reject_target)),
            "confidence_plus_distance": float(np.quantile(inner_combined_signal, 1.0 - reject_target)),
        }

        eval_mask = ~train_mask
        scores_eval = _predict_ridge_evidence_calibrator(x[eval_mask], mean, std, weights)
        pred_eval = np.argmax(scores_eval, axis=1)
        scores_hidden = _predict_ridge_evidence_calibrator(x_hidden, mean, std, weights)
        pred_hidden = np.argmax(scores_hidden, axis=1)

        full_dist_model = _fit_feature_distance_ood_model(x[train_mask], y[train_mask], len(labels))
        eval_conf_signal = _confidence_unknown_score(scores_eval)
        hidden_conf_signal = _confidence_unknown_score(scores_hidden)
        eval_dist_signal = _feature_distance_ood_score(x[eval_mask], *full_dist_model)
        hidden_dist_signal = _feature_distance_ood_score(x_hidden, *full_dist_model)
        eval_signals = {
            "confidence_margin": eval_conf_signal,
            "feature_distance": eval_dist_signal,
            "confidence_plus_distance": _safe_standardized(eval_dist_signal, inner_dist_signal)
            + _safe_standardized(eval_conf_signal, inner_conf_signal),
        }
        hidden_signals = {
            "confidence_margin": hidden_conf_signal,
            "feature_distance": hidden_dist_signal,
            "confidence_plus_distance": _safe_standardized(hidden_dist_signal, inner_dist_signal)
            + _safe_standardized(hidden_conf_signal, inner_conf_signal),
        }
        y_eval = y[eval_mask]
        for policy in policies:
            accept_eval = eval_signals[policy] <= thresholds[policy]
            accept_hidden = hidden_signals[policy] <= thresholds[policy]
            clean_acc = (
                float(np.mean(pred_eval[accept_eval] == y_eval[accept_eval]))
                if np.any(accept_eval)
                else float("nan")
            )
            hidden_acc = (
                float(np.mean(pred_hidden[accept_hidden] == y_hidden[accept_hidden]))
                if np.any(accept_hidden)
                else float("nan")
            )
            rows_by_policy[policy].append({
                "clean_reject": float(1.0 - np.mean(accept_eval)),
                "clean_accepted_acc": clean_acc,
                "hidden_reject": float(1.0 - np.mean(accept_hidden)),
                "hidden_accepted_acc": hidden_acc,
                "hidden_accepted_risk": float(1.0 - hidden_acc) if np.isfinite(hidden_acc) else float("nan"),
                "hidden_accept": float(np.mean(accept_hidden)),
            })
    rows = []
    for policy in policies:
        rows_accum = rows_by_policy[policy]
        hidden_accept_mean = _mean_std([r["hidden_accept"] for r in rows_accum])[0]
        hidden_risk_mean = _mean_std([r["hidden_accepted_risk"] for r in rows_accum])[0]
        if hidden_accept_mean <= 0.05 and (not np.isfinite(hidden_risk_mean) or hidden_risk_mean <= 0.20):
            status = "low_hidden_exposure_candidate"
        elif hidden_accept_mean <= 0.10:
            status = "strong_hidden_rejection_but_risk_tail"
        elif np.isfinite(hidden_risk_mean) and hidden_risk_mean <= 0.20:
            status = "low_accepted_hidden_risk_candidate"
        else:
            status = "diagnostic_only"
        rows.append([
            f"fixed_alpha=100_inner_{policy}",
            fmt_float(reject_target),
            int(len(rows_accum)),
            fmt_float(_mean_std([r["clean_reject"] for r in rows_accum])[0]),
            fmt_float(_mean_std([r["clean_accepted_acc"] for r in rows_accum])[0]),
            fmt_float(_mean_std([r["hidden_reject"] for r in rows_accum])[0]),
            fmt_float(hidden_accept_mean),
            fmt_float(_mean_std([r["hidden_accepted_acc"] for r in rows_accum])[0]),
            fmt_float(hidden_risk_mean),
            status,
        ])
    rows.sort(key=lambda r: (_to_float(r[5]), -_to_float(r[3]), -_to_float(r[8]) if np.isfinite(_to_float(r[8])) else 0.0), reverse=True)
    return rows


def _stacked_evidence_space_diagnostic_rows(
    pypeec_details: List[dict],
    hidden_details: List[dict],
    near_hidden_details: List[dict],
    labels: List[str],
    outputs_dir: Path,
) -> List[List[object]]:
    import matplotlib.pyplot as plt

    p_ids, x_p, y_p, _, _ = _stacked_evidence_dataset(pypeec_details, labels)
    h_ids, x_h, y_h, _, _ = _stacked_evidence_dataset(hidden_details, labels, field_key="hidden_mechanism")
    n_ids, x_n, y_n, _, _ = _stacked_evidence_dataset(near_hidden_details, labels, field_key="near_boundary_hidden")
    mean = np.mean(x_p, axis=0)
    std = np.std(x_p, axis=0) + 1e-6
    z_p = (x_p - mean) / std
    z_h = (x_h - mean) / std
    z_n = (x_n - mean) / std
    z_center = z_p - np.mean(z_p, axis=0)
    _, _, vt = np.linalg.svd(z_center, full_matrices=False)
    basis = vt[:2].T
    proj_p = z_center @ basis
    proj_h = (z_h - np.mean(z_p, axis=0)) @ basis
    proj_n = (z_n - np.mean(z_p, axis=0)) @ basis

    dist_model = _fit_feature_distance_ood_model(x_p, y_p, len(labels))
    dist_p = _feature_distance_ood_score(x_p, *dist_model)
    dist_h = _feature_distance_ood_score(x_h, *dist_model)
    dist_n = _feature_distance_ood_score(x_n, *dist_model)

    rows = []
    for name, ids, y_arr, proj, dist in [
        ("in_library_pypeec", p_ids, y_p, proj_p, dist_p),
        ("base_hidden", h_ids, y_h, proj_h, dist_h),
        ("near_boundary_hidden", n_ids, y_n, proj_n, dist_n),
    ]:
        rows.append([
            name,
            int(len(ids)),
            fmt_float(float(np.median(dist))),
            fmt_float(float(np.quantile(dist, 0.90))),
            fmt_float(float(np.mean(proj[:, 0]))),
            fmt_float(float(np.std(proj[:, 0]))),
            fmt_float(float(np.mean(proj[:, 1]))),
            fmt_float(float(np.std(proj[:, 1]))),
            ", ".join(f"{labels[i]}:{int(np.sum(y_arr == i))}" for i in range(len(labels))),
        ])

    fig, ax = plt.subplots(figsize=(7.0, 5.4), dpi=160)
    colors = ["#2b6cb0", "#2f855a", "#b7791f", "#805ad5"]
    for label_idx, label in enumerate(labels):
        mask = y_p == label_idx
        ax.scatter(proj_p[mask, 0], proj_p[mask, 1], s=10, alpha=0.55, label=f"in-library {label}", color=colors[label_idx])
    ax.scatter(proj_h[:, 0], proj_h[:, 1], s=18, alpha=0.75, marker="x", color="#c53030", label="base hidden")
    ax.scatter(proj_n[:, 0], proj_n[:, 1], s=18, alpha=0.75, marker="+", color="#dd6b20", label="near-boundary hidden")
    ax.set_xlabel("PC1 of stacked evidence")
    ax.set_ylabel("PC2 of stacked evidence")
    ax.set_title("Exp08 stacked-evidence space")
    ax.legend(loc="best", fontsize=6, frameon=False, ncol=1)
    fig.tight_layout()
    fig.savefig(outputs_dir / "stacked_evidence_space_pca.png")
    plt.close(fig)
    return rows


def _severity_from_family(family: str) -> str:
    parts = str(family).split("_")
    if len(parts) >= 2 and parts[0] == "severity":
        return parts[1]
    return "unknown"


def _stacked_evidence_near_hidden_severity_rows(
    pypeec_details: List[dict],
    severity_details: List[dict],
    labels: List[str],
    cfg: dict,
) -> List[List[object]]:
    case_ids, x, y, _, _ = _stacked_evidence_dataset(pypeec_details, labels)
    h_ids, x_h, y_h, _, h_meta = _stacked_evidence_dataset(severity_details, labels, field_key="near_boundary_hidden_severity")
    severity_by_case = {case_id: _severity_from_family(str(h_meta[case_id].get("family", "unknown"))) for case_id in h_ids}
    fake = [{"case_id": case_id, "true_hypothesis": labels[int(y_idx)]} for case_id, y_idx in zip(case_ids, y)]
    n_repeats = int(cfg.get("model_selection_calibration", {}).get("repeated_split_count", 25))
    alpha = 100.0
    reject_target = float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20))
    policies = ["feature_distance", "confidence_margin"]
    buckets: dict[tuple[str, str], list[dict[str, float]]] = defaultdict(list)
    for repeat_idx in range(n_repeats):
        split = _pypeec_repeated_split_map(fake, cfg, repeat_idx)
        train_mask, mean, std, weights = _fit_stacked_on_split(case_ids, x, y, split, labels, alpha)
        inner_train_mask, inner_val_mask = _inner_train_val_masks(y, train_mask)
        if not np.any(inner_train_mask) or not np.any(inner_val_mask):
            continue
        inner_mean, inner_std, inner_weights = _fit_ridge_evidence_calibrator(
            x[inner_train_mask], y[inner_train_mask], len(labels), alpha
        )
        inner_scores = _predict_ridge_evidence_calibrator(x[inner_val_mask], inner_mean, inner_std, inner_weights)
        inner_conf = _confidence_unknown_score(inner_scores)
        inner_dist_model = _fit_feature_distance_ood_model(x[inner_train_mask], y[inner_train_mask], len(labels))
        inner_dist = _feature_distance_ood_score(x[inner_val_mask], *inner_dist_model)
        thresholds = {
            "feature_distance": float(np.quantile(inner_dist, 1.0 - reject_target)),
            "confidence_margin": float(np.quantile(inner_conf, 1.0 - reject_target)),
        }
        eval_mask = ~train_mask
        scores_eval = _predict_ridge_evidence_calibrator(x[eval_mask], mean, std, weights)
        pred_eval = np.argmax(scores_eval, axis=1)
        eval_dist_model = _fit_feature_distance_ood_model(x[train_mask], y[train_mask], len(labels))
        eval_dist = _feature_distance_ood_score(x[eval_mask], *eval_dist_model)
        eval_conf = _confidence_unknown_score(scores_eval)
        clean_signals = {"feature_distance": eval_dist, "confidence_margin": eval_conf}
        scores_h = _predict_ridge_evidence_calibrator(x_h, mean, std, weights)
        pred_h = np.argmax(scores_h, axis=1)
        hidden_signals = {
            "feature_distance": _feature_distance_ood_score(x_h, *eval_dist_model),
            "confidence_margin": _confidence_unknown_score(scores_h),
        }
        for policy in policies:
            clean_accept = clean_signals[policy] <= thresholds[policy]
            clean_acc = float(np.mean(pred_eval[clean_accept] == y[eval_mask][clean_accept])) if np.any(clean_accept) else float("nan")
            for severity in sorted(set(severity_by_case.values())):
                sev_mask = np.asarray([severity_by_case[case_id] == severity for case_id in h_ids], dtype=bool)
                accept_h = hidden_signals[policy][sev_mask] <= thresholds[policy]
                y_sev = y_h[sev_mask]
                pred_sev = pred_h[sev_mask]
                acc = float(np.mean(pred_sev[accept_h] == y_sev[accept_h])) if np.any(accept_h) else float("nan")
                buckets[(policy, severity)].append({
                    "clean_reject": float(1.0 - np.mean(clean_accept)),
                    "clean_acc": clean_acc,
                    "hidden_reject": float(1.0 - np.mean(accept_h)),
                    "hidden_accept": float(np.mean(accept_h)),
                    "hidden_acc": acc,
                    "hidden_risk": float(1.0 - acc) if np.isfinite(acc) else float("nan"),
                    "median_signal": float(np.median(hidden_signals[policy][sev_mask])),
                })
    rows = []
    for (policy, severity), runs in sorted(buckets.items(), key=lambda item: (item[0][0], float(item[0][1]))):
        rows.append([
            policy,
            severity,
            int(n_repeats),
            fmt_float(_mean_std([r["clean_reject"] for r in runs])[0]),
            fmt_float(_mean_std([r["clean_acc"] for r in runs])[0]),
            fmt_float(_mean_std([r["hidden_reject"] for r in runs])[0]),
            fmt_float(_mean_std([r["hidden_accept"] for r in runs])[0]),
            fmt_float(_mean_std([r["hidden_acc"] for r in runs])[0]),
            fmt_float(_mean_std([r["hidden_risk"] for r in runs])[0]),
            fmt_float(_mean_std([r["median_signal"] for r in runs])[0]),
        ])
    return rows


def _near_hidden_accepted_case_rows(
    pypeec_details: List[dict],
    near_hidden_details: List[dict],
    labels: List[str],
    cfg: dict,
) -> List[List[object]]:
    case_ids, x, y, _, _ = _stacked_evidence_dataset(pypeec_details, labels)
    h_ids, x_h, y_h, _, h_meta = _stacked_evidence_dataset(near_hidden_details, labels, field_key="near_boundary_hidden")
    fake = [{"case_id": case_id, "true_hypothesis": labels[int(y_idx)]} for case_id, y_idx in zip(case_ids, y)]
    split = _pypeec_repeated_split_map(fake, cfg, 0)
    train_mask, mean, std, weights = _fit_stacked_on_split(case_ids, x, y, split, labels, 100.0)
    threshold, dist_model = _distance_gate_for_train_mask(
        x,
        y,
        train_mask,
        labels,
        float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20)),
    )
    scores = _predict_ridge_evidence_calibrator(x_h, mean, std, weights)
    pred = np.argmax(scores, axis=1)
    dist = _feature_distance_ood_score(x_h, *dist_model)
    conf = np.sort(scores, axis=1)[:, -1] - np.sort(scores, axis=1)[:, -2]
    accept = dist <= threshold
    rows = []
    order = np.argsort(dist)
    for idx in order:
        if not accept[idx]:
            continue
        case_id = h_ids[int(idx)]
        true_label = labels[int(y_h[idx])]
        pred_label = labels[int(pred[idx])]
        family = str(h_meta[case_id].get("family", "unknown"))
        if "wrong_layer" in family or "shifted" in family:
            mechanism_status = "primary_label_correct_but_geometry_hidden" if pred_label == true_label else "primary_label_wrong"
        elif "shadow" in family:
            mechanism_status = "primary_label_correct_but_artifact_unexplained" if pred_label == true_label else "primary_label_wrong"
        else:
            mechanism_status = "primary_label_only"
        rows.append([
            case_id,
            family,
            true_label,
            pred_label,
            fmt_float(float(dist[idx])),
            fmt_float(float(threshold)),
            fmt_float(float(conf[idx])),
            mechanism_status,
        ])
    return rows[:30]


def _pypeec_stacked_external_stress_rows(
    pypeec_details: List[dict],
    external_detail_sets: dict[str, List[dict]],
    labels: List[str],
    cfg: dict,
) -> List[List[object]]:
    case_ids, x, y, _, _ = _stacked_evidence_dataset(pypeec_details, labels)
    fake = [{"case_id": case_id, "true_hypothesis": labels[int(y_idx)]} for case_id, y_idx in zip(case_ids, y)]
    n_repeats = int(cfg.get("model_selection_calibration", {}).get("repeated_split_count", 25))
    alpha = 100.0
    rows = []
    for name, ext_details in external_detail_sets.items():
        ext_ids, x_ext, y_ext, _, _ = _stacked_evidence_dataset(ext_details, labels, field_key=name)
        ext_id_index = {case_id: idx for idx, case_id in enumerate(ext_ids)}
        runs = []
        for repeat_idx in range(n_repeats):
            split = _pypeec_repeated_split_map(fake, cfg, repeat_idx)
            train_mask, mean, std, weights = _fit_stacked_on_split(case_ids, x, y, split, labels, alpha)
            held_ids = [case_id for case_id in case_ids if split.get(case_id) == "heldout" and case_id in ext_id_index]
            if held_ids:
                ext_mask = np.asarray([case_id in set(held_ids) for case_id in ext_ids], dtype=bool)
            else:
                ext_mask = np.ones(len(ext_ids), dtype=bool)
            scores = _predict_ridge_evidence_calibrator(x_ext[ext_mask], mean, std, weights)
            pred = np.argmax(scores, axis=1)
            summary = _stacked_prediction_summary(y_ext[ext_mask], pred, labels)
            runs.append(_stacked_run_to_flat(summary, labels))
        rows.append([
            name,
            int(n_repeats),
            int(len(ext_ids)),
            fmt_float(_mean_std([r["accuracy"] for r in runs])[0]),
            fmt_float(_mean_std([r["H0_sheet_only"] for r in runs])[0]),
            fmt_float(_mean_std([r["H1_sheet_via"] for r in runs])[0]),
            fmt_float(_mean_std([r["H2_sheet_return"] for r in runs])[0]),
            fmt_float(_mean_std([r["H3_sheet_artifact"] for r in runs])[0]),
            fmt_float(_mean_std([r["h0_false_any"] for r in runs])[0]),
        ])
    return rows


def _pypeec_split_table_rows(details: List[dict], cfg: dict) -> List[List[object]]:
    split = _pypeec_split_map(details, cfg)
    rows = []
    for true_h in sorted({d["true_hypothesis"] for d in details}):
        ids = sorted({d["case_id"] for d in details if d["true_hypothesis"] == true_h})
        rows.append([
            true_h,
            len(ids),
            sum(1 for case_id in ids if split.get(case_id) == "calibration"),
            sum(1 for case_id in ids if split.get(case_id) == "heldout"),
        ])
    return rows


def _pypeec_distribution_gap_rows(details: List[dict], labels: List[str], cfg: dict) -> List[List[object]]:
    targets = cfg.get("model_selection_calibration", {}).get("target_cases_per_hypothesis", {})
    case_info: dict[str, dict] = {}
    for d in details:
        case_info.setdefault(d["case_id"], {"true_hypothesis": d["true_hypothesis"], "families": set()})
        case_info[d["case_id"]]["families"].add(str(d.get("family", "unknown")))
    rows = []
    for true_h in labels:
        ids = sorted([case_id for case_id, info in case_info.items() if info["true_hypothesis"] == true_h])
        families = sorted({fam for case_id in ids for fam in case_info[case_id]["families"]})
        target = int(targets.get(true_h, 100))
        gap = max(0, target - len(ids))
        if len(ids) == 0:
            status = "absent_in_current_pypeec_bridge"
        elif gap > 0:
            status = "needs_exp07_distribution_expansion"
        else:
            status = "meets_target"
        rows.append([
            true_h,
            int(len(ids)),
            int(target),
            int(gap),
            ", ".join(families[:8]) + (" ..." if len(families) > 8 else ""),
            status,
        ])
    return rows


def _model_bank_allowed_basis_rows() -> List[List[object]]:
    return [
        [
            "H0_sheet_only",
            "sheet + finite_width_sheet",
            "return_bank / artifact_bank / distributed_via",
            "Protect no-via against residual-only over-explanation.",
        ],
        [
            "H1_sheet_via",
            "sheet + finite_width_sheet + compact/distributed via",
            "artifact_bank unless explicitly diagnosed",
            "Keep true-via evidence separate from bend/corner artifacts.",
        ],
        [
            "H2_sheet_return",
            "sheet + finite_width_sheet + return_bank",
            "distributed_via as a first explanation",
            "Return-current mismatch is a physical nuisance, not a via by default.",
        ],
        [
            "H3_sheet_artifact",
            "sheet + finite_width_sheet + artifact_bank",
            "return_bank unless route metadata supports it",
            "Bend/corner residuals should compete with via, not silently become via.",
        ],
        [
            "unknown/refusal",
            "all evidence families as diagnostic scores",
            "label-changing calibration on PyPEEC frozen rows",
            "Reject or defer when model evidence is not identifiable.",
        ],
    ]


def _unknown_safety_benchmark_rows(
    clean_rows: List[dict],
    hidden_rows: List[dict],
    clean_marg_rows: List[dict],
    hidden_marg_rows: List[dict],
    cfg: dict,
) -> List[List[object]]:
    ablation = _unknown_detector_ablation_rows(clean_rows, hidden_rows, clean_marg_rows, hidden_marg_rows, cfg)
    target = float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20))
    rows_out: List[List[object]] = []
    for row in ablation:
        clean_false = _to_float(row[2])
        hidden_reject = _to_float(row[3])
        accepted_clean_acc = _to_float(row[6])
        accepted_hidden_acc = _to_float(row[7])
        if clean_false > target + 1e-9:
            status = "fails_clean_reject_budget"
        elif hidden_reject >= 0.60 and accepted_hidden_acc >= 0.70:
            status = "usable_screen"
        else:
            status = "diagnostic_only"
        rows_out.append([
            row[0],
            status,
            fmt_float(clean_false),
            fmt_float(hidden_reject),
            row[4],
            row[5],
            fmt_float(accepted_clean_acc),
            fmt_float(accepted_hidden_acc),
        ])
    return rows_out


def _unknown_accepted_hidden_risk_rows(unknown_ablation: List[List[object]]) -> List[List[object]]:
    rows_out: List[List[object]] = []
    for row in unknown_ablation:
        signal = row[0]
        clean_false = _to_float(row[2])
        hidden_reject = _to_float(row[3])
        accepted_clean = int(row[4])
        accepted_hidden = int(row[5])
        accepted_clean_acc = _to_float(row[6])
        accepted_hidden_acc = _to_float(row[7])
        hidden_accept_rate = 1.0 - hidden_reject if np.isfinite(hidden_reject) else float("nan")
        accepted_hidden_risk = 1.0 - accepted_hidden_acc if np.isfinite(accepted_hidden_acc) else float("nan")
        if clean_false > 0.20 + 1e-9:
            status = "fails_clean_budget"
        elif hidden_accept_rate <= 0.30 and accepted_hidden_risk <= 0.30:
            status = "usable_low_hidden_risk"
        elif hidden_accept_rate <= 0.35:
            status = "rejects_many_but_accepted_hidden_risky"
        else:
            status = "diagnostic_only"
        rows_out.append([
            signal,
            status,
            fmt_float(clean_false),
            fmt_float(hidden_reject),
            fmt_float(hidden_accept_rate),
            int(accepted_clean),
            int(accepted_hidden),
            fmt_float(accepted_clean_acc),
            fmt_float(accepted_hidden_acc),
            fmt_float(accepted_hidden_risk),
        ])
    rows_out.sort(key=lambda r: (_to_float(r[4]), _to_float(r[9]), -_to_float(r[2])))
    return rows_out


def _unknown_risk_objective_rows(unknown_ablation: List[List[object]], cfg: dict) -> List[List[object]]:
    """Rank unknown/refusal signals by accepted-hidden risk under a clean budget.

    This table is deliberately post-hoc evaluation: thresholds are still chosen
    from clean rows only in `_unknown_detector_ablation_rows`. Hidden rows are
    used here only to report which fixed signal has the safest accepted tail.
    """
    clean_budget = float(cfg.get("unknown_rejection", {}).get("clean_false_reject_target", 0.20))
    target_hidden_accept = float(cfg.get("unknown_rejection", {}).get("target_hidden_accept_rate", 0.30))
    target_accepted_hidden_risk = float(cfg.get("unknown_rejection", {}).get("target_accepted_hidden_risk", 0.20))
    rows_out: List[List[object]] = []
    for row in unknown_ablation:
        signal = row[0]
        clean_false = _to_float(row[2])
        hidden_reject = _to_float(row[3])
        hidden_accept_rate = 1.0 - hidden_reject if np.isfinite(hidden_reject) else float("nan")
        accepted_clean_acc = _to_float(row[6])
        accepted_hidden_acc = _to_float(row[7])
        accepted_hidden_risk = 1.0 - accepted_hidden_acc if np.isfinite(accepted_hidden_acc) else float("nan")
        clean_penalty = max(0.0, clean_false - clean_budget)
        hidden_accept_penalty = max(0.0, hidden_accept_rate - target_hidden_accept)
        hidden_risk_penalty = max(0.0, accepted_hidden_risk - target_accepted_hidden_risk)
        objective = (
            hidden_accept_rate
            + accepted_hidden_risk
            + 3.0 * clean_penalty
            + hidden_accept_penalty
            + hidden_risk_penalty
            + max(0.0, 0.75 - accepted_clean_acc)
        )
        if clean_false > clean_budget + 1e-9:
            status = "fails_clean_budget"
        elif hidden_accept_rate <= target_hidden_accept and accepted_hidden_risk <= target_accepted_hidden_risk:
            status = "meets_risk_targets"
        elif hidden_accept_rate <= target_hidden_accept:
            status = "accepts_few_but_tail_risky"
        elif accepted_hidden_risk <= target_accepted_hidden_risk:
            status = "tail_safe_but_accepts_many_hidden"
        else:
            status = "diagnostic_only"
        rows_out.append([
            signal,
            status,
            fmt_float(objective),
            fmt_float(clean_false),
            fmt_float(hidden_accept_rate),
            fmt_float(accepted_hidden_risk),
            fmt_float(accepted_clean_acc),
            fmt_float(accepted_hidden_acc),
        ])
    rows_out.sort(key=lambda r: (_to_float(r[2]), _to_float(r[4]), _to_float(r[5])))
    return rows_out


def _active_policy_constraint_status(policy: str, summary: dict, cfg: dict) -> str:
    constraints = cfg.get("active_constraints", {})
    allowed = set(constraints.get("allowed_policies", []))
    if allowed and policy not in allowed:
        return "not_allowed"
    if policy == "extra_sign_flip" and not bool(constraints.get("allow_extra_sign_flip", False)):
        return "not_allowed"
    max_extra_gain = float(constraints.get("max_extra_gain", float("inf")))
    max_sheet_drop = float(constraints.get("max_sheet_drop", float("inf")))
    if policy in {"max_expected_margin", "extra_boost"} and max_extra_gain < 2.5:
        return "constraint_limited"
    if policy == "h0_disambiguation" and max_sheet_drop < 0.40:
        return "constraint_limited"
    if abs(float(summary.get("median_margin_gain", 0.0))) > max_extra_gain:
        return "constraint_limited"
    return "allowed"


def pypeec_bridge_outputs(
    cfg: dict,
    complexity_penalty: float,
    threshold: float,
    marginal_threshold: float,
    global_threshold: float,
    via_offsets: list[tuple[float, float]],
    global_transforms: list[dict],
    outputs_dir: Path,
) -> dict:
    bridge_cfg = cfg.get("pypeec_bridge", {})
    default_npz = EXP_DIR.parent / "E07_solver_bridge" / "data" / "pypeec_exp03_like_mini_dataset.npz"
    npz_path = Path(bridge_cfg.get("npz_path", default_npz))
    if not npz_path.is_absolute():
        npz_path = (EXP_DIR / npz_path).resolve()
    labels = list(cfg["scoring"]["hypotheses"])
    result = {"enabled": bool(bridge_cfg.get("enabled", True)), "npz_path": str(npz_path), "available": npz_path.exists()}
    if not result["enabled"] or not npz_path.exists():
        result["summaries"] = {}
        return result

    summaries = {}
    all_rows_by_field = {}
    pypeec_basis_rows = []
    global_reg_rows = []
    evidence_rows = []
    evidence_detail_rows = []
    h0_hard_rows = []
    evidence_modes = list(cfg.get("model_evidence", {}).get("modes", ["default_score"]))
    for field_key in ["B_centerline", "B_pypeec"]:
        records, obs_grid = load_exp07_graph_bridge_records(npz_path, field_key=field_key)
        rows = evaluate_records(records, obs_grid, cfg, complexity_penalty=complexity_penalty)
        summaries[field_key] = _summary_for_rows(rows, labels, threshold)
        for evidence_mode in evidence_modes:
            ev_summary = _summary_for_evidence_mode(rows, labels, cfg, evidence_mode)
            evidence_rows.append(_model_evidence_table_row(field_key, "base", evidence_mode, ev_summary))
            if field_key == "B_pypeec":
                evidence_detail_rows.extend(_evidence_detail_rows(field_key, "base", evidence_mode, rows, labels, cfg))
            if field_key == "B_pypeec" and evidence_mode in {"default_score", "h0_conservative"}:
                h0_rows = [r for r in rows if r["true_hypothesis"] == "H0_sheet_only"]
                h0_hard_rows.append(_h0_hard_row("pypeec_no_via", f"base/{evidence_mode}", _summary_for_evidence_mode(h0_rows, labels, cfg, evidence_mode)))
        rows_marg = _evaluate_via_marginalized_records(records, obs_grid, cfg, complexity_penalty, via_offsets)
        summaries[f"{field_key}_via_marginalized"] = _summary_for_rows(rows_marg, labels, marginal_threshold)
        summaries[f"{field_key}_via_marginalized"]["median_best_offset_um"] = float(
            np.median([r["best_via_offset_norm_m"] for r in rows_marg]) * 1e6
        )
        rows_global = _evaluate_global_registration_records(records, obs_grid, cfg, complexity_penalty, global_transforms)
        summaries[f"{field_key}_global_registered"] = _summary_for_rows(rows_global, labels, global_threshold)
        summaries[f"{field_key}_global_registered"]["median_translation_um"] = float(
            np.median([r["best_global_translation_norm_m"] for r in rows_global]) * 1e6
        )
        summaries[f"{field_key}_global_registered"]["median_rotation_deg"] = float(
            np.median([r["best_global_rotation_abs_deg"] for r in rows_global])
        )
        summaries[f"{field_key}_global_registered"]["median_scale_delta"] = float(
            np.median([r["best_global_scale_delta"] for r in rows_global])
        )
        global_reg_rows.extend([
            [
                field_key,
                "base",
                fmt_float(summaries[field_key]["accuracy"]),
                fmt_float(summaries[field_key]["via_detection"]["auc"]),
                fmt_float(summaries[field_key]["via_detection"]["false_positive_rate"]),
                fmt_float(summaries[field_key]["median_best_residual_rel_l2"]),
                "",
                "",
                "",
            ],
            [
                field_key,
                "global_registration_search",
                fmt_float(summaries[f"{field_key}_global_registered"]["accuracy"]),
                fmt_float(summaries[f"{field_key}_global_registered"]["via_detection"]["auc"]),
                fmt_float(summaries[f"{field_key}_global_registered"]["via_detection"]["false_positive_rate"]),
                fmt_float(summaries[f"{field_key}_global_registered"]["median_best_residual_rel_l2"]),
                fmt_float(summaries[f"{field_key}_global_registered"]["median_translation_um"]),
                fmt_float(summaries[f"{field_key}_global_registered"]["median_rotation_deg"]),
                fmt_float(summaries[f"{field_key}_global_registered"]["median_scale_delta"]),
            ],
        ])
        basis_modes = list(cfg.get("pypeec_aware_basis", {}).get("modes", []))
        for mode in basis_modes:
            variant_records = [augment_record_for_pypeec_basis(rec, cfg, mode) for rec in records]
            basis_rows = evaluate_records(variant_records, obs_grid, cfg, complexity_penalty=complexity_penalty)
            key = f"{field_key}_basis_{mode}"
            summaries[key] = _summary_for_rows(basis_rows, labels, threshold)
            for evidence_mode in evidence_modes:
                ev_summary = _summary_for_evidence_mode(basis_rows, labels, cfg, evidence_mode)
                evidence_rows.append(_model_evidence_table_row(field_key, mode, evidence_mode, ev_summary))
                if field_key == "B_pypeec":
                    evidence_detail_rows.extend(_evidence_detail_rows(field_key, mode, evidence_mode, basis_rows, labels, cfg))
                if field_key == "B_pypeec" and evidence_mode in {"default_score", "h0_conservative"}:
                    h0_rows = [r for r in basis_rows if r["true_hypothesis"] == "H0_sheet_only"]
                    h0_hard_rows.append(_h0_hard_row("pypeec_no_via", f"{mode}/{evidence_mode}", _summary_for_evidence_mode(h0_rows, labels, cfg, evidence_mode)))
            residual_delta = summaries[key]["median_best_residual_rel_l2"] - summaries[field_key]["median_best_residual_rel_l2"]
            pypeec_basis_rows.append([
                field_key,
                mode,
                fmt_float(summaries[key]["accuracy"]),
                fmt_float(summaries[key]["per_class_accuracy"].get("H0_sheet_only", float("nan"))),
                fmt_float(summaries[key]["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
                fmt_float(summaries[key]["per_class_accuracy"].get("H2_sheet_return", float("nan"))),
                fmt_float(summaries[key]["via_detection"]["auc"]),
                fmt_float(summaries[key]["via_detection"]["false_positive_rate"]),
                fmt_float(summaries[key]["median_best_residual_rel_l2"]),
                fmt_float(residual_delta),
            ])
        all_rows_by_field[field_key] = rows

    table_rows = [_summary_table_row(field_key, summaries[field_key]) for field_key in ["B_centerline", "B_pypeec"]]
    (outputs_dir / "PYPEEC_GRAPH_BRIDGE_TABLE.md").write_text(
        "# Exp08 graph scorer on exp07 centerline and PyPEEC fields\n\n"
        + markdown_table(
            [
                "field",
                "n",
                "4-way acc",
                "H0 acc",
                "H1 acc",
                "H2 acc",
                "H3 acc",
                "via AUC",
                "via recall",
                "via F1",
                "no-via FP",
                "median margin",
                "median residual",
            ],
            table_rows,
        )
        + "\nBoundary: exp07 metadata is converted to an approximate graph; this is not real CAD import.\n",
        encoding="utf-8",
    )

    failures = []
    for row in all_rows_by_field["B_pypeec"]:
        if row["true_hypothesis"] == row["pred_hypothesis"]:
            continue
        failures.append([
            row["case_id"],
            row["record"].metadata.get("case_type", ""),
            row["record"].metadata.get("is_exp03_like", ""),
            row["class_label"],
            row["true_hypothesis"],
            row["pred_hypothesis"],
            fmt_float(row["confidence_margin"]),
            fmt_float(row["via_evidence"]),
            fmt_float(row["results"][row["true_hypothesis"]].residual_rel_l2),
            fmt_float(row["results"][row["pred_hypothesis"]].residual_rel_l2),
        ])
    (outputs_dir / "PYPEEC_GRAPH_BRIDGE_FAILURE_CASES.md").write_text(
        "# Exp08 exp07-PyPEEC bridge failure cases\n\n"
        + markdown_table(
            [
                "case",
                "case type",
                "exp03-like",
                "class",
                "true H",
                "pred H",
                "margin",
                "via evidence",
                "true residual",
                "pred residual",
            ],
            failures[:100],
        )
        + f"\nTotal PyPEEC bridge misclassified cases: `{len(failures)}`.\n",
        encoding="utf-8",
    )
    result["summaries"] = summaries
    result["n_pypeec_failures"] = len(failures)
    reg_rows = []
    for field_key in ["B_centerline", "B_pypeec"]:
        base = summaries[field_key]
        marg = summaries[f"{field_key}_via_marginalized"]
        reg_rows.append([
            field_key,
            "base",
            fmt_float(base["accuracy"]),
            fmt_float(base["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
            fmt_float(base["via_detection"]["auc"]),
            fmt_float(base["via_detection"]["recall"]),
            fmt_float(base["via_detection"]["f1"]),
            fmt_float(base["via_detection"]["false_positive_rate"]),
            "",
        ])
        reg_rows.append([
            field_key,
            "via_location_marginalized",
            fmt_float(marg["accuracy"]),
            fmt_float(marg["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
            fmt_float(marg["via_detection"]["auc"]),
            fmt_float(marg["via_detection"]["recall"]),
            fmt_float(marg["via_detection"]["f1"]),
            fmt_float(marg["via_detection"]["false_positive_rate"]),
            fmt_float(marg["median_best_offset_um"]),
        ])
    (outputs_dir / "PYPEEC_BRIDGE_REGISTRATION_TABLE.md").write_text(
        "# Exp08 P0-next PyPEEC bridge with via-location marginalization\n\n"
        + markdown_table(
            [
                "field",
                "mode",
                "4-way acc",
                "H1 acc",
                "via AUC",
                "via recall",
                "via F1",
                "no-via FP",
                "median best offset um",
            ],
            reg_rows,
        )
        + "\nOffsets are fixed by configuration and are not selected on PyPEEC labels.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_BRIDGE_GLOBAL_REGISTRATION_TABLE.md").write_text(
        "# Exp08 P1 global graph-to-field registration diagnostic\n\n"
        + markdown_table(
            [
                "field",
                "mode",
                "4-way acc",
                "via AUC",
                "no-via FP",
                "median residual",
                "median translation um",
                "median abs rotation deg",
                "median scale delta",
            ],
            global_reg_rows,
        )
        + "\nThe transform grid is fixed by config and is not selected on PyPEEC labels.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_AWARE_BASIS_TABLE.md").write_text(
        "# Exp08 P0 PyPEEC-aware graph basis-bank diagnostic\n\n"
        + markdown_table(
            [
                "field",
                "basis mode",
                "4-way acc",
                "H0 acc",
                "H1 acc",
                "H2 acc",
                "via AUC",
                "no-via FP",
                "median residual",
                "residual delta vs base",
            ],
            pypeec_basis_rows,
        )
        + "\nBasis-bank modes are fixed diagnostics: finite-width sheet, return bank, artifact bank, distributed via, and a combined mode. They do not use PyPEEC labels for selection.\n",
        encoding="utf-8",
    )
    evidence_header = [
        "field",
        "basis mode",
        "evidence mode",
        "n",
        "4-way acc",
        "H0 acc",
        "H1 acc",
        "H2 acc",
        "H3 acc",
        "false H1 rate",
        "false H2 rate",
        "false H3 rate",
        "median residual",
        "median params",
    ]
    (outputs_dir / "MODEL_EVIDENCE_SELECTION_TABLE.md").write_text(
        "# Exp08 P0 model-evidence selection diagnostic\n\n"
        + markdown_table(evidence_header, evidence_rows)
        + "\nEvidence modes reuse the same fitted basis matrices and change only model-selection scoring. They are diagnostics, not PyPEEC-calibrated thresholds.\n",
        encoding="utf-8",
    )
    pypeec_rows = [row for row in evidence_rows if row[0] == "B_pypeec"]
    (outputs_dir / "PYPEEC_MODEL_BANK_EVIDENCE_TABLE.md").write_text(
        "# Exp08 P2 disciplined PyPEEC model-bank evidence table\n\n"
        + markdown_table(evidence_header, pypeec_rows)
        + "\nThis table audits which fixed basis/evidence combinations improve classification and which merely reduce residual by over-expanding the model space.\n",
        encoding="utf-8",
    )
    model_selection_rows = _model_selection_calibration_rows(evidence_rows, cfg)
    (outputs_dir / "MODEL_SELECTION_CALIBRATION_TABLE.md").write_text(
        "# Exp08 P0 formal model-selection calibration audit\n\n"
        + markdown_table(
            [
                "basis mode",
                "evidence mode",
                "objective",
                "4-way acc",
                "H0 acc",
                "H1 acc",
                "H2 acc",
                "false H1",
                "false H2",
                "false H3",
                "median residual",
                "median params",
                "meets H1 floor",
            ],
            model_selection_rows,
        )
        + "\nThe objective is a fixed audit formula over PyPEEC frozen rows. It ranks trade-offs for analysis but is not used to tune the current PyPEEC predictions or thresholds.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_MODEL_BANK_ALLOWED_BASIS_TABLE.md").write_text(
        "# Exp08 P3 disciplined model-bank allowed-basis table\n\n"
        + markdown_table(
            ["hypothesis", "allowed evidence/basis", "restricted basis", "reason"],
            _model_bank_allowed_basis_rows(),
        )
        + "\nThis table states the model-bank discipline explicitly: richer bases must compete as hypotheses and should not be silently admitted to every class.\n",
        encoding="utf-8",
    )
    heldout_rows, tradeoff_rows = _pypeec_heldout_model_selection_rows(evidence_detail_rows, labels, cfg)
    stability_rows = _pypeec_model_selection_stability_rows(evidence_detail_rows, labels, cfg)
    selective_rows = _pypeec_class_specific_selective_rows(evidence_detail_rows, labels, cfg)
    stacked_rows = _pypeec_stacked_evidence_calibrator_rows(evidence_detail_rows, labels, cfg)
    stacked_group_rows = _pypeec_stacked_group_heldout_rows(evidence_detail_rows, labels, cfg)
    stacked_group_distance_rows = _pypeec_stacked_group_distance_refusal_rows(evidence_detail_rows, labels, cfg)
    stacked_ablation_rows = _pypeec_stacked_feature_ablation_rows(evidence_detail_rows, labels, cfg)
    hidden_records = generate_hidden_mechanism_records(cfg)
    hidden_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    hidden_details = _stacked_evidence_details_for_records(hidden_records, hidden_grid, cfg, complexity_penalty, labels, "hidden_mechanism")
    near_hidden_records = generate_near_boundary_hidden_records(cfg)
    near_hidden_details = _stacked_evidence_details_for_records(
        near_hidden_records,
        hidden_grid,
        cfg,
        complexity_penalty,
        labels,
        "near_boundary_hidden",
    )
    severity_records = generate_near_boundary_hidden_severity_records(cfg)
    severity_details = _stacked_evidence_details_for_records(
        severity_records,
        hidden_grid,
        cfg,
        complexity_penalty,
        labels,
        "near_boundary_hidden_severity",
    )
    finite_records, finite_grid = load_exp07_graph_bridge_records(npz_path, field_key="B_finite")
    finite_details = _stacked_evidence_details_for_records(finite_records, finite_grid, cfg, complexity_penalty, labels, "B_finite")
    center_records, center_grid = load_exp07_graph_bridge_records(npz_path, field_key="B_centerline")
    center_details = _stacked_evidence_details_for_records(center_records, center_grid, cfg, complexity_penalty, labels, "B_centerline")
    stacked_unknown_rows = _pypeec_stacked_unknown_safety_rows(evidence_detail_rows, hidden_details, labels, cfg)
    stacked_near_unknown_rows = _pypeec_stacked_unknown_safety_rows(
        evidence_detail_rows,
        near_hidden_details,
        labels,
        cfg,
        hidden_field_key="near_boundary_hidden",
    )
    stacked_space_rows = _stacked_evidence_space_diagnostic_rows(
        evidence_detail_rows,
        hidden_details,
        near_hidden_details,
        labels,
        outputs_dir,
    )
    family_fewshot_rows = _pypeec_family_fewshot_adaptation_rows(evidence_detail_rows, labels, cfg)
    near_hidden_severity_rows = _stacked_evidence_near_hidden_severity_rows(
        evidence_detail_rows,
        severity_details,
        labels,
        cfg,
    )
    near_hidden_accepted_rows = _near_hidden_accepted_case_rows(evidence_detail_rows, near_hidden_details, labels, cfg)
    stacked_external_rows = _pypeec_stacked_external_stress_rows(
        evidence_detail_rows,
        {"B_finite": finite_details, "B_centerline": center_details, "hidden_mechanism": hidden_details},
        labels,
        cfg,
    )
    stacked_selective_rows = _pypeec_stacked_selective_risk_rows(evidence_detail_rows, labels, cfg)
    distribution_gap_rows = _pypeec_distribution_gap_rows(evidence_detail_rows, labels, cfg)
    split_rows = _pypeec_split_table_rows(evidence_detail_rows, cfg)
    (outputs_dir / "PYPEEC_HELDOUT_SPLIT_TABLE.md").write_text(
        "# Exp08 P0 held-out PyPEEC model-selection split\n\n"
        + markdown_table(["true hypothesis", "n cases", "calibration", "heldout"], split_rows)
        + "\nThis deterministic split is used only for the pilot held-out model-selection audit. The frozen bridge tables above remain no-calibration results.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_HELDOUT_MODEL_SELECTION_TABLE.md").write_text(
        "# Exp08 P0 held-out PyPEEC model-selection pilot\n\n"
        + markdown_table(
            [
                "basis mode",
                "evidence mode",
                "cal objective",
                "heldout objective",
                "cal n",
                "heldout n",
                "cal 4-way acc",
                "heldout 4-way acc",
                "cal H0 acc",
                "heldout H0 acc",
                "cal H1 acc",
                "heldout H1 acc",
                "heldout H2 acc",
                "heldout H0 false H1",
                "heldout H0 false H2",
                "heldout H0 false H3",
            ],
            heldout_rows,
        )
        + "\nRows are ranked by calibration objective and evaluated on held-out PyPEEC cases. This is a pilot split on the current mini distribution, not broad CAD/FEM validation.\n",
        encoding="utf-8",
    )
    (outputs_dir / "H0_H1_MODEL_SELECTION_TRADEOFF_TABLE.md").write_text(
        "# Exp08 P1 H0/H1 model-selection trade-off table\n\n"
        + markdown_table(
            [
                "basis mode",
                "evidence mode",
                "heldout H0 acc",
                "heldout H1 acc",
                "heldout 4-way acc",
                "heldout H0 false H1",
                "heldout H0 false H2",
                "heldout H0 false H3",
                "heldout median residual",
                "heldout median params",
            ],
            tradeoff_rows,
        )
        + "\nThis table treats H0/no-via safety and H1/true-via recall as primary endpoints rather than secondary columns hidden inside overall accuracy.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_MODEL_SELECTION_STABILITY_TABLE.md").write_text(
        "# Exp08 P0 repeated-split PyPEEC model-selection stability\n\n"
        + markdown_table(
            [
                "basis mode",
                "evidence mode",
                "repeats",
                "top-1 selected",
                "top-1 rate",
                "heldout obj mean",
                "heldout obj std",
                "heldout obj CI low",
                "heldout obj CI high",
                "heldout 4-way mean",
                "heldout 4-way std",
                "heldout H0 mean",
                "heldout H0 std",
                "heldout H1 mean",
                "heldout H1 std",
                "heldout H2 mean",
                "heldout H0 false-any mean",
                "heldout params mean",
            ],
            stability_rows,
        )
        + "\nRows use repeated stratified calibration/held-out splits of the same PyPEEC mini distribution. The table estimates ranking stability; it does not create a final model-selection claim.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_CLASS_SPECIFIC_SELECTIVE_TABLE.md").write_text(
        "# Exp08 P0 class-specific selective hypothesis audit\n\n"
        + markdown_table(
            [
                "policy",
                "field",
                "basis mode",
                "evidence mode",
                "repeats",
                "coverage mean",
                "coverage std",
                "coverage p10",
                "coverage p90",
                "accepted acc mean",
                "accepted acc std",
                "H0 false-any mean",
                "H0 false-any median",
                "H0 accepted-correct mean",
                "H1 accepted-correct mean",
                "H1 acceptance mean",
                "unknown mean",
                "status",
            ],
            selective_rows,
        )
        + "\nThis table is the formal audit of the current core bottleneck: class-specific refusal can carve out a trusted-output region, but a reliable detector also needs high true-via acceptance. Thresholds are selected only on calibration folds and evaluated on repeated held-out folds of the PyPEEC mini distribution.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_STACKED_EVIDENCE_CALIBRATOR_TABLE.md").write_text(
        "# Exp08 P0 PyPEEC stacked evidence calibrator\n\n"
        + markdown_table(
            [
                "calibration policy",
                "repeats",
                "heldout 4-way mean",
                "heldout 4-way std",
                "heldout H0 mean",
                "heldout H1 mean",
                "heldout H2 mean",
                "heldout H3 mean",
                "heldout H0 false-any mean",
                "heldout objective mean",
                "heldout objective std",
                "alpha counts",
                "status",
            ],
            stacked_rows,
        )
        + "\nThis is the first explicit PyPEEC calibration/held-out evidence-fusion experiment in exp08. It trains a simple ridge one-vs-rest calibrator on calibration folds using all frozen basis/evidence scores as features, then evaluates held-out folds. It is not a frozen no-calibration claim; it tests whether the current evidence bank already contains enough information once legal calibration is allowed.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_STACKED_EVIDENCE_GROUP_HELDOUT_TABLE.md").write_text(
        "# Exp08 P0 stacked evidence group-heldout stress\n\n"
        + markdown_table(
            [
                "group policy",
                "heldout group",
                "heldout n",
                "train n",
                "4-way acc",
                "H0 acc",
                "H1 acc",
                "H2 acc",
                "H3 acc",
                "H0 false-any",
                "status",
            ],
            stacked_group_rows,
        )
        + "\nThis table tests whether the stacked calibrator survives stricter group-heldout splits. Variant-mod folds are evaluable for all classes; pure family leaveout is skipped when the training set would lose the held-out class entirely.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_STACKED_EVIDENCE_GROUP_DISTANCE_REFUSAL_TABLE.md").write_text(
        "# Exp08 family-heldout feature-distance refusal audit\n\n"
        + markdown_table(
            [
                "group policy",
                "heldout group",
                "heldout n",
                "train n",
                "raw acc",
                "raw H0 false-any",
                "distance reject",
                "accepted acc",
                "accepted risk",
                "accepted H0 false-any",
                "status",
            ],
            stacked_group_distance_rows,
        )
        + "\nThis table asks whether the feature-distance safety layer makes unseen held-out families safer. High rejection means the system is refusing out-of-family evidence rather than pretending it can classify it; high accepted accuracy is required before calling it cross-family generalization.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_FAMILY_FEWSHOT_ADAPTATION_TABLE.md").write_text(
        "# Exp08 few-shot family adaptation audit\n\n"
        + markdown_table(
            [
                "heldout family",
                "shots from family",
                "train n",
                "eval n",
                "raw acc",
                "raw H0 false-any",
                "distance reject",
                "accepted acc",
                "accepted risk",
                "accepted H0 false-any",
                "status",
            ],
            family_fewshot_rows,
        )
        + "\nThis table tests whether an unseen generated family can move from safe refusal toward useful diagnosis after a small number of family-specific calibration samples. Shots are added only to the calibration side; the remaining family rows are evaluated held out.\n",
        encoding="utf-8",
    )
    (outputs_dir / "STACKED_EVIDENCE_FEATURE_ABLATION_TABLE.md").write_text(
        "# Exp08 P1 stacked evidence feature ablation\n\n"
        + markdown_table(
            [
                "feature policy",
                "n features",
                "repeats",
                "heldout 4-way mean",
                "heldout 4-way std",
                "heldout H0 mean",
                "heldout H1 mean",
                "heldout H2 mean",
                "heldout H3 mean",
                "heldout H0 false-any mean",
                "heldout objective mean",
                "heldout objective std",
                "alpha counts",
                "status",
            ],
            stacked_ablation_rows,
        )
        + "\nAll rows use fixed alpha=100 and repeated PyPEEC calibration/held-out splits. This ablation identifies whether the breakthrough comes from scores, margins, predicted one-hot outputs, or specific basis families.\n",
        encoding="utf-8",
    )
    (outputs_dir / "STACKED_EVIDENCE_UNKNOWN_SAFETY_TABLE.md").write_text(
        "# Exp08 P2 stacked evidence unknown-safety stress\n\n"
        + markdown_table(
            [
                "policy",
                "clean false reject target",
                "repeats",
                "clean reject",
                "accepted clean acc",
                "hidden reject",
                "hidden accept",
                "accepted hidden acc",
                "accepted hidden risk",
                "status",
            ],
            stacked_unknown_rows,
        )
        + "\nEach threshold is selected only inside the PyPEEC calibration fold and then applied to held-out PyPEEC and hidden-mechanism stress. Confidence-margin rejection tests classifier uncertainty; feature-distance rejection tests whether a stacked-evidence vector is outside the calibrated in-library class manifold; the combined row is an ablation rather than a tuned production rule.\n",
        encoding="utf-8",
    )
    (outputs_dir / "STACKED_EVIDENCE_NEAR_BOUNDARY_HIDDEN_TABLE.md").write_text(
        "# Exp08 near-boundary hidden stress with stacked-evidence OOD screens\n\n"
        + markdown_table(
            [
                "policy",
                "clean false reject target",
                "repeats",
                "clean reject",
                "accepted clean acc",
                "near-hidden reject",
                "near-hidden accept",
                "accepted near-hidden acc",
                "accepted near-hidden risk",
                "status",
            ],
            stacked_near_unknown_rows,
        )
        + "\nNear-boundary hidden cases are intentionally closer to known return/via/artifact candidates than the base hidden stress. This table tests whether the distance screen only rejects obvious outliers or also protects against harder near-manifold unknowns.\n",
        encoding="utf-8",
    )
    (outputs_dir / "STACKED_EVIDENCE_NEAR_HIDDEN_SEVERITY_TABLE.md").write_text(
        "# Exp08 near-boundary hidden severity sweep\n\n"
        + markdown_table(
            [
                "policy",
                "severity",
                "repeats",
                "clean reject",
                "accepted clean acc",
                "hidden reject",
                "hidden accept",
                "accepted hidden acc",
                "accepted hidden risk",
                "median unknown signal",
            ],
            near_hidden_severity_rows,
        )
        + "\nThis sweep varies near-boundary hidden strength and displacement. It reports how refusal and accepted risk change as hidden mechanisms move closer to or farther from the calibrated evidence manifold.\n",
        encoding="utf-8",
    )
    (outputs_dir / "NEAR_HIDDEN_ACCEPTED_CASES.md").write_text(
        "# Exp08 accepted near-boundary hidden case audit\n\n"
        + markdown_table(
            [
                "case id",
                "hidden family",
                "primary truth",
                "predicted",
                "feature distance",
                "distance threshold",
                "confidence margin",
                "mechanism status",
            ],
            near_hidden_accepted_rows,
        )
        + "\nAccepted near-hidden rows are audited separately because primary-label correctness is weaker than mechanism-level explanation. A wrong-layer or shifted via can be primary-label correct while still indicating an incomplete graph/candidate model.\n",
        encoding="utf-8",
    )
    (outputs_dir / "STACKED_EVIDENCE_SPACE_DIAGNOSTICS_TABLE.md").write_text(
        "# Exp08 stacked-evidence space diagnostics\n\n"
        + markdown_table(
            [
                "dataset",
                "n",
                "median feature distance",
                "p90 feature distance",
                "pc1 mean",
                "pc1 std",
                "pc2 mean",
                "pc2 std",
                "label counts",
            ],
            stacked_space_rows,
        )
        + "\nThe companion `stacked_evidence_space_pca.png` projects in-library PyPEEC, base hidden, and near-boundary hidden evidence vectors into the first two PCA axes of the in-library stacked-evidence space. The table reports feature-distance separation; the plot is explanatory only and is not used to tune thresholds.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_STACKED_EVIDENCE_EXTERNAL_STRESS_TABLE.md").write_text(
        "# Exp08 P3 stacked evidence external/operator stress\n\n"
        + markdown_table(
            [
                "stress field",
                "repeats",
                "n cases",
                "4-way acc",
                "H0 acc",
                "H1 acc",
                "H2 acc",
                "H3 acc",
                "H0 false-any",
            ],
            stacked_external_rows,
        )
        + "\nThe calibrator is trained on PyPEEC calibration folds and evaluated on operator-shifted or hidden-mechanism fields. These are stress proxies, not real CAD/FEM/QDM validation.\n",
        encoding="utf-8",
    )
    (outputs_dir / "STACKED_EVIDENCE_SELECTIVE_RISK_TABLE.md").write_text(
        "# Exp08 P4 stacked evidence selective-risk table\n\n"
        + markdown_table(
            [
                "policy",
                "coverage",
                "repeats",
                "accepted acc",
                "accepted H0 acc",
                "accepted H1 acc",
                "accepted H0 false-any",
                "H1 acceptance",
                "reject rate",
            ],
            stacked_selective_rows,
        )
        + "\nThis table keeps refusal in the final diagnostic path. A strong calibrator should still expose coverage/risk rather than forcing every ambiguous residual into a hard label.\n",
        encoding="utf-8",
    )
    (outputs_dir / "PYPEEC_DISTRIBUTION_GAP_TABLE.md").write_text(
        "# Exp08 P1 PyPEEC distribution target coverage\n\n"
        + markdown_table(
            [
                "true hypothesis",
                "current unique cases",
                "target cases",
                "gap to target",
                "observed families",
                "status",
            ],
            distribution_gap_rows,
        )
        + "\nThis table audits the current PyPEEC model-selection target coverage. Meeting the mini-distribution targets is necessary for stronger model-selection stress, but it is still not a claim that CAD/FEM/QDM distribution coverage has been solved.\n",
        encoding="utf-8",
    )
    result["model_selection_calibration_rows"] = model_selection_rows
    result["pypeec_heldout_model_selection_rows"] = heldout_rows
    result["h0_h1_tradeoff_rows"] = tradeoff_rows
    result["pypeec_model_selection_stability_rows"] = stability_rows
    result["pypeec_class_specific_selective_rows"] = selective_rows
    result["pypeec_stacked_evidence_calibrator_rows"] = stacked_rows
    result["pypeec_stacked_evidence_group_heldout_rows"] = stacked_group_rows
    result["pypeec_stacked_evidence_group_distance_refusal_rows"] = stacked_group_distance_rows
    result["pypeec_family_fewshot_adaptation_rows"] = family_fewshot_rows
    result["stacked_evidence_feature_ablation_rows"] = stacked_ablation_rows
    result["stacked_evidence_unknown_safety_rows"] = stacked_unknown_rows
    result["stacked_evidence_near_boundary_hidden_rows"] = stacked_near_unknown_rows
    result["stacked_evidence_space_diagnostic_rows"] = stacked_space_rows
    result["stacked_evidence_near_hidden_severity_rows"] = near_hidden_severity_rows
    result["near_hidden_accepted_case_rows"] = near_hidden_accepted_rows
    result["pypeec_stacked_evidence_external_stress_rows"] = stacked_external_rows
    result["stacked_evidence_selective_risk_rows"] = stacked_selective_rows
    result["pypeec_distribution_gap_rows"] = distribution_gap_rows
    result["h0_hard_rows"] = h0_hard_rows
    return result


def hidden_stress_outputs(
    cfg: dict,
    complexity_penalty: float,
    threshold: float,
    marginal_threshold: float,
    via_offsets: list[tuple[float, float]],
    unknown_thresholds: dict,
    clean_risk_rows: List[dict],
    outputs_dir: Path,
) -> dict:
    labels = list(cfg["scoring"]["hypotheses"])
    records = generate_hidden_mechanism_records(cfg)
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    rows = evaluate_records(records, obs_grid, cfg, complexity_penalty=complexity_penalty)
    rows_marg = _evaluate_via_marginalized_records(records, obs_grid, cfg, complexity_penalty, via_offsets)
    clean_records = [r["record"] for r in clean_risk_rows]
    clean_marg_rows = _evaluate_via_marginalized_records(clean_records, obs_grid, cfg, complexity_penalty, via_offsets)
    summary_all = _summary_for_rows(rows, labels, threshold)
    summary_all_marg = _summary_for_rows(rows_marg, labels, marginal_threshold)
    by_family: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_family[str(row["record"].metadata.get("hidden_mechanism_family", "unknown"))].append(row)
    family_summaries = {family: _summary_for_rows(family_rows, labels, threshold) for family, family_rows in by_family.items()}
    table_rows = [_summary_table_row("all_hidden", summary_all)] + [
        _summary_table_row(family, summary) for family, summary in sorted(family_summaries.items())
    ]
    (outputs_dir / "HIDDEN_MECHANISM_STRESS_TABLE.md").write_text(
        "# Exp08 hidden-mechanism OOD stress\n\n"
        + markdown_table(
            [
                "family",
                "n",
                "4-way acc",
                "H0 acc",
                "H1 acc",
                "H2 acc",
                "H3 acc",
                "via AUC",
                "via recall",
                "via F1",
                "no-via FP",
                "median margin",
                "median residual",
            ],
            table_rows,
        )
        + "\nHidden mechanisms are deliberately missing or mismatched in the candidate library; perfect accuracy is not expected.\n",
        encoding="utf-8",
    )
    failures = []
    for row in rows:
        if row["true_hypothesis"] == row["pred_hypothesis"]:
            continue
        failures.append([
            row["case_id"],
            row["record"].metadata.get("hidden_mechanism_family", ""),
            row["class_label"],
            row["true_hypothesis"],
            row["pred_hypothesis"],
            fmt_float(row["confidence_margin"]),
            fmt_float(row["via_evidence"]),
            fmt_float(row["results"][row["true_hypothesis"]].residual_rel_l2),
            fmt_float(row["results"][row["pred_hypothesis"]].residual_rel_l2),
        ])
    (outputs_dir / "HIDDEN_MECHANISM_FAILURE_CASES.md").write_text(
        "# Exp08 hidden-mechanism failure cases\n\n"
        + markdown_table(
            ["case", "family", "class", "true H", "pred H", "margin", "via evidence", "true residual", "pred residual"],
            failures[:120],
        )
        + f"\nTotal hidden-stress misclassified cases: `{len(failures)}`.\n",
        encoding="utf-8",
    )
    reg_rows = [
        [
            "all_hidden",
            "base",
            fmt_float(summary_all["accuracy"]),
            fmt_float(summary_all["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
            fmt_float(summary_all["via_detection"]["recall"]),
            fmt_float(summary_all["via_detection"]["f1"]),
            fmt_float(summary_all["via_detection"]["false_positive_rate"]),
            "",
        ],
        [
            "all_hidden",
            "via_location_marginalized",
            fmt_float(summary_all_marg["accuracy"]),
            fmt_float(summary_all_marg["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
            fmt_float(summary_all_marg["via_detection"]["recall"]),
            fmt_float(summary_all_marg["via_detection"]["f1"]),
            fmt_float(summary_all_marg["via_detection"]["false_positive_rate"]),
            fmt_float(np.median([r["best_via_offset_norm_m"] for r in rows_marg]) * 1e6),
        ],
    ]
    marg_family_summaries = {}
    for family, family_rows in sorted(by_family.items()):
        marg_family_rows = [r for r in rows_marg if r["record"].metadata.get("hidden_mechanism_family") == family]
        base_summary = family_summaries[family]
        marg_summary = _summary_for_rows(marg_family_rows, labels, marginal_threshold)
        marg_family_summaries[family] = marg_summary
        reg_rows.append([
            family,
            "base",
            fmt_float(base_summary["accuracy"]),
            fmt_float(base_summary["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
            fmt_float(base_summary["via_detection"]["recall"]),
            fmt_float(base_summary["via_detection"]["f1"]),
            fmt_float(base_summary["via_detection"]["false_positive_rate"]),
            "",
        ])
        reg_rows.append([
            family,
            "via_location_marginalized",
            fmt_float(marg_summary["accuracy"]),
            fmt_float(marg_summary["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
            fmt_float(marg_summary["via_detection"]["recall"]),
            fmt_float(marg_summary["via_detection"]["f1"]),
            fmt_float(marg_summary["via_detection"]["false_positive_rate"]),
            fmt_float(np.median([r["best_via_offset_norm_m"] for r in marg_family_rows]) * 1e6) if marg_family_rows else "nan",
        ])
    (outputs_dir / "REGISTRATION_MARGINALIZATION_TABLE.md").write_text(
        "# Exp08 P0-next/P1-next via-location marginalization\n\n"
        + markdown_table(
            [
                "family",
                "mode",
                "4-way acc",
                "H1 acc",
                "via recall",
                "via F1",
                "no-via FP",
                "median best offset um",
            ],
            reg_rows,
        )
        + "\nVia candidate offsets are fixed by config and selected without hidden/PyPEEC labels.\n",
        encoding="utf-8",
    )
    unknown_rows = [_unknown_table_row("hidden_all", _unknown_summary(rows, unknown_thresholds))]
    for family, family_rows in sorted(by_family.items()):
        unknown_rows.append(_unknown_table_row(f"hidden_{family}", _unknown_summary(family_rows, unknown_thresholds)))
    (outputs_dir / "UNKNOWN_REJECTION_TABLE.md").write_text(
        "# Exp08 P2-next unknown / out-of-library rejection\n\n"
        + markdown_table(
            [
                "dataset",
                "n",
                "accepted",
                "rejected",
                "unknown rate",
                "full acc",
                "accepted acc",
                "median margin",
                "median residual",
            ],
            unknown_rows,
        )
        + f"\nValidation thresholds: min_margin=`{unknown_thresholds['min_margin']:.6g}`, max_residual=`{unknown_thresholds['max_residual']:.6g}`.\n",
        encoding="utf-8",
    )
    risk_rows = _selective_unknown_rows("clean_ood", clean_risk_rows)
    risk_rows += _selective_unknown_rows("hidden_all", rows)
    for family, family_rows in sorted(by_family.items()):
        risk_rows += _selective_unknown_rows(f"hidden_{family}", family_rows)
    (outputs_dir / "UNKNOWN_RISK_COVERAGE_TABLE.md").write_text(
        "# Exp08 P2 unknown rejection risk-coverage diagnostic\n\n"
        + markdown_table(
            [
                "dataset",
                "coverage",
                "accepted",
                "rejected",
                "accepted acc",
                "accepted risk",
                "median confidence/residual",
            ],
            risk_rows,
        )
        + "\nConfidence is margin divided by best residual. This is a selective-prediction diagnostic, not a new classifier.\n",
        encoding="utf-8",
    )
    unknown_ablation = _unknown_detector_ablation_rows(clean_risk_rows, rows, clean_marg_rows, rows_marg, cfg)
    (outputs_dir / "UNKNOWN_DETECTOR_ABLATION_TABLE.md").write_text(
        "# Exp08 P3 unknown/OOD detector ablation\n\n"
        + markdown_table(
            [
                "signal",
                "clean threshold",
                "clean false reject",
                "hidden reject",
                "accepted clean",
                "accepted hidden",
                "accepted clean acc",
                "accepted hidden acc",
            ],
            unknown_ablation,
        )
        + "\nThresholds target the configured clean false-reject rate on clean OOD rows. Hidden rows are never used to select thresholds.\n",
        encoding="utf-8",
    )
    unknown_safety = _unknown_safety_benchmark_rows(clean_risk_rows, rows, clean_marg_rows, rows_marg, cfg)
    (outputs_dir / "UNKNOWN_SAFETY_BENCHMARK.md").write_text(
        "# Exp08 P2 unknown-safety benchmark\n\n"
        + markdown_table(
            [
                "signal",
                "safety status",
                "clean false reject",
                "hidden reject",
                "accepted clean",
                "accepted hidden",
                "accepted clean acc",
                "accepted hidden acc",
            ],
            unknown_safety,
        )
        + "\nA usable screen must stay within the clean false-reject budget while rejecting many hidden mechanisms and preserving accepted-case accuracy. This is a safety diagnostic, not a deployed refusal policy.\n",
        encoding="utf-8",
    )
    accepted_hidden_risk = _unknown_accepted_hidden_risk_rows(unknown_ablation)
    (outputs_dir / "UNKNOWN_ACCEPTED_HIDDEN_RISK_TABLE.md").write_text(
        "# Exp08 P2 accepted-hidden risk endpoint\n\n"
        + markdown_table(
            [
                "signal",
                "risk status",
                "clean false reject",
                "hidden reject",
                "hidden accept rate",
                "accepted clean",
                "accepted hidden",
                "accepted clean acc",
                "accepted hidden acc",
                "accepted hidden risk",
            ],
            accepted_hidden_risk,
        )
        + "\nThe primary safety question is not only how many hidden mechanisms are rejected, but how risky the hidden mechanisms are after they are accepted. Thresholds are still selected from clean rows only.\n",
        encoding="utf-8",
    )
    unknown_risk_objective = _unknown_risk_objective_rows(unknown_ablation, cfg)
    (outputs_dir / "UNKNOWN_RISK_OBJECTIVE_TABLE.md").write_text(
        "# Exp08 P2 accepted-risk objective ranking\n\n"
        + markdown_table(
            [
                "signal",
                "objective status",
                "risk objective",
                "clean false reject",
                "hidden accept rate",
                "accepted hidden risk",
                "accepted clean acc",
                "accepted hidden acc",
            ],
            unknown_risk_objective,
        )
        + "\nRows rank fixed clean-thresholded unknown signals by accepted-hidden risk, hidden accept rate, and clean false-reject budget. Hidden rows are not used to choose thresholds; they only evaluate the frozen signals.\n",
        encoding="utf-8",
    )
    physical_names = {
        "evidence_entropy",
        "residual_gap_ambiguity",
        "h0_h1_score_ambiguity",
        "residual_score_disagreement",
        "combined_physical_unknown_score",
    }
    physical_unknown = [row for row in unknown_ablation if row[0] in physical_names]
    (outputs_dir / "UNKNOWN_PHYSICAL_EVIDENCE_ABLATION_TABLE.md").write_text(
        "# Exp08 P2 physical-evidence unknown/OOD ablation\n\n"
        + markdown_table(
            [
                "signal",
                "clean threshold",
                "clean false reject",
                "hidden reject",
                "accepted clean",
                "accepted hidden",
                "accepted clean acc",
                "accepted hidden acc",
            ],
            physical_unknown,
        )
        + "\nThese signals use model-evidence entropy, residual ambiguity, H0/H1 score ambiguity, and residual-vs-score disagreement. Thresholds are still clean-validation only.\n",
        encoding="utf-8",
    )
    h0_hard_rows = [
        _h0_hard_row("clean_ood_no_via", "base/default_score", _summary_for_evidence_mode(
            [r for r in clean_risk_rows if r["true_hypothesis"] == "H0_sheet_only"], labels, cfg, "default_score"
        )),
        _h0_hard_row("hidden_return_no_via", "base/default_score", _summary_for_evidence_mode(
            by_family.get("hidden_return_no_via", []), labels, cfg, "default_score"
        )),
    ]
    return {
        "n": len(records),
        "summary": summary_all,
        "via_marginalized_summary": summary_all_marg,
        "family_summaries": family_summaries,
        "via_marginalized_family_summaries": marg_family_summaries,
        "unknown_rejection": _unknown_summary(rows, unknown_thresholds),
        "risk_coverage": {
            "clean_ood": _selective_unknown_rows("clean_ood", clean_risk_rows),
            "hidden_all": _selective_unknown_rows("hidden_all", rows),
        },
        "unknown_detector_ablation": unknown_ablation,
        "unknown_safety_benchmark": unknown_safety,
        "unknown_accepted_hidden_risk": accepted_hidden_risk,
        "unknown_risk_objective": unknown_risk_objective,
        "unknown_physical_evidence_ablation": physical_unknown,
        "h0_hard_rows": h0_hard_rows,
        "n_failures": len(failures),
    }


def multistate_outputs(cfg: dict, records: List, rows_all: List[dict], complexity_penalty: float, outputs_dir: Path) -> dict:
    rng = np.random.default_rng(int(cfg["seed"]) + 909)
    base_records = [r for r in records if r.split == "ood"]
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    state1_by_id = {row["case_id"]: row for row in rows_all if row["split"] == "ood"}
    true = [rec.hypothesis_label for rec in base_records]
    single_pred = [state1_by_id[rec.case_id]["pred_hypothesis"] for rec in base_records]
    single_acc = hypothesis_accuracy(true, single_pred)
    single_pc = per_class_accuracy(true, single_pred)
    single_margins = np.asarray([float(state1_by_id[rec.case_id]["confidence_margin"]) for rec in base_records], dtype=float)
    policies = list(cfg.get("multistate", {}).get("design_policies", ["random_independent"]))
    design_summaries = {}
    rows = [[
        "single_state",
        len(true),
        fmt_float(single_acc),
        fmt_float(single_pc.get("H0_sheet_only", float("nan"))),
        fmt_float(single_pc.get("H1_sheet_via", float("nan"))),
        fmt_float(single_pc.get("H2_sheet_return", float("nan"))),
        fmt_float(single_pc.get("H3_sheet_artifact", float("nan"))),
        "",
    ]]
    for policy in policies:
        policy_rng = np.random.default_rng(int(cfg["seed"]) + 909 + 17 * (len(design_summaries) + 1))
        state2_records = [make_second_excitation_state(r, cfg, policy_rng, policy=policy) for r in base_records]
        state2_rows = evaluate_records(state2_records, obs_grid, cfg, complexity_penalty=complexity_penalty)
        joint_pred = []
        joint_margins = []
        joint_best_scores = []
        for rec, row2 in zip(base_records, state2_rows):
            row1 = state1_by_id[rec.case_id]
            pred = best_joint_hypothesis([row1["results"], row2["results"]])
            joint_pred.append(pred)
            score_map = joint_hypothesis_scores([row1["results"], row2["results"]])
            scores = sorted(score_map.values())
            joint_margins.append(float(scores[1] - scores[0]) if len(scores) > 1 else 0.0)
            joint_best_scores.append(float(min(score_map.values())))
        joint_acc = hypothesis_accuracy(true, joint_pred)
        joint_pc = per_class_accuracy(true, joint_pred)
        margin_gain = np.asarray(joint_margins, dtype=float) - single_margins
        label_free_utility = float(np.median(joint_margins) + 0.50 * np.median(margin_gain) - 0.10 * np.median(joint_best_scores))
        design_summaries[policy] = {
            "accuracy": joint_acc,
            "per_class_accuracy": joint_pc,
            "median_joint_margin": float(np.median(joint_margins)) if joint_margins else float("nan"),
            "median_margin_gain": float(np.median(margin_gain)) if len(margin_gain) else float("nan"),
            "median_joint_best_score": float(np.median(joint_best_scores)) if joint_best_scores else float("nan"),
            "label_free_utility": label_free_utility,
        }
        rows.append([
            f"joint_{policy}",
            len(true),
            fmt_float(joint_acc),
            fmt_float(joint_pc.get("H0_sheet_only", float("nan"))),
            fmt_float(joint_pc.get("H1_sheet_via", float("nan"))),
            fmt_float(joint_pc.get("H2_sheet_return", float("nan"))),
            fmt_float(joint_pc.get("H3_sheet_artifact", float("nan"))),
            fmt_float(design_summaries[policy]["median_joint_margin"]),
        ])
    best_policy = max(design_summaries.items(), key=lambda item: (item[1]["accuracy"], item[1]["median_joint_margin"]))[0]
    (outputs_dir / "MULTISTATE_DESIGN_TABLE.md").write_text(
        "# Exp08 P3-next synthetic multi-state design scan\n\n"
        + markdown_table(["method", "n", "4-way acc", "H0 acc", "H1 acc", "H2 acc", "H3 acc", "median joint margin"], rows)
        + "\nSecond excitation is synthetic and generated from the same graph; this is not active-measurement data.\n",
        encoding="utf-8",
    )
    utility_rows = []
    for policy, summary in sorted(design_summaries.items(), key=lambda item: item[1]["label_free_utility"], reverse=True):
        utility_rows.append([
            policy,
            fmt_float(summary["label_free_utility"]),
            fmt_float(summary["accuracy"]),
            fmt_float(summary["per_class_accuracy"].get("H0_sheet_only", float("nan"))),
            fmt_float(summary["median_joint_margin"]),
            fmt_float(summary["median_margin_gain"]),
            fmt_float(summary["median_joint_best_score"]),
        ])
    best_utility_policy = utility_rows[0][0] if utility_rows else ""
    (outputs_dir / "MULTISTATE_EXPERIMENTAL_DESIGN_TABLE.md").write_text(
        "# Exp08 P3 active-measurement design utility diagnostic\n\n"
        + markdown_table(
            [
                "policy",
                "label-free utility",
                "4-way acc",
                "H0 acc",
                "median joint margin",
                "median margin gain",
                "median joint best score",
            ],
            utility_rows,
        )
        + f"\nBest label-free synthetic policy: `{best_utility_policy}`. The utility uses margins and residual scores, not labels, but evaluation columns are reported for audit.\n",
        encoding="utf-8",
    )
    (outputs_dir / "ACTIVE_DESIGN_OBJECTIVE_TABLE.md").write_text(
        "# Exp08 P4 active-design objective table\n\n"
        + markdown_table(
            [
                "policy",
                "label-free utility",
                "4-way acc",
                "H0 acc",
                "median joint margin",
                "median margin gain",
                "median joint best score",
            ],
            utility_rows,
        )
        + "\nThe objective is a synthetic proxy for expected evidence separation. It does not include real port, voltage, heating, or return-network constraints.\n",
        encoding="utf-8",
    )
    constraint_rows = []
    for policy, summary in sorted(design_summaries.items(), key=lambda item: item[1]["label_free_utility"], reverse=True):
        constraint_rows.append([
            policy,
            _active_policy_constraint_status(policy, summary, cfg),
            fmt_float(summary["label_free_utility"]),
            fmt_float(summary["accuracy"]),
            fmt_float(summary["per_class_accuracy"].get("H0_sheet_only", float("nan"))),
            fmt_float(summary["median_joint_margin"]),
            fmt_float(summary["median_margin_gain"]),
            fmt_float(summary["median_joint_best_score"]),
        ])
    (outputs_dir / "ACTIVE_DESIGN_CONSTRAINT_TABLE.md").write_text(
        "# Exp08 P4 constrained active-design audit\n\n"
        + markdown_table(
            [
                "policy",
                "constraint status",
                "label-free utility",
                "4-way acc",
                "H0 acc",
                "median joint margin",
                "median margin gain",
                "median joint best score",
            ],
            constraint_rows,
        )
        + "\nThe constraints are synthetic feasibility screens for current gain, sheet-current perturbation, and allowed excitation families. They do not represent real hardware limits yet.\n",
        encoding="utf-8",
    )
    # Keep the original table name as the concise headline artifact.
    headline = [
        rows[0][:-1],
        [f"joint_{best_policy}", len(true), fmt_float(design_summaries[best_policy]["accuracy"]),
         fmt_float(design_summaries[best_policy]["per_class_accuracy"].get("H0_sheet_only", float("nan"))),
         fmt_float(design_summaries[best_policy]["per_class_accuracy"].get("H1_sheet_via", float("nan"))),
         fmt_float(design_summaries[best_policy]["per_class_accuracy"].get("H2_sheet_return", float("nan"))),
         fmt_float(design_summaries[best_policy]["per_class_accuracy"].get("H3_sheet_artifact", float("nan")))],
    ]
    (outputs_dir / "MULTISTATE_IDENTIFICATION_TABLE.md").write_text(
        "# Exp08 synthetic two-state identification\n\n"
        + markdown_table(["method", "n", "4-way acc", "H0 acc", "H1 acc", "H2 acc", "H3 acc"], headline)
        + f"\nBest synthetic design policy: `{best_policy}`.\n",
        encoding="utf-8",
    )
    return {
        "n": len(true),
        "single_state_accuracy": single_acc,
        "joint_two_state_accuracy": design_summaries[best_policy]["accuracy"],
        "single_state_per_class_accuracy": single_pc,
        "joint_two_state_per_class_accuracy": design_summaries[best_policy]["per_class_accuracy"],
        "median_joint_margin": design_summaries[best_policy]["median_joint_margin"],
        "best_policy": best_policy,
        "best_label_free_policy": best_utility_policy,
        "design_summaries": design_summaries,
        "active_constraint_rows": constraint_rows,
    }


def _record_segments(record) -> list:
    return (
        list(record.sheet_segments)
        + list(record.via_candidates)
        + list(record.return_candidates)
        + list(record.artifact_candidates)
    )


def _registration_stress_record(record, cfg: dict, obs_grid: np.ndarray, transform: dict, suffix: str):
    transformed_segments = []
    transformed_currents: Dict[str, float] = {}
    rotation_rad = np.deg2rad(float(transform.get("rotation_deg", 0.0)))
    for seg in _record_segments(record):
        trans = transform_segment_xy(
            seg,
            dx=float(transform.get("dx_m", 0.0)),
            dy=float(transform.get("dy_m", 0.0)),
            rotation_rad=rotation_rad,
            scale=float(transform.get("scale", 1.0)),
        )
        transformed_segments.append(trans)
        transformed_currents[trans.name] = float(record.truth_currents.get(seg.name, 0.0))
    b_clean = field_from_segments(
        transformed_segments,
        transformed_currents,
        obs_grid,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )
    metadata = dict(record.metadata)
    metadata.update({"registration_stress": dict(transform), "claim_boundary": "Synthetic registration stress only."})
    return replace(
        record,
        case_id=f"{record.case_id}__reg_{suffix}",
        split="registration_stress",
        b_clean=b_clean,
        b_obs=b_clean,
        metadata=metadata,
    )


def registration_stress_outputs(
    cfg: dict,
    records: List,
    complexity_penalty: float,
    threshold: float,
    global_threshold: float,
    global_transforms: list[dict],
    outputs_dir: Path,
) -> dict:
    labels = list(cfg["scoring"]["hypotheses"])
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    cfg_reg = cfg.get("registration_stress", {})
    n_per_class = int(cfg_reg.get("n_per_class", 8))
    by_class: dict[str, list] = defaultdict(list)
    for rec in records:
        if rec.split == "ood" and len(by_class[rec.class_label]) < n_per_class:
            by_class[rec.class_label].append(rec)
    base_records = [rec for cls in sorted(by_class) for rec in by_class[cls]]
    stress_specs = [{"name": "identity", "dx_m": 0.0, "dy_m": 0.0, "rotation_deg": 0.0, "scale": 1.0}]
    for um in cfg_reg.get("translation_um", []):
        if float(um) != 0.0:
            stress_specs.append({"name": f"translation_{float(um):.0f}um", "dx_m": float(um) * 1e-6, "dy_m": 0.0, "rotation_deg": 0.0, "scale": 1.0})
    for deg in cfg_reg.get("rotation_deg", []):
        stress_specs.append({"name": f"rotation_{float(deg):.1f}deg", "dx_m": 0.0, "dy_m": 0.0, "rotation_deg": float(deg), "scale": 1.0})
    for delta in cfg_reg.get("scale_delta", []):
        stress_specs.append({"name": f"scale_{float(delta):.3f}", "dx_m": 0.0, "dy_m": 0.0, "rotation_deg": 0.0, "scale": 1.0 + float(delta)})
    for um in cfg_reg.get("standoff_um", []):
        stress_specs.append({
            "name": f"standoff_{float(um):.0f}um",
            "dx_m": 0.0,
            "dy_m": 0.0,
            "rotation_deg": 0.0,
            "scale": 1.0,
            "obs_z_shift_m": float(um) * 1e-6,
        })
    for mrad in cfg_reg.get("tilt_mrad", []):
        stress_specs.append({
            "name": f"tilt_{float(mrad):.0f}mrad",
            "dx_m": 0.0,
            "dy_m": 0.0,
            "rotation_deg": 0.0,
            "scale": 1.0,
            "tilt_x_mrad": float(mrad),
        })

    table_rows = []
    summaries = {}
    for spec in stress_specs:
        stress_obs_grid = np.array(obs_grid, copy=True)
        if "obs_z_shift_m" in spec:
            stress_obs_grid[..., 2] += float(spec["obs_z_shift_m"])
        if "tilt_x_mrad" in spec:
            stress_obs_grid[..., 2] += float(spec["tilt_x_mrad"]) * 1e-3 * stress_obs_grid[..., 0]
        stressed = [_registration_stress_record(rec, cfg, stress_obs_grid, spec, str(spec["name"])) for rec in base_records]
        rows_base = evaluate_records(stressed, obs_grid, cfg, complexity_penalty=complexity_penalty)
        rows_global = _evaluate_global_registration_records(stressed, obs_grid, cfg, complexity_penalty, global_transforms)
        base_summary = _summary_for_rows(rows_base, labels, threshold)
        global_summary = _summary_for_rows(rows_global, labels, global_threshold)
        summaries[spec["name"]] = {"base": base_summary, "global": global_summary}
        for mode, summary in [("base", base_summary), ("global_registered", global_summary)]:
            pc = summary["per_class_accuracy"]
            table_rows.append([
                spec["name"],
                mode,
                int(summary["n"]),
                fmt_float(summary["accuracy"]),
                fmt_float(pc.get("H0_sheet_only", float("nan"))),
                fmt_float(pc.get("H1_sheet_via", float("nan"))),
                fmt_float(pc.get("H2_sheet_return", float("nan"))),
                fmt_float(pc.get("H3_sheet_artifact", float("nan"))),
                fmt_float(summary["via_detection"]["false_positive_rate"]),
                fmt_float(summary["median_best_residual_rel_l2"]),
            ])
    (outputs_dir / "REGISTRATION_STRESS_CURVE.md").write_text(
        "# Exp08 P5 synthetic registration stress curve\n\n"
        + markdown_table(
            [
                "stress",
                "mode",
                "n",
                "4-way acc",
                "H0 acc",
                "H1 acc",
                "H2 acc",
                "H3 acc",
                "no-via FP",
                "median residual",
            ],
            table_rows,
        )
        + "\nThe stressed observation field is generated from transformed graph geometry while the scorer sees the original graph. This is a synthetic registration sensitivity curve, not real CAD alignment.\n",
        encoding="utf-8",
    )
    return {"n": len(base_records), "summaries": summaries}


def write_outputs(cfg, records, rows_all, complexity_penalty, via_thresholds, outputs_dir, data_dir) -> dict:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    if cfg["artifacts"].get("write_dataset_npz", True) or cfg["artifacts"].get("write_case_jsonl", True):
        write_dataset_artifacts(records, data_dir)

    labels = list(cfg["scoring"]["hypotheses"])
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    reg_cfg = cfg.get("registration_search", {})
    via_offsets = offset_grid(
        radius_m=float(reg_cfg.get("via_offset_radius_m", 0.0)),
        n_side=int(reg_cfg.get("via_offset_grid_n", 1)),
    )
    glob_cfg = cfg.get("global_registration", {})
    global_transforms = transform_grid(
        translation_radius_m=float(glob_cfg.get("translation_radius_m", 0.0)),
        rotation_degrees=list(glob_cfg.get("rotation_degrees", [0.0])),
        scales=list(glob_cfg.get("scales", [1.0])),
    )
    rows_val = split_rows(rows_all, "val")
    val_records = [r for r in records if r.split == "val"]
    rows_val_marg = _evaluate_via_marginalized_records(val_records, obs_grid, cfg, complexity_penalty, via_offsets)
    y_val_marg = [1 if r["class_label"] == "true_via" else 0 for r in rows_val_marg]
    score_val_marg = [float(r["via_evidence"]) for r in rows_val_marg]
    marginal_threshold, marginal_metrics = select_threshold_with_fp_cap(
        y_val_marg,
        score_val_marg,
        max_fp_rate=float(cfg["scoring"]["max_allowed_no_via_fp_for_threshold_selection"]),
    )
    via_thresholds["graph_h1_h0_via_location_marginalized"] = float(marginal_threshold)
    rows_val_global = _evaluate_global_registration_records(val_records, obs_grid, cfg, complexity_penalty, global_transforms)
    y_val_global = [1 if r["class_label"] == "true_via" else 0 for r in rows_val_global]
    score_val_global = [float(r["via_evidence"]) for r in rows_val_global]
    global_threshold, global_metrics = select_threshold_with_fp_cap(
        y_val_global,
        score_val_global,
        max_fp_rate=float(cfg["scoring"]["max_allowed_no_via_fp_for_threshold_selection"]),
    )
    via_thresholds["graph_h1_h0_global_registered"] = float(global_threshold)
    unknown_thresholds = _unknown_thresholds(rows_val, cfg)
    metrics = {
        "experiment_name": cfg["experiment_name"],
        "seed": int(cfg["seed"]),
        "selected_complexity_penalty": float(complexity_penalty),
        "selected_thresholds": via_thresholds,
        "selected_unknown_rejection_thresholds": unknown_thresholds,
        "registration_search": {
            "n_offsets": len(via_offsets),
            "via_offset_radius_m": float(reg_cfg.get("via_offset_radius_m", 0.0)),
            "via_offset_grid_n": int(reg_cfg.get("via_offset_grid_n", 1)),
            "validation_marginalized_threshold_metrics": marginal_metrics,
        },
        "global_registration": {
            "n_transforms": len(global_transforms),
            "translation_radius_m": float(glob_cfg.get("translation_radius_m", 0.0)),
            "rotation_degrees": list(glob_cfg.get("rotation_degrees", [0.0])),
            "scales": list(glob_cfg.get("scales", [1.0])),
            "validation_global_threshold_metrics": global_metrics,
        },
        "dataset": {
            "n_cases": len(records),
            "splits": {s: sum(1 for r in records if r.split == s) for s in ["val", "test", "ood"]},
            "classes": {c: sum(1 for r in records if r.class_label == c) for c in cfg["dataset"]["classes"]},
        },
        "hypothesis_identification": {},
        "via_detection": {},
        "acceptance_gates": {},
    }

    for split in ["val", "test", "ood"]:
        split_r = split_rows(rows_all, split)
        metrics["hypothesis_identification"][split] = summarize_hypothesis(split_r, labels)
        metrics["via_detection"].setdefault("graph_h1_h0", {})[split] = via_eval(
            split_r, via_thresholds["graph_h1_h0"], "via_evidence"
        )
        metrics["via_detection"].setdefault("raw_template", {})[split] = via_eval(
            split_r, via_thresholds["raw_template"], "raw_via_score"
        )
        metrics["via_detection"].setdefault("sheet_residual_template", {})[split] = via_eval(
            split_r, via_thresholds["sheet_residual_template"], "sheet_residual_via_score"
        )

    metrics["pypeec_graph_bridge"] = pypeec_bridge_outputs(
        cfg,
        complexity_penalty,
        via_thresholds["graph_h1_h0"],
        via_thresholds["graph_h1_h0_via_location_marginalized"],
        via_thresholds["graph_h1_h0_global_registered"],
        via_offsets,
        global_transforms,
        outputs_dir,
    )
    metrics["hidden_mechanism_stress"] = hidden_stress_outputs(
        cfg,
        complexity_penalty,
        via_thresholds["graph_h1_h0"],
        via_thresholds["graph_h1_h0_via_location_marginalized"],
        via_offsets,
        unknown_thresholds,
        split_rows(rows_all, "ood"),
        outputs_dir,
    )
    metrics["multistate_identification"] = multistate_outputs(
        cfg, records, rows_all, complexity_penalty, outputs_dir
    )
    metrics["registration_stress_curve"] = registration_stress_outputs(
        cfg,
        records,
        complexity_penalty,
        via_thresholds["graph_h1_h0"],
        via_thresholds["graph_h1_h0_global_registered"],
        global_transforms,
        outputs_dir,
    )
    h0_hard_rows = []
    h0_hard_rows += metrics["pypeec_graph_bridge"].get("h0_hard_rows", [])
    h0_hard_rows += metrics["hidden_mechanism_stress"].get("h0_hard_rows", [])
    (outputs_dir / "H0_HARD_NEGATIVE_TABLE.md").write_text(
        "# Exp08 P1 H0/no-via hard-negative diagnostic\n\n"
        + markdown_table(
            [
                "dataset",
                "mode",
                "n",
                "H0 acc",
                "false H1 rate",
                "false H2 rate",
                "false H3 rate",
                "4-way acc",
                "median residual",
            ],
            h0_hard_rows,
        )
        + "\nH0/no-via is the hard negative class: a reliable system must avoid explaining every residual as via, return, or artifact.\n",
        encoding="utf-8",
    )
    metrics["h0_hard_negative"] = {"rows": h0_hard_rows}

    # Scientific gates: designed to prevent a polished but non-informative experiment.
    test_graph = metrics["via_detection"]["graph_h1_h0"]["test"]
    test_raw = metrics["via_detection"]["raw_template"]["test"]
    test_resid = metrics["via_detection"]["sheet_residual_template"]["test"]
    test_hyp = metrics["hypothesis_identification"]["test"]
    ood_graph = metrics["via_detection"]["graph_h1_h0"]["ood"]
    ood_resid = metrics["via_detection"]["sheet_residual_template"]["ood"]
    ood_hyp = metrics["hypothesis_identification"]["ood"]
    ood_pc = ood_hyp["per_class_accuracy"]
    bridge = metrics["pypeec_graph_bridge"]
    bridge_center = bridge.get("summaries", {}).get("B_centerline", {})
    bridge_pypeec = bridge.get("summaries", {}).get("B_pypeec", {})
    bridge_pypeec_basis = bridge.get("summaries", {}).get("B_pypeec_basis_combined_pypeec_aware", {})
    bridge_pypeec_global = bridge.get("summaries", {}).get("B_pypeec_global_registered", {})
    hidden = metrics["hidden_mechanism_stress"]
    hidden_summary = hidden["summary"]
    hidden_marg = hidden["via_marginalized_summary"]
    hidden_unknown = hidden["unknown_rejection"]
    shifted_base = hidden["family_summaries"].get("shifted_true_via", {})
    shifted_marg = hidden.get("via_marginalized_family_summaries", {}).get("shifted_true_via", {})
    multistate = metrics["multistate_identification"]
    h0_hard = metrics["h0_hard_negative"]
    reg_stress = metrics["registration_stress_curve"]
    metrics["acceptance_gates"] = {
        "graph_hypothesis_accuracy_above_random_4way": test_hyp["accuracy"] > 0.35,
        "graph_test_accuracy_is_high": test_hyp["accuracy"] >= 0.80,
        "graph_ood_accuracy_is_material": ood_hyp["accuracy"] >= 0.70,
        "graph_ood_no_via_accuracy_is_material": ood_pc.get("H0_sheet_only", 0.0) >= 0.60,
        "graph_ood_true_via_accuracy_is_material": ood_pc.get("H1_sheet_via", 0.0) >= 0.70,
        "graph_ood_return_path_accuracy_is_material": ood_pc.get("H2_sheet_return", 0.0) >= 0.80,
        "graph_auc_not_worse_than_raw_template": test_graph["auc"] >= test_raw["auc"] - 1e-9,
        "graph_ood_auc_not_worse_than_residual_template": ood_graph["auc"] >= ood_resid["auc"] - 1e-9,
        "graph_no_via_fp_below_raw_template": test_graph["false_positive_rate"] <= test_raw["false_positive_rate"] + 1e-9,
        "graph_ood_no_via_fp_below_residual_template": ood_graph["false_positive_rate"] <= ood_resid["false_positive_rate"] + 1e-9,
        "graph_selective_accuracy_20pct_above_full_accuracy": test_hyp["selective_risk"]["accuracy_at_20pct_coverage"] >= test_hyp["accuracy"],
        "graph_ood_selective_accuracy_20pct_above_full_accuracy": ood_hyp["selective_risk"]["accuracy_at_20pct_coverage"] >= ood_hyp["accuracy"],
        "residual_baseline_reported_not_hidden": "sheet_residual_template" in metrics["via_detection"],
        "pypeec_graph_bridge_available": bool(bridge.get("available", False)),
        "pypeec_centerline_bridge_accuracy_is_high": bridge_center.get("accuracy", 0.0) >= 0.95,
        "pypeec_bridge_exposes_solver_gap": bridge_center.get("accuracy", 0.0) - bridge_pypeec.get("accuracy", 0.0) >= 0.10,
        "pypeec_bridge_via_auc_is_material": bridge_pypeec.get("via_detection", {}).get("auc", 0.0) >= 0.85,
        "hidden_mechanism_stress_is_evaluated": hidden.get("n", 0) > 0,
        "hidden_mechanism_is_nontrivial": hidden_summary.get("accuracy", 1.0) < 0.98,
        "hidden_selective_accuracy_not_worse_than_full": hidden_summary["selective_risk"]["accuracy_at_20pct_coverage"] >= hidden_summary["accuracy"],
        "via_location_marginalization_is_evaluated": "B_pypeec_via_marginalized" in bridge.get("summaries", {}),
        "via_location_marginalization_improves_shifted_via": shifted_marg.get("per_class_accuracy", {}).get("H1_sheet_via", 0.0)
        >= shifted_base.get("per_class_accuracy", {}).get("H1_sheet_via", 0.0),
        "pypeec_aware_basis_bank_is_evaluated": bool(bridge_pypeec_basis),
        "pypeec_aware_basis_residual_not_worse_than_base": bridge_pypeec_basis.get("median_best_residual_rel_l2", float("inf"))
        <= bridge_pypeec.get("median_best_residual_rel_l2", float("inf")) + 1e-9,
        "model_selection_calibration_is_evaluated": bool(bridge.get("model_selection_calibration_rows")),
        "pypeec_heldout_model_selection_is_evaluated": bool(bridge.get("pypeec_heldout_model_selection_rows")),
        "h0_h1_tradeoff_curve_is_evaluated": bool(bridge.get("h0_h1_tradeoff_rows")),
        "pypeec_model_selection_stability_is_evaluated": bool(bridge.get("pypeec_model_selection_stability_rows")),
        "pypeec_class_specific_selective_is_evaluated": bool(bridge.get("pypeec_class_specific_selective_rows")),
        "pypeec_stacked_evidence_calibrator_is_evaluated": bool(bridge.get("pypeec_stacked_evidence_calibrator_rows")),
        "pypeec_stacked_group_heldout_is_evaluated": bool(bridge.get("pypeec_stacked_evidence_group_heldout_rows")),
        "pypeec_stacked_group_distance_refusal_is_evaluated": bool(
            bridge.get("pypeec_stacked_evidence_group_distance_refusal_rows")
        ),
        "pypeec_family_fewshot_adaptation_is_evaluated": bool(bridge.get("pypeec_family_fewshot_adaptation_rows")),
        "stacked_evidence_feature_ablation_is_evaluated": bool(bridge.get("stacked_evidence_feature_ablation_rows")),
        "stacked_evidence_unknown_safety_is_evaluated": bool(bridge.get("stacked_evidence_unknown_safety_rows")),
        "stacked_evidence_distance_ood_is_evaluated": any(
            "feature_distance" in str(row[0]) for row in bridge.get("stacked_evidence_unknown_safety_rows", [])
        ),
        "stacked_evidence_near_boundary_hidden_is_evaluated": bool(
            bridge.get("stacked_evidence_near_boundary_hidden_rows")
        ),
        "stacked_evidence_near_hidden_severity_is_evaluated": bool(
            bridge.get("stacked_evidence_near_hidden_severity_rows")
        ),
        "near_hidden_accepted_cases_are_audited": bool(bridge.get("near_hidden_accepted_case_rows")),
        "stacked_evidence_space_diagnostics_are_evaluated": bool(
            bridge.get("stacked_evidence_space_diagnostic_rows")
        )
        and (outputs_dir / "stacked_evidence_space_pca.png").exists(),
        "pypeec_stacked_external_stress_is_evaluated": bool(bridge.get("pypeec_stacked_evidence_external_stress_rows")),
        "stacked_evidence_selective_risk_is_evaluated": bool(bridge.get("stacked_evidence_selective_risk_rows")),
        "pypeec_distribution_gap_is_evaluated": bool(bridge.get("pypeec_distribution_gap_rows")),
        "disciplined_model_bank_is_documented": (outputs_dir / "PYPEEC_MODEL_BANK_ALLOWED_BASIS_TABLE.md").exists(),
        "global_registration_search_is_evaluated": bool(bridge_pypeec_global),
        "unknown_rejection_catches_hidden_mechanisms": hidden_unknown.get("unknown_rate", 0.0) >= 0.50,
        "unknown_risk_coverage_is_evaluated": bool(hidden.get("risk_coverage", {}).get("hidden_all")),
        "unknown_detector_ablation_is_evaluated": bool(hidden.get("unknown_detector_ablation")),
        "unknown_safety_benchmark_is_evaluated": bool(hidden.get("unknown_safety_benchmark")),
        "unknown_accepted_hidden_risk_is_evaluated": bool(hidden.get("unknown_accepted_hidden_risk")),
        "unknown_risk_objective_is_evaluated": bool(hidden.get("unknown_risk_objective")),
        "unknown_physical_evidence_ablation_is_evaluated": bool(hidden.get("unknown_physical_evidence_ablation")),
        "h0_hard_negatives_are_evaluated": bool(h0_hard.get("rows")),
        "multistate_identification_is_evaluated": multistate.get("n", 0) > 0,
        "multistate_joint_not_worse_than_single": multistate["joint_two_state_accuracy"] >= multistate["single_state_accuracy"] - 1e-9,
        "multistate_design_scan_is_evaluated": len(multistate.get("design_summaries", {})) >= 2,
        "multistate_label_free_design_is_evaluated": bool(multistate.get("best_label_free_policy")),
        "active_design_objective_is_evaluated": (outputs_dir / "ACTIVE_DESIGN_OBJECTIVE_TABLE.md").exists(),
        "active_design_constraints_are_evaluated": bool(multistate.get("active_constraint_rows")),
        "registration_stress_curve_is_evaluated": bool(reg_stress.get("summaries")),
        "registration_standoff_tilt_stress_is_evaluated": "standoff_15um" in reg_stress.get("summaries", {})
        and "tilt_10mrad" in reg_stress.get("summaries", {}),
        "all_scientific_gates_passed": False,
    }
    metrics["acceptance_gates"]["all_scientific_gates_passed"] = all(
        bool(v) for k, v in metrics["acceptance_gates"].items() if k != "all_scientific_gates_passed"
    )

    write_json(outputs_dir / "metrics.json", metrics)

    # Tables.
    h_rows = []
    for split in ["val", "test", "ood"]:
        h = metrics["hypothesis_identification"][split]
        h_rows.append([
            split,
            fmt_float(h["accuracy"]),
            fmt_float(h["median_best_residual_rel_l2"]),
            fmt_float(h["selective_risk"]["accuracy_at_20pct_coverage"]),
            fmt_float(h["selective_risk"]["accuracy_at_50pct_coverage"]),
        ])
    (outputs_dir / "HYPOTHESIS_IDENTIFICATION_TABLE.md").write_text(
        markdown_table(
            ["split", "4-way accuracy", "median best residual L2", "acc@20% coverage", "acc@50% coverage"],
            h_rows,
        ),
        encoding="utf-8",
    )

    (outputs_dir / "HYPOTHESIS_PER_CLASS_TABLE.md").write_text(
        markdown_table(["split", "true hypothesis", "accuracy"], per_class_rows(metrics)),
        encoding="utf-8",
    )

    (outputs_dir / "SELECTIVE_RISK_TABLE.md").write_text(
        markdown_table(["split", "coverage", "selected", "accuracy", "risk"], selective_rows(metrics)),
        encoding="utf-8",
    )

    v_rows = []
    for method in ["raw_template", "sheet_residual_template", "graph_h1_h0"]:
        for split in ["val", "test", "ood"]:
            m = metrics["via_detection"][method][split]
            v_rows.append([
                method,
                split,
                fmt_float(m["auc"]),
                fmt_float(m["precision"]),
                fmt_float(m["recall"]),
                fmt_float(m["f1"]),
                fmt_float(m["false_positive_rate"]),
                fmt_float(m["threshold"]),
            ])
    (outputs_dir / "VIA_HYPOTHESIS_TEST_TABLE.md").write_text(
        markdown_table(
            ["method", "split", "AUC", "precision", "recall", "F1", "no-via FP rate", "threshold"],
            v_rows,
        ),
        encoding="utf-8",
    )

    failure_table_rows = failure_rows(rows_all)
    (outputs_dir / "FAILURE_CASES_TABLE.md").write_text(
        markdown_table(
            [
                "split",
                "case",
                "class",
                "true H",
                "pred H",
                "margin",
                "via evidence",
                "true residual",
                "pred residual",
                "raw via score",
                "sheet-residual score",
            ],
            failure_table_rows[:80],
        ) + f"\n\nTotal misclassified cases: `{len(failure_table_rows)}`.\n",
        encoding="utf-8",
    )

    # Plots.
    if cfg["artifacts"].get("write_figures", True):
        for split in ["test", "ood"]:
            split_r = split_rows(rows_all, split)
            cm = np.asarray(metrics["hypothesis_identification"][split]["confusion_matrix"])
            save_confusion_matrix(outputs_dir / f"{split}_hypothesis_confusion.png", cm, labels, f"Exp08 {split} hypothesis confusion")
            pos = [r["via_evidence"] for r in split_r if r["class_label"] == "true_via"]
            neg = [r["via_evidence"] for r in split_r if r["class_label"] != "true_via"]
            save_score_histogram(outputs_dir / f"{split}_via_evidence_hist.png", pos, neg, via_thresholds["graph_h1_h0"], f"Exp08 {split} graph H1/H0 evidence")
        # Save one representative failure/ambiguity and one true-via success.
        examples = []
        for desired in ["true_via", "return_path", "no_via"]:
            for row in rows_all:
                if row["split"] == "test" and row["class_label"] == desired:
                    examples.append(row)
                    break
        for row in examples:
            save_example_case(outputs_dir / f"example_{row['class_label']}.png", row["record"], row["results"])

    # RUN_REPORT.
    report = f"""# Exp08 Run Report — Graph-guided Magnetic System Identification

## Purpose

Exp08 is the first-stage successor to the pixel-map inverse pipeline. It tests whether a synthetic graph/CAD-like candidate space and explicit H0/H1/H2/H3 hypothesis scoring can reduce the false confidence of via detection under no-via, return-path, and bend/artifact ambiguity.

This experiment is self-contained and synthetic. It is not a real QDM/CAD/PyPEEC validation. Its role is to establish the code path, metrics, and scientific gates for the next graph-guided stage.

## Frozen protocol

- Random seed: `{cfg['seed']}`
- Grid: `{cfg['grid']['n']} × {cfg['grid']['n']}` over `{cfg['grid']['fov_m']} m` FOV
- Classes: `{', '.join(cfg['dataset']['classes'])}`
- Hypotheses: `{', '.join(labels)}`
- Selected complexity penalty from validation split: `{complexity_penalty}`
- Via H1/H0 threshold selected only on validation split: `{via_thresholds['graph_h1_h0']}`

## Main results

### Hypothesis identification

{(outputs_dir / 'HYPOTHESIS_IDENTIFICATION_TABLE.md').read_text(encoding='utf-8')}

### Per-class hypothesis accuracy

{(outputs_dir / 'HYPOTHESIS_PER_CLASS_TABLE.md').read_text(encoding='utf-8')}

### Selective risk / refusal

{(outputs_dir / 'SELECTIVE_RISK_TABLE.md').read_text(encoding='utf-8')}

### Via hypothesis test

{(outputs_dir / 'VIA_HYPOTHESIS_TEST_TABLE.md').read_text(encoding='utf-8')}

### Misclassified cases

{(outputs_dir / 'FAILURE_CASES_TABLE.md').read_text(encoding='utf-8')}

### P0: exp07 PyPEEC graph bridge

{(outputs_dir / 'PYPEEC_GRAPH_BRIDGE_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_GRAPH_BRIDGE_FAILURE_CASES.md').read_text(encoding='utf-8')}

### P0: PyPEEC-aware basis bank

{(outputs_dir / 'PYPEEC_AWARE_BASIS_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'MODEL_EVIDENCE_SELECTION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_MODEL_BANK_EVIDENCE_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'MODEL_SELECTION_CALIBRATION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_MODEL_BANK_ALLOWED_BASIS_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_HELDOUT_SPLIT_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_HELDOUT_MODEL_SELECTION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'H0_H1_MODEL_SELECTION_TRADEOFF_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_MODEL_SELECTION_STABILITY_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_CLASS_SPECIFIC_SELECTIVE_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_STACKED_EVIDENCE_CALIBRATOR_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_STACKED_EVIDENCE_GROUP_HELDOUT_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_STACKED_EVIDENCE_GROUP_DISTANCE_REFUSAL_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_FAMILY_FEWSHOT_ADAPTATION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'STACKED_EVIDENCE_FEATURE_ABLATION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'STACKED_EVIDENCE_UNKNOWN_SAFETY_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'STACKED_EVIDENCE_NEAR_BOUNDARY_HIDDEN_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'STACKED_EVIDENCE_NEAR_HIDDEN_SEVERITY_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'NEAR_HIDDEN_ACCEPTED_CASES.md').read_text(encoding='utf-8')}

{(outputs_dir / 'STACKED_EVIDENCE_SPACE_DIAGNOSTICS_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_STACKED_EVIDENCE_EXTERNAL_STRESS_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'STACKED_EVIDENCE_SELECTIVE_RISK_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_DISTRIBUTION_GAP_TABLE.md').read_text(encoding='utf-8')}

### P1: H0/no-via hard negatives

{(outputs_dir / 'H0_HARD_NEGATIVE_TABLE.md').read_text(encoding='utf-8')}

### P0-next/P1-next: registration marginalization

{(outputs_dir / 'PYPEEC_BRIDGE_REGISTRATION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'PYPEEC_BRIDGE_GLOBAL_REGISTRATION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'REGISTRATION_MARGINALIZATION_TABLE.md').read_text(encoding='utf-8')}

### P1: hidden-mechanism OOD stress

{(outputs_dir / 'HIDDEN_MECHANISM_STRESS_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'HIDDEN_MECHANISM_FAILURE_CASES.md').read_text(encoding='utf-8')}

### P2-next: unknown / out-of-library rejection

{(outputs_dir / 'UNKNOWN_REJECTION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'UNKNOWN_RISK_COVERAGE_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'UNKNOWN_DETECTOR_ABLATION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'UNKNOWN_SAFETY_BENCHMARK.md').read_text(encoding='utf-8')}

{(outputs_dir / 'UNKNOWN_ACCEPTED_HIDDEN_RISK_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'UNKNOWN_RISK_OBJECTIVE_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'UNKNOWN_PHYSICAL_EVIDENCE_ABLATION_TABLE.md').read_text(encoding='utf-8')}

### P3: synthetic two-state identification

{(outputs_dir / 'MULTISTATE_IDENTIFICATION_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'MULTISTATE_DESIGN_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'MULTISTATE_EXPERIMENTAL_DESIGN_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'ACTIVE_DESIGN_OBJECTIVE_TABLE.md').read_text(encoding='utf-8')}

{(outputs_dir / 'ACTIVE_DESIGN_CONSTRAINT_TABLE.md').read_text(encoding='utf-8')}

### P5: synthetic registration stress curve

{(outputs_dir / 'REGISTRATION_STRESS_CURVE.md').read_text(encoding='utf-8')}

## Scientific gates

{markdown_table(['gate', 'passed'], [[k, v] for k, v in metrics['acceptance_gates'].items()])}

## Interpretation

- The graph scorer is not another pixel-threshold detector. It compares explicit physical explanations: sheet-only, sheet+via, sheet+return, and sheet+artifact.
- The raw template and sheet-residual template are intentionally kept as baselines to prevent the graph method from hiding behind polished metrics.
- The exp07 bridge intentionally tests the same graph scorer on real PyPEEC fields. Centerline bridge performance is expected to be easier; a PyPEEC drop is evidence of solver/operator mismatch, not a failed run.
- Hidden-mechanism rows deliberately put some true field components outside the hypothesis library. They are designed to expose ambiguity and selective-risk behavior, not to inflate accuracy.
- The two-state table is a synthetic active-measurement prototype. It validates the joint-scoring code path, not real multi-excitation hardware.
- Via-location marginalization is a registration-uncertainty diagnostic. It is useful only if it improves shifted/bridge behavior without hiding false-positive trade-offs.
- The PyPEEC-aware basis-bank table tests whether finite-width, return-bank, artifact-bank, distributed-via, or combined graph bases reduce solver residuals. It is not a PyPEEC-calibrated model.
- Model-evidence rows test whether complexity-aware selection can preserve identifiability when richer basis banks lower residuals.
- The model-selection calibration table ranks PyPEEC frozen trade-offs with a fixed audit objective. It is not used to alter frozen predictions.
- The allowed-basis table makes the model-bank discipline explicit: H0, H1, return, artifact, and refusal explanations should not share every nuisance basis by default.
- The held-out PyPEEC model-selection table is a pilot calibration/held-out split on the current mini distribution. It is separate from the frozen no-calibration bridge and is not broad CAD/FEM validation.
- The H0/H1 trade-off table treats no-via safety and true-via recall as primary endpoints.
- The repeated-split stability table estimates model-selection rank stability under many stratified mini-distribution splits. It is not a substitute for a larger PyPEEC distribution.
- The PyPEEC distribution table states current H0/H1/H2/H3 target coverage before any final model-selection claim is made.
- H0 hard-negative rows isolate the hardest practical diagnostic: not over-explaining no-via fields.
- Global registration search tests coarse CAD-to-field translation/rotation/scale uncertainty. It is intentionally kept separate from PyPEEC physics mismatch.
- Unknown rejection is calibrated from clean validation rows and then applied to hidden stress. It is a refusal mechanism, not a new classifier.
- Unknown risk-coverage reports whether refusal can become selective prediction rather than simply rejecting every hard case.
- Unknown-detector ablations compare margin, residual, margin/residual, registration instability, prediction disagreement, and combined unknown scores.
- The unknown-safety benchmark labels each refusal signal as a usable screen or diagnostic-only under a clean false-reject budget.
- The accepted-hidden risk table makes the safety endpoint sharper: a rejection signal is not enough if the hidden cases that remain accepted are still frequently wrong.
- The accepted-risk objective table ranks fixed refusal signals by clean-budget compliance, hidden acceptance, and accepted-hidden tail risk; hidden rows still do not choose thresholds.
- Physical-evidence unknown ablations add evidence entropy, residual-gap ambiguity, H0/H1 ambiguity, and residual-vs-score disagreement signals.
- The multi-state design scan compares synthetic excitation policies. It is an information-gain study, not a hardware protocol.
- The active-design utility table ranks policies using label-free margin/residual proxies and audits the resulting label accuracy.
- The constrained active-design table applies first-order feasibility screens to the label-free active policies.
- The registration stress curve measures how synthetic graph-to-field misregistration, standoff shift, and sensor tilt degrade identification and whether the fixed global search can recover geometric parts of the mismatch.
- A pass means the graph-identification framing is promising enough to replace further U-Net/pixel-output tuning as the next research direction. It does not mean no-via/return-path ambiguity is solved in real data.
"""
    (outputs_dir / "RUN_REPORT.md").write_text(report, encoding="utf-8")
    return metrics


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run Exp08 graph-guided magnetic system identification.")
    parser.add_argument("--config", type=Path, default=EXP_DIR / "configs" / "default.json")
    parser.add_argument("--outputs", type=Path, default=EXP_DIR / "outputs")
    parser.add_argument("--data", type=Path, default=EXP_DIR / "data")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    records = generate_dataset(cfg)
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )

    val_records = [r for r in records if r.split == "val"]
    complexity_penalty, _ = tune_complexity(val_records, obs_grid, cfg)
    rows_all = evaluate_records(records, obs_grid, cfg, complexity_penalty=complexity_penalty)
    rows_val = split_rows(rows_all, "val")

    via_thresholds = {}
    for key, name in [
        ("graph_h1_h0", "via_evidence"),
        ("raw_template", "raw_via_score"),
        ("sheet_residual_template", "sheet_residual_via_score"),
    ]:
        th, _ = tune_threshold(rows_val, cfg, score_key=name)
        via_thresholds[key] = float(th)

    metrics = write_outputs(cfg, records, rows_all, complexity_penalty, via_thresholds, args.outputs, args.data)
    print(json.dumps({
        "experiment": cfg["experiment_name"],
        "all_scientific_gates_passed": metrics["acceptance_gates"]["all_scientific_gates_passed"],
        "metrics_path": str(args.outputs / "metrics.json"),
    }, indent=2, ensure_ascii=False))
    return 0 if metrics["acceptance_gates"]["all_scientific_gates_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
