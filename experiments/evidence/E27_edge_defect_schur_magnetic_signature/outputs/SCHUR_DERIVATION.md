# Schur Derivation for E27 Edge-Defect Signatures

## Core Formula

For a baseline graph Laplacian L = D C D^T with gauge fixing, adding a candidate
edge with incidence vector a_q and conductance alpha gives:

```
L_alpha = L + alpha * a_q a_q^T
```

By Sherman-Morrison, the perturbed potential is:

```
phi(alpha) = phi - (alpha * v_q / (1 + alpha * R_q)) * G * a_q
```

where:
- v_q = a_q^T phi (baseline voltage drop across candidate endpoints)
- R_q = a_q^T G a_q (effective resistance across candidate endpoints)
- G = L^dagger (grounded Laplacian pseudo-inverse)

## Current Perturbation

For existing edges:
```
Delta_i_existing = -(alpha * v_q / (1 + alpha * R_q)) * C D^T G a_q
```

For the new candidate edge:
```
i_q_new = alpha * v_q / (1 + alpha * R_q)
```

## Magnetic Signature

```
Delta_y = A * Delta_i
```

## State Design

Optimal port excitation maximizes:
```
b* = argmax |a_q^T G b| / (1 + alpha * a_q^T G a_q)
```

For multiple critical defects, use minimax:
```
U* = argmax min_{q in Q_crit} Gamma_q(U)
```

## Robust Edge-Defect Certificate

```
Gamma_q(U) = S_q(U) - epsilon - rho_q(U) - tau
```

where S_q(U) = ||W * Delta_Y_q(U)||_2 is the stacked signal energy.
