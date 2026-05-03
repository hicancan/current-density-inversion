# Exp07 PyPEEC voxel convergence table

| case | level | pitch_xy_um | pitch_z_um | n_xy | n_z | n_voxel_used | shape_rel_l2 | to_next_finer_shape_rel_l2 | src_current_rel_error | solution_ok |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| straight_trace | coarse | 60 | 25 | 17 | 7 | 15 | 0.00350416 | 0.107959 | 2.1684e-16 | True |
| straight_trace | medium | 40 | 25 | 25 | 7 | 69 | 0.107915 | 0.066791 | 3.57787e-14 | True |
| straight_trace | fine | 30 | 25 | 33 | 7 | 87 | 0.0548972 | 0.0292916 | 2.77556e-14 | True |
| straight_trace | ultrafine | 20 | 25 | 49 | 7 | 129 | 0.0263483 |  | 1.29237e-13 | True |
| via_pair | coarse | 60 | 25 | 17 | 7 | 23 | 0.00639167 | 0.20378 | 7.58942e-15 | True |
| via_pair | medium | 40 | 25 | 25 | 7 | 72 | 0.202964 | 0.192951 | 8.71699e-14 | True |
| via_pair | fine | 30 | 25 | 33 | 7 | 146 | 0.0552739 | 0.0294343 | 6.35342e-14 | True |
| via_pair | ultrafine | 20 | 25 | 49 | 7 | 200 | 0.0259314 |  | 2.84495e-13 | True |
| two_layer_route_with_via | coarse | 60 | 25 | 17 | 7 | 27 | 0.0901243 | 0.174573 | 1.32273e-14 | True |
| two_layer_route_with_via | medium | 40 | 25 | 25 | 7 | 66 | 0.12668 | 0.108393 | 6.33174e-14 | True |
| two_layer_route_with_via | fine | 30 | 25 | 33 | 7 | 114 | 0.0492465 | 0.0313654 | 4.70544e-14 | True |
| two_layer_route_with_via | ultrafine | 20 | 25 | 49 | 7 | 182 | 0.0296048 |  | 2.78857e-13 | True |
| dense_via_background | coarse | 60 | 25 | 17 | 7 | 60 | 0.158787 | 0.134144 | 9.54098e-15 | True |
| dense_via_background | medium | 40 | 25 | 25 | 7 | 121 | 0.141357 | 0.122188 | 3.38271e-14 | True |
| dense_via_background | fine | 30 | 25 | 33 | 7 | 178 | 0.0767739 | 0.134709 | 1.29671e-13 | True |
| dense_via_background | ultrafine | 20 | 25 | 49 | 7 | 297 | 0.113479 |  | 3.69496e-13 | True |
| no_via_background | coarse | 60 | 25 | 17 | 7 | 55 | 0.256902 | 0.176018 | 1.34441e-14 | True |
| no_via_background | medium | 40 | 25 | 25 | 7 | 94 | 0.124506 | 0.0679911 | 5.20417e-14 | True |
| no_via_background | fine | 30 | 25 | 33 | 7 | 121 | 0.069031 | 0.0987035 | 3.46945e-14 | True |
| no_via_background | ultrafine | 20 | 25 | 49 | 7 | 237 | 0.126456 |  | 1.28803e-13 | True |
