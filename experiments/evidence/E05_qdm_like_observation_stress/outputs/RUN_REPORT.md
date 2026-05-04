# exp05 Run Report

## Role

MVP-4 QDM-like sensor nonidealities. This experiment stress-tests standoff tilt,
PSF blur, correlated channel noise, spatial confidence, and via-scale band-pass
detection before these effects are mixed into learned inversion.

## Gate Summary

Overall: PASS

- correlated_noise_matches_target_covariance: PASS; value=0.017124789480940206; threshold=mean absolute correlation error < 0.05
- psf_removes_high_frequency_energy: PASS; value=0.13518745971250534; threshold=full-case Bz high-frequency ratio < 0.25
- tilt_creates_measurable_forward_mismatch: PASS; value=[20.00000000000001, 0.025910848788833846]; threshold=tilt range > 10 um and field mismatch > 1%
- residual_detection_beats_raw_total_field: PASS; value=[2.6062046057082138, 692.7823633900667, 36.26188621469471]; threshold=full residual/raw peak ratio > 2 and residual loc error < raw loc error
- hard_case_residual_still_localizes_reasonably: PASS; value=81.08404256841936; threshold=hard-full residual loc error < 100 um
- nv_four_axis_projection_is_well_conditioned: PASS; value=[3, 1.0, 2.0962044950314923e-16]; threshold=four-axis rank is 3, condition number < 2, reconstruction error < 1e-10
- single_nv_axis_is_rank_deficient: PASS; value=1; threshold=single-axis rank < 3
- nv_axis_gain_mismatch_is_measurable: PASS; value=0.018257854857061807; threshold=gain-mismatch reconstruction relative L2 > 1%

## Key Results

- full-case tilt range: `20.00 um`
- full-case constant-vs-tilted field relative L2: `2.591e-02`
- full-case Bz high-frequency energy ratio after PSF: `0.135`
- full-case raw via localization error: `692.78 um`
- full-case residual via localization error: `36.26 um`
- NV four-axis reconstruction relative L2: `2.096e-16`
- NV axis-gain mismatch reconstruction relative L2: `1.826e-02`

## Boundary

This is still a proxy, not an ODMR or NV-Hamiltonian simulator. The four-axis
NV projection check verifies vector-field observability under ideal calibrated
axes, and the axis-gain mismatch check quantifies one calibration risk. The
residual detector still uses oracle sheet-background subtraction.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
