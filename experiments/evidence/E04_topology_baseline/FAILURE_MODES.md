# exp04 Failure Modes

Passing exp04 does not prove real-world current inversion.

Known limitations:

- The dataset is synthetic and line-current based.
- Truth maps are raster labels, while magnetic fields are generated from segment geometry.
- The forward residual is a linear proxy fitted from the benchmark dataset, not a physical Biot-Savart re-forward of predicted maps.
- The U-Net-lite architecture is intentionally small and not a final model.
- There is no real QDM, COMSOL, FastHenry, CAD, or measured sample data.
- The lambda sweep uses shortened training runs, so it demonstrates the shape of
  the trade-off and not the globally optimal hyperparameter.
- The multi-seed check is a stability gate, not a full statistical study.
- Per-channel relative L2 is undefined for inactive truth channels; those entries
  are now reported as `null`, and current-scale RMSE is the stable comparison.
- Stress perturbations are still proxy perturbations applied to `B_obs`; they do
  not replace full NV/ODMR, FEM, FastHenry, or measured-data validation.
- The finite-width/return stress row is a stronger operator-mismatch proxy, but
  it is still generated from simple raster kernels and not from a field solver.
- The physical re-forward operator is a rasterized short-segment Biot-Savart
  model. It is independent of the fitted proxy, but it is still not a
  finite-width conductor, return-current, FEM, or QDM sensor model.
- The physics Tikhonov baseline is intentionally generic; poor performance can
  reflect ill-conditioning or raster/segment mismatch rather than a failed
  learned model.
- Detector thresholds and the two-stage refined baseline are calibrated on the
  validation split and frozen for test/OOD reporting. They still remain
  synthetic calibration procedures; changing them after looking at test/OOD
  would invalidate the detector claims.
- The two-stage refined baseline currently updates only the `s1` channel from
  validation-calibrated residual-adjoint scores. It can improve peak
  localization while worsening dense `s1` L2 or presence F1, so it is a
  diagnostic route, not a final model.

Likely failure causes:

- topology loss too high: lower L2 quality or via amplitude;
- topology loss too low: no physical consistency gain;
- dataset too small: high seed variance;
- OOD shift too strong: both models fail, topology only reduces residual;
- raster truth and segment-field mismatch: topology residual and supervised labels may pull in different directions.
- posthoc projection may reduce topology residual more aggressively than
  training-time topology loss while hurting the via/source channel.
- residual via detection can localize via candidates while still producing a
  poor dense `s1` amplitude map; detector hit rate is therefore reported
  separately from `s1_rel_l2`.
- raw adjoint via scores can be dominated by sheet-current background, so a good
  residual detector still requires a credible sheet-current estimate.
- unfiltered residual detectors can over-trigger on OOD no-via/background cases;
  the DoG/strict variant tests false-positive control but trades precision
  against recall.
- finite-width/return operator stress can change the ranking of L2 and physical
  residuals, which is exactly why same-family centerline performance must stay
  separated from real-hardware claims.
