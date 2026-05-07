"""Generated E20 OQCI data cases with multi-state support.

Adapted from E19.2 data.py. Supports multi-height field observation tiling
and multi-state excitation perturbation.
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


def _rng_for(cfg: dict) -> np.random.Generator:
    return np.random.default_rng(int(cfg["random_seed"]))


def _smooth_background_current(bundle: OperatorBundle, rng: np.random.Generator, scale: float = 1.0) -> np.ndarray:
    n = int(bundle.index["n"]); curr_dim = bundle.A.shape[1]
    x = np.zeros(curr_dim, dtype=float)
    for layer in range(int(bundle.index["layers"])):
        amp = scale * rng.normal(0.75, 0.12) * (1.0 - 0.09 * layer)
        add_gaussian_sheet_mode(x, bundle, layer, "x", (n * 0.45, n * 0.52), max(2.0, n / 4.0), amp)
        add_gaussian_sheet_mode(x, bundle, layer, "y", (n * 0.58, n * 0.46), max(2.0, n / 4.0), 0.35 * amp)
    return x


def _noise(bundle: OperatorBundle, cfg: dict, rng: np.random.Generator) -> np.ndarray:
    return rng.normal(0.0, float(cfg["noise_sigma"]), size=bundle.A.shape[0])


def _tile_for_multi_height(pattern: np.ndarray, bundle: OperatorBundle) -> np.ndarray:
    n_heights = max(1, len(bundle.heights) if bundle.heights else 1)
    if n_heights <= 1:
        return pattern
    per_height = bundle.A_per_height
    if per_height is None:
        return np.tile(pattern, n_heights)
    parts = []
    for A_h in per_height.values():
        h_rows = A_h.shape[0]
        if h_rows == pattern.size:
            parts.append(pattern)
        else:
            parts.append(np.zeros(h_rows, dtype=float))
    return np.concatenate(parts) if parts else pattern


def generate_case(bundle: OperatorBundle, cfg: dict, family: str, index: int, rng: np.random.Generator) -> GeneratedCase:
    n = int(bundle.index["n"])
    truth = FAMILY_TO_TRUTH[family]
    current = _smooth_background_current(bundle, rng)
    model_gap = np.zeros(bundle.A.shape[0], dtype=float)
    metadata: dict = {"generator": "E20_OQCI_v2"}

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
        if bundle.heights and len(bundle.heights) > 1 and bundle.A_per_height:
            first_A = next(iter(bundle.A_per_height.values()))
            single_clean = clean[:first_A.shape[0]]
        else:
            single_clean = clean
        model_gap = standoff_laplacian_pattern(single_clean, 0.20 * max(np.linalg.norm(single_clean), 1e-12))
        model_gap = _tile_for_multi_height(model_gap, bundle)

    observed = clean + model_gap + _noise(bundle, cfg, rng)
    return GeneratedCase(
        case_id=f"E20_{family}_{index:03d}", family=family,
        truth_hypothesis=truth, current=current,
        field_clean=clean, field_observed=observed,
        model_gap_field=model_gap, metadata=metadata,
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


# ── multi-state case generation ───────────────────────────────────────────

def _perturb_via_sensitive(bundle: OperatorBundle, base: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Perturbation that amplifies via-current signal."""
    n = int(bundle.index["n"]); layers = int(bundle.index["layers"])
    x = base.copy()
    for layer in range(layers - 1):
        cx, cy = rng.integers(n // 3, 2 * n // 3), rng.integers(n // 3, 2 * n // 3)
        add_via_spot(x, bundle, layer, layer + 1, (int(cx), int(cy)), rng.normal(0.5, 0.08), radius=0)
    return x


def _perturb_return_sensitive(bundle: OperatorBundle, base: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Perturbation that amplifies deep-layer return current."""
    x = base.copy()
    add_return_loop(x, bundle, layer=int(bundle.index["layers"]) - 1, amplitude=rng.normal(0.6, 0.1))
    return x


def _perturb_gap_sensitive(bundle: OperatorBundle, base: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Perturbation that shifts smooth sheet modes to simulate registration/model gap."""
    n = int(bundle.index["n"]); layers = int(bundle.index["layers"])
    x = base.copy()
    for layer in range(layers):
        add_gaussian_sheet_mode(x, bundle, layer, "x", (n * 0.48, n * 0.51), max(1.5, n / 6.0), rng.normal(0.15, 0.03))
        add_gaussian_sheet_mode(x, bundle, layer, "y", (n * 0.53, n * 0.47), max(1.5, n / 6.0), rng.normal(0.10, 0.02))
    return x


def _perturb_alternate_port(bundle: OperatorBundle, base: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Alternative port/load pattern: shift current injection region."""
    n = int(bundle.index["n"]); layers = int(bundle.index["layers"])
    x = base.copy()
    for layer in range(layers):
        add_gaussian_sheet_mode(x, bundle, layer, "x", (n * 0.30, n * 0.70), max(2.5, n / 3.5), rng.normal(0.25, 0.05))
        add_gaussian_sheet_mode(x, bundle, layer, "y", (n * 0.70, n * 0.30), max(2.5, n / 3.5), rng.normal(0.20, 0.04))
    return x


_PERTURB_MAP = [
    ("state0_baseline", lambda b, base, rng: base.copy()),
    ("state1_via_sensitive", _perturb_via_sensitive),
    ("state2_return_sensitive", _perturb_return_sensitive),
    ("state3_gap_sensitive", _perturb_gap_sensitive),
]


def generate_multi_state_case(
    bundle: OperatorBundle, cfg: dict, family: str, index: int,
    rng: np.random.Generator, n_states: int,
) -> GeneratedCase:
    """Generate a multi-state case with N different current excitation patterns.

    Returns a GeneratedCase where current/field vectors are stacked:
      current = [J_0; J_1; ...; J_{N-1}]
      field = [y_0; y_1; ...; y_{N-1}]  where y_i = A_base @ J_i
    """
    n = int(bundle.index["n"])
    truth = FAMILY_TO_TRUTH[family]
    curr_dim_per_state = bundle.A.shape[1] // n_states
    obs_dim_per_state = bundle.A.shape[0] // n_states

    # Generate base current for state 0
    base_single = _smooth_background_current(
        OperatorBundle(
            A=bundle.A[:obs_dim_per_state, :curr_dim_per_state],
            positions=bundle.positions[:n * n] if n_states == 1 else bundle.positions[:n * n],
            obs_positions=bundle.obs_positions[:obs_dim_per_state],
            index=bundle.index, column_norms=bundle.column_norms[:curr_dim_per_state],
        ), rng,
    )

    # Apply family-specific modifications to state 0
    family_current = base_single.copy()
    md: dict = {"generator": "E20_OQCI_v2_multi_state", "n_states": n_states}
    if family == "single_via_observable":
        center = (int(rng.integers(n // 3, 2 * n // 3)), int(rng.integers(n // 3, 2 * n // 3)))
        layer0 = int(rng.integers(0, int(bundle.index["layers"]) - 1))
        single_bundle = OperatorBundle(
            A=bundle.A[:obs_dim_per_state, :curr_dim_per_state],
            positions=bundle.positions[:n * n], obs_positions=bundle.obs_positions[:obs_dim_per_state],
            index=bundle.index, column_norms=bundle.column_norms[:curr_dim_per_state],
        )
        add_via_spot(family_current, single_bundle, layer0, layer0 + 1, center, amplitude=rng.normal(1.3, 0.12), radius=0)
        md.update({"via_center": center, "via_layer_pair": [layer0, layer0 + 1]})
    elif family == "dense_via_cluster":
        center = (int(rng.integers(n // 3, 2 * n // 3)), int(rng.integers(n // 3, 2 * n // 3)))
        layer0 = int(rng.integers(0, int(bundle.index["layers"]) - 1))
        single_bundle = OperatorBundle(
            A=bundle.A[:obs_dim_per_state, :curr_dim_per_state],
            positions=bundle.positions[:n * n], obs_positions=bundle.obs_positions[:obs_dim_per_state],
            index=bundle.index, column_norms=bundle.column_norms[:curr_dim_per_state],
        )
        add_via_spot(family_current, single_bundle, layer0, layer0 + 1, center, amplitude=rng.normal(0.95, 0.08), radius=1)
        md.update({"via_center": center, "via_layer_pair": [layer0, layer0 + 1], "dense_radius": 1})
    elif family == "model_gap_registration":
        md["gap_type"] = "registration_gradient"
    elif family == "model_gap_standoff":
        md["gap_type"] = "standoff_laplacian"
    elif family == "return_path_deep_loop":
        single_bundle = OperatorBundle(
            A=bundle.A[:obs_dim_per_state, :curr_dim_per_state],
            positions=bundle.positions[:n * n], obs_positions=bundle.obs_positions[:obs_dim_per_state],
            index=bundle.index, column_norms=bundle.column_norms[:curr_dim_per_state],
        )
        add_return_loop(family_current, single_bundle, layer=int(bundle.index["layers"]) - 1, amplitude=rng.normal(0.9, 0.1))
        md["return_path"] = "deep_layer_loop"

    # Generate N state currents
    current_parts = []
    for s in range(min(n_states, len(_PERTURB_MAP))):
        state_name, perturb_fn = _PERTURB_MAP[s]
        single_bundle = OperatorBundle(
            A=bundle.A[:obs_dim_per_state, :curr_dim_per_state],
            positions=bundle.positions[:n * n], obs_positions=bundle.obs_positions[:obs_dim_per_state],
            index=bundle.index, column_norms=bundle.column_norms[:curr_dim_per_state],
        )
        perturbed = perturb_fn(single_bundle, family_current, rng)
        current_parts.append(perturbed)
        md[f"state_{s}"] = state_name
    # Pad with baseline copies if n_states > len(_PERTURB_MAP)
    while len(current_parts) < n_states:
        current_parts.append(family_current.copy())
    current_stacked = np.concatenate(current_parts)

    # Forward through block-diagonal A
    A_base = bundle.A[:obs_dim_per_state, :curr_dim_per_state]
    field_parts = []
    for s in range(n_states):
        field_parts.append(A_base @ current_parts[s])
    clean_stacked = np.concatenate(field_parts)

    # Model gap (applied to state 0 only, repeated for all states)
    # Build single-state model gap, then tile for multi-height and multi-state
    base_pattern = np.zeros(3 * n * n, dtype=float)  # default Bxyz size
    if family == "model_gap_registration":
        ref_field = field_parts[0][:3 * n * n] if len(field_parts[0]) >= 3 * n * n else field_parts[0]
        base_pattern = registration_pattern(n, (n / 2, n / 2), max(1.5, n / 6.0),
            0.12 * max(np.linalg.norm(ref_field), 1e-12))
    elif family == "model_gap_standoff":
        ref_field = field_parts[0][:3 * n * n] if len(field_parts[0]) >= 3 * n * n else field_parts[0]
        base_pattern = standoff_laplacian_pattern(ref_field,
            0.20 * max(np.linalg.norm(ref_field), 1e-12))
    # Tile single-state pattern across heights+components using per_height
    bundle_single_state = OperatorBundle(
        A=bundle.A[:obs_dim_per_state, :curr_dim_per_state],
        positions=bundle.positions[:n * n],
        obs_positions=bundle.obs_positions[:obs_dim_per_state],
        index=bundle.index, column_norms=bundle.column_norms[:curr_dim_per_state],
        heights=bundle.heights, A_per_height=bundle.A_per_height,
        per_height_components=bundle.per_height_components,
    )
    model_gap_single = _tile_for_multi_height(base_pattern, bundle_single_state)
    model_gap_stacked = np.tile(model_gap_single, n_states)

    noise_stacked = _noise(bundle, cfg, rng)
    observed = clean_stacked + model_gap_stacked + noise_stacked

    return GeneratedCase(
        case_id=f"E20_ms_{family}_{index:03d}", family=family,
        truth_hypothesis=truth, current=current_stacked,
        field_clean=clean_stacked, field_observed=observed,
        model_gap_field=model_gap_stacked, metadata=md,
    )


def generate_multi_state_cases(bundle: OperatorBundle, cfg: dict, n_states: int) -> list[GeneratedCase]:
    """Generate cases with multi-state excitation patterns."""
    rng = _rng_for(cfg)
    cases: list[GeneratedCase] = []
    count = int(cfg["case_count_per_family"])
    for family in cfg["families"]:
        if family not in FAMILY_TO_TRUTH:
            raise ValueError(f"Unknown generated family: {family}")
        for i in range(count):
            cases.append(generate_multi_state_case(bundle, cfg, family, i, rng, n_states))
    return cases
