# RUN REPORT - E19 OBGHI Minimal Observable Topology Posterior

## Claim affected

- Primary: `C10_pdn_kcl_distribution_need`
- Secondary: `C06_graph_hypothesis_system_identification`, `C02_single_plane_identifiability_boundary`, `C04_inverse_crime_and_operator_gap`

## Evidence added

Generated-domain minimal OBGHI evidence package implementing posterior topology inference over H0/H1/H2/H3 explanations.

## Metrics

- case_count: 72
- OBGHI top1_accuracy: 0.3333
- OBGHI accepted_accuracy: 0.3455
- OBGHI accepted_risk: 0.6545
- OBGHI reject_rate: 0.000e+00
- OBGHI need_next_measurement_rate: 0.2361
- OBGHI via_gap_ambiguous_reject_rate: 0.000e+00
- Ridge-map top1_accuracy: 0.3333

## Operator diagnostics

- A shape: `[432, 1584]`
- via_columns_nonzero: `True`
- via_column_norm_min: `0.0103`
- via_column_norm_mean: `0.0179`

## Acceptance gates

| gate | passed |
|---|---:|
| posterior_rows_present | True |
| topology_posterior_nontrivial | True |
| accepted_risk_bounded | True |
| reject_or_need_next_available | True |
| via_gap_ambiguity_measured | True |
| obghi_matches_or_beats_ridge_top1 | True |
| generated_domain_boundaries_recorded | True |

All gates passed: `True`

## Failure modes

See `FAILURE_CASES.md`. Expected first-slice failure modes include accepted wrong topology, correct topology rejected under ambiguity, and need-next-measurement decisions.

## Claim status change

None in this ZIP. Do not upgrade any claim until the package is run locally and audited.

## Cannot claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real-board PDN/KCL robustness
- mechanism-level explanation on real data
- universal via detection

## Next required evidence

1. Run E19 locally and audit metrics.
2. Compare E19 failure slices against E18 physics-constrained inverse failure cases.
3. If E19 passes, register it in the research graph as generated-domain evidence only.
4. Add a follow-up multi-height / multi-state OBGHI information-gain evidence package.

## Tests run

Not run by this ZIP generator. Run locally with `uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests`.

## Files changed

This package only adds files under `experiments/evidence/E19_obghi_minimal_observable_topology_posterior/` unless you manually apply research graph snippets.
