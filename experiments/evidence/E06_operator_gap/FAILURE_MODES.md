# exp06 Failure Modes

Passing exp06 does not prove real multi-fidelity validation.

Known limitations:

- Medium and high operators are synthetic surrogates, not COMSOL, FastHenry,
  Ansys, QDM, or measured data.
- Calibration is intentionally low-dimensional and may be much easier than real
  device calibration.
- The basis has only three current degrees of freedom, so it is a concept gate,
  not a full layout-scale inverse benchmark.
- The high surrogate includes simplified return currents and PSF, not full
  conductor thickness, dielectric stack, package, or boundary conditions.
- A low calibrated error here only proves that this surrogate gap is learnable.

Most sensitive parameters:

- `return_current_scale`;
- finite-width filament count;
- depth shifts;
- PSF sigma;
- calibration-set size and ridge strength.
