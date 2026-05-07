# E21 External-Solver Operator-Gap Ladder — Run Report

## Gate Summary

Overall: FAIL

- package_runs_to_completion: PASS — metrics.json written
- all_operators_same_shape: PASS — all field maps have identical shape
- operator_gaps_nonzero: PASS — at least one operator gap > 0
- decision_stress_executed: PASS — at least one cross-operator decision test run
- external_artifact_contract_written: PASS — EXTERNAL_ARTIFACT_CONTRACT.md exists with blocked/interface status
- reports_written: PASS — all required reports present
- no_fake_external_validation: PASS — external_validation_status is blocked when artifacts missing
- generated_domain_boundary_explicit: PASS — PyPEEC results marked generated-domain
- decision_instability_ratio_gt_1_25: PASS — at least one mechanism cross/same accuracy ratio > 1.25
- template_same_operator_accuracy_ge_0_60: FAIL — template evidence scorer same-operator accuracy >= 0.60
- template_cross_operator_drop_ge_0_20: FAIL — template scorer cross-operator accuracy drop >= 0.20
- ridge_same_operator_accuracy_ge_0_60: FAIL — ridge evidence scorer same-operator accuracy >= 0.60
- ridge_cross_operator_drop_ge_0_20: FAIL — ridge scorer cross-operator accuracy drop >= 0.20
- ridge_wrong_accept_rate_cross_le_0_10_at_refusal: FAIL — ridge wrong-accept rate cross-op <= 0.10 at refusal
- ridge_accepted_accuracy_cross_ge_0_80_at_refusal: FAIL — ridge accepted accuracy cross-op >= 0.80 at refusal
- pyquant_external_solver_pipeline_completed: FAIL — external solver pipeline completed (PyPEEC/FastHenry/COMSOL)
- multibasis_same_operator_accuracy_ge_0_60: FAIL — multibasis evidence scorer same-op accuracy >= 0.60
- multibasis_cross_operator_drop_ge_0_20: FAIL — multibasis cross-operator accuracy drop >= 0.20
- operator_shift_less_than_half_margin: FAIL — operator shift radius < 0.5 * interclass delta min
- margin_refusal_wrong_accept_rate_le_0_10: FAIL — margin refusal wrong-accept rate <= 0.10
- margin_refusal_accepted_accuracy_ge_0_80: FAIL — margin refusal accepted accuracy >= 0.80
- external_solver_used_in_metrics: FAIL — external solver contributes to any metric

## Key Metrics

- case_count: 6
- available_operator_count: 6
- external_solver_artifacts_present: False
- unit_sanity_passed: True

### Operator Gap Table

| Pair | Rel RMSE | Per-Component |
|---|---|---|
| straight_wire__analytic_reference_vs_centerline_biot_savart | 3.2485e-01 | Bx=0.0000e+00 By=2.8287e-01 Bz=3.9390e-01 |
| straight_wire__analytic_reference_vs_deep_layer_shift_surrogate | 2.7242e-01 | Bx=0.0000e+00 By=2.5761e-01 Bz=2.9542e-01 |
| straight_wire__analytic_reference_vs_finite_width_surrogate | 7.8138e-01 | Bx=0.0000e+00 By=8.1779e-01 Bz=7.2437e-01 |
| straight_wire__analytic_reference_vs_missing_return_surrogate | 2.8786e-01 | Bx=0.0000e+00 By=2.5254e-01 Bz=3.4524e-01 |
| straight_wire__analytic_reference_vs_registration_gap_surrogate | 3.4426e-01 | Bx=0.0000e+00 By=3.0212e-01 Bz=4.1412e-01 |
| straight_wire__centerline_biot_savart_vs_deep_layer_shift_surrogate | 2.8003e-01 | Bx=0.0000e+00 By=2.5989e-01 Bz=3.1065e-01 |
| straight_wire__centerline_biot_savart_vs_finite_width_surrogate | 4.0923e-01 | Bx=0.0000e+00 By=4.8094e-01 Bz=2.7085e-01 |
| straight_wire__centerline_biot_savart_vs_missing_return_surrogate | 4.4123e-02 | Bx=0.0000e+00 By=4.0813e-02 Bz=4.9818e-02 |
| straight_wire__centerline_biot_savart_vs_registration_gap_surrogate | 9.8515e-02 | Bx=0.0000e+00 By=9.2070e-02 Bz=1.0998e-01 |
| straight_wire__deep_layer_shift_surrogate_vs_finite_width_surrogate | 7.4860e-01 | Bx=0.0000e+00 By=7.9109e-01 Bz=6.8113e-01 |
| straight_wire__deep_layer_shift_surrogate_vs_missing_return_surrogate | 3.0908e-01 | Bx=0.0000e+00 By=2.7919e-01 Bz=3.5916e-01 |
| straight_wire__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 3.8830e-01 | Bx=0.0000e+00 By=3.5147e-01 Bz=4.5141e-01 |
| straight_wire__finite_width_surrogate_vs_missing_return_surrogate | 3.2234e-01 | Bx=0.0000e+00 By=3.5612e-01 Bz=2.4553e-01 |
| straight_wire__finite_width_surrogate_vs_registration_gap_surrogate | 3.2083e-01 | Bx=0.0000e+00 By=3.5335e-01 Bz=2.4554e-01 |
| straight_wire__missing_return_surrogate_vs_registration_gap_surrogate | 1.1238e-01 | Bx=0.0000e+00 By=1.0472e-01 Bz=1.2594e-01 |
| wire_loop__analytic_reference_vs_centerline_biot_savart | 3.7777e+00 | Bx=3.4372e+00 By=3.4372e+00 Bz=4.0905e+00 |
| wire_loop__analytic_reference_vs_deep_layer_shift_surrogate | 2.3622e+00 | Bx=2.1160e+00 By=2.1160e+00 Bz=2.5859e+00 |
| wire_loop__analytic_reference_vs_finite_width_surrogate | 4.2493e+00 | Bx=3.8587e+00 By=3.8587e+00 Bz=4.6101e+00 |
| wire_loop__analytic_reference_vs_missing_return_surrogate | 3.5043e+00 | Bx=3.1802e+00 By=3.1802e+00 Bz=3.8015e+00 |
| wire_loop__analytic_reference_vs_registration_gap_surrogate | 3.7940e+00 | Bx=3.4612e+00 By=3.4497e+00 Bz=4.1051e+00 |
| wire_loop__centerline_biot_savart_vs_deep_layer_shift_surrogate | 3.6252e-01 | Bx=3.6217e-01 By=3.6217e-01 Bz=3.6287e-01 |
| wire_loop__centerline_biot_savart_vs_finite_width_surrogate | 1.6232e-01 | Bx=1.4951e-01 By=1.4951e-01 Bz=1.7430e-01 |
| wire_loop__centerline_biot_savart_vs_missing_return_surrogate | 6.6250e-02 | Bx=6.6240e-02 By=6.6240e-02 Bz=6.6260e-02 |
| wire_loop__centerline_biot_savart_vs_registration_gap_surrogate | 2.1539e-01 | Bx=2.4520e-01 By=1.8014e-01 Bz=2.1564e-01 |
| wire_loop__deep_layer_shift_surrogate_vs_finite_width_surrogate | 6.4015e-01 | Bx=6.3712e-01 By=6.3712e-01 Bz=6.4320e-01 |
| wire_loop__deep_layer_shift_surrogate_vs_missing_return_surrogate | 4.4660e-01 | Bx=4.4628e-01 By=4.4628e-01 Bz=4.4692e-01 |
| wire_loop__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 6.1341e-01 | Bx=6.3205e-01 By=5.9355e-01 Bz=6.1371e-01 |
| wire_loop__finite_width_surrogate_vs_missing_return_surrogate | 1.7100e-01 | Bx=1.6284e-01 By=1.6284e-01 Bz=1.7882e-01 |
| wire_loop__finite_width_surrogate_vs_registration_gap_surrogate | 2.6212e-01 | Bx=2.8096e-01 By=2.2684e-01 Bz=2.6874e-01 |
| wire_loop__missing_return_surrogate_vs_registration_gap_surrogate | 2.3520e-01 | Bx=2.6498e-01 By=2.0049e-01 Bz=2.3544e-01 |
| finite_width_trace__analytic_reference_vs_centerline_biot_savart | 3.2645e-01 | Bx=0.0000e+00 By=2.8398e-01 Bz=3.9717e-01 |
| finite_width_trace__analytic_reference_vs_deep_layer_shift_surrogate | 2.6235e-01 | Bx=0.0000e+00 By=2.4834e-01 Bz=2.8456e-01 |
| finite_width_trace__analytic_reference_vs_finite_width_surrogate | 7.9699e-01 | Bx=0.0000e+00 By=8.3236e-01 Bz=7.4089e-01 |
| finite_width_trace__analytic_reference_vs_missing_return_surrogate | 2.9172e-01 | Bx=0.0000e+00 By=2.5506e-01 Bz=3.5213e-01 |
| finite_width_trace__analytic_reference_vs_registration_gap_surrogate | 3.4493e-01 | Bx=0.0000e+00 By=3.0237e-01 Bz=4.1635e-01 |
| finite_width_trace__centerline_biot_savart_vs_deep_layer_shift_surrogate | 2.6839e-01 | Bx=0.0000e+00 By=2.4901e-01 Bz=2.9840e-01 |
| finite_width_trace__centerline_biot_savart_vs_finite_width_surrogate | 4.1754e-01 | Bx=0.0000e+00 By=4.8950e-01 Bz=2.7683e-01 |
| finite_width_trace__centerline_biot_savart_vs_missing_return_surrogate | 3.8169e-02 | Bx=0.0000e+00 By=3.5651e-02 Bz=4.2633e-02 |
| finite_width_trace__centerline_biot_savart_vs_registration_gap_surrogate | 9.5665e-02 | Bx=0.0000e+00 By=8.9580e-02 Bz=1.0666e-01 |
| finite_width_trace__deep_layer_shift_surrogate_vs_finite_width_surrogate | 7.5136e-01 | Bx=0.0000e+00 By=7.9503e-01 Bz=6.8079e-01 |
| finite_width_trace__deep_layer_shift_surrogate_vs_missing_return_surrogate | 2.9991e-01 | Bx=0.0000e+00 By=2.7068e-01 Bz=3.4973e-01 |
| finite_width_trace__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 3.6910e-01 | Bx=0.0000e+00 By=3.3447e-01 Bz=4.2934e-01 |
| finite_width_trace__finite_width_surrogate_vs_missing_return_surrogate | 3.2556e-01 | Bx=0.0000e+00 By=3.5908e-01 Bz=2.4791e-01 |
| finite_width_trace__finite_width_surrogate_vs_registration_gap_surrogate | 3.2226e-01 | Bx=0.0000e+00 By=3.5479e-01 Bz=2.4573e-01 |
| finite_width_trace__missing_return_surrogate_vs_registration_gap_surrogate | 1.0647e-01 | Bx=0.0000e+00 By=9.9624e-02 Bz=1.1883e-01 |
| via_vertical_segment__analytic_reference_vs_centerline_biot_savart | 0.0000e+00 | Bx=0.0000e+00 By=0.0000e+00 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_deep_layer_shift_surrogate | 5.5899e-01 | Bx=5.5899e-01 By=5.5899e-01 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_finite_width_surrogate | 9.9605e-02 | Bx=9.9605e-02 By=9.9605e-02 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_missing_return_surrogate | 9.9605e-02 | Bx=9.9605e-02 By=9.9605e-02 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_registration_gap_surrogate | 2.6607e-01 | Bx=2.2296e-01 By=3.0312e-01 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_deep_layer_shift_surrogate | 5.5899e-01 | Bx=5.5899e-01 By=5.5899e-01 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_finite_width_surrogate | 9.9605e-02 | Bx=9.9605e-02 By=9.9605e-02 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_missing_return_surrogate | 9.9605e-02 | Bx=9.9605e-02 By=9.9605e-02 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_registration_gap_surrogate | 2.6607e-01 | Bx=2.2296e-01 By=3.0312e-01 Bz=0.0000e+00 |
| via_vertical_segment__deep_layer_shift_surrogate_vs_finite_width_surrogate | 8.3570e-01 | Bx=8.3570e-01 By=8.3570e-01 Bz=0.0000e+00 |
| via_vertical_segment__deep_layer_shift_surrogate_vs_missing_return_surrogate | 8.3570e-01 | Bx=8.3570e-01 By=8.3570e-01 Bz=0.0000e+00 |
| via_vertical_segment__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 1.1037e+00 | Bx=1.0765e+00 By=1.1303e+00 Bz=0.0000e+00 |
| via_vertical_segment__finite_width_surrogate_vs_missing_return_surrogate | 0.0000e+00 | Bx=0.0000e+00 By=0.0000e+00 Bz=0.0000e+00 |
| via_vertical_segment__finite_width_surrogate_vs_registration_gap_surrogate | 3.0968e-01 | Bx=2.6628e-01 By=3.4773e-01 Bz=0.0000e+00 |
| via_vertical_segment__missing_return_surrogate_vs_registration_gap_surrogate | 3.0968e-01 | Bx=2.6628e-01 By=3.4773e-01 Bz=0.0000e+00 |
| return_path_pair__analytic_reference_vs_centerline_biot_savart | 2.6879e-01 | Bx=0.0000e+00 By=2.3984e-01 Bz=3.1076e-01 |
| return_path_pair__analytic_reference_vs_deep_layer_shift_surrogate | 6.7115e-01 | Bx=0.0000e+00 By=6.2401e-01 Bz=7.1632e-01 |
| return_path_pair__analytic_reference_vs_finite_width_surrogate | 5.6302e-01 | Bx=0.0000e+00 By=6.2636e-01 Bz=4.7190e-01 |
| return_path_pair__analytic_reference_vs_missing_return_surrogate | 2.3574e-01 | Bx=0.0000e+00 By=2.1184e-01 Bz=2.6986e-01 |
| return_path_pair__analytic_reference_vs_registration_gap_surrogate | 3.3890e-01 | Bx=0.0000e+00 By=3.0706e-01 Bz=3.8575e-01 |
| return_path_pair__centerline_biot_savart_vs_deep_layer_shift_surrogate | 6.7913e-01 | Bx=0.0000e+00 By=6.3154e-01 Bz=7.2475e-01 |
| return_path_pair__centerline_biot_savart_vs_finite_width_surrogate | 3.1479e-01 | Bx=0.0000e+00 By=3.8703e-01 Bz=1.8875e-01 |
| return_path_pair__centerline_biot_savart_vs_missing_return_surrogate | 6.2264e-02 | Bx=0.0000e+00 By=5.8323e-02 Bz=6.8142e-02 |
| return_path_pair__centerline_biot_savart_vs_registration_gap_surrogate | 1.9033e-01 | Bx=0.0000e+00 By=1.7608e-01 Bz=2.1177e-01 |
| return_path_pair__deep_layer_shift_surrogate_vs_finite_width_surrogate | 1.6265e+00 | Bx=0.0000e+00 By=1.4770e+00 Bz=1.7961e+00 |
| return_path_pair__deep_layer_shift_surrogate_vs_missing_return_surrogate | 1.3133e+00 | Bx=0.0000e+00 By=1.1023e+00 Bz=1.5958e+00 |
| return_path_pair__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 1.4609e+00 | Bx=0.0000e+00 By=1.2316e+00 Bz=1.7758e+00 |
| return_path_pair__finite_width_surrogate_vs_missing_return_surrogate | 2.7692e-01 | Bx=0.0000e+00 By=3.2268e-01 Bz=1.8008e-01 |
| return_path_pair__finite_width_surrogate_vs_registration_gap_surrogate | 3.3131e-01 | Bx=0.0000e+00 By=3.6289e-01 Bz=2.7125e-01 |
| return_path_pair__missing_return_surrogate_vs_registration_gap_surrogate | 2.0718e-01 | Bx=0.0000e+00 By=1.9215e-01 Bz=2.2986e-01 |
| small_multilayer_route__analytic_reference_vs_centerline_biot_savart | 1.0461e+00 | Bx=9.3049e-01 By=1.0420e+00 Bz=1.0870e+00 |
| small_multilayer_route__analytic_reference_vs_deep_layer_shift_surrogate | 8.1041e-01 | Bx=7.3874e-01 By=8.1132e-01 Bz=8.1688e-01 |
| small_multilayer_route__analytic_reference_vs_finite_width_surrogate | 1.2318e+00 | Bx=1.6220e+00 By=1.1902e+00 Bz=1.1854e+00 |
| small_multilayer_route__analytic_reference_vs_missing_return_surrogate | 9.7188e-01 | Bx=8.7643e-01 By=9.7329e-01 Bz=9.9935e-01 |
| small_multilayer_route__analytic_reference_vs_registration_gap_surrogate | 1.0661e+00 | Bx=9.5018e-01 By=1.0557e+00 Bz=1.1144e+00 |
| small_multilayer_route__centerline_biot_savart_vs_deep_layer_shift_surrogate | 6.9774e-01 | Bx=4.0329e-01 By=6.7909e-01 Bz=7.3831e-01 |
| small_multilayer_route__centerline_biot_savart_vs_finite_width_surrogate | 2.1227e-01 | Bx=4.5239e-01 By=1.9484e-01 Bz=1.4333e-01 |
| small_multilayer_route__centerline_biot_savart_vs_missing_return_surrogate | 7.1190e-02 | Bx=6.4174e-02 By=7.1528e-02 Bz=7.2933e-02 |
| small_multilayer_route__centerline_biot_savart_vs_registration_gap_surrogate | 2.2923e-01 | Bx=1.4118e-01 By=2.4104e-01 Bz=2.3819e-01 |
| small_multilayer_route__deep_layer_shift_surrogate_vs_finite_width_surrogate | 1.6496e+00 | Bx=9.0904e-01 By=1.5410e+00 Bz=1.8728e+00 |
| small_multilayer_route__deep_layer_shift_surrogate_vs_missing_return_surrogate | 1.4341e+00 | Bx=4.8252e-01 By=1.3570e+00 Bz=1.7065e+00 |
| small_multilayer_route__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 1.6127e+00 | Bx=6.0923e-01 By=1.5378e+00 Bz=1.9076e+00 |
| small_multilayer_route__finite_width_surrogate_vs_missing_return_surrogate | 1.9792e-01 | Bx=3.5026e-01 By=1.8165e-01 Bz=1.3941e-01 |
| small_multilayer_route__finite_width_surrogate_vs_registration_gap_surrogate | 3.0818e-01 | Bx=3.7702e-01 By=3.0809e-01 Bz=2.8140e-01 |
| small_multilayer_route__missing_return_surrogate_vs_registration_gap_surrogate | 2.4923e-01 | Bx=1.6535e-01 By=2.6118e-01 Bz=2.5760e-01 |

### Spectral Gaps

See `outputs/SPECTRAL_GAP.md` for per-frequency analysis.

### Decision Instability

Cross/same error ratio: min=1.0x, median=1.0x, max=1.0x across 30 operator swaps

### External Validation Status

blocked

## Cannot Claim

- COMSOL/FastHenry/FEM validation unless real external artifacts are loaded
- PyPEEC is ground-truth real physics
- Generated operator agreement proves real CAD/GDS or real QDM/NV validation
- Inverse decisions transfer to real hardware

## Boundary

This package quantifies operator gaps among implemented/generated operators.
External solver validation is blocked — no COMSOL/FastHenry artifacts loaded.
All PyPEEC results are generated-domain evidence.
