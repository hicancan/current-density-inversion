# E20 Round 3 Directive: Truth Coverage for Multi-State OQCI Signal

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e20-active-oqci`
- previous session: `aa6a240a-8b3b-46fc-9229-1123e36dc61b`

## Audit Finding from Round 2

Round 2 found a possible signal:

```text
add_state2_Bz at epsilon=1.0: interval_width = 0.0, ambiguity_rate = 0.0
add_h1.6_state4_Bxyz at epsilon=1.5: interval_width = 0.0417
```

But the report also warned about empty-set discrimination. The current metrics
do not prove whether singleton consistent sets contain the true hypothesis.
This cannot be called a breakthrough until coverage and correctness are
audited.

## Round 3 Goal

Separate four cases:

1. empty consistent set;
2. singleton correct;
3. singleton wrong;
4. multiple consistent hypotheses.

The scientific question is:

```text
Does multi-state active OQCI produce nonempty, singleton, truth-containing
consistent sets at any epsilon/candidate combination?
```

## Required Metrics

For every candidate and every epsilon multiplier, compute:

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

Definitions:

```text
valid_disambiguation_rate =
fraction of all cases where consistent set is singleton and equals truth.

accepted_accuracy =
singleton_correct / max(singleton_count, 1)

truth_in_consistent_set_rate =
fraction of all cases where truth hypothesis is in the consistent set.
```

Do not reward empty sets as reduced ambiguity.

## Utility Revision

Replace or augment robust utility with:

```text
utility_valid =
  valid_disambiguation_rate
+ 0.5 * truth_in_consistent_set_rate
- 2.0 * singleton_wrong_rate
- 1.0 * empty_rate
- measurement_cost
```

The best candidate should be selected by `utility_valid`, not interval width
alone.

## Breakthrough Gate

Add:

```text
valid_disambiguation_rate_ge_0_50
truth_in_consistent_set_rate_ge_0_90
singleton_wrong_rate_eq_0
empty_rate_le_0_10
```

A real generated-domain breakthrough requires all four gates for at least one
candidate/epsilon pair.

If only weak gates pass, preserve as "promising but not breakthrough."

## Scale Check

Run a larger default if feasible:

```text
grid_size >= 10
case_count >= 36
```

If runtime blocks this, preserve current scale and state the limitation.

## Required Outputs

Add:

```text
outputs/TRUTH_COVERAGE_AUDIT.md
outputs/VALID_DISAMBIGUATION_MATRIX.md
outputs/BREAKTHROUGH_GATE_AUDIT.md
```

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Final Report

Report:

- whether `add_state2_Bz` at epsilon=1.0 is empty-set, singleton-correct, or
  singleton-wrong;
- best candidate by valid-disambiguation utility;
- coverage/risk metrics;
- whether breakthrough gates passed;
- failure modes;
- cannot_claim;
- next required evidence.

