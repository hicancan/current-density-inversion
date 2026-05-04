# E17 L1-Curl and Divergence-Free Regularization Baseline Evidence

## Summary

Fourier Wiener, Tikhonov, L1-sparse curl, and divergence-free regularized baselines
compared across noise levels (0.0, 0.01, 0.05) and standoffs (0um, 50um) on the
E03 two-layer via benchmark train/val/test/ood splits.

## Key Findings

- Fourier Wiener: zero divergence residual (3e-12), fast (0.19s), but no edge
  preservation.
- Tikhonov: lower current RMSE (1.45 vs 1.55), but high divergence residual
  (0.256) and curl sparsity (0.31).
- L1-curl-like: balances edge preservation with moderate divergence.
- Div-free: lowest divergence residual (< 1e-10), moderate current RMSE.

## Boundary

Generated-domain centerline Biot-Savart evaluation only. Not validated against
external solvers, real CAD/GDS, or real QDM/NV measurements. No calibration
used; evaluation-only on E03 dataset splits.

## Metrics

See `experiments/evidence/E17_l1_curl_divergence_free_baseline/outputs/metrics.json`
for full results across 144 runs (4 baselines x 3 noise x 2 standoff x 6 conditions).

## Acceptance Gates

All 7 acceptance gates passed (fourier runs >= 1, tikhonov runs >= 1,
l1-curl runs >= 1, div-free runs >= 1, multiple noise+standoff conditions,
no unverified literature claims, same splits for all baselines).
