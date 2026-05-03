# exp05 Failure Modes

Passing exp05 does not mean the QDM/NV sensor model is complete.

Known limitations:

- The model is still a Cartesian vector-field proxy plus idealized four-axis NV
  projection; it is not an ODMR Hamiltonian or fitting pipeline.
- The residual detector uses oracle sheet-background subtraction.
- PSF, correlated noise, standoff tilt, confidence, and axis gain mismatch are
  hand-controlled perturbations rather than measured calibration artifacts.
- Four-axis reconstruction assumes known axes and calibrated gains; real
  experiments may have strain, temperature, microwave, optical, and fitting
  biases.
- The via template is generated from the same simplified circuit geometry.

Most sensitive parameters:

- `psf_sigma_px`;
- `tilt_alpha` / `tilt_beta`;
- channel covariance in `noise_corr`;
- `nv_axis_gain_mismatch`;
- via patch radius and DoG scales.
