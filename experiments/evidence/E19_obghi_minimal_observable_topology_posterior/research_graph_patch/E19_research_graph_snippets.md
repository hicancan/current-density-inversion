# E19 Research Graph Snippets

Apply these snippets only **after** running and auditing E19 locally.

Do not mark claims as stronger solely from blueprint text or unrun code.

## Suggested `research_graph/experiments.yml` entry

```yaml
E19_obghi_minimal_observable_topology_posterior:
  title: "OBGHI minimal observable topology posterior evidence"
  claim: C10_pdn_kcl_distribution_need
  secondary_claims:
    - C06_graph_hypothesis_system_identification
    - C02_single_plane_identifiability_boundary
    - C04_inverse_crime_and_operator_gap
  data:
    - D11_chip_like_generated_pdn_family
  physics:
    - P01_biot_savart_maxwell_forward
    - P04_divJ_source_sink_consistency
    - P05_kcl_node_conservation
    - P07_current_closure_loop
  forward:
    - F02_centerline_biot_savart
  observation:
    - O01_ideal_Bxyz
  representation:
    - R02_layer_current_plus_via_source_sink
    - R06_pdn_circuit_graph
    - R08_hypothesis_set
    - R09_posterior_candidate_set
  algorithm:
    - A04_hypothesis_scorer
    - A08_differentiable_forward_optimization
    - A12_bayesian_or_glrt_model_evidence
  protocol:
    - S02_variant_heldout
    - S11_no_leakage_calibration_heldout
    - S12_conformal_or_selective_risk_protocol
  metrics:
    - M01_field_l2_or_rmse
    - M04_kcl_residual
    - M08_accepted_accuracy
    - M09_accepted_risk
    - M10_reject_rate
    - M13_family_generalization_gap
    - M14_hidden_accept_risk
  outputs:
    - outputs/by_claim/C10_pdn_kcl_distribution_need/OBGHI_MINIMAL_POSTERIOR_EVIDENCE.md
    - outputs/by_claim/C06_graph_hypothesis_system_id/OBGHI_MINIMAL_POSTERIOR_EVIDENCE.md
    - outputs/by_claim/C02_identifiability_boundary/OBGHI_MINIMAL_POSTERIOR_EVIDENCE.md
  runtime:
    package_dir: experiments/evidence/E19_obghi_minimal_observable_topology_posterior
    run_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs"
    smoke_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke"
    test_command: "uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests"
    metrics_files:
      - experiments/evidence/E19_obghi_minimal_observable_topology_posterior/outputs/metrics.json
  result_summary: "Fill after local audit. Generated-domain OBGHI posterior topology inference over H0/H1/H2/H3 explanations; cannot claim real validation."
  status: planned
  last_run: null
```

## Suggested evidence edges

Use `supports` only if the run passes and the failure modes are audited.
Otherwise use `motivates`, `limits`, or `requires`.

```yaml
- evidence: E19_obghi_minimal_observable_topology_posterior
  claim: C10_pdn_kcl_distribution_need
  relation: motivates
  strength: planned
  scope: generated-domain minimal OBGHI slice
  caveats:
    - generated-domain only
    - no real CAD/Gerber/GDS validation
    - no external solver validation
    - no real QDM/NV validation

- evidence: E19_obghi_minimal_observable_topology_posterior
  claim: C06_graph_hypothesis_system_identification
  relation: motivates
  strength: planned
  scope: posterior topology/hypothesis scoring
  caveats:
    - hypothesis set is small
    - generated observation model only
```

## Suggested output report path

After run, copy or summarize `outputs/RUN_REPORT.md` to:

```text
outputs/by_claim/C10_pdn_kcl_distribution_need/OBGHI_MINIMAL_POSTERIOR_EVIDENCE.md
```

Keep the `cannot_claim` block unchanged unless real/external evidence exists.
