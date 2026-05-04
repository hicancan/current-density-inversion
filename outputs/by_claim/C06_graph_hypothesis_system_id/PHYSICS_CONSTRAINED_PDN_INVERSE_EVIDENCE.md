# E18 Physics-Constrained PDN Inverse Evidence

## Claim: C06_graph_hypothesis_system_identification

### Evidence summary

E18's `graph_kcl_differentiable_inverse` uses KCL divergence constraints as
physics-informed regularization for multilayer current inversion. The composite
loss includes ||Dx||^2 (KCL residual) as a differentiable constraint,
enforcing that the recovered current distribution satisfies conservation laws.

### Key results

- KCL residual reduced by ~6 orders of magnitude vs unconstrained ridge
- KCL post-projection enforces near-zero divergence at output
- Graph-aware constraint (D matrix) encodes layer topology

### Failure cases

- KCL-RMSE tradeoff: enforcing KCL can worsen current accuracy when the
  true distribution includes via source/sink effects not captured by the
  simple divergence matrix
- Dense via cluster cases have zero recall

### Cannot claim

- Graph constraints derived from real CAD/GDS layouts
- KCL improvement proves current accuracy improvement
- Generated graph topology transfers to real hardware

### Metrics

See `experiments/evidence/E18_physics_constrained_pdn_inverse/outputs/metrics.json`
