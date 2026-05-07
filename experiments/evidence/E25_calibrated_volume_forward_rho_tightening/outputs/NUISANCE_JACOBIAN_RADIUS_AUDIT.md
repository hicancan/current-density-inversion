# Nuisance Jacobian Radius Audit

| Parameter | Abs Radius | Rel Radius | Bound | FD Step |
|---|---|---|---|---|
| rho_sensor_z | 1.8574e-03 | 1.0453e-01 | 1e-05 | 1e-07 |
| rho_sensor_dx | 8.5859e-04 | 4.8322e-02 | 1e-05 | 1e-07 |
| rho_sensor_dy | 1.7220e-03 | 9.6916e-02 | 1e-05 | 1e-07 |
| rho_layer_z | 9.2868e-04 | 5.2267e-02 | 5e-06 | 1e-07 |
| rho_width | 2.5595e-05 | 1.4405e-03 | 2e-06 | 1e-07 |
| rho_thickness | 3.5952e-06 | 2.0234e-04 | 1e-06 | 1e-07 |
| rho_nuisance_combined_box | 5.3958e-03 | 3.0368e-01 | None | None |
| rho_nuisance_combined_rss | 2.8311e-03 | 1.5934e-01 | None | None |

## Interpretation

Parameters with relative radius > 0.1 dominate the calibration budget.
These must be bounded through external measurement or included in Gamma.
