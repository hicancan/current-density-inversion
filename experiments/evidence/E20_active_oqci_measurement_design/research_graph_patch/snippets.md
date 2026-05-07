# E20 Active OQCI Research Graph Patch (proposed)

Do not merge directly. These are proposed SSOT updates. A Codex audit must
approve and merge them into the global files.

## experiments.yml (new entry)

```yaml
E20_active_oqci_measurement_design:
  title: "Active OQCI next-measurement selection for ambiguity reduction"
  claim: C10_pdn_kcl_distribution_need
  secondary_claims:
    - C02_single_plane_identifiability_boundary
    - C04_inverse_crime_and_operator_gap
    - C06_graph_hypothesis_system_identification
    - C13_calibration_protocol_reality
  data: [D11_chip_like_generated_pdn_family]
  physics:
    - P01_biot_savart_maxwell_forward
    - P04_divJ_source_sink_consistency
    - P05_kcl_node_conservation
    - P07_current_closure_loop
    - P08_return_path_completeness
  forward: [F02_centerline_biot_savart]
  observation: [O01_ideal_Bxyz, O02_Bz_only, O03_Bxy, O08_multi_height, O09_multi_state_excitation]
  representation: [R08_hypothesis_set, R09_posterior_candidate_set, R10_multilayer_chip_like_pdn_graph]
  algorithm: [A04_hypothesis_scorer, A12_bayesian_or_glrt_model_evidence]
  protocol:
    - S11_no_leakage_calibration_heldout
    - S12_conformal_or_selective_risk_protocol
  metrics:
    - M08_accepted_accuracy
    - M09_accepted_risk
    - M10_reject_rate
    - M13_family_generalization_gap
  outputs:
    - outputs/by_claim/C10_pdn_kcl_distribution_need/E20_ACTIVE_OQCI_EVIDENCE.md
  runtime:
    package_dir: experiments/evidence/E20_active_oqci_measurement_design
    run_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs"
    smoke_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke"
    test_command: "uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests"
    metrics_files:
      - experiments/evidence/E20_active_oqci_measurement_design/outputs/metrics.json
  result_summary: "E20 selects next measurements by multi-objective utility over candidate heights and component sets. Generated-domain evidence shows which candidates reduce ambiguity, but cannot claim real QDM/NV, CAD/GDS, or external solver validation."
  status: partial
  last_run: "2026-05-06"
```

## evidence_edges.yml (proposed new edges)

```yaml
- id: edge_E20_to_C10
  from: E20_active_oqci_measurement_design
  to: C10_pdn_kcl_distribution_need
  relation: supports
  strength: medium
  scope: "generated-domain active OQCI optimal next-measurement selection"
  caveat: "Generated-domain evidence only. Does not validate real QDM/NV, CAD/GDS, or external solver rows."
  evidence_files:
    - outputs/by_claim/C10_pdn_kcl_distribution_need/E20_ACTIVE_OQCI_EVIDENCE.md

- id: edge_E20_limits_C10
  from: E20_active_oqci_measurement_design
  to: C10_pdn_kcl_distribution_need
  relation: limits
  strength: strong
  scope: "generated-domain candidate measurement boundary"
  caveat: "E20 candidate selection and utility ordering are generated-domain only. Cannot claim that recommended measurements are hardware-feasible or transfer to real devices."

- id: edge_E20_to_C02
  from: E20_active_oqci_measurement_design
  to: C02_single_plane_identifiability_boundary
  relation: supports
  strength: medium
  scope: "generated-domain multi-height/candidate evidence for identifiability boundary"
  caveat: "Generated-domain evidence only. Candidate measurements reduce ambiguity in the generated domain but do not prove real multi-height protocol feasibility."

- id: edge_E20_to_C06
  from: E20_active_oqci_measurement_design
  to: C06_graph_hypothesis_system_identification
  relation: supports
  strength: medium
  scope: "generated-domain hypothesis distinguishability under candidate measurements"
  caveat: "Generated hypothesis basis and forward family only. Does not validate real CAD/Gerber/GDS graph inference."

- id: edge_E20_to_C13
  from: E20_active_oqci_measurement_design
  to: C13_calibration_protocol_reality
  relation: motivates
  strength: medium
  scope: "next-measurement policy defines what calibration data should be collected"
  caveat: "The candidate measurement recommendations are generated-domain; calibration protocol must be validated with real data."
```

## open_questions.md (proposed new/update)

```markdown
## OQ09: Can the optimal next measurement from generated-domain utility ranking improve ambiguity on real devices?

Status: active, E20 provides generated-domain ranking.

E20 ranks candidate measurements (heights + components) by multi-objective
utility. The open question is whether the top-ranked measurement class
reduces ambiguity when actually performed on a real QDM/NV setup with real
chip layouts.
```

## update_log.md (proposed entry)

```markdown
2026-05-06: E20 package implemented. Candidate measurement pool (heights,
components) with multi-objective utility ranking. Generated-domain only.
Pending Codex audit and research graph registration.
```
