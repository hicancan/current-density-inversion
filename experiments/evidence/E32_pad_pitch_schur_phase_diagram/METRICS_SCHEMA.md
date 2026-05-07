# Metrics Schema

`outputs/metrics.json` uses `research-ssot-metrics-v1`.

Important fields:

- `phase_diagram.designs`: exact Schur reachability rows for each pad geometry.
- `phase_diagram.summary`: best/worst design summaries by category and stride.
- `barrier_certificate`: headline pad-pitch locality barrier metrics and gates.
- `leakage_audit`: generated-domain and no-real-data discipline.

Core metric:

```text
M23_pad_pitch_reachability_floor =
  min_e osc_P(L^+ d_e) / (d_e^T L^+ d_e)
```

Low `eta` is a physical active-mode reachability barrier for the pad set under
the current-budget model. It is not a magnetic finite-difference Gamma margin.
