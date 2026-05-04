# Update Log

## 2026-05-03 - Initial claim graph

Claim affected:
- C01_forward_sanity
- C02_single_plane_identifiability_boundary
- C03_unet_topology_baseline_boundary
- C04_inverse_crime_and_operator_gap
- C05_pypeec_solver_bridge
- C06_graph_hypothesis_system_identification
- C07_stacked_evidence_calibration
- C08_ood_refusal_safety
- C09_fewshot_family_adaptation
- C10_pdn_kcl_distribution_need
- C11_mechanism_level_explanation
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality
- C14_unlabeled_family_adaptation

Change type:
- claim graph initialization
- evidence registration
- boundary registration

Files changed:
- research graph SSOT
- claim-scoped experiment plans
- claim-scoped output summaries
- validation and rendering scripts

Evidence:
- nine evidence packages registered from forward sanity through real-data
  intake gates.

Metrics:
- graph integrity is enforced by `scripts/validate_graph.py`.

Claim status before:
- no graph state.

Claim status after:
- claim-centered graph state initialized.

Cannot claim:
- real QDM/NV validation.
- real CAD/Gerber/GDS validation.
- deployment-safe via/no-via diagnosis.
- mechanism-level explanation for accepted hidden rows.

Next required evidence:
- implement `D08_pdn_kcl_circuit_graph` with KCL, current closure, return path,
  and held-out/few-shot protocols.

## 2026-05-03 - Runnable evidence packages

Claim affected:
- C01-C09
- C11-C13

Change type:
- runnable evidence implementation added
- no-leakage runtime commands registered
- evidence output gate check added

Files changed:
- `experiments/evidence/`
- `research_graph/experiments.yml`
- `scripts/run_evidence.py`
- `scripts/check_evidence_outputs.py`
- `tests/test_graph_integrity.py`

Evidence:
- Claim-graph evidence packages now contain runnable code, configs, tests, and
  local result artifacts.

Metrics:
- `scripts/check_evidence_outputs.py` checks registered metrics gates.
- `scripts/run_evidence.py --all --mode test --continue-on-fail` runs the
  evidence package test suites.

Claim status before:
- graph state initialized with evidence summaries only.

Claim status after:
- graph state initialized with runnable evidence packages.

Cannot claim:
- real QDM/NV validation.
- real CAD/Gerber/GDS validation.
- deployment-safe via/no-via diagnosis.

Next required evidence:
- implement and validate the PDN/KCL circuit-graph distribution.

## 2026-05-03 - Runtime verification pass

Claim affected:
- C01-C09
- C11-C13

Change type:
- runtime verification
- path repair

Files changed:
- `experiments/evidence/`
- `research_graph/experiments.yml`

Evidence:
- Evidence package unit tests pass across all registered runtime packages.
- Reproduction smoke entries were run for canonical forward, observability,
  two-layer topology, sensor observation stress, operator gap, solver quick
  bridge, graph hypothesis scoring, and real-data intake validation.

Metrics:
- All registered metrics gates pass.
- Graph hypothesis scoring reports `all_scientific_gates_passed`.

Claim status before:
- runnable evidence packages registered.

Claim status after:
- runnable evidence packages verified locally.

Cannot claim:
- real QDM/NV validation.
- full retraining of the image inverse benchmark during the smoke run.
- PDN/KCL distribution robustness.

Next required evidence:
- run the full image-inverse training package only when retraining is needed;
  current claim state uses the preserved gate artifacts and package tests.

## 2026-05-04 - Agent control layer and PDN/KCL prototype

Claim affected:
- C10_pdn_kcl_distribution_need
- C06_graph_hypothesis_system_identification
- C14_unlabeled_family_adaptation

Change type:
- agent-first architecture upgrade
- artifact registry and agent queue added
- generated PDN/KCL runnable evidence package added

Files changed:
- `research_graph/`
- `docs/`
- `scripts/`
- `src/research_ssot/`
- `experiments/evidence/E10_pdn_kcl_distribution/`
- `outputs/by_claim/C10_pdn_kcl_distribution_need/`

Evidence:
- `E10_pdn_kcl_distribution` generates small resistive PDN/KCL graphs, solves
  edge currents under KCL, checks current closure, forwards `Bxyz`, and reports
  matched generated H0/H1/H2/H3 hypothesis rows.

Metrics:
- max interior KCL residual: `7.147e-16`
- max current closure error: `3.128e-15`
- max divB proxy residual: `0.003842`
- held-out H0/H1/H2/H3 accuracy: `1.000`

Claim status before:
- `C10_pdn_kcl_distribution_need`: active, missing runnable evidence.

Claim status after:
- `C10_pdn_kcl_distribution_need`: supported_generated.

Cannot claim:
- real-board PDN/KCL robustness.
- real CAD/Gerber/GDS validation.
- external FEM/FastHenry validation.
- real QDM/NV validation.
- mechanism-level correctness under real layouts.

Next required evidence:
- expand the generated PDN/KCL distribution toward CAD/Gerber/GDS-like graph
  families and independent external-solver held-out rows.

## 2026-05-04 - Chip-like PDN and physics-learning closure

Claim affected:
- C10_pdn_kcl_distribution_need
- C06_graph_hypothesis_system_identification
- C11_mechanism_level_explanation
- C14_unlabeled_family_adaptation

Change type:
- generated chip-like multilayer PDN evidence package added
- generated physics-learning closure evidence package added
- Research Graph nodes, evidence edges, artifacts, and agent queue updated

Files changed:
- `experiments/evidence/E11_chip_like_pdn_distribution/`
- `experiments/evidence/E12_pdn_physics_learning/`
- `outputs/by_claim/C10_pdn_kcl_distribution_need/`
- `outputs/by_claim/C11_mechanism_explanation/`
- `research_graph/`

Evidence:
- `E11_chip_like_pdn_distribution` generates a four-layer artificial micro-PDN
  with top straps, intermediate meshes, lower return grid, via stacks,
  distributed loads, KCL-solved currents, current closure, divB proxy, and
  balanced generated H0/H1/H2/H3 rows.
- `E12_pdn_physics_learning` reads E11 rows and compares CPU baselines:
  residual scorer, graph-agnostic Bxyz learner, and physics-aware graph/KCL
  projection. The physics-aware branch improves predicted-current KCL and
  current closure over unconstrained current regression.

Metrics:
- E11 case count: `96`
- E11 layer count: `4`
- E11 max KCL residual: `4.913e-15`
- E11 max current closure error: `7.391e-15`
- E11 max divB proxy residual: `2.835e-03`
- E11 held-out/family-hidden hypothesis accuracy: `1.000` / `1.000`
- E12 held-out accuracy: `1.000`
- E12 family generalization gap: `0.250`
- E12 unconstrained max predicted KCL residual: `1.567e-02`
- E12 physics-aware max predicted KCL residual: `3.830e-15`
- E12 physics-aware field RMSE: `2.166e-06`

Claim status before:
- `C10_pdn_kcl_distribution_need`: supported_generated by E10 prototype.
- `C11_mechanism_level_explanation`: limited.
- `C14_unlabeled_family_adaptation`: proposed.

Claim status after:
- `C10_pdn_kcl_distribution_need`: remains supported_generated with stronger
  generated-domain support from E11/E12.
- `C11_mechanism_level_explanation`: remains limited; E12 is a boundary, not a
  mechanism audit.
- `C14_unlabeled_family_adaptation`: remains proposed; E12 is supervised, not
  unlabeled adaptation.

Cannot claim:
- real chip PDN realism.
- real CAD/Gerber/GDS validation.
- external FEM/FastHenry validation.
- real QDM/NV validation.
- mechanism-level explanation from label correctness.
- real learned physics from generated graph/KCL projection.

Next required evidence:
- import CAD/Gerber/GDS-like graph families.
- validate a small generated/CAD-like subset against independent external
  solvers.
- add mechanism labels and accepted-row mechanism audits.

## 2026-05-04 - Multi-height multi-state observability evidence

Claim affected:
- C02_single_plane_identifiability_boundary
- C06_graph_hypothesis_system_identification

Change type:
- new evidence package E13_multi_height_multistate_observability added
- observability nodes O08 (multi-height) and O09 (multi-state) status upgraded
- C02 and C06 supported_by updated with E13
- evidence edges registered (E13->C02 supports+limits, E13->C06 supports+limits)

Files changed:
- `experiments/evidence/E13_multi_height_multistate_observability/`
- `outputs/by_claim/C02_identifiability_boundary/`
- `outputs/by_claim/C06_graph_hypothesis_system_id/`
- `research_graph/`

Evidence:
- `E13_multi_height_multistate_observability` evaluates 27 configurations across
  3 heights, 3 state counts, 3 component modes, and 2 graph-prior settings on
  40 generated two-layer route/via/return cases. Effective rank is stable across
  heights (~10), multi-state excitation improves hypothesis margin, Bxyz matches
  Bz, and graph prior reduces layer misallocation (~1.4x).

Metrics:
- Case count: 40, Configurations: 27
- All 6 acceptance gates passed.
- Effective rank: stable at ~10 across heights
- Graph prior layer error reduction: ~1.4x

Claim status before:
- C02: supported by E02, E03.
- C06: supported by E08, E12.

Claim status after:
- C02: supported by E02, E03, E13.
- C06: supported by E08, E12, E13.

Cannot claim:
- arbitrary real multilayer recovery from multi-height observations
- real QDM/NV validation
- hardware-feasible active measurement
- generated-domain graph prior proves real CAD/GDS graph inference

Next required evidence:
- validate multi-height/multi-state observability with real measurement or
  external solver held-out rows.
- replace generated graph families with CAD/Gerber/GDS-derived graph candidates.

## 2026-05-04 - Agent-native full-run audit and old-experiment migration

Claim affected:
- C01_forward_sanity
- C02_single_plane_identifiability_boundary
- C03_unet_topology_baseline_boundary
- C04_inverse_crime_and_operator_gap
- C05_pypeec_solver_bridge
- C06_graph_hypothesis_system_identification
- C07_stacked_evidence_calibration
- C08_ood_refusal_safety
- C09_fewshot_family_adaptation
- C10_pdn_kcl_distribution_need
- C11_mechanism_level_explanation
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality
- C14_unlabeled_family_adaptation

Change type:
- old exp01-exp09 migration coverage audit
- evidence package contract hardening
- metrics schema/no-leakage audit hardening
- E09 real-data intake scaffold execution
- full evidence run execution
- CI and agent command layer upgrade

Files changed:
- `AGENTS.md`
- `README.md`
- `pyproject.toml`
- `Makefile`
- `.github/workflows/ci.yml`
- `.github/pull_request_template.md`
- `docs/`
- `scripts/`
- `src/research_ssot/`
- `research_graph/`
- `tests/`
- `experiments/evidence/E09_real_data_intake_gate/`
- `outputs/full_run_audit.md`
- `outputs/migration_coverage_matrix.md`

Evidence:
- `E01` through `E08` completed fresh full package runs in the all-evidence
  run sweep.
- `E07` completed the real PyPEEC API bridge, including the 400-case target
  and exp03-like mini dataset.
- `E09` now has non-empty interface-scaffold metrics and a RUN_REPORT, but no
  measured rows.
- `E10` through `E12` completed generated-domain PDN/KCL evidence runs.

Metrics:
- `scripts/check_evidence_outputs.py`: 12/12 metrics gates pass.
- `scripts/check_metrics_schema.py`: 12/12 metrics files have schema version,
  boolean gates, leakage audit, and RUN_REPORT metrics references after
  normalization.
- `scripts/check_no_leakage.py`: 12/12 metrics files pass calibration/held-out
  and hidden-row leakage checks.
- `scripts/audit_old_new_experiment_coverage.py`: migration matrix written.
- `uv run python scripts/run_evidence.py --all --mode run --continue-on-fail`:
  pass, 1703.9 s.

Claim status before:
- E04 and E08 evidence entries were partial because fresh full reruns had not
  been recorded in the new repository.
- C12 remained blocked by absence of measured QDM/NV rows.

Claim status after:
- E04 and E08 evidence entries are passed after fresh full runs.
- C12 remains blocked; E09 is passed_interface only.
- C11 remains limited; no mechanism-level correctness claim was upgraded.
- Generated-domain claims remain bounded by cannot-claim lists.

Cannot claim:
- real QDM/NV validation.
- real CAD/Gerber/GDS validation.
- COMSOL/FastHenry/FEM validation.
- PyPEEC as real ground truth.
- mechanism-level explanation from primary-label correctness.
- CI smoke/test results as full-run evidence.

Next required evidence:
- add measured simple-wire or known-via QDM/NV rows for C12.
- add imported CAD/Gerber/GDS graph families and independent external-solver
  held-out rows.
- add mechanism labels and accepted-row parameter-level audits for C11.
