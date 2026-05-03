from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from forward.segments import make_grid, field_from_segments, group_field, norm_field, Segment, rel_l2
from geometry.toy_circuit import build_two_layer_via_segments, finite_volume_route_maps, make_random_toy_segments
from detection.matched_filter import normalized_template_score, peak_location
from experiments.plotting import save_bxyz_panels, save_map_grid, save_line_plot


def ensure_dirs():
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "data").mkdir(exist_ok=True)


def load_cfg(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_example(cfg):
    g = cfg["grid"]
    p = cfg["physics"]
    X, Y, Z = make_grid(g["fov_m"], g["n"], g["sensor_z_m"])
    x = X[0, :]
    y = Y[:, 0]
    segments = build_two_layer_via_segments(
        p["current_A"], p["layer1_z_m"], p["layer2_z_m"], p["via_x_m"], p["via_y_m"],
        p["left_port_x_m"], p["right_port_x_m"], p["route_y_m"]
    )
    B_total = field_from_segments(X, Y, Z, segments, n_quad=p["n_quad"])
    B_l1 = group_field(X, Y, Z, segments, "layer1", n_quad=p["n_quad"])
    B_l2 = group_field(X, Y, Z, segments, "layer2", n_quad=p["n_quad"])
    B_via = group_field(X, Y, Z, segments, "via", n_quad=p["n_quad"])
    B_sum = B_l1 + B_l2 + B_via
    maps = finite_volume_route_maps(g["fov_m"], g["n"], p["current_A"], p["via_x_m"], p["via_y_m"], p["left_port_x_m"], p["right_port_x_m"], p["route_y_m"])
    return X, Y, Z, x, y, segments, B_total, B_l1, B_l2, B_via, B_sum, maps


def via_template_at_center(cfg, X, Y, Z):
    p = cfg["physics"]
    tcfg = cfg["template"]
    seg = Segment((0.0, 0.0, p["layer1_z_m"]), (0.0, 0.0, p["layer2_z_m"]), p["current_A"], "center_template_via", "via")
    return field_from_segments(X, Y, Z, [seg], n_quad=tcfg["n_quad"])


def compute_layer_mixing(cfg, X, Y, Z):
    p = cfg["physics"]
    lm = cfg["layer_mixing"]
    z0 = lm["shallow_z_m"]
    offsets = np.array(lm["depth_offsets_um"], dtype=float) * 1e-6
    sims = []
    amp_ratios = []
    # Use identical horizontal segment at two depths; compare normalized Bxyz templates.
    shallow = Segment((-0.0005, -0.0002, z0), (0.0005, -0.0002, z0), p["current_A"], "shallow", "shallow")
    B_shallow = field_from_segments(X, Y, Z, [shallow], n_quad=80)
    a = B_shallow.ravel()
    for dz in offsets:
        deep = Segment((-0.0005, -0.0002, z0 - dz), (0.0005, -0.0002, z0 - dz), p["current_A"], "deep", "deep")
        B_deep = field_from_segments(X, Y, Z, [deep], n_quad=80)
        b = B_deep.ravel()
        sims.append(float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-30)))
        amp_ratios.append(float(np.max(np.abs(B_deep)) / (np.max(np.abs(B_shallow)) + 1e-30)))
    return offsets, np.array(sims), np.array(amp_ratios)


def make_small_dataset(cfg):
    dcfg = cfg["dataset"]
    pcfg = cfg["physics"]
    rng = np.random.default_rng(dcfg["seed"])
    X, Y, Z = make_grid(dcfg["fov_m"], dcfg["n"], cfg["grid"].get("sensor_z_m", 0.0))
    Bs = []
    via_xyI = []
    source_counts = []
    for _ in range(dcfg["n_samples"]):
        segments, meta = make_random_toy_segments(rng, dcfg["fov_m"], pcfg["current_A"], pcfg["layer1_z_m"], pcfg["layer2_z_m"])
        B = field_from_segments(X, Y, Z, segments, n_quad=dcfg["n_quad"])
        Bs.append(B.astype(np.float32))
        via_xyI.append(meta)
        source_counts.append(len(segments))
    return X, Y, np.stack(Bs, axis=0), np.array(via_xyI, dtype=np.float32), np.array(source_counts)


def clipped_y(y_m: float, fov_m: float) -> float:
    return float(np.clip(y_m, -0.42 * fov_m, 0.42 * fov_m))


def route_paths_from_spec(spec, z1, z2):
    """Return layer paths as axis-aligned point lists for one benchmark path."""
    kind = spec["route_kind"]
    vx, vy = spec["via_x_m"], spec["via_y_m"]
    left_x, right_x = spec["left_x_m"], spec["right_x_m"]
    left_y, right_y = spec["left_y_m"], spec["right_y_m"]

    if kind in {"no_via", "no_via_background"} or not spec.get("has_via", True):
        l1 = [(left_x, left_y, z1), (right_x, left_y, z1)]
        l2 = [(left_x, right_y, z2), (right_x, right_y, z2)]
        return l1, l2

    if kind in {"l1_jog", "both_jog", "both_jog_background", "dense_via_background"}:
        l1 = [(left_x, left_y, z1), (vx, left_y, z1), (vx, vy, z1)]
    else:
        l1 = [(left_x, vy, z1), (vx, vy, z1)]

    if kind in {"l2_jog", "both_jog", "both_jog_background", "dense_via_background"}:
        l2 = [(vx, vy, z2), (vx, right_y, z2), (right_x, right_y, z2)]
    else:
        l2 = [(vx, vy, z2), (right_x, vy, z2)]
    return l1, l2


def path_specs_from_meta(meta):
    return meta.get("paths", [meta])


def segments_from_path(points, current, prefix, group):
    return [
        Segment(points[i], points[i + 1], current, f"{prefix}_{i}", group)
        for i in range(len(points) - 1)
    ]


def rasterize_axis_path(truth, channel_x, channel_y, x, y, path, current):
    dx = float(x[1] - x[0])
    for p0, p1 in zip(path[:-1], path[1:]):
        x0, y0 = p0[0], p0[1]
        x1, y1 = p1[0], p1[1]
        ix0 = int(np.argmin(np.abs(x - x0)))
        ix1 = int(np.argmin(np.abs(x - x1)))
        iy0 = int(np.argmin(np.abs(y - y0)))
        iy1 = int(np.argmin(np.abs(y - y1)))
        if abs(ix1 - ix0) >= abs(iy1 - iy0):
            c0, c1 = sorted([ix0, ix1])
            sign = 1.0 if ix1 >= ix0 else -1.0
            truth[channel_x, iy0, c0 : c1 + 1] = sign * current / dx
        else:
            r0, r1 = sorted([iy0, iy1])
            sign = 1.0 if iy1 >= iy0 else -1.0
            truth[channel_y, r0 : r1 + 1, ix0] = sign * current / dx


def route_truth_maps(fov_m, n, meta, z1, z2):
    """Raster truth maps for the benchmark dataset.

    Channels are J1x, J1y, J2x, J2y, s1. Values are finite-volume-like densities
    on the same grid used by the magnetic fields. This is a label map for
    algorithm comparison; the field is still generated from line segments.
    """
    x = np.linspace(-fov_m / 2, fov_m / 2, n)
    y = np.linspace(-fov_m / 2, fov_m / 2, n)
    dx = float(x[1] - x[0])
    ix_v = int(np.argmin(np.abs(x - meta["via_x_m"])))
    iy_v = int(np.argmin(np.abs(y - meta["via_y_m"])))
    truth = np.zeros((5, n, n), dtype=np.float32)

    for spec in path_specs_from_meta(meta):
        l1, l2 = route_paths_from_spec(spec, z1, z2)
        rasterize_axis_path(truth, 0, 1, x, y, l1, spec["current_A"])
        rasterize_axis_path(truth, 2, 3, x, y, l2, spec["current_A"])
        if spec.get("has_via", True):
            ix_v = int(np.argmin(np.abs(x - spec["via_x_m"])))
            iy_v = int(np.argmin(np.abs(y - spec["via_y_m"])))
            truth[4, iy_v, ix_v] += spec["current_A"] / dx
    return truth


def benchmark_segments_from_meta(meta, z1, z2):
    segs = []
    for idx, spec in enumerate(path_specs_from_meta(meta)):
        I = spec["current_A"]
        vx, vy = spec["via_x_m"], spec["via_y_m"]
        l1, l2 = route_paths_from_spec(spec, z1, z2)
        segs.extend(segments_from_path(l1, I, f"bench_L1_{idx}", "layer1"))
        if spec.get("has_via", True):
            segs.append(Segment((vx, vy, z1), (vx, vy, z2), I, f"bench_via_{idx}", "via"))
        segs.extend(segments_from_path(l2, I, f"bench_L2_{idx}", "layer2"))
    if meta["scenario"] == "ood":
        I_bg = meta.get("background_current_A", meta["paths"][0]["current_A"] if meta.get("paths") else meta["current_A"])
        segs.append(Segment((-0.9e-3, -0.33e-3, z1), (0.9e-3, -0.33e-3, z1), -0.7 * I_bg, "ood_background", "layer1"))
    return segs


def finite_width_return_surrogate_segments(
    segments,
    width_m: float = 28e-6,
    via_radius_m: float = 18e-6,
    n_filaments: int = 3,
    return_scale: float = 0.22,
    ground_z_m: float = -0.24e-3,
):
    """Approximate line segments with finite-width filaments and weak returns."""
    out = []
    for seg in segments:
        p0 = np.asarray(seg.p0, dtype=float)
        p1 = np.asarray(seg.p1, dtype=float)
        direction = p1 - p0
        dxy = direction[:2]
        if np.linalg.norm(dxy) > 0:
            tangent = dxy / np.linalg.norm(dxy)
            normal = np.array([-tangent[1], tangent[0], 0.0])
            offsets = np.linspace(-0.5, 0.5, n_filaments) * width_m
            for k, off in enumerate(offsets):
                shift = normal * off
                out.append(Segment(tuple(p0 + shift), tuple(p1 + shift), seg.I_A / n_filaments, f"{seg.name}_fw{k}", seg.group))
                gp0 = p0 + shift
                gp1 = p1 + shift
                gp0[2] = ground_z_m
                gp1[2] = ground_z_m
                out.append(Segment(tuple(gp0), tuple(gp1), -return_scale * seg.I_A / n_filaments, f"{seg.name}_ret{k}", "return"))
        else:
            offsets = [(0.0, 0.0), (via_radius_m, 0.0), (-via_radius_m, 0.0), (0.0, via_radius_m), (0.0, -via_radius_m)]
            for k, (ox, oy) in enumerate(offsets):
                shift = np.array([ox, oy, 0.0])
                out.append(Segment(tuple(p0 + shift), tuple(p1 + shift), seg.I_A / len(offsets), f"{seg.name}_viafw{k}", seg.group))
    return out


def compute_forward_realism_probe(cfg, benchmark, max_samples: int = 18):
    """Quantify the gap between centerline data and a finite-width/return surrogate."""
    bcfg = cfg["benchmark_dataset"]
    pcfg = cfg["physics"]
    X, Y, Z = make_grid(bcfg["fov_m"], bcfg["n"], cfg["grid"].get("sensor_z_m", 0.0))
    meta = json.loads(benchmark["metadata_json"])
    split = benchmark["split"]
    candidate_idx = [int(i) for i in np.where((split == "test") | (split == "ood"))[0][:max_samples]]
    rel_diffs = []
    rel_diffs_by_split = {}
    for idx in candidate_idx:
        centerline = benchmark_segments_from_meta(meta[idx], pcfg["layer1_z_m"], pcfg["layer2_z_m"])
        surrogate = finite_width_return_surrogate_segments(centerline)
        b_low = field_from_segments(X, Y, Z, centerline, n_quad=max(12, bcfg["n_quad"] // 2))
        b_high = field_from_segments(X, Y, Z, surrogate, n_quad=max(12, bcfg["n_quad"] // 2))
        diff = float(np.linalg.norm(b_high - b_low) / (np.linalg.norm(b_low) + 1e-30))
        rel_diffs.append(diff)
        rel_diffs_by_split.setdefault(str(split[idx]), []).append(diff)
    return {
        "model": "finite-width filaments + weak ground-return surrogate",
        "n_samples": len(rel_diffs),
        "median_rel_l2_gap": float(np.median(rel_diffs)) if rel_diffs else 0.0,
        "max_rel_l2_gap": float(np.max(rel_diffs)) if rel_diffs else 0.0,
        "by_split_median_rel_l2_gap": {
            k: float(np.median(v)) for k, v in rel_diffs_by_split.items()
        },
        "boundary": "diagnostic only; dataset labels remain centerline line-current truth",
    }


def recoverability_summary(benchmark):
    meta = json.loads(benchmark["metadata_json"])
    out = {}
    for split in sorted(set(benchmark["split"].tolist())):
        idx = np.where(benchmark["split"] == split)[0]
        rows = [meta[int(i)] for i in idx]
        truth = benchmark["truth"][idx]
        b_clean = benchmark["B_clean"][idx]
        b_obs = benchmark["B_obs"][idx]
        s_peak = np.max(np.abs(truth[:, 4]).reshape(len(idx), -1), axis=1)
        no_via = np.array([row["route_kind"].startswith("no_via") for row in rows], dtype=bool)
        multi_or_dense = np.array([row["route_kind"] in {"multi_via", "dense_via_background"} for row in rows], dtype=bool)
        background = np.array(["background" in row["route_kind"] for row in rows], dtype=bool)
        noise = b_obs - b_clean
        snr = np.linalg.norm(b_clean.reshape(len(idx), -1), axis=1) / (np.linalg.norm(noise.reshape(len(idx), -1), axis=1) + 1e-30)
        out[split] = {
            "n": int(len(idx)),
            "via_present_fraction": float(np.mean(s_peak > 0.0)),
            "no_via_fraction": float(np.mean(no_via)),
            "multi_or_dense_via_fraction": float(np.mean(multi_or_dense)),
            "background_stress_fraction": float(np.mean(background)),
            "median_observation_snr_proxy": float(np.median(snr)),
            "min_observation_snr_proxy": float(np.min(snr)),
        }
    return out


def route_kind_for_sample(split: str, index: int) -> str:
    if split == "ood":
        return ["both_jog_background", "dense_via_background", "no_via_background"][index % 3]
    return ["straight", "l1_jog", "l2_jog", "both_jog", "multi_via", "no_via"][index % 6]


def make_path_spec(rng, bcfg, pcfg, route_kind: str, split: str, current_scale: float = 1.0):
    ood = split == "ood"
    via_span = 0.33 if not ood else 0.42
    vx = rng.uniform(-via_span, via_span) * bcfg["fov_m"]
    vy = rng.uniform(-via_span, via_span) * bcfg["fov_m"]
    left_x = -0.5 * bcfg["fov_m"] + rng.uniform(0.12, 0.30) * bcfg["fov_m"]
    right_x = 0.5 * bcfg["fov_m"] - rng.uniform(0.12, 0.30) * bcfg["fov_m"]
    I = pcfg["current_A"] * current_scale * rng.uniform(0.65, 1.35) * (1.0 if rng.random() > 0.2 else -1.0)
    jog_sign = 1 if rng.random() > 0.5 else -1
    left_y = clipped_y(vy + jog_sign * rng.uniform(0.08, 0.22) * bcfg["fov_m"], bcfg["fov_m"])
    right_y = clipped_y(vy - jog_sign * rng.uniform(0.08, 0.22) * bcfg["fov_m"], bcfg["fov_m"])
    return {
        "route_kind": route_kind,
        "has_via": route_kind not in {"no_via", "no_via_background"},
        "current_A": float(I),
        "via_x_m": float(vx),
        "via_y_m": float(vy),
        "left_x_m": float(left_x),
        "right_x_m": float(right_x),
        "left_y_m": left_y,
        "right_y_m": right_y,
    }


def make_sample_meta(rng, bcfg, pcfg, split: str, sample_idx: int):
    route_kind = route_kind_for_sample(split, sample_idx)
    scenario = "ood" if split == "ood" else "id"
    if route_kind == "multi_via":
        child_kinds = ["l1_jog", "l2_jog"]
        paths = [make_path_spec(rng, bcfg, pcfg, k, split, current_scale=0.75) for k in child_kinds]
    elif route_kind == "dense_via_background":
        child_kinds = ["both_jog_background", "l1_jog", "l2_jog"]
        paths = [make_path_spec(rng, bcfg, pcfg, k, split, current_scale=0.55) for k in child_kinds]
    elif route_kind == "no_via_background":
        paths = [make_path_spec(rng, bcfg, pcfg, "no_via_background", split, current_scale=0.9)]
    else:
        paths = [make_path_spec(rng, bcfg, pcfg, route_kind, split)]
    first = paths[0]
    return {
        "split": split,
        "scenario": scenario,
        "route_kind": route_kind,
        "paths": paths,
        "background_current_A": float(first["current_A"]),
        # Compatibility fields for older readers and quick inspection.
        "current_A": float(first["current_A"]),
        "via_x_m": float(first["via_x_m"]),
        "via_y_m": float(first["via_y_m"]),
        "left_x_m": float(first["left_x_m"]),
        "right_x_m": float(first["right_x_m"]),
        "left_y_m": float(first["left_y_m"]),
        "right_y_m": float(first["right_y_m"]),
    }


def truth_channel_norms_by_split(benchmark):
    channels = ["J1x", "J1y", "J2x", "J2y", "s1"]
    out = {}
    for split in sorted(set(benchmark["split"].tolist())):
        arr = benchmark["truth"][benchmark["split"] == split]
        out[split] = {
            ch: float(np.linalg.norm(arr[:, i]))
            for i, ch in enumerate(channels)
        }
    return out


def route_kind_counts(benchmark):
    meta = json.loads(benchmark["metadata_json"])
    out = {}
    for row in meta:
        split = row["split"]
        out.setdefault(split, {})
        kind = row["route_kind"]
        out[split][kind] = out[split].get(kind, 0) + 1
    return out


def make_benchmark_dataset(cfg):
    bcfg = cfg["benchmark_dataset"]
    pcfg = cfg["physics"]
    rng = np.random.default_rng(bcfg["seed"])
    X, Y, Z = make_grid(bcfg["fov_m"], bcfg["n"], cfg["grid"].get("sensor_z_m", 0.0))
    split_names = []
    B_clean = []
    B_obs = []
    y_truth = []
    meta = []
    for split, count in bcfg["splits"].items():
        for sample_idx in range(int(count)):
            sample_meta = make_sample_meta(rng, bcfg, pcfg, split, sample_idx)
            segs = benchmark_segments_from_meta(sample_meta, pcfg["layer1_z_m"], pcfg["layer2_z_m"])
            B = field_from_segments(X, Y, Z, segs, n_quad=bcfg["n_quad"]).astype(np.float32)
            truth = route_truth_maps(bcfg["fov_m"], bcfg["n"], sample_meta, pcfg["layer1_z_m"], pcfg["layer2_z_m"])
            noise_rel = float(bcfg["noise_relative_to_max_abs_B"][split])
            sigma = noise_rel * (float(np.max(np.abs(B))) + 1e-30)
            Bn = (B + rng.normal(0.0, sigma, size=B.shape)).astype(np.float32)

            B_clean.append(B)
            B_obs.append(Bn)
            y_truth.append(truth)
            split_names.append(split)
            meta.append(sample_meta)
    return {
        "x": X[0, :].astype(np.float32),
        "y": Y[:, 0].astype(np.float32),
        "B_clean": np.stack(B_clean).astype(np.float32),
        "B_obs": np.stack(B_obs).astype(np.float32),
        "truth": np.stack(y_truth).astype(np.float32),
        "split": np.array(split_names),
        "metadata_json": json.dumps(meta),
    }


def background_swamping_stress(cfg, X, Y, Z, x, y, out):
    """A harder via-detection case where raw total-field matching is misleading."""
    p = cfg["physics"]
    I = p["current_A"]
    z1 = p["layer1_z_m"]
    z2 = p["layer2_z_m"]
    vx, vy = 0.23e-3, -0.17e-3
    segments = [
        Segment((-0.86e-3, vy, z1), (vx, vy, z1), I, "stress_L1_to_via", "layer1"),
        Segment((vx, vy, z1), (vx, vy, z2), I, "stress_via", "via"),
        Segment((vx, vy, z2), (0.82e-3, 0.35e-3, z2), I, "stress_L2_from_via", "layer2"),
        Segment((-0.90e-3, 0.12e-3, z1), (0.90e-3, 0.12e-3, z1), 4.0 * I, "strong_L1_background", "layer1"),
        Segment((0.12e-3, -0.90e-3, z2), (0.12e-3, 0.90e-3, z2), -3.2 * I, "strong_L2_background", "layer2"),
    ]
    B_total = field_from_segments(X, Y, Z, segments, n_quad=p["n_quad"])
    B_sheet = group_field(X, Y, Z, segments, "layer1", n_quad=p["n_quad"]) + group_field(X, Y, Z, segments, "layer2", n_quad=p["n_quad"])
    B_via = group_field(X, Y, Z, segments, "via", n_quad=p["n_quad"])
    residual = B_total - B_sheet
    template = Segment((0.0, 0.0, z1), (0.0, 0.0, z2), I, "stress_template", "via")
    B_template = field_from_segments(X, Y, Z, [template], n_quad=cfg["template"]["n_quad"])

    raw_score = normalized_template_score(B_total[..., :2], B_template[..., :2])
    residual_score = normalized_template_score(residual[..., :2], B_template[..., :2])
    raw_peak = peak_location(raw_score, x, y)
    residual_peak = peak_location(residual_score, x, y)
    true_xy = np.array([vx, vy])
    raw_err = float(np.linalg.norm(np.array([raw_peak["x_m"], raw_peak["y_m"]]) - true_xy))
    residual_err = float(np.linalg.norm(np.array([residual_peak["x_m"], residual_peak["y_m"]]) - true_xy))

    save_map_grid(
        [norm_field(B_total[..., :2]), norm_field(residual[..., :2]), raw_score, residual_score],
        ["stress |Bxy| total", "stress |Bxy| oracle residual", "raw matched filter", "residual matched filter"],
        x * 1e6,
        y * 1e6,
        out / "07_background_swamping_stress.png",
        cmap="magma",
    )
    return {
        "true_via_xy_m": true_xy.tolist(),
        "raw_peak": raw_peak,
        "residual_peak": residual_peak,
        "raw_localization_error_m": raw_err,
        "residual_localization_error_m": residual_err,
        "raw_peak_score": raw_peak["score"],
        "residual_peak_score": residual_peak["score"],
        "raw_to_residual_localization_error_ratio": raw_err / (residual_err + 1e-30),
        "via_to_sheet_Bxy_energy_ratio": float(np.linalg.norm(B_via[..., :2].ravel()) / (np.linalg.norm(B_sheet[..., :2].ravel()) + 1e-30)),
    }


def add_acceptance_gates(metrics, pixel_size_m):
    stress = metrics["background_swamping_stress"]
    bench = metrics["benchmark_dataset"]
    norms = bench["truth_channel_l2_norms_by_split"]
    route_counts = bench["route_kind_counts"]
    recoverability = bench.get("recoverability_summary", {})
    realism = metrics.get("forward_realism_probe", {})
    gates = {
        "field_superposition_is_linear": {
            "threshold": "relative_l2 < 1e-12",
            "value": metrics["superposition_rel_l2_error"],
            "pass": metrics["superposition_rel_l2_error"] < 1e-12,
        },
        "vertical_via_has_no_bz": {
            "threshold": "Bz/Bxy < 1e-10",
            "value": metrics["via"]["Bz_over_Bxy_max_ratio"],
            "pass": metrics["via"]["Bz_over_Bxy_max_ratio"] < 1e-10,
        },
        "finite_volume_topology_cancels_internal_via": {
            "threshold": "both residual ratios < 1e-12",
            "value": [
                metrics["topology"]["residual_to_div_norm_ratio_layer1"],
                metrics["topology"]["residual_to_div_norm_ratio_layer2"],
            ],
            "pass": (
                metrics["topology"]["residual_to_div_norm_ratio_layer1"] < 1e-12
                and metrics["topology"]["residual_to_div_norm_ratio_layer2"] < 1e-12
            ),
        },
        "stress_residual_filter_localizes_via": {
            "threshold": "residual localization error <= 2 pixels",
            "value": stress["residual_localization_error_m"],
            "pass": stress["residual_localization_error_m"] <= 2.0 * pixel_size_m,
        },
        "stress_raw_total_field_is_misleading": {
            "threshold": "raw localization error > residual localization error",
            "value": stress["raw_to_residual_localization_error_ratio"],
            "pass": stress["raw_localization_error_m"] > stress["residual_localization_error_m"],
        },
        "formal_benchmark_has_required_splits": {
            "threshold": "train/val/test/ood are all present",
            "value": bench["split_counts"],
            "pass": all(k in bench["split_counts"] and bench["split_counts"][k] > 0 for k in ["train", "val", "test", "ood"]),
        },
        "formal_benchmark_has_full_truth_maps": {
            "threshold": "truth channels are [J1x,J1y,J2x,J2y,s1]",
            "value": bench["truth_shape"],
            "pass": len(bench["truth_shape"]) == 4 and bench["truth_shape"][1] == 5,
        },
        "formal_benchmark_has_directional_current_diversity": {
            "threshold": "train/test J1y and J2y truth norms are nonzero",
            "value": {
                "train": {"J1y": norms["train"]["J1y"], "J2y": norms["train"]["J2y"]},
                "test": {"J1y": norms["test"]["J1y"], "J2y": norms["test"]["J2y"]},
            },
            "pass": (
                norms["train"]["J1y"] > 0.0
                and norms["train"]["J2y"] > 0.0
                and norms["test"]["J1y"] > 0.0
                and norms["test"]["J2y"] > 0.0
            ),
        },
        "formal_benchmark_has_route_kind_diversity": {
            "threshold": "ID train/test include straight, l1_jog, l2_jog, both_jog, multi_via, no_via; OOD includes background stress variants",
            "value": route_counts,
            "pass": (
                all(route_counts.get("train", {}).get(k, 0) > 0 for k in ["straight", "l1_jog", "l2_jog", "both_jog", "multi_via", "no_via"])
                and all(route_counts.get("test", {}).get(k, 0) > 0 for k in ["straight", "l1_jog", "l2_jog", "both_jog", "multi_via", "no_via"])
                and all(route_counts.get("ood", {}).get(k, 0) > 0 for k in ["both_jog_background", "dense_via_background", "no_via_background"])
            ),
        },
        "benchmark_reports_recoverability_health": {
            "threshold": "test has via/no-via diversity and OOD has background stress",
            "value": recoverability,
            "pass": (
                recoverability.get("test", {}).get("via_present_fraction", 0.0) > 0.0
                and recoverability.get("test", {}).get("no_via_fraction", 0.0) > 0.0
                and recoverability.get("ood", {}).get("background_stress_fraction", 0.0) > 0.5
            ),
        },
        "finite_width_return_surrogate_gap_is_quantified": {
            "threshold": "median surrogate gap is finite and > 1%",
            "value": realism.get("median_rel_l2_gap", None),
            "pass": bool(np.isfinite(realism.get("median_rel_l2_gap", np.nan)) and realism.get("median_rel_l2_gap", 0.0) > 0.01),
        },
    }
    metrics["acceptance_gates"] = gates
    metrics["all_acceptance_gates_passed"] = all(g["pass"] for g in gates.values())


def write_run_report(out, metrics):
    gate_lines = "\n".join(
        f"- {name}: {'PASS' if gate['pass'] else 'FAIL'}; value={gate['value']}; threshold={gate['threshold']}"
        for name, gate in metrics["acceptance_gates"].items()
    )
    stress = metrics["background_swamping_stress"]
    report = f"""# exp03 Run Report

## Role

MVP-2 two-layer + via toy benchmark. This experiment verifies multilayer field
superposition, finite-volume topology conservation, layer mixing, and via
detectability before any learned inverse model is trusted.

## Gate Summary

Overall: {'PASS' if metrics['all_acceptance_gates_passed'] else 'FAIL'}

{gate_lines}

## Stress Case

- raw total-field via localization error: `{stress['raw_localization_error_m'] * 1e6:.2f} um`
- residual matched-filter localization error: `{stress['residual_localization_error_m'] * 1e6:.2f} um`
- stress via/sheet Bxy energy ratio: `{stress['via_to_sheet_Bxy_energy_ratio']:.3e}`
- formal benchmark file: `{metrics['benchmark_dataset']['file']}`
- benchmark splits: `{metrics['benchmark_dataset']['split_counts']}`
- benchmark route kinds: `{metrics['benchmark_dataset']['route_kind_counts']}`
- benchmark truth channel norms: `{metrics['benchmark_dataset']['truth_channel_l2_norms_by_split']}`
- recoverability summary: `{metrics['benchmark_dataset']['recoverability_summary']}`
- finite-width/return surrogate median gap: `{metrics['forward_realism_probe']['median_rel_l2_gap']:.3f}`

## Boundary

This remains an ideal free-space toy benchmark. The residual detector uses
oracle sheet-background subtraction, so it is an upper bound on via detectability.
The finite-width/return-current probe quantifies a synthetic forward gap but
does not replace FEM, FastHenry, CAD/Gerber, or measured QDM validation.
"""
    (out / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def run(config_path: Path):
    ensure_dirs()
    cfg = load_cfg(config_path)
    out = ROOT / "outputs"
    data = ROOT / "data"
    X, Y, Z, x, y, segments, B_total, B_l1, B_l2, B_via, B_sum, maps = compute_example(cfg)
    x_um = x * 1e6
    y_um = y * 1e6

    # Geometry maps.
    save_map_grid(
        [maps["J1_vis"], maps["J2_vis"], maps["s"]],
        ["Layer 1 trace visual map", "Layer 2 trace visual map", "Via s map (+ L1→L2)"],
        x_um, y_um, out / "01_two_layer_geometry.png"
    )

    # B decomposition.
    save_bxyz_panels(
        [B_total, B_l1, B_l2, B_via],
        ["total", "layer 1", "layer 2", "via"],
        x_um, y_um, out / "02_field_decomposition_Bxyz.png"
    )

    # Via matched filtering.
    template = via_template_at_center(cfg, X, Y, Z)
    residual_oracle = B_total - B_l1 - B_l2
    score_res = normalized_template_score(residual_oracle[..., :2], template[..., :2])
    score_raw = normalized_template_score(B_total[..., :2], template[..., :2])
    peak_res = peak_location(score_res, x, y)
    peak_raw = peak_location(score_raw, x, y)
    true_xy = np.array([cfg["physics"]["via_x_m"], cfg["physics"]["via_y_m"]])
    loc_res = np.array([peak_res["x_m"], peak_res["y_m"]])
    loc_raw = np.array([peak_raw["x_m"], peak_raw["y_m"]])
    save_map_grid(
        [norm_field(B_via[..., :2]), norm_field(residual_oracle[..., :2]), score_res, score_raw],
        ["|Bxy| via template/contribution", "|Bxy| oracle residual", "matched filter on residual", "matched filter on raw total"],
        x_um, y_um, out / "03_via_template_matched_filter.png",
        cmap="magma"
    )

    # Topology maps.
    inner = maps["inner_mask"]
    res1_inner_norm = float(np.linalg.norm(maps["res1"][inner]))
    res2_inner_norm = float(np.linalg.norm(maps["res2"][inner]))
    div1_inner_norm = float(np.linalg.norm(maps["div1"][inner]))
    div2_inner_norm = float(np.linalg.norm(maps["div2"][inner]))
    save_map_grid(
        [maps["div1"], maps["div2"], maps["s"], maps["res1"], maps["res2"]],
        ["div J1", "div J2", "s1", "div J1 + s1", "div J2 - s1"],
        x_um, y_um, out / "04_topology_constraint_residual.png",
        cmap="coolwarm"
    )

    # Layer mixing and via SNR indicators.
    offsets, sims, amp_ratios = compute_layer_mixing(cfg, X, Y, Z)
    save_line_plot(offsets * 1e6, [sims, amp_ratios], ["template cosine similarity", "deep/shallow max |B|"], "Layer depth offset from shallow layer (µm)", "value", "Layer mixing indicators", out / "05_layer_mixing_and_snr.png")

    # Dataset generation and sample plot.
    Xd, Yd, Bds, via_xyI, source_counts = make_small_dataset(cfg)
    np.savez_compressed(data / "toy_dataset_small.npz", B=Bds, via_xyI=via_xyI, source_counts=source_counts, x=Xd[0, :], y=Yd[:, 0], config=json.dumps(cfg))
    sample_maps = [norm_field(Bds[i]) * 1e6 for i in range(min(4, Bds.shape[0]))]
    sample_titles = [f"sample {i}: |B| (µT)" for i in range(len(sample_maps))]
    save_map_grid(sample_maps, sample_titles, Xd[0, :] * 1e6, Yd[:, 0] * 1e6, out / "06_toy_dataset_samples.png", cmap="viridis")

    benchmark = make_benchmark_dataset(cfg)
    np.savez_compressed(data / "two_layer_via_benchmark.npz", **benchmark)
    split_counts = {name: int(np.sum(benchmark["split"] == name)) for name in sorted(set(benchmark["split"].tolist()))}
    channel_norms = truth_channel_norms_by_split(benchmark)
    route_counts = route_kind_counts(benchmark)
    recoverability = recoverability_summary(benchmark)
    forward_realism = compute_forward_realism_probe(cfg, benchmark)
    # Show one ID and one OOD truth/input pair so dataset regressions are visible.
    id_idx = int(np.where(benchmark["split"] == "test")[0][0])
    ood_idx = int(np.where(benchmark["split"] == "ood")[0][0])
    save_map_grid(
        [
            norm_field(benchmark["B_obs"][id_idx]) * 1e6,
            np.sqrt(np.sum(benchmark["truth"][id_idx, :4] ** 2, axis=0)),
            np.abs(benchmark["truth"][id_idx, 4]),
            norm_field(benchmark["B_obs"][ood_idx]) * 1e6,
            np.sqrt(np.sum(benchmark["truth"][ood_idx, :4] ** 2, axis=0)),
            np.abs(benchmark["truth"][ood_idx, 4]),
        ],
        ["ID |B|", "ID |J_sheet|", "ID |s1|", "OOD |B|", "OOD |J_sheet|", "OOD |s1|"],
        benchmark["x"] * 1e6,
        benchmark["y"] * 1e6,
        out / "08_benchmark_dataset_examples.png",
        cmap="viridis",
    )

    stress_metrics = background_swamping_stress(cfg, X, Y, Z, x, y, out)

    # Save example.
    np.savez_compressed(
        data / "two_layer_via_example.npz",
        x=x, y=y, B_total=B_total, B_l1=B_l1, B_l2=B_l2, B_via=B_via, template=template,
        score_residual=score_res, score_raw=score_raw, div1=maps["div1"], div2=maps["div2"], s=maps["s"], res1=maps["res1"], res2=maps["res2"], config=json.dumps(cfg)
    )

    superposition_err = rel_l2(B_total, B_sum)
    via_bxy_max = float(np.max(norm_field(B_via[..., :2])))
    via_bz_max = float(np.max(np.abs(B_via[..., 2])))
    sheet_bxy_max = float(np.max(norm_field((B_l1 + B_l2)[..., :2])))
    via_energy_ratio = float(np.linalg.norm(B_via[..., :2].ravel()) / (np.linalg.norm((B_l1 + B_l2)[..., :2].ravel()) + 1e-30))
    metrics = {
        "experiment": "exp03-two-layer-via-toy-benchmark",
        "stage": "MVP-2: two-layer + via toy benchmark before neural topology loss",
        "units": {"length": "m internally", "current": "A", "magnetic_field": "T"},
        "config_summary": cfg,
        "superposition_rel_l2_error": superposition_err,
        "via": {
            "max_abs_Bxy_T": via_bxy_max,
            "max_abs_Bz_T": via_bz_max,
            "Bz_over_Bxy_max_ratio": via_bz_max / (via_bxy_max + 1e-30),
            "via_to_sheet_Bxy_max_ratio": via_bxy_max / (sheet_bxy_max + 1e-30),
            "via_to_sheet_Bxy_energy_ratio": via_energy_ratio,
        },
        "matched_filter": {
            "true_via_xy_m": true_xy.tolist(),
            "residual_peak": peak_res,
            "raw_peak": peak_raw,
            "residual_localization_error_m": float(np.linalg.norm(loc_res - true_xy)),
            "raw_localization_error_m": float(np.linalg.norm(loc_raw - true_xy)),
            "residual_peak_score": peak_res["score"],
            "raw_peak_score": peak_raw["score"],
        },
        "topology": {
            "res1_inner_l2": res1_inner_norm,
            "res2_inner_l2": res2_inner_norm,
            "div1_inner_l2_before_topology": div1_inner_norm,
            "div2_inner_l2_before_topology": div2_inner_norm,
            "residual_to_div_norm_ratio_layer1": res1_inner_norm / (div1_inner_norm + 1e-30),
            "residual_to_div_norm_ratio_layer2": res2_inner_norm / (div2_inner_norm + 1e-30),
        },
        "layer_mixing": {
            "depth_offsets_um": (offsets * 1e6).tolist(),
            "template_cosine_similarity": sims.tolist(),
            "deep_to_shallow_max_abs_B_ratio": amp_ratios.tolist(),
        },
        "toy_dataset": {
            "n_samples": int(Bds.shape[0]),
            "shape_B": list(Bds.shape),
            "file": "data/toy_dataset_small.npz"
        },
        "benchmark_dataset": {
            "file": "data/two_layer_via_benchmark.npz",
            "B_obs_shape": list(benchmark["B_obs"].shape),
            "truth_shape": list(benchmark["truth"].shape),
            "split_counts": split_counts,
            "channels": ["J1x", "J1y", "J2x", "J2y", "s1"],
            "truth_channel_l2_norms_by_split": channel_norms,
            "route_kind_counts": route_counts,
            "recoverability_summary": recoverability,
            "label_note": "truth maps are raster labels for current support and via amplitude; finite-volume topology is validated separately in the topology gate",
        },
        "forward_realism_probe": forward_realism,
        "background_swamping_stress": stress_metrics,
        "limitations": [
            "Ideal free-space finite-line Biot-Savart only.",
            "Finite-width/return-current effects are only quantified as a surrogate gap, not used as ground-truth FEM.",
            "No QDM PSF, NV projection noise, standoff tilt, or FEM validation yet.",
            "Matched filtering uses an oracle sheet-background subtraction to show an upper bound of via detectability; raw score is also reported to expose background swamping."
        ]
    }
    pixel_size_m = float(x[1] - x[0])
    add_acceptance_gates(metrics, pixel_size_m)
    with open(out / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    gate_lines = "\n".join(
        f"- {name}: {'PASS' if gate['pass'] else 'FAIL'}; value={gate['value']}; threshold={gate['threshold']}"
        for name, gate in metrics["acceptance_gates"].items()
    )
    report = f"""# RUN_REPORT

## Summary

Experiment exp03 completed.

Acceptance gates: `{'PASS' if metrics['all_acceptance_gates_passed'] else 'FAIL'}`

{gate_lines}

## Key metrics

- Superposition relative L2 error: `{superposition_err:.3e}`
- Via Bz/Bxy max ratio: `{metrics['via']['Bz_over_Bxy_max_ratio']:.3e}`
- Via-to-sheet Bxy energy ratio: `{via_energy_ratio:.3e}`
- Residual matched-filter localization error: `{metrics['matched_filter']['residual_localization_error_m']*1e6:.2f} µm`
- Raw matched-filter localization error: `{metrics['matched_filter']['raw_localization_error_m']*1e6:.2f} µm`
- Topology residual ratio layer1: `{metrics['topology']['residual_to_div_norm_ratio_layer1']:.3e}`
- Topology residual ratio layer2: `{metrics['topology']['residual_to_div_norm_ratio_layer2']:.3e}`
- Stress raw localization error: `{stress_metrics['raw_localization_error_m']*1e6:.2f} µm`
- Stress residual localization error: `{stress_metrics['residual_localization_error_m']*1e6:.2f} µm`
- Benchmark route kinds: `{route_counts}`
- Benchmark truth channel norms: `{channel_norms}`
- Recoverability summary: `{recoverability}`
- Finite-width/return surrogate median forward gap: `{forward_realism['median_rel_l2_gap']:.3f}`

## Interpretation

This experiment verifies the minimum two-layer + via physics before neural inversion:

1. B-field decomposition is linear.
2. An ideal vertical via produces almost no Bz and mainly Bxy circulation.
3. Via detection is much easier after sheet-background subtraction; raw total-field matching can fail or shift, exposing the swamping risk.
4. The finite-volume topology residual cancels the via source/sink inside the FOV when boundary ports are excluded.
5. Layer template similarity remains high for small depth offsets, motivating later topology constraints and observability gates.
6. A finite-width/return-current surrogate creates a measurable forward gap,
   so same-family centerline synthetic performance must not be treated as
   real hardware validation.
"""
    with open(out / "RUN_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    return metrics


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=ROOT / "configs" / "default.json")
    args = ap.parse_args()
    m = run(args.config)
    print(json.dumps({
        "superposition_rel_l2_error": m["superposition_rel_l2_error"],
        "via_Bz_over_Bxy": m["via"]["Bz_over_Bxy_max_ratio"],
        "residual_via_loc_error_um": m["matched_filter"]["residual_localization_error_m"] * 1e6,
        "raw_via_loc_error_um": m["matched_filter"]["raw_localization_error_m"] * 1e6,
        "topology_residual_ratio_l1": m["topology"]["residual_to_div_norm_ratio_layer1"],
        "topology_residual_ratio_l2": m["topology"]["residual_to_div_norm_ratio_layer2"],
    }, indent=2))
