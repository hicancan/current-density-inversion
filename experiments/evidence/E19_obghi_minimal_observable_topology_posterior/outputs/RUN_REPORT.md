# RUN REPORT - E19.1 OBGHI Calibrated Posterior Diagnostics

- Metrics file: `outputs/metrics.json`

E19.1 is generated-domain algorithm evidence. It does not constitute real
QDM/NV, CAD/Gerber/GDS, or external-solver validation.

## Engineering run status

Engineering gates passed: `True`

## Scientific status

Scientific gates passed: `False`

## Claim affected

- Primary: `C10_pdn_kcl_distribution_need`
- Secondary: `C06_graph_hypothesis_system_identification`, `C02_single_plane_identifiability_boundary`, `C04_inverse_crime_and_operator_gap`

## Evidence added

E19.1 calibrated OBGHI posterior evidence with:
- Split engineering/scientific gates
- Block-diagonal group priors
- Per-column observable normalization
- Expanded H2 gap basis (registration derivatives, standoff laplacians, drift)
- Split H1 via basis (vertical modes + sheet compensation)
- Expanded H3 return basis (multi-position loops, edge modes, distributed)
- Residual-conditioned case-specific via/gap diagnostic
- Multi-tier decision rule with no-via false-positive guard

## Metrics

- case_count: 72
- OBGHI top1_accuracy: 0.2222
- OBGHI accepted_accuracy: 0.1803
- OBGHI accepted_risk: 0.8197
- OBGHI reject_rate: 0.0833
- OBGHI need_next_measurement_rate: 0.0694
- OBGHI via_gap_ambiguous_reject_rate: 0.1250
- OBGHI h0_top1_accuracy: 0.000e+00
- OBGHI h2_mean_true_posterior: 7.298e-29
- OBGHI h2_top1_accuracy: 0.000e+00
- OBGHI h3_top1_accuracy: 1.0000
- OBGHI h3_mean_true_posterior: 0.9307
- OBGHI no_via_false_positive_guard_count: 0
- Ridge-map top1_accuracy: 0.3333

## Operator diagnostics

- A shape: `[432, 1584]`
- via_columns_nonzero: `True`
- via_column_norm_min: `0.0103`
- via_column_norm_mean: `0.0179`

## Engineering Gates

| gate | passed |
|---|---:|
| posterior_rows_present | True |
| operator_via_columns_nonzero | True |
| topology_posterior_nontrivial | True |
| generated_domain_boundaries_recorded | True |
| leakage_audit_present | True |
| reports_written | True |

## Scientific Gates

| gate | passed |
|---|---:|
| accepted_risk_le_0_45 | False |
| reject_rate_ge_0_10_or_need_next_ge_0_20 | False |
| h0_top1_ge_0_50 | False |
| h2_true_posterior_ge_0_10_or_h2_reject_rate_ge_0_30 | False |
| h3_top1_ge_0_20_or_h3_need_next_reject_ge_0_40 | True |
| obghi_top1_beats_ridge_by_0_05 | False |
| via_gap_ambiguous_reject_nonzero_on_gap_or_via | True |

Engineering gates passed: `True`
Scientific gates passed: `False`

## Claim status change

None. Do not upgrade any claim. If scientific gates fail, E19.1 is
diagnostic/limiting evidence only. If they pass, E19.1 supports/motivates
the generated-domain claims but does not prove real validation.

## Failure modes

See `FAILURE_CASES.md` and `SCIENTIFIC_GATES.md`.

## Cannot claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real-board PDN/KCL robustness
- mechanism-level explanation on real data
- universal via detection
- that generated-domain evidence transfers to real hardware

## Next required evidence

1. Multi-height observation for standoff discrimination
2. Multi-state excitation for current-path discrimination
3. Replace generated families with CAD/Gerber/GDS-derived graph candidates
4. Validate against external solver (COMSOL/FastHenry/FEM) on small subset

## Tests run

See repository CI or run locally:
`uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests`

## Files changed

- `experiments/evidence/E19_obghi_minimal_observable_topology_posterior/`
- `research_graph/experiments.yml`
- `research_graph/evidence_edges.yml`
- `research_graph/update_log.md`
