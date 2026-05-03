# PDN/KCL Next Evidence Loop

Claim: `C10_pdn_kcl_distribution_need`.

This is the highest-priority missing evidence loop.

Required implementation:

| Component | Required node |
|---|---|
| circuit graph generator | `D08_pdn_kcl_circuit_graph` |
| KCL solve | `P05_kcl_node_conservation` |
| current closure | `P07_current_closure_loop` |
| return-path completeness | `P08_return_path_completeness` |
| PDN representation | `R06_pdn_circuit_graph` |
| metrics | `M04_kcl_residual`, `M05_divB_residual` |

Cannot claim: PDN/KCL robustness before this loop exists and passes metrics.

