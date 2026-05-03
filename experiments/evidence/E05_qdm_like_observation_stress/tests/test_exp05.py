import json
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for prefix in ["forward", "sensor", "detection"]:
    for name in list(sys.modules):
        if name == prefix or name.startswith(prefix + "."):
            del sys.modules[name]
sys.path.insert(0, str(ROOT / "src"))

from forward import make_grid, standoff_plane, high_frequency_energy
from sensor import correlated_noise, empirical_corr, apply_psf
from detection import dog_filter


class Exp05Tests(unittest.TestCase):
    def setUp(self):
        with open(ROOT / "configs" / "default.json", "r", encoding="utf-8") as f:
            self.cfg = json.load(f)

    def test_standoff_plane_has_expected_range(self):
        X, Y, _ = make_grid(self.cfg["fov_m"], self.cfg["grid_n"])
        Z = standoff_plane(X, Y, self.cfg["standoff_m"], self.cfg["tilt_alpha"], self.cfg["tilt_beta"])
        self.assertGreater(float(Z.max() - Z.min()), 1e-6)
        self.assertGreater(float(Z.min()), 0.0)

    def test_correlated_noise_has_reasonable_correlation(self):
        rng = np.random.default_rng(123)
        sigma_T = np.asarray(self.cfg["noise_sigma_uT"]) * 1e-6
        target = np.asarray(self.cfg["noise_corr"])
        noise, base = correlated_noise((160, 160), sigma_T, target, 0.0, rng)
        emp = empirical_corr(base)
        self.assertLess(float(np.mean(np.abs(emp - target))), 0.04)
        self.assertEqual(noise.shape, (160, 160, 3))

    def test_psf_reduces_high_frequency_energy(self):
        rng = np.random.default_rng(0)
        img = rng.normal(size=(96, 96))
        B = np.stack([img, img, img], axis=-1)
        B_blur = apply_psf(B, 1.5)
        self.assertLess(high_frequency_energy(B_blur[..., 0]), high_frequency_energy(B[..., 0]))

    def test_dog_suppresses_constant_background(self):
        arr = np.ones((64, 64)) * 7.0
        out = dog_filter(arr, 1.0, 3.0)
        self.assertLess(float(np.max(np.abs(out))), 1e-10)

    def test_reference_outputs_pass_acceptance_gates(self):
        metrics = json.loads((ROOT / "outputs" / "metrics.json").read_text(encoding="utf-8"))
        self.assertTrue(metrics["all_acceptance_gates_passed"])
        full = next(row for row in metrics["case_metrics"] if row["label"] == "full")
        self.assertLess(full["residual_loc_error_um"], full["raw_loc_error_um"])
        self.assertEqual(metrics["nv_projection"]["four_axis_rank"], 3)
        self.assertLess(metrics["nv_projection"]["four_axis_reconstruction_rel_l2"], 1e-10)
        self.assertGreater(metrics["nv_projection"]["axis_gain_mismatch_reconstruction_rel_l2"], 0.01)
        self.assertTrue((ROOT / "outputs" / "RUN_REPORT.md").exists())


if __name__ == "__main__":
    unittest.main()
