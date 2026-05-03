# exp06 Metrics Schema

## Operators

- `low_test_rel_l2_physics_decoder`: same-operator low-fidelity test error.
- `medium_test_rel_l2_physics_decoder`: low-operator decoder tested on an
  intermediate finite-width/depth-shift surrogate.
- `high_test_rel_l2_physics_decoder`: low-operator decoder tested on the high
  surrogate with finite width, return currents, PSF, depth offsets, and noise.
- `medium_basis_rel_difference_from_low`: medium operator basis gap.
- `operator_basis_rel_difference`: high operator basis gap.
- `fidelity_ladder`: ordered low/medium/high operator gap and decoder error.
- `real_pypeec_bridge`: read-only exp07 real PyPEEC fidelity bridge. It records
  exp07 backend status, case count, exp03-like shape gap, convergence delta, and
  per-case raw/shape gaps. It is not a PyPEEC-calibrated decoder.

## Calibration

- `calibration_sizes`: high-fidelity calibration-set sizes.
- `calibration_curve_rel_l2`: high-test error after each calibration size.
- `high_test_rel_l2_calibrated_400`: calibrated high-test error at the largest
  configured calibration size.
- `calibration_improvement_ratio`: calibrated error divided by uncalibrated
  high-fidelity error.

## Gates

- Same-operator low test must be nearly exact.
- High surrogate must create a visible inverse-crime gap.
- Calibration must reduce the high-fidelity gap.
- High operator basis must materially differ from low.
- Fidelity ladder must be monotone: low error < medium error < high error.
- Medium operator gap must lie between low and high.
- Calibrated high-fidelity error must be small enough for the MVP gate.
- Real PyPEEC bridge artifact must exist, have exp07 gates passed, complete the
  required 40+ cases, and show a material but bounded exp03-like shape gap.
