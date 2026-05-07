# Nuisance Jacobian Radius Audit

| Parameter | Abs Radius | Rel Radius | Bound | FD Step |
|---|---|---|---|---|
| rho_sensor_z | 8.1562e-04 | 9.1413e-02 | 1e-05 | 1e-07 |
| rho_sensor_dx | 1.0340e-03 | 1.1588e-01 | 1e-05 | 1e-07 |
| rho_sensor_dy | 8.9126e-04 | 9.9890e-02 | 1e-05 | 1e-07 |
| rho_layer_z | 4.0781e-04 | 4.5706e-02 | 5e-06 | 1e-07 |
| rho_width | 1.2788e-05 | 1.4332e-03 | 2e-06 | 1e-07 |
| rho_thickness | 8.9182e-07 | 9.9953e-05 | 1e-06 | 1e-07 |
| rho_nuisance_combined_box | 3.1623e-03 | 3.5443e-01 | None | None |
| rho_nuisance_combined_rss | 1.6417e-03 | 1.8400e-01 | None | None |

## Interpretation

Parameters with relative radius > 0.1 dominate the calibration budget.
These must be bounded through external measurement or included in Gamma.
