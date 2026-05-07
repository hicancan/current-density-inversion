# E23 Round 3 Directive: SVD Nullspace Projection and Multi-State Graph-Hodge OQCI

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e23-graph-hodge`
- previous session: `19e97ba9-2b0d-406e-95f9-f8c5eafb15d4`

## Audit Finding from Round 2

Round 2 strengthened the boundary:

```text
multi-height H1/H2 distance did not improve
operator_rank_1h = operator_rank_2h = operator_rank_3h = 18
wrong_accepts stayed 2
```

It also showed the projected-block KCL implementation is not robust:

```text
kcl_residual_projected_blocks = 0.574
projected_blocks_kcl_below_tolerance = false
```

The next attempt must use a true SVD nullspace basis, not pseudoinverse
projection, and then test multi-state Graph-Hodge OQCI.

## Required Changes

Implement only inside:

```text
experiments/evidence/E23_cad_gds_graph_hodge_basis/
```

Do not edit global research graph files.

### 1. SVD Nullspace Projection

Compute an explicit nullspace basis `N` for `D_interior`:

```text
D_interior N = 0
```

Project raw mode `v`:

```text
v_proj = N (N^T v)
```

For affine source/sink modes, solve a particular current `i0` and add nullspace:

```text
i = i0 + N z
```

Report:

```text
nullspace_dim
projection_retained_energy
collapsed_mode_count
kcl_residual_projected_blocks
```

### 2. Multi-State Graph-Hodge OQCI

Add deterministic excitation states over graph ports/loads:

- baseline state;
- via-sensitive state;
- return-sensitive state;
- differential source/sink swap state.

Compute OQCI for:

- single-state single-height;
- multi-height only;
- multi-state only;
- multi-height + multi-state.

### 3. Breakthrough Gate

Add:

```text
svd_projected_blocks_kcl_below_tolerance
multistate_reduces_h1_h2_wrong_accepts
multistate_increases_h1_h2_distance_ge_0_20
```

If multi-state helps where multi-height failed, this is the strongest current
breakthrough route.

## Required Outputs

Add:

```text
outputs/SVD_NULLSPACE_PROJECTION.md
outputs/MULTISTATE_GRAPH_HODGE_OQCI.md
outputs/H1_H2_BREAKTHROUGH_AUDIT.md
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

- SVD projection residuals;
- projected block KCL;
- H1/H2 distance under single/multi-height/multi-state;
- wrong accepts under each protocol;
- whether multi-state broke the degeneracy;
- failure modes;
- cannot_claim;
- next required evidence.

