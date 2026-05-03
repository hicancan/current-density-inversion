from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


def confusion_matrix(y_true: Sequence[str], y_pred: Sequence[str], labels: Sequence[str]) -> np.ndarray:
    index = {label: i for i, label in enumerate(labels)}
    m = np.zeros((len(labels), len(labels)), dtype=int)
    for t, p in zip(y_true, y_pred):
        m[index[t], index[p]] += 1
    return m


def binary_metrics(y_true: Sequence[int], y_score: Sequence[float], threshold: float) -> Dict[str, float]:
    y_true_arr = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_score, dtype=float) > float(threshold)
    tp = int(np.sum((y_true_arr == 1) & y_pred))
    fp = int(np.sum((y_true_arr == 0) & y_pred))
    tn = int(np.sum((y_true_arr == 0) & (~y_pred)))
    fn = int(np.sum((y_true_arr == 1) & (~y_pred)))
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-30)
    fp_rate = fp / max(fp + tn, 1)
    return {
        "tp": float(tp),
        "fp": float(fp),
        "tn": float(tn),
        "fn": float(fn),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "false_positive_rate": float(fp_rate),
        "accuracy": float((tp + tn) / max(len(y_true_arr), 1)),
    }


def auc_pairwise(y_true: Sequence[int], y_score: Sequence[float]) -> float:
    """Simple Mann-Whitney AUC without sklearn dependency."""

    y = np.asarray(y_true, dtype=int)
    s = np.asarray(y_score, dtype=float)
    pos = s[y == 1]
    neg = s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    for p in pos:
        wins += float(np.sum(p > neg)) + 0.5 * float(np.sum(p == neg))
    return float(wins / (len(pos) * len(neg)))


def select_threshold_with_fp_cap(
    y_true: Sequence[int],
    y_score: Sequence[float],
    max_fp_rate: float,
) -> Tuple[float, Dict[str, float]]:
    scores = np.asarray(y_score, dtype=float)
    if len(scores) == 0:
        return 0.0, {}
    candidates = np.unique(np.concatenate([
        [scores.min() - 1e-12],
        scores,
        [scores.max() + 1e-12],
    ]))
    best_threshold = float(candidates[0])
    best = None
    for th in candidates:
        m = binary_metrics(y_true, y_score, threshold=float(th))
        if m["false_positive_rate"] <= float(max_fp_rate):
            key = (m["f1"], m["recall"], -abs(float(th)))
        else:
            # Still keep a fallback if no candidate satisfies the cap.
            key = (-1.0 + m["f1"] * 1e-3, -m["false_positive_rate"], -abs(float(th)))
        if best is None or key > best[0]:
            best = (key, m)
            best_threshold = float(th)
    return best_threshold, best[1]


def hypothesis_accuracy(y_true: Sequence[str], y_pred: Sequence[str]) -> float:
    return float(np.mean([t == p for t, p in zip(y_true, y_pred)])) if y_true else 0.0


def per_class_accuracy(y_true: Sequence[str], y_pred: Sequence[str]) -> Dict[str, float]:
    buckets = defaultdict(list)
    for t, p in zip(y_true, y_pred):
        buckets[t].append(t == p)
    return {label: float(np.mean(vals)) for label, vals in sorted(buckets.items())}


def selective_risk(y_true: Sequence[str], y_pred: Sequence[str], confidence: Sequence[float], coverages=(0.2, 0.5, 0.8, 1.0)) -> Dict[str, float]:
    conf = np.asarray(confidence, dtype=float)
    order = np.argsort(-conf)
    out = {}
    n = len(order)
    for cov in coverages:
        k = max(1, int(round(float(cov) * n)))
        idx = order[:k]
        acc = np.mean([y_true[i] == y_pred[i] for i in idx])
        out[f"accuracy_at_{int(cov * 100)}pct_coverage"] = float(acc)
        out[f"coverage_{int(cov * 100)}pct_n"] = float(k)
    return out
