# E17 Run Report

Overall: PASS

- fourier_baseline_runs: PASS; value=48; threshold=>=1 Fourier run
- tikhonov_baseline_runs: PASS; value=24; threshold=>=1 Tikhonov run
- l1_curl_like_baseline_runs: PASS; value=48; threshold=>=1 L1-sparse run
- div_free_baseline_runs: PASS; value=24; threshold=>=1 div-free run
- metrics_reported_across_noise_and_standoff: PASS; value={'n_noise': 3, 'n_standoff': 2, 'n_conditions': 24}; threshold=multiple noise+standoff
- no_unverified_literature_claim: PASS; value=verified; threshold=no unverified claims
- fair_same_split_comparison: PASS; value=24; threshold=same splits for all

Dataset: D:\code\github\hicancan\current-density-inversion\experiments\evidence\E03_two_layer_via_topology\data\two_layer_via_benchmark.npz
Grid: 49

Boundary: synthetic centerline Biot-Savart only. Not real QDM/NV/CAD.

Metrics: `outputs/metrics.json`

Calibration: No calibration used; evaluation-only on E03 benchmark splits (train/val/test/ood).