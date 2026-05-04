"""Metrics computation for E18 physics-constrained PDN inverse."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR.parent))

from src.forward_adapter import build_div_matrix

LAYER_IDS = ["L1", "L2", "L3", "L4"]


def rel_l2(a: np.ndarray, b: np.ndarray, cap: float = 10.0) -> float:
    nd = float(np.linalg.norm(a.ravel() - b.ravel()))
    nr = float(np.linalg.norm(b.ravel()))
    if nr < 1e-30:
        return 0.0 if nd < 1e-30 else cap
    return float(min(nd / nr, cap))


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((a.ravel() - b.ravel()) ** 2)))


def current_rmse(pred: np.ndarray, truth: np.ndarray) -> float:
    return rmse(pred, truth)


def current_relative_l2(pred: np.ndarray, truth: np.ndarray) -> float:
    return rel_l2(pred, truth)


def layer_wise_rmse(pred: np.ndarray, truth: np.ndarray, n: int) -> dict:
    """RMSE per layer (relative L2)."""
    pl = n * n
    result = {}
    for li in range(4):
        js = li * 2 * pl
        jys = js + pl
        pj = np.concatenate([pred[js:js + pl], pred[jys:jys + pl]])
        tj = np.concatenate([truth[js:js + pl], truth[jys:jys + pl]])
        result[LAYER_IDS[li]] = rel_l2(pj.reshape(2, n, n), tj.reshape(2, n, n))
    return result


def layer_misallocation(pred: np.ndarray, truth: np.ndarray, n: int) -> float:
    """Mean absolute difference in layer energy fraction."""
    pl = n * n
    fracs_p = []
    fracs_t = []
    total_p = float(np.sum(pred[:8 * pl] ** 2))
    total_t = float(np.sum(truth[:8 * pl] ** 2))
    for li in range(4):
        js = li * 2 * pl
        jys = js + pl
        ep = float(np.sum(pred[js:jys + pl] ** 2))
        et = float(np.sum(truth[js:jys + pl] ** 2))
        fracs_p.append(ep / max(total_p, 1e-30))
        fracs_t.append(et / max(total_t, 1e-30))
    return float(np.mean(np.abs(np.array(fracs_p) - np.array(fracs_t))))


def via_precision_recall_f1(
    pred: np.ndarray, truth: np.ndarray, n: int
) -> dict:
    """Via detection precision, recall, F1."""
    pl = n * n
    vb = 8 * pl
    vmax = float(np.max(np.abs(truth[vb:])))
    vth = 0.1 * vmax if vmax > 1e-6 else 0.005

    all_pb = []
    all_tb = []
    per_via = {}
    for vi, nm in enumerate(["s12", "s23", "s34"]):
        s = vb + vi * pl
        e = s + pl
        p = pred[s:e]
        t = truth[s:e]
        tb = (np.abs(t) > vth).astype(float)
        pb = (np.abs(p) > vth).astype(float)
        all_pb.append(pb)
        all_tb.append(tb)
        per_via[f"{nm}_rmse"] = rel_l2(p, t)

    pa = np.concatenate([p.ravel() for p in all_pb])
    ta = np.concatenate([t.ravel() for t in all_tb])
    tp = float(np.sum((pa > 0.5) & (ta > 0.5)))
    fp = float(np.sum((pa > 0.5) & (ta <= 0.5)))
    fn = float(np.sum((pa <= 0.5) & (ta > 0.5)))
    prec = tp / max(tp + fp, 1.0)
    rec = tp / max(tp + fn, 1.0)
    f1 = 2 * prec * rec / max(prec + rec, 1e-30)

    return {
        "via_precision": float(prec),
        "via_recall": float(rec),
        "via_f1": float(f1),
        "via_fp": int(fp),
        "via_fn": int(fn),
        "via_tp": int(tp),
        **per_via,
    }


def no_via_false_positive(
    pred: np.ndarray, truth: np.ndarray, n: int
) -> float:
    """Count false positive via detections on no-via ground truth."""
    pl = n * n
    vb = 8 * pl
    t_via = truth[vb:]
    p_via = pred[vb:]
    # If ground truth has no vias, count any detection as FP
    if np.max(np.abs(t_via)) < 1e-6:
        return float(np.sum(np.abs(p_via) > 0.005))
    return 0.0


def physical_b_residual(
    pred: np.ndarray, b_obs: np.ndarray, A: np.ndarray
) -> float:
    b_pred = A @ pred
    return float(np.sqrt(np.mean((b_pred - b_obs) ** 2)))


def kcl_residual(pred: np.ndarray, n: int) -> float:
    D = build_div_matrix(n)
    return float(np.sqrt(np.mean((D @ pred) ** 2)))


def topology_residual(pred: np.ndarray, n: int) -> float:
    return kcl_residual(pred, n)


def current_closure_error(pred: np.ndarray, n: int) -> float:
    """Total current magnitude imbalance across layers."""
    pl = n * n
    layer_totals = []
    for li in range(4):
        js = li * 2 * pl
        layer_totals.append(float(np.sum(pred[js:js + 2 * pl])))
    via_totals = []
    for vi in range(3):
        s = 8 * pl + vi * pl
        via_totals.append(float(np.sum(pred[s:s + pl])))
    # Closure: sum of all currents should approach zero for physical consistency
    return float(abs(sum(layer_totals) + sum(via_totals)))


def b_residual_rel(
    pred: np.ndarray, field: np.ndarray, A: np.ndarray
) -> float:
    """Relative B residual."""
    b_pred = A @ pred
    return rel_l2(b_pred, field.ravel())


def compute_all_metrics(
    pred: np.ndarray,
    truth: np.ndarray,
    field: np.ndarray,
    A: np.ndarray,
    n: int,
) -> dict:
    """Compute all metrics for a single case."""
    return {
        "current_rmse": current_rmse(pred, truth),
        "current_relative_l2": current_relative_l2(pred, truth),
        "layer_wise_rmse": layer_wise_rmse(pred, truth, n),
        "layer_misallocation": layer_misallocation(pred, truth, n),
        "via_metrics": via_precision_recall_f1(pred, truth, n),
        "no_via_fp": no_via_false_positive(pred, truth, n),
        "physical_b_residual": physical_b_residual(pred, field.ravel(), A),
        "kcl_residual": kcl_residual(pred, n),
        "topology_residual": topology_residual(pred, n),
        "current_closure_error": current_closure_error(pred, n),
        "b_residual_rel": b_residual_rel(pred, field, A),
    }
