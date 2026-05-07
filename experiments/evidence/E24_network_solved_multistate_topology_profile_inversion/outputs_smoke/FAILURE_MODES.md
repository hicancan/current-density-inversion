# E24 Failure Modes

## Scientific Gates Failed

- shared_network_beats_free_kcl_wrong_topology
- h1_h2_shared_profile_gap_positive_rate_ge_0_80
- critical_pair_profile_gamma_positive_rate_ge_0_50
- operator_stress_gamma_positive_rate_ge_0_30

## Known Limitations

- Generated domain only; no real QDM/NV or CAD/GDS validation
- Pairwise profile margin computation uses surrogate residual-gap method
- Operator stress radii use simplified perturbation models
- Gradient-based fitting may converge to local minima
- Conductance priors are uniform; no edge-role-specific priors applied

## E24-Specific Failure Modes

1. **Shared network may underfit truth**: If conductances cannot capture
   the true current distribution, gamma becomes small.
2. **Wrong topology may have enough degrees of freedom**: If nullspace
   dimension compensates for wrong graph structure, free KCL gap closes.
3. **Stress radii may dominate margin**: In heavily stressed conditions,
   rho_h + rho_g > residual gap, making gamma negative.
