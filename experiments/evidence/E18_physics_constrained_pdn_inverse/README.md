# E18: Physics-Constrained Multilayer PDN Inverse

## Overview

This evidence package implements and evaluates a physics-constrained multilayer
PCB/PDN current inversion algorithm (`graph_kcl_differentiable_inverse`) against
established baselines on a generated four-layer via-chain benchmark.

## Core Question

> Does graph + KCL/PDN + differentiable Biot-Savart inverse outperform
> naive / incorrect two-layer / ridge / Tikhonov / Fourier / L1-like /
> graph_kcl_aware baselines in current accuracy and physical consistency?

## Algorithm

`graph_kcl_differentiable_inverse`:
1. Warm-start with constrained ridge regression
2. L-BFGS-B optimization of composite loss:
   - B-field fidelity: ||Ax - b_obs||²
   - KCL constraint: ||Dx||²
   - Via sparsity: smooth L1(x_via)
   - Proximity prior: ||x - x_init||²
3. Post-projection via soft KCL constraint

## Benchmark

- 6 families × 3 variants = 18 cases
- 4-layer stack (L1 at -20µm to L4 at -260µm)
- 11 output channels: J1x,J1y,J2x,J2y,J3x,J3y,J4x,J4y,s12,s23,s34

### Families
- `nominal_via_chain` - standard via chain routing
- `no_via_hard_negative` - no vias, only layer currents
- `dense_via_cluster` - dense multi-via stress
- `return_grid_bottleneck` - bottleneck in return path
- `deep_layer_only` - current only in deep layers L3/L4
- `layer_misallocation_trap` - current in L1+L4 only, skipping inner layers

## Claims

- Primary: C10_pdn_kcl_distribution_need
- Secondary: C06_graph_hypothesis_system_identification, C02_single_plane_identifiability_boundary, C04_inverse_crime_and_operator_gap

## Cannot Claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Real multilayer PCB/PDN recovery
- Generated benchmark transfers to real hardware
- Universally outperforms all baselines
