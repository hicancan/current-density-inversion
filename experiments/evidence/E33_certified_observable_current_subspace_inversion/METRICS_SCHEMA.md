# Metrics Schema

`outputs/metrics.json` uses `research-ssot-metrics-v1`.

Important fields:

- `protocols.single_height`: certified inversion metrics for the single-height
  observation.
- `protocols.multi_height`: the same metrics after adding a second height.
- `stable_mode_count`: number of current modes above Fisher/SNR threshold.
- `dark_mode_count`: number of refused current modes.
- `certified_stable_rmse`: RMSE on the data-supported current projection.
- `full_naive_total_rmse`: RMSE of an unconstrained full least-squares inverse.
- `full_dark_hallucination_norm`: norm of dark-mode current hallucinated by the
  full inverse.

Core metric:

```text
M24_observable_current_subspace_fraction =
  #{i: sqrt(lambda_i) >= tau_obs} / #{all current modes}
```

Core certificate:

```text
lambda_i = phi_i^T A^T Sigma^-1 A phi_i
```

where `phi_i` is a normalized current mode. Low `lambda_i` means the current
mode is not data-supported under the configured observation model.
