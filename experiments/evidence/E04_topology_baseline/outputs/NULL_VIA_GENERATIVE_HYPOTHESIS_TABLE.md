# Null-Via Generative Hypothesis Scoring

- enabled: `True`
- used for PyPEEC threshold selection: `False`
- used for PyPEEC calibration: `False`
- boundary: Generative hypothesis scoring compares explicit H1(with predicted s1) and H0(same prediction with s1 zeroed) re-forward energies. It is a frozen PyPEEC diagnostic and does not select thresholds.

Positive `Delta evidence H1-H0` means the explicit H1 model with predicted `s1` has lower energy than the H0 model with `s1=0`.

## Summary

| model | rows | AUC | mean DeltaE | H1 favored | H1 precision | H1 recall | H1 F1 | no-via H1 FP | mean uncertainty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 400 | 0.646 | -0.035 | 0.275 | 0.591 | 0.325 | 0.419 | 0.225 | 0.949 |
| `unet_topology_soft_loss` | 400 | 0.671 | 0.004 | 0.450 | 0.628 | 0.565 | 0.595 | 0.335 | 0.958 |
| `unet_topology_two_stage_refined` | 400 | 0.615 | 0.027 | 0.680 | 0.533 | 0.725 | 0.614 | 0.635 | 0.962 |

## Calibration Rows

| model | bin | n | score min | score max | score mean | observed true-via rate | observed no-via rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 1 | 67 | -0.178 | -0.092 | -0.119 | 0.299 | 0.701 |
| `unet_no_topology` | 2 | 66 | -0.092 | -0.064 | -0.078 | 0.333 | 0.667 |
| `unet_no_topology` | 3 | 67 | -0.064 | -0.034 | -0.048 | 0.478 | 0.522 |
| `unet_no_topology` | 4 | 67 | -0.033 | -0.011 | -0.023 | 0.627 | 0.373 |
| `unet_no_topology` | 5 | 66 | -0.011 | 0.020 | 0.004 | 0.652 | 0.348 |
| `unet_no_topology` | 6 | 67 | 0.020 | 0.160 | 0.055 | 0.612 | 0.388 |
| `unet_topology_soft_loss` | 1 | 67 | -0.157 | -0.048 | -0.072 | 0.284 | 0.716 |
| `unet_topology_soft_loss` | 2 | 66 | -0.048 | -0.026 | -0.037 | 0.333 | 0.667 |
| `unet_topology_soft_loss` | 3 | 67 | -0.026 | -0.006 | -0.016 | 0.552 | 0.448 |
| `unet_topology_soft_loss` | 4 | 67 | -0.005 | 0.015 | 0.005 | 0.448 | 0.552 |
| `unet_topology_soft_loss` | 5 | 66 | 0.015 | 0.056 | 0.038 | 0.682 | 0.318 |
| `unet_topology_soft_loss` | 6 | 67 | 0.056 | 0.309 | 0.103 | 0.701 | 0.299 |
| `unet_topology_two_stage_refined` | 1 | 67 | -0.082 | -0.017 | -0.034 | 0.343 | 0.657 |
| `unet_topology_two_stage_refined` | 2 | 66 | -0.016 | 8.724e-04 | -0.006 | 0.515 | 0.485 |
| `unet_topology_two_stage_refined` | 3 | 67 | 0.002 | 0.021 | 0.013 | 0.373 | 0.627 |
| `unet_topology_two_stage_refined` | 4 | 67 | 0.021 | 0.040 | 0.031 | 0.522 | 0.478 |
| `unet_topology_two_stage_refined` | 5 | 66 | 0.040 | 0.065 | 0.051 | 0.591 | 0.409 |
| `unet_topology_two_stage_refined` | 6 | 67 | 0.065 | 0.290 | 0.106 | 0.657 | 0.343 |

## Highest-Margin Rows

| case | type | model | true via | candidate | DeltaE H1-H0 | E(H1) | E(H0) | physical gain | artifact prox | decision |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `multi_via_route__v01` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.309 | 1.338 | 1.647 | 0.026 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route__v01` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.290 | 1.304 | 1.594 | 0.022 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background__v03` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | 0.232 | 1.303 | 1.534 | 0.005 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route__v03` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.215 | 1.530 | 1.745 | 0.009 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.203 | 1.146 | 1.349 | 0.026 | 0.500 | `generative_h1_true_via_favored` |
| `multi_via_route` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.201 | 1.175 | 1.376 | 0.029 | 0.500 | `generative_h1_true_via_favored` |
| `dense_via_background__v01` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | 0.199 | 1.372 | 1.571 | 0.007 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background__v03` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | yes | 0.189 | 1.287 | 1.475 | 0.005 | 1.000 | `generative_h1_true_via_favored` |
| `no_via_background__v09` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.187 | 1.396 | 1.583 | 0.002 | 1.000 | `generative_h1_true_via_favored` |
| `no_via_background__v74` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.187 | 1.396 | 1.583 | 0.002 | 1.000 | `generative_h1_true_via_favored` |
| `two_layer_route_with_via` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | 0.184 | 1.422 | 1.606 | 0.002 | 1.000 | `generative_h1_true_via_favored` |
| `single_via` | `canonical` | `unet_no_topology` | yes | yes | -0.178 | 3.845 | 3.667 | -0.121 | 0.000 | `generative_h0_artifact_favored` |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_no_topology` | no | yes | -0.175 | 1.526 | 1.352 | 1.718e-04 | 1.000 | `generative_h0_artifact_favored` |
| `multi_via_route__v03` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.173 | 1.529 | 1.702 | 0.009 | 1.000 | `generative_h1_true_via_favored` |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_no_topology` | no | yes | -0.172 | 1.827 | 1.655 | 0.004 | 1.000 | `generative_h0_artifact_favored` |
| `no_via_background__v72` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.172 | 1.391 | 1.563 | 1.945e-04 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background__v02` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | 0.170 | 1.394 | 1.564 | 0.004 | 1.000 | `generative_h1_true_via_favored` |
| `no_via_background__v59` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.160 | 1.287 | 1.446 | 9.823e-04 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route__v03` | `multi_via` | `unet_no_topology` | yes | yes | 0.160 | 1.766 | 1.926 | 0.014 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background__v29` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.159 | 1.498 | 1.340 | -0.005 | 1.000 | `generative_h0_artifact_favored` |
| `two_layer_route_with_via__v16` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | -0.157 | 1.236 | 1.079 | 3.247e-04 | 1.000 | `generative_h0_artifact_favored` |
| `no_via_background__v24` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.156 | 1.457 | 1.613 | 0.001 | 1.000 | `generative_h1_true_via_favored` |
| `no_via_background__v59` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.156 | 1.235 | 1.391 | 0.005 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background__v01` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | yes | 0.155 | 1.363 | 1.518 | 0.006 | 1.000 | `generative_h1_true_via_favored` |
| `no_via_background__v09` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.154 | 1.373 | 1.527 | 0.005 | 1.000 | `generative_h1_true_via_favored` |
| `no_via_background__v74` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.154 | 1.373 | 1.527 | 0.005 | 1.000 | `generative_h1_true_via_favored` |
| `no_via_background__v25` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.152 | 1.297 | 1.449 | 3.109e-04 | 1.000 | `generative_h1_true_via_favored` |
| `two_layer_route_with_via__v01` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | 0.151 | 1.464 | 1.615 | 0.008 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | yes | 0.151 | 1.222 | 1.373 | 0.005 | 1.000 | `generative_h1_true_via_favored` |
| `trace_with_return_path__v08` | `return_path` | `unet_no_topology` | yes | yes | -0.150 | 1.408 | 1.258 | 0.015 | 0.500 | `generative_h0_artifact_favored` |
| `no_via_background__v58` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.150 | 1.233 | 1.383 | 4.315e-04 | 1.000 | `generative_h1_true_via_favored` |
| `two_layer_route_with_via` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.149 | 1.403 | 1.553 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_no_topology` | no | yes | -0.148 | 1.477 | 1.329 | 0.003 | 0.000 | `generative_low_margin_refusal` |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.148 | 1.086 | 0.938 | -0.012 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v87` | `no_via_background` | `unet_no_topology` | no | yes | -0.145 | 1.226 | 1.081 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_no_topology` | no | yes | -0.144 | 1.345 | 1.201 | -2.581e-05 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v50` | `no_via_background` | `unet_no_topology` | no | yes | -0.143 | 1.762 | 1.619 | -0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v30` | `multi_via` | `unet_no_topology` | yes | yes | -0.142 | 1.723 | 1.581 | -0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v17` | `l1_jog` | `unet_no_topology` | yes | yes | -0.141 | 1.421 | 1.280 | -0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v58` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.141 | 1.296 | 1.438 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v16` | `l1_jog` | `unet_no_topology` | yes | yes | -0.141 | 1.544 | 1.404 | 0.012 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v17` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | -0.140 | 1.174 | 1.034 | -0.011 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v72` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.139 | 1.370 | 1.510 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v27` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.139 | 1.396 | 1.535 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v10` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.138 | 1.357 | 1.495 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_no_topology` | no | yes | -0.138 | 1.949 | 1.811 | 8.385e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v10` | `no_via_background` | `unet_no_topology` | no | yes | 0.138 | 1.792 | 1.930 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_no_topology` | no | yes | -0.137 | 1.399 | 1.262 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_no_topology` | no | yes | -0.136 | 1.496 | 1.359 | -0.003 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v73` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.136 | 1.274 | 1.410 | -0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v25` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.136 | 1.259 | 1.395 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v73` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.136 | 1.224 | 1.360 | -4.372e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v16` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.134 | 1.542 | 1.408 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | 0.134 | 1.296 | 1.430 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_no_topology` | no | yes | 0.133 | 1.788 | 1.921 | 0.023 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v28` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | -0.131 | 1.362 | 1.231 | -0.005 | 0.500 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v24` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.131 | 1.427 | 1.559 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_no_topology` | no | yes | -0.131 | 1.932 | 1.801 | -6.131e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v18` | `multi_via` | `unet_no_topology` | yes | yes | -0.131 | 1.452 | 1.321 | -0.006 | 0.500 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v19` | `l1_jog` | `unet_no_topology` | yes | yes | -0.131 | 1.350 | 1.220 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v23` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.128 | 1.191 | 1.063 | 0.003 | 0.000 | `generative_low_margin_refusal` |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_no_topology` | no | yes | -0.127 | 1.408 | 1.281 | -0.005 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v27` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.125 | 1.366 | 1.491 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_no_topology` | no | yes | -0.124 | 1.581 | 1.456 | 0.004 | 0.000 | `generative_low_margin_refusal` |
| `trace_with_return_path__v68` | `return_path` | `unet_no_topology` | yes | yes | -0.124 | 1.847 | 1.723 | 0.034 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_no_topology` | no | yes | -0.122 | 2.005 | 1.883 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v51` | `no_via_background` | `unet_no_topology` | no | yes | -0.122 | 1.735 | 1.614 | -0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v02` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | yes | 0.121 | 1.396 | 1.517 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_no_topology` | no | yes | -0.120 | 1.397 | 1.277 | -0.002 | 0.000 | `generative_low_margin_refusal` |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.119 | 1.329 | 1.210 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v26` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.118 | 1.426 | 1.544 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_no_topology` | no | yes | -0.118 | 1.783 | 1.665 | 0.016 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v12` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.118 | 1.365 | 1.247 | -0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v11` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.118 | 1.560 | 1.678 | -0.014 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v26` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.118 | 1.560 | 1.678 | -0.014 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_no_topology` | no | yes | -0.117 | 1.436 | 1.319 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v66` | `no_via_background` | `unet_no_topology` | no | yes | -0.116 | 1.163 | 1.047 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v58` | `return_path` | `unet_no_topology` | yes | yes | -0.116 | 1.269 | 1.153 | 0.009 | 0.500 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v98` | `return_path` | `unet_no_topology` | yes | yes | -0.116 | 1.269 | 1.153 | 0.009 | 0.500 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v85` | `no_via_background` | `unet_no_topology` | no | yes | -0.114 | 1.382 | 1.268 | 0.002 | 0.000 | `generative_low_margin_refusal` |
| `dense_via_background__v01` | `dense_via_background` | `unet_no_topology` | yes | yes | 0.114 | 1.864 | 1.978 | 0.010 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v17` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.114 | 1.399 | 1.285 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v53` | `no_via_background` | `unet_no_topology` | no | yes | -0.114 | 1.481 | 1.368 | 0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v56` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.114 | 1.277 | 1.391 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v01` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.113 | 1.454 | 1.567 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_no_topology` | no | yes | -0.113 | 1.474 | 1.360 | 0.005 | 0.000 | `generative_low_margin_refusal` |
| `multi_via_route__v31` | `multi_via` | `unet_no_topology` | yes | yes | -0.113 | 1.680 | 1.567 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v02` | `dense_via_background` | `unet_no_topology` | yes | yes | 0.113 | 1.763 | 1.876 | 0.017 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v49` | `return_path` | `unet_no_topology` | yes | yes | -0.113 | 1.296 | 1.183 | 0.013 | 0.500 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v20` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.112 | 2.122 | 2.234 | 0.048 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v76` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.112 | 2.229 | 2.341 | 0.052 | 1.000 | `no_candidate` |
| `bend_artifact_trace__v29` | `bend_artifact` | `unet_no_topology` | no | yes | -0.111 | 1.863 | 1.752 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v26` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.111 | 1.389 | 1.500 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v04` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.111 | 1.735 | 1.846 | 0.019 | 1.000 | `no_candidate` |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_no_topology` | no | yes | -0.110 | 1.498 | 1.388 | 8.354e-04 | 0.000 | `generative_low_margin_refusal` |
| `multi_via_route__v21` | `multi_via` | `unet_no_topology` | yes | yes | -0.110 | 1.615 | 1.504 | 0.001 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v56` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.108 | 1.333 | 1.442 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v10` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.108 | 1.338 | 1.446 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.107 | 1.096 | 0.989 | -0.014 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v13` | `no_via_background` | `unet_no_topology` | no | yes | -0.106 | 1.398 | 1.291 | -0.004 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v93` | `no_via_background` | `unet_no_topology` | no | yes | -0.106 | 1.398 | 1.291 | -0.004 | 0.000 | `generative_low_margin_refusal` |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_no_topology` | no | yes | -0.106 | 2.154 | 2.048 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v30` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.106 | 3.268 | 3.373 | 0.067 | 1.000 | `no_candidate` |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.106 | 1.265 | 1.159 | -0.012 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v01` | `multi_via` | `unet_no_topology` | yes | yes | 0.106 | 1.831 | 1.937 | 0.015 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_topology_two_stage_refined` | no | yes | 0.106 | 1.166 | 1.272 | -0.009 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v65` | `no_via_background` | `unet_no_topology` | no | yes | -0.105 | 1.432 | 1.327 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v05` | `l1_jog` | `unet_no_topology` | yes | yes | -0.105 | 1.918 | 1.813 | -5.721e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.105 | 1.193 | 1.088 | 0.002 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v68` | `no_via_background` | `unet_no_topology` | no | yes | -0.105 | 1.538 | 1.433 | 0.014 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_no_topology` | no | yes | -0.105 | 1.751 | 1.647 | -0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v02` | `multi_via` | `unet_no_topology` | yes | yes | 0.104 | 1.923 | 2.026 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v54` | `bend_artifact` | `unet_no_topology` | no | yes | -0.104 | 1.512 | 1.408 | 0.017 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_no_topology` | no | yes | -0.103 | 1.501 | 1.398 | -0.001 | 0.000 | `generative_low_margin_refusal` |
| `trace_with_return_path__v06` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.103 | 3.277 | 3.380 | 0.068 | 1.000 | `no_candidate` |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_no_topology` | no | yes | -0.102 | 1.257 | 1.155 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v55` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.102 | 1.653 | 1.755 | 0.011 | 1.000 | `no_candidate` |
| `trace_with_return_path__v18` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.102 | 2.010 | 2.112 | 0.030 | 1.000 | `no_candidate` |
| `no_via_background__v36` | `no_via_background` | `unet_no_topology` | no | yes | -0.101 | 1.494 | 1.393 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_no_topology` | no | yes | -0.101 | 1.992 | 1.891 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v70` | `no_via_background` | `unet_no_topology` | no | yes | -0.101 | 1.356 | 1.255 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v57` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.100 | 1.428 | 1.528 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v40` | `no_via_background` | `unet_no_topology` | no | yes | -0.100 | 1.516 | 1.415 | -0.010 | 0.000 | `generative_low_margin_refusal` |
| `trace_with_return_path__v31` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.098 | 3.206 | 3.304 | 0.059 | 1.000 | `no_candidate` |
| `no_via_background__v67` | `no_via_background` | `unet_no_topology` | no | yes | -0.098 | 1.191 | 1.093 | 0.004 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v58` | `no_via_background` | `unet_no_topology` | no | yes | 0.098 | 1.672 | 1.770 | 0.011 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v19` | `multi_via` | `unet_no_topology` | yes | yes | -0.098 | 1.297 | 1.199 | 0.002 | 0.500 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v01` | `no_via_background` | `unet_no_topology` | no | yes | -0.097 | 1.738 | 1.641 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v81` | `no_via_background` | `unet_no_topology` | no | yes | -0.097 | 1.738 | 1.641 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v20` | `no_via_background` | `unet_no_topology` | no | yes | -0.097 | 1.436 | 1.339 | 7.176e-04 | 0.000 | `generative_low_margin_refusal` |
| `dense_via_background__v03` | `dense_via_background` | `unet_no_topology` | yes | yes | 0.096 | 1.722 | 1.818 | 0.017 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v64` | `no_via_background` | `unet_no_topology` | no | yes | -0.096 | 1.199 | 1.103 | 0.007 | 0.000 | `generative_low_margin_refusal` |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.096 | 1.265 | 1.169 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v39` | `no_via_background` | `unet_no_topology` | no | yes | -0.096 | 1.307 | 1.211 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v20` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.095 | 2.154 | 2.248 | 0.061 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v02` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.094 | 1.249 | 1.343 | 0.012 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v03` | `no_via_background` | `unet_no_topology` | no | yes | -0.094 | 1.834 | 1.740 | -0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v83` | `no_via_background` | `unet_no_topology` | no | yes | -0.094 | 1.834 | 1.740 | -0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v11` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.094 | 1.531 | 1.625 | -0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v26` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.094 | 1.531 | 1.625 | -0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v08` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | 0.094 | 1.579 | 1.673 | -0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v88` | `no_via_background` | `unet_no_topology` | no | yes | -0.093 | 1.322 | 1.229 | -0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_no_topology` | no | yes | -0.093 | 1.433 | 1.340 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v64` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.093 | 1.263 | 1.170 | -0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_topology_two_stage_refined` | no | yes | 0.093 | 1.010 | 1.103 | -0.009 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v57` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.092 | 1.394 | 1.486 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_no_topology` | no | yes | -0.092 | 2.169 | 2.077 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v54` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.092 | 1.718 | 1.810 | 0.011 | 1.000 | `no_candidate` |
| `bend_artifact_trace__v73` | `bend_artifact` | `unet_topology_two_stage_refined` | no | yes | 0.092 | 1.050 | 1.142 | 0.012 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v04` | `bend_artifact` | `unet_no_topology` | no | yes | -0.092 | 1.577 | 1.485 | 0.016 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v77` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.092 | 2.282 | 2.374 | 0.049 | 0.500 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v52` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.091 | 2.590 | 2.681 | 0.043 | 1.000 | `no_candidate` |
| `trace_with_return_path__v55` | `return_path` | `unet_no_topology` | yes | no | 0.091 | 2.414 | 2.506 | 0.015 | 1.000 | `no_candidate` |
| `trace_with_return_path__v54` | `return_path` | `unet_no_topology` | yes | no | 0.091 | 2.439 | 2.530 | 0.017 | 1.000 | `no_candidate` |
| `trace_with_return_path__v38` | `return_path` | `unet_no_topology` | yes | yes | -0.090 | 1.722 | 1.632 | 0.033 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v25` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.090 | 2.247 | 2.337 | 0.051 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v80` | `no_via_background` | `unet_no_topology` | no | yes | -0.090 | 1.857 | 1.766 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v89` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.090 | 1.162 | 1.072 | -0.009 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v89` | `no_via_background` | `unet_no_topology` | no | yes | -0.090 | 1.205 | 1.115 | -0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_no_topology` | no | yes | -0.090 | 1.701 | 1.611 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v02` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.090 | 1.570 | 1.659 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_no_topology` | no | yes | -0.089 | 1.334 | 1.244 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v21` | `no_via_background` | `unet_no_topology` | no | yes | -0.089 | 1.388 | 1.299 | 0.010 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v86` | `no_via_background` | `unet_no_topology` | no | yes | -0.089 | 1.388 | 1.299 | 0.010 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_no_topology` | no | yes | -0.089 | 1.399 | 1.310 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v21` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.088 | 1.312 | 1.224 | 0.008 | 0.000 | `generative_low_margin_refusal` |
| `multi_via_route__v22` | `multi_via` | `unet_no_topology` | yes | yes | -0.088 | 1.321 | 1.232 | -0.004 | 0.500 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v22` | `no_via_background` | `unet_topology_two_stage_refined` | no | no | 0.088 | 0.977 | 1.066 | -0.001 | 0.000 | `no_candidate` |
| `multi_via_route__v23` | `multi_via` | `unet_topology_two_stage_refined` | yes | no | 0.088 | 0.922 | 1.010 | 0.002 | 0.000 | `no_candidate` |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_no_topology` | no | yes | -0.088 | 1.594 | 1.506 | 0.015 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v02` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | 0.087 | 1.301 | 1.389 | 0.014 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v65` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.087 | 2.073 | 2.160 | 0.046 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v73` | `no_via_background` | `unet_no_topology` | no | yes | 0.087 | 1.682 | 1.770 | 0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v65` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.087 | 2.097 | 2.185 | 0.059 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v21` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.087 | 1.051 | 1.138 | 0.051 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v66` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.087 | 1.051 | 1.138 | 0.051 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v86` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.087 | 1.051 | 1.138 | 0.051 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v54` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.087 | 1.733 | 1.820 | 0.016 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v30` | `return_path` | `unet_topology_soft_loss` | yes | no | 0.086 | 3.287 | 3.373 | 0.037 | 1.000 | `no_candidate` |
| `bend_artifact_trace__v46` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.086 | 0.997 | 0.911 | -0.007 | 1.000 | `generative_ambiguous_artifact_zone` |

Interpretation: this is still diagnostic. It upgrades rule evidence into an explicit H1-vs-H0 re-forward energy comparison, but it does not claim a solved detector.
