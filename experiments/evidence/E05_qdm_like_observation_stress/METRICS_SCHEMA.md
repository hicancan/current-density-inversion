# exp05 Metrics Schema

## Sensor Proxy

- `case_metrics`: per-stress-case QDM-like metrics for tilt, PSF blur,
  correlated noise, confidence, and raw/residual/DoG via detection.
- `summary.full_case_*`: canonical full-case values used by acceptance gates.
- `nv_projection`: ideal four-axis NV projection diagnostics plus axis-gain
  mismatch sensitivity.

## Detection Metrics

- `raw_loc_error_um`: via localization error from the raw observed field.
- `residual_loc_error_um`: localization error after oracle sheet-background
  subtraction.
- `dog_loc_error_um`: localization error after DoG band-pass residual filtering.
- `*_peak`: matched-filter peak score for raw, residual, or band-pass residual.

## NV Projection Metrics

- `four_axis_rank`: rank of the four-axis NV projection matrix; should be 3.
- `single_axis_rank`: rank of one NV axis; should be rank-deficient for full
  vector recovery.
- `four_axis_reconstruction_rel_l2`: ideal calibrated four-axis vector-field
  reconstruction error.
- `axis_gain_mismatch_reconstruction_rel_l2`: vector-field error when per-axis
  gains are slightly wrong.

## Gates

- Correlated noise must match the target covariance.
- PSF must remove high-frequency energy.
- Standoff tilt must create measurable forward mismatch.
- Residual via detection must beat raw total-field detection.
- Hard-case residual detection must localize reasonably.
- Four calibrated NV axes must be well-conditioned, one axis must be
  rank-deficient, and gain mismatch must be measurable.
