# RUN_REPORT - exp07 Real PyPEEC Solver Cross-Validation

## Purpose

Run a true PyPEEC 5.x Python API mesher/solver path on small canonical conductor
geometries and exp03-like route families with cross-section voxel fill, compare
the resulting sensor-plane magnetic field against the in-repository centerline
and finite-width Biot-Savart references, and quantify a small layer-aligned
xy-pitch refinement sweep.

## Backend status

```json
{
  "python_module_available": true,
  "python_module_origin": "D:\\Dev\\uv-cache\\archive-v0\\Zzl01taRLTUbouW5KV4qm\\Lib\\site-packages\\pypeec\\__init__.py",
  "python_package_version": "5.8.0",
  "api_functions_checked": [
    "run_mesher_data",
    "run_mesher_file",
    "run_solver_data",
    "run_solver_file",
    "run_arguments"
  ],
  "api_functions_found": {
    "run_mesher_data": true,
    "run_mesher_file": true,
    "run_solver_data": true,
    "run_solver_file": true,
    "run_arguments": true
  },
  "python_import_error": null,
  "optional_acceleration_packages": {
    "cupy": {
      "available": false,
      "origin": null
    },
    "mkl_fft": {
      "available": false,
      "origin": null
    },
    "pyfftw": {
      "available": false,
      "origin": null
    },
    "pydiso": {
      "available": false,
      "origin": null
    },
    "pyamg": {
      "available": false,
      "origin": null
    }
  }
}
```

Executed backend mode: `real_pypeec_api`.

## Key summary

- cases completed: `400` / `400`
- PyPEEC package version: `5.8.0`
- finite-width reference median gap: `0.0411592`
- PyPEEC-vs-centerline median gap: `0.197034`
- PyPEEC-vs-finite-width median gap: `0.18501`
- scalar-fitted PyPEEC shape median gap: `0.186085`
- max source-current relative error: `9.67108e-14`
- single-via PyPEEC `Bz/Bxy`: `0`
- finite-width/straight voxel ratio: `3`
- exp03-like cases completed: `295` / `295`
- exp03-like scalar-fitted shape median gap: `0.173889`
- PyPEEC distribution expansion counts: `{"H0_sheet_only": 100, "H1_sheet_via": 100, "H2_sheet_return": 100, "H3_sheet_artifact": 100}`
- PyPEEC FFT library: `SciPy`
- max convergence shape delta: `0.20378`
- max finest-step convergence shape delta: `0.134709`
- solver table: `outputs/SOLVER_CROSS_VALIDATION_TABLE.md`
- convergence table: `outputs/VOXEL_CONVERGENCE_TABLE.md`
- all gates passed: `True`

## Acceptance gates

| gate | status |
| --- | --- |
| experiment_outputs_exist | PASS |
| real_pypeec_module_available | PASS |
| real_pypeec_mesher_solver_api_available | PASS |
| real_pypeec_backend_executed_for_all_cases | PASS |
| all_requested_cases_completed | PASS |
| all_pypeec_solutions_ok | PASS |
| pypeec_fields_are_finite | PASS |
| source_current_matches_target | PASS |
| standoff_decay_is_monotone_for_reference | PASS |
| single_via_pypeec_bz_over_bxy_is_bounded | PASS |
| finite_width_gap_is_quantified | PASS |
| finite_width_pypeec_geometry_is_wider | PASS |
| pypeec_raw_gap_is_finite_and_bounded | PASS |
| pypeec_shape_gap_is_finite_and_bounded | PASS |
| voxel_convergence_sweep_completed | PASS |
| voxel_convergence_shape_delta_is_bounded | PASS |
| voxel_convergence_finest_step_is_bounded | PASS |
| exp03_like_pypeec_subset_completed | PASS |
| exp03_like_shape_gap_is_finite_and_bounded | PASS |
| exp03_like_source_current_matches_target | PASS |
| pypeec_exp03_like_mini_dataset_written | PASS |
| pypeec_distribution_targets_are_met | PASS |
| claim_boundary_records_real_pypeec_status | PASS |


## Boundary

This experiment now executes real PyPEEC through `pypeec.run_mesher_data` and
`pypeec.run_solver_data` with canonical cross-section voxel fill and a small
exp03-like route subset. It is still a solver-level cross-validation gate: it
does not claim FastHenry/FEM/QDM, CAD-scale convergence, or real-chip agreement,
and it does not validate the inverse neural model until these fields are
explicitly fed back into exp04.
