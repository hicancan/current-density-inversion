# E31 Pad-Schur Reachability Certificate

Generated-domain evidence package for the next step after E30.

E30 showed that local dual-Schur endpoint excitation makes central via-open
defect signatures robustly separable, while ordinary and perimeter boundary
ports fail. E31 asks whether that local dual mode can be synthesized by a
deployable pad-accessible source pattern.

The key mathematical object is the exact pad reachability ratio:

```text
eta_e(P) = osc_P(L^+ d_e) / (d_e^T L^+ d_e)
```

where `P` is the accessible pad set and `d_e` is the candidate defect edge
incidence vector. `eta_e(P)` is the exact best possible fraction of the local
Schur voltage drop obtainable by any balanced pad pair under the same current
budget.

This remains generated-domain evidence. It is not real CAD/GDS, real QDM/NV,
or external solver validation.

