| split | detector | loc error px | hit <=2px | precision | recall | F1 | false positive no-via | threshold |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `test` | `raw_adjoint` | 14.472 | 0.028 | 0.500 | 0.009 | 0.018 | 0.048 | 1.169e-12 |
| `test` | `oracle_sheet_residual` | 1.374 | 0.972 | 1.000 | 0.991 | 0.995 | 0.000 | 1.867e-13 |
| `test` | `unet_no_topology_sheet_residual` | 1.576 | 0.916 | 1.000 | 0.944 | 0.971 | 0.000 | 2.015e-13 |
| `test` | `unet_topology_soft_loss_sheet_residual` | 1.836 | 0.897 | 0.990 | 0.944 | 0.967 | 0.048 | 2.024e-13 |
| `test` | `unet_topology_two_stage_refined_sheet_residual` | 1.836 | 0.897 | 0.990 | 0.944 | 0.967 | 0.048 | 2.024e-13 |
| `test` | `raw_adjoint_dog_fp_controlled` | 14.434 | 0.028 | 0.000 | 0.000 | 0.000 | 0.000 | 3.178e-13 |
| `test` | `oracle_sheet_residual_dog_fp_controlled` | 0.997 | 0.981 | 1.000 | 0.804 | 0.891 | 0.000 | 8.776e-14 |
| `test` | `unet_no_topology_sheet_residual_dog_fp_controlled` | 1.235 | 0.935 | 1.000 | 0.720 | 0.837 | 0.000 | 9.398e-14 |
| `test` | `unet_topology_soft_loss_sheet_residual_dog_fp_controlled` | 1.344 | 0.925 | 1.000 | 0.617 | 0.763 | 0.000 | 1.005e-13 |
| `test` | `unet_topology_two_stage_refined_sheet_residual_dog_fp_controlled` | 1.344 | 0.925 | 1.000 | 0.617 | 0.763 | 0.000 | 1.005e-13 |
| `ood` | `raw_adjoint` | 17.887 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.169e-12 |
| `ood` | `oracle_sheet_residual` | 21.581 | 0.081 | 0.672 | 1.000 | 0.804 | 1.000 | 1.867e-13 |
| `ood` | `unet_no_topology_sheet_residual` | 7.468 | 0.547 | 0.933 | 0.977 | 0.955 | 0.143 | 2.015e-13 |
| `ood` | `unet_topology_soft_loss_sheet_residual` | 6.757 | 0.640 | 0.822 | 0.965 | 0.888 | 0.429 | 2.024e-13 |
| `ood` | `unet_topology_two_stage_refined_sheet_residual` | 6.757 | 0.640 | 0.822 | 0.965 | 0.888 | 0.429 | 2.024e-13 |
| `ood` | `raw_adjoint_dog_fp_controlled` | 18.231 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 3.178e-13 |
| `ood` | `oracle_sheet_residual_dog_fp_controlled` | 7.749 | 0.663 | 0.606 | 0.500 | 0.548 | 0.667 | 8.776e-14 |
| `ood` | `unet_no_topology_sheet_residual_dog_fp_controlled` | 6.089 | 0.663 | 0.939 | 0.535 | 0.681 | 0.071 | 9.398e-14 |
| `ood` | `unet_topology_soft_loss_sheet_residual_dog_fp_controlled` | 5.410 | 0.709 | 0.950 | 0.442 | 0.603 | 0.048 | 1.005e-13 |
| `ood` | `unet_topology_two_stage_refined_sheet_residual_dog_fp_controlled` | 5.410 | 0.709 | 0.950 | 0.442 | 0.603 | 0.048 | 1.005e-13 |
