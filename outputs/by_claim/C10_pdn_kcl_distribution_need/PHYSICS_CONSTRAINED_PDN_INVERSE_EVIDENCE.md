# E18 Physics-Constrained PDN Inverse Evidence

## Claim: C10_pdn_kcl_distribution_need

### Evidence summary

E18 implements `graph_kcl_differentiable_inverse`: a warm-started constrained
ridge regression + L-BFGS-B composite loss optimization (B-fidelity + KCL +
via sparsity + prior) + KCL post-projection, evaluated on a generated
four-layer via-chain benchmark (18 cases, 6 families, 11 channels) against
4 baselines (naive, incorrect two-layer, ridge, graph_kcl_aware).

### Key results

- KCL residual: 2.4e-19 (new method) vs 1.6e-13 (ridge) — orders of magnitude improvement
- Layer misallocation: 0.213 (new) ≈ 0.213 (graph_kcl_aware) — matched, not improved
- Physical B residual: 1.000 (all methods) — same-operator inverse
- Via F1: 0.000 (all methods) — via detection not effective at this scale

### Failure cases

1. Dense-via recall = 0 on cluster stress cases
2. Deep-layer misallocation > 0.3
3. Return-grid ambiguity: higher RMSE than ridge
4. KCL-RMSE tradeoff: KCL improves but current RMSE worsens vs ridge

### Leaderboard

See `experiments/evidence/E18_physics_constrained_pdn_inverse/outputs/UNIFIED_LEADERBOARD.md`

### Cannot claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universally outperforms all baselines
- Generated benchmark transfers to real hardware

### Metrics

See `experiments/evidence/E18_physics_constrained_pdn_inverse/outputs/metrics.json`
