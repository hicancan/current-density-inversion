# E11 Metrics Schema

Minimum required fields in `outputs/metrics.json`:

- `evidence_id`
- `claim_id`
- `status`
- `generated_at`
- `case_count`
- `family_count`
- `layer_count`
- `node_count`
- `edge_count`
- `split_roles`
- `kcl.max_residual`
- `closure.max_error`
- `divB.max_proxy_residual`
- `hypothesis.balance`
- `acceptance_gates`
- `all_acceptance_gates_passed`
- `cannot_claim`

Acceptance requires KCL residual, current closure, divB proxy, held-out family
coverage, and balanced H0/H1/H2/H3 generated rows to pass.

