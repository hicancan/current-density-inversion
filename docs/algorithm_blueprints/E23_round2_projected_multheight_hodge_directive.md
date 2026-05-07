# E23 Round 2 Directive: Projected Graph-Hodge Basis and Multi-Height OQCI

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e23-graph-hodge`
- previous session: `19e97ba9-2b0d-406e-95f9-f8c5eafb15d4`

## Audit Finding from Round 1

Round 1 produced a useful Graph-Hodge scaffold but did not pass all gates:

```text
dimension reduction = 57x
graph_prior_ambiguity_delta = 0.0
wrong_high_confidence_accept_count = 2
H1_via_defect vs H2_return_bottleneck rel_l2 = 0.007
```

There is also a metrics/reporting inconsistency:

```text
max_kcl_residual = 1.5986
kcl_residual_below_tolerance = true
```

The final report explains that only port+loop blocks are KCL-compatible, while
via/return/gap/residual are building blocks. The metrics must represent this
honestly.

## Round 2 Goal

Turn the Graph-Hodge basis from a structural scaffold into a safer admissible
current-space restriction by:

1. reporting KCL separately by block;
2. adding projected KCL-compatible via/return modes;
3. testing whether multi-height observations reduce the H1/H2 degeneracy.

## Required Changes

Implement only inside:

```text
experiments/evidence/E23_cad_gds_graph_hodge_basis/
```

Do not edit global research graph files.

### 1. Fix KCL Metrics and Gates

Separate:

```text
kcl_residual_port_loop
kcl_residual_raw_blocks
kcl_residual_projected_blocks
```

Gate names must be honest:

```text
port_loop_kcl_below_tolerance
projected_blocks_kcl_below_tolerance
raw_blocks_kcl_reported_not_gated
```

Do not mark `kcl_residual_below_tolerance` true while reporting a global max
above threshold.

### 2. Projected KCL-Compatible Blocks

For via/return block candidates, project raw edge modes onto the affine or
homogeneous KCL-compatible subspace.

For a raw edge vector `v`, compute:

```text
v_proj = argmin ||v_proj - v||_2
subject to D_interior v_proj = 0
```

or, for source/sink via transfer modes:

```text
D v_proj = q_via
```

Report projection residual:

```text
||v_proj - v|| / ||v||
```

Do not silently discard modes whose projection collapses.

### 3. Multi-Height OQCI

Add config support:

```text
heights = [0.35, 0.70, 1.40]  # units consistent with current package
component_mode = Bz or Bxyz
```

Compute OQCI for:

- single height;
- two heights;
- three heights.

Report:

- H1/H2 pairwise distance before/after;
- wrong high-confidence accepts before/after;
- ambiguity rate before/after;
- operator rank before/after;
- claim interval width before/after.

### 4. Breakthrough Gate

Add:

```text
multi_height_reduces_h1_h2_wrong_accepts
```

and:

```text
projected_blocks_kcl_below_tolerance
```

If multi-height still fails, preserve it as a stronger identifiability boundary.

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
- corrected KCL metrics;
- projection residuals;
- multi-height H1/H2 distinguishability;
- whether wrong accepts dropped;
- failure modes;
- cannot_claim;
- next required evidence.

