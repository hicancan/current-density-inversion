# E23 R5 Run
Status: partial
Layouts: 4 mp=3
min_gamma_all=-5064.8324 min_gamma_crit=-5064.7263
H1/H2 gamma=-2445.3387 cert_rate=0.000
Adv worst gamma=-7139.0144 pos=False
## Gates
- [PASS] all_layouts_parse
- [PASS] incidence_matrix_valid
- [PASS] basis_blocks_have_expected_dims
- [PASS] port_loop_kcl_below_tolerance
- [PASS] svd_projected_blocks_kcl_below_tolerance
- [PASS] raw_blocks_kcl_reported_not_gated
- [PASS] graph_hodge_reduces_dimension
- [PASS] basis_not_trivial
- [PASS] residual_basis_present
- [FAIL] layout_ensemble_count_ge_40
- [FAIL] multiport_layout_count_ge_30
- [FAIL] h1_h2_hardcase_gamma_positive
- [FAIL] h1_h2_gamma_positive_rate_ge_0_90
- [FAIL] critical_pair_certified_rate_ge_0_80
- [FAIL] greedy_port_states_beat_default
- [FAIL] greedy_port_states_beat_random
- [FAIL] adversarial_h1_h2_gamma_positive
- [PASS] adversarial_wrong_accept_rate_le_0_10
- [PASS] adversarial_truth_missing_rate_le_0_10
- [PASS] no_internal_actuation_needed

All: False