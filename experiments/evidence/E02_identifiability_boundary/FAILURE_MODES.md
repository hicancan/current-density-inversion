# Failure Modes

## 1. High-frequency loss

Sensor standoff suppresses high-frequency current information and can make
inverse recovery ill-conditioned.

## 2. Single-plane multilayer ambiguity

Even with `Bxyz`, a single measurement plane does not make arbitrary multilayer
current decomposition identifiable without priors or extra observations.

## 3. Finite-FOV and noise amplification

Finite fields of view and noise can dominate ideal Fourier inversion results.

