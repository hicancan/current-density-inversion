# Outputs

Run `src/run_all.py` to generate:

- `metrics.json`
- `RUN_REPORT.md`
- `SOLVER_CROSS_VALIDATION_TABLE.md`
- `VOXEL_CONVERGENCE_TABLE.md`
- `01_case_pypeec_gap_summary.svg`
- `02_standoff_decay.svg`
- `03_voxel_convergence_shape_gap.svg`

The outputs are produced by the real PyPEEC Python API. No proxy backend is used.
The default output set covers ten cases: six canonical solver checks and four
exp03-like connected route-family checks.
