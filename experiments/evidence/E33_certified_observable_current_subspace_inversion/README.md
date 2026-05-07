# E33 Certified Observable Current Subspace Inversion

Generated-domain evidence package for the strict current-density inversion
problem.

E33 reframes current inversion from full-map recovery to certified projection
recovery:

```text
J = J_observable + J_dark
```

Only `J_observable` is recovered. `J_dark` is explicitly refused with an
operator-level Fisher/SNR certificate.

The runnable slice uses the Fourier/stream-function diagonalization of a
thin-sheet Biot-Savart forward. For a normalized divergence-free current mode
with spatial frequency `q`, the magnetic response at standoff `h` is

```text
s(q,h) = q exp(-q h)
```

and the Fisher eigenvalue is

```text
lambda_q = sum_h s(q,h)^2 / sigma^2 .
```

Modes with `sqrt(lambda_q)` above the configured threshold are recovered; all
others are reported as dark current modes. This remains generated-domain
evidence, not real QDM/NV, CAD/GDS, or external-solver validation.
