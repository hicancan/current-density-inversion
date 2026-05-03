from __future__ import annotations

import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from observability.grid import Grid2D
from observability.spectral import (
    streamfunction_current,
    forward_sheet_fft,
    inverse_bxy_fft,
    inverse_bz_fft,
    attenuation_for_feature,
    recoverable_feature_size,
    relative_l2,
)


def test_bxy_inverse_recovers_divergence_free_current_clean():
    grid = Grid2D(n=64, fov_m=1e-3)
    jx, jy, _ = streamfunction_current(grid, seed=5)
    bx, by, bz = forward_sheet_fft(jx, jy, grid, standoff_m=25e-6)
    rec = inverse_bxy_fft(bx, by, grid, standoff_m=25e-6)
    assert relative_l2(rec, (jx, jy)) < 1e-4


def test_bz_inverse_recovers_divergence_free_current_clean_except_dc():
    grid = Grid2D(n=64, fov_m=1e-3)
    jx, jy, _ = streamfunction_current(grid, seed=6)
    # Remove any tiny numerical DC current component because Bz cannot observe it.
    jx = jx - np.mean(jx)
    jy = jy - np.mean(jy)
    bx, by, bz = forward_sheet_fft(jx, jy, grid, standoff_m=25e-6)
    rec = inverse_bz_fft(bz, grid, standoff_m=25e-6)
    assert relative_l2(rec, (jx, jy)) < 5e-3


def test_attenuation_threshold_formula_is_self_consistent():
    z = 50e-6
    threshold = 1e-2
    lam = recoverable_feature_size(z, threshold)
    att = attenuation_for_feature_size = attenuation_for_feature(np.array([lam]), z)[0]
    assert abs(att - threshold) / threshold < 1e-12


def test_reference_outputs_pass_acceptance_gates():
    metrics_path = ROOT / "outputs" / "metrics.json"
    assert metrics_path.exists()
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert metrics["all_acceptance_gates_passed"] is True
    assert metrics["two_layer_single_plane_rank_gate"]["single_plane_two_layer_rank_deficient"] is True
    assert (ROOT / "outputs" / "RUN_REPORT.md").exists()
