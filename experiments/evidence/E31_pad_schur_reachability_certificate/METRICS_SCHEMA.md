# Metrics Schema

`outputs/metrics.json` uses `research-ssot-metrics-v1`.

Important fields:

- `pad_reachability`: exact Schur reachability ratios for each pad set.
- `pad_schur_certificate`: finite-difference magnetic signature certificate
  for the synthesized pad-pair active design.
- `negative_controls`: perimeter and non-optimized pad controls.
- `current_budget_law`: critical current for the synthesized pad design.
- `leakage_audit`: generated-domain and no-real-data discipline.

Core metric:

```text
M22_pad_schur_reachability_ratio = osc_P(L^+ d_e) / (d_e^T L^+ d_e)
```

Core certificate:

```text
Gamma_ij = delta_ij - z*sigma - rho_i - rho_j - tau
```

where signatures are produced by pad-feasible Schur-optimal pairs, not local
defect endpoint injection.

