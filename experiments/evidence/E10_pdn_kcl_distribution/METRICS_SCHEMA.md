# Metrics Schema

`outputs/metrics.json` contains the common agent-facing contract:

- `evidence_id`: `E10_pdn_kcl_distribution`.
- `claim_id`: `C10_pdn_kcl_distribution_need`.
- `status`: evidence run status.
- `dataset`: case counts by hypothesis and split role.
- `split_roles`: row counts for train, calibration, and heldout.
- `pdn_kcl`: KCL residual, current closure error, and thresholds.
- `divB`: full finite-difference magnetic divergence proxy at the sensor plane.
- `hypothesis_scoring`: H0/H1/H2/H3 residual-scoring accuracy and H0/H1 endpoints.
- `acceptance_gates`: gate booleans and `all_acceptance_gates_passed`.
- `cannot_claim`: generated-domain boundaries.
- `generated_at`: deterministic run metadata timestamp.

Primary human-readable artifacts:

- `RUN_REPORT.md`
- `PDN_KCL_METRICS_TABLE.md`
- `HYPOTHESIS_SCORE_TABLE.md`
- `CASE_COUNTS_TABLE.md`

