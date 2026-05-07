# Pad-Schur Reachability Theorem

For a graph Laplacian `L`, candidate defect edge incidence `d_e`, and an
accessible pad set `P`, any balanced pad-pair current with amplitude `I` obeys

```text
|d_e^T L^+ b| <= I * osc_P(L^+ d_e)
```

where

```text
osc_P(h) = max_{p in P} h_p - min_{p in P} h_p .
```

The local dual-Schur endpoint current `b = I d_e` creates voltage drop

```text
I * d_e^T L^+ d_e .
```

Therefore the exact best pad-accessible fraction of the local dual-Schur drop is

```text
eta_e(P) = osc_P(L^+ d_e) / (d_e^T L^+ d_e).
```

This is not a heuristic. It is the operator norm of the scalar functional
`b -> d_e^T L^+ b` over the balanced pad-pair current budget. The optimizing
pad pair is the max/min pair of `L^+ d_e` restricted to `P`.

E31's central finding is:

- Perimeter pads have near-zero `eta`, proving why E30's perimeter control
  fails.
- Candidate-projection top-surface pads have `eta` above the current-budget
  threshold.
- Using the theorem's optimizing pad pairs yields a positive finite-difference
  magnetic Gamma certificate after nuisance subtraction.
