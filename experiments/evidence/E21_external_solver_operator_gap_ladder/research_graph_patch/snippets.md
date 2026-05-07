# E21 Research Graph Patch — Proposed Snippets

Do NOT write these directly into the global SSOT files. These are proposals for
Codex audit and integration.

---

## experiments.yml — new entry

```yaml
E21_external_solver_operator_gap_ladder:
  title: "External-solver operator-gap ladder with field-level and decision-level stability"
  claim: C04_inverse_crime_and_operator_gap
  secondary_claims: [C10_pdn_kcl_distribution_need, C05_pypeec_solver_bridge]
  data: [D00_canonical_wire_loop_via]
  physics: [P01_biot_savart_maxwell_forward, P02_divB_zero, P08_return_path_completeness, P09_finite_width_material_thickness]
  forward: [F01_analytic_reference, F02_centerline_biot_savart, F03_finite_width_surrogate, F04_pypeec, F05_comsol_fem, F06_fasthenry]
  observation: [O01_ideal_Bxyz]
  representation: [R01_pixel_current_map]
  algorithm: [A04_hypothesis_scorer, A08_differentiable_forward_optimization]
  protocol: [S05_solver_heldout, S11_no_leakage_calibration_heldout]
  metrics: [M01_field_l2_or_rmse, M02_current_l2_or_rmse, M06_h0_false_any, M07_h1_recall, M13_family_generalization_gap]
  outputs:
    - outputs/by_claim/C04_inverse_crime_operator_gap/E21_OPERATOR_GAP_LADDER_EVIDENCE.md
  runtime:
    package_dir: experiments/evidence/E21_external_solver_operator_gap_ladder
    run_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs"
    smoke_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke"
    test_command: "uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests"
    metrics_files:
      - experiments/evidence/E21_external_solver_operator_gap_ladder/outputs/metrics.json
  result_summary: "Field-level and decision-level operator gaps quantified across analytic, centerline, and finite-width operators on canonical geometries. External solver validation blocked (no COMSOL/FastHenry artifacts). PyPEEC interface scaffold ready but operator blocked (not installed)."
  status: partial
  last_run: "2026-05-06"
```

## evidence_edges.yml — new edges

```yaml
- id: edge_E21_to_C04
  from: E21_external_solver_operator_gap_ladder
  to: C04_inverse_crime_and_operator_gap
  relation: supports
  strength: medium
  scope: "field-level and decision-level operator gap quantification on canonical geometries"
  caveat: "Generated-domain evidence only; external solver validation blocked. PyPEEC operator scaffold only."
  evidence_files:
    - outputs/by_claim/C04_inverse_crime_operator_gap/E21_OPERATOR_GAP_LADDER_EVIDENCE.md

- id: edge_E21_limits_C04
  from: E21_external_solver_operator_gap_ladder
  to: C04_inverse_crime_and_operator_gap
  relation: limits
  strength: strong
  scope: "generated-domain operator gap boundary"
  caveat: "No COMSOL/FastHenry/FEM artifacts loaded. Operator gaps are within generated-domain operators only. Cannot claim external validation."

- id: edge_E21_to_C10
  from: E21_external_solver_operator_gap_ladder
  to: C10_pdn_kcl_distribution_need
  relation: motivates
  strength: medium
  scope: "operator-gap ladder on canonical geometries motivates PDN operator realism"
  caveat: "Canonical geometries only; not yet applied to PDN/KCL distributions."

- id: edge_E21_to_C05
  from: E21_external_solver_operator_gap_ladder
  to: C05_pypeec_solver_bridge
  relation: motivates
  strength: medium
  scope: "PyPEEC interface scaffold ready; operator blocked"
  caveat: "PyPEEC operator is scaffold-level interface only; full bridge not exercised."
```

## open_questions.md — new question

```markdown
## OQ09: Can the E21 operator-gap ladder be extended to COMSOL/FastHenry/FEM artifacts?

Status: active, E21 scaffold-level only.

E21 quantifies field-level and decision-level operator gaps among analytic,
centerline, and finite-width operators on canonical geometries. The COMSOL and
FastHenry artifact interfaces are scaffolded with schema validation but no real
external solver data is loaded. This open question is the next critical
step for moving C04 from supported_generated toward supported with external
validation.
```

## update_log.md — new entry

```markdown
## 2026-05-06 - E21 external-solver operator-gap ladder implementation

Claim affected:
- C04_inverse_crime_and_operator_gap
- C10_pdn_kcl_distribution_need
- C05_pypeec_solver_bridge

Change type:
- new evidence package E21 added with operator-gap ladder on canonical geometries
- field-level operator gaps (analytic vs centerline vs finite-width) quantified
- decision-level instability (cross-operator ridge decoder) measured
- COMSOL/FastHenry external artifact interfaces scaffolded with schema validation
- PyPEEC interface scaffold ready (operator blocked: not installed)
- all engineering gates pass (8/8)
- external validation status: blocked

Evidence:
- E21 implements analytic reference, centerline Biot-Savart, and finite-width
  surrogate forward operators on 5-6 canonical geometries (straight wire, loop,
  finite-width trace, via, return path pair, multilayer route).
- Pairwise operator gaps computed with component RMSE, spectral low/high-k
  decomposition, sign/polarity consistency, and divB proxy.
- Decision instability measured via ridge decoder trained on one operator and
  tested on another.
- External artifact interfaces include schema validation and explicit
  blocked/interface status when artifacts are absent.

Metrics:
- case_count: 5 (smoke), 6 (default)
- available_operator_count: 3 (analytic, centerline, finite_width)
- external_solver_artifacts_present: false
- unit_sanity_passed: true
- operator gaps: nonzero and quantified
- decision stress: executed
- all engineering gates: pass

Claim status before:
- C04: supported_generated (E04, E06, E07, E16, E18, E19, E19_2)
- C05: supported_generated (E07)
- C10: supported_generated (E10, E11, E12, E14, E15, E18, E19, E19_2)

Claim status after:
- No status change. E21 adds generated-domain operator-gap evidence with
  explicit external-validation blocked status.

Cannot claim:
- COMSOL/FastHenry/FEM validation — no external artifacts loaded
- PyPEEC is ground-truth real physics
- generated operator agreement proves real CAD/GDS or real QDM/NV validation
- inverse decisions transfer to real hardware

Next required evidence:
- Load COMSOL or FastHenry artifact files for external solver comparison
- Extend operator ladder to PDN/KCL graph-based geometries
- Run PyPEEC full forward pipeline (mesh, solve, field extraction)
- Add multi-height observation support to operator-gap comparison

Files changed:
- `experiments/evidence/E21_external_solver_operator_gap_ladder/`
```

## overclaim_guardrails.md — proposed addition

No new guardrail items needed; existing guardrails 1 (real QDM/NV), 2 (real
CAD/GDS), 3 (PyPEEC ground truth), and 5 (external FEM/FastHenry) already
cover E21 boundaries. Guardrail 31 (Claude worker output is not evidence
before audit) applies.
