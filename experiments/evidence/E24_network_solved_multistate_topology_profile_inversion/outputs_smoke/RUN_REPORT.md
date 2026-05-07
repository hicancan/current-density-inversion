# E24 Run Report

Evidence: E24_network_solved_multistate_topology_profile_inversion
Status: passed_with_limitations
Timestamp: 2026-05-06T10:24:20.162324+00:00
Runtime: 105.3s

## Engineering Gates

- package_runs_to_completion: PASS
- all_layouts_parse: PASS
- network_kcl_residual_below_tolerance: PASS
- conductances_positive: PASS
- topology_hypotheses_change_graph: PASS
- multi_state_shared_theta_implemented: PASS
- free_kcl_baseline_implemented: PASS
- operator_stress_executed: PASS
- reports_written: PASS
- generated_domain_boundary_explicit: PASS

## Scientific Gates
- shared_network_beats_free_kcl_wrong_topology: FAIL
- shared_network_reduces_consistent_set_size: PASS
- truth_in_consistent_set_rate_ge_0_90: PASS
- singleton_wrong_rate_eq_0: PASS
- empty_rate_le_0_10: PASS
- h1_h2_shared_profile_gap_positive_rate_ge_0_80: FAIL
- critical_pair_profile_gamma_positive_rate_ge_0_50: FAIL
- operator_stress_gamma_positive_rate_ge_0_30: FAIL

## Consistent Set
- Truth in consistent set: 1.000
- Empty rate: 0.000
- Singleton wrong: 0.000

## Cannot Claim
- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- universal via detection
- real-board PDN robustness
- mechanism-level explanation on real data
- that generated-domain ambiguity holds for all real hardware
- that network-solved topology profile inversion proves chip reverse analysis before real CAD/GDS-derived graphs, external forward validation, and real QDM/NV sanity gates exist