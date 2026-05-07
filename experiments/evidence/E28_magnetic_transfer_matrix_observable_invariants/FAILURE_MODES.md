# E28 Failure Modes

See `outputs/FAILURE_MODES.md` for per-run failure documentation.

## Systematic failure modes

1. **Transfer matrix rank deficiency**: When port excitation does not span the accessible subspace, T_y has insufficient rank for reliable invariant computation.

2. **Invariant collapse**: When transfer matrices of different hypotheses share the same column space (e.g., via conductance too small), projector and Gram distances become zero.

3. **Nuisance dominates signal**: When perturbation radius exceeds invariant distance, robust margins are negative even for well-separated hypotheses.

4. **Small port excitation**: When port amplitudes are too small, the transfer matrix is dominated by noise rather than topology-dependent signal.

5. **Graph model mismatch**: When the incidence matrix does not accurately represent the physical current topology, the transfer matrix loses discriminative power.
