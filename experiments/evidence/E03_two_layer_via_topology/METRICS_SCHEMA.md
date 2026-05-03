# exp03 Metrics Schema

## Core Physics

- `superposition_rel_l2_error`: relative L2 error between total field and grouped layer/via field sum. Should be near machine precision.
- `via.Bz_over_Bxy_max_ratio`: max `|Bz| / |Bxy|` for the ideal vertical via contribution.
- `topology.residual_to_div_norm_ratio_layer1/2`: finite-volume topology residual after adding/removing via source term, normalized by the divergence norm before topology correction.

## Detection

- `matched_filter.*`: center-via easy-case matched-filter results.
- `background_swamping_stress.*`: hard case with strong sheet background. This is the primary via swamping gate.
- `raw_to_residual_localization_error_ratio`: raw total-field localization error divided by oracle residual localization error.

## Benchmark Dataset

- `benchmark_dataset.B_obs_shape`: noisy magnetic observation shape `[N,H,W,3]`.
- `benchmark_dataset.truth_shape`: label shape `[N,5,H,W]` with channels `J1x,J1y,J2x,J2y,s1`.
- `benchmark_dataset.split_counts`: number of samples in `train/val/test/ood`.
- `benchmark_dataset.truth_channel_l2_norms_by_split`: per-split truth energy for each output channel. `J1y` and `J2y` should be nonzero in train/test.
- `benchmark_dataset.route_kind_counts`: per-split route-type counts. ID splits include `straight`, `l1_jog`, `l2_jog`, `both_jog`, `multi_via`, and `no_via`; OOD uses background stress variants including dense-via and no-via cases.
- `benchmark_dataset.recoverability_summary`: split-wise via/no-via fractions,
  multi/dense-via fraction, background-stress fraction, and observation SNR
  proxy. This prevents silently turning the benchmark into only easy via cases.
- `forward_realism_probe`: held-out finite-width filament plus weak
  ground-return surrogate gap relative to the centerline operator. It quantifies
  a synthetic forward gap without replacing FEM/FastHenry validation.

## Gates

- `all_acceptance_gates_passed`: true only when superposition, via direction,
  finite-volume topology, stress detection, dataset-shape,
  truth-channel-diversity, route-kind-diversity, recoverability-health, and
  forward-realism-probe gates pass.
