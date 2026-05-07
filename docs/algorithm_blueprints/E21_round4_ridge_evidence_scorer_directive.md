# E21 Round 4 Directive: Ridge Evidence Scorer Under Operator Gap

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e21-operator-gap`
- previous session: `b13de309-4299-467a-a6e3-0368eda21f3b`

## Audit Finding from Round 3

Round 3 fixed the reporting inconsistency and added a dependency-free template
scorer, but the in-domain baseline remained weak:

```text
same-operator template accuracy was below random-useful levels
cross-operator collapse therefore did not establish a strong algorithmic route
```

The next attempt should use a better hypothesis evidence score before judging
operator-gap instability:

```text
For each mechanism hypothesis, fit a regularized field template dictionary and
score evidence by penalized residual plus uncertainty margin.
```

## Required Scope

Implement only inside:

```text
experiments/evidence/E21_external_solver_operator_gap_ladder/
```

Do not edit global research graph files.

Do not claim PyPEEC or external-solver validation unless the full external
field-generation pipeline runs and outputs are audited.

## Required Changes

### 1. Ridge Evidence Scorer

For each mechanism hypothesis `h`, build a small template dictionary `A_h` and
score an observation `y` with:

```text
score_h = min_x ||W (y - A_h x)||_2^2 + lambda ||x||_2^2 + complexity_penalty_h
```

Use a deterministic lambda grid:

```text
lambda in [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]
```

Report:

```text
ridge_evidence_best_lambda
same_operator_accuracy_ridge_evidence
cross_operator_accuracy_ridge_evidence
ridge_evidence_instability_ratio
ridge_evidence_confusion_matrix_same
ridge_evidence_confusion_matrix_cross
ridge_evidence_false_via_rate
ridge_evidence_return_confusion_rate
```

### 2. Margin and Refusal Audit

Add a margin-based refusal policy:

```text
margin = score_second_best - score_best
accept if margin >= margin_threshold
```

Scan deterministic thresholds from calibration split margins. Report:

```text
accepted_rate_same
accepted_accuracy_same
accepted_rate_cross
accepted_accuracy_cross
wrong_accept_rate_cross
refusal_rate_cross
```

This is essential because a real reverse-analysis workflow can refuse
underdetermined mechanism calls.

### 3. Operator-Gap Ladder

Evaluate at least:

```text
analytic_centerline
finite_width_surrogate
missing_return_surrogate
registration_gap_surrogate
deep_layer_shift_surrogate
```

If PyPEEC imports but cannot produce fields, preserve the exact API blocker in
the report and keep PyPEEC out of the evidence claim.

### 4. Breakthrough Gates

Add:

```text
ridge_same_operator_accuracy_ge_0_60
ridge_cross_operator_drop_ge_0_20
ridge_wrong_accept_rate_cross_le_0_10_at_refusal
ridge_accepted_accuracy_cross_ge_0_80_at_refusal
pyquant_external_solver_pipeline_completed
```

The last gate can be false; it is a hard boundary marker.

## Required Outputs

Add:

```text
outputs/RIDGE_EVIDENCE_SCORER_AUDIT.md
outputs/MARGIN_REFUSAL_OPERATOR_GAP_AUDIT.md
outputs/ROUND4_OPERATOR_GAP_GATE_AUDIT.md
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

- ridge evidence scorer accuracy and confusion matrices;
- margin/refusal tradeoff under operator gap;
- which operator shifts still break mechanism identification;
- PyPEEC/external-solver status;
- all breakthrough gates;
- failure modes;
- cannot_claim;
- next required evidence.

