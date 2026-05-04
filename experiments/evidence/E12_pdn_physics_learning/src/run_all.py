from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np


EVIDENCE_ID = "E12_pdn_physics_learning"
CLAIM_ID = "C10_pdn_kcl_distribution_need"
GENERATED_AT = "2026-05-04T00:00:00Z"


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def load_e11_module(e11_package_dir: Path) -> Any:
    module_path = e11_package_dir / "src" / "run_all.py"
    spec = importlib.util.spec_from_file_location("e11_chip_like_pdn_run_all", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import E11 module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_or_generate_e11_cases(cfg: dict[str, Any], package_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any], Any]:
    e11_package_dir = _resolve(package_dir, str(cfg["e11_package_dir"]))
    e11_config_path = _resolve(package_dir, str(cfg["e11_config"]))
    e11_dataset_path = _resolve(package_dir, str(cfg["e11_dataset_json"]))
    e11 = load_e11_module(e11_package_dir)
    e11_cfg = e11.load_config(e11_config_path)
    if e11_dataset_path.exists():
        cases = json.loads(e11_dataset_path.read_text(encoding="utf-8"))
    else:
        generated = e11.generate_cases(e11_cfg)
        cases = e11.serializable_cases(generated)
    return cases, e11_cfg, e11


def labels_from_cases(cases: list[dict[str, Any]], hypotheses: list[str]) -> np.ndarray:
    index = {hypothesis: idx for idx, hypothesis in enumerate(hypotheses)}
    return np.array([index[case["true_hypothesis"]] for case in cases], dtype=int)


def feature_matrix(cases: list[dict[str, Any]]) -> np.ndarray:
    return np.array([case["field_features"] for case in cases], dtype=float)


def standardize_train_only(x: np.ndarray, train_mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = x[train_mask].mean(axis=0)
    scale = x[train_mask].std(axis=0)
    scale = np.where(scale < 1e-15, 1.0, scale)
    return (x - mean) / scale, mean, scale


def one_hot(labels: np.ndarray, class_count: int) -> np.ndarray:
    y = np.zeros((labels.shape[0], class_count), dtype=float)
    y[np.arange(labels.shape[0]), labels] = 1.0
    return y


def ridge_fit(x: np.ndarray, y: np.ndarray, alpha: float) -> np.ndarray:
    x_aug = np.concatenate([x, np.ones((x.shape[0], 1), dtype=float)], axis=1)
    reg = np.eye(x_aug.shape[1], dtype=float) * alpha
    reg[-1, -1] = 0.0
    return np.linalg.solve(x_aug.T @ x_aug + reg, x_aug.T @ y)


def ridge_predict(x: np.ndarray, weights: np.ndarray) -> np.ndarray:
    x_aug = np.concatenate([x, np.ones((x.shape[0], 1), dtype=float)], axis=1)
    return x_aug @ weights


def nearest_centroid_predict(x: np.ndarray, labels: np.ndarray, train_mask: np.ndarray, eval_indices: np.ndarray, class_count: int) -> np.ndarray:
    centroids = []
    for label in range(class_count):
        rows = x[train_mask & (labels == label)]
        if len(rows) == 0:
            centroids.append(np.zeros(x.shape[1], dtype=float))
        else:
            centroids.append(rows.mean(axis=0))
    centroid_matrix = np.stack(centroids, axis=0)
    distances = np.linalg.norm(x[eval_indices, None, :] - centroid_matrix[None, :, :], axis=2)
    return distances.argmin(axis=1)


def accuracy(predicted: np.ndarray, labels: np.ndarray) -> float:
    return float(np.mean(predicted == labels)) if len(labels) else 0.0


def edge_universe(cases: list[dict[str, Any]]) -> list[str]:
    ids = sorted({edge["id"] for case in cases for edge in case["solved"]["edges"]})
    return ids


def current_vector(case: dict[str, Any], edge_ids: list[str]) -> np.ndarray:
    by_id = {edge["id"]: float(edge["current"]) for edge in case["solved"]["edges"]}
    return np.array([by_id.get(edge_id, 0.0) for edge_id in edge_ids], dtype=float)


def currents_from_graph(graph: dict[str, Any], solved: dict[str, Any], edge_ids: list[str]) -> np.ndarray:
    by_id = {edge["id"]: float(edge["current"]) for edge in solved["edges"]}
    return np.array([by_id.get(edge_id, 0.0) for edge_id in edge_ids], dtype=float)


def solved_from_edge_vector(graph: dict[str, Any], vector: np.ndarray, edge_ids: list[str]) -> dict[str, Any]:
    by_id = {edge_id: float(vector[idx]) for idx, edge_id in enumerate(edge_ids)}
    edges = []
    for edge in graph["edges"]:
        solved_edge = dict(edge)
        solved_edge["current"] = by_id.get(edge["id"], 0.0)
        edges.append(solved_edge)
    return {"edges": edges}


def current_metrics_for_vector(graph: dict[str, Any], vector: np.ndarray, edge_ids: list[str]) -> dict[str, float]:
    by_id = {edge_id: float(vector[idx]) for idx, edge_id in enumerate(edge_ids)}
    net_out = {node: 0.0 for node in graph["nodes"]}
    for edge in graph["edges"]:
        current = by_id.get(edge["id"], 0.0)
        net_out[edge["a"]] += current
        net_out[edge["b"]] -= current
    boundary = graph["boundary_voltages"]
    interior = [abs(net_out[node]) for node in graph["nodes"] if node not in boundary]
    source = net_out["vdd_bump"]
    sink = net_out["gnd_bump"]
    closure = abs(source + sink) / max(abs(source), abs(sink), 1e-30)
    return {
        "max_kcl_residual": float(max(interior) if interior else 0.0),
        "current_closure_error": float(closure),
    }


def rel_l2(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(b), 1e-30))


def evaluate_field_rmse(e11: Any, graph: dict[str, Any], solved: dict[str, Any], true_field: np.ndarray, e11_cfg: dict[str, Any]) -> float:
    field = e11.forward_biot_savart(graph, solved, int(e11_cfg["grid_size"]), float(e11_cfg["sensor_z"]))
    return rel_l2(field, true_field)


def acceptance_gates_from_metrics(metrics: dict[str, Any], cfg: dict[str, Any]) -> dict[str, bool]:
    gain = metrics["physics_learning_gain_vs_unconstrained"]
    gates = {
        "heldout_accuracy_material": metrics["heldout_accuracy"] >= float(cfg["heldout_accuracy_threshold"]),
        "accuracy_above_majority_baseline": (
            metrics["heldout_accuracy"] - metrics["models"]["majority_baseline"]["heldout_accuracy"]
        )
        >= float(cfg["accuracy_gain_vs_majority_threshold"]),
        "family_generalization_gap_below_threshold": metrics["family_generalization_gap"] <= float(cfg["family_generalization_gap_threshold"]),
        "predicted_kcl_improves_over_unconstrained": gain["kcl_residual_reduction_ratio"] >= float(cfg["kcl_improvement_ratio_threshold"]),
        "predicted_closure_improves_over_unconstrained": gain["closure_error_reduction_ratio"] >= float(cfg["closure_improvement_ratio_threshold"]),
        "field_reconstruction_not_degraded": metrics["field_reconstruction_rmse"] <= float(cfg["field_reconstruction_rmse_threshold"]),
    }
    gates["all_acceptance_gates_passed"] = all(gates.values())
    return gates


def run_learning(cfg: dict[str, Any], package_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    cases, e11_cfg, e11 = load_or_generate_e11_cases(cfg, package_dir)
    hypotheses = list(e11.HYPOTHESES)
    labels = labels_from_cases(cases, hypotheses)
    x_raw = feature_matrix(cases)
    roles = np.array([case["split_role"] for case in cases])
    train_mask = np.isin(roles, np.array(cfg["train_roles"], dtype=object))
    eval_mask = np.isin(roles, np.array(cfg["eval_roles"], dtype=object))
    heldout_mask = roles == "heldout"
    family_hidden_mask = roles == "family_hidden"
    if not train_mask.any() or not eval_mask.any():
        raise ValueError("E12 requires non-empty train and eval roles")

    x, _, _ = standardize_train_only(x_raw, train_mask)
    class_count = len(hypotheses)
    alpha = float(cfg["ridge_lambda"])

    majority_label = int(np.bincount(labels[train_mask], minlength=class_count).argmax())
    majority_pred_eval = np.full(eval_mask.sum(), majority_label, dtype=int)
    majority_pred_heldout = np.full(heldout_mask.sum(), majority_label, dtype=int)

    eval_indices = np.where(eval_mask)[0]
    heldout_indices = np.where(heldout_mask)[0]
    family_hidden_indices = np.where(family_hidden_mask)[0]
    scorer_pred_eval = nearest_centroid_predict(x, labels, train_mask, eval_indices, class_count)
    scorer_pred_heldout = nearest_centroid_predict(x, labels, train_mask, heldout_indices, class_count)

    weights_cls = ridge_fit(x[train_mask], one_hot(labels[train_mask], class_count), alpha)
    logits = ridge_predict(x, weights_cls)
    graph_agnostic_pred = logits.argmax(axis=1)

    edge_ids = edge_universe(cases)
    current_targets = np.stack([current_vector(case, edge_ids) for case in cases], axis=0)
    weights_current = ridge_fit(x[train_mask], current_targets[train_mask], alpha)
    unconstrained_currents = ridge_predict(x, weights_current)

    graph_agnostic_kcl = []
    graph_agnostic_closure = []
    graph_agnostic_field = []
    physics_kcl = []
    physics_closure = []
    physics_field = []
    physics_pred_current_vectors = []

    for idx in eval_indices:
        case = cases[idx]
        true_field = np.array(case["field"], dtype=float)

        unconstrained_vector = unconstrained_currents[idx]
        graph_agnostic_metrics = current_metrics_for_vector(case["graph"], unconstrained_vector, edge_ids)
        graph_agnostic_kcl.append(graph_agnostic_metrics["max_kcl_residual"])
        graph_agnostic_closure.append(graph_agnostic_metrics["current_closure_error"])
        unconstrained_solved = solved_from_edge_vector(case["graph"], unconstrained_vector, edge_ids)
        graph_agnostic_field.append(evaluate_field_rmse(e11, case["graph"], unconstrained_solved, true_field, e11_cfg))

        predicted_hypothesis = hypotheses[int(graph_agnostic_pred[idx])]
        candidate_graph = e11.build_graph(predicted_hypothesis, int(case["family"]), int(case["variant"]), e11_cfg)
        candidate_solved = e11.solve_kcl(candidate_graph)
        physics_vector = currents_from_graph(candidate_graph, candidate_solved, edge_ids)
        physics_pred_current_vectors.append(physics_vector)
        physics_metrics = current_metrics_for_vector(candidate_graph, physics_vector, edge_ids)
        physics_kcl.append(physics_metrics["max_kcl_residual"])
        physics_closure.append(physics_metrics["current_closure_error"])
        physics_field.append(evaluate_field_rmse(e11, candidate_graph, candidate_solved, true_field, e11_cfg))

    heldout_accuracy = accuracy(graph_agnostic_pred[heldout_mask], labels[heldout_mask])
    family_hidden_accuracy = accuracy(graph_agnostic_pred[family_hidden_mask], labels[family_hidden_mask])
    train_accuracy = accuracy(graph_agnostic_pred[train_mask], labels[train_mask])
    family_gap = max(0.0, train_accuracy - family_hidden_accuracy)
    majority_heldout_accuracy = accuracy(majority_pred_heldout, labels[heldout_mask])

    unconstrained_kcl = float(max(graph_agnostic_kcl) if graph_agnostic_kcl else 0.0)
    unconstrained_closure = float(max(graph_agnostic_closure) if graph_agnostic_closure else 0.0)
    physics_kcl_max = float(max(physics_kcl) if physics_kcl else 0.0)
    physics_closure_max = float(max(physics_closure) if physics_closure else 0.0)
    kcl_reduction = max(0.0, (unconstrained_kcl - physics_kcl_max) / max(unconstrained_kcl, 1e-30))
    closure_reduction = max(0.0, (unconstrained_closure - physics_closure_max) / max(unconstrained_closure, 1e-30))

    model_summary = {
        "majority_baseline": {
            "heldout_accuracy": float(majority_heldout_accuracy),
            "eval_accuracy": accuracy(majority_pred_eval, labels[eval_mask]),
        },
        "scorer": {
            "type": "nearest centroid residual scorer over E11 Bxyz features",
            "heldout_accuracy": accuracy(scorer_pred_heldout, labels[heldout_mask]),
            "eval_accuracy": accuracy(scorer_pred_eval, labels[eval_mask]),
        },
        "graph_agnostic": {
            "type": "ridge classifier Bxyz features -> H0/H1/H2/H3 plus unconstrained edge-current ridge",
            "heldout_accuracy": float(heldout_accuracy),
            "family_hidden_accuracy": float(family_hidden_accuracy),
            "eval_accuracy": accuracy(graph_agnostic_pred[eval_mask], labels[eval_mask]),
            "max_predicted_kcl_residual": unconstrained_kcl,
            "max_predicted_current_closure_error": unconstrained_closure,
            "field_reconstruction_rmse": float(np.median(graph_agnostic_field) if graph_agnostic_field else 0.0),
        },
        "physics_aware": {
            "type": "ridge hypothesis classifier with generated graph/KCL projection for currents",
            "heldout_accuracy": float(heldout_accuracy),
            "family_hidden_accuracy": float(family_hidden_accuracy),
            "max_predicted_kcl_residual": physics_kcl_max,
            "max_predicted_current_closure_error": physics_closure_max,
            "field_reconstruction_rmse": float(np.median(physics_field) if physics_field else 0.0),
        },
    }

    split_roles = {role: int(np.sum(roles == role)) for role in sorted(set(roles.tolist()))}
    metrics = {
        "evidence_id": EVIDENCE_ID,
        "claim_id": CLAIM_ID,
        "status": "running",
        "generated_at": GENERATED_AT,
        "dataset": {
            "source_evidence": "E11_chip_like_pdn_distribution",
            "case_count": len(cases),
            "hypotheses": hypotheses,
            "feature_source": "Bxyz summary features fit with train-only scaling",
            "heldout_not_used_for_tuning": True,
        },
        "split_roles": split_roles,
        "models": model_summary,
        "heldout_accuracy": float(heldout_accuracy),
        "family_generalization_gap": float(family_gap),
        "predicted_kcl_residual": physics_kcl_max,
        "predicted_current_closure_error": physics_closure_max,
        "field_reconstruction_rmse": float(np.median(physics_field) if physics_field else 0.0),
        "physics_learning_gain_vs_unconstrained": {
            "kcl_residual_reduction_ratio": float(kcl_reduction),
            "closure_error_reduction_ratio": float(closure_reduction),
            "unconstrained_max_kcl_residual": unconstrained_kcl,
            "unconstrained_max_current_closure_error": unconstrained_closure,
            "physics_aware_max_kcl_residual": physics_kcl_max,
            "physics_aware_max_current_closure_error": physics_closure_max,
        },
        "cannot_claim": [
            "real chip PDN validation",
            "real CAD/Gerber/GDS validation",
            "external FEM/FastHenry validation",
            "real QDM/NV validation",
            "mechanism-level explanation",
            "that label correctness alone proves learned physics",
        ],
    }
    gates = acceptance_gates_from_metrics(metrics, cfg)
    metrics["acceptance_gates"] = gates
    metrics["all_acceptance_gates_passed"] = gates["all_acceptance_gates_passed"]
    metrics["status"] = "passed" if gates["all_acceptance_gates_passed"] else "failed"

    details = {
        "eval_case_count": int(eval_mask.sum()),
        "heldout_case_count": int(heldout_mask.sum()),
        "family_hidden_case_count": int(family_hidden_mask.sum()),
        "edge_universe_count": len(edge_ids),
        "edge_universe": edge_ids,
    }
    return metrics, details


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")


def md_float(value: float) -> str:
    return f"{value:.3e}" if abs(value) < 1e-3 else f"{value:.3f}"


def write_outputs(outputs: Path, metrics: dict[str, Any], details: dict[str, Any]) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    lines = [
        "# PDN Physics Learning Metrics Table\n\n",
        "| Metric | Value | Gate |\n",
        "|---|---:|---|\n",
        f"| heldout accuracy | {metrics['heldout_accuracy']:.3f} | {metrics['acceptance_gates']['heldout_accuracy_material']} |\n",
        f"| majority heldout accuracy | {metrics['models']['majority_baseline']['heldout_accuracy']:.3f} | - |\n",
        f"| family generalization gap | {metrics['family_generalization_gap']:.3f} | {metrics['acceptance_gates']['family_generalization_gap_below_threshold']} |\n",
        f"| unconstrained max KCL residual | {md_float(metrics['physics_learning_gain_vs_unconstrained']['unconstrained_max_kcl_residual'])} | - |\n",
        f"| physics-aware max KCL residual | {md_float(metrics['predicted_kcl_residual'])} | {metrics['acceptance_gates']['predicted_kcl_improves_over_unconstrained']} |\n",
        f"| unconstrained max closure error | {md_float(metrics['physics_learning_gain_vs_unconstrained']['unconstrained_max_current_closure_error'])} | - |\n",
        f"| physics-aware max closure error | {md_float(metrics['predicted_current_closure_error'])} | {metrics['acceptance_gates']['predicted_closure_improves_over_unconstrained']} |\n",
        f"| physics-aware field RMSE | {metrics['field_reconstruction_rmse']:.3f} | {metrics['acceptance_gates']['field_reconstruction_not_degraded']} |\n",
    ]
    (outputs / "PDN_PHYSICS_LEARNING_METRICS_TABLE.md").write_text("".join(lines), encoding="utf-8")
    write_json(outputs / "learning_details.json", details)
    report = f"""# RUN_REPORT - E12 PDN Physics Learning

Claim: `{CLAIM_ID}`.

This run reads/generated E11 chip-like PDN rows and evaluates whether a CPU
baseline can improve label learning while also improving predicted-current KCL
and current closure. The physics-aware branch uses generated graph/KCL
projection; therefore the result is evidence for generated-domain physics
closure, not for real mechanism explanation.

## Metrics

{(outputs / "PDN_PHYSICS_LEARNING_METRICS_TABLE.md").read_text(encoding="utf-8")}

## Boundary

This evidence cannot be claimed as real chip, CAD/Gerber/GDS, external solver,
real QDM/NV, or mechanism-level validation. Label correctness remains separate
from mechanism correctness.
"""
    (outputs / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def run_experiment(cfg: dict[str, Any], outputs: Path, package_dir: Path | None = None) -> dict[str, Any]:
    package_dir = package_dir or Path.cwd()
    metrics, details = run_learning(cfg, package_dir)
    write_outputs(outputs, metrics, details)
    write_json(outputs / "metrics.json", metrics)
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Run E12 generated PDN physics-learning evidence.")
    parser.add_argument("--config", type=Path, default=Path("configs/default.json"))
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    cfg = load_config(args.config)
    metrics = run_experiment(cfg, args.out, Path.cwd())
    print(
        json.dumps(
            {
                "evidence_id": EVIDENCE_ID,
                "metrics_path": str(args.out / "metrics.json"),
                "passed": metrics["all_acceptance_gates_passed"],
            },
            sort_keys=True,
        )
    )
    return 0 if metrics["all_acceptance_gates_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
