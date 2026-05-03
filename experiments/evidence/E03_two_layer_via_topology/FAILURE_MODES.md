# exp03 Failure Modes

Passing exp03 does not mean the final inverse method is solved.

Known failure modes:

- The residual detector uses oracle sheet-background subtraction; real models must estimate that background.
- Raster truth maps are benchmark labels, not a replacement for the finite-volume topology gate.
- The benchmark still uses ideal free-space line-current Biot-Savart. The
  finite-width/return-current probe quantifies a same-family forward gap, but it
  is not a finite-element, FastHenry, CAD, or measured-device validation.
- OOD samples are synthetic route/noise perturbations, not real layout or real sensor OOD.
- Multiple dense via arrays and PDN-style group priors are not yet represented.
- Route diversity now includes simple no-via, multi-via, and dense-via cases, but
  routes are still synthetic Manhattan paths rather than full CAD-style networks.
- Recoverability labels are proxy dataset metadata, not a mathematical
  identifiability theorem.

Most sensitive parameters:

- via/sheet Bxy energy ratio;
- standoff and layer depth separation;
- sheet-background strength;
- noise level in `benchmark_dataset.noise_relative_to_max_abs_B`;
- grid resolution and via location relative to pixel centers.
