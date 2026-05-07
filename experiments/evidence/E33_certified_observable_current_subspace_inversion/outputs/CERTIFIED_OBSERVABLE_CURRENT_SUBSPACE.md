# Certified Observable Current Subspace

The strict current inversion model is

```text
y = A J + n,       n ~ N(0, Sigma).
```

Let `Phi` be an orthonormal current-mode basis and write `J = Phi alpha`.
The data-supported current modes are the eigenspaces of

```text
G_obs = Phi^T A^T Sigma^-1 A Phi.
```

In the thin-sheet stream-function Fourier basis used here, each normalized
current mode is diagonal. For spatial frequency `q` and standoff `h`,

```text
s(q,h) = q exp(-q h)
lambda_q = sum_h s(q,h)^2 / sigma^2.
```

The certified inverse is not a full inverse. It is

```text
alpha_hat_i = <a_i, y> / lambda_i     if lambda_i >= tau_obs
alpha_hat_i = refused                 if lambda_i < tau_obs.
```

This changes the scientific object:

```text
recoverable current = Pi_obs J
dark current        = (I - Pi_obs) J.
```

The breakthrough is not that dark current becomes recoverable. It is that the
algorithm reports the recoverable projection and refuses unsupported modes
before they become hallucinated current.
