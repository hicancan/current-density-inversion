# E20 Round 2 Directive: Epsilon Sweep and Multi-State Active OQCI

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e20-active-oqci`
- previous session: `aa6a240a-8b3b-46fc-9229-1123e36dc61b`

## Audit Finding from Round 1

Round 1 passed engineering gates but did not break ambiguity:

```text
baseline_ambiguity_rate = 1.0
best_ambiguity_rate = 1.0
claim_interval_width_reduction = 0.0
best_candidate = add_h1.6_Bz
best_utility < 0 for every candidate
```

This is useful negative evidence, but it is not yet a breakthrough. The worker
identified two likely missing levers:

1. epsilon sensitivity: E19.2 had partial discrimination near 1.0 sigma;
2. multi-state excitation: height/component alone may not change the relevant
   hypothesis subspaces.

## Round 2 Goal

Add active OQCI over:

```text
measurement = height x component x epsilon_policy x excitation_state
```

The scientific question is:

```text
Can calibrated epsilon and multi-state excitation shrink claim intervals where
height/component alone failed?
```

## Required Changes

Implement only inside:

```text
experiments/evidence/E20_active_oqci_measurement_design/
```

Do not edit global research graph files.

### 1. Epsilon Sweep

Add config-driven epsilon multipliers:

```text
epsilon_multipliers = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
```

For each candidate measurement, compute:

- nonempty rate;
- ambiguity rate;
- mean interval width;
- empty rate;
- wrong high-confidence accept count;
- best utility.

Add outputs:

```text
outputs/EPSILON_SWEEP.md
outputs/EPSILON_CANDIDATE_MATRIX.md
```

### 2. Multi-State Candidate Family

Implement deterministic synthetic multi-state excitation as a generated-domain
observation design stress. Do not claim hardware feasibility.

Minimum acceptable implementation:

- state 0: baseline current coefficients;
- state 1: via-sensitive perturbation or alternate port/load pattern;
- state 2: return-path-sensitive perturbation;
- state 3: gap/residual-sensitive perturbation.

For each state, build a stacked operator or stacked observation:

```text
F_E = [F_height_component_state0, F_height_component_state1, ...]
```

Candidate names:

```text
add_state2_Bz
add_state2_Bxyz
add_state4_Bz
add_state4_Bxyz
add_h1.6_state2_Bz
add_h1.6_state4_Bxyz
```

### 3. Utility Must Reward Honest Partial Discrimination

Do not optimize only the 2.5 sigma primary epsilon. Compute robust utility over
epsilon policies:

```text
utility = median_over_epsilons(
  interval_width_reduction
  + near_null_reduction
  + pairwise_distance_gain
  - wrong_accept_penalty
  - cost
)
```

Also report the best candidate at each epsilon.

### 4. Breakthrough Gate

Add a new scientific gate:

```text
any_epsilon_any_candidate_interval_width_reduction_ge_0_20
```

If this fails, preserve as a stronger negative result:

```text
tested height/component/multi-state candidates still do not shrink OQCI
ambiguity under the generated basis family.
```

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Required Final Report

Report:

- files changed;
- commands run;
- whether epsilon sweep changed the conclusion;
- whether multi-state changed the conclusion;
- best candidate by epsilon;
- failure modes;
- cannot_claim;
- next required evidence.

