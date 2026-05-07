# Pad-Pitch Schur Phase Diagram

The table reports exact Schur reachability ratios. Because these ratios are
operator norms over the accessible pad set, a low value is a pad-geometry
barrier, not a failed optimizer.

| design | category | pads | min eta | mean eta | max nearest top-pad distance |
|---|---|---:|---:|---:|---:|
| perimeter_top_bottom | boundary_control | 88 | 2.48821324e-09 | 1.15502788e-07 | 5 |
| top_full_surface | surface_upper_bound | 144 | 0.4767196129 | 0.6062087878 | 0 |
| top_candidate_patch_radius_0 | local_patch | 5 | 0.4767196129 | 0.6062087878 | 0 |
| top_bottom_candidate_patch_radius_0 | top_bottom_local_patch | 9 | 0.9534392258 | 0.9596257419 | 0 |
| nearest_top_grid_stride_1_offset_0_0 | nearest_regular_grid_pads | 5 | 0.4767196129 | 0.6062087878 | 0 |
| top_grid_stride_1_offset_0_0 | regular_grid_all_pads | 144 | 0.4767196129 | 0.6062087878 | 0 |
| nearest_top_grid_stride_2_offset_1_1 | nearest_regular_grid_pads | 5 | 0.0003372396621 | 0.1568913008 | 1 |
| top_grid_stride_2_offset_1_0 | regular_grid_all_pads | 37 | 0.0003372396628 | 0.1568913008 | 1 |
| nearest_top_grid_stride_3_offset_2_2 | nearest_regular_grid_pads | 2 | 0.0003372396621 | 0.1568913008 | 1 |
| top_grid_stride_3_offset_2_1 | regular_grid_all_pads | 17 | 0.0003372396628 | 0.1568913008 | 1 |
| nearest_top_grid_stride_4_offset_2_2 | nearest_regular_grid_pads | 5 | 3.703218498e-07 | 0.0001042212174 | 2 |
| top_grid_stride_4_offset_1_0 | regular_grid_all_pads | 10 | 0.0003372396628 | 0.1568913008 | 1 |
| nearest_top_grid_stride_5_offset_1_1 | nearest_regular_grid_pads | 2 | 3.703218314e-07 | 0.0001042212174 | 2 |
| top_grid_stride_5_offset_0_4 | regular_grid_all_pads | 7 | 0.0003372396628 | 0.1568913008 | 1 |
| top_grid_stride_6_offset_1_1 | regular_grid_all_pads | 5 | 4.754241203e-10 | 1.195834402e-07 | 3 |
| top_grid_stride_6_offset_5_4 | regular_grid_all_pads | 5 | 0.0003372396628 | 0.1568913008 | 1 |

## By Stride

```json
{
  "stride_1": {
    "worst_design_id": "nearest_top_grid_stride_1_offset_0_0",
    "worst_min_ratio": 0.47671961290842524,
    "worst_mean_ratio": 0.6062087877949888,
    "best_design_id": "top_grid_stride_1_offset_0_0",
    "best_min_ratio": 0.47671961290941633,
    "best_mean_ratio": 0.6062087877952278,
    "design_count": 2
  },
  "stride_2": {
    "worst_design_id": "nearest_top_grid_stride_2_offset_1_1",
    "worst_min_ratio": 0.00033723966209300615,
    "worst_mean_ratio": 0.15689130082956335,
    "best_design_id": "top_grid_stride_2_offset_1_0",
    "best_min_ratio": 0.00033723966281265527,
    "best_mean_ratio": 0.15689130082979746,
    "design_count": 8
  },
  "stride_3": {
    "worst_design_id": "nearest_top_grid_stride_3_offset_2_2",
    "worst_min_ratio": 0.0003372396620872536,
    "worst_mean_ratio": 0.1568913008295537,
    "best_design_id": "top_grid_stride_3_offset_2_1",
    "best_min_ratio": 0.0003372396628073341,
    "best_mean_ratio": 0.15689130082979152,
    "design_count": 18
  },
  "stride_4": {
    "worst_design_id": "nearest_top_grid_stride_4_offset_2_2",
    "worst_min_ratio": 3.703218498499214e-07,
    "worst_mean_ratio": 0.00010422121741625898,
    "best_design_id": "top_grid_stride_4_offset_1_0",
    "best_min_ratio": 0.0003372396628080532,
    "best_mean_ratio": 0.15689130082977157,
    "design_count": 32
  },
  "stride_5": {
    "worst_design_id": "nearest_top_grid_stride_5_offset_1_1",
    "worst_min_ratio": 3.7032183144167143e-07,
    "worst_mean_ratio": 0.0001042212173606899,
    "best_design_id": "top_grid_stride_5_offset_0_4",
    "best_min_ratio": 0.00033723966280589597,
    "best_mean_ratio": 0.15689130082979047,
    "design_count": 50
  },
  "stride_6": {
    "worst_design_id": "top_grid_stride_6_offset_1_1",
    "worst_min_ratio": 4.75424120258572e-10,
    "worst_mean_ratio": 1.1958344018165326e-07,
    "best_design_id": "top_grid_stride_6_offset_5_4",
    "best_min_ratio": 0.0003372396628073341,
    "best_mean_ratio": 0.1568913008297913,
    "design_count": 72
  }
}
```
