# RUN REPORT - E20 Active OQCI Measurement Design (Round 2)

Status: **passed_with_limitations**
Engineering gates passed: **True**
Scientific gates passed: **False**

## Engineering Gates

| gate | passed |
|---|---|
| candidate_pool_nonempty | True |
| candidate_count_ge_4 | True |
| baseline_oqci_computed | True |
| every_candidate_has_utility | True |
| epsilon_sweep_present | True |
| regularization_sweep_present | True |
| calibration_split_present | True |
| truth_coverage_audit_present | True |
| reports_written | True |
| leakage_audit_present | True |
| generated_domain_boundaries_recorded | True |

## Scientific Gates

| gate | passed |
|---|---|
| ambiguity_rate_reduction_gt_0 | False |
| claim_interval_width_reduction_ge_0_10 | False |
| no_wrong_high_confidence_accepts | True |
| best_not_residual_only | True |
| valid_disambiguation_rate_ge_0_50 | False |
| truth_in_consistent_set_rate_ge_0_90 | True |
| singleton_wrong_rate_eq_0 | True |
| empty_rate_le_0_10 | True |
| any_candidate_passes_all_four | False |
| best_coverage_pair | add_h1.6_Bxyz@1.5 |
| regularized_valid_disambiguation_rate_ge_0_50 | False |
| regularized_truth_in_consistent_set_rate_ge_0_90 | False |
| regularized_singleton_wrong_rate_eq_0 | True |
| regularized_empty_rate_le_0_10 | False |
| regularization_beats_ols_by_0_20 | False |
| all_regularized_gates_pass | False |
| best_regularized_coverage_pair | add_h1.6_Bxyz:ridge@λ=1e-02 |
| calibration_eval_vdr_nondegenerate | True |
| pairwise_margin_policy_improves_min_gamma | False |
| pairwise_margin_policy_improves_vdr_by_0_20 | False |
| two_step_policy_min_gamma_positive | False |
| two_step_policy_truth_coverage_ge_0_90 | True |
| two_step_policy_singleton_wrong_rate_eq_0 | True |
| two_step_policy_empty_rate_le_0_10 | True |
| critical_h1_h2_gamma_positive | False |

## Summary Metrics

- case_count: 18
- candidate_count: 11
- baseline_ambiguity_rate: 1.0000
- baseline_mean_interval_width: 1.0000
- baseline_near_null_count: 50
- baseline_effective_rank: 26
- best_candidate: add_h1.6_Bz
- runtime_s: 17.0

## Best Candidate by Epsilon

| epsilon_mult | best_candidate |
|---|---:|
| 0.5 | add_h1.6_Bz |
| 1.0 | add_h1.6_Bz |
| 1.5 | add_h1.6_Bz |
| 2.0 | add_h1.6_Bz |
| 2.5 | add_h1.6_Bz |
| 3.0 | add_h1.6_Bz |

## Scope & Limitations

Generated-domain OQCI with epsilon sweep, multi-height, multi-component,
and multi-state excitation candidates. No real QDM/NV, CAD/GDS, or
external solver validation.

## Cannot Claim

- real QDM/NV validation
- real CAD/GDS validation
- hardware feasibility of active measurement
- universal multilayer recovery
- that generated multi-height improvements transfer to real devices
- that no improvement means all physical measurement protocols are useless