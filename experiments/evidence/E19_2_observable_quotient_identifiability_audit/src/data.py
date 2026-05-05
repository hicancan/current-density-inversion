"""Generated E19.2 OQCI data cases with adversarial pair and oracle generators.

Standard cases are reused from E19.1. New generators produce:
- Adversarial pairs: (z1, z2) where ||F(z1)-F(z2)|| <= epsilon but L(z1) != L(z2)
- Oracle cases: cases generated exactly from a hypothesis basis.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import numpy as np

from operators import (
    OperatorBundle, empty_current, add_gaussian_sheet_mode,
    add_via_spot, add_return_loop,
)
from hypotheses import registration_pattern, standoff_laplacian_pattern


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


@dataclass
class AdversarialPair:
    pair_id: str
    state_a: np.ndarray
    state_b: np.ndarray
    label_a: str
    label_b: str
    forward_distance: float


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


def _noise(bundle: OperatorBundle, cfg: dict, rng: np.random.Generator) -> np.ndarray:
    sigma = float(cfg["noise_sigma"])
    return rng.normal(0.0, sigma, size=bundle.A.shape[0])


def _tile_for_multi_height(pattern: np.ndarray, bundle: OperatorBundle) -> np.ndarray:
    """Tile a single-height observation pattern for multi-height stacks."""
    n_heights = max(1, len(bundle.heights) if bundle.heights else 1)
    obs_per_height = bundle.A.shape[0] // n_heights if n_heights > 0 else pattern.size
    if n_heights > 1 and pattern.size == obs_per_height:
        return np.tile(pattern, n_heights)
    return pattern


def generate_case(bundle: OperatorBundle, cfg: dict, family: str, index: int, rng: np.random.Generator) -> GeneratedCase:
    n = int(bundle.index["n"])
    truth = FAMILY_TO_TRUTH[family]
    current = _smooth_background_current(bundle, rng)
    model_gap = np.zeros(bundle.A.shape[0], dtype=float)
    metadata: dict = {"generator": "E19_2_OQCI_v1"}

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
        metadata["gap_type"] = "registration_gradient"

    elif family == "model_gap_standoff":
        metadata["gap_type"] = "standoff_laplacian"

    elif family == "return_path_deep_loop":
        add_return_loop(current, bundle, layer=int(bundle.index["layers"]) - 1, amplitude=rng.normal(0.9, 0.1))
        metadata["return_path"] = "deep_layer_loop"

    clean = bundle.A @ current

    if family == "model_gap_registration":
        model_gap = registration_pattern(n, (n / 2, n / 2), max(1.5, n / 6.0), 0.12 * max(np.linalg.norm(clean), 1e-12))
        model_gap = _tile_for_multi_height(model_gap, bundle)
    elif family == "model_gap_standoff":
        # For multi-height, use single-height clean for pattern, then tile
        single_clean = clean[:bundle.A.shape[0] // max(1, len(bundle.heights or [1]))] if bundle.heights and len(bundle.heights) > 1 else clean
        model_gap = standoff_laplacian_pattern(single_clean, 0.20 * max(np.linalg.norm(single_clean), 1e-12))
        model_gap = _tile_for_multi_height(model_gap, bundle)

    observed = clean + model_gap + _noise(bundle, cfg, rng)
    return GeneratedCase(
        case_id=f"E19_2_{family}_{index:03d}",
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


# ── adversarial pair generation ──

def generate_adversarial_pairs(bundle: OperatorBundle, cfg: dict) -> list[AdversarialPair]:
    """Construct pairs of states that are forward-close but have different labels.

    Strategy:
    1. H0 vs H1: take a via-containing current and create a nearby no-via current
       by canceling the via spot and adjusting nearby sheet currents.
    2. H1 vs H3: a via current vs the same current with a deep return loop added.
    3. H0 vs H3: no-via vs deep return loop (should be far).
    """
    rng = _rng_for(cfg)
    n = int(bundle.index["n"])
    count = int(cfg["adversarial_pair_count"])
    pairs: list[AdversarialPair] = []

    # Pair type 1: H0 vs H1 (no-via vs small via)
    for i in range(max(1, count // 3)):
        base = _smooth_background_current(bundle, rng)
        via_state = base.copy()
        center = (n // 2, n // 2)
        add_via_spot(via_state, bundle, 0, 1, center, amplitude=0.15, radius=0)

        no_via_state = base.copy()
        add_gaussian_sheet_mode(no_via_state, bundle, 0, "x", center, max(1.5, n / 7.0), 0.04)
        add_gaussian_sheet_mode(no_via_state, bundle, 0, "y", center, max(1.5, n / 7.0), -0.04)

        f_a = bundle.A @ via_state
        f_b = bundle.A @ no_via_state
        dist = float(np.linalg.norm(f_a - f_b))
        pairs.append(AdversarialPair(
            pair_id=f"adv_H0_H1_{i:03d}",
            state_a=via_state, state_b=no_via_state,
            label_a="H1_via", label_b="H0_no_via",
            forward_distance=dist,
        ))

    # Pair type 2: H1 vs H3 (via vs return loop)
    for i in range(max(1, count // 3)):
        base = _smooth_background_current(bundle, rng)
        via_state = base.copy()
        center = (int(rng.integers(n // 3, 2 * n // 3)), int(rng.integers(n // 3, 2 * n // 3)))
        add_via_spot(via_state, bundle, 0, 1, center, amplitude=0.8, radius=0)

        return_state = base.copy()
        add_return_loop(return_state, bundle, layer=int(bundle.index["layers"]) - 1, amplitude=0.3)

        f_a = bundle.A @ via_state
        f_b = bundle.A @ return_state
        dist = float(np.linalg.norm(f_a - f_b))
        pairs.append(AdversarialPair(
            pair_id=f"adv_H1_H3_{i:03d}",
            state_a=via_state, state_b=return_state,
            label_a="H1_via", label_b="H3_return_path",
            forward_distance=dist,
        ))

    # Pair type 3: H0 vs H2 (no-via vs model-gap)
    for i in range(max(1, count - 2 * max(1, count // 3))):
        base = _smooth_background_current(bundle, rng)
        no_via_state = base.copy()
        f_no_via = bundle.A @ no_via_state

        gap_pattern = registration_pattern(n, (n / 2, n / 2), max(1.5, n / 6.0), 0.08 * max(np.linalg.norm(f_no_via), 1e-12))
        gap_pattern = _tile_for_multi_height(gap_pattern, bundle)
        f_gap = f_no_via + gap_pattern

        dist = float(np.linalg.norm(f_no_via - f_gap))
        pairs.append(AdversarialPair(
            pair_id=f"adv_H0_H2_{i:03d}",
            state_a=no_via_state, state_b=base.copy(),
            label_a="H0_no_via", label_b="H2_model_gap",
            forward_distance=dist,
        ))

    return pairs


# ── oracle test case generation ──

def generate_oracle_case(
    bundle: OperatorBundle, cfg: dict, hypothesis: str,
    rng: np.random.Generator, index: int = 0,
) -> GeneratedCase:
    """Generate a case whose clean field is exactly from one hypothesis basis.

    The current is a random linear combination of the H0 graph basis,
    optionally with hypothesis-specific additions.
    """
    n = int(bundle.index["n"])
    base = _smooth_background_current(bundle, rng)
    clean = bundle.A @ base
    model_gap = np.zeros(bundle.A.shape[0], dtype=float)
    family_map = {
        "H0_no_via": "no_via_clean",
        "H1_via": "single_via_observable",
        "H2_model_gap": "model_gap_registration",
        "H3_return_path": "return_path_deep_loop",
    }
    family = family_map.get(hypothesis, "no_via_clean")

    if hypothesis == "H1_via":
        center = (int(rng.integers(n // 3, 2 * n // 3)), int(rng.integers(n // 3, 2 * n // 3)))
        add_via_spot(base, bundle, 0, 1, center, amplitude=1.0, radius=0)

    elif hypothesis == "H3_return_path":
        add_return_loop(base, bundle, layer=int(bundle.index["layers"]) - 1, amplitude=0.8)

    elif hypothesis == "H2_model_gap":
        single_clean = bundle.A @ base
        model_gap = registration_pattern(n, (n / 2, n / 2), max(1.5, n / 6.0), 0.10 * max(np.linalg.norm(single_clean), 1e-12))
        model_gap = _tile_for_multi_height(model_gap, bundle)

    clean_after = bundle.A @ base
    observed = clean_after + model_gap + _noise(bundle, cfg, rng)

    return GeneratedCase(
        case_id=f"E19_2_oracle_{hypothesis}_{index:03d}",
        family=family,
        truth_hypothesis=hypothesis,
        current=base,
        field_clean=clean_after,
        field_observed=observed,
        model_gap_field=model_gap,
        metadata={"oracle": True, "hypothesis": hypothesis},
    )
