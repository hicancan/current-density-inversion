# Reproduce exp07

From the repository root:

```bash
uv run --with numpy --with pypeec python experiments/evidence/E07_solver_bridge/src/run_all.py
```

Fast smoke run:

```bash
uv run --with numpy --with pypeec python experiments/evidence/E07_solver_bridge/src/run_all.py --quick
```

Tests:

```bash
uv run --with numpy --with pypeec --with pytest pytest -q experiments/evidence/E07_solver_bridge/tests
```

Expected report outputs:

- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `outputs/SOLVER_CROSS_VALIDATION_TABLE.md`
- `outputs/VOXEL_CONVERGENCE_TABLE.md`
- `data/exp07_fields.npz`
- `data/pypeec_exp03_like_mini_dataset.npz`
- `data/pypeec_case_payloads/`

`pypeec` is required. The experiment should not be run or interpreted in a proxy
mode. The default run includes 400 real PyPEEC cases: canonical sanity cases plus
deterministic variants that meet the exp08 bridge target of 100 cases each for
`H0_sheet_only`, `H1_sheet_via`, `H2_sheet_return`, and `H3_sheet_artifact`.
There are 295 exp03-like route-family cases, including explicit bend/corner
artifact cases. The run also performs a small layer-aligned xy-pitch convergence
sweep for `straight_trace`, `via_pair`, `two_layer_route_with_via`,
`dense_via_background`, and `no_via_background`. The mini dataset is consumed by
exp04 as a frozen no-retraining PyPEEC stress artifact and by exp08 as a balanced
H0/H1/H2/H3 graph-bridge distribution.

