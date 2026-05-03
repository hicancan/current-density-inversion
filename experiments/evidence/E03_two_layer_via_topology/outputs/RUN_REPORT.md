# RUN_REPORT

## Summary

Experiment exp03 completed.

Acceptance gates: `PASS`

- field_superposition_is_linear: PASS; value=4.068155483659732e-17; threshold=relative_l2 < 1e-12
- vertical_via_has_no_bz: PASS; value=0.0; threshold=Bz/Bxy < 1e-10
- finite_volume_topology_cancels_internal_via: PASS; value=[0.0, 0.0]; threshold=both residual ratios < 1e-12
- stress_residual_filter_localizes_via: PASS; value=4.759858191164941e-06; threshold=residual localization error <= 2 pixels
- stress_raw_total_field_is_misleading: PASS; value=249.0138481123574; threshold=raw localization error > residual localization error
- formal_benchmark_has_required_splits: PASS; value={'ood': 128, 'test': 128, 'train': 512, 'val': 128}; threshold=train/val/test/ood are all present
- formal_benchmark_has_full_truth_maps: PASS; value=[896, 5, 49, 49]; threshold=truth channels are [J1x,J1y,J2x,J2y,s1]
- formal_benchmark_has_directional_current_diversity: PASS; value={'train': {'J1y': 1045.15478515625, 'J2y': 1036.4327392578125}, 'test': {'J1y': 518.7255859375, 'J2y': 519.7576904296875}}; threshold=train/test J1y and J2y truth norms are nonzero
- formal_benchmark_has_route_kind_diversity: PASS; value={'train': {'straight': 86, 'l1_jog': 86, 'l2_jog': 85, 'both_jog': 85, 'multi_via': 85, 'no_via': 85}, 'val': {'straight': 22, 'l1_jog': 22, 'l2_jog': 21, 'both_jog': 21, 'multi_via': 21, 'no_via': 21}, 'test': {'straight': 22, 'l1_jog': 22, 'l2_jog': 21, 'both_jog': 21, 'multi_via': 21, 'no_via': 21}, 'ood': {'both_jog_background': 43, 'dense_via_background': 43, 'no_via_background': 42}}; threshold=ID train/test include straight, l1_jog, l2_jog, both_jog, multi_via, no_via; OOD includes background stress variants
- benchmark_reports_recoverability_health: PASS; value={'ood': {'n': 128, 'via_present_fraction': 0.671875, 'no_via_fraction': 0.328125, 'multi_or_dense_via_fraction': 0.3359375, 'background_stress_fraction': 1.0, 'median_observation_snr_proxy': 15.546403884887695, 'min_observation_snr_proxy': 11.297666549682617}, 'test': {'n': 128, 'via_present_fraction': 0.8359375, 'no_via_fraction': 0.1640625, 'multi_or_dense_via_fraction': 0.1640625, 'background_stress_fraction': 0.0, 'median_observation_snr_proxy': 55.23963165283203, 'min_observation_snr_proxy': 36.49273681640625}, 'train': {'n': 512, 'via_present_fraction': 0.833984375, 'no_via_fraction': 0.166015625, 'multi_or_dense_via_fraction': 0.166015625, 'background_stress_fraction': 0.0, 'median_observation_snr_proxy': 57.4359016418457, 'min_observation_snr_proxy': 37.54959487915039}, 'val': {'n': 128, 'via_present_fraction': 0.8359375, 'no_via_fraction': 0.1640625, 'multi_or_dense_via_fraction': 0.1640625, 'background_stress_fraction': 0.0, 'median_observation_snr_proxy': 59.95231246948242, 'min_observation_snr_proxy': 38.7739372253418}}; threshold=test has via/no-via diversity and OOD has background stress
- finite_width_return_surrogate_gap_is_quantified: PASS; value=0.10630371449143175; threshold=median surrogate gap is finite and > 1%

## Key metrics

- Superposition relative L2 error: `4.068e-17`
- Via Bz/Bxy max ratio: `0.000e+00`
- Via-to-sheet Bxy energy ratio: `1.073e-01`
- Residual matched-filter localization error: `0.00 µm`
- Raw matched-filter localization error: `0.00 µm`
- Topology residual ratio layer1: `0.000e+00`
- Topology residual ratio layer2: `0.000e+00`
- Stress raw localization error: `1185.27 µm`
- Stress residual localization error: `4.76 µm`
- Benchmark route kinds: `{'train': {'straight': 86, 'l1_jog': 86, 'l2_jog': 85, 'both_jog': 85, 'multi_via': 85, 'no_via': 85}, 'val': {'straight': 22, 'l1_jog': 22, 'l2_jog': 21, 'both_jog': 21, 'multi_via': 21, 'no_via': 21}, 'test': {'straight': 22, 'l1_jog': 22, 'l2_jog': 21, 'both_jog': 21, 'multi_via': 21, 'no_via': 21}, 'ood': {'both_jog_background': 43, 'dense_via_background': 43, 'no_via_background': 42}}`
- Benchmark truth channel norms: `{'ood': {'J1x': 1218.6644287109375, 'J1y': 572.8372192382812, 'J2x': 1172.406494140625, 'J2y': 581.4647827148438, 's1': 227.14581298828125}, 'test': {'J1x': 1171.445556640625, 'J1y': 518.7255859375, 'J2x': 1213.01904296875, 'J2y': 519.7576904296875, 's1': 258.6656494140625}, 'train': {'J1x': 2383.669677734375, 'J1y': 1045.15478515625, 'J2x': 2363.389404296875, 'J2y': 1036.4327392578125, 's1': 520.3272094726562}, 'val': {'J1x': 1158.398681640625, 'J1y': 521.4226684570312, 'J2x': 1205.5458984375, 'J2y': 509.5070495605469, 's1': 256.1455078125}}`
- Recoverability summary: `{'ood': {'n': 128, 'via_present_fraction': 0.671875, 'no_via_fraction': 0.328125, 'multi_or_dense_via_fraction': 0.3359375, 'background_stress_fraction': 1.0, 'median_observation_snr_proxy': 15.546403884887695, 'min_observation_snr_proxy': 11.297666549682617}, 'test': {'n': 128, 'via_present_fraction': 0.8359375, 'no_via_fraction': 0.1640625, 'multi_or_dense_via_fraction': 0.1640625, 'background_stress_fraction': 0.0, 'median_observation_snr_proxy': 55.23963165283203, 'min_observation_snr_proxy': 36.49273681640625}, 'train': {'n': 512, 'via_present_fraction': 0.833984375, 'no_via_fraction': 0.166015625, 'multi_or_dense_via_fraction': 0.166015625, 'background_stress_fraction': 0.0, 'median_observation_snr_proxy': 57.4359016418457, 'min_observation_snr_proxy': 37.54959487915039}, 'val': {'n': 128, 'via_present_fraction': 0.8359375, 'no_via_fraction': 0.1640625, 'multi_or_dense_via_fraction': 0.1640625, 'background_stress_fraction': 0.0, 'median_observation_snr_proxy': 59.95231246948242, 'min_observation_snr_proxy': 38.7739372253418}}`
- Finite-width/return surrogate median forward gap: `0.106`

## Interpretation

This experiment verifies the minimum two-layer + via physics before neural inversion:

1. B-field decomposition is linear.
2. An ideal vertical via produces almost no Bz and mainly Bxy circulation.
3. Via detection is much easier after sheet-background subtraction; raw total-field matching can fail or shift, exposing the swamping risk.
4. The finite-volume topology residual cancels the via source/sink inside the FOV when boundary ports are excluded.
5. Layer template similarity remains high for small depth offsets, motivating later topology constraints and observability gates.
6. A finite-width/return-current surrogate creates a measurable forward gap,
   so same-family centerline synthetic performance must not be treated as
   real hardware validation.
