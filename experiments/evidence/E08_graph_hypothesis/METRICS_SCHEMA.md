# Metrics Schema

`outputs/metrics.json` contains:

- `selected_complexity_penalty`: validation-selected graph hypothesis complexity penalty.
- `selected_thresholds`: validation-selected thresholds for graph/raw/residual via detectors.
- `dataset`: case counts by split and class.
- `hypothesis_identification.{split}`:
  - `accuracy`: 4-way H0/H1/H2/H3 accuracy.
  - `per_class_accuracy`: accuracy by hypothesis.
  - `confusion_matrix`: rows true, columns predicted.
  - `selective_risk`: high-confidence subset accuracy.
  - `median_best_residual_rel_l2`: median residual of chosen hypothesis.
- `via_detection.{method}.{split}`:
  - `auc`, `precision`, `recall`, `f1`, `false_positive_rate`, `threshold`.
- `acceptance_gates`: scientific pass/fail gates.
- `pypeec_graph_bridge`: P0 bridge summary for exp07 centerline and real
  PyPEEC fields converted to approximate graph records.
- `pypeec_graph_bridge.model_selection_calibration_rows`: fixed-objective
  audit rows for PyPEEC basis/evidence trade-offs. These rows do not select or
  tune PyPEEC predictions.
- `pypeec_graph_bridge.pypeec_heldout_model_selection_rows`: deterministic
  calibration/held-out pilot rows on the current PyPEEC mini distribution.
- `pypeec_graph_bridge.h0_h1_tradeoff_rows`: H0/no-via safety and H1/true-via
  recall trade-off rows on held-out PyPEEC cases.
- `pypeec_graph_bridge.pypeec_model_selection_stability_rows`: repeated
  stratified split stability rows for PyPEEC model-selection ranking.
- `pypeec_graph_bridge.pypeec_class_specific_selective_rows`: repeated
  stratified split audit for class-specific margin refusal. This reports the
  trusted-output region, H0 false-any rate, and true-via acceptance separately
  so no-via safety cannot hide recall collapse.
- `pypeec_graph_bridge.pypeec_stacked_evidence_calibrator_rows`: explicit
  PyPEEC calibration/held-out ridge evidence-fusion rows. These use calibration
  folds to learn how to combine all frozen basis/evidence scores and report
  held-out H0/H1/H2/H3 performance; they are not frozen no-calibration claims.
- `pypeec_graph_bridge.pypeec_stacked_evidence_group_heldout_rows`: P0
  group-heldout stress rows for the stacked calibrator.
- `pypeec_graph_bridge.stacked_evidence_feature_ablation_rows`: P1 feature
  ablation rows for scores, one-hot decisions, margins/residuals, and basis
  families.
- `pypeec_graph_bridge.stacked_evidence_unknown_safety_rows`: P2 unknown/
  hidden-mechanism safety rows for confidence-gated stacked calibration.
- `pypeec_graph_bridge.pypeec_stacked_evidence_external_stress_rows`: P3
  operator/external stress rows for `B_finite`, `B_centerline`, and hidden
  mechanisms.
- `pypeec_graph_bridge.stacked_evidence_selective_risk_rows`: P4 risk/
  coverage rows for stacked evidence confidence refusal.
- `pypeec_graph_bridge.pypeec_distribution_gap_rows`: current unique PyPEEC
  case counts versus target H0/H1/H2/H3 model-selection distribution sizes.
  In the current full bridge run these targets are met at 100 cases per
  hypothesis, but the table remains the audit artifact for future changes.
- `h0_hard_negative`: P1 H0/no-via hard-negative rows across PyPEEC,
  clean OOD, and hidden no-via stress.
- `hidden_mechanism_stress`: P1 OOD stress where true field components are
  deliberately missing or mismatched in the hypothesis library.
  - `unknown_safety_benchmark`: fixed clean-false-reject safety status for
    unknown/OOD signals.
  - `unknown_accepted_hidden_risk`: accepted-hidden risk endpoint for each
    unknown/OOD signal.
  - `unknown_physical_evidence_ablation`: entropy, residual-gap, H0/H1
    ambiguity, and residual-vs-score disagreement signals.
- `registration_search`: P0-next/P1-next fixed via-offset grid and
  validation-selected marginalized H1/H0 threshold.
- `global_registration`: P1 fixed global translation/rotation/scale search
  grid and validation-selected global-registration H1/H0 threshold.
- `multistate_identification`: P3 synthetic two-state joint-scoring diagnostic.
- `registration_stress_curve`: P5 synthetic graph-to-field registration,
  standoff, and tilt sensitivity rows.

Primary human-readable artifacts:

- `HYPOTHESIS_IDENTIFICATION_TABLE.md`: split-level 4-way accuracy, residual,
  and selective accuracy summary.
- `HYPOTHESIS_PER_CLASS_TABLE.md`: per-split accuracy for `H0_sheet_only`,
  `H1_sheet_via`, `H2_sheet_return`, and `H3_sheet_artifact`.
- `VIA_HYPOTHESIS_TEST_TABLE.md`: via/no-via binary comparison for raw
  template, sheet-residual template, and graph H1/H0 evidence.
- `SELECTIVE_RISK_TABLE.md`: risk/coverage rows for refusal-style reporting.
- `FAILURE_CASES_TABLE.md`: misclassified cases with true/predicted
  hypothesis, confidence margin, and baseline scores.
- `PYPEEC_GRAPH_BRIDGE_TABLE.md`: graph scorer on exp07 `B_centerline` versus
  `B_pypeec`; this tests solver/operator gap, not real CAD import.
- `PYPEEC_GRAPH_BRIDGE_FAILURE_CASES.md`: misclassified exp07 PyPEEC bridge
  cases.
- `PYPEEC_AWARE_BASIS_TABLE.md`: fixed PyPEEC-aware basis-bank variants
  (finite-width sheet, return bank, artifact bank, distributed via, combined)
  on centerline and PyPEEC fields.
- `MODEL_EVIDENCE_SELECTION_TABLE.md`: residual-only, default, parameter-count,
  extra-count, BIC-like, and H0-conservative evidence rules on bridge rows.
- `PYPEEC_MODEL_BANK_EVIDENCE_TABLE.md`: PyPEEC-only view of basis/evidence
  combinations for disciplined model-bank audit.
- `MODEL_SELECTION_CALIBRATION_TABLE.md`: fixed audit objective ranking of
  PyPEEC basis/evidence combinations across accuracy, H0 protection, H1
  recall, false explanations, and parameter count.
- `PYPEEC_MODEL_BANK_ALLOWED_BASIS_TABLE.md`: explicit allowed/restricted basis
  discipline for H0/H1/H2/H3/refusal explanations.
- `PYPEEC_HELDOUT_SPLIT_TABLE.md`: deterministic pilot split of PyPEEC mini
  cases into calibration and held-out subsets.
- `PYPEEC_HELDOUT_MODEL_SELECTION_TABLE.md`: calibration-ranked model-selection
  rows with held-out PyPEEC metrics.
- `H0_H1_MODEL_SELECTION_TRADEOFF_TABLE.md`: held-out H0/H1 endpoint table that
  reports no-via safety and true-via recall together.
- `PYPEEC_MODEL_SELECTION_STABILITY_TABLE.md`: repeated-split model-selection
  stability table with top-1 frequency, held-out means, standard deviations,
  and empirical confidence intervals.
- `PYPEEC_CLASS_SPECIFIC_SELECTIVE_TABLE.md`: class-specific selective
  hypothesis audit. Thresholds are selected only on calibration folds and
  evaluated on repeated held-out PyPEEC folds; the purpose is to quantify the
  H0-safety/H1-acceptance bottleneck rather than claim a solved detector.
- `PYPEEC_STACKED_EVIDENCE_CALIBRATOR_TABLE.md`: stacked evidence calibrator
  rows for PyPEEC calibration/held-out splits. A simple ridge one-vs-rest model
  learns from calibration folds how to fuse all basis/evidence scores and is
  evaluated on held-out folds.
- `PYPEEC_STACKED_EVIDENCE_GROUP_HELDOUT_TABLE.md`: P0 group-heldout stress for
  the stacked calibrator, including variant-mod folds and family leaveout.
- `PYPEEC_STACKED_EVIDENCE_GROUP_DISTANCE_REFUSAL_TABLE.md`: family-heldout
  feature-distance refusal audit, reporting raw accuracy, rejection rate, and
  accepted risk for unseen groups.
- `PYPEEC_FAMILY_FEWSHOT_ADAPTATION_TABLE.md`: generated-family few-shot
  calibration audit for 0/2/5/10 samples from each held-out family.
- `STACKED_EVIDENCE_FEATURE_ABLATION_TABLE.md`: P1 feature ablation for the
  stacked calibrator.
- `STACKED_EVIDENCE_UNKNOWN_SAFETY_TABLE.md`: P2 confidence-margin,
  feature-distance, and combined hidden/unknown safety table.
- `STACKED_EVIDENCE_NEAR_BOUNDARY_HIDDEN_TABLE.md`: harder near-manifold hidden
  stress evaluated with the same OOD screens.
- `STACKED_EVIDENCE_NEAR_HIDDEN_SEVERITY_TABLE.md`: near-boundary hidden
  severity sweep, reporting rejection and accepted risk versus perturbation
  strength.
- `NEAR_HIDDEN_ACCEPTED_CASES.md`: accepted near-hidden case audit separating
  primary-label correctness from mechanism-level explanation.
- `STACKED_EVIDENCE_SPACE_DIAGNOSTICS_TABLE.md`: feature-distance and PCA-space
  summary for in-library PyPEEC, base hidden, and near-boundary hidden evidence
  vectors.
- `stacked_evidence_space_pca.png`: explanatory PCA scatter plot for the same
  evidence vectors. It is not used for threshold selection.
- `PYPEEC_STACKED_EVIDENCE_EXTERNAL_STRESS_TABLE.md`: P3 operator/external
  stress table.
- `STACKED_EVIDENCE_SELECTIVE_RISK_TABLE.md`: P4 stacked evidence
  risk-coverage/refusal table.
- `PYPEEC_DISTRIBUTION_GAP_TABLE.md`: explicit PyPEEC case-count coverage
  against target H0/H1/H2/H3 sample sizes for non-pilot model selection.
- `H0_HARD_NEGATIVE_TABLE.md`: H0/no-via hard-negative classification and
  false H1/H2/H3 over-explanation rates.
- `PYPEEC_BRIDGE_REGISTRATION_TABLE.md`: exp07 bridge before/after fixed
  via-location marginalization.
- `PYPEEC_BRIDGE_GLOBAL_REGISTRATION_TABLE.md`: exp07 bridge before/after
  fixed global graph-to-field translation/rotation/scale search.
- `HIDDEN_MECHANISM_STRESS_TABLE.md`: hidden return, shifted via, mismatched
  artifact, and combined-mechanism stress.
- `HIDDEN_MECHANISM_FAILURE_CASES.md`: hidden-stress failure rows.
- `REGISTRATION_MARGINALIZATION_TABLE.md`: hidden-stress before/after
  via-location marginalization, including shifted-via recovery.
- `UNKNOWN_REJECTION_TABLE.md`: validation-thresholded unknown/out-of-library
  rejection on hidden mechanisms.
- `UNKNOWN_RISK_COVERAGE_TABLE.md`: selective risk/coverage rows for clean OOD
  and hidden-mechanism stress.
- `UNKNOWN_DETECTOR_ABLATION_TABLE.md`: unknown/OOD signals compared at a fixed
  clean false-reject target.
- `UNKNOWN_SAFETY_BENCHMARK.md`: labels each unknown/OOD signal as usable,
  diagnostic-only, or violating the clean false-reject budget.
- `UNKNOWN_ACCEPTED_HIDDEN_RISK_TABLE.md`: focuses on hidden mechanisms that
  remain accepted after rejection and reports their residual risk.
- `UNKNOWN_PHYSICAL_EVIDENCE_ABLATION_TABLE.md`: physical-evidence unknown/OOD
  signals at the same clean false-reject target.
- `MULTISTATE_IDENTIFICATION_TABLE.md`: single-state versus synthetic two-state
  joint hypothesis scoring.
- `MULTISTATE_DESIGN_TABLE.md`: synthetic second-excitation policy scan.
- `MULTISTATE_EXPERIMENTAL_DESIGN_TABLE.md`: label-free margin/residual utility
  ranking for synthetic second-excitation policies.
- `ACTIVE_DESIGN_OBJECTIVE_TABLE.md`: active-design objective audit with
  additional objective-named synthetic policies.
- `ACTIVE_DESIGN_CONSTRAINT_TABLE.md`: first-order synthetic feasibility
  constraints for active-design policies.
- `REGISTRATION_STRESS_CURVE.md`: translation/rotation/scale/standoff/tilt
  stress curve with and without global registration search.

Important gates:

- `graph_test_accuracy_is_high`: test 4-way accuracy remains high, not only
  above random.
- `graph_ood_accuracy_is_material`: OOD 4-way accuracy stays materially above
  random under geometry/noise/current shifts.
- `graph_ood_no_via_accuracy_is_material`: no-via OOD cases are not mostly
  hallucinated into via/return/artifact.
- `graph_ood_true_via_accuracy_is_material`: true-via OOD recall does not
  collapse.
- `graph_ood_return_path_accuracy_is_material`: return-path OOD cases are
  recognized as return-current explanations rather than forced via.
- `graph_ood_auc_not_worse_than_residual_template`: graph evidence must beat or
  match the stronger residual-template baseline, not only the weak raw
  template.
- `graph_ood_no_via_fp_below_residual_template`: graph evidence must not buy
  recall by increasing OOD no-via false positives.
- `pypeec_centerline_bridge_accuracy_is_high`: approximate exp07 graph
  conversion should be internally consistent on centerline fields.
- `pypeec_bridge_exposes_solver_gap`: PyPEEC fields should be materially harder
  than centerline fields, otherwise P0 would not test the solver gap.
- `pypeec_bridge_via_auc_is_material`: H1/H0 evidence should remain informative
  on real PyPEEC fields even when 4-way accuracy drops.
- `hidden_mechanism_is_nontrivial`: hidden-mechanism stress must not be a
  polished easy duplicate of the base dataset.
- `via_location_marginalization_is_evaluated`: P0-next registration search
  artifacts exist.
- `via_location_marginalization_improves_shifted_via`: fixed offset
  marginalization must improve or at least not worsen shifted-via identification.
- `pypeec_aware_basis_bank_is_evaluated`: P0 PyPEEC-aware graph basis variants
  are explicitly evaluated rather than assumed.
- `pypeec_aware_basis_residual_not_worse_than_base`: the combined PyPEEC-aware
  basis bank must not worsen the PyPEEC median best residual, even if its
  hypothesis classification trade-off is unfavorable.
- `model_selection_calibration_is_evaluated`: the fixed PyPEEC model-selection
  audit table is present and nonempty.
- `pypeec_heldout_model_selection_is_evaluated`: deterministic calibration and
  held-out PyPEEC model-selection rows are present.
- `h0_h1_tradeoff_curve_is_evaluated`: H0/H1 held-out trade-off rows are
  present.
- `pypeec_model_selection_stability_is_evaluated`: repeated stratified
  PyPEEC split stability rows are present.
- `pypeec_class_specific_selective_is_evaluated`: class-specific selective
  PyPEEC audit rows are present.
- `pypeec_stacked_evidence_calibrator_is_evaluated`: PyPEEC calibration/
  held-out stacked evidence rows are present.
- `pypeec_stacked_group_heldout_is_evaluated`: group-heldout stacked evidence
  rows are present.
- `pypeec_stacked_group_distance_refusal_is_evaluated`: family/variant heldout
  feature-distance refusal rows are present.
- `pypeec_family_fewshot_adaptation_is_evaluated`: few-shot generated-family
  adaptation rows are present.
- `stacked_evidence_feature_ablation_is_evaluated`: feature ablation rows are
  present.
- `stacked_evidence_unknown_safety_is_evaluated`: confidence-, feature-distance-,
  and combined hidden/unknown safety rows are present.
- `stacked_evidence_distance_ood_is_evaluated`: feature-distance OOD rejection
  over the calibrated stacked-evidence manifold is included in the unknown
  safety table.
- `stacked_evidence_near_boundary_hidden_is_evaluated`: near-boundary hidden
  stress rows are present.
- `stacked_evidence_near_hidden_severity_is_evaluated`: near-hidden severity
  sweep rows are present.
- `near_hidden_accepted_cases_are_audited`: accepted near-hidden case rows are
  present.
- `stacked_evidence_space_diagnostics_are_evaluated`: evidence-space table and
  PCA figure are present.
- `pypeec_stacked_external_stress_is_evaluated`: external/operator stress rows
  are present.
- `stacked_evidence_selective_risk_is_evaluated`: risk-coverage rows are
  present.
- `pypeec_distribution_gap_is_evaluated`: current PyPEEC distribution size is
  explicitly reported against target counts, even when all targets are met.
- `disciplined_model_bank_is_documented`: the allowed-basis discipline table is
  present.
- `h0_hard_negatives_are_evaluated`: no-via hard-negative rows must be reported.
- `global_registration_search_is_evaluated`: P1 global graph-to-field
  registration is evaluated separately from local via marginalization.
- `unknown_rejection_catches_hidden_mechanisms`: clean-validation rejection
  thresholds must flag most hidden/out-of-library cases.
- `unknown_risk_coverage_is_evaluated`: hidden/clean selective-risk rows are
  reported so rejection is not reduced to one conservative operating point.
- `unknown_detector_ablation_is_evaluated`: multiple unknown-score signals are
  compared at a fixed clean false-reject target.
- `unknown_safety_benchmark_is_evaluated`: unknown-score signals are judged
  against a clean false-reject budget and accepted-case accuracy.
- `unknown_accepted_hidden_risk_is_evaluated`: accepted hidden mechanisms are
  audited as a primary risk endpoint.
- `unknown_physical_evidence_ablation_is_evaluated`: physical evidence signals
  are included in unknown/OOD ablation.
- `multistate_joint_not_worse_than_single`: joint synthetic excitation scoring
  must not degrade OOD hypothesis identification.
- `multistate_design_scan_is_evaluated`: more than one second-excitation policy
  is evaluated.
- `multistate_label_free_design_is_evaluated`: P3 reports a label-free
  margin/residual design utility in addition to label accuracy.
- `active_design_objective_is_evaluated`: P4 active-design objective table is
  present.
- `active_design_constraints_are_evaluated`: active-design policies are
  screened by first-order synthetic feasibility constraints.
- `registration_stress_curve_is_evaluated`: P5 synthetic registration stress
  curve is present.
- `registration_standoff_tilt_stress_is_evaluated`: standoff and tilt stress
  rows are present, so sensor-height nuisance is not collapsed into xy
  registration.
