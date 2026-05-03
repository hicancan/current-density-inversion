from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np

from .forward import field_from_segments, make_observation_grid
from .types import CaseRecord, Segment


CLASS_TO_HYPOTHESIS = {
    "no_via": "H0_sheet_only",
    "true_via": "H1_sheet_via",
    "return_path": "H2_sheet_return",
    "bend_artifact": "H3_sheet_artifact",
}


def _rng_uniform(rng: np.random.Generator, lo: float, hi: float) -> float:
    return float(rng.uniform(float(lo), float(hi)))


def _make_base_graph(case_index: int, split: str, rng: np.random.Generator, cfg: dict, ood: bool) -> dict:
    fov = float(cfg["grid"]["fov_m"])
    z1, z2 = [float(z) for z in cfg["geometry"]["layer_depths_m"]]
    zr = float(cfg["geometry"]["return_depth_m"])
    za = float(cfg["geometry"]["corner_artifact_depth_m"])

    margin = 0.24 * fov
    jitter = float(cfg["dataset"]["ood_shift"]["geometry_jitter_m"]) if ood else 0.0
    y1 = _rng_uniform(rng, -0.18 * fov, 0.18 * fov) + rng.normal(0.0, jitter)
    x2 = _rng_uniform(rng, -0.18 * fov, 0.18 * fov) + rng.normal(0.0, jitter)
    x_left = -0.5 * fov + margin + rng.normal(0.0, 0.25 * jitter)
    x_right = 0.5 * fov - margin + rng.normal(0.0, 0.25 * jitter)
    y_bot = -0.5 * fov + margin + rng.normal(0.0, 0.25 * jitter)
    y_top = 0.5 * fov - margin + rng.normal(0.0, 0.25 * jitter)

    # Main sheet-current graph: one horizontal trace on L1 and one vertical trace on L2.
    sheet = [
        Segment(
            name=f"edge_l1_{case_index:04d}",
            layer="L1",
            kind="edge",
            start=(x_left, y1, -z1),
            end=(x_right, y1, -z1),
            prior_group="sheet",
        ),
        Segment(
            name=f"edge_l2_{case_index:04d}",
            layer="L2",
            kind="edge",
            start=(x2, y_bot, -z2),
            end=(x2, y_top, -z2),
            prior_group="sheet",
        ),
    ]

    via = [
        Segment(
            name=f"via_l1_l2_{case_index:04d}",
            layer="L1-L2",
            kind="via",
            start=(x2, y1, -z1),
            end=(x2, y1, -z2),
            prior_group="via",
        )
    ]

    # Return-current candidate: a hidden lower conductor that can masquerade as a via residual.
    yr = y1 + _rng_uniform(rng, -0.18 * fov, 0.18 * fov)
    return_path = [
        Segment(
            name=f"return_l2_{case_index:04d}",
            layer="RETURN",
            kind="return",
            start=(x_right, yr, -zr),
            end=(x_left, yr, -zr),
            prior_group="return",
        )
    ]

    # Artifact candidate: a short local segment near the crossing; it captures bend/corner/finite-width mismatch.
    da = _rng_uniform(rng, 0.05 * fov, 0.12 * fov)
    artifact = [
        Segment(
            name=f"corner_artifact_{case_index:04d}",
            layer="ARTIFACT",
            kind="artifact",
            start=(x2 - 0.5 * da, y1 - 0.5 * da, -za),
            end=(x2 + 0.5 * da, y1 + 0.5 * da, -za),
            prior_group="artifact",
        )
    ]
    return {"sheet": sheet, "via": via, "return": return_path, "artifact": artifact, "crossing_xy": (x2, y1)}


def _truth_currents(case_class: str, graph: dict, rng: np.random.Generator, cfg: dict, ood: bool) -> Dict[str, float]:
    curr_cfg = cfg["currents"]
    low, high = [float(v) for v in curr_cfg["edge_current_a_range"]]
    if ood:
        scale_range = cfg["dataset"]["ood_shift"]["current_scale_range"]
        low *= float(scale_range[0])
        high *= float(scale_range[1])
    i1 = _rng_uniform(rng, low, high)
    i2 = _rng_uniform(rng, low, high) * rng.choice([-1.0, 1.0])
    currents: Dict[str, float] = {
        graph["sheet"][0].name: i1,
        graph["sheet"][1].name: i2,
    }
    if case_class == "true_via":
        lo, hi = [float(v) for v in curr_cfg["via_current_fraction_range"]]
        currents[graph["via"][0].name] = i1 * _rng_uniform(rng, lo, hi) * rng.choice([-1.0, 1.0])
    elif case_class == "return_path":
        lo, hi = [float(v) for v in curr_cfg["return_current_fraction_range"]]
        currents[graph["return"][0].name] = i1 * _rng_uniform(rng, lo, hi)
    elif case_class == "bend_artifact":
        lo, hi = [float(v) for v in curr_cfg["artifact_current_fraction_range"]]
        currents[graph["artifact"][0].name] = i1 * _rng_uniform(rng, lo, hi) * rng.choice([-1.0, 1.0])
    elif case_class == "no_via":
        pass
    else:
        raise ValueError(f"unknown class: {case_class}")
    return currents


def _make_case(case_index: int, split: str, case_class: str, rng: np.random.Generator, cfg: dict) -> CaseRecord:
    ood = split == "ood"
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    graph = _make_base_graph(case_index, split, rng, cfg, ood=ood)
    truth = _truth_currents(case_class, graph, rng, cfg, ood=ood)

    segments = list(graph["sheet"]) + list(graph["via"]) + list(graph["return"]) + list(graph["artifact"])
    b_clean = field_from_segments(
        segments,
        truth,
        obs_grid,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )

    if ood and rng.random() < float(cfg["dataset"]["ood_shift"]["extra_background_return_probability"]):
        # OOD stress: add a weak unmodeled broad return component. The graph scorer
        # should either refuse/flag ambiguity or prefer H2 over false H1-via.
        fov = float(cfg["grid"]["fov_m"])
        depth = float(cfg["geometry"]["return_depth_m"]) * 1.35
        hidden = Segment(
            name=f"hidden_return_{case_index:04d}",
            layer="HIDDEN_RETURN",
            kind="return",
            start=(0.42 * fov, -0.40 * fov, -depth),
            end=(-0.42 * fov, -0.40 * fov, -depth),
            prior_group="hidden",
        )
        truth[hidden.name] = 0.35 * max(abs(v) for v in truth.values())
        b_clean += field_from_segments(
            [hidden],
            truth,
            obs_grid,
            edge_steps=int(cfg["geometry"]["edge_discretization"]),
            via_steps=int(cfg["geometry"]["via_discretization"]),
        )

    rel_noise = float(cfg["dataset"]["noise_std_relative_to_max_abs_b"][split])
    sigma = rel_noise * max(float(np.max(np.abs(b_clean))), 1e-30)
    noise = rng.normal(0.0, sigma, size=b_clean.shape)
    b_obs = b_clean + noise

    return CaseRecord(
        case_id=f"{split}_{case_index:05d}_{case_class}",
        split=split,
        class_label=case_class,
        hypothesis_label=CLASS_TO_HYPOTHESIS[case_class],
        b_clean=b_clean,
        b_obs=b_obs,
        sheet_segments=list(graph["sheet"]),
        via_candidates=list(graph["via"]),
        return_candidates=list(graph["return"]),
        artifact_candidates=list(graph["artifact"]),
        truth_currents=truth,
        metadata={
            "crossing_xy_m": graph["crossing_xy"],
            "noise_sigma_t": sigma,
            "noise_relative": rel_noise,
            "is_ood": ood,
        },
    )


def generate_dataset(cfg: dict) -> List[CaseRecord]:
    rng = np.random.default_rng(int(cfg["seed"]))
    records: List[CaseRecord] = []
    classes = list(cfg["dataset"]["classes"])
    split_counts = {
        "val": int(cfg["dataset"]["n_val_per_class"]),
        "test": int(cfg["dataset"]["n_test_per_class"]),
        "ood": int(cfg["dataset"]["n_ood_per_class"]),
    }
    idx = 0
    for split, count in split_counts.items():
        for cls in classes:
            for _ in range(count):
                records.append(_make_case(idx, split, cls, rng, cfg))
                idx += 1
    return records


def write_dataset_artifacts(records: List[CaseRecord], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_dir / "exp08_graph_id_dataset.npz",
        b_clean=np.stack([r.b_clean for r in records]),
        b_obs=np.stack([r.b_obs for r in records]),
        split=np.asarray([r.split for r in records]),
        class_label=np.asarray([r.class_label for r in records]),
        hypothesis_label=np.asarray([r.hypothesis_label for r in records]),
        case_id=np.asarray([r.case_id for r in records]),
    )
    with (out_dir / "exp08_cases.jsonl").open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r.graph_json(), ensure_ascii=False) + "\n")
