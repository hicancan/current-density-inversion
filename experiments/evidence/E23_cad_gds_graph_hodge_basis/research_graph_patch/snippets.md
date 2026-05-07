# E23 Proposed Research Graph Snippets

Do not apply to global SSOT files automatically. These are proposals
for manual review and merge by the research owner.

---

## Proposed experiment entry (append to experiments.yml)

```yaml
E23_cad_gds_graph_hodge_basis:
  title: "CAD/GDS-derived Graph-Hodge current basis evidence"
  claim: C06_graph_hypothesis_system_identification
  secondary_claims: [C10_pdn_kcl_distribution_need]
  data: [D09_cad_gerber_gds_like]
  physics:
    - P01_biot_savart_maxwell_forward
    - P04_divJ_source_sink_consistency
    - P05_kcl_node_conservation
    - P06_kvl_or_resistive_network_consistency
    - P07_current_closure_loop
    - P08_return_path_completeness
  forward: [F02_centerline_biot_savart]
  observation: [O01_ideal_Bxyz]
  representation:
    - R04_route_graph
    - R06_pdn_circuit_graph
    - R08_hypothesis_set
    - R10_multilayer_chip_like_pdn_graph
  algorithm:
    - A04_hypothesis_scorer
    - A08_differentiable_forward_optimization
  protocol:
    - S11_no_leakage_calibration_heldout
  metrics:
    - M01_field_l2_or_rmse
    - M03_topology_residual
    - M04_kcl_residual
    - M08_accepted_accuracy
    - M09_accepted_risk
    - M10_reject_rate
    - M16_predicted_kcl_residual
    - M17_predicted_current_closure_error
  outputs:
    - outputs/by_claim/C06_graph_hypothesis_system_id/GRAPH_HODGE_BASIS_EVIDENCE.md
    - outputs/by_claim/C10_pdn_kcl_distribution_need/GRAPH_HODGE_BASIS_EVIDENCE.md
  runtime:
    package_dir: experiments/evidence/E23_cad_gds_graph_hodge_basis
    run_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs"
    smoke_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke"
    test_command: "uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests"
    metrics_files:
      - experiments/evidence/E23_cad_gds_graph_hodge_basis/outputs/metrics.json
  result_summary: "Generated layout-derived Graph-Hodge basis decomposes edge-current space into port/loop/via/return/harmonic/gap/residual blocks with KCL validation and OQCI ambiguity comparison. Generated-domain evidence only; not real CAD/GDS validation."
  status: pending_review
  last_run: "2026-05-06"
```

## Proposed evidence edges (append to evidence_edges.yml)

```yaml
- id: edge_E23_to_C06
  from: E23_cad_gds_graph_hodge_basis
  to: C06_graph_hypothesis_system_identification
  relation: supports
  strength: medium
  scope: "generated layout-derived Graph-Hodge basis with KCL/closure/OQCI"
  caveat: "Generated-domain layout graphs only; does not validate real CAD/GDS import or graph inference."

- id: edge_E23_limits_C06
  from: E23_cad_gds_graph_hodge_basis
  to: C06_graph_hypothesis_system_identification
  relation: limits
  strength: strong
  scope: "generated layout graph boundary"
  caveat: "Layout graphs are simplified JSON schemas, not real CAD/Gerber/GDS files. Graph-Hodge prior is generated-domain only."

- id: edge_E23_to_C10
  from: E23_cad_gds_graph_hodge_basis
  to: C10_pdn_kcl_distribution_need
  relation: supports
  strength: medium
  scope: "generated KCL-constrained Graph-Hodge basis with return paths"
  caveat: "Return paths are simplified, no real board PDN. Forward is centerline Biot-Savart only."

- id: edge_E23_limits_C10
  from: E23_cad_gds_graph_hodge_basis
  to: C10_pdn_kcl_distribution_need
  relation: limits
  strength: strong
  scope: "generated graph basis boundary for PDN/KCL"
  caveat: "Graph-Hodge basis is constructed from generated layout graphs. Does not validate real CAD/GDS, external solvers, or real QDM/NV."
```

## Proposed node status suggestions

- `D09_cad_gerber_gds_like`: status could remain `partial` — E23 uses the same schema but adds Graph-Hodge decomposition.
- `R04_route_graph`: status could remain `implemented` — E23 builds graphs from the E14 schema.
- `R06_pdn_circuit_graph`: status could be upgraded from `partial` to `implemented` — E23 constructs full incidence matrix and KCL system.

## Open question proposal

```markdown
## OQ09: Can the Graph-Hodge basis resolve identifiability ambiguity under multi-height or multi-state observations?

Status: new, E23 provides single-height baseline.

E23 demonstrates that the Graph-Hodge basis reduces admissible current
space dimension. Open question: does this dimension reduction translate
to improved identifiability when combined with multi-height (E13) or
multi-state excitation observations?
```

## Do NOT apply

These are proposed updates only. The global `experiments.yml`,
`evidence_edges.yml`, `claims.yml`, `nodes.yml`, and `open_questions.md`
must NOT be modified until reviewed and approved by the research owner.
