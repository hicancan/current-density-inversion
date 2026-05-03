# Null-Via Synthetic Validation Stress

- enabled: `True`
- calibration split: `val_synthetic_null_via_stress`
- used for PyPEEC threshold selection: `False`
- boundary: Gate parameters are selected only on synthetic validation stress generated from the validation split; PyPEEC cases are not used for threshold selection.

## Selected Gate

- score threshold: `0.179`
- artifact radius px: `0.000`
- return radius px: `2.000`
- artifact physical override: `0.000`

## Validation Before/After

| split | precision | recall | F1 | no-via FP | pred present | TP | FP |
|---|---:|---:|---:|---:|---:|---:|---:|
| `before` | 1.000 | 0.902 | 0.948 | 0.000 | n/a | n/a | n/a |
| `after` | 1.000 | 0.863 | 0.926 | 0.000 | 554 | 554 | 0 |

## Family Rows

| family | cases | input gap | FP before | FP after | recall before | recall after | F1 before | F1 after |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `no_via_clean` | 21 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `synthetic_null_via_bend_corner_stress` | 21 | 0.114 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `synthetic_null_via_layer_allocation_stress` | 21 | 0.324 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `synthetic_null_via_operator_gap_stress` | 21 | 0.182 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `synthetic_null_via_return_path_stress` | 21 | 0.155 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `synthetic_null_via_strong_local_b_gap_stress` | 21 | 0.165 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| `true_via_bend_corner_stress` | 107 | 0.063 | 0.000 | 0.000 | 0.953 | 0.944 | 0.976 | 0.971 |
| `true_via_clean` | 107 | 0.000 | 0.000 | 0.000 | 0.963 | 0.953 | 0.981 | 0.976 |
| `true_via_layer_allocation_stress` | 107 | 0.335 | 0.000 | 0.000 | 0.654 | 0.449 | 0.791 | 0.619 |
| `true_via_near_bend_corner_strong_stress` | 107 | 0.091 | 0.000 | 0.000 | 0.925 | 0.916 | 0.961 | 0.956 |
| `true_via_operator_gap_stress` | 107 | 0.197 | 0.000 | 0.000 | 0.944 | 0.944 | 0.971 | 0.971 |
| `true_via_return_path_stress` | 107 | 0.167 | 0.000 | 0.000 | 0.972 | 0.972 | 0.986 | 0.986 |

Interpretation: this table is the only place where the null-via gate parameters are selected. It uses synthetic validation stress, not PyPEEC test cases.
