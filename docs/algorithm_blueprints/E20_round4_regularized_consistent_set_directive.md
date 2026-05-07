# E20 Round 4 Directive: Regularized Consistent Sets and Honest Calibration

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e20-active-oqci`
- previous session: `aa6a240a-8b3b-46fc-9229-1123e36dc61b`

## Audit Finding from Round 3

Round 3 showed that the apparent ambiguity collapse was mostly empty-set
discrimination:

```text
best valid_disambiguation_rate = 0.111
no candidate passed truth coverage, singleton correctness, and low empty rate
```

This means the raw least-squares residual model is too flexible or too poorly
calibrated to produce reliable consistent sets. The next attempt should test a
first-principles fix:

```text
Use regularized/reduced hypothesis fitting so the consistent set measures
physically admissible current explanations, not overfit residual degrees of
freedom.
```

## Required Scope

Implement only inside:

```text
experiments/evidence/E20_active_oqci_measurement_design/
```

Do not edit global research graph files.

Do not treat generated-domain results as real QDM/NV or real-chip validation.

## Required Changes

### 1. Regularized Hypothesis Fitting

Add at least two fitting modes:

```text
ols_baseline
ridge_regularized
reduced_basis_ridge
```

For ridge, scan a deterministic lambda grid:

```text
lambda in [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]
```

For reduced-basis ridge, restrict each hypothesis to a compact physically
motivated basis. Acceptable examples:

```text
source_sink_mode
loop_mode
via_mode
return_mode
low_order_smooth_modes
```

Report:

```text
fit_mode
lambda
effective_dof
residual_norm_true
residual_norm_nearest_wrong
residual_margin_true_vs_wrong
```

### 2. Honest Epsilon Calibration

Do not pick epsilon from best disambiguation. Add calibration based only on
truth residual distribution for the generated calibration split:

```text
epsilon_quantile_90
epsilon_quantile_95
epsilon_quantile_99
```

Then evaluate on a separate generated evaluation split. If the current code has
no split, add deterministic split by case index.

Report:

```text
calibration_case_count
evaluation_case_count
epsilon_source
calibration_truth_coverage
evaluation_truth_coverage
```

### 3. Truth-Coverage Metrics

Preserve all Round 3 metrics:

```text
nonempty_rate
empty_rate
singleton_rate
singleton_correct_rate
singleton_wrong_rate
truth_in_consistent_set_rate
truth_missing_rate
multi_consistent_rate
mean_consistent_set_size
accepted_accuracy
accepted_risk
valid_disambiguation_rate
```

Add:

```text
best_regularized_valid_disambiguation_rate
best_regularized_truth_in_consistent_set_rate
best_regularized_singleton_wrong_rate
best_regularized_empty_rate
regularization_beats_ols
```

### 4. Breakthrough Gates

Add:

```text
regularized_valid_disambiguation_rate_ge_0_50
regularized_truth_in_consistent_set_rate_ge_0_90
regularized_singleton_wrong_rate_eq_0
regularized_empty_rate_le_0_10
regularization_beats_ols_by_0_20
```

If these fail, this route remains a boundary result, not a breakthrough.

## Required Outputs

Add:

```text
outputs/REGULARIZED_CONSISTENT_SET_AUDIT.md
outputs/EPSILON_CALIBRATION_AUDIT.md
outputs/REGULARIZATION_BREAKTHROUGH_GATE_AUDIT.md
```

Update metrics JSON with the required metric keys.

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Final Report

Report:

- best OLS versus ridge versus reduced-basis ridge metrics;
- calibrated epsilon values and split discipline;
- whether empty-set discrimination was reduced;
- whether truth coverage survives on evaluation split;
- all breakthrough gates;
- failure modes;
- cannot_claim;
- next required evidence.

