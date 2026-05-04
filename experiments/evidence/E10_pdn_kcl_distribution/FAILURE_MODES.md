# Failure Modes

## 1. KCL correctness is not layout realism

The generated graph can satisfy node conservation and current closure while
still being a toy PDN. This evidence cannot be described as real CAD/Gerber/GDS
validation.

## 2. Lowest residual is not mechanism truth

The current H0/H1/H2/H3 scorer uses matched generated candidates. It verifies
that the PDN/KCL loop is runnable, not that real mechanisms are identifiable.

## 3. Return paths are represented but simplified

The return network is explicit and current-carrying, but it is a small
resistive graph. Plane spreading, package return, inductive effects, and
material thickness are not validated.

## 4. Magnetic divergence is a numerical proxy

The `M05_divB_residual` gate uses finite differences around the sensor plane.
It is a sanity gate for the generated field, not a replacement for full solver
validation.

