# E12 Metrics Schema

Minimum required fields in `outputs/metrics.json`:

- `evidence_id`
- `claim_id`
- `status`
- `dataset`
- `split_roles`
- `models.scorer`
- `models.graph_agnostic`
- `models.physics_aware`
- `heldout_accuracy`
- `family_generalization_gap`
- `predicted_kcl_residual`
- `predicted_current_closure_error`
- `field_reconstruction_rmse`
- `physics_learning_gain_vs_unconstrained`
- `acceptance_gates`
- `all_acceptance_gates_passed`
- `cannot_claim`

The gate must fail if label accuracy improves but predicted-current KCL or
current closure does not improve over the unconstrained current predictor.

