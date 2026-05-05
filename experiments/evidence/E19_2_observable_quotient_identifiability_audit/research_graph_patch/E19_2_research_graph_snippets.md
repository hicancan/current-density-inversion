# E19.2 Research Graph Snippets

Apply after the run is audited.

## experiments.yml entry

```yaml
E19_2_observable_quotient_identifiability_audit:
  title: "Observable Quotient Current Inversion identifiability audit"
  claim: C10_pdn_kcl_distribution_need
  secondary_claims:
    - C06_graph_hypothesis_system_identification
    - C02_single_plane_identifiability_boundary
    - C04_inverse_crime_and_operator_gap
  data: [D11_chip_like_generated_pdn_family]
  physics: [P01_biot_savart_maxwell_forward]
  forward: [F02_centerline_biot_savart]
  observation: [O01_ideal_Bxyz, O08_multi_height]
  representation: [R08_hypothesis_set, R09_posterior_candidate_set]
  algorithm: [A04_hypothesis_scorer, A12_bayesian_or_glrt_model_evidence]
  protocol: [S11_no_leakage_calibration_heldout]
  metrics: [M08_accepted_accuracy, M09_accepted_risk, M10_reject_rate]
  outputs: []
  runtime:
    package_dir: experiments/evidence/E19_2_observable_quotient_identifiability_audit
    run_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs"
    smoke_command: "uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke"
    test_command: "uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests"
    metrics_files:
      - experiments/evidence/E19_2_observable_quotient_identifiability_audit/outputs/metrics.json
  result_summary: ""
  status: planned
  last_run: ""
```

## evidence_edges.yml entries

Add after metrics are audited.
