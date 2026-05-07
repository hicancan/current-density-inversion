# RUN REPORT - E26 Active Port-State Gamma Design

Status: **passed_with_limitations**
Engineering gates passed: **True**
Scientific gates passed: **False**

## Engineering Gates

| gate | passed |
|---|---:|
| package_runs_to_completion | True |
| feasible_port_states_generated | True |
| state_constraints_satisfied | True |
| greedy_gamma_implemented | True |
| two_step_or_lookahead_implemented | True |
| baselines_implemented | True |
| sequential_refusal_reported | True |
| reports_written | True |
| generated_domain_boundary_explicit | True |

## Scientific Gates

| gate | passed |
|---|---:|
| greedy_gamma_beats_random_by_0_10 | False |
| greedy_gamma_beats_default | False |
| two_step_beats_greedy_or_ties | True |
| critical_pair_gamma_improves_with_states | True |
| wrong_accept_rate_decreases_with_states | False |
| truth_missing_rate_le_0_10 | True |
| mean_states_used_le_smax | True |
| positive_gamma_rate_ge_0_50 | False |

## Aggregate Metrics

- Layout count: 24
- Greedy min Gamma (mean): -inf
- Two-step min Gamma (mean): -inf
- Random min Gamma (mean): -inf
- Single default min Gamma (mean): -inf
- Truth missing rate: 0.0000
- Wrong accept rate: 0.0000
- Mean states used: 0.00
- Positive Gamma rate: 0.0000
- Gamma improves with states: True
- Wrong accept decreases: False

## Scope & Limitations

This evidence is scoped to generated-domain port-network layouts
with simplified resistance-network models. The state design strategy
is demonstrated on these generated layouts only.

## Cannot Claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
- That generated-domain port-state optimality transfers to real hardware
- Real-world port excitation hardware feasibility

## Next Required Evidence

- E24 shared-network profile topology separability results
- Real port-state hardware constraints from QDM/NV testbed
- Validation against E23 multi-state excitation measurements on same layouts