# E31 RUN REPORT - Pad-Schur Reachability Certificate

Generated: 2026-05-06T15:25:22.981182+00:00

E31 is generated-domain evidence. It does not constitute real QDM/NV,
CAD/GDS, external-solver, or real chip reverse-analysis validation.

## Status

- Status: `passed`
- Engineering gates passed: `True`
- Scientific gates passed: `True`
- All acceptance gates passed: `True`

## Main Result

- Candidate defects: `8`
- Perimeter reachability min ratio: `2.48821324e-09`
- Top-candidate surface pad reachability min ratio: `0.4767196129`
- Pad-Schur pairwise positive rate: `1`
- Pad-Schur min Gamma after nuisance: `0.01963293336`
- Pad-Schur truth pairwise certified rate: `1`
- Pad-Schur critical amplitude: `38.26243887`
- Configured amplitude: `50`

## Acceptance Gates

| gate | passed |
|---|---:|
| package_runs_to_completion | True |
| e30_e28_operator_reused | True |
| candidate_defects_generated | True |
| reachability_theorem_evaluated | True |
| pad_schur_certificate_executed | True |
| negative_controls_executed | True |
| reports_written | True |
| generated_domain_boundary_explicit | True |
| no_external_or_real_data_used | True |
| top_candidate_reachability_ratio_min_ge_0_30 | True |
| perimeter_reachability_ratio_min_le_1e_minus_6 | True |
| pad_schur_all_pair_positive_after_nuisance | True |
| pad_schur_min_gamma_positive | True |
| pad_schur_truth_pairwise_certified_rate_eq_1 | True |
| pad_current_budget_above_critical | True |

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real chip reverse analysis
- perimeter-only pad probing works
- arbitrary current recovery outside the configured central via-open candidate set
- that candidate-projection pads exist or are usable on a real chip without design-for-test access
- finite-width, contact resistance, frequency-dependent, or package parasitic robustness
- that generated-domain positive Gamma transfers to real hardware

## Next Required Evidence

- Constrain the top-candidate pad design to realistic pad pitch, current limits, contact resistance, and package parasitics.
- Stress pad-Schur synthesis over broader/non-central defect families and layout ensembles.
- Add finite-width, registration, layer-z, and external-solver rho to the pad-Schur certificate.
- Validate pad reachability and magnetic signatures on CAD/GDS-derived graphs and independent solver rows.
- Only after real simple-wire/known-via sanity gates, test on QDM/NV measurements.
