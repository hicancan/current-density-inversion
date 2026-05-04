# PDN/KCL Next Evidence Loop

Claim: `C10_pdn_kcl_distribution_need`.

The first generated prototype exists in `E10_pdn_kcl_distribution`. The
generated chip-like expansion exists in `E11_chip_like_pdn_distribution`, and
the generated physics-learning closure exists in
`E12_pdn_physics_learning`. The next loop is no longer another hand-designed
generated prototype; it is an imported-layout or external-solver bridge while
preserving the same KCL/current-closure gates.

Required expansion:

| Component | Required node |
|---|---|
| CAD/Gerber/GDS-like graph families | `D09_cad_gerber_gds_like` |
| multilayer generated reference distribution | `D11_chip_like_generated_pdn_family` |
| broader KCL solve | `P05_kcl_node_conservation` |
| current closure under return-network variation | `P07_current_closure_loop` |
| return-path completeness audit | `P08_return_path_completeness` |
| external solver held-out rows | `F05_comsol_fem`, `F06_fasthenry` |
| metrics | `M04_kcl_residual`, `M05_divB_residual`, `M13_family_generalization_gap`, `M16_predicted_kcl_residual`, `M17_predicted_current_closure_error` |

Cannot claim: real-board PDN/KCL robustness before CAD-like and external-solver
held-out rows exist and pass metrics. E11/E12 are generated-domain evidence and
do not change that boundary.
