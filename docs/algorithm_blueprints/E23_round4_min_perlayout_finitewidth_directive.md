# E23 Round 4 Directive: Per-Layout Minimum Gain and Finite-Width Stress

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e23-graph-hodge`
- previous session: `19e97ba9-2b0d-406e-95f9-f8c5eafb15d4`

## Audit Finding from Round 3

Round 3 produced the first credible generated-domain breakthrough signal:

```text
SVD-projected Graph-Hodge modes satisfy KCL to numerical tolerance.
Multi-state excitation increases H1/H2 separation where multi-height alone did not.
H1/H2 wrong accepts were eliminated in the audited hard pair.
```

But this is not yet a stable breakthrough. The current report can still hide
failure modes because it emphasizes aggregate or best-case distances. The next
audit must answer the harder question:

```text
Does selective multi-state Graph-Hodge OQCI break the hardest H1/H2 ambiguity
per layout, under plausible finite-width/operator perturbation?
```

## Required Scope

Implement only inside:

```text
experiments/evidence/E23_cad_gds_graph_hodge_basis/
```

Do not edit global research graph files.

Do not claim real CAD/GDS, real QDM/NV, or external-solver validation.

## Required Changes

### 1. Per-Layout Hard-Case Audit

Replace any single aggregate H1/H2 summary with a per-layout table. For every
layout/case, report:

```text
layout_id
layout_family
h1_h2_distance_1state_1height
h1_h2_distance_multiheight_only
h1_h2_distance_multistate_only
h1_h2_distance_multistate_multiheight
h1_h2_gain_multistate_vs_1state
h1_h2_wrong_accept_1state_1height
h1_h2_wrong_accept_multiheight_only
h1_h2_wrong_accept_multistate_only
h1_h2_wrong_accept_multistate_multiheight
truth_hypothesis
accepted_hypotheses_by_protocol
```

Add aggregate metrics that cannot be satisfied by a single easy layout:

```text
h1_h2_distance_min_1state_1height
h1_h2_distance_min_multiheight_only
h1_h2_distance_min_multistate_only
h1_h2_distance_min_multistate_multiheight
h1_h2_gain_min_multistate_vs_1state
h1_h2_wrong_accept_count_by_protocol
h1_h2_wrong_accept_rate_by_protocol
hardcase_layout_id
hardcase_gain_multistate_vs_1state
```

The breakthrough signal survives only if the hardest layout improves.

### 2. Finite-Width and Operator-Gap Stress

Add a deterministic operator-stress ladder:

```text
centerline_operator
finite_width_surrogate_operator
registration_gap_surrogate_operator
deep_layer_shift_surrogate_operator
```

Keep the surrogate simple and dependency-light if needed. The purpose is not a
perfect field solver; it is to test whether the signal collapses under
plausible forward-model mismatch.

For each operator, compute the same per-layout H1/H2 metrics. Report:

```text
operator_name
h1_h2_distance_min_multistate_multiheight
h1_h2_gain_min_multistate_vs_1state
h1_h2_wrong_accept_rate_multistate_multiheight
accepted_set_empty_rate
truth_missing_rate
```

If finite-width or registration stress erases the gain, preserve that as the
main failure mode.

### 3. Hardware-Feasible Multi-State Audit

Separate excitation states into:

```text
port_feasible_states
ideal_internal_states
```

Report the multi-state benefit for both. A real path to chip reverse analysis
needs port-feasible states; ideal internal states can remain a mathematical
upper bound only.

Metrics:

```text
port_feasible_state_count
ideal_internal_state_count
h1_h2_gain_min_port_feasible
h1_h2_gain_min_ideal_internal
port_feasible_beats_1state
ideal_internal_upper_bound_only
```

### 4. Breakthrough Gates

Add these gates:

```text
svd_projected_blocks_kcl_below_tolerance
hardcase_multistate_h1_h2_distance_gain_ge_0_20
hardcase_h1_h2_wrong_accept_eliminated
finite_width_hardcase_gain_ge_0_10
finite_width_h1_h2_wrong_accept_rate_le_0_10
port_feasible_multistate_gain_ge_0_10
truth_missing_rate_le_0_10
accepted_set_empty_rate_le_0_10
```

Round 4 can be called a generated-domain robust signal only if all gates pass.
It still cannot upgrade a real-data claim.

## Required Outputs

Add:

```text
outputs/PER_LAYOUT_H1_H2_AUDIT.md
outputs/FINITE_WIDTH_BREAKTHROUGH_STRESS.md
outputs/PORT_FEASIBLE_MULTISTATE_AUDIT.md
outputs/ROUND4_BREAKTHROUGH_GATE_AUDIT.md
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

- per-layout minimum H1/H2 gains;
- whether the hardest H1/H2 layout is fixed;
- finite-width/registration/deep-layer stress results;
- port-feasible versus ideal-internal multi-state results;
- all breakthrough gates;
- failure modes;
- cannot_claim;
- next required evidence.

