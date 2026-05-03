# exp07 - Real PyPEEC Solver Cross-Validation

## Role

`exp07` is a solver-level cross-validation gate. It does not train an inverse
model. It verifies that the repository can drive the real PyPEEC Python API,
generate canonical conductor voxel models with conductor cross-section fill,
solve them, export sensor-plane magnetic fields, and compare those fields
against the internal Biot-Savart references.

## Backend

There is only one accepted backend:

```text
pypeec.run_mesher_data
pypeec.run_solver_data
```

No proxy, fallback, or external fake PyPEEC path is allowed. If PyPEEC is not
installed, exp07 should fail rather than silently downgrade.

## Canonical and exp03-like geometries

The default run now contains 400 cases:

- six canonical solver sanity cases;
- deterministic `trace_with_return_path`, `no_via_background`,
  `two_layer_route_with_via`, `multi_via_route`, `dense_via_background`, and
  `bend_artifact_trace` variants;
- a balanced H0/H1/H2/H3 bridge distribution with 100 real PyPEEC solves each
  for `H0_sheet_only`, `H1_sheet_via`, `H2_sheet_return`, and
  `H3_sheet_artifact`;
- 295 exp03-like connected Manhattan route-family cases, including explicit
  bend/corner artifact cases for exp08 system-identification stress.

Variant names use the `base__vNN` convention and are deterministic geometric
translations/mirrors/scale changes, not random samples. They make the PyPEEC
mini stress less dependent on a single hand-picked geometry while keeping every
case auditable. These are still toy geometries, not CAD/Gerber imports. Each
case writes the exact PyPEEC
geometry/problem/tolerance JSON used for the run under
`data/pypeec_case_payloads/`.

The PyPEEC voxel model now uses a swept cross-section rasterization rather than
a centerline-only skeleton. The finite-width trace must therefore use more
PyPEEC voxels than the straight trace. A small layer-aligned xy-pitch sweep
(`60`, `40`, `30`, `20` um at fixed `25` um z pitch) is also run for
`straight_trace`, `via_pair`, `two_layer_route_with_via`,
`dense_via_background`, and `no_via_background`.

## Outputs

```text
outputs/metrics.json
outputs/RUN_REPORT.md
outputs/SOLVER_CROSS_VALIDATION_TABLE.md
outputs/VOXEL_CONVERGENCE_TABLE.md
outputs/01_case_pypeec_gap_summary.svg
outputs/02_standoff_decay.svg
outputs/03_voxel_convergence_shape_gap.svg
data/exp07_fields.npz
data/pypeec_exp03_like_mini_dataset.npz
data/pypeec_case_payloads/*/*_geometry.json
data/pypeec_case_payloads/*/*_problem.json
data/pypeec_case_payloads/*/*_tolerance.json
data/pypeec_case_payloads/*/*_solution_summary.json
```

`pypeec_exp03_like_mini_dataset.npz` is the exp04-compatible frozen stress
artifact. It contains `B_centerline`, `B_finite`, `B_pypeec`, rasterized
`truth[J1x,J1y,J2x,J2y,s1]`, case metadata, and `split=pypeec_test`. It is not
a training or calibration split.

## Solver Acceleration Boundary

PyPEEC 5.x exposes multiple FFT backends in its tolerance schema, including a
`CuPy` backend for GPU FFTs. The default repository configuration uses
`pypeec.solver.fft_library = "SciPy"` because it is the most portable backend and
because the current Windows `uv` PyPEEC environment does not have `cupy`
installed. If `fft_library` is changed to `CuPy`, the adapter checks for CuPy and
fails loudly when it is missing instead of silently pretending to use the GPU.
Current full-run metadata therefore represents CPU/SciPy PyPEEC solves unless a
CuPy-enabled PyPEEC environment is installed explicitly.

## Current Result Boundary

Supported:

- real PyPEEC 5.x API is installed and callable;
- `run_mesher_data` and `run_solver_data` execute for all 400 configured cases;
- terminal source current matches the configured current;
- finite-width PyPEEC geometry uses more voxels than the straight trace;
- 295 exp03-like route-family cases complete as real PyPEEC solves;
- H0/H1/H2/H3 graph-bridge hypothesis classes each have 100 real PyPEEC cases;
- a small voxel pitch sweep completes and the finest-step field-shape delta is
  bounded;
- sensor-plane `B = mu0 H_p` fields are finite and shape-compatible;
- PyPEEC fields are compared against centerline and finite-width Biot-Savart
  references with both raw relative L2 and scalar-fitted shape gaps.
- an exp04-compatible mini PyPEEC dataset is exported for no-retraining frozen
  inference stress in exp04.

Not supported:

- FastHenry, FEM, COMSOL, Ansys, or QDM agreement;
- real PCB/FPC/chip validation;
- full 3D voxel convergence over CAD-like geometries;
- broad inverse-model robustness on a full PyPEEC-generated exp03 distribution.

## Run

```bash
uv run --with numpy --with pypeec python experiments/evidence/E07_solver_bridge/src/run_all.py
```

Quick smoke:

```bash
uv run --with numpy --with pypeec python experiments/evidence/E07_solver_bridge/src/run_all.py --quick
```

Tests:

```bash
uv run --with numpy --with pypeec --with pytest pytest -q experiments/evidence/E07_solver_bridge/tests
```

## PyPEEC References

- Official API documentation: https://pypeec.otvam.ch/content/api.html
- Repository: https://github.com/otvam/pypeec
- PyPI package: https://pypi.org/project/pypeec/

