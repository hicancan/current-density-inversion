# Notes

Exp07 is intentionally small. It answers the solver-control question before any
expensive high-fidelity data generation is attempted.

Current status:

1. Real `pypeec==5.8.0` is required.
2. The experiment calls `pypeec.run_mesher_data` and `pypeec.run_solver_data`.
3. Each case writes the exact geometry/problem/tolerance JSON used for PyPEEC.
4. The reported `H_p` point-cloud field is converted to `B = mu0 H_p`.
5. The PyPEEC fields are compared to internal centerline and finite-width
   Biot-Savart references.
6. PyPEEC voxel geometry uses swept cross-section fill instead of a centerline
   skeleton; finite-width cases must therefore allocate more voxels.
7. A small layer-aligned xy-pitch sweep runs on `straight_trace` and `via_pair`.
8. Four exp03-like connected route-family cases now run through the same real
   PyPEEC backend: `two_layer_route_with_via`, `multi_via_route`,
   `dense_via_background`, and `no_via_background`.

Recommended next steps:

1. Promote the exp03-like PyPEEC fields into an exp06 real-solver fidelity
   bridge.
2. Add PyPEEC-generated fields as a frozen operator stress in exp04.
3. Extend the PyPEEC sweep to CAD-like multi-layer routes and explicit return
   structures.
4. Keep the claim boundary: PyPEEC cross-validation is not FEM/QDM/real-chip
   validation.
