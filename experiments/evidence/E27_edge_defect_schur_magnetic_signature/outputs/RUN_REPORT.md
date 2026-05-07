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

- A shape: `[432, 1488]`
- Edge count: `1488`
- Node count: `576`
- Via edges nonzero: `True`
- Laplacian rank: `575`

## Sherman-Morrison Validation

- Max relative error: `1.909e-14`
- Mean relative error: `7.075e-15`
- SM matches direct: `True`

## Candidate Edge Sensitivity

- Candidate defect count: `84`
- Families covered: `7`
- Mean edge signal: `0.002372`
- Mean edge Gamma: `-0.035664`
- Positive edge Gamma rate: `0.000e+00`

## Schur State Design

- Schur state count: `6`
- Schur mean signal: `0.002372`
- Schur mean Gamma: `-0.035664`
- Schur positive Gamma rate: `0.000e+00`

## Signal/Gamma Improvement Over Baselines

- Schur vs best other signal ratio: `0.557181x`
- Schur vs best other Gamma delta: `-0.001857`
- Best other baseline signal: `0.004257`
- Best other baseline Gamma: `-0.033807`

## Baseline Comparison

| strategy | state_count | mean_signal | mean_gamma | positive_gamma_rate |
|---|---:|---:|---:|---:|
| random | 6 | 0.002727 | -0.035314 | 0.005952 |
| max_current_norm | 6 | 0.004257 | -0.033807 | 0.017857 |
| max_resistance_contrast | 6 | 0.004179 | -0.033884 | 0.021825 |
| schur_voltage_drop | 6 | 0.002372 | -0.035664 | 0.000e+00 |
| oracle | 6 | 4.081e-04 | -0.037598 | 0.000e+00 |

## Pairwise Defect Gamma Matrix

- Total pairs: `3486`
- Mean pairwise delta: `0.008030`
- Max pairwise delta: `0.039297`
- Min pairwise delta: `2.493e-07`
- Mean pairwise Gamma: `-0.030211`
- Positive pairwise Gamma rate: `2.869e-04`

## Per-Family Edge Gamma

| family | count | mean_gamma | positive_rate |
|---|---:|---:|---:|
| via_insertion | 12 | -0.037734 | 0.000e+00 |
| via_removal | 12 | -0.037826 | 0.000e+00 |
| return_path_insertion | 12 | -0.035549 | 0.000e+00 |
| return_path_removal | 12 | -0.021356 | 0.000e+00 |
| local_open_segment | 12 | -0.037630 | 0.000e+00 |
| parasitic_short_bridge | 12 | -0.034957 | 0.000e+00 |
| deep_layer_alternate_return | 12 | -0.028931 | 0.000e+00 |

## Consistent Set Metrics

- Total defects: `84`
- Defects in consistent set: `0`
- In-set rate: `0.000e+00`
- Truth in consistent set rate: `0.000e+00`
- Singleton wrong count: `84`
- Singleton wrong rate: `1.000000`
- Empty count: `84`
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
| schur_states_beat_e26_generic_gamma | False |
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
