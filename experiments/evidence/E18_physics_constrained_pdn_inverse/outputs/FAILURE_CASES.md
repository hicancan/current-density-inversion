# FAILURE CASES

**4 failure case(s) identified:**

| # | Type | Family | Detail |
|---:|---|---|---|
| 1 | dense_via_low_recall | dense_via_cluster | Via recall 0.000 < 0.5 on dense-via cases |
| 2 | deep_layer_misallocation | deep_layer_only | Layer misallocation 0.424 > 0.3 on deep-layer cases |
| 3 | return_grid_ambiguity | return_grid_bottleneck | New method has higher current RMSE than ridge on return-grid cases |
| 4 | kcl_improves_but_rmse_worsens | aggregate | KCL residual improves but overall current RMSE is worse than ridge |

## Mandatory Failure Categories Checked

- [x] No-via false positives
- [x] Dense-via failure
- [x] Deep-layer misallocation
- [x] Return-grid ambiguity
- [x] B residual improves but current allocation wrong
- [x] KCL improves but current RMSE worsens

Generated-domain benchmark only. Cannot claim real validation.