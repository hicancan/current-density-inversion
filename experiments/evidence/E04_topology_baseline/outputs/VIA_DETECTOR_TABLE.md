| split | detector | loc error px | hit <=2px | precision | recall | F1 | false positive no-via | threshold |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `test` | `raw_adjoint` | 14.472 | 0.028 | 0.500 | 0.009 | 0.018 | 0.048 | 1.169e-12 |
| `test` | `oracle_sheet_residual` | 1.374 | 0.972 | 1.000 | 0.991 | 0.995 | 0.000 | 1.867e-13 |
| `test` | `unet_no_topology_sheet_residual` | 1.470 | 0.916 | 1.000 | 0.953 | 0.976 | 0.000 | 1.963e-13 |
| `test` | `unet_topology_soft_loss_sheet_residual` | 1.644 | 0.879 | 1.000 | 0.757 | 0.862 | 0.000 | 2.399e-13 |
| `test` | `unet_topology_two_stage_refined_sheet_residual` | 1.644 | 0.879 | 1.000 | 0.757 | 0.862 | 0.000 | 2.399e-13 |
| `test` | `raw_adjoint_dog_fp_controlled` | 14.434 | 0.028 | 0.000 | 0.000 | 0.000 | 0.000 | 3.178e-13 |
| `test` | `oracle_sheet_residual_dog_fp_controlled` | 0.997 | 0.981 | 1.000 | 0.804 | 0.891 | 0.000 | 8.776e-14 |
| `test` | `unet_no_topology_sheet_residual_dog_fp_controlled` | 1.261 | 0.925 | 1.000 | 0.710 | 0.831 | 0.000 | 9.450e-14 |
| `test` | `unet_topology_soft_loss_sheet_residual_dog_fp_controlled` | 1.431 | 0.897 | 1.000 | 0.636 | 0.777 | 0.000 | 9.531e-14 |
| `test` | `unet_topology_two_stage_refined_sheet_residual_dog_fp_controlled` | 1.431 | 0.897 | 1.000 | 0.636 | 0.777 | 0.000 | 9.531e-14 |
| `ood` | `raw_adjoint` | 17.887 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.169e-12 |
| `ood` | `oracle_sheet_residual` | 21.581 | 0.081 | 0.672 | 1.000 | 0.804 | 1.000 | 1.867e-13 |
| `ood` | `unet_no_topology_sheet_residual` | 6.200 | 0.616 | 0.878 | 1.000 | 0.935 | 0.286 | 1.963e-13 |
| `ood` | `unet_topology_soft_loss_sheet_residual` | 7.512 | 0.593 | 0.962 | 0.872 | 0.915 | 0.071 | 2.399e-13 |
| `ood` | `unet_topology_two_stage_refined_sheet_residual` | 7.512 | 0.593 | 0.962 | 0.872 | 0.915 | 0.071 | 2.399e-13 |
| `ood` | `raw_adjoint_dog_fp_controlled` | 18.231 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 3.178e-13 |
| `ood` | `oracle_sheet_residual_dog_fp_controlled` | 7.749 | 0.663 | 0.606 | 0.500 | 0.548 | 0.667 | 8.776e-14 |
| `ood` | `unet_no_topology_sheet_residual_dog_fp_controlled` | 4.891 | 0.698 | 0.966 | 0.663 | 0.786 | 0.048 | 9.450e-14 |
| `ood` | `unet_topology_soft_loss_sheet_residual_dog_fp_controlled` | 6.177 | 0.698 | 0.980 | 0.581 | 0.730 | 0.024 | 9.531e-14 |
| `ood` | `unet_topology_two_stage_refined_sheet_residual_dog_fp_controlled` | 6.177 | 0.698 | 0.980 | 0.581 | 0.730 | 0.024 | 9.531e-14 |
