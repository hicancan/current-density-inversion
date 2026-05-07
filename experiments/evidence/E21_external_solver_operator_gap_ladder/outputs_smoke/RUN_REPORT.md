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
- multibasis_same_operator_accuracy_ge_0_60: PASS — multibasis evidence scorer same-op accuracy >= 0.60
- multibasis_cross_operator_drop_ge_0_20: PASS — multibasis cross-operator accuracy drop >= 0.20
- operator_shift_less_than_half_margin: FAIL — operator shift radius < 0.5 * interclass delta min
- margin_refusal_wrong_accept_rate_le_0_10: FAIL — margin refusal wrong-accept rate <= 0.10
- margin_refusal_accepted_accuracy_ge_0_80: FAIL — margin refusal accepted accuracy >= 0.80
- external_solver_used_in_metrics: FAIL — external solver contributes to any metric

## Key Metrics

- case_count: 5
- available_operator_count: 6
- external_solver_artifacts_present: False
- unit_sanity_passed: True

### Operator Gap Table

| Pair | Rel RMSE | Per-Component |
|---|---|---|
| straight_wire__analytic_reference_vs_centerline_biot_savart | 4.2996e-01 | Bx=0.0000e+00 By=3.9423e-01 Bz=5.0712e-01 |
| straight_wire__analytic_reference_vs_deep_layer_shift_surrogate | 2.8054e-01 | Bx=0.0000e+00 By=2.7510e-01 Bz=2.9100e-01 |
| straight_wire__analytic_reference_vs_finite_width_surrogate | 8.1804e-01 | Bx=0.0000e+00 By=8.6210e-01 Bz=7.3127e-01 |
| straight_wire__analytic_reference_vs_missing_return_surrogate | 3.7781e-01 | Bx=0.0000e+00 By=3.4969e-01 Bz=4.3778e-01 |
| straight_wire__analytic_reference_vs_registration_gap_surrogate | 4.5211e-01 | Bx=0.0000e+00 By=4.1490e-01 Bz=5.3261e-01 |
| straight_wire__centerline_biot_savart_vs_deep_layer_shift_surrogate | 3.0030e-01 | Bx=0.0000e+00 By=2.7552e-01 Bz=3.4410e-01 |
| straight_wire__centerline_biot_savart_vs_finite_width_surrogate | 3.1762e-01 | Bx=0.0000e+00 By=3.7524e-01 Bz=1.6842e-01 |
| straight_wire__centerline_biot_savart_vs_missing_return_surrogate | 4.7404e-02 | Bx=0.0000e+00 By=4.3772e-02 Bz=5.5127e-02 |
| straight_wire__centerline_biot_savart_vs_registration_gap_surrogate | 1.1105e-01 | Bx=0.0000e+00 By=1.0355e-01 Bz=1.2761e-01 |
| straight_wire__deep_layer_shift_surrogate_vs_finite_width_surrogate | 7.1717e-01 | Bx=0.0000e+00 By=7.4017e-01 Bz=6.7338e-01 |
| straight_wire__deep_layer_shift_surrogate_vs_missing_return_surrogate | 3.4394e-01 | Bx=0.0000e+00 By=3.0477e-01 Bz=4.2314e-01 |
| straight_wire__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 4.3429e-01 | Bx=0.0000e+00 By=3.8678e-01 Bz=5.3333e-01 |
| straight_wire__finite_width_surrogate_vs_missing_return_surrogate | 2.7377e-01 | Bx=0.0000e+00 By=3.0369e-01 Bz=1.8341e-01 |
| straight_wire__finite_width_surrogate_vs_registration_gap_surrogate | 2.7104e-01 | Bx=0.0000e+00 By=2.9746e-01 Bz=1.9119e-01 |
| straight_wire__missing_return_surrogate_vs_registration_gap_surrogate | 1.2618e-01 | Bx=0.0000e+00 By=1.1731e-01 Bz=1.4570e-01 |
| wire_loop__analytic_reference_vs_centerline_biot_savart | 4.0103e+00 | Bx=3.3793e+00 By=3.3793e+00 Bz=4.5409e+00 |
| wire_loop__analytic_reference_vs_deep_layer_shift_surrogate | 2.3458e+00 | Bx=1.8891e+00 By=1.8891e+00 Bz=2.7271e+00 |
| wire_loop__analytic_reference_vs_finite_width_surrogate | 4.3449e+00 | Bx=3.6081e+00 By=3.6081e+00 Bz=4.9829e+00 |
| wire_loop__analytic_reference_vs_missing_return_surrogate | 3.6984e+00 | Bx=3.0962e+00 By=3.0962e+00 Bz=4.2052e+00 |
| wire_loop__analytic_reference_vs_registration_gap_surrogate | 4.0353e+00 | Bx=3.4236e+00 By=3.4009e+00 Bz=4.5586e+00 |
| wire_loop__centerline_biot_savart_vs_deep_layer_shift_surrogate | 3.9401e-01 | Bx=3.9474e-01 By=3.9474e-01 Bz=3.9328e-01 |
| wire_loop__centerline_biot_savart_vs_finite_width_surrogate | 1.2583e-01 | Bx=9.4523e-02 By=9.4523e-02 Bz=1.5111e-01 |
| wire_loop__centerline_biot_savart_vs_missing_return_surrogate | 6.9586e-02 | Bx=7.0319e-02 By=7.0319e-02 Bz=6.8861e-02 |
| wire_loop__centerline_biot_savart_vs_registration_gap_surrogate | 2.3806e-01 | Bx=2.7113e-01 By=1.9900e-01 Bz=2.3835e-01 |
| wire_loop__deep_layer_shift_surrogate_vs_finite_width_surrogate | 6.8020e-01 | Bx=6.7463e-01 By=6.7463e-01 Bz=6.8581e-01 |
| wire_loop__deep_layer_shift_surrogate_vs_missing_return_surrogate | 5.1386e-01 | Bx=5.1740e-01 By=5.1740e-01 Bz=5.1037e-01 |
| wire_loop__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 7.0071e-01 | Bx=7.2851e-01 By=6.8405e-01 Bz=6.9496e-01 |
| wire_loop__finite_width_surrogate_vs_missing_return_surrogate | 1.4331e-01 | Bx=1.2340e-01 By=1.2340e-01 Bz=1.6043e-01 |
| wire_loop__finite_width_surrogate_vs_registration_gap_surrogate | 2.6761e-01 | Bx=2.8657e-01 By=2.1971e-01 Bz=2.7903e-01 |
| wire_loop__missing_return_surrogate_vs_registration_gap_surrogate | 2.5949e-01 | Bx=2.9324e-01 By=2.2121e-01 Bz=2.5930e-01 |
| via_vertical_segment__analytic_reference_vs_centerline_biot_savart | 9.6900e-05 | Bx=9.6900e-05 By=9.6900e-05 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_deep_layer_shift_surrogate | 4.9008e-01 | Bx=4.9008e-01 By=4.9008e-01 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_finite_width_surrogate | 9.6100e-02 | Bx=9.6100e-02 By=9.6100e-02 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_missing_return_surrogate | 9.6100e-02 | Bx=9.6100e-02 By=9.6100e-02 Bz=0.0000e+00 |
| via_vertical_segment__analytic_reference_vs_registration_gap_surrogate | 2.5745e-01 | Bx=2.1469e-01 By=2.9414e-01 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_deep_layer_shift_surrogate | 4.9014e-01 | Bx=4.9014e-01 By=4.9014e-01 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_finite_width_surrogate | 9.6179e-02 | Bx=9.6179e-02 By=9.6179e-02 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_missing_return_surrogate | 9.6179e-02 | Bx=9.6179e-02 By=9.6179e-02 Bz=0.0000e+00 |
| via_vertical_segment__centerline_biot_savart_vs_registration_gap_surrogate | 2.5743e-01 | Bx=2.1467e-01 By=2.9412e-01 Bz=0.0000e+00 |
| via_vertical_segment__deep_layer_shift_surrogate_vs_finite_width_surrogate | 6.7719e-01 | Bx=6.7719e-01 By=6.7719e-01 Bz=0.0000e+00 |
| via_vertical_segment__deep_layer_shift_surrogate_vs_missing_return_surrogate | 6.7719e-01 | Bx=6.7719e-01 By=6.7719e-01 Bz=0.0000e+00 |
| via_vertical_segment__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 9.3214e-01 | Bx=9.0535e-01 By=9.5823e-01 Bz=0.0000e+00 |
| via_vertical_segment__finite_width_surrogate_vs_missing_return_surrogate | 0.0000e+00 | Bx=0.0000e+00 By=0.0000e+00 Bz=0.0000e+00 |
| via_vertical_segment__finite_width_surrogate_vs_registration_gap_surrogate | 2.9741e-01 | Bx=2.5485e-01 By=3.3469e-01 Bz=0.0000e+00 |
| via_vertical_segment__missing_return_surrogate_vs_registration_gap_surrogate | 2.9741e-01 | Bx=2.5485e-01 By=3.3469e-01 Bz=0.0000e+00 |
| finite_width_trace__analytic_reference_vs_centerline_biot_savart | 4.3138e-01 | Bx=0.0000e+00 By=3.9535e-01 Bz=5.1028e-01 |
| finite_width_trace__analytic_reference_vs_deep_layer_shift_surrogate | 2.7400e-01 | Bx=0.0000e+00 By=2.6961e-01 Bz=2.8265e-01 |
| finite_width_trace__analytic_reference_vs_finite_width_surrogate | 8.2565e-01 | Bx=0.0000e+00 By=8.6905e-01 Bz=7.3909e-01 |
| finite_width_trace__analytic_reference_vs_missing_return_surrogate | 3.7935e-01 | Bx=0.0000e+00 By=3.5088e-01 Bz=4.4089e-01 |
| finite_width_trace__analytic_reference_vs_registration_gap_surrogate | 4.5297e-01 | Bx=0.0000e+00 By=4.1553e-01 Bz=5.3509e-01 |
| finite_width_trace__centerline_biot_savart_vs_deep_layer_shift_surrogate | 2.9251e-01 | Bx=0.0000e+00 By=2.6836e-01 Bz=3.3595e-01 |
| finite_width_trace__centerline_biot_savart_vs_finite_width_surrogate | 3.2101e-01 | Bx=0.0000e+00 By=3.7847e-01 Bz=1.7036e-01 |
| finite_width_trace__centerline_biot_savart_vs_missing_return_surrogate | 4.6954e-02 | Bx=0.0000e+00 By=4.3361e-02 Bz=5.4705e-02 |
| finite_width_trace__centerline_biot_savart_vs_registration_gap_surrogate | 1.0910e-01 | Bx=0.0000e+00 By=1.0190e-01 Bz=1.2525e-01 |
| finite_width_trace__deep_layer_shift_surrogate_vs_finite_width_surrogate | 7.1172e-01 | Bx=0.0000e+00 By=7.3645e-01 Bz=6.6377e-01 |
| finite_width_trace__deep_layer_shift_surrogate_vs_missing_return_surrogate | 3.3155e-01 | Bx=0.0000e+00 By=2.9408e-01 Bz=4.0847e-01 |
| finite_width_trace__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 4.2063e-01 | Bx=0.0000e+00 By=3.7508e-01 Bz=5.1707e-01 |
| finite_width_trace__finite_width_surrogate_vs_missing_return_surrogate | 2.7559e-01 | Bx=0.0000e+00 By=3.0518e-01 Bz=1.8497e-01 |
| finite_width_trace__finite_width_surrogate_vs_registration_gap_surrogate | 2.7164e-01 | Bx=0.0000e+00 By=2.9806e-01 Bz=1.9036e-01 |
| finite_width_trace__missing_return_surrogate_vs_registration_gap_surrogate | 1.2410e-01 | Bx=0.0000e+00 By=1.1554e-01 Bz=1.4326e-01 |
| return_path_pair__analytic_reference_vs_centerline_biot_savart | 3.8103e-01 | Bx=0.0000e+00 By=3.5765e-01 Bz=4.2539e-01 |
| return_path_pair__analytic_reference_vs_deep_layer_shift_surrogate | 5.1318e-01 | Bx=0.0000e+00 By=4.8042e-01 Bz=5.5656e-01 |
| return_path_pair__analytic_reference_vs_finite_width_surrogate | 6.7210e-01 | Bx=0.0000e+00 By=7.4226e-01 Bz=5.5028e-01 |
| return_path_pair__analytic_reference_vs_missing_return_surrogate | 3.3122e-01 | Bx=0.0000e+00 By=3.1398e-01 Bz=3.6351e-01 |
| return_path_pair__analytic_reference_vs_registration_gap_surrogate | 4.2981e-01 | Bx=0.0000e+00 By=4.0053e-01 Bz=4.8501e-01 |
| return_path_pair__centerline_biot_savart_vs_deep_layer_shift_surrogate | 5.3243e-01 | Bx=0.0000e+00 By=4.9368e-01 Bz=5.8323e-01 |
| return_path_pair__centerline_biot_savart_vs_finite_width_surrogate | 2.7974e-01 | Bx=0.0000e+00 By=3.4172e-01 Bz=1.4301e-01 |
| return_path_pair__centerline_biot_savart_vs_missing_return_surrogate | 5.7039e-02 | Bx=0.0000e+00 By=5.3041e-02 Bz=6.4351e-02 |
| return_path_pair__centerline_biot_savart_vs_registration_gap_surrogate | 1.6802e-01 | Bx=0.0000e+00 By=1.5388e-01 Bz=1.9412e-01 |
| return_path_pair__deep_layer_shift_surrogate_vs_finite_width_surrogate | 1.1101e+00 | Bx=0.0000e+00 By=1.0649e+00 Bz=1.1747e+00 |
| return_path_pair__deep_layer_shift_surrogate_vs_missing_return_surrogate | 8.3170e-01 | Bx=0.0000e+00 By=7.1975e-01 Bz=1.0208e+00 |
| return_path_pair__deep_layer_shift_surrogate_vs_registration_gap_surrogate | 9.5820e-01 | Bx=0.0000e+00 By=8.3162e-01 Bz=1.1784e+00 |
| return_path_pair__finite_width_surrogate_vs_missing_return_surrogate | 2.5328e-01 | Bx=0.0000e+00 By=2.9110e-01 Bz=1.5037e-01 |
| return_path_pair__finite_width_surrogate_vs_registration_gap_surrogate | 2.8526e-01 | Bx=0.0000e+00 By=3.1100e-01 Bz=2.2249e-01 |
| return_path_pair__missing_return_surrogate_vs_registration_gap_surrogate | 1.8448e-01 | Bx=0.0000e+00 By=1.6935e-01 Bz=2.1250e-01 |

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
