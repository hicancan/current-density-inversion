# Locality Barrier Derivation

Let `L` be the connected graph Laplacian for the nominal circuit graph and
let `d_e` be the signed incidence vector of a candidate via-open edge. For an
accessible pad set `P`, a balanced pad-pair current has the form

```text
b = I (e_p - e_q), p,q in P .
```

The Schur voltage drop that drives the defect signature is

```text
d_e^T L^+ b = I * (L^+ d_e)_p - I * (L^+ d_e)_q .
```

Therefore the best possible pad-pair excitation over the same current budget is

```text
max_{p,q in P} |d_e^T L^+(e_p-e_q)|
  = osc_P(L^+ d_e)
  = max_{p in P}(L^+d_e)_p - min_{p in P}(L^+d_e)_p .
```

The local endpoint excitation used by E30 has Schur drop

```text
d_e^T L^+ d_e .
```

So the exact pad-accessible fraction is

```text
eta_e(P) = osc_P(L^+ d_e) / (d_e^T L^+ d_e).
```

Consequences:

1. Adding pads can only increase `eta_e(P)`.
2. If a sparse pad grid misses the localized extrema of `L^+ d_e`, no linear
   or nonlinear post-processing algorithm can recover the missing active-mode
   contrast under the same physical current budget.
3. E31's positive certificate depends on local candidate-projection pad access,
   not merely on having many far-away pads.
4. Top+bottom local candidate pads are the generated-domain upper design target
   because they recover almost the full local Schur drop for the configured
   defect family.
