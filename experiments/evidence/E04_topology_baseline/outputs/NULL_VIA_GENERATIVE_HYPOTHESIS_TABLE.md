# Null-Via Generative Hypothesis Scoring

- enabled: `True`
- used for PyPEEC threshold selection: `False`
- used for PyPEEC calibration: `False`
- boundary: Generative hypothesis scoring compares explicit H1(with predicted s1) and H0(same prediction with s1 zeroed) re-forward energies. It is a frozen PyPEEC diagnostic and does not select thresholds.

Positive `Delta evidence H1-H0` means the explicit H1 model with predicted `s1` has lower energy than the H0 model with `s1=0`.

## Summary

| model | rows | AUC | mean DeltaE | H1 favored | H1 precision | H1 recall | H1 F1 | no-via H1 FP | mean uncertainty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 400 | 0.620 | -0.035 | 0.235 | 0.596 | 0.280 | 0.381 | 0.190 | 0.949 |
| `unet_topology_soft_loss` | 400 | 0.705 | 0.001 | 0.463 | 0.708 | 0.655 | 0.681 | 0.270 | 0.952 |
| `unet_topology_two_stage_refined` | 400 | 0.687 | 0.026 | 0.693 | 0.574 | 0.795 | 0.667 | 0.590 | 0.960 |

## Calibration Rows

| model | bin | n | score min | score max | score mean | observed true-via rate | observed no-via rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 1 | 67 | -0.254 | -0.097 | -0.122 | 0.343 | 0.657 |
| `unet_no_topology` | 2 | 66 | -0.097 | -0.060 | -0.076 | 0.364 | 0.636 |
| `unet_no_topology` | 3 | 67 | -0.060 | -0.035 | -0.046 | 0.448 | 0.552 |
| `unet_no_topology` | 4 | 67 | -0.035 | -0.012 | -0.023 | 0.582 | 0.418 |
| `unet_no_topology` | 5 | 66 | -0.012 | 0.013 | -0.002 | 0.712 | 0.288 |
| `unet_no_topology` | 6 | 67 | 0.016 | 0.167 | 0.060 | 0.552 | 0.448 |
| `unet_topology_soft_loss` | 1 | 67 | -0.160 | -0.058 | -0.085 | 0.343 | 0.657 |
| `unet_topology_soft_loss` | 2 | 66 | -0.057 | -0.033 | -0.045 | 0.318 | 0.682 |
| `unet_topology_soft_loss` | 3 | 67 | -0.033 | -0.007 | -0.020 | 0.239 | 0.761 |
| `unet_topology_soft_loss` | 4 | 67 | -0.007 | 0.025 | 0.009 | 0.582 | 0.418 |
| `unet_topology_soft_loss` | 5 | 66 | 0.025 | 0.064 | 0.042 | 0.712 | 0.288 |
| `unet_topology_soft_loss` | 6 | 67 | 0.064 | 0.214 | 0.107 | 0.806 | 0.194 |
| `unet_topology_two_stage_refined` | 1 | 67 | -0.094 | -0.022 | -0.040 | 0.328 | 0.672 |
| `unet_topology_two_stage_refined` | 2 | 66 | -0.021 | 0.001 | -0.008 | 0.348 | 0.652 |
| `unet_topology_two_stage_refined` | 3 | 67 | 0.002 | 0.022 | 0.012 | 0.403 | 0.597 |
| `unet_topology_two_stage_refined` | 4 | 67 | 0.022 | 0.041 | 0.032 | 0.507 | 0.493 |
| `unet_topology_two_stage_refined` | 5 | 66 | 0.041 | 0.069 | 0.056 | 0.545 | 0.455 |
| `unet_topology_two_stage_refined` | 6 | 67 | 0.069 | 0.188 | 0.106 | 0.866 | 0.134 |

## Highest-Margin Rows

| case | type | model | true via | candidate | DeltaE H1-H0 | E(H1) | E(H0) | physical gain | artifact prox | decision |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `single_via` | `canonical` | `unet_no_topology` | yes | yes | -0.254 | 3.586 | 3.332 | -0.214 | 0.000 | `generative_h0_artifact_favored` |
| `multi_via_route__v03` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.214 | 1.577 | 1.791 | 0.010 | 1.000 | `generative_h1_true_via_favored` |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_no_topology` | no | yes | -0.195 | 1.453 | 1.258 | -3.071e-04 | 1.000 | `generative_h0_artifact_favored` |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_no_topology` | no | yes | -0.190 | 1.771 | 1.581 | -0.002 | 1.000 | `generative_h0_artifact_favored` |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_no_topology` | no | yes | -0.189 | 1.525 | 1.337 | -7.663e-04 | 1.000 | `generative_h0_artifact_favored` |
| `no_via_background__v56` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.188 | 1.226 | 1.414 | 0.016 | 1.000 | `generative_h1_true_via_favored` |
| `two_layer_route_with_via__v01` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | 0.180 | 1.579 | 1.759 | 0.011 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route__v01` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.179 | 1.412 | 1.591 | 0.024 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route__v01` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.178 | 1.446 | 1.624 | 0.028 | 1.000 | `generative_h1_true_via_favored` |
| `two_layer_route_with_via__v08` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | 0.174 | 1.332 | 1.507 | 9.313e-04 | 1.000 | `generative_h1_true_via_favored` |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_no_topology` | no | yes | -0.173 | 1.340 | 1.167 | -0.002 | 0.000 | `generative_h0_artifact_favored` |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_no_topology` | no | yes | -0.167 | 1.435 | 1.268 | 0.005 | 1.000 | `generative_h0_artifact_favored` |
| `multi_via_route__v03` | `multi_via` | `unet_no_topology` | yes | yes | 0.167 | 1.875 | 2.042 | 0.002 | 1.000 | `generative_h1_true_via_favored` |
| `two_layer_route_with_via__v08` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.167 | 1.279 | 1.445 | 0.003 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.165 | 1.226 | 1.391 | 0.019 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.162 | 1.256 | 1.418 | 0.023 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | yes | 0.162 | 1.186 | 1.348 | 0.013 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background__v28` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | -0.160 | 1.335 | 1.175 | -0.003 | 0.500 | `generative_h0_artifact_favored` |
| `no_via_background__v56` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.160 | 1.296 | 1.456 | 0.016 | 1.000 | `generative_h1_true_via_favored` |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.159 | 1.396 | 1.237 | -0.014 | 0.000 | `generative_h0_artifact_favored` |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.159 | 1.450 | 1.291 | -0.013 | 1.000 | `generative_h0_artifact_favored` |
| `two_layer_route_with_via__v16` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | -0.159 | 1.225 | 1.066 | 0.009 | 1.000 | `generative_h0_artifact_favored` |
| `trace_with_return_path__v07` | `return_path` | `unet_no_topology` | yes | yes | -0.158 | 1.856 | 1.698 | -0.010 | 1.000 | `generative_h0_artifact_favored` |
| `no_via_background__v87` | `no_via_background` | `unet_no_topology` | no | yes | -0.156 | 1.228 | 1.071 | 0.006 | 1.000 | `generative_h0_artifact_favored` |
| `two_layer_route_with_via__v01` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.156 | 1.563 | 1.719 | 0.011 | 1.000 | `generative_h1_true_via_favored` |
| `multi_via_route__v03` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.154 | 1.588 | 1.742 | 0.008 | 1.000 | `generative_h1_true_via_favored` |
| `dense_via_background__v01` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | 0.153 | 1.321 | 1.474 | 0.012 | 1.000 | `generative_h1_true_via_favored` |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_no_topology` | no | yes | -0.153 | 1.555 | 1.402 | 7.080e-04 | 1.000 | `generative_h0_artifact_favored` |
| `dense_via_background__v03` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | 0.151 | 1.286 | 1.438 | 0.006 | 1.000 | `generative_h1_true_via_favored` |
| `two_layer_route_with_via__v01` | `l1_jog` | `unet_no_topology` | yes | yes | 0.148 | 1.867 | 2.015 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | 0.148 | 1.245 | 1.393 | 0.013 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v17` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.145 | 1.317 | 1.171 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v33` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.145 | 3.063 | 3.209 | 0.064 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v73` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.145 | 3.063 | 3.209 | 0.064 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v32` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.144 | 3.181 | 3.325 | 0.071 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v72` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.144 | 3.181 | 3.325 | 0.071 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v05` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.144 | 2.716 | 2.860 | 0.039 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v25` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.143 | 1.458 | 1.601 | -0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v19` | `return_path` | `unet_topology_soft_loss` | yes | yes | -0.143 | 1.768 | 1.625 | 0.020 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v03` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.143 | 3.068 | 3.211 | 0.061 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v83` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.143 | 3.068 | 3.211 | 0.061 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v85` | `bend_artifact` | `unet_no_topology` | no | yes | -0.143 | 1.420 | 1.277 | -0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v03` | `dense_via_background` | `unet_no_topology` | yes | yes | 0.141 | 1.688 | 1.829 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v19` | `l1_jog` | `unet_no_topology` | yes | yes | -0.141 | 1.420 | 1.279 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v21` | `multi_via` | `unet_no_topology` | yes | yes | -0.140 | 1.479 | 1.340 | 0.009 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v33` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.140 | 3.050 | 3.189 | 0.063 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v73` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.140 | 3.050 | 3.189 | 0.063 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_no_topology` | no | yes | -0.140 | 1.468 | 1.329 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v46` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.139 | 2.332 | 2.471 | 0.035 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_no_topology` | no | yes | -0.139 | 1.374 | 1.235 | 4.902e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v46` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.139 | 2.291 | 2.429 | 0.029 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v21` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | -0.136 | 1.131 | 0.995 | -1.338e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v16` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.135 | 1.433 | 1.298 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v02` | `dense_via_background` | `unet_no_topology` | yes | yes | 0.135 | 1.781 | 1.915 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v40` | `no_via_background` | `unet_no_topology` | no | yes | -0.135 | 1.411 | 1.276 | -0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `single_via` | `canonical` | `unet_topology_soft_loss` | yes | yes | -0.133 | 4.353 | 4.220 | -0.114 | 0.000 | `generative_low_margin_refusal` |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_no_topology` | no | yes | -0.133 | 1.749 | 1.617 | 0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v03` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.133 | 3.099 | 3.232 | 0.062 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v83` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.133 | 3.099 | 3.232 | 0.062 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v38` | `bend_artifact` | `unet_no_topology` | no | yes | -0.132 | 1.498 | 1.366 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v70` | `no_via_background` | `unet_no_topology` | no | yes | -0.132 | 1.410 | 1.278 | 0.002 | 0.000 | `generative_low_margin_refusal` |
| `multi_via_route__v11` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.131 | 1.305 | 1.435 | -0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v26` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.131 | 1.305 | 1.435 | -0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.130 | 1.190 | 1.060 | -0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v01` | `multi_via` | `unet_no_topology` | yes | yes | 0.130 | 1.739 | 1.869 | 0.013 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v28` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.130 | 1.444 | 1.314 | 0.002 | 0.500 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_no_topology` | no | yes | -0.129 | 1.488 | 1.359 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v23` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.128 | 1.101 | 0.973 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v52` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.127 | 1.433 | 1.560 | -0.009 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v91` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.127 | 2.262 | 2.389 | 0.029 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v08` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.126 | 1.428 | 1.554 | -9.679e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v09` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.126 | 3.177 | 3.303 | 0.062 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | 0.126 | 1.450 | 1.575 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v32` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.125 | 3.222 | 3.347 | 0.065 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v72` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.125 | 3.222 | 3.347 | 0.065 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v37` | `bend_artifact` | `unet_no_topology` | no | yes | -0.125 | 1.254 | 1.129 | -1.400e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v39` | `no_via_background` | `unet_no_topology` | no | yes | -0.123 | 1.305 | 1.181 | 0.004 | 0.000 | `generative_low_margin_refusal` |
| `dense_via_background__v01` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | yes | 0.123 | 1.321 | 1.443 | 0.009 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v10` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.122 | 1.495 | 1.617 | -0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v55` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.121 | 2.710 | 2.831 | 0.031 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v05` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.120 | 2.742 | 2.862 | 0.031 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v77` | `return_path` | `unet_no_topology` | yes | yes | -0.120 | 2.132 | 2.011 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v11` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.120 | 1.375 | 1.495 | -0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v26` | `multi_via` | `unet_topology_soft_loss` | yes | yes | 0.120 | 1.375 | 1.495 | -0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v02` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.119 | 3.175 | 3.294 | 0.060 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v82` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.119 | 3.175 | 3.294 | 0.060 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v69` | `no_via_background` | `unet_no_topology` | no | yes | -0.117 | 1.276 | 1.159 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v54` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.117 | 2.729 | 2.846 | 0.038 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_no_topology` | no | yes | -0.116 | 1.905 | 1.789 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_no_topology` | no | yes | -0.115 | 1.604 | 1.489 | 0.003 | 0.000 | `generative_low_margin_refusal` |
| `two_layer_route_with_via__v10` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.115 | 1.103 | 1.218 | 0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v04` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.114 | 2.895 | 3.009 | 0.049 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v30` | `multi_via` | `unet_no_topology` | yes | yes | -0.114 | 1.776 | 1.662 | -0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v08` | `return_path` | `unet_no_topology` | yes | yes | -0.113 | 1.154 | 1.041 | 0.018 | 0.500 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v22` | `multi_via` | `unet_no_topology` | yes | yes | -0.112 | 1.325 | 1.214 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v10` | `no_via_background` | `unet_no_topology` | no | yes | 0.111 | 1.752 | 1.863 | 0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v68` | `bend_artifact` | `unet_no_topology` | no | yes | -0.110 | 1.429 | 1.318 | -0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v02` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.110 | 3.171 | 3.281 | 0.068 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v82` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.110 | 3.171 | 3.281 | 0.068 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v43` | `no_via_background` | `unet_no_topology` | no | yes | -0.110 | 1.493 | 1.383 | 0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v55` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.109 | 2.719 | 2.829 | 0.036 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v17` | `l1_jog` | `unet_no_topology` | yes | yes | -0.109 | 1.440 | 1.331 | -0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v91` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.108 | 2.241 | 2.349 | 0.021 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v29` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.108 | 1.553 | 1.444 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_no_topology` | no | yes | -0.108 | 1.440 | 1.332 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v71` | `no_via_background` | `unet_no_topology` | no | yes | -0.108 | 1.411 | 1.303 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v06` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.107 | 3.547 | 3.654 | 0.050 | 1.000 | `no_candidate` |
| `trace_with_return_path__v55` | `return_path` | `unet_no_topology` | yes | yes | 0.107 | 2.290 | 2.397 | 0.026 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v22` | `no_via_background` | `unet_no_topology` | no | yes | -0.106 | 1.268 | 1.162 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v09` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.106 | 3.217 | 3.323 | 0.054 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v24` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.106 | 1.469 | 1.575 | 0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v58` | `return_path` | `unet_no_topology` | yes | yes | -0.105 | 1.239 | 1.134 | 0.010 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v98` | `return_path` | `unet_no_topology` | yes | yes | -0.105 | 1.239 | 1.134 | 0.010 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v48` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.105 | 3.232 | 3.337 | 0.072 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v80` | `no_via_background` | `unet_topology_soft_loss` | no | yes | -0.105 | 1.603 | 1.498 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v43` | `no_via_background` | `unet_topology_soft_loss` | no | yes | -0.105 | 1.104 | 0.999 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_no_topology` | no | yes | -0.105 | 1.535 | 1.431 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_no_topology` | no | yes | -0.104 | 2.079 | 1.975 | -0.008 | 0.000 | `generative_low_margin_refusal` |
| `dense_via_background__v03` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | yes | 0.104 | 1.291 | 1.395 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v50` | `no_via_background` | `unet_no_topology` | no | yes | -0.104 | 1.684 | 1.579 | -0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v65` | `no_via_background` | `unet_topology_soft_loss` | no | yes | -0.104 | 1.081 | 0.978 | -0.002 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v25` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.104 | 1.369 | 1.472 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_no_topology` | no | yes | -0.103 | 1.876 | 1.773 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v19` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | -0.103 | 1.031 | 0.928 | 0.011 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v58` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.103 | 1.314 | 1.417 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_no_topology` | no | yes | -0.103 | 1.528 | 1.426 | -0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v96` | `no_via_background` | `unet_no_topology` | no | yes | -0.103 | 1.849 | 1.746 | -0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v05` | `l1_jog` | `unet_no_topology` | yes | yes | -0.102 | 1.786 | 1.683 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v02` | `multi_via` | `unet_no_topology` | yes | yes | 0.102 | 1.913 | 2.015 | -0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v17` | `l1_jog` | `unet_topology_soft_loss` | yes | yes | -0.102 | 1.188 | 1.086 | 0.002 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via` | `l1_jog` | `unet_no_topology` | yes | yes | 0.102 | 1.767 | 1.869 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v36` | `no_via_background` | `unet_no_topology` | no | yes | -0.102 | 1.440 | 1.338 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v11` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.102 | 1.025 | 1.127 | 0.009 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v26` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.102 | 1.025 | 1.127 | 0.009 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v09` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.102 | 1.240 | 1.342 | -4.679e-05 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.102 | 1.523 | 1.421 | -0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_no_topology` | no | yes | 0.101 | 1.883 | 1.984 | 0.021 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v12` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.101 | 1.458 | 1.357 | -0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v53` | `no_via_background` | `unet_no_topology` | no | yes | -0.101 | 1.493 | 1.392 | 3.118e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v20` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.101 | 1.486 | 1.385 | -0.001 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v20` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | -0.101 | 1.238 | 1.137 | -0.001 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v21` | `no_via_background` | `unet_no_topology` | no | yes | -0.101 | 1.405 | 1.304 | 0.010 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v86` | `no_via_background` | `unet_no_topology` | no | yes | -0.101 | 1.405 | 1.304 | 0.010 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v49` | `return_path` | `unet_no_topology` | yes | yes | -0.100 | 1.178 | 1.077 | 0.018 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_no_topology` | no | yes | -0.100 | 1.476 | 1.376 | -8.371e-04 | 0.000 | `generative_low_margin_refusal` |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_no_topology` | no | yes | -0.100 | 1.345 | 1.245 | 0.002 | 0.000 | `generative_low_margin_refusal` |
| `multi_via_route__v15` | `multi_via` | `unet_topology_two_stage_refined` | yes | yes | 0.100 | 1.040 | 1.140 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v02` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.100 | 1.393 | 1.492 | 0.014 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v18` | `multi_via` | `unet_no_topology` | yes | yes | -0.099 | 1.332 | 1.233 | -0.011 | 0.500 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v68` | `no_via_background` | `unet_no_topology` | no | yes | -0.099 | 1.520 | 1.421 | 0.011 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v26` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.099 | 1.342 | 1.442 | 0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v13` | `dense_via_background` | `unet_topology_soft_loss` | yes | yes | -0.099 | 1.235 | 1.136 | -0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v90` | `no_via_background` | `unet_no_topology` | no | yes | -0.099 | 1.389 | 1.290 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v34` | `no_via_background` | `unet_no_topology` | no | yes | -0.099 | 1.795 | 1.696 | -3.272e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v06` | `l1_jog` | `unet_no_topology` | yes | yes | -0.099 | 1.646 | 1.547 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.099 | 1.212 | 1.113 | 0.008 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v27` | `no_via_background` | `unet_topology_soft_loss` | no | yes | 0.099 | 1.321 | 1.420 | 0.007 | 1.000 | `generative_ambiguous_artifact_zone` |
| `multi_via_route__v31` | `multi_via` | `unet_no_topology` | yes | yes | -0.099 | 1.814 | 1.715 | -9.251e-04 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v52` | `no_via_background` | `unet_topology_two_stage_refined` | no | yes | 0.098 | 1.411 | 1.509 | -0.004 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v13` | `no_via_background` | `unet_no_topology` | no | yes | -0.098 | 1.500 | 1.402 | -0.003 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v93` | `no_via_background` | `unet_no_topology` | no | yes | -0.098 | 1.500 | 1.402 | -0.003 | 0.000 | `generative_low_margin_refusal` |
| `no_via_background__v65` | `no_via_background` | `unet_no_topology` | no | yes | -0.098 | 1.226 | 1.128 | 0.002 | 0.000 | `generative_low_margin_refusal` |
| `two_layer_route_with_via` | `l1_jog` | `unet_topology_two_stage_refined` | yes | yes | 0.098 | 1.445 | 1.543 | 0.005 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background__v13` | `dense_via_background` | `unet_no_topology` | yes | yes | -0.098 | 1.423 | 1.325 | -0.007 | 0.000 | `generative_low_margin_refusal` |
| `trace_with_return_path__v58` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.097 | 1.126 | 1.223 | 0.017 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v98` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.097 | 1.126 | 1.223 | 0.017 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v51` | `no_via_background` | `unet_no_topology` | no | yes | -0.097 | 1.660 | 1.563 | -0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `two_layer_route_with_via__v16` | `l1_jog` | `unet_no_topology` | yes | yes | -0.097 | 1.484 | 1.387 | 0.006 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v85` | `no_via_background` | `unet_no_topology` | no | yes | -0.096 | 1.372 | 1.276 | 0.001 | 0.000 | `generative_low_margin_refusal` |
| `trace_with_return_path__v68` | `return_path` | `unet_no_topology` | yes | yes | -0.096 | 1.819 | 1.723 | 0.026 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v41` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.096 | 2.312 | 2.408 | 0.026 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v61` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | 0.096 | 2.312 | 2.408 | 0.026 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v31` | `return_path` | `unet_topology_two_stage_refined` | yes | no | 0.095 | 3.431 | 3.527 | 0.041 | 1.000 | `no_candidate` |
| `trace_with_return_path__v43` | `return_path` | `unet_no_topology` | yes | yes | -0.095 | 2.054 | 1.959 | -0.007 | 0.500 | `generative_ambiguous_artifact_zone` |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_topology_soft_loss` | no | yes | -0.095 | 1.354 | 1.260 | -0.004 | 0.000 | `generative_low_margin_refusal` |
| `trace_with_return_path__v54` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.094 | 2.752 | 2.847 | 0.027 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v99` | `return_path` | `unet_topology_soft_loss` | yes | yes | 0.094 | 3.415 | 3.509 | 0.049 | 1.000 | `generative_ambiguous_artifact_zone` |
| `dense_via_background` | `dense_via_background` | `unet_no_topology` | yes | yes | 0.094 | 1.694 | 1.788 | 0.008 | 1.000 | `generative_ambiguous_artifact_zone` |
| `no_via_background__v59` | `no_via_background` | `unet_no_topology` | no | yes | 0.094 | 1.714 | 1.808 | 0.003 | 1.000 | `generative_ambiguous_artifact_zone` |
| `trace_with_return_path__v19` | `return_path` | `unet_topology_two_stage_refined` | yes | yes | -0.094 | 1.695 | 1.602 | 0.014 | 1.000 | `generative_ambiguous_artifact_zone` |

Interpretation: this is still diagnostic. It upgrades rule evidence into an explicit H1-vs-H0 re-forward energy comparison, but it does not claim a solved detector.
