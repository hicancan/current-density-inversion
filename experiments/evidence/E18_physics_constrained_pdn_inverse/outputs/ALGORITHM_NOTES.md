# ALGORITHM NOTES

## graph_kcl_differentiable_inverse

### Architecture
1. **Warm start**: Constrained ridge regression (A^T A + alpha I + cw D^T D)^{-1} A^T b
2. **Optimization**: L-BFGS-B minimizing composite loss:
   - B-fidelity: w_b * ||Ax - b_obs||^2
   - KCL constraint: w_kcl * ||Dx||^2
   - Via sparsity: w_via * smooth_L1(x_via)
   - Proximity prior: w_prior * ||x - x_init||^2
3. **Post-projection**: Soft KCL projection (I + proj_w * D^T D)^{-1} x_opt

### Design decisions
- CPU-first with scipy L-BFGS-B (no GPU dependency)
- Smooth L1 (Huber-like) for via sparsity to maintain differentiability
- Warm start from constrained ridge for faster convergence
- KCL post-projection enforces physical consistency at output

### Hyperparameters (from config)
- inverse_max_iter: 200
- inverse_lr: 0.01
- inverse_b_weight: 1.0
- inverse_kcl_weight: 0.5
- inverse_topo_weight: 0.3
- inverse_via_sparsity_weight: 0.1
- inverse_layer_prior_weight: 0.05
- ridge_alpha: 0.01
- kcl_constraint_weight: 0.5

### Trade-offs
- Higher KCL weight improves physics consistency but may worsen B residual
- Via sparsity promotes sparse via detection but may miss dense clusters
- Post-projection can shift optimized solution

### Cannot claim
- Optimal hyperparameters for real boards
- Universally outperforms all baselines
- Real physics validation
- Mechanism-level explanation
