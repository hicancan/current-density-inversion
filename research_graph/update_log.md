# Update Log

## 2026-05-05 - E19.2 OQCI identifiability audit

- E19.2_observable_quotient_identifiability_audit implemented as new evidence package
- Paradigm shift: from winner-take-all Bayesian posterior to OQCI consistent-set analysis
- 72 generated cases: ambiguity_rate=1.0, all 4 hypotheses consistent in every case
- Pairwise extra_distance=0 for H1/H2/H3: via/gap/return bases share subspace even beyond H0
- Effective rank=27 of 100 basis dimensions observable; 50 near-null modes
- Multi-height (3.2um+6.4um) does not reduce ambiguity or near-null count
- Engineering gates: 7/7 passed. 15/15 tests pass.
- Evidence edges added: limits C10, supports C02, limits C06
- Status: passed_with_limitations

## 2026-05-04 - E19 OBGHI minimal observable topology posterior evidence

Claim affected:
- C10_pdn_kcl_distribution_need (E19 motivates+limits)
- C06_graph_hypothesis_system_identification (E19 motivates+limits)
- C02_single_plane_identifiability_boundary (secondary claim)
- C04_inverse_crime_and_operator_gap (secondary claim)

Change type:
- new evidence package E19 added with minimal OBGHI posterior topology inference
- closed-form Gaussian Bayesian evidence for H0/H1/H2/H3 explanations
- 72 generated four-layer cases across 6 families
- operator diagnostics confirm via columns nonzero
- evidence edges registered (motivates+limits for C10 and C06)

Evidence:
- E19 implements deterministic four-layer sheet/via forward operator, graph-Hodge-inspired low-dimensional current bases, observable compression via singular-value energy filtering, closed-form Gaussian Bayesian evidence, posterior topology probabilities, via-vs-gap principal-angle ambiguity diagnostic, and accept/reject/need-next-measurement decision rule.

Metrics:
- case_count: 72 (smoke: 12)
- OBGHI top1_accuracy: 0.333 (matches ridge baseline)
- OBGHI accepted_accuracy: 0.345
- OBGHI accepted_risk: 0.655 (GATE FAILS: >0.45)
- OBGHI reject_rate: 0.0
- OBGHI need_next_measurement_rate: 0.236
- OBGHI brier_score: 0.247
- OBGHI via_gap_angle_deg: 67.8
- Ridge-map top1_accuracy: 0.333

By truth:
- H0_no_via (12 cases): top1=0.0, mean_true_posterior=0.056
- H1_via (24 cases): top1=1.0, mean_true_posterior=0.727
- H2_model_gap (24 cases): top1=0.0, mean_true_posterior=5.87e-07
- H3_return_path (12 cases): top1=0.0, mean_true_posterior=0.255

Debugging priority audit:
1. Via forward columns nonzero: PASS (min norm 0.0103)
2. H1/H2/H3 posterior differs: PARTIALLY PASS (H1 vs H3 differ; H2 collapses to zero due to gap basis/data mismatch)
3. Accept/reject/need-next decisions present: PASS (55 accept, 17 need_next, 0 reject)
4. OBGHI vs ridge baseline: PASS (both top1=0.333)
5. Failures preserved: PASS (57 failure cases documented)

Failure modes:
1. H1_via dominates H0_no_via (no-via false-positive): via basis flexibility captures no-via background fields
2. H2_model_gap posterior collapses to zero: gap basis uses Gaussian field patterns that don't match gradient/Laplacian data generation; uniform prior variance penalizes H2 relative to H0
3. H1_via dominates H3_return_path: return-path basis (4 modes) too small vs via basis

Claim status before:
- C10: supported_generated (E10, E11, E12, E14, E15, E18)
- C06: supported_generated (E08, E12, E13, E14, E15, E18)
- C02: supported (E02, E03, E13, E15, E17, E18)
- C04: supported_generated (E04, E06, E07, E16, E18)

Claim status after:
- No status change. E19 adds generated-domain evidence with explicit limitations.
  Claims remain bounded by existing cannot-claim lists.

Cannot claim:
- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real-board PDN/KCL robustness
- mechanism-level explanation on real data
- universal via detection
- that H2_model_gap is resolved
- that the via-gap ambiguity is quantified sufficiently for deployment

Next required evidence:
- replace simple Gaussian gap basis with gradient/Laplacian/registration-matched patterns
- add multi-height observation support for standoff discrimination
- add multi-state excitation support for current injection pattern discrimination
- add per-block prior variances instead of uniform per-hypothesis prior variance
- compare E19 failure slices against E18 physics-constrained inverse failure cases

Tests run:
- `uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests`: 5 passed (1.61s)
- Smoke config: passed_with_limitations (1.14s, 12 cases)
- Full default config: passed_with_limitations (20.26s, 72 cases)
- `uv run python scripts/validate_graph.py`: PASS

Files changed:
- `experiments/evidence/E19_obghi_minimal_observable_topology_posterior/`
- `research_graph/experiments.yml`
- `research_graph/evidence_edges.yml`
- `research_graph/update_log.md`

## 2026-05-04 - E18.1 physics/numerical fix for constrained inverse

Root causes fixed:
1. Via columns in A were all zeros → added vertical-current kernel
2. KCL matrix D did not couple via → added source/sink terms
3. Fixed ridge_alpha with SI-scale A caused near-zero → column-normalized solvers
4. Metrics did not distinguish methods → now b_res_rel spans 0.003–1.0
5. Leaderboard mixed runtime → separated scientific/runtime tables

Key results:
- oracle b_res_rel=0.0, zero=1.0 (sanity confirmed)
- ridge_scaled ranks #1 (b_res_rel=0.003, via_f1=0.41)
- New method matches graph_kcl_aware_scaled, KCL residual 1e-15
- New method does NOT beat ridge_scaled on b_residual or via_f1
- KCL constraint overpowers data fidelity in constrained solvers

Status: passed (all gates pass, limitations documented)
Tests: 11 unit tests pass, full run 18 cases 11 methods

## 2026-05-04 - Physics-constrained multilayer PDN inverse evidence (E18)

Claim affected:
- C10_pdn_kcl_distribution_need (+E18 in supported_by)
- C06_graph_hypothesis_system_identification (+E18 in supported_by)
- C04_inverse_crime_and_operator_gap (+E18 in supported_by)
- C02_single_plane_identifiability_boundary (+E18 in supported_by)

Change type:
- new evidence package E18 added with physics-constrained differentiable
  inverse, unified baseline leaderboard, failure case analysis

Evidence:
- E18 implements graph_kcl_differentiable_inverse: warm-started constrained
  ridge + L-BFGS-B composite loss + KCL post-projection vs 4 baselines
  on 18 cases, 6 families, 11 channels.

Metrics:
- KCL residual: 2.4e-19 (new) vs 1.6e-13 (ridge)
- Layer misallocation: 0.213 (new) ≈ 0.213 (graph_kcl_aware)
- 4 failure cases: dense-via recall=0, deep-layer >0.3, return-grid, KCL-RMSE tradeoff
- All acceptance gates pass

Tests run:
- tests: PASS (13 tests, 0.52s)
- Full run: PASS (14.1s, all gates passed)

## 2026-05-04 - Next-stage current inversion breakthrough evidence integration

Claim affected:
- C02_single_plane_identifiability_boundary (+E13, +E15, +E17 in supported_by)
- C06_graph_hypothesis_system_identification (+E13, +E14, +E15 in supported_by)
- C10_pdn_kcl_distribution_need (+E14, +E15 in supported_by)
- C04_inverse_crime_and_operator_gap (+E16 in supported_by via experiments)
- C03_unet_topology_baseline_boundary (E16 motivates, E17 motivates)
- D09_cad_gerber_gds_like (missing → partial via E14)

Change type:
- 5 new evidence packages integrated: E13, E14, E15, E16, E17
- Safe integration protocol: branch diff audit, clean cherry-pick where contaminated,
  merge conflict resolution, research graph entry accumulation
- O08_multi_height and O09_multi_state_excitation status upgraded (proposed/partial → implemented)

Evidence added:
- E13: Multi-height multi-state observability (27 configs, 40 cases)
- E14: Layout graph import scaffold (4 example layouts)
- E15: Four-layer via-chain benchmark (18 cases, 6 stress families, 4 baselines)
- E16: Differentiable Biot-Savart forward layer (sheet + via forward, 6 acceptance gates)
- E17: L1-curl divergence-free baseline (144 runs, 4 baselines, 7 acceptance gates)

Metrics:
- E13: effective rank ~10.1, multi-state margin gain 1.24x, graph prior layer error reduction 1.4x
- E14: 4 examples validated, all 4 generate H0/H1/H2/H3 candidates
- E15: 18 cases, 4 layers, 11 output channels, all 8 acceptance gates pass
- E16: 10/10 unit tests pass (1 skipped: torch not installed), all 6 gates pass
- E17: Fourier divergence residual 3e-12, Tikhonov current RMSE 1.45, all 7 gates pass

Claim status before:
- C02: supported (E02, E03 only)
- C06: supported_generated (E08, E12 only)
- C10: supported_generated (E10, E11, E12 only)
- D09: missing

Claim status after:
- C02: supported (E02, E03, E13, E15, E17) — strengthened with multi-height, via-chain, and regularization evidence
- C06: supported_generated (E08, E12, E13, E14, E15) — strengthened with multi-state, layout scaffold, and via-chain evidence
- C10: supported_generated (E10, E11, E12, E14, E15) — strengthened with layout import scaffold and via-chain benchmark
- C04: supported_generated — E16 strengthens generated-domain operator gap evidence
- C03: supported_generated — E16/E17 provide boundary constraints and lower bounds
- D09: partial (was missing)
- O08, O09: implemented (were proposed/partial)

Cannot claim:
- real QDM/NV validation
- real CAD/Gerber/GDS validation (E14 is scaffold only)
- external FEM/FastHenry validation
- real multilayer recovery from multi-height observations
- real hardware via-chain sensitivity
- that differentiable forward validates against external solvers
- that regularization baselines transfer to real measurements

Next required evidence:
- validate multi-height observability with real measurement or external solver rows
- replace hand-authored layout JSON with real CAD/Gerber/GDS parsing
- validate differentiable forward against COMSOL/FastHenry/FEM
- validate regularization baselines against external solver forward fields

Test results:
- `uv run python scripts/validate_graph.py`: PASS (0 errors, 0 warnings)
- `uv run python scripts/check_claim_gates.py`: PASS
- `uv run python scripts/check_metrics_schema.py`: PASS (17 files)
- `uv run python scripts/check_no_leakage.py`: PASS (17 files)
- `uv run python scripts/check_evidence_outputs.py`: PASS (17 files)
- `uv run python -m pytest -q`: PASS (11 tests)
- `uv run python scripts/run_evidence.py --all --mode test --continue-on-fail`: PASS (all 17)
- `uv run python scripts/run_evidence.py --all --mode smoke --continue-on-fail`: TIMEOUT (600s at E07 PyPEEC)

Branch integration audit:
- feat/e14-layout-graph-import-clean: CLEAN merge (fast-forward)
- feat/e13-multistate-observability: CLEAN merge (conflicts resolved)
- feat/e16-differentiable-forward: CONTAMINATED (E13/E14/E15/E17 mixed) — clean cherry-pick used
- feat/e15-four-layer-via-chain: EMPTY (no commits) — extracted from feat/e16
- feat/e17-l1curl-baseline: EMPTY (no commits) — extracted from feat/e16 + new research graph entries

## 2026-05-04 - L1-curl and divergence-free regularization baselines

Claim affected:
- C02_single_plane_identifiability_boundary
- C03_unet_topology_baseline_boundary

Change type:
- new evidence package E17 added with Fourier Wiener, Tikhonov, L1-curl, and
  div-free regularization baselines on E03 two-layer via benchmark

Files changed:
- `experiments/evidence/E17_l1_curl_divergence_free_baseline/`
- `outputs/by_claim/C02_identifiability_boundary/`
- `research_graph/`

Evidence:
- E17 compares 4 regularization baselines across 3 noise levels and 2 standoffs
  (144 runs total) on E03 train/val/test/ood splits.

Metrics:
- Fourier Wiener: divergence residual 3e-12, edge preservation 0.14
- Tikhonov: current RMSE 1.45, divergence residual 0.26
- L1-curl: edge preservation and divergence balanced
- Div-free: divergence residual < 1e-10
- All 7 acceptance gates pass.

Claim status before:
- C02: supported by E02, E03, E13, E15.
- C03: supported_generated by E03, E04.

Claim status after:
- C02: supported by E02, E03, E13, E15, E17 (strengthened with regularization baseline).
- C03: motivated by E17 (physics-regularized baselines as lower bound).

Cannot claim:
- real CAD/Gerber/GDS validation
- real QDM/NV validation
- external FEM/FastHenry validation
- that optimal regularization on generated data transfers to real measurements

Next required evidence:
- validate regularization baselines against external solver forward fields.

## 2026-05-04 - Differentiable Biot-Savart forward layer evidence

Claim affected:
- C04_inverse_crime_and_operator_gap
- C03_unet_topology_baseline_boundary
- C10_pdn_kcl_distribution_need

Change type:
- new experiment E16 added with FFT-domain differentiable Biot-Savart forward
- sheet forward (Jx/Jy -> Bx/By/Bz) and via forward (s_l -> Bx/By)
- numpy reference implementation with optional torch autograd path
- no CUDA hard dependency

Files changed:
- `experiments/evidence/E16_differentiable_forward_layer/`
- `research_graph/experiments.yml`
- `research_graph/evidence_edges.yml`
- `outputs/by_claim/` for C03, C04, C10

Evidence:
- E16 provides a reusable differentiable Biot-Savart forward building block
  for white-box inverse optimization, topology baseline constraint, and
  multilayer PDN forward.

Metrics:
- All 6 acceptance gates pass. 10/10 unit tests pass (1 skipped: torch not installed).

Claim status before:
- C04: supported_generated by E04, E06, E07.
- C03: supported_generated by E03, E04.
- C10: supported_generated by E10, E11, E12.

Claim status after:
- No status change. E16 strengthens the generated-domain evidence base
  without upgrading to real validation.

Cannot claim:
- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL agreement
- that the forward layer is a substitute for external solver validation

Next required evidence:
- validate the differentiable forward against COMSOL/FastHenry/FEM on a small
  auditable subset for operator-gap quantification.

## 2026-05-04 - Four-layer via-chain benchmark evidence

Claim affected:
- C10_pdn_kcl_distribution_need
- C02_single_plane_identifiability_boundary
- C06_graph_hypothesis_system_identification

Change type:
- generated four-layer via-chain benchmark evidence package (E15) added
- 6 stress families, 11-channel output, 4 baselines
- graph/KCL-aware baseline reduces layer misallocation vs naive

Files changed:
- `experiments/evidence/E15_four_layer_via_chain_benchmark/`
- `outputs/by_claim/C10_pdn_kcl_distribution_need/`
- `outputs/by_claim/C02_identifiability_boundary/`
- `outputs/by_claim/C06_graph_hypothesis_system_id/`
- `research_graph/`

Evidence:
- E15 generates 6 families x 3 variants = 18 cases of four-layer via-chain
  current distributions with centerline Biot-Savart forward fields.

Metrics:
- 18 cases, 4 layers, 11 output channels, 4 baselines, all 8 acceptance gates pass.

Claim status before:
- C10: supported_generated by E10, E11, E12, E14.
- C02: supported by E02, E03, E13.
- C06: supported_generated by E08, E12, E13, E14.

Claim status after:
- No change (all three claims already supported_generated/supported).

Cannot claim:
- real four-layer PCB/chip, CAD/Gerber/GDS, external FEM/FastHenry/COMSOL,
  real QDM/NV validation, mechanism-level correctness.

Next required evidence:
- validate a small generated/CAD-like subset against independent external solvers.

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

## 2026-05-04 - Layout graph import scaffold

Claim affected:
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need

Change type:
- generated layout graph import scaffold evidence package added
- D09_cad_gerber_gds_like status moved from missing to partial
- evidence edges and outputs/by_claim updated

Files changed:
- `experiments/evidence/E14_layout_graph_import_scaffold/`
- `outputs/by_claim/C06_graph_hypothesis_system_id/`
- `outputs/by_claim/C10_pdn_kcl_distribution_need/`
- `research_graph/`

Evidence:
- `E14_layout_graph_import_scaffold` parses simplified JSON/YAML layout schemas
  into route graphs, via candidate graphs, layer stacks, net/port graphs, and
  return candidates. H0/H1/H2/H3 hypothesis candidates are generated from the
  extracted graph. Four example layouts demonstrate the scaffold capability.

Metrics:
- Example count: 4
- Schema validates all examples: True
- Total layers found: 6 across all examples
- All 4 examples generate all 4 hypothesis candidates
- All acceptance gates passed

Claim status before:
- `C06_graph_hypothesis_system_identification`: supported_generated.
- `C10_pdn_kcl_distribution_need`: supported_generated.
- `D09_cad_gerber_gds_like`: missing.

Claim status after:
- `C06_graph_hypothesis_system_identification`: remains supported_generated with
  scaffold-level support from E14.
- `C10_pdn_kcl_distribution_need`: remains supported_generated with scaffold-level
  support from E14.
- `D09_cad_gerber_gds_like`: partial.

Cannot claim:
- real CAD/Gerber/GDS validation.
- real QDM/NV validation.
- external FEM/FastHenry validation.
- that the generated scaffold replaces CAD-derived graph candidates.
- that the KCL proxy is a real circuit solve.

Next required evidence:
- replace hand-authored layout JSON with actual CAD/Gerber/GDS parsing.
- validate a small generated/CAD-like subset against independent external solvers.
