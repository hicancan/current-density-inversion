# RUN REPORT - E19.2 OQCI Identifiability Audit

Status: **passed_with_limitations**
Engineering gates passed: **True**
Scientific gates passed: **False**

## Engineering Gates

| gate | passed |
|---|---:|---:|
| consistent_set_nonempty | True |
| pairwise_distances_computed | True |
| near_null_modes_extracted | True |
| claim_intervals_valid | True |
| generated_domain_boundaries_recorded | True |
| leakage_audit_present | True |
| reports_written | True |

## Scientific Gates

| gate | passed |
|---|---:|---:|
| consistent_set_nonempty_rate_ge_0_95 | True |
| ambiguity_rate_ge_0_50 | True |
| no_wrong_high_confidence_accepts | True |
| ambiguity_rate_reduces_with_multi_height | False |
| near_null_dimension_decreases_with_multi_height | False |
| claim_interval_width_reduces_with_multi_height_ge_0_20 | False |

## OQCI Metrics

- case_count: 72
- epsilon: 0.9353
- consistent_set_nonempty_rate: 1.0000
- ambiguity_rate: 1.0000
- mean_interval_width: 1.0000
- near_null_count: 50
- effective_rank: 27

## Decision Distribution

- ambiguous: 72

## Cannot Claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
- That generated-domain ambiguity holds for all real hardware