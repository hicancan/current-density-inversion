# E33 RUN REPORT - Certified Observable Current Subspace Inversion

Generated: 2026-05-07T08:28:45.267075+00:00

E33 is generated-domain current-inversion evidence. It does not claim complete
current recovery, real QDM/NV validation, CAD/GDS validation, or external-solver
validation. It claims only the Fisher-stable current projection under the
configured thin-sheet Fourier/Biot-Savart model.

## Status

- Status: `passed`
- Engineering gates passed: `True`
- Scientific gates passed: `True`
- All acceptance gates passed: `True`
- Metrics file: `outputs/metrics.json`

## Main Result

- Mode count: `144`
- Single-height stable modes: `8`
- Single-height dark modes: `136`
- Single-height truth dark energy fraction: `0.9228192454`
- Certified stable projection RMSE: `0.1164511532`
- Full naive inverse total RMSE: `720.7362501`
- Certified inverse total RMSE: `0.4657956787`
- Full/certified total RMSE ratio: `1547.322749`
- Full dark hallucination norm: `8649.239996`
- Certified dark hallucination norm: `0`
- Stable confidence coverage: `1`
- Multi-height stable modes: `37`

## Acceptance Gates

| gate | passed |
|---|---:|
| package_runs_to_completion | True |
| mode_table_constructed | True |
| single_height_protocol_executed | True |
| multi_height_protocol_executed | True |
| fisher_spectrum_reported | True |
| reports_written | True |
| generated_domain_boundary_explicit | True |
| no_external_or_real_data_used | True |
| single_height_has_stable_modes | True |
| truth_contains_material_dark_energy | True |
| certified_stable_projection_rmse_below_gate | True |
| full_naive_inverse_is_worse_than_certified_projection | True |
| certified_inverse_does_not_hallucinate_dark_modes | True |
| stable_confidence_intervals_cover_truth | True |
| multi_height_expands_stable_current_subspace | True |
| multi_height_reduces_dark_energy_fraction | True |

## Cannot Claim

- full current-density recovery
- dark current modes are recovered
- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- finite-width conductor or package parasitic robustness
- multi-layer chip current recovery under real layouts
- that the Fourier thin-sheet generated result transfers to measured data

## Next Required Evidence

- Move the certified observable-subspace split from diagonal Fourier modes to graph/Hodge/CAD-like current bases.
- Add finite-width, registration, background, and external-solver rho terms to the Fisher threshold.
- Validate the observable projection on independent solver rows and then real QDM/NV sanity-gated rows.
- Combine E33 observable current modes with E30-E32 active pad reachability for observable-reachable current-mode inversion.
