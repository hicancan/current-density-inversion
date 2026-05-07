# Metrics Schema

`outputs/metrics.json` includes acceptance gates per the evidence package contract.

## Required fields

- `evidence_id`: "E25_calibrated_volume_forward_rho_tightening"
- `claim_id`: "C04_inverse_crime_and_operator_gap"
- `status`: "partial"
- `acceptance_gates`: dict of engineering and scientific gates
- `cannot_claim`: list of explicit boundary statements
- `generated_at`: ISO 8601 UTC timestamp

## Acceptance Gates

### Engineering
- `package_runs_to_completion`
- `canonical_geometries_generated`
- `volume_quadrature_runs`
- `quadrature_convergence_reported`
- `rho_decomposition_reported`
- `no_fake_external_solver_claim`
- `reports_written`
- `generated_domain_boundary_explicit`

### Scientific
- `volume_quadrature_relative_change_le_0_05`
- `multifilament_beats_centerline_error`
- `rho_finite_width_relative_below_centerline_surrogate`
- `rho_combined_budget_finite`
- `dominant_rho_source_identified`
- `recommended_gamma_rho_available`
