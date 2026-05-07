# Metrics Schema

`outputs/metrics.json` includes acceptance gates per the evidence package contract.

## Required fields

- `evidence_id`: "E29_rho_integrated_schur_gamma_certificate"
- `claim_ids`: [C04, C06, C10, C13]
- `status`: "partial"
- `acceptance_gates`: dict of engineering and scientific gates
- `aggregate_rates`: per-ablation pass rates
- `calibration_evaluation_split`: split audit results
- `pairwise_rates`: pairwise certificate rates
- `cannot_claim`: list of explicit boundary statements
- `generated_at`: ISO 8601 UTC timestamp

## Acceptance Gates

### Engineering

- `package_runs_to_completion`
- `rho_artifacts_loaded_or_recomputed`
- `calibration_evaluation_split_enforced`
- `conservative_and_rss_gamma_reported`
- `pairwise_gamma_reported`
- `ablation_table_reported`
- `reports_written`
- `generated_domain_boundary_explicit`

### Scientific

- `E25_rho_improves_gamma_over_E23_old_rho`
- `positive_conservative_gamma_rate_ge_0_30`
- `positive_rss_gamma_rate_ge_0_50`
- `pairwise_conservative_gamma_rate_ge_0_20`
- `truth_in_consistent_set_rate_ge_0_90`
- `wrong_accept_rate_le_0_10`
- `empty_rate_le_0_10`
