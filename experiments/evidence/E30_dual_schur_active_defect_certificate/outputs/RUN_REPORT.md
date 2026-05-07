# E30 RUN REPORT - Dual-Schur Active Defect Certificate

- Metrics file: `outputs/metrics.json`

Generated: 2026-05-06T15:09:22.368114+00:00

E30 is generated-domain evidence. It does not constitute real QDM/NV,
CAD/GDS, external-solver, or real chip reverse-analysis validation.

## Status

- Status: `passed`
- Engineering gates passed: `True`
- Scientific gates passed: `True`
- All acceptance gates passed: `True`

## Main Result

- Candidate family: `central_via_open`
- Candidate defects: `8`
- Boundary control min Gamma, no nuisance: `-0.06399999999`
- Perimeter boundary upper-bound min Gamma, no nuisance: `-0.06399999992`
- Dual Schur min Gamma after noise/nuisance/tau: `0.1348041937`
- Dual Schur all pair positive: `True`
- Dual truth pairwise certified rate: `1.0`

## Current Budget Law

- Noise plus tau: `0.064`
- Dual usable slope per amp: `0.003976083874`
- Dual critical amplitude: `16.09623992`
- Configured dual amplitude: `50`
- Boundary optimistic critical amplitude: `3.191177882e+11`
- Perimeter boundary optimistic critical amplitude: `4.117612711e+10`

## Acceptance Gates

| gate | passed |
|---|---:|
| package_runs_to_completion | True |
| e28_operator_reused | True |
| candidate_defects_generated | True |
| boundary_control_executed | True |
| perimeter_boundary_upper_bound_executed | True |
| dual_schur_ports_executed | True |
| directional_nuisance_audit_executed | True |
| reports_written | True |
| generated_domain_boundary_explicit | True |
| no_external_or_real_data_used | True |
| dual_all_pair_positive_after_noise_nuisance_tau | True |
| dual_min_gamma_ge_0_05 | True |
| dual_beats_boundary_min_gamma_by_0_10 | True |
| boundary_control_negative_without_nuisance | True |
| perimeter_boundary_upper_bound_negative_without_nuisance | True |
| dual_configured_current_above_critical | True |
| boundary_configured_current_below_optimistic_critical | True |
| perimeter_configured_current_below_optimistic_critical | True |
| truth_pairwise_certified_rate_eq_1 | True |

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real chip reverse analysis
- pad-feasible active probing; dual endpoint excitation is a local-access observability upper bound
- arbitrary current recovery outside the configured central via-open candidate set
- H1_via versus H2_model_gap separation
- via-short, return-path, dense-cluster, or finite-width defect resolution
- that generated-domain positive Gamma transfers to real hardware

## Next Required Evidence

- Constrain the dual Schur source patterns to real pad-accessible boundary ports and optimize the closest feasible drives.
- Repeat the certificate over broader generated layout ensembles and non-central via defects.
- Add finite-width, registration, layer-z, and external solver transfer-matrix rho components.
- Validate a small candidate set against CAD/GDS-derived graphs and independent FastHenry/COMSOL-style solves.
- Only after simple-wire and known-via sanity gates, test on real QDM/NV measurements.
