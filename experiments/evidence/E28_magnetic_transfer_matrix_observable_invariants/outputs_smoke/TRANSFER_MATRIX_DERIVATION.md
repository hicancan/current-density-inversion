# Transfer Matrix Derivation

## Graph Model

- Nodes (V): 576
- Edges (E): 1584
- Operator shape (A): [432, 1584]
- Incidence matrix shape (D): [576, 1584]
- D rank: 576 (nullity: 1008)

## Transfer Matrix Construction

```math
T_y = A C D^T L^+ B
```

where:
- A: Biot-Savart operator (M_obs x E)
- C: diagonal conductance matrix (E x E)
- D: incidence matrix (V x E)
- L = D C D^T: graph Laplacian (V x V)
- B: port excitation matrix (V x S)

## Per-Hypothesis Diagnostics

| hypothesis | shape | eff_rank | condition | frob_norm |
|---|---:|---:|---:|---:|
| H0_no_via | [432, 4] | 4 | 2.22e+01 | 16.6465 |
| H1_via | [432, 4] | 4 | 2.07e+01 | 15.1442 |
| H2_model_gap | [432, 4] | 4 | 2.07e+01 | 15.1320 |
| H3_return_path | [432, 4] | 4 | 1.51e+01 | 13.6827 |

## Port Excitation

Port excitations use balanced injection/extraction at boundary nodes.
Each column of B represents a different port pair configuration.

## Graph Laplacian Regularization

The pseudo-inverse L^+ is computed via SVD with rcond=1e-10.
The nullspace of L corresponds to the constant vector (global potential shift).