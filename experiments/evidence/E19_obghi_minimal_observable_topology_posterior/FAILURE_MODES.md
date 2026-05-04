# E19 Failure Modes

See `outputs/FAILURE_CASES.md` for per-case failure documentation.

## Systematic failure modes

1. **H1_via dominates H0_no_via (no-via false-positive)**: The via basis has
   enough flexibility to fit no-via background fields better than H0, creating
   overconfident via predictions on clean no-via cases.

2. **H2_model_gap posterior collapses to zero**: The gap basis uses simple
   Gaussian field-space patterns that do not match the gradient (registration)
   and Laplacian (standoff) model-gap data generation patterns. Additionally,
   the uniform per-hypothesis prior variance penalizes H2 relative to H0.

3. **H1_via dominates H3_return_path**: The return-path basis (4 deep-layer
   loop modes) is too small to overcome the via basis flexibility. H3 has
   non-zero posterior (mean 0.255) but never wins.

4. **No reject decisions**: The decision rule requires top_p < 0.45 or via-gap
   ambiguity for rejection. Neither condition triggers on the current
   parameterization, resulting in 0 reject decisions and 55 accepted cases.

## Comparison with E18 failure modes

| E18 failure | E19 equivalent |
|---|---|
| dense-via recall=0 | Not evaluated (pixel via detection not in this slice) |
| deep-layer misallocation >0.3 | Not evaluated (no layer assignment metric) |
| return-grid ambiguity | Partial: H3_return_path never wins |
| KCL-RMSE tradeoff | Not evaluated (no KCL constraint) |
