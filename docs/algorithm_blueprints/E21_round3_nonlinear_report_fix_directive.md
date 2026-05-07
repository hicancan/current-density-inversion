# E21 Round 3 Directive: Mechanism Report Fix and Nonlinear Scorer

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e21-operator-gap`
- previous session: `b13de309-4299-467a-a6e3-0368eda21f3b`

## Audit Finding from Round 2

Metrics contain the new mechanism decision instability and gate:

```text
max_mechanism_instability_ratio = 1.5
decision_instability_ratio_gt_1_25 = true
```

But `outputs/DECISION_INSTABILITY.md` still reports only ridge reconstruction
error ratios and says max ratio is 1.0. The report and metrics are inconsistent.

Also, same-operator mechanism accuracy is low (`0.375`), so instability is
measured near a weak baseline. E21 should add a stronger nonlinear scorer or
template evidence scorer to test whether better in-domain discrimination still
breaks under operator shift.

## Required Changes

Implement only inside:

```text
experiments/evidence/E21_external_solver_operator_gap_ladder/
```

Do not edit global research graph files.

### 1. Report Fix

Update `DECISION_INSTABILITY.md` so it has separate sections:

- ridge reconstruction instability;
- mechanism decision instability;
- confusion matrices;
- false-via and return-confusion rates;
- acceptance gate summary.

Do not let the report say max ratio is 1.0 when mechanism metrics say 1.5.

### 2. Nonlinear or Template Mechanism Scorer

Add one stronger mechanism scorer:

Option A: template evidence scorer:

```text
score_h = min_alpha || y - alpha * template_h ||^2
```

Option B: lightweight nonlinear classifier, CPU only:

- polynomial features over field summary;
- nearest-centroid in spectral feature space;
- random forest only if dependency-free or available.

Prefer dependency-free template/spectral nearest-centroid.

Report:

```text
same_operator_accuracy_template
cross_operator_accuracy_template
template_instability_ratio
template_confusion_matrix
```

### 3. Gate

Add:

```text
template_same_operator_accuracy_ge_0_60
template_cross_operator_drop_ge_0_20
```

If this fails, preserve as limitation.

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Final Report

Report:

- report inconsistency fixed or not;
- template/nonlinear scorer metrics;
- whether gate passed;
- operator shifts that cause mechanism collapse;
- cannot_claim;
- next required evidence.

