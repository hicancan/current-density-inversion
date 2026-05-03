# Evidence Inventory

This repository starts from evidence packages, not chronological experiment
numbers. Each evidence package is registered in `experiments.yml` and connected
to claims through `evidence_edges.yml`.

| Evidence package | Main role | Main claims | Primary boundary |
|---|---|---|---|
| E01_canonical_forward_sanity | Forward sanity on wire, loop, and via cases | C01 | Does not validate finite-width, return path, FEM, or real QDM/NV. |
| E02_observability_bxy_bz | Single-plane observability and Bxy/Bz inverse boundary | C02 | Ideal thin-sheet operator only. |
| E03_two_layer_via_topology | Two-layer/via topology and dataset diversity | C02, C03 | Synthetic route-like distribution only. |
| E04_topology_baseline_and_failures | Topology-aware inverse baseline plus no-via/return diagnostics | C03, C04, C11 | Diagnostic baseline, not final detector. |
| E05_qdm_like_observation_stress | PSF, noise, tilt, confidence, and NV projection stress | C13 | QDM-like proxy, not ODMR-level real measurement. |
| E06_multifidelity_operator_gap | Anti-inverse-crime and operator-gap ladder | C04 | Surrogate high-fidelity operator, not FEM/FastHenry/QDM. |
| E07_pypeec_solver_bridge | PyPEEC solver execution and solver-gap bridge | C05 | Toy generated geometries, not real CAD/FEM/QDM. |
| E08_graph_hypothesis_system_id | H0/H1/H2/H3 graph hypothesis scoring, refusal, calibration, and few-shot adaptation | C06, C07, C08, C09, C11 | Generated graph/PyPEEC-domain scope. |
| E09_real_data_intake_gate | Real-data metadata, array, background, and simple-wire gate design | C12, C13 | Interface scaffold; no measured-data validation included. |

