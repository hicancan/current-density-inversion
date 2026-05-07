# E21 Round 2 Directive: Stronger Operator Perturbation and PyPEEC Attempt

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e21-operator-gap`
- previous session: `b13de309-4299-467a-a6e3-0368eda21f3b`

## Audit Finding from Round 1

Round 1 quantified field gaps but decision instability remained trivial:

```text
cross/same error ratio ~= 1.0
external_validation_status = blocked
pypeec_status = unavailable
```

The limitation is clear: finite-width was only a mild perturbation and the ridge
decoder absorbed it. E21 must now test stronger operator changes.

## Round 2 Goal

Determine whether conclusion instability appears when the forward operator
changes in a way that cannot be absorbed by a simple ridge decoder.

## Required Changes

Implement only inside:

```text
experiments/evidence/E21_external_solver_operator_gap_ladder/
```

Do not edit global research graph files.

### 1. PyPEEC Attempt

Update `requirements.txt` or command guidance so the package can attempt:

```powershell
uv run --with numpy --with pypeec ...
```

If PyPEEC cannot run, preserve a blocked result with the exact error. Do not
fake PyPEEC validation.

Minimum acceptable:

- detect whether PyPEEC imports;
- if available, run one very small generated conductor or call a smoke adapter;
- if unavailable or API mismatch, write `pypeec_status` with error and keep
  gates honest.

### 2. Strong Finite-Width / Return-Path Perturbation

Add at least one stronger generated-domain operator perturbation:

- shifted return path;
- missing return path;
- finite-width trace with asymmetric current distribution;
- layer-depth perturbation large enough to change decision;
- background/registration model-gap operator.

Candidate operator names:

```text
return_path_surrogate
missing_return_surrogate
registration_gap_surrogate
deep_layer_shift_surrogate
```

### 3. Decision Instability Must Use Mechanism Claims

Current decision instability can be too forgiving if it only reconstructs fields
or ridge coefficients. Add mechanism-level decision comparisons:

```text
H0_no_via vs H1_via vs H2_model_gap vs H3_return_path
```

Report:

- same-operator mechanism accuracy;
- cross-operator mechanism accuracy;
- cross/same accuracy ratio;
- confusion matrix;
- false via rate under no-via;
- return-path confusion rate.

### 4. Breakthrough Gate

Add:

```text
decision_instability_ratio_gt_1_25
```

If this fails, preserve a limitation explaining why the tested perturbations are
still too weak.

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

If attempting PyPEEC separately:

```powershell
uv run --with numpy --with pypeec python src/run_all.py --config configs/smoke.json --out outputs_pypeec_smoke
```

## Required Final Report

Report:

- files changed;
- commands run;
- PyPEEC availability/error;
- strongest operator gap;
- mechanism decision instability;
- whether the new gate passed;
- failure modes;
- cannot_claim;
- next required evidence.

