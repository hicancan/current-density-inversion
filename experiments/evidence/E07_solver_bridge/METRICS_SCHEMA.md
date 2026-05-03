# Metrics Schema - exp07

`outputs/metrics.json` records a real PyPEEC API run.

## Top-Level Fields

- `experiment_name`: experiment identifier.
- `pypeec_detection`: Python package detection, installed version, module path,
  and checked public API entry points.
- `backend_mode_executed`: must be `real_pypeec_api`.
- `n_cases_requested`, `n_cases_completed`.
- `sensor_grid`: exported sensor-plane grid metadata.
- `case_metrics`: per-case field comparison and solver metadata.
- `case_metrics.<case>.case`: case names may include deterministic
  `base__vNN` geometry variants.
- `standoff_scan`: reference Biot-Savart standoff sanity scan.
- `summary`: aggregate field gaps and current-normalization checks.
- `summary.pypeec_distribution_expansion`: configured H0/H1/H2/H3 distribution
  target status for the exp08 bridge. The default full run targets 100 cases in
  each of `H0_sheet_only`, `H1_sheet_via`, `H2_sheet_return`, and
  `H3_sheet_artifact`.
- `voxel_convergence_sweep`: layer-aligned xy-pitch sweep records for selected
  canonical cases.
- `pypeec_exp03_like_mini_dataset`: exported exp04-compatible mini dataset
  metadata, including file path, field shape, truth shape, case names, and
  split name.
- `acceptance_gates`: boolean gate results.
- `all_acceptance_gates_passed`: conjunction of all gates.

## Per-Case Metrics

- `center_vs_finite_rel_l2`: finite-width filament reference vs centerline
  Biot-Savart.
- `pypeec_vs_center_rel_l2`: raw PyPEEC field vs centerline reference.
- `pypeec_vs_finite_rel_l2`: raw PyPEEC field vs finite-width reference.
- `pypeec_fit_alpha_to_center`: least-squares scalar that maps PyPEEC to the
  centerline reference.
- `pypeec_centerline_shape_rel_l2`: relative L2 after scalar fitting. This
  isolates spatial/vector-field shape agreement from a global amplitude offset.
- `peak_pypeec_over_center`: peak field magnitude ratio.
- `source_current_a`: source terminal current reported by PyPEEC.
- `source_current_rel_error`: source-current mismatch relative to config.
- `n_voxel_used`: number of PyPEEC voxels used by the case.
- `n_voxel_centerline`: number of centerline voxels before cross-section fill.
- `rasterization`: PyPEEC voxel rasterization mode.
- `solution_ok`, `solver_ok`, `condition_ok`: PyPEEC sweep status.
- `backend_metadata`: voxel shape, domain counts, PyPEEC API calls, and solution
  summary.
- `single_via_pypeec_bz_over_bxy`: single-via diagnostic only.

## Exp03-Like Subset Summary

The `summary` object records:

- `exp03_like_requested_cases`: configured exp03-like route-family cases,
  including deterministic variants in the default run.
- `exp03_like_completed_cases`: subset completed by the real PyPEEC backend.
- `exp03_like_case_count`: completed exp03-like case count.
- `exp03_like_shape_gap_median`: scalar-fitted PyPEEC-vs-centerline median gap
  for the exp03-like subset.
- `exp03_like_max_terminal_current_rel_error`: maximum source-current mismatch
  over the exp03-like subset.

## Output Tables

- `SOLVER_CROSS_VALIDATION_TABLE.md`: per-case real PyPEEC vs reference field
  comparison and source-current checks.
- `VOXEL_CONVERGENCE_TABLE.md`: selected-case xy-pitch refinement table. The
  coarse-to-medium deltas quantify discretization sensitivity; the finest-step
  delta is the acceptance signal for the current small canonical sweep.
- `data/pypeec_exp03_like_mini_dataset.npz`: `B_centerline`, `B_finite`,
  `B_pypeec`, rasterized `truth[J1x,J1y,J2x,J2y,s1]`, case metadata, and
  `split=pypeec_test` for exp04 frozen inference and exp08 graph-bridge
  evaluation.

## Interpretation

This experiment supports a solver-level claim: real PyPEEC can be run and
compared against the internal references on canonical and small exp03-like
geometries, with real cross-section voxel fill, a small refinement sweep, and a
mini dataset export for exp04 frozen inference. It does not by itself validate
FastHenry/FEM/QDM data, CAD-like convergence, or broad inverse-model robustness.
