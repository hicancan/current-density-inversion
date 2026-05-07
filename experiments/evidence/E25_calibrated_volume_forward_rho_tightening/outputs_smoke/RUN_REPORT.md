# E25 RUN REPORT

Generated: 2026-05-06T10:25:30.868172+00:00

## Execution Summary

- Config: smoke
- Smoke mode: True
- Families tested: 2
- Quadrature levels tested: 16

## Acceptance Gates

- **package_runs_to_completion**: PASS
- **canonical_geometries_generated**: PASS
- **volume_quadrature_runs**: PASS
- **quadrature_convergence_reported**: PASS
- **rho_decomposition_reported**: PASS
- **no_fake_external_solver_claim**: PASS
- **reports_written**: PASS
- **generated_domain_boundary_explicit**: PASS
- **volume_quadrature_relative_change_le_0_05**: FAIL
- **multifilament_beats_centerline_error**: PASS
- **rho_finite_width_relative_below_centerline_surrogate**: PASS
- **rho_combined_budget_finite**: PASS
- **dominant_rho_source_identified**: PASS
- **recommended_gamma_rho_available**: PASS
- **all_engineering_gates_passed**: PASS
- **all_scientific_gates_passed**: FAIL
- **all_acceptance_gates_passed**: FAIL

## Quadrature Convergence
- Best relative change: 0.18471021375728644
- Median relative change: 0.4550593958587934
- Gate (<=0.05): FAIL

## Dominant Rho Source
- straight_strip/rho_combined_conservative

## Cannot Claim
- All results are generated-domain only; no real QDM/NV sensor data is used.
- No external solver (PyPEEC, FastHenry, COMSOL) is used for cross-validation.
- Volume quadrature is numerical; no analytic volume integral for rectangular prisms is implemented.
- Multifilament approximation uses uniform filament spacing; no adaptive refinement.
- Nuisance Jacobian uses first-order finite differences; higher-order effects are not quantified.
- No real CAD/GDS layouts are used; all geometries are canonical generated families.

## Next Required Evidence
- E24/E26: integrate calibrated rho into robust Gamma certificates
- External solver cross-validation (PyPEEC, FastHenry)
- Real CAD/GDS layout import
