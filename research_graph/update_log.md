# Update Log

## 2026-05-03 - Initial claim graph

Claim affected:
- C01_forward_sanity
- C02_single_plane_identifiability_boundary
- C03_unet_topology_baseline_boundary
- C04_inverse_crime_and_operator_gap
- C05_pypeec_solver_bridge
- C06_graph_hypothesis_system_identification
- C07_stacked_evidence_calibration
- C08_ood_refusal_safety
- C09_fewshot_family_adaptation
- C10_pdn_kcl_distribution_need
- C11_mechanism_level_explanation
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality
- C14_unlabeled_family_adaptation

Change type:
- claim graph initialization
- evidence registration
- boundary registration

Files changed:
- research graph SSOT
- claim-scoped experiment plans
- claim-scoped output summaries
- validation and rendering scripts

Evidence:
- nine evidence packages registered from forward sanity through real-data
  intake gates.

Metrics:
- graph integrity is enforced by `scripts/validate_graph.py`.

Claim status before:
- no graph state.

Claim status after:
- claim-centered graph state initialized.

Cannot claim:
- real QDM/NV validation.
- real CAD/Gerber/GDS validation.
- deployment-safe via/no-via diagnosis.
- mechanism-level explanation for accepted hidden rows.

Next required evidence:
- implement `D08_pdn_kcl_circuit_graph` with KCL, current closure, return path,
  and held-out/few-shot protocols.

