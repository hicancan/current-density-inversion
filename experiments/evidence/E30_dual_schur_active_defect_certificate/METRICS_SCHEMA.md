# Metrics Schema

`outputs/metrics.json` uses `research-ssot-metrics-v1`.

Top-level fields:

- `evidence_id`: `E30_dual_schur_active_defect_certificate`
- `claim`: primary affected claim.
- `status`: `passed`, `passed_with_limitations`, or `failed_sanity`.
- `engineering_gates`, `scientific_gates`, `acceptance_gates`.
- `operator_diagnostics`: E28 generated graph/forward dimensions.
- `candidate_defects`: deterministic via-open candidates.
- `boundary_control`: ordinary boundary-port control certificate.
- `perimeter_boundary_upper_bound`: top/bottom perimeter-node boundary basis
  evaluated optimistically without nuisance subtraction.
- `dual_schur_certificate`: Schur-aligned local excitation certificate.
- `nuisance_audit`: directional nuisance subtraction settings and maxima.
- `current_budget_law`: critical-current calculation from the linear signature
  law.
- `leakage_audit`: generated-domain/no-real-data discipline.
- `cannot_claim`: explicit overclaim boundaries.

Core metric:

`M21_dual_schur_defect_gamma = delta_directional - z*sigma - rho_i - rho_j - tau`

where `delta_directional` is the pairwise local-defect signature distance under
active dual excitation, `z*sigma` is the directional Gaussian noise radius,
`rho_i` and `rho_j` are nuisance projections along the pair separation
direction, and `tau` is the decision threshold.
