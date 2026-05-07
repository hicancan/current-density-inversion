# E27 Metrics Schema

Follows `research-ssot-metrics-v1` with E27-specific extensions.

## Top-level fields

| field | type | description |
|---|---|---|
| schema_version | string | `research-ssot-metrics-v1` |
| evidence_id | string | `E27_edge_defect_schur_magnetic_signature` |
| status | string | `passed`, `passed_with_limitations`, or `failed_sanity` |
| sherman_morrison_max_error | float | Max relative error SM vs direct |
| candidate_edge_sensitivity | object | Edge signal/gamma statistics |
| schur_state_info | object | Schur state design summary |
| signal_gamma_improvement | object | Improvement over baselines |
| baseline_summaries | array | Per-strategy summary rows |
| pairwise_gamma_summary | object | Pairwise defect discrimination |
| per_family_edge_gamma | object | Per-family gamma stats |
| consistent_set_metrics | object | Identifiability set analysis |
| cannot_claim | array | Explicit evidence boundary |

## Edge Gamma

```
Gamma_q = S_q - epsilon - rho_q - tau
```

where `S_q = ||W * Delta_Y_q||_2`, `epsilon` is noise sigma, `rho_q` is operator perturbation, `tau` is decision threshold.

## Pairwise Gamma

```
Gamma_qr = Delta_qr - epsilon - rho_q - rho_r - tau
```

where `Delta_qr = ||W * (Delta_Y_q - Delta_Y_r)||_2`.
