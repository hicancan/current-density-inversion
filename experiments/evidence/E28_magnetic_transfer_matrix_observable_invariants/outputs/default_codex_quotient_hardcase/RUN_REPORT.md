# RUN REPORT - E28 Magnetic Transfer-Matrix Observable Invariants

Status: **passed**
Engineering gates passed: **True**
Scientific gates passed: **True**

## Engineering Gates

| gate | passed |
|---|---:|
| transfer_matrix_computed | True |
| transfer_matrix_nontrivial | True |
| invariants_computed | True |
| nuisance_stress_executed | True |
| reports_written | True |
| generated_domain_boundary_explicit | True |
| pairwise_distances_computed | True |

## Scientific Gates

| gate | passed |
|---|---:|
| selected_invariant_is_not_raw | True |
| selected_invariant_gamma_beats_raw_gamma | True |
| selected_invariant_positive_gamma_rate_ge_0_30 | True |
| selected_invariant_critical_pair_positive_gamma_rate_ge_0_30 | True |
| selected_invariant_rho_less_than_raw_rho | True |
| selected_invariant_nontrivial | True |
| observable_quotient_selected_invariant_all_positive | True |
| hard_h1_h2_reported_unresolved | True |
| hardcase_gain_sweep_executed | True |
| hardcase_gram_quotient_survives_when_raw_fails | True |
| truth_in_consistent_set_rate_ge_0_90 | True |
| singleton_wrong_rate_eq_0 | True |

## Transfer Matrix Diagnostics

| hypothesis | shape | eff_rank | cond | frob_norm | max_col | min_col |
|---|---:|---:|---:|---:|---:|---:|
| H0_no_via | [432, 6] | 6 | 2.80e+01 | 21.7415 | 14.4051 | 2.9162 |
| H1_via | [432, 6] | 6 | 2.39e+01 | 18.2531 | 10.3363 | 2.8798 |
| H2_model_gap | [432, 6] | 6 | 2.39e+01 | 18.2364 | 10.3425 | 2.8416 |
| H3_return_path | [432, 6] | 6 | 1.76e+01 | 17.4208 | 10.6862 | 2.7351 |

## Raw vs Invariant Margin Comparison

### Nuisance Radii

- Raw field nuisance radius: 0.798817
- Projector nuisance radius: 0.088068
- Gram nuisance radius: 0.037428
- Differential nuisance radius: 1.234101

### Nuisance Reduction Factors

- Projector reduction: 0.1102
- Gram reduction: 0.0469
- Differential reduction: 1.5449

### Invariant Beats Raw

- projector_beats_raw: True
- gram_beats_raw: True
- differential_beats_raw: True

### Margin Summary

- Best invariant: **gram**
- Positive gamma (raw): 0.8333
- Positive gamma (projector): 0.0000
- Positive gamma (gram): 0.8333
- Positive gamma (differential): 0.8333
- Critical pair gamma (raw): 1.0000
- Critical pair gamma (projector): 0.0000
- Critical pair gamma (gram): 1.0000

## Observable Quotient Certificate

The run distinguishes quotient groups, not all four hypotheses:
- Q0_no_via = {H0_no_via}
- Q12_via_or_model_gap = {H1_via, H2_model_gap}
- Q3_return_path = {H3_return_path}

- Selected invariant: **gram**
- Quotient min Gamma: 0.451121
- Quotient all positive: True
- H1/H2 hard-pair Gamma: -0.128614
- H1/H2 reported unresolved: True

## Gain Hard-Case Sweep

- Sweep count: 5
- Raw-fails/Gram-passes count: 3
- First gain where raw fails and Gram passes: 0.08
- Gram quotient survival rate: 1.0000
- Max gain with positive Gram quotient: 0.18
- H1/H2 unresolved across sweep: True

## Consistent Set Analysis

- n_cases: 72
- epsilon: 2.291026
- nonempty rate: 1.0000
- ambiguity rate: 0.6667
- empty rate: 0.0000
- truth-in-consistent rate: 1.0000
- singleton correct rate: 0.3333
- singleton wrong rate: 0.0000

## Scope & Limitations

This evidence is scoped to the generated-domain graph conductance model
under ideal free-space Biot-Savart forward. The transfer matrix approach
is evaluated on four topology hypotheses (H0-H3) with known graph structure.

The invariant margin improvements are demonstrated within this controlled
generated domain. Extrapolation to real hardware with unknown graph topology,
unknown conductance values, and unknown noise statistics is not claimed.

## Cannot Claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
- That invariants work for all real hardware
- That generated-domain margins hold for all observation protocols
- That transfer matrix approach replaces all existing methods
- That nuisance model captures all real-world perturbation families
- That H1_via and H2_model_gap are separable under this generator
- Full four-hypothesis robust separability