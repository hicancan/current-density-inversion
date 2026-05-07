# RUN REPORT - E27 Edge-Defect Schur Magnetic Signature Inversion

E27 is generated-domain algorithm evidence. It does not constitute real
QDM/NV, CAD/Gerber/GDS, or external-solver validation.

## Status

- Status: `passed_with_limitations`
- Engineering gates passed: `True`
- Scientific gates passed: `False`
- All acceptance gates passed: `False`

## Claims affected

- Primary: `C06_graph_hypothesis_system_identification`
- Secondary: `C02_single_plane_identifiability_boundary`, `C10_pdn_kcl_distribution_need`, `C13_calibration_protocol_reality`

## Operator diagnostics

- A shape: `[192, 640]`
- Edge count: `640`
- Node count: `256`
- Via edges nonzero: `True`
- Laplacian rank: `255`

## Sherman-Morrison Validation

- Max relative error: `2.150e-14`
- Mean relative error: `7.178e-15`
- SM matches direct: `True`

## Candidate Edge Sensitivity

- Candidate defect count: `8`
- Families covered: `4`
- Mean edge signal: `0.003414`
- Mean edge Gamma: `-0.071689`
- Positive edge Gamma rate: `0.000e+00`

## Schur State Design

- Schur state count: `4`
- Schur mean signal: `0.003414`
- Schur mean Gamma: `-0.071689`
- Schur positive Gamma rate: `0.000e+00`

## Signal/Gamma Improvement Over Baselines

- Schur vs best other signal ratio: `1.662400x`
- Schur vs best other Gamma delta: `0.001319`
- Best other baseline signal: `0.002053`
- Best other baseline Gamma: `-0.073008`

## Baseline Comparison

| strategy | state_count | mean_signal | mean_gamma | positive_gamma_rate |
|---|---:|---:|---:|---:|
| random | 4 | 0.001298 | -0.073741 | 0.000e+00 |
| max_current_norm | 4 | 0.001900 | -0.073157 | 0.000e+00 |
| max_resistance_contrast | 4 | 0.002053 | -0.073008 | 0.000e+00 |
| schur_voltage_drop | 4 | 0.003414 | -0.071689 | 0.000e+00 |
| oracle | 4 | 7.257e-04 | -0.074296 | 0.000e+00 |

## Pairwise Defect Gamma Matrix

- Total pairs: `28`
- Mean pairwise delta: `0.010166`
- Max pairwise delta: `0.025272`
- Min pairwise delta: `1.176e-04`
- Mean pairwise Gamma: `-0.065444`
- Positive pairwise Gamma rate: `0.000e+00`

## Per-Family Edge Gamma

| family | count | mean_gamma | positive_rate |
|---|---:|---:|---:|
| via_insertion | 2 | -0.074633 | 0.000e+00 |
| via_removal | 2 | -0.074838 | 0.000e+00 |
| return_path_insertion | 2 | -0.073662 | 0.000e+00 |
| return_path_removal | 2 | -0.055241 | 0.000e+00 |

## Consistent Set Metrics

- Total defects: `8`
- Defects in consistent set: `0`
- In-set rate: `0.000e+00`
- Truth in consistent set rate: `0.000e+00`
- Singleton wrong count: `8`
- Singleton wrong rate: `1.000000`
- Empty count: `8`
- Empty rate: `1.000000`

## Acceptance Gates

| gate | passed |
|---|---:|
| package_runs_to_completion | True |
| laplacian_solve_valid | True |
| sherman_morrison_matches_direct_solve | True |
| candidate_edge_families_generated | True |
| edge_segment_forward_runs | True |
| schur_state_design_implemented | True |
| baselines_implemented | True |
| reports_written | True |
| generated_domain_boundary_explicit | True |
| schur_states_beat_random_signal_by_2x | False |
| schur_states_beat_e26_generic_gamma | True |
| positive_edge_gamma_rate_ge_0_50 | False |
| positive_pairwise_defect_gamma_rate_ge_0_30 | False |
| via_return_pair_gamma_positive_rate_ge_0_50 | False |
| truth_in_consistent_set_rate_ge_0_90 | False |
| singleton_wrong_rate_eq_0 | False |
| empty_rate_le_0_10 | False |

## Failure Modes

See `FAILURE_MODES.md`.

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real-board PDN/KCL robustness
- Schur minimax with hardware port constraints (current limits, pad positions)
- universal edge-defect detection
- finite-width conductor corrections (multifilament)
- multi-height sensor validation
- generated-domain evidence transfers to real hardware

## Next Required Evidence

1. Replace generated defect geometries with CAD/Gerber/GDS-derived candidate families
2. Validate Sherman-Morrison perturbation against external FEM/FastHenry on a small subset
3. Calibrate operator perturbation rho against E25 finite-width/registration tests
4. Scale Schur state design across layout ensemble (not single hand-picked network)
5. Test Schur minimax against real port-feasible constraints (current limits, pad positions)

## Files Changed

- `experiments/evidence/E27_edge_defect_schur_magnetic_signature/` (all files created)
