# E21 Round 5 Directive: Multi-Basis Operator-Gap Certificate

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e21-operator-gap`
- previous session: `b13de309-4299-467a-a6e3-0368eda21f3b`

## Mathematical Objective

E21 has repeatedly shown that weak mechanism scorers fail under operator gap.
Round 5 should not chase another fragile classifier. It should quantify the
operator-gap boundary with a stronger subspace evidence model.

For each mechanism hypothesis `h`, build a low-rank observation dictionary:

```math
A_h = [q_{h,1},\ldots,q_{h,k_h}],
\qquad Q_h^T Q_h = I.
```

Score observation `y` by regularized evidence:

```math
d_h(y)^2
=
\min_x
\|W(y-Q_hx)\|_2^2
+\lambda\|x\|_2^2 .
```

The closed-form solution is:

```math
\hat{x}_h
=
(Q_h^T W^T W Q_h+\lambda I)^{-1}
Q_h^T W^T W y.
```

Mechanism prediction:

```math
\hat{h}(y)=\arg\min_h d_h(y)^2.
```

Margin:

```math
m(y)=d_{(2)}(y)^2-d_{(1)}(y)^2.
```

Operator shift from training operator `A` to test operator `A+\Delta A` creates
an intra-hypothesis manifold shift:

```math
s_h
=
\sup_{i\in\mathcal{I}_h,\|i\|\le R_h}
\|W\Delta A\,i\|_2 .
```

Inter-class separation is:

```math
\delta_{hg}
=
\inf_{u\in\mathcal{S}_h,v\in\mathcal{S}_g}
\|W(u-v)\|_2 .
```

No classifier using these observations can be stable if:

```math
\max_h s_h
\gtrsim
{1\over 2}\min_{h\ne g}\delta_{hg}.
```

Round 5 should produce this certificate. A negative result is valuable if it
proves the operator gap is larger than the mechanism margin.

## Required Scope

Implement only inside:

```text
experiments/evidence/E21_external_solver_operator_gap_ladder/
```

Do not edit global research graph files.

## Required Changes

### 1. Multi-Basis Evidence Scorer

Replace scalar class templates with low-rank dictionaries. Acceptable
dependency-light construction:

```text
center class observations
SVD/PCA per class
keep k components by energy threshold or fixed k in {1,2,3,5}
ridge residual evidence for each class
```

Report:

```text
k_components
energy_retained
same_operator_accuracy_multibasis
cross_operator_accuracy_multibasis
multibasis_cross_operator_drop
multibasis_confusion_matrix_same
multibasis_confusion_matrix_cross
```

### 2. Margin-Shift Certificate

Compute:

```text
interclass_delta_min
interclass_delta_by_pair
operator_shift_radius_by_hypothesis
operator_shift_radius_max
gap_to_margin_ratio = operator_shift_radius_max / max(interclass_delta_min, eps)
stable_classification_possible_by_margin
```

The certificate should explicitly answer:

```text
Is the operator shift smaller than half the inter-class margin?
```

### 3. Refusal Policy from Margin Certificate

Set refusal threshold from calibration margins:

```math
m(y) \ge t_\alpha,
```

where `t_alpha` is a calibration quantile. Report:

```text
accepted_rate_same
accepted_accuracy_same
accepted_rate_cross
accepted_accuracy_cross
wrong_accept_rate_cross
refusal_rate_cross
```

### 4. External Solver Boundary

Keep PyPEEC/FastHenry/COMSOL status explicit:

```text
external_solver_import_status
external_solver_field_pipeline_status
external_solver_artifact_count
external_solver_used_in_metrics
```

If no field pipeline completes, set:

```text
external_solver_used_in_metrics = false
```

### 5. Breakthrough or Boundary Gates

Add:

```text
multibasis_same_operator_accuracy_ge_0_60
multibasis_cross_operator_drop_ge_0_20
operator_shift_less_than_half_margin
margin_refusal_wrong_accept_rate_le_0_10
margin_refusal_accepted_accuracy_ge_0_80
external_solver_used_in_metrics
```

If the scorer still fails, preserve the negative theorem boundary:

```text
operator_gap_exceeds_mechanism_margin
```

## Required Outputs

Add:

```text
outputs/MULTIBASIS_EVIDENCE_SCORER_AUDIT.md
outputs/MARGIN_SHIFT_CERTIFICATE.md
outputs/ROUND5_OPERATOR_GAP_BOUNDARY_AUDIT.md
```

Update metrics JSON with all Round 5 keys.

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Final Report

Report:

- multi-basis scorer metrics;
- margin-shift certificate;
- whether operator gap is below or above mechanism margin;
- refusal tradeoff;
- external solver status;
- all Round 5 gates;
- failure modes;
- cannot_claim;
- next required evidence.

