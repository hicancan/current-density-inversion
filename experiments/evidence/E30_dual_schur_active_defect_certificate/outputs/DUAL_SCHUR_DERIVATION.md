# Dual-Schur Derivation

Let the generated resistive graph have incidence matrix `D`, diagonal
conductance `C`, graph Laplacian

```text
L(C) = D C D^T
```

and magnetic forward operator `A`. For a port excitation matrix `B`, the
magnetic transfer matrix is

```text
T(C; B) = A C D^T L(C)^+ B .
```

For a candidate via edge `e=(u,v)`, define the incidence vector

```text
d_e = e_v - e_u .
```

A via-open perturbation replaces `c_e` by `alpha c_e`, where
`0 < alpha << 1`. The exact finite-difference local-defect signature used by
E30 is

```text
S_e(B) = T(C + Delta C_e; B) - T(C; B).
```

The first-order Schur sensitivity explains the active design:

```text
delta T_e(B) =
  A [E_e D^T L^+ B
     - C D^T L^+ d_e d_e^T L^+ B] delta c_e
  + higher-order terms.
```

The only factor controlled by the experimenter is the potential drop term

```text
d_e^T L^+ b .
```

Therefore the Schur-aligned local excitation

```text
b_e = I d_e
```

maximizes the voltage drop on the candidate edge under the local-access
idealization. Because the network solve and magnetic forward are linear in the
drive amplitude `I`, every pairwise signature distance obeys

```text
delta_ij(I) = I delta_ij(1).
```

The directional robust margin is

```text
Gamma_ij(I) = delta_ij(I) - z sigma - rho_i(I) - rho_j(I) - tau.
```

For relative nuisance at fixed perturbation percentages, the usable slope is
approximately `(delta_ij(I)-rho_i(I)-rho_j(I))/I`, giving the critical-current
law

```text
I_crit = (z sigma + tau) / min_ij s_ij .
```

E30's breakthrough is not that arbitrary chip current is recovered. It is the
sharper observability statement: under the generated graph, the local via-open
defect family is below threshold for boundary excitation but above threshold
for Schur-aligned local excitation at the configured current budget.
