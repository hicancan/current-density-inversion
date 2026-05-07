# Round 4 Operator Gap Gate Audit

Breakthrough gates for ridge evidence scorer and margin refusal.

| Gate | Result | Value | Threshold |
|---|---:|---:|---:|
| package_runs_to_completion | PASS | True | metrics.json written |
| all_operators_same_shape | PASS | True | all field maps have identical shape |
| operator_gaps_nonzero | PASS | True | at least one operator gap > 0 |
| decision_stress_executed | PASS | True | at least one cross-operator decision test run |
| external_artifact_contract_written | PASS | True | EXTERNAL_ARTIFACT_CONTRACT.md exists with blocked/interface status |
| reports_written | PASS | True | all required reports present |
| no_fake_external_validation | PASS | blocked | external_validation_status is blocked when artifacts missing |
| generated_domain_boundary_explicit | PASS | True | PyPEEC results marked generated-domain |
| decision_instability_ratio_gt_1_25 | PASS | 1.5 | at least one mechanism cross/same accuracy ratio > 1.25 |
| template_same_operator_accuracy_ge_0_60 | FAIL | 0.2031 | template evidence scorer same-operator accuracy >= 0.60 |
| template_cross_operator_drop_ge_0_20 | FAIL | 0 | template scorer cross-operator accuracy drop >= 0.20 |
| ridge_same_operator_accuracy_ge_0_60 | FAIL | 0.3125 | ridge evidence scorer same-operator accuracy >= 0.60 |
| ridge_cross_operator_drop_ge_0_20 | FAIL | 0.07812 | ridge scorer cross-operator accuracy drop >= 0.20 |
| ridge_wrong_accept_rate_cross_le_0_10_at_refusal | FAIL | 0.75 | ridge wrong-accept rate cross-op <= 0.10 at refusal |
| ridge_accepted_accuracy_cross_ge_0_80_at_refusal | FAIL | 0.25 | ridge accepted accuracy cross-op >= 0.80 at refusal |
| pyquant_external_solver_pipeline_completed | FAIL | False | external solver pipeline completed (PyPEEC/FastHenry/COMSOL) |
| multibasis_same_operator_accuracy_ge_0_60 | FAIL | 0.4062 | multibasis evidence scorer same-op accuracy >= 0.60 |
| multibasis_cross_operator_drop_ge_0_20 | FAIL | 0.1562 | multibasis cross-operator accuracy drop >= 0.20 |
| operator_shift_less_than_half_margin | FAIL | False | operator shift radius < 0.5 * interclass delta min |
| margin_refusal_wrong_accept_rate_le_0_10 | FAIL | 0.6094 | margin refusal wrong-accept rate <= 0.10 |
| margin_refusal_accepted_accuracy_ge_0_80 | FAIL | 0.3906 | margin refusal accepted accuracy >= 0.80 |
| external_solver_used_in_metrics | FAIL | False | external solver contributes to any metric |

