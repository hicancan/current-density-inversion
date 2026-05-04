# Evidence Edge Table

| Evidence | Relation | Claim | Strength | Scope | Caveat |
|---|---|---|---|---|---|
| `E01_canonical_forward_sanity` | `supports` | `C01_forward_sanity` | `strong` | canonical ideal Biot-Savart | Does not validate finite-width, return path, FEM, or real QDM/NV. |
| `E02_observability_bxy_bz` | `supports` | `C02_single_plane_identifiability_boundary` | `strong` | ideal thin-sheet single-plane observations | Does not make arbitrary multilayer inversion identifiable. |
| `E03_two_layer_via_topology` | `supports` | `C02_single_plane_identifiability_boundary` | `medium` | two-layer generated route/via benchmark | Synthetic route-like families only. |
| `E03_two_layer_via_topology` | `motivates` | `C03_unet_topology_baseline_boundary` | `medium` | two-layer generated route/via benchmark | This provides a benchmark distribution, not a final detector. |
| `E04_topology_baseline_and_failures` | `limits` | `C03_unet_topology_baseline_boundary` | `strong` | synthetic and PyPEEC-domain stress | Topology-aware models remain baselines with no-via and return-path failures. |
| `E04_topology_baseline_and_failures` | `supports` | `C04_inverse_crime_and_operator_gap` | `medium` | operator stress diagnostics | Diagnostic stress, not external solver proof. |
| `E04_topology_baseline_and_failures` | `motivates` | `C11_mechanism_level_explanation` | `medium` | no-via and return-path failure analysis | Failure labels are not yet full mechanism-level correctness metrics. |
| `E05_qdm_like_observation_stress` | `motivates` | `C13_calibration_protocol_reality` | `medium` | QDM-like observation proxy | Not real ODMR or measured sensor calibration. |
| `E06_multifidelity_operator_gap` | `supports` | `C04_inverse_crime_and_operator_gap` | `strong` | low/medium/high surrogate fidelity ladder | High-fidelity branch is still a surrogate. |
| `E07_pypeec_solver_bridge` | `supports` | `C05_pypeec_solver_bridge` | `strong` | generated PyPEEC conductor cases | PyPEEC-domain bridge is not real CAD/FEM/QDM validation. |
| `E07_pypeec_solver_bridge` | `limits` | `C04_inverse_crime_and_operator_gap` | `medium` | centerline/finite-width/PyPEEC solver gap | Generated solver bridge exposes operator gap but does not close it. |
| `E08_graph_hypothesis_system_id` | `supports` | `C06_graph_hypothesis_system_identification` | `strong` | generated graph and generated PyPEEC-domain H0/H1/H2/H3 | No real CAD/Gerber/GDS graph import. |
| `E08_graph_hypothesis_system_id` | `supports` | `C07_stacked_evidence_calibration` | `strong` | legal generated PyPEEC calibration/held-out folds | Does not support no-calibration or real-world deployment claims. |
| `E08_graph_hypothesis_system_id` | `supports` | `C08_ood_refusal_safety` | `medium` | generated hidden and near-hidden stress | Accepted hidden rows still need mechanism-level correctness. |
| `E08_graph_hypothesis_system_id` | `supports` | `C09_fewshot_family_adaptation` | `medium` | generated family few-shot adaptation | Calibration label source is not yet realistic. |
| `E08_graph_hypothesis_system_id` | `limits` | `C11_mechanism_level_explanation` | `strong` | hidden and near-hidden accepted-row analysis | Primary-label accuracy does not prove mechanism explanation. |
| `E08_graph_hypothesis_system_id` | `motivates` | `C13_calibration_protocol_reality` | `medium` | few-shot generated-family calibration | Real calibration source remains unresolved. |
| `E09_real_data_intake_gate` | `requires` | `C12_real_qdm_nv_validation` | `strong` | real-data intake gate | No measured rows are validated by the scaffold alone. |
| `E09_real_data_intake_gate` | `motivates` | `C13_calibration_protocol_reality` | `medium` | real calibration gate design | The protocol is not validated until real rows exist. |
| `E10_pdn_kcl_distribution` | `supports` | `C10_pdn_kcl_distribution_need` | `medium` | generated resistive PDN/KCL graph prototype | Runnable KCL/current-closure evidence only; not real CAD/Gerber/GDS, external solver, or real QDM/NV validation. |
| `E10_pdn_kcl_distribution` | `motivates` | `C06_graph_hypothesis_system_identification` | `medium` | PDN/KCL-generated H0/H1/H2/H3 hypothesis rows | The scorer is matched to generated candidates and does not replace CAD-derived graph candidates. |
| `E11_chip_like_pdn_distribution` | `supports` | `C10_pdn_kcl_distribution_need` | `strong` | generated chip-like four-layer PDN graph distribution with KCL, current closure, return paths, and Bxyz fields | Artificial micro-PDN only; not real chip, CAD/Gerber/GDS, external solver, or real QDM/NV validation. |
| `E11_chip_like_pdn_distribution` | `motivates` | `C06_graph_hypothesis_system_identification` | `medium` | generated chip-like H0/H1/H2/H3 PDN hypothesis rows | Rows are generated from a hand-designed family and do not replace CAD-derived graph candidates. |
| `E12_pdn_physics_learning` | `supports` | `C10_pdn_kcl_distribution_need` | `medium` | generated E11 physics-learning closure with held-out label learning and predicted-current KCL/current-closure improvement | Physics-aware projection is generated-domain evidence and cannot be claimed as real learned physics under real layouts. |
| `E12_pdn_physics_learning` | `supports` | `C06_graph_hypothesis_system_identification` | `medium` | Bxyz-to-hypothesis learning plus graph/KCL projected current consistency on generated E11 rows | It still depends on generated graph families and matched graph projection. |
| `E12_pdn_physics_learning` | `limits` | `C11_mechanism_level_explanation` | `strong` | separation of label learning, KCL/current-closure consistency, and mechanism-level explanation | E12 does not add mechanism labels or accepted-row mechanism audits; label correctness remains insufficient. |
| `E12_pdn_physics_learning` | `motivates` | `C14_unlabeled_family_adaptation` | `medium` | generated E11 family-hidden rows expose a next target for label-free adaptation | E12 is supervised generated-domain learning, not unlabeled adaptation evidence. |
