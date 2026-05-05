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

## OQCI Metrics (scoped to generated-domain admissible basis family)

- case_count: 72
- primary epsilon: 0.9353
- consistent_set_nonempty_rate: 1.0000
- ambiguity_rate: 1.0000
- mean_interval_width: 1.0000
- near_null_count: 50
- effective_rank: 27

## Epsilon Sensitivity Sweep

| multiplier | epsilon | nonempty_rate | ambiguity_rate | empty_rate |
|---|---:|---:|---:|---:|
| 0.5 | 0.1871 | 0.0000 | 0.0000 | 1.0000 |
| 1.0 | 0.3741 | 0.8472 | 0.7083 | 0.1528 |
| 1.5 | 0.5612 | 1.0000 | 1.0000 | 0.0000 |
| 2.0 | 0.7482 | 1.0000 | 1.0000 | 0.0000 |
| 2.5 | 0.9353 | 1.0000 | 1.0000 | 0.0000 |
| 3.0 | 1.1224 | 1.0000 | 1.0000 | 0.0000 |

## Decision Distribution

- ambiguous: 72

## Scope & Limitations

This evidence is scoped to the generated-domain admissible basis family
(E19.2 basis: graph + residual + via/gap/return blocks) under ideal
free-space Biot-Savart forward. The ambiguity findings do not constitute
an absolute physical theorem about all possible observation protocols.
They demonstrate that under the CURRENT experiment family and basis
construction, H0/H1/H2/H3 topology claims are not forced by the data.

## Cannot Claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
- That this generated-domain ambiguity holds for ALL real hardware
- An absolute physical identifiability theorem (this is a basis-family audit)