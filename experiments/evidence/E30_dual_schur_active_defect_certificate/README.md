# E30 Dual-Schur Active Defect Certificate

Generated-domain evidence package for local via-open current-inversion
observability under active Schur-aligned excitation.

This package tests a specific first-principles hypothesis:

> Boundary magnetic measurements may fail for local current defects because the
> excitation does not create enough voltage drop on the defective edge. If the
> excitation is aligned with the defect edge's graph-incidence direction, the
> local magnetic defect signature should scale linearly with drive current and
> can become robustly separable after directional noise and nuisance subtraction.

The result is not real-chip validation. It is an observability certificate in a
generated KCL/Biot-Savart graph using E28's transfer-matrix forward operator.
The default run also includes an optimistic top/bottom perimeter-boundary basis
control to test whether the negative result is only due to using six diagonal
boundary states.
