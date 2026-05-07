"""Schur signal computation for candidate edge defects.

For each candidate edge defect q, the Schur signal is:

    S_q(U) = ||W * Delta Y_q(U)||_2

where Delta Y_q is the magnetic field perturbation signature of defect q
relative to the nominal topology.

Because E27 Schur signatures are not yet available, this module generates
synthetic but physically motivated defect signatures based on:
- Edge removal (via absence)
- Edge displacement (misregistration)
- Edge width error
- Return path gap
"""
from __future__ import annotations

import numpy as np


def generate_candidate_defects(
    n_edges: int, seed: int = 42,
) -> list[dict]:
    """Generate a set of candidate edge defects for hypothetical topology.

    Each defect is a perturbation on one or more edges of the nominal graph.

    Returns list of defect dicts with:
      - defect_id: unique string identifier
      - defect_type: type of defect
      - affected_edges: list of edge indices
      - perturbation_magnitude: relative perturbation magnitude
    """
    rng = np.random.default_rng(seed)
    defect_types = [
        "via_absence",
        "via_misplacement",
        "trace_width_error",
        "return_path_gap",
        "layer_misassignment",
        "edge_break",
        "parallel_coupling",
    ]
    n_defects = min(n_edges * 3, 20)

    defects = []
    for i in range(n_defects):
        dtype = defect_types[i % len(defect_types)]
        n_affected = rng.integers(1, min(3, n_edges) + 1)
        affected = sorted(
            rng.choice(n_edges, size=n_affected, replace=False).tolist()
        )
        mag = 10.0 ** rng.uniform(-3, 0)  # 0.001 to 1.0

        defects.append({
            "defect_id": f"defect_{i:03d}",
            "defect_type": dtype,
            "affected_edges": affected,
            "perturbation_magnitude": float(mag),
        })

    return defects


def compute_schur_signal(
    A_nominal: np.ndarray,
    A_defect: np.ndarray,
    current_samples: np.ndarray,
    noise_sigma: float = 0.0,
) -> dict:
    """Compute Schur signal S_q = ||W * (A_defect - A_nominal) * i||_2.

    Args:
        A_nominal: (M, E) nominal forward operator.
        A_defect: (M, E) perturbed forward operator for this defect.
        current_samples: (E, K) sample current vectors.
        noise_sigma: measurement noise standard deviation.

    Returns dict with signal, noise_floor, and snr.
    """
    if current_samples.ndim == 1:
        current_samples = current_samples[:, None]

    K = current_samples.shape[1]
    M = A_nominal.shape[0]

    signals = []
    for k in range(K):
        i_k = current_samples[:, k]
        delta_y = (A_defect - A_nominal) @ i_k
        signals.append(float(np.linalg.norm(delta_y)))

    s_max = max(signals)
    s_mean = float(np.mean(signals))
    s_median = float(np.median(signals))

    noise_floor = noise_sigma * np.sqrt(M) if noise_sigma > 0 else s_max * 1e-6
    snr = s_max / max(noise_floor, 1e-30)

    return {
        "signal_max": s_max,
        "signal_mean": s_mean,
        "signal_median": s_median,
        "noise_floor": noise_floor,
        "snr": snr,
        "num_samples": K,
    }


def generate_defect_operator(
    A_nominal: np.ndarray,
    edges: np.ndarray,
    widths: np.ndarray,
    thicknesses: np.ndarray,
    defect: dict,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Generate a perturbed forward operator for a given edge defect.

    Perturbations simulate:
    - via_absence: zero out affected edge columns (open circuit)
    - via_misplacement: shift edge endpoints
    - trace_width_error: scale column norms
    - return_path_gap: attenuate affected columns
    - layer_misassignment: shift z-coordinates
    - edge_break: zero out column with additive noise
    - parallel_coupling: add cross-talk between affected edges
    """
    if rng is None:
        rng = np.random.default_rng(42)

    A_defect = A_nominal.copy()
    M, E = A_defect.shape
    affected = defect["affected_edges"]
    mag = defect["perturbation_magnitude"]

    dtype = defect["defect_type"]
    for e in affected:
        if e >= E:
            continue

        if dtype == "via_absence":
            # Zero out the column (open circuit at via)
            A_defect[:, e] *= (1.0 - mag)

        elif dtype == "via_misplacement":
            # Shift column by a fraction proportional to magnitude
            shift = mag * rng.standard_normal(M)
            A_defect[:, e] += shift * np.linalg.norm(A_defect[:, e]) / M

        elif dtype == "trace_width_error":
            # Scale column norm by (1 + perturbation)
            A_defect[:, e] *= (1.0 + rng.uniform(-mag, mag))

        elif dtype == "return_path_gap":
            # Attenuate return-path columns
            A_defect[:, e] *= (1.0 - mag)

        elif dtype == "layer_misassignment":
            # Mix with noise to simulate wrong layer assignment
            noise_scale = mag * np.linalg.norm(A_defect[:, e])
            A_defect[:, e] += rng.standard_normal(M) * noise_scale / np.sqrt(M)

        elif dtype == "edge_break":
            # Near-complete column zeroing
            A_defect[:, e] *= (1.0 - mag)

        elif dtype == "parallel_coupling":
            # Add cross-talk between affected edges
            for e2 in affected:
                if e2 != e and e2 < E:
                    coupling = mag * 0.1
                    A_defect[:, e] += coupling * A_nominal[:, e2]

    return A_defect


def compute_all_schur_signals(
    A_nominal: np.ndarray,
    edges: np.ndarray,
    widths: np.ndarray,
    thicknesses: np.ndarray,
    defects: list[dict],
    current_samples: np.ndarray,
    noise_sigma: float = 0.0,
    seed: int = 42,
) -> list[dict]:
    """Compute Schur signals for all candidate defects."""
    rng = np.random.default_rng(seed)
    results = []

    for defect in defects:
        A_defect = generate_defect_operator(
            A_nominal, edges, widths, thicknesses, defect, rng,
        )
        signal = compute_schur_signal(
            A_nominal, A_defect, current_samples, noise_sigma,
        )
        results.append({
            **defect,
            **signal,
        })

    return results
