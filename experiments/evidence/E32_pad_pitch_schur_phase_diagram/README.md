# E32 Pad-Pitch Schur Phase Diagram

Generated-domain evidence package after E31.

E31 proved the exact pad-Schur reachability ratio

```text
eta_e(P) = osc_P(L^+ d_e) / (d_e^T L^+ d_e)
```

and showed that candidate-projection surface pads can yield a positive magnetic
Gamma certificate. E32 asks the next harder question: what happens when the
accessible pads are constrained by pitch, offset, and local patch geometry?

The central object is a phase diagram over pad sets:

- perimeter top/bottom pads,
- full top-surface access,
- candidate-local top patches,
- candidate-local top+bottom patches,
- regular top pad grids over all pitch offsets,
- nearest-grid approximations when exact candidate pads are not present.

This remains generated-domain reachability evidence. It is not real CAD/GDS,
external-solver, real QDM/NV, or real chip reverse-analysis validation.
