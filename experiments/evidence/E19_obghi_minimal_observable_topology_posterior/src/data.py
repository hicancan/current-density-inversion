"""Generated E19 data cases.

The cases are deliberately synthetic. They are designed to stress ambiguity
between candidate via, model-gap, and return-path explanations under one
controlled observation operator.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import numpy as np

from operators import (
    OperatorBundle,
    empty_current,
    add_gaussian_sheet_mode,
    add_via_spot,
    add_return_loop,
)


FAMILY_TO_TRUTH = {
    "no_via_clean": "H0_no_via",
    "single_via_observable": "H1_via",
    "dense_via_cluster": "H1_via",
    "model_gap_registration": "H2_model_gap",
    "model_gap_standoff": "H2_model_gap",
    "return_path_deep_loop": "H3_return_path",
}


@dataclass
class GeneratedCase:
    case_id: str
    family: str
    truth_hypothesis: str
    current: np.ndarray
    field_clean: np.ndarray
    field_observed: np.ndarray
    model_gap_field: np.ndarray
    metadata: dict

    def to_metrics_dict(self) -> dict:
        d = asdict(self)
        for k in ["current", "field_clean", "field_observed", "model_gap_field"]:
            d[k] = f"array{tuple(getattr(self, k).shape)}"
        return d


def _rng_for(cfg: dict) -> np.random.Generator:
    return np.random.default_rng(int(cfg["random_seed"]))


def _smooth_background_current(bundle: OperatorBundle, rng: np.random.Generator, scale: float = 1.0) -> np.ndarray:
    n = int(bundle.index["n"])
    x = empty_current(bundle)
    for layer in range(int(bundle.index["layers"])):
        amp = scale * rng.normal(0.75, 0.12) * (1.0 - 0.09 * layer)
        add_gaussian_sheet_mode(x, bundle, layer, "x", (n * 0.45, n * 0.52), max(2.0, n / 4.0), amp)
        add_gaussian_sheet_mode(x, bundle, layer, "y", (n * 0.58, n * 0.46), max(2.0, n / 4.0), 0.35 * amp)
    return x


def _gap_registration_pattern(bundle: OperatorBundle, rng: np.random.Generator, amplitude: float) -> np.ndarray:
    n = int(bundle.index["n"])
    yy, xx = np.mgrid[0:n, 0:n]
    cx = n * rng.uniform(0.35, 0.65)
    cy = n * rng.uniform(0.35, 0.65)
    sig = max(1.4, n / 6.0)
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sig**2))
    gx = np.gradient(g, axis=1)
    gy = np.gradient(g, axis=0)
    out = np.zeros((3, n, n), dtype=float)
    out[0] = amplitude * gx
    out[1] = amplitude * gy
    out[2] = 0.5 * amplitude * (gx - gy)
    out -= np.mean(out, axis=(1, 2), keepdims=True)
    return out.reshape(-1)


def _gap_standoff_pattern(bundle: OperatorBundle, clean_field: np.ndarray, amplitude: float) -> np.ndarray:
    n = int(bundle.index["n"])
    f = clean_field.reshape(3, n, n)
    lap = np.zeros_like(f)
    for c in range(3):
        arr = f[c]
        lap[c] = (
            -4 * arr
            + np.roll(arr, 1, axis=0)
            + np.roll(arr, -1, axis=0)
            + np.roll(arr, 1, axis=1)
            + np.roll(arr, -1, axis=1)
        )
    norm = np.linalg.norm(lap.ravel())
    if norm > 0:
        lap = lap / norm
    return amplitude * lap.reshape(-1)


def _noise(bundle: OperatorBundle, cfg: dict, rng: np.random.Generator) -> np.ndarray:
    sigma = float(cfg["noise_sigma"])
    return rng.normal(0.0, sigma, size=bundle.A.shape[0])


def generate_case(bundle: OperatorBundle, cfg: dict, family: str, index: int, rng: np.random.Generator) -> GeneratedCase:
    n = int(bundle.index["n"])
    truth = FAMILY_TO_TRUTH[family]
    current = _smooth_background_current(bundle, rng)
    model_gap = np.zeros(bundle.A.shape[0], dtype=float)
    metadata: dict = {"generator": "E19_generated_obghi_v1"}

    if family == "single_via_observable":
        center = (int(rng.integers(n // 3, 2 * n // 3)), int(rng.integers(n // 3, 2 * n // 3)))
        layer0 = int(rng.integers(0, int(bundle.index["layers"]) - 1))
        add_via_spot(current, bundle, layer0, layer0 + 1, center, amplitude=rng.normal(1.3, 0.12), radius=0)
        metadata.update({"via_center": center, "via_layer_pair": [layer0, layer0 + 1]})

    elif family == "dense_via_cluster":
        center = (int(rng.integers(n // 3, 2 * n // 3)), int(rng.integers(n // 3, 2 * n // 3)))
        layer0 = int(rng.integers(0, int(bundle.index["layers"]) - 1))
        add_via_spot(current, bundle, layer0, layer0 + 1, center, amplitude=rng.normal(0.95, 0.08), radius=1)
        metadata.update({"via_center": center, "via_layer_pair": [layer0, layer0 + 1], "dense_radius": 1})

    elif family == "model_gap_registration":
        # No true via; observation-space residual mimics a local magnetic anomaly.
        metadata["gap_type"] = "registration_gradient"

    elif family == "model_gap_standoff":
        metadata["gap_type"] = "standoff_laplacian"

    elif family == "return_path_deep_loop":
        add_return_loop(current, bundle, layer=int(bundle.index["layers"]) - 1, amplitude=rng.normal(0.9, 0.1))
        metadata["return_path"] = "deep_layer_loop"

    clean = bundle.A @ current

    if family == "model_gap_registration":
        model_gap = _gap_registration_pattern(bundle, rng, amplitude=0.12 * max(np.linalg.norm(clean), 1e-12))
    elif family == "model_gap_standoff":
        model_gap = _gap_standoff_pattern(bundle, clean, amplitude=0.20 * max(np.linalg.norm(clean), 1e-12))

    observed = clean + model_gap + _noise(bundle, cfg, rng)
    return GeneratedCase(
        case_id=f"E19_{family}_{index:03d}",
        family=family,
        truth_hypothesis=truth,
        current=current,
        field_clean=clean,
        field_observed=observed,
        model_gap_field=model_gap,
        metadata=metadata,
    )


def generate_cases(bundle: OperatorBundle, cfg: dict) -> list[GeneratedCase]:
    rng = _rng_for(cfg)
    cases: list[GeneratedCase] = []
    count = int(cfg["case_count_per_family"])
    for family in cfg["families"]:
        if family not in FAMILY_TO_TRUTH:
            raise ValueError(f"Unknown generated family: {family}")
        for i in range(count):
            cases.append(generate_case(bundle, cfg, family, i, rng))
    return cases
