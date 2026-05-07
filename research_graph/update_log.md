# Update Log

## 2026-05-07 - GPU environment migrated from WSL conda to Windows-native uv

Claim affected:
- None. Compute environment migration, not scientific evidence.

Change type:
- Migrated GPU PyTorch from WSL `quantum-dev` conda to Windows-native `uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128`
- Verified: CUDA 12.8, RTX 5060 Laptop GPU, torch 2.11.0+cu128
- Updated all project docs: AGENTS.md, worktree protocol, E07/E12 reproduce guides
- CuPy/JAX GPU backends now install via `uv pip install` in project venv
- Removed WSL-specific GPU entrypoint; everything is Windows-native

Evidence:
- `uv run python -c "import torch; print(torch.cuda.is_available())"` → True
- `torch.cuda.get_device_name(0)` → "NVIDIA GeForce RTX 5060 Laptop GPU"

Cannot claim:
- GPU is always available (still requires NVIDIA driver + cu128-compatible GPU).

Next required evidence:
- None. This is infrastructure, not evidence.

Files changed:
- `AGENTS.md`
- `docs/research_strategy/claude_worktree_breakthrough_protocol.md`
- `experiments/evidence/E07_solver_bridge/README.md`
- `experiments/evidence/E12_pdn_physics_learning/REPRODUCE.md`

## 2026-05-06 - Compute policy clarified for CPU/GPU selection

Claim affected:
- None. This is an agent execution policy update, not scientific evidence.

Change type:
- Updated global and project agent instructions so GPU is selected when the
  workload itself is naturally GPU-accelerated and materially faster on GPU
- Preserved CPU as default for small scripts, metadata, IO, lightweight fitting,
  and short tests
- Documented WSL `quantum-dev` as the GPU environment and retained CPU fallback

Evidence:
- None. This does not support or upgrade any claim.

Cannot claim:
- A GPU run is more scientifically valid than CPU by default.
- CUDA is always faster or always available.

Next required evidence:
- For future evidence packages using GPU, record the compute path and preserve
  reproducible CPU fallback where feasible.

Files changed:
- `AGENTS.md`
- `docs/research_strategy/claude_worktree_breakthrough_protocol.md`
- global `C:\Users\yunca\.claude\CLAUDE.md`

## 2026-05-06 - First-principles magnetic-current inversion breakthrough strategy

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality

Change type:
- Strategic design document added under `docs/research_strategy/`
- No new evidence package
- No claim status change

Evidence:
- None. The document is a first-principles research strategy and cannot support
  or upgrade claims.

Cannot claim:
- That the taxonomy is experimental validation.
- That direction coverage proves practical recovery of all chip currents.
- That generated-domain, external-solver, or real QDM/NV gaps are closed.

Next required evidence:
- Active OQCI measurement design over multi-height/multi-state/vector channels.
- External-solver operator-gap validation.
- Real QDM/NV simple-wire or known-via sanity rows.
- CAD/GDS-derived Graph-Hodge current bases.

Files changed:
- `docs/research_strategy/current_inversion_breakthrough_first_principles.md`
- `research_graph/overclaim_guardrails.md`
- `research_graph/update_log.md`

## 2026-05-06 - Claude worktree breakthrough protocol

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality

Change type:
- Operating protocol added for future Claude Code worktree delegation
- Requires `--effort max` for all Claude worker invocations
- Establishes design-first, worktree-isolated, Codex-audited breakthrough loop
- No new evidence package
- No claim status change

Evidence:
- None. This is orchestration protocol, not scientific evidence.

Cannot claim:
- Claude worker output is evidence before Codex audit and research graph
  registration.
- Claude implementation success proves real validation.

Next required evidence:
- Write detailed algorithm design documents for the next top-level breakthrough
  packages before launching workers.
- Launch up to three `claude --effort max --worktree ...` workers on disjoint
  scopes, then audit and iterate.

Files changed:
- `docs/research_strategy/claude_worktree_breakthrough_protocol.md`
- `research_graph/overclaim_guardrails.md`
- `research_graph/update_log.md`

## 2026-05-06 - Top-level breakthrough design documents E20/E21/E23

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality

Change type:
- Three detailed algorithm blueprint documents added before implementation
- E20 targets active OQCI measurement design
- E21 targets external-solver/operator-gap ladder
- E23 targets CAD/GDS-derived Graph-Hodge current basis
- No new evidence package
- No claim status change

Evidence:
- None. These are implementation blueprints for Claude worktree workers.

Cannot claim:
- The design documents validate the algorithms.
- The planned packages close real QDM/NV, real CAD/GDS, or external-solver gaps
  before implementation and audit.

Next required evidence:
- Launch `claude --effort max --worktree ...` workers on E20, E21, and E23.
- Audit worker outputs and iterate until evidence packages produce useful
  metrics or preserved failure modes.

Files changed:
- `docs/algorithm_blueprints/E20_active_oqci_measurement_design.md`
- `docs/algorithm_blueprints/E21_external_solver_operator_gap_ladder.md`
- `docs/algorithm_blueprints/E23_cad_gds_graph_hodge_basis.md`
- `research_graph/update_log.md`

## 2026-05-06 - Round-2 worker directives after E20/E21/E23 audit

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality

Change type:
- Added three round-2 directive documents after auditing first Claude worker
  outputs
- E20 round 2 targets epsilon sweep and multi-state active OQCI
- E21 round 2 targets stronger operator perturbation and PyPEEC attempt
- E23 round 2 targets projected KCL-compatible Graph-Hodge blocks and
  multi-height OQCI
- No new evidence integrated into main worktree
- No claim status change

Evidence:
- None in main worktree. First worker outputs remain in isolated worktrees until
  audited and integrated.

Cannot claim:
- Round-1 worker outputs are registered evidence.
- Round-2 directives validate any algorithm.

Next required evidence:
- Resume the three Claude workers with `--effort max` using these directives.
- Audit round-2 outputs before any integration.

Files changed:
- `docs/algorithm_blueprints/E20_round2_epsilon_multistate_directive.md`
- `docs/algorithm_blueprints/E21_round2_pypeec_decision_instability_directive.md`
- `docs/algorithm_blueprints/E23_round2_projected_multheight_hodge_directive.md`
- `research_graph/update_log.md`

## 2026-05-06 - Round-3 decisive validation directives

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need

Change type:
- Added three round-3 directive documents after auditing round-2 outputs
- E20 round 3 tests whether the multi-state signal is real using truth coverage,
  singleton correctness, and empty-set separation
- E21 round 3 fixes mechanism-instability reporting and adds a stronger
  template/nonlinear scorer
- E23 round 3 replaces pseudoinverse projection with SVD nullspace projection
  and tests multi-state Graph-Hodge OQCI
- No new evidence integrated into main worktree
- No claim status change

Evidence:
- None in main worktree. Worker outputs remain isolated until audited and
  integrated.

Cannot claim:
- The E20 round-2 interval shrink is a breakthrough before truth coverage is
  audited.
- E21 mechanism instability is fully reported until report/metrics consistency
  is fixed.
- E23 Graph-Hodge projection is KCL-safe until SVD projection passes.

Next required evidence:
- Resume the three Claude workers with `--effort max` using these round-3
  directives.
- Audit whether E20 produces nonempty singleton-correct consistent sets.

Files changed:
- `docs/algorithm_blueprints/E20_round3_truth_coverage_directive.md`
- `docs/algorithm_blueprints/E21_round3_nonlinear_report_fix_directive.md`
- `docs/algorithm_blueprints/E23_round3_svd_multistate_graph_hodge_directive.md`
- `research_graph/update_log.md`

## 2026-05-06 - Round-4 robustness directives for generated-domain signal

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need

Change type:
- Added three round-4 directive documents after auditing round-3 worker outputs
- E23 round 4 stress-tests the first credible generated-domain signal using
  per-layout hard-case metrics, finite-width/operator perturbations, and
  port-feasible multi-state separation
- E20 round 4 tests whether regularized/reduced-basis consistent sets can
  remove empty-set discrimination and improve truth coverage
- E21 round 4 tests a ridge evidence scorer and margin-refusal policy under
  operator gap
- No new evidence integrated into main worktree
- No claim status change

Evidence:
- None in main worktree. These are implementation directives for Claude
  workers and cannot support claims by themselves.

Cannot claim:
- The E23 round-3 multi-state Graph-Hodge signal is robust until per-layout
  hard-case and finite-width stress gates pass.
- E20 active OQCI is a breakthrough unless nonempty singleton-correct
  consistent sets dominate under calibrated epsilon.
- E21 operator-gap mitigation works unless a stronger scorer survives
  cross-operator shifts with bounded wrong accepts.

Next required evidence:
- Resume the three Claude workers with `--effort max` using these round-4
  directives.
- Audit whether E23 keeps H1/H2 separation under finite-width and
  port-feasible excitation states.
- Keep all generated-domain claims separated from real CAD/GDS, PyPEEC, and
  real QDM/NV validation.

Files changed:
- `docs/algorithm_blueprints/E20_round4_regularized_consistent_set_directive.md`
- `docs/algorithm_blueprints/E21_round4_ridge_evidence_scorer_directive.md`
- `docs/algorithm_blueprints/E23_round4_min_perlayout_finitewidth_directive.md`
- `research_graph/update_log.md`

## 2026-05-06 - Round-5 theorem-driven mathematical directives

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality

Change type:
- Added a top-level mathematical breakthrough program for magnetic-field to
  current inversion
- Added three round-5 Claude worker directives with explicit formulas for
  Graph-Hodge KCL affine current spaces, OQCI observation manifolds, pairwise
  affine separation, robust operator/noise margins, active port-excitation
  design, and operator-gap certificates
- E23 round 5 targets robust observable-quotient certification over a generated
  layout ensemble and adversarial perturbations
- E20 round 5 targets pairwise-margin active measurement design
- E21 round 5 targets multi-basis operator-gap margin certificates
- No new evidence integrated into main worktree
- No claim status change

Evidence:
- None. These are theorem-driven design documents and worker directives, not
  experimental evidence.

Cannot claim:
- The mathematical program proves practical current recovery without runnable
  evidence.
- The E23 generated-domain signal is robust until positive margins survive
  layout ensemble, port-feasible excitation, and adversarial perturbation gates.
- E20/E21 improvements support real QDM/NV, real CAD/GDS, or external-solver
  validation before those data/artifacts are added.

Next required evidence:
- Resume the three Claude workers with `--effort max` using the round-5
  directives.
- Audit robust margins rather than raw distance gains.
- Treat a negative E20/E21 result as useful boundary evidence if it is
  mathematically quantified and cannot-claim guarded.

Files changed:
- `docs/research_strategy/current_inversion_mathematical_breakthrough_program.md`
- `docs/algorithm_blueprints/E20_round5_pairwise_margin_active_design_directive.md`
- `docs/algorithm_blueprints/E21_round5_multibasis_operator_gap_certificate_directive.md`
- `docs/algorithm_blueprints/E23_round5_robust_observable_quotient_certificate_directive.md`
- `research_graph/update_log.md`

## 2026-05-06 - E24/E25/E26 high-density breakthrough directives

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need
- C13_calibration_protocol_reality

Change type:
- Added three dense mathematical directives for the next breakthrough cycle
- E24 targets network-solved multi-state topology profile inversion where all
  excitation states share one topology and one conductance vector
- E25 targets calibrated volume forward modeling and operator-radius
  decomposition to replace crude finite-width uncertainty penalties
- E26 targets active port-state design that optimizes robust profile margin
  rather than raw distance, entropy, or top-1 accuracy
- Added guardrails that raw generated-domain distance and network-profile
  success do not constitute real chip reverse-analysis validation
- No new evidence integrated into main worktree
- No claim status change

Evidence:
- None. These are design directives for Claude workers and cannot support
  claims by themselves.

Cannot claim:
- E24/E25/E26 design text proves a current-inversion breakthrough.
- A generated positive distance is a breakthrough before the robust margin
  remains positive after noise, calibration, and operator-radius subtraction.
- Network-solved generated topology inversion proves real chip reverse analysis
  before real layout, external solver, and measured QDM/NV gates.

Next required evidence:
- Launch `claude --effort max` workers on E24, E25, and E26 in isolated
  worktrees.
- Audit whether E24 produces profile separation from shared conductance
  constraints, whether E25 tightens or confirms the operator radius, and whether
  E26 finds port states that improve certified Gamma.

Files changed:
- `docs/algorithm_blueprints/E24_network_solved_multistate_topology_profile_inversion.md`
- `docs/algorithm_blueprints/E25_calibrated_volume_forward_rho_tightening.md`
- `docs/algorithm_blueprints/E26_active_port_state_gamma_design.md`
- `research_graph/overclaim_guardrails.md`
- `research_graph/update_log.md`

## 2026-05-06 - E27/E28/E29 Schur-signature breakthrough directives

Claim affected:
- C02_single_plane_identifiability_boundary
- C04_inverse_crime_and_operator_gap
- C06_graph_hypothesis_system_identification
- C10_pdn_kcl_distribution_need
- C13_calibration_protocol_reality

Change type:
- Added three high-density directives after auditing E24/E25/E26 outputs
- E27 targets edge-defect Schur/Sherman-Morrison magnetic signatures, using
  analytic network perturbation to design defect-sensitive port states
- E28 targets magnetic transfer-matrix invariants, including projector, Gram,
  and differential common-mode cancellation representations
- E29 targets rho-integrated conservative/RSS Schur Gamma certificates using
  E25-style calibrated operator-radius budgets
- No new evidence integrated into the research graph
- No claim status change

Evidence:
- None in main research graph. E24/E25/E26 worker outputs remain implementation
  material until audited, migrated if needed, and registered.

Cannot claim:
- E24 shared-network smoke output is a breakthrough; profile gaps remained too
  small and robust Gamma stayed negative.
- E25 operator-radius calibration alone creates current-inversion
  identifiability.
- E26 active port-state search solves topology diagnosis; generic states did
  not produce positive Gamma.
- E27/E28/E29 design text proves a breakthrough before runnable evidence and
  robust certificates exist.

Next required evidence:
- Launch `claude --effort max` workers on E27, E28, and E29.
- Prioritize positive conservative Gamma, not raw signal energy.
- If conservative Gamma fails but raw/RSS gains pass, preserve the boundary
  rather than upgrading claims.

Files changed:
- `docs/algorithm_blueprints/E27_edge_defect_schur_magnetic_signature.md`
- `docs/algorithm_blueprints/E28_magnetic_transfer_matrix_observable_invariants.md`
- `docs/algorithm_blueprints/E29_rho_integrated_schur_gamma_certificate.md`
- `research_graph/update_log.md`

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
# 2026-05-06: E01-E29 critical review and next breakthrough direction

- Added `docs/research_strategy/E01_E29_critical_review_next_breakthrough.md`.
- Scope: strategic mathematical audit only; not evidence and not claim support.
- Main conclusion: no E01-E29 package is yet a claim-level major
  current-inversion breakthrough.
- Strongest next candidate identified as transfer-operator observable quotient
  inversion: multi-state port-to-magnetic transfer Gram invariants plus
  Graph-Hodge/KCL/network bases, E25-style calibrated rho, hard-case
  layout-ensemble certification, and active port-state design.
- Audit risks recorded in the document include E28 best-invariant/gate
  inconsistency, E25 over-lenient convergence gate, E26 metric inconsistency,
  and E29 split-discipline failure.
- Claim status unchanged.

# 2026-05-06: E28 transfer-matrix Gram quotient evidence

Claim affected:
- `C02_single_plane_identifiability_boundary`
- secondary: `C06_graph_hypothesis_system_identification`,
  `C04_inverse_crime_and_operator_gap`, `C10_pdn_kcl_distribution_need`

Evidence added:
- `E28_magnetic_transfer_matrix_observable_invariants`

Change type:
- New generated-domain evidence package.
- Fixed best-invariant selection to exclude raw observations and bind gates to
  one selected invariant.
- Added deterministic nuisance seeding, observable quotient certificate, and
  gain-only hard-case sweep.

Metrics:
- selected invariant: Gram.
- Gram positive full-pair Gamma rate: 5/6 = 0.8333333333.
- Gram observable quotient Q0={H0}, Q12={H1,H2}, Q3={H3}: all cross-quotient
  margins positive; min Gamma = 0.4511206603.
- H1_via vs H2_model_gap remains unresolved; Gram Gamma = -0.1286141869.
- Gain-only hardcase sweep: 3/5 rows where raw quotient fails but Gram quotient
  remains positive; first gain = 0.08; max tested positive Gram quotient gain =
  0.18.
- Consistent-set truth-in-consistent rate: 1.0; singleton wrong rate: 0.0.
- Engineering and scientific gates pass under the revised E28 gates.

Claim status change:
- `C02_single_plane_identifiability_boundary` remains `supported`.
- E28 adds medium generated-domain support for quotient identifiability and
  strong limitations against full four-hypothesis separability.

Cannot claim:
- full H0/H1/H2/H3 robust separability.
- H1_via versus H2_model_gap separation.
- real QDM/NV validation.
- real CAD/Gerber/GDS validation.
- external solver validation.
- real chip reverse analysis.

Next required evidence:
- Broader layout ensemble hard cases.
- External-solver held-out transfer matrices.
- Real-calibrated gain, standoff, registration, background, and noise nuisance.
- Richer hypotheses or observations that could split H1_via from
  H2_model_gap.

# 2026-05-06: E01-E29 deep replay and next breakthrough strategy

Change type:
- Strategic audit document added; not evidence and not claim support.

Files changed:
- `docs/research_strategy/E01_E29_deep_replay_next_major_breakthrough.md`

Conclusion:
- E28 is the only current positive major-breakthrough candidate, but only for
  an observable quotient Q0={H0}, Q12={H1,H2}, Q3={H3}.
- E20/E21/E23/E24/E26/E27/E29 remain negative, partial, or provisional for
  claim-level breakthrough purposes.
- The next most likely major breakthrough is an E28-centered calibrated
  transfer-operator quotient certificate: transfer-matrix Gram invariant,
  E25-style rho, family-heldout hard cases, Graph-Hodge/shared-network physics,
  and active port states scored by robust invariant Gamma.

Cannot claim:
- new experimental evidence.
- claim status upgrade.
- real QDM/NV, real CAD/GDS, or external solver validation.
- full H0/H1/H2/H3 separability.

# 2026-05-06: E28 H1/H2 phase-diagram audit

Claim affected:
- `C02_single_plane_identifiability_boundary`
- secondary: `C06_graph_hypothesis_system_identification`,
  `C04_inverse_crime_and_operator_gap`, `C10_pdn_kcl_distribution_need`

Evidence updated:
- `E28_magnetic_transfer_matrix_observable_invariants`

Change type:
- Added parameterized H2 model-gap controls:
  `h2_via_factor`, `h2_sheet_jitter`, `h2_sheet_jitter_seed`.
- Added `H1_H2_PHASE_DIAGRAM.md` and top-level
  `h1_h2_phase_diagram` metrics.
- The phase diagram sweeps 32 generated-domain H2 via-factor/sheet-jitter rows
  and evaluates the same robust Gram Gamma with an explicit reduced nuisance
  budget.

Metrics:
- E28 status remains `passed`; engineering and scientific gates pass.
- Gram observable quotient Q0={H0}, Q12={H1,H2}, Q3={H3} remains all-positive.
- H1/H2 phase rows with positive Gram Gamma: 0/32.
- Default H1/H2 row: Gamma = -0.0948871365.
- Default zero-noise H1/H2 row: Gamma = -0.0138906779.
- Default required eps+rho for H1/H2: <= 0.0028658462.
- Default observed eps+rho for H1/H2: 0.0977529827.
- Gram quotient survival across phase rows: 1.0.

Claim status change:
- `C02_single_plane_identifiability_boundary` remains `supported`.
- E28's positive support remains the observable quotient, not full
  H0/H1/H2/H3 separability.

Cannot claim:
- H1_via versus H2_model_gap separation under the default generated row.
- that the phase-diagram axes span all real model-gap mechanisms.
- real QDM/NV validation, real CAD/GDS validation, external solver validation,
  or real chip reverse analysis.

Next required evidence:
- Stop treating default H1/H2 splitting as the next likely breakthrough under
  the same observation/Gram setup.
- Prioritize broader quotient certification, calibrated nuisance/rho tightening,
  external-solver transfer matrices, and real-calibrated observation nuisance.

# 2026-05-06: E28 directional statistical Gamma certificate

Claim affected:
- `C02_single_plane_identifiability_boundary`
- secondary: `C06_graph_hypothesis_system_identification`,
  `C04_inverse_crime_and_operator_gap`, `C10_pdn_kcl_distribution_need`

Evidence updated:
- `E28_magnetic_transfer_matrix_observable_invariants`

Change type:
- Added `DIRECTIONAL_STATISTICAL_CERTIFICATE.md`.
- Added `directional_statistical_certificate` metrics.
- Added `M20_directional_statistical_gamma`.
- Implemented raw and Gram directional matched-filter margins:
  hypothesis separation `delta` minus z-threshold directional noise, directional
  nuisance, and tau.

Metrics:
- E28 status remains `passed`; engineering and scientific gates pass.
- Baseline selected Gram quotient min Gamma: 0.4511206603.
- Directional Gram quotient min Gamma: 0.5323884196.
- Directional Gram quotient improvement: +0.0812677593.
- Directional Gram quotient all-positive: true.
- Directional Gram H1/H2 Gamma: -0.0560703448.
- Directional raw H1/H2 Gamma: -0.2327572519.

Claim status change:
- `C02_single_plane_identifiability_boundary` remains `supported`.
- The update sharpens the quotient certificate but does not upgrade to full
  H0/H1/H2/H3 separability.

Cannot claim:
- H1_via versus H2_model_gap separation.
- real detection risk control.
- real QDM/NV validation, real CAD/GDS validation, external solver validation,
  or real chip reverse analysis.

Next required evidence:
- Test whether directional Gamma survives broader layout ensembles and
  external-solver transfer matrices.
- Treat H1/H2 splitting as requiring new physical information, not merely
  tighter full-ball-to-directional statistical accounting.

# 2026-05-06: E30 dual-Schur active local defect certificate

Claim affected:
- `C06_graph_hypothesis_system_identification`
- secondary: `C02_single_plane_identifiability_boundary`,
  `C04_inverse_crime_and_operator_gap`, `C10_pdn_kcl_distribution_need`,
  `C11_mechanism_level_explanation`

Evidence added:
- `E30_dual_schur_active_defect_certificate`

Change type:
- Added a generated-domain local via-open defect certificate using E28's
  transfer-matrix forward operator.
- Compared ordinary boundary diagonal ports against local dual Schur endpoint
  excitations.
- Added the current-budget law
  `Gamma_ij(I) = I*s_ij - z*sigma - rho_i(I) - rho_j(I) - tau`.

Metrics:
- E30 status: `passed`; engineering and scientific gates pass.
- Candidate defects: 8 central via-open candidates.
- Pairwise dual Schur certificates: 28/28 positive.
- Boundary control min Gamma without nuisance: -0.06399999999.
- Perimeter-boundary upper-bound min Gamma without nuisance: -0.06399999992.
- Dual Schur min Gamma after noise/nuisance/tau: 0.1348041937.
- Truth pairwise certified rate: 1.0.
- Dual critical amplitude: 16.09623992 under configured amplitude 50.
- Boundary optimistic critical amplitude: 3.191177882e11.
- Perimeter-boundary optimistic critical amplitude: 4.117612711e10.

Claim status change:
- `C06_graph_hypothesis_system_identification` remains `supported_generated`
  but gains a positive local-access defect-signature certificate.
- `C02_single_plane_identifiability_boundary` remains `supported` with a new
  active-measurement boundary: local Schur access changes observability, while
  ordinary boundary ports remain negative for the E30 control.

Cannot claim:
- pad-feasible active probing.
- arbitrary current recovery or real chip reverse analysis.
- real QDM/NV validation, real CAD/GDS validation, or external solver
  validation.
- H1_via versus H2_model_gap separation.
- via-short, return-path, dense-cluster, finite-width, or real mechanism-level
  explanation.

Next required evidence:
- Constrain dual Schur endpoint patterns to real pad-accessible boundary ports.
- Repeat over broader generated layout ensembles and non-central defect
  families.
- Add finite-width, registration, layer-z, and external-solver rho components.
- Validate against CAD/GDS-derived graph candidates and independent solver rows.

# 2026-05-06: E31 pad-Schur reachability certificate

Claim affected:
- `C06_graph_hypothesis_system_identification`
- secondary: `C02_single_plane_identifiability_boundary`,
  `C04_inverse_crime_and_operator_gap`, `C10_pdn_kcl_distribution_need`

Evidence added:
- `E31_pad_schur_reachability_certificate`

Change type:
- Added exact pad reachability theorem:
  `eta_e(P)=osc_P(L^+ d_e)/(d_e^T L^+ d_e)`.
- Added theorem-selected max/min pad-pair synthesis for top candidate-projection
  surface pads plus a reference pad.
- Added finite-difference magnetic directional Gamma certificate with
  height/gain nuisance subtraction.

Metrics:
- E31 status: `passed`; engineering and scientific gates pass.
- Candidate defects: 8 central via-open candidates.
- Perimeter pad reachability min ratio: 2.48821324e-09.
- Top candidate-projection surface pad reachability min ratio: 0.4767196129.
- Pad-Schur pairwise certificates: 28/28 positive.
- Pad-Schur min Gamma after nuisance: 0.01963293336.
- Truth pairwise certified rate: 1.0.
- Pad-Schur critical amplitude: 38.26243887 under configured amplitude 50.
- Negative control top-candidate reference-basis min Gamma: -0.004862585689.

Claim status change:
- `C06_graph_hypothesis_system_identification` remains `supported_generated`
  but now has a positive generated-domain pad-accessible Schur synthesis result,
  not only a local endpoint-access upper bound.
- `C02_single_plane_identifiability_boundary` gains a sharper active-access
  boundary: perimeter pads are provably near-null for the E31 central via-open
  set, while candidate-projection surface pads are sufficient in the generated
  model.

Cannot claim:
- real pad availability or package/contact parasitic robustness.
- perimeter-only probing works.
- arbitrary current recovery or real chip reverse analysis.
- real QDM/NV validation, real CAD/GDS validation, or external solver
  validation.

Next required evidence:
- Add realistic pad pitch/current/contact/package constraints.
- Stress over broader/non-central defect families and layout ensembles.
- Add finite-width, registration, layer-z, and external-solver rho.
- Validate on CAD/GDS-derived graph candidates and independent solver rows.

# 2026-05-06: E32 pad-pitch Schur phase diagram

Claim affected:
- `C06_graph_hypothesis_system_identification`
- secondary: `C02_single_plane_identifiability_boundary`,
  `C04_inverse_crime_and_operator_gap`, `C10_pdn_kcl_distribution_need`

Evidence added:
- `E32_pad_pitch_schur_phase_diagram`

Change type:
- Added exact pad-pitch, offset, and local-patch Schur reachability phase
  diagram using the E31 theorem.
- Added locality barrier derivation: low
  `osc_P(L^+d_e)/(d_e^T L^+d_e)` is a pad-space active-mode reachability
  limit, not an optimizer failure.
- Added design-rule evidence separating candidate-local pads, top+bottom
  local pads, perimeter pads, and sparse regular-grid offsets.

Metrics:
- E32 status: `passed`; engineering and scientific gates pass.
- Candidate defects: 8 central via-open candidates.
- Candidate-projection top pad min reachability: 0.4767196129.
- Top+bottom candidate pad min reachability: 0.9534392258.
- Perimeter pad min reachability: 2.48821324e-09.
- Stride-2 worst min reachability: 3.37239662e-04.
- Stride-5+ worst min reachability: 4.75424120e-10.
- Candidate/stride-2 worst current multiplier proxy: about 1413.59.
- Candidate/stride-5+ worst current multiplier proxy: about 1.0027e9.

Claim status change:
- `C06_graph_hypothesis_system_identification` remains `supported_generated`.
  E32 adds a generated-domain pad-geometry locality barrier and design-for-test
  direction, not real pad/package validation.
- `C02_single_plane_identifiability_boundary` gains a sharper active-access
  boundary: sparse or perimeter pad spaces can be mathematically unable to
  synthesize the local Schur defect mode even before magnetic post-processing.

Cannot claim:
- fresh magnetic Gamma evidence beyond E31.
- real pad availability, contact resistance, package parasitic robustness, or
  driver current/voltage feasibility.
- arbitrary current recovery or real chip reverse analysis.
- real QDM/NV validation, real CAD/GDS validation, or external solver
  validation.

Next required evidence:
- Run magnetic Gamma only on the E32-selected physically plausible local pad
  designs.
- Add contact resistance, voltage/current driver limits, and package return
  impedance.
- Repeat over broader/non-central generated layout families.
- Move reachability and Gamma audits to CAD/GDS-derived graph candidates and
  independent solver rows.

# 2026-05-07: E33 certified observable current subspace inversion

Claim affected:
- `C02_single_plane_identifiability_boundary`
- secondary: `C04_inverse_crime_and_operator_gap`,
  `C06_graph_hypothesis_system_identification`

Evidence added:
- `E33_certified_observable_current_subspace_inversion`

Change type:
- Added strict current-density inversion certificate based on the Fisher
  spectrum `G_obs=Phi^T A^T Sigma^-1 A Phi`.
- Added a generated Fourier/stream-function thin-sheet runnable slice where
  each current mode has response `s(q,h)=q exp(-q h)` and Fisher eigenvalue
  `lambda(q)=sum_h s(q,h)^2/sigma^2`.
- Added explicit dark-mode refusal and full-inverse hallucination audit.

Metrics:
- E33 status: `passed`; engineering and scientific gates pass.
- Mode count: 144.
- Single-height stable current modes: 8.
- Single-height dark/refused current modes: 136.
- Generated truth dark-energy fraction: 0.9228192454.
- Certified stable projection RMSE: 0.1164511532.
- Full naive least-squares current inverse total RMSE: 720.7362501.
- Full/certified total RMSE ratio: 1547.322749.
- Full naive dark hallucination norm: 8649.239996.
- Certified dark hallucination norm: 0.0.
- Stable 3-sigma coefficient coverage: 1.0.
- Multi-height stable current modes: 37.

Claim status change:
- `C02_single_plane_identifiability_boundary` remains `supported`, now with a
  strict generated-domain current-inversion certificate: the data-supported
  object is `Pi_obs J`, not full `J`.
- `C04_inverse_crime_and_operator_gap` remains limited because E33 is
  same-forward generated Fourier/thin-sheet evidence.
- `C06_graph_hypothesis_system_identification` gains a bridge from current-map
  inversion to observable graph/Hodge current modes.

Cannot claim:
- full current-density recovery.
- recovery of dark current modes.
- real QDM/NV validation, real CAD/GDS validation, or external solver
  validation.
- finite-width, package, contact, or real multilayer chip robustness.

Next required evidence:
- Move the observable-current subspace split from diagonal Fourier modes to
  graph/Hodge/CAD-like current bases.
- Add finite-width, registration, background, and external-solver rho to the
  Fisher threshold.
- Combine E33 observable current modes with E30-E32 active pad reachability.
- Validate on independent solver rows, then real QDM/NV sanity-gated rows.
