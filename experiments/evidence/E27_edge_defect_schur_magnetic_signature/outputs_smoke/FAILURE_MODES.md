# Failure Modes - E27

Failure modes are preserved as generated-domain evidence boundaries.

## Failed Scientific Gates
- `schur_states_beat_random_signal_by_2x`: FAILED
- `positive_edge_gamma_rate_ge_0_50`: FAILED
- `positive_pairwise_defect_gamma_rate_ge_0_30`: FAILED
- `via_return_pair_gamma_positive_rate_ge_0_50`: FAILED
- `truth_in_consistent_set_rate_ge_0_90`: FAILED
- `singleton_wrong_rate_eq_0`: FAILED
- `empty_rate_le_0_10`: FAILED

## Low-Gamma Defect Families
- `via_insertion`: positive rate 0.000e+00
- `via_removal`: positive rate 0.000e+00
- `return_path_insertion`: positive rate 0.000e+00
- `return_path_removal`: positive rate 0.000e+00

## Pairwise Discrimination Failure
- Positive pairwise Gamma rate: 0.000e+00
- Many defect pairs are not distinguishable under current uncertainty.

## High Empty Rate
- Empty rate: 1.000000
- Many defects have no observable signature above the noise floor.

## Inherent Limitations

- Generated graph network is a simplified planar model; real layouts have complex via stacks, non-uniform trace widths, and irregular geometries.
- Edge-segment Biot-Savart uses midpoint quadrature; finite-width and multifilament corrections are not applied.
- Schur state design uses random search over port pairs; a full combinatorial optimization would be needed for real port constraints.
- Operator perturbation rho is a scalar estimate; E25-style per-defect decomposition would give tighter bounds.
- Deep-layer defects have exponentially attenuated signals; multi-height observation may partially recover them.
