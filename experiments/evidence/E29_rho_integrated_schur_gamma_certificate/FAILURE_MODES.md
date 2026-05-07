# Failure Modes

Documented failure modes specific to E29.

## synthetic_schur_signatures

- Severity: warning
- Description: Schur defect signatures are synthetic (generated perturbations). Real E27 edge-Schur artifacts are not available.

## local_rho_not_e25_calibrated

- Severity: warning
- Description: Rho estimates are computed locally; E25 artifacts were not available in the E29 worktree.

## shared_rho_all_defects

- Severity: info
- Description: Pairwise certificate uses a single shared rho for all defects; per-defect rho requires E27 artifacts.
