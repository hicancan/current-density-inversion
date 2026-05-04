# ABLATION TABLE

| Method | rel_l2 | misalloc | b_res_rel | kcl_res | via_f1 |
|---|---:|---:|---:|---:|---:|
| graph_kcl_differentiable_inverse_scaled | 9.590102 | 0.164399 | 0.400859 | 1.216e-15 | 0.273775 |
| new_no_projection | 9.590102 | 0.164399 | 0.400859 | 1.444e-13 | 0.273775 |
| new_no_via_sparsity | 9.590102 | 0.164399 | 0.400859 | 1.198e-15 | 0.273775 |