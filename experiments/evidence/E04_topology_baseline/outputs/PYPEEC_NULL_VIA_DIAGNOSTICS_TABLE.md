# Real PyPEEC No-Via False-Positive Diagnostics

- no-via cases: `200`
- presence threshold: `2.666667`
- boundary: Diagnostic only. No PyPEEC no-via threshold is selected from these rows.

## Summary

| model | cases | FP rate | mean s1 peak | mean topology MSE | mean physical B PyPEEC | mean leakage | dominant failure modes |
|---|---:|---:|---:|---:|---:|---:|---|
| `unet_no_topology` | 200 | 0.930 | 0.448 | 1.660 | 0.869 | 0.374 | bend/corner induced residual: 162, detector threshold sensitivity: 15, model hallucination: 2, no false positive: 14, operator mismatch: 7 |
| `unet_topology_soft_loss` | 200 | 0.940 | 0.390 | 1.013 | 0.727 | 0.396 | bend/corner induced residual: 151, detector threshold sensitivity: 6, model hallucination: 4, no false positive: 12, operator mismatch: 27 |
| `unet_topology_two_stage_refined` | 200 | 0.720 | 0.260 | 0.955 | 0.725 | 0.396 | bend/corner induced residual: 124, detector threshold sensitivity: 4, model hallucination: 2, no false positive: 56, operator mismatch: 14 |

## Per-Case Rows

| case | type | model | FP | s1 peak | s1 rms | via px | comp | d trace | d bend | d return | topology MSE | B PyPEEC | gap | leakage | failure mode |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `straight_trace` | `canonical` | `unet_no_topology` | no | 0.020 | 0.004 | 0 | 0 | 0.000 | n/a | n/a | 0.810 | 1.275 | 0.004 | 0.007 | no false positive |
| `finite_width_trace` | `canonical` | `unet_no_topology` | no | 0.085 | 0.008 | 0 | 0 | 0.000 | n/a | n/a | 0.748 | 1.207 | 0.194 | 0.388 | no false positive |
| `l_shape_trace` | `canonical` | `unet_no_topology` | yes | 0.547 | 0.042 | 3 | 2 | 0.000 | 10.000 | n/a | 0.829 | 0.558 | 0.004 | 0.055 | model hallucination |
| `no_via_background` | `no_via_background` | `unet_no_topology` | yes | 0.235 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.518 | 0.676 | 0.265 | 0.754 | bend/corner induced residual |
| `no_via_background__v01` | `no_via_background` | `unet_no_topology` | yes | 0.432 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.458 | 1.077 | 0.197 | 0.259 | bend/corner induced residual |
| `no_via_background__v02` | `no_via_background` | `unet_no_topology` | yes | 0.495 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.228 | 0.921 | 0.146 | 0.364 | bend/corner induced residual |
| `no_via_background__v03` | `no_via_background` | `unet_no_topology` | no | 0.191 | 0.016 | 0 | 0 | 0.000 | 0.000 | n/a | 1.104 | 0.977 | 0.146 | 0.273 | no false positive |
| `no_via_background__v04` | `no_via_background` | `unet_no_topology` | yes | 0.384 | 0.033 | 2 | 1 | 1.000 | 1.000 | n/a | 1.343 | 1.122 | 0.231 | 0.417 | bend/corner induced residual |
| `no_via_background__v05` | `no_via_background` | `unet_no_topology` | yes | 0.353 | 0.033 | 2 | 1 | 0.000 | 0.000 | n/a | 1.243 | 1.029 | 0.215 | 0.179 | bend/corner induced residual |
| `no_via_background__v06` | `no_via_background` | `unet_no_topology` | yes | 0.356 | 0.028 | 1 | 1 | 1.000 | 1.000 | n/a | 1.500 | 1.000 | 0.214 | 0.509 | bend/corner induced residual |
| `no_via_background__v07` | `no_via_background` | `unet_no_topology` | yes | 0.247 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.337 | 1.124 | 0.171 | 0.352 | bend/corner induced residual |
| `no_via_background__v08` | `no_via_background` | `unet_no_topology` | yes | 0.754 | 0.054 | 3 | 2 | 0.000 | 0.000 | n/a | 2.848 | 0.954 | 0.203 | 0.389 | bend/corner induced residual |
| `no_via_background__v09` | `no_via_background` | `unet_no_topology` | yes | 1.223 | 0.073 | 1 | 1 | 0.000 | 0.000 | n/a | 2.606 | 0.980 | 0.183 | 0.287 | bend/corner induced residual |
| `no_via_background__v10` | `no_via_background` | `unet_no_topology` | yes | 0.965 | 0.058 | 1 | 1 | 0.000 | 0.000 | n/a | 1.954 | 0.953 | 0.136 | 0.356 | bend/corner induced residual |
| `no_via_background__v11` | `no_via_background` | `unet_no_topology` | yes | 0.561 | 0.041 | 2 | 2 | 0.000 | 0.000 | n/a | 2.489 | 0.979 | 0.176 | 0.344 | bend/corner induced residual |
| `no_via_background__v12` | `no_via_background` | `unet_no_topology` | yes | 0.225 | 0.021 | 1 | 1 | 0.000 | 5.000 | n/a | 1.435 | 1.207 | 0.222 | 0.067 | detector threshold sensitivity |
| `no_via_background__v13` | `no_via_background` | `unet_no_topology` | yes | 0.287 | 0.029 | 2 | 2 | 0.000 | 5.000 | n/a | 1.188 | 0.896 | 0.195 | 0.104 | detector threshold sensitivity |
| `no_via_background__v14` | `no_via_background` | `unet_no_topology` | yes | 0.220 | 0.025 | 2 | 2 | 1.000 | 1.000 | n/a | 1.413 | 1.082 | 0.210 | 0.691 | bend/corner induced residual |
| `no_via_background__v15` | `no_via_background` | `unet_no_topology` | yes | 0.234 | 0.022 | 1 | 1 | 0.000 | 2.000 | n/a | 0.942 | 0.817 | 0.116 | 0.158 | bend/corner induced residual |
| `no_via_background__v16` | `no_via_background` | `unet_no_topology` | no | 0.198 | 0.021 | 0 | 0 | 0.000 | 0.000 | n/a | 1.181 | 0.513 | 0.165 | 0.380 | no false positive |
| `no_via_background__v17` | `no_via_background` | `unet_no_topology` | no | 0.198 | 0.020 | 0 | 0 | 0.000 | 5.000 | n/a | 1.119 | 0.498 | 0.176 | 0.358 | no false positive |
| `no_via_background__v18` | `no_via_background` | `unet_no_topology` | no | 0.199 | 0.023 | 0 | 0 | 0.000 | 0.000 | n/a | 0.930 | 0.540 | 0.194 | 0.362 | no false positive |
| `no_via_background__v19` | `no_via_background` | `unet_no_topology` | no | 0.161 | 0.018 | 0 | 0 | 0.000 | 6.000 | n/a | 0.870 | 0.519 | 0.170 | 0.270 | no false positive |
| `no_via_background__v20` | `no_via_background` | `unet_no_topology` | yes | 0.276 | 0.033 | 3 | 2 | 0.000 | 4.000 | n/a | 1.439 | 0.707 | 0.253 | 0.340 | operator mismatch |
| `no_via_background__v21` | `no_via_background` | `unet_no_topology` | yes | 0.476 | 0.041 | 3 | 3 | 0.000 | 0.000 | n/a | 1.679 | 0.640 | 0.201 | 0.305 | bend/corner induced residual |
| `no_via_background__v22` | `no_via_background` | `unet_no_topology` | yes | 0.266 | 0.031 | 3 | 3 | 0.000 | 0.000 | n/a | 1.192 | 0.635 | 0.143 | 0.191 | bend/corner induced residual |
| `no_via_background__v23` | `no_via_background` | `unet_no_topology` | yes | 0.326 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.167 | 0.666 | 0.174 | 0.339 | bend/corner induced residual |
| `no_via_background__v24` | `no_via_background` | `unet_no_topology` | yes | 1.212 | 0.072 | 1 | 1 | 0.000 | 0.000 | n/a | 2.674 | 1.028 | 0.165 | 0.271 | bend/corner induced residual |
| `no_via_background__v25` | `no_via_background` | `unet_no_topology` | yes | 1.195 | 0.071 | 1 | 1 | 0.000 | 0.000 | n/a | 2.320 | 0.897 | 0.194 | 0.306 | bend/corner induced residual |
| `no_via_background__v26` | `no_via_background` | `unet_no_topology` | yes | 1.123 | 0.067 | 1 | 1 | 0.000 | 0.000 | n/a | 2.322 | 0.999 | 0.210 | 0.596 | bend/corner induced residual |
| `no_via_background__v27` | `no_via_background` | `unet_no_topology` | yes | 1.103 | 0.066 | 1 | 1 | 0.000 | 0.000 | n/a | 2.287 | 0.976 | 0.171 | 0.286 | bend/corner induced residual |
| `no_via_background__v28` | `no_via_background` | `unet_no_topology` | no | 0.174 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 1.867 | 0.909 | 0.163 | 0.531 | no false positive |
| `no_via_background__v29` | `no_via_background` | `unet_no_topology` | yes | 0.349 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.942 | 0.907 | 0.231 | 0.474 | bend/corner induced residual |
| `no_via_background__v30` | `no_via_background` | `unet_no_topology` | no | 0.196 | 0.023 | 0 | 0 | 0.000 | 0.000 | n/a | 1.947 | 0.933 | 0.146 | 0.492 | no false positive |
| `no_via_background__v31` | `no_via_background` | `unet_no_topology` | yes | 0.283 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 2.470 | 0.914 | 0.176 | 0.683 | bend/corner induced residual |
| `no_via_background__v32` | `no_via_background` | `unet_no_topology` | yes | 0.592 | 0.037 | 1 | 1 | 0.000 | 0.000 | n/a | 1.453 | 1.017 | 0.264 | 0.334 | bend/corner induced residual |
| `no_via_background__v33` | `no_via_background` | `unet_no_topology` | no | 0.193 | 0.016 | 0 | 0 | 0.000 | 0.000 | n/a | 1.117 | 0.997 | 0.207 | 0.458 | no false positive |
| `no_via_background__v34` | `no_via_background` | `unet_no_topology` | yes | 0.411 | 0.031 | 2 | 2 | 0.000 | 0.000 | n/a | 1.478 | 1.098 | 0.248 | 0.533 | bend/corner induced residual |
| `no_via_background__v35` | `no_via_background` | `unet_no_topology` | yes | 0.510 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 1.743 | 0.695 | 0.209 | 0.717 | bend/corner induced residual |
| `no_via_background__v36` | `no_via_background` | `unet_no_topology` | yes | 0.469 | 0.039 | 3 | 3 | 0.000 | 0.000 | n/a | 1.513 | 0.715 | 0.165 | 0.324 | bend/corner induced residual |
| `no_via_background__v37` | `no_via_background` | `unet_no_topology` | yes | 0.458 | 0.033 | 1 | 1 | 0.000 | 5.000 | n/a | 1.483 | 0.569 | 0.160 | 0.306 | operator mismatch |
| `no_via_background__v38` | `no_via_background` | `unet_no_topology` | yes | 0.312 | 0.031 | 2 | 2 | 0.000 | 0.000 | n/a | 1.269 | 0.729 | 0.185 | 0.287 | bend/corner induced residual |
| `no_via_background__v39` | `no_via_background` | `unet_no_topology` | yes | 0.405 | 0.038 | 3 | 3 | 0.000 | 6.000 | n/a | 1.439 | 0.607 | 0.177 | 0.188 | detector threshold sensitivity |
| `no_via_background__v40` | `no_via_background` | `unet_no_topology` | yes | 0.336 | 0.033 | 3 | 3 | 0.000 | 0.000 | n/a | 1.100 | 0.799 | 0.223 | 0.249 | bend/corner induced residual |
| `no_via_background__v41` | `no_via_background` | `unet_no_topology` | yes | 0.290 | 0.028 | 1 | 1 | 0.000 | 2.000 | n/a | 0.734 | 0.711 | 0.202 | 0.097 | bend/corner induced residual |
| `no_via_background__v42` | `no_via_background` | `unet_no_topology` | yes | 0.385 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 0.966 | 0.922 | 0.143 | 0.086 | bend/corner induced residual |
| `no_via_background__v43` | `no_via_background` | `unet_no_topology` | yes | 0.287 | 0.033 | 3 | 3 | 0.000 | 0.000 | n/a | 1.002 | 0.917 | 0.179 | 0.082 | bend/corner induced residual |
| `no_via_background__v44` | `no_via_background` | `unet_no_topology` | yes | 0.301 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 1.404 | 1.051 | 0.211 | 0.387 | bend/corner induced residual |
| `no_via_background__v45` | `no_via_background` | `unet_no_topology` | yes | 0.260 | 0.022 | 1 | 1 | 0.000 | 5.000 | n/a | 1.353 | 0.963 | 0.203 | 0.191 | detector threshold sensitivity |
| `no_via_background__v46` | `no_via_background` | `unet_no_topology` | yes | 0.271 | 0.028 | 2 | 2 | 0.000 | 1.000 | n/a | 1.149 | 0.811 | 0.263 | 0.372 | bend/corner induced residual |
| `no_via_background__v47` | `no_via_background` | `unet_no_topology` | yes | 0.290 | 0.029 | 1 | 1 | 0.000 | 6.000 | n/a | 1.330 | 1.025 | 0.151 | 0.095 | detector threshold sensitivity |
| `no_via_background__v48` | `no_via_background` | `unet_no_topology` | yes | 0.237 | 0.024 | 1 | 1 | 0.000 | 4.000 | n/a | 0.992 | 1.062 | 0.135 | 0.246 | detector threshold sensitivity |
| `no_via_background__v49` | `no_via_background` | `unet_no_topology` | yes | 0.364 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.135 | 0.920 | 0.197 | 0.335 | bend/corner induced residual |
| `no_via_background__v50` | `no_via_background` | `unet_no_topology` | yes | 0.432 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.428 | 1.024 | 0.135 | 0.214 | bend/corner induced residual |
| `no_via_background__v51` | `no_via_background` | `unet_no_topology` | yes | 0.260 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.346 | 1.030 | 0.109 | 0.202 | bend/corner induced residual |
| `no_via_background__v52` | `no_via_background` | `unet_no_topology` | yes | 0.499 | 0.037 | 2 | 2 | 0.000 | 0.000 | n/a | 1.814 | 1.078 | 0.234 | 0.432 | bend/corner induced residual |
| `no_via_background__v53` | `no_via_background` | `unet_no_topology` | yes | 0.427 | 0.035 | 3 | 2 | 0.000 | 0.000 | n/a | 1.173 | 0.881 | 0.170 | 0.343 | bend/corner induced residual |
| `no_via_background__v54` | `no_via_background` | `unet_no_topology` | yes | 0.243 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.793 | 1.204 | 0.263 | 0.739 | bend/corner induced residual |
| `no_via_background__v55` | `no_via_background` | `unet_no_topology` | yes | 0.363 | 0.032 | 2 | 1 | 0.000 | 0.000 | n/a | 0.969 | 0.813 | 0.239 | 0.378 | bend/corner induced residual |
| `no_via_background__v56` | `no_via_background` | `unet_no_topology` | yes | 1.095 | 0.065 | 1 | 1 | 0.000 | 0.000 | n/a | 1.939 | 0.957 | 0.211 | 0.732 | bend/corner induced residual |
| `no_via_background__v57` | `no_via_background` | `unet_no_topology` | yes | 1.102 | 0.066 | 1 | 1 | 0.000 | 0.000 | n/a | 2.428 | 1.042 | 0.211 | 0.256 | bend/corner induced residual |
| `no_via_background__v58` | `no_via_background` | `unet_no_topology` | yes | 1.162 | 0.070 | 1 | 1 | 0.000 | 0.000 | n/a | 1.993 | 0.806 | 0.185 | 0.493 | bend/corner induced residual |
| `no_via_background__v59` | `no_via_background` | `unet_no_topology` | yes | 1.199 | 0.072 | 1 | 1 | 0.000 | 0.000 | n/a | 2.250 | 0.847 | 0.176 | 0.480 | bend/corner induced residual |
| `no_via_background__v60` | `no_via_background` | `unet_no_topology` | yes | 0.363 | 0.029 | 2 | 2 | 0.000 | 5.000 | n/a | 1.201 | 0.888 | 0.221 | 0.065 | detector threshold sensitivity |
| `no_via_background__v61` | `no_via_background` | `unet_no_topology` | yes | 0.271 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 1.149 | 0.811 | 0.202 | 0.119 | bend/corner induced residual |
| `no_via_background__v62` | `no_via_background` | `unet_no_topology` | yes | 0.382 | 0.032 | 2 | 2 | 0.000 | 5.000 | n/a | 1.510 | 1.124 | 0.143 | 0.114 | detector threshold sensitivity |
| `no_via_background__v63` | `no_via_background` | `unet_no_topology` | yes | 0.223 | 0.022 | 1 | 1 | 0.000 | 5.000 | n/a | 1.267 | 0.966 | 0.177 | 0.206 | detector threshold sensitivity |
| `no_via_background__v64` | `no_via_background` | `unet_no_topology` | yes | 0.230 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.356 | 0.502 | 0.155 | 0.434 | bend/corner induced residual |
| `no_via_background__v65` | `no_via_background` | `unet_no_topology` | yes | 0.243 | 0.029 | 2 | 2 | 0.000 | 5.000 | n/a | 1.259 | 0.603 | 0.192 | 0.422 | operator mismatch |
| `no_via_background__v66` | `no_via_background` | `unet_no_topology` | yes | 0.225 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.246 | 0.493 | 0.248 | 0.773 | bend/corner induced residual |
| `no_via_background__v67` | `no_via_background` | `unet_no_topology` | yes | 0.211 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 1.096 | 0.481 | 0.153 | 0.386 | bend/corner induced residual |
| `no_via_background__v68` | `no_via_background` | `unet_no_topology` | yes | 0.606 | 0.043 | 3 | 2 | 0.000 | 0.000 | n/a | 2.000 | 0.700 | 0.203 | 0.419 | bend/corner induced residual |
| `no_via_background__v69` | `no_via_background` | `unet_no_topology` | yes | 0.333 | 0.035 | 3 | 3 | 0.000 | 0.000 | n/a | 1.201 | 0.638 | 0.230 | 0.201 | bend/corner induced residual |
| `no_via_background__v70` | `no_via_background` | `unet_no_topology` | yes | 0.391 | 0.036 | 3 | 3 | 0.000 | 5.000 | n/a | 1.460 | 0.706 | 0.143 | 0.224 | model hallucination |
| `no_via_background__v71` | `no_via_background` | `unet_no_topology` | yes | 0.270 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 1.682 | 0.669 | 0.218 | 0.523 | bend/corner induced residual |
| `no_via_background__v72` | `no_via_background` | `unet_no_topology` | yes | 1.207 | 0.072 | 1 | 1 | 0.000 | 0.000 | n/a | 2.655 | 1.027 | 0.262 | 0.354 | bend/corner induced residual |
| `no_via_background__v73` | `no_via_background` | `unet_no_topology` | yes | 1.042 | 0.062 | 1 | 1 | 0.000 | 0.000 | n/a | 1.862 | 0.802 | 0.205 | 0.558 | bend/corner induced residual |
| `no_via_background__v74` | `no_via_background` | `unet_no_topology` | yes | 1.223 | 0.073 | 1 | 1 | 0.000 | 0.000 | n/a | 2.606 | 0.980 | 0.248 | 0.460 | bend/corner induced residual |
| `no_via_background__v75` | `no_via_background` | `unet_no_topology` | yes | 1.120 | 0.067 | 1 | 1 | 0.000 | 0.000 | n/a | 2.391 | 0.942 | 0.091 | 0.084 | bend/corner induced residual |
| `no_via_background__v76` | `no_via_background` | `unet_no_topology` | yes | 0.219 | 0.023 | 1 | 1 | 1.000 | 1.000 | n/a | 1.830 | 0.944 | 0.263 | 0.805 | bend/corner induced residual |
| `no_via_background__v77` | `no_via_background` | `unet_no_topology` | yes | 0.518 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 2.161 | 0.933 | 0.193 | 0.453 | bend/corner induced residual |
| `no_via_background__v78` | `no_via_background` | `unet_no_topology` | yes | 0.231 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 1.596 | 0.834 | 0.166 | 0.488 | bend/corner induced residual |
| `no_via_background__v79` | `no_via_background` | `unet_no_topology` | yes | 0.316 | 0.025 | 1 | 1 | 1.000 | 1.000 | n/a | 1.405 | 0.801 | 0.170 | 0.449 | bend/corner induced residual |
| `no_via_background__v80` | `no_via_background` | `unet_no_topology` | yes | 0.283 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.541 | 1.077 | 0.232 | 0.188 | bend/corner induced residual |
| `no_via_background__v81` | `no_via_background` | `unet_no_topology` | yes | 0.432 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.458 | 1.077 | 0.197 | 0.259 | bend/corner induced residual |
| `no_via_background__v82` | `no_via_background` | `unet_no_topology` | yes | 0.495 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.228 | 0.921 | 0.146 | 0.364 | bend/corner induced residual |
| `no_via_background__v83` | `no_via_background` | `unet_no_topology` | no | 0.191 | 0.016 | 0 | 0 | 0.000 | 0.000 | n/a | 1.104 | 0.977 | 0.146 | 0.273 | no false positive |
| `no_via_background__v84` | `no_via_background` | `unet_no_topology` | yes | 0.459 | 0.039 | 3 | 2 | 1.000 | 1.000 | n/a | 1.221 | 0.684 | 0.143 | 0.436 | bend/corner induced residual |
| `no_via_background__v85` | `no_via_background` | `unet_no_topology` | yes | 0.300 | 0.035 | 2 | 2 | 1.000 | 1.000 | n/a | 1.372 | 0.715 | 0.203 | 0.276 | bend/corner induced residual |
| `no_via_background__v86` | `no_via_background` | `unet_no_topology` | yes | 0.476 | 0.041 | 3 | 3 | 0.000 | 0.000 | n/a | 1.679 | 0.640 | 0.248 | 0.628 | bend/corner induced residual |
| `no_via_background__v87` | `no_via_background` | `unet_no_topology` | yes | 0.502 | 0.045 | 3 | 3 | 0.000 | 0.000 | n/a | 1.261 | 0.570 | 0.159 | 0.197 | bend/corner induced residual |
| `no_via_background__v88` | `no_via_background` | `unet_no_topology` | yes | 0.324 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 0.925 | 0.868 | 0.260 | 0.596 | bend/corner induced residual |
| `no_via_background__v89` | `no_via_background` | `unet_no_topology` | yes | 0.319 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 0.870 | 0.775 | 0.183 | 0.103 | bend/corner induced residual |
| `no_via_background__v90` | `no_via_background` | `unet_no_topology` | yes | 0.247 | 0.028 | 3 | 3 | 0.000 | 0.000 | n/a | 0.933 | 0.834 | 0.143 | 0.104 | bend/corner induced residual |
| `no_via_background__v91` | `no_via_background` | `unet_no_topology` | yes | 0.560 | 0.038 | 1 | 1 | 0.000 | 3.000 | n/a | 0.986 | 0.641 | 0.248 | 0.363 | detector threshold sensitivity |
| `no_via_background__v92` | `no_via_background` | `unet_no_topology` | yes | 0.225 | 0.021 | 1 | 1 | 0.000 | 5.000 | n/a | 1.435 | 1.207 | 0.222 | 0.067 | detector threshold sensitivity |
| `no_via_background__v93` | `no_via_background` | `unet_no_topology` | yes | 0.287 | 0.029 | 2 | 2 | 0.000 | 5.000 | n/a | 1.188 | 0.896 | 0.195 | 0.104 | detector threshold sensitivity |
| `no_via_background__v94` | `no_via_background` | `unet_no_topology` | yes | 0.220 | 0.025 | 2 | 2 | 1.000 | 1.000 | n/a | 1.413 | 1.082 | 0.210 | 0.691 | bend/corner induced residual |
| `no_via_background__v95` | `no_via_background` | `unet_no_topology` | yes | 0.222 | 0.020 | 1 | 1 | 0.000 | 2.000 | n/a | 0.934 | 0.736 | 0.182 | 0.269 | bend/corner induced residual |
| `no_via_background__v96` | `no_via_background` | `unet_no_topology` | yes | 0.427 | 0.031 | 2 | 2 | 0.000 | 0.000 | n/a | 1.531 | 1.136 | 0.155 | 0.146 | bend/corner induced residual |
| `bend_artifact_trace` | `bend_artifact` | `unet_no_topology` | yes | 0.710 | 0.045 | 1 | 1 | 0.000 | 0.000 | n/a | 2.033 | 0.972 | 0.217 | 0.369 | bend/corner induced residual |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_no_topology` | yes | 0.359 | 0.027 | 1 | 1 | 1.000 | 1.000 | n/a | 1.990 | 1.063 | 0.176 | 0.415 | bend/corner induced residual |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_no_topology` | yes | 0.219 | 0.024 | 1 | 1 | 1.000 | 1.000 | n/a | 2.257 | 1.248 | 0.190 | 0.254 | bend/corner induced residual |
| `bend_artifact_trace__v03` | `bend_artifact` | `unet_no_topology` | yes | 0.438 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.945 | 1.005 | 0.146 | 0.262 | bend/corner induced residual |
| `bend_artifact_trace__v04` | `bend_artifact` | `unet_no_topology` | yes | 0.586 | 0.045 | 4 | 3 | 0.000 | 0.000 | n/a | 2.286 | 0.867 | 0.196 | 0.516 | bend/corner induced residual |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_no_topology` | yes | 0.304 | 0.035 | 2 | 2 | 0.000 | 0.000 | n/a | 2.189 | 0.835 | 0.229 | 0.571 | bend/corner induced residual |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_no_topology` | yes | 0.626 | 0.045 | 2 | 2 | 0.000 | 0.000 | n/a | 2.181 | 0.810 | 0.134 | 0.620 | bend/corner induced residual |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_no_topology` | yes | 0.507 | 0.037 | 1 | 1 | 0.000 | 0.000 | n/a | 1.506 | 0.601 | 0.207 | 0.716 | bend/corner induced residual |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_no_topology` | yes | 0.304 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 2.064 | 1.136 | 0.173 | 0.138 | bend/corner induced residual |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_no_topology` | yes | 0.244 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 2.168 | 1.025 | 0.236 | 0.144 | bend/corner induced residual |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_no_topology` | yes | 0.585 | 0.054 | 4 | 3 | 0.000 | 0.000 | n/a | 2.289 | 0.865 | 0.187 | 0.362 | bend/corner induced residual |
| `bend_artifact_trace__v11` | `bend_artifact` | `unet_no_topology` | yes | 0.770 | 0.050 | 2 | 1 | 0.000 | 0.000 | n/a | 2.655 | 0.957 | 0.150 | 0.243 | bend/corner induced residual |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_no_topology` | yes | 0.626 | 0.040 | 1 | 1 | 0.000 | 0.000 | n/a | 1.105 | 0.797 | 0.223 | 0.231 | bend/corner induced residual |
| `bend_artifact_trace__v13` | `bend_artifact` | `unet_no_topology` | yes | 0.499 | 0.041 | 2 | 1 | 1.000 | 1.000 | n/a | 1.282 | 0.921 | 0.238 | 0.628 | bend/corner induced residual |
| `bend_artifact_trace__v14` | `bend_artifact` | `unet_no_topology` | yes | 0.212 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 0.943 | 0.603 | 0.162 | 0.303 | bend/corner induced residual |
| `bend_artifact_trace__v15` | `bend_artifact` | `unet_no_topology` | yes | 0.350 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 1.242 | 0.816 | 0.164 | 0.131 | bend/corner induced residual |
| `bend_artifact_trace__v16` | `bend_artifact` | `unet_no_topology` | yes | 0.328 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 1.672 | 0.718 | 0.214 | 0.526 | bend/corner induced residual |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_no_topology` | yes | 0.322 | 0.031 | 1 | 1 | 1.000 | 3.162 | n/a | 1.707 | 0.630 | 0.219 | 0.508 | operator mismatch |
| `bend_artifact_trace__v18` | `bend_artifact` | `unet_no_topology` | yes | 0.462 | 0.038 | 3 | 3 | 0.000 | 3.000 | n/a | 1.440 | 0.633 | 0.167 | 0.240 | detector threshold sensitivity |
| `bend_artifact_trace__v19` | `bend_artifact` | `unet_no_topology` | yes | 0.324 | 0.029 | 1 | 1 | 0.000 | 3.000 | n/a | 1.464 | 0.627 | 0.204 | 0.367 | operator mismatch |
| `bend_artifact_trace__v20` | `bend_artifact` | `unet_no_topology` | no | 0.183 | 0.022 | 0 | 0 | 0.000 | 0.000 | n/a | 1.275 | 0.524 | 0.245 | 0.681 | no false positive |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_no_topology` | yes | 0.411 | 0.044 | 4 | 4 | 0.000 | 0.000 | n/a | 2.073 | 0.651 | 0.216 | 0.649 | bend/corner induced residual |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_no_topology` | yes | 0.589 | 0.044 | 3 | 3 | 0.000 | 0.000 | n/a | 1.837 | 0.629 | 0.233 | 0.563 | bend/corner induced residual |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_no_topology` | yes | 0.360 | 0.041 | 3 | 3 | 0.000 | 0.000 | n/a | 1.523 | 0.646 | 0.218 | 0.582 | bend/corner induced residual |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_no_topology` | yes | 0.505 | 0.040 | 3 | 3 | 0.000 | 0.000 | n/a | 2.142 | 1.034 | 0.214 | 0.357 | bend/corner induced residual |
| `bend_artifact_trace__v25` | `bend_artifact` | `unet_no_topology` | yes | 0.316 | 0.026 | 1 | 1 | 1.000 | 1.000 | n/a | 2.215 | 1.149 | 0.233 | 0.209 | bend/corner induced residual |
| `bend_artifact_trace__v26` | `bend_artifact` | `unet_no_topology` | yes | 0.807 | 0.053 | 2 | 1 | 0.000 | 0.000 | n/a | 2.494 | 1.053 | 0.162 | 0.376 | bend/corner induced residual |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_no_topology` | yes | 0.697 | 0.047 | 1 | 1 | 0.000 | 0.000 | n/a | 2.543 | 0.967 | 0.177 | 0.181 | bend/corner induced residual |
| `bend_artifact_trace__v28` | `bend_artifact` | `unet_no_topology` | yes | 0.393 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.758 | 0.953 | 0.222 | 0.647 | bend/corner induced residual |
| `bend_artifact_trace__v29` | `bend_artifact` | `unet_no_topology` | yes | 0.398 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.870 | 0.905 | 0.202 | 0.559 | bend/corner induced residual |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_no_topology` | yes | 0.398 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 2.066 | 0.894 | 0.154 | 0.621 | bend/corner induced residual |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_no_topology` | yes | 0.360 | 0.035 | 3 | 3 | 0.000 | 0.000 | n/a | 1.879 | 0.837 | 0.150 | 0.607 | bend/corner induced residual |
| `bend_artifact_trace__v32` | `bend_artifact` | `unet_no_topology` | yes | 0.692 | 0.046 | 2 | 1 | 0.000 | 0.000 | n/a | 2.716 | 1.366 | 0.229 | 0.146 | bend/corner induced residual |
| `bend_artifact_trace__v33` | `bend_artifact` | `unet_no_topology` | yes | 0.283 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.944 | 1.128 | 0.158 | 0.165 | bend/corner induced residual |
| `bend_artifact_trace__v34` | `bend_artifact` | `unet_no_topology` | yes | 0.737 | 0.046 | 1 | 1 | 0.000 | 0.000 | n/a | 2.288 | 1.018 | 0.247 | 0.457 | bend/corner induced residual |
| `bend_artifact_trace__v35` | `bend_artifact` | `unet_no_topology` | yes | 0.756 | 0.048 | 1 | 1 | 0.000 | 0.000 | n/a | 2.564 | 0.959 | 0.237 | 0.548 | bend/corner induced residual |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_no_topology` | yes | 0.403 | 0.045 | 4 | 4 | 0.000 | 0.000 | n/a | 1.814 | 0.621 | 0.214 | 0.670 | bend/corner induced residual |
| `bend_artifact_trace__v37` | `bend_artifact` | `unet_no_topology` | yes | 0.318 | 0.034 | 3 | 3 | 0.000 | 0.000 | n/a | 1.564 | 0.516 | 0.240 | 0.560 | bend/corner induced residual |
| `bend_artifact_trace__v38` | `bend_artifact` | `unet_no_topology` | yes | 0.488 | 0.049 | 4 | 4 | 0.000 | 0.000 | n/a | 1.727 | 0.702 | 0.219 | 0.617 | bend/corner induced residual |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_no_topology` | yes | 0.459 | 0.050 | 4 | 4 | 0.000 | 3.000 | n/a | 1.665 | 0.567 | 0.113 | 0.398 | detector threshold sensitivity |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_no_topology` | yes | 0.841 | 0.053 | 1 | 1 | 0.000 | 0.000 | n/a | 2.168 | 1.050 | 0.222 | 0.273 | bend/corner induced residual |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_no_topology` | yes | 0.553 | 0.040 | 2 | 2 | 0.000 | 0.000 | n/a | 1.834 | 0.901 | 0.234 | 0.280 | bend/corner induced residual |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_no_topology` | yes | 0.374 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 1.393 | 0.798 | 0.210 | 0.148 | bend/corner induced residual |
| `bend_artifact_trace__v43` | `bend_artifact` | `unet_no_topology` | yes | 0.461 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 1.590 | 0.983 | 0.202 | 0.175 | bend/corner induced residual |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_no_topology` | yes | 0.713 | 0.047 | 1 | 1 | 0.000 | 0.000 | n/a | 1.338 | 0.705 | 0.213 | 0.416 | bend/corner induced residual |
| `bend_artifact_trace__v45` | `bend_artifact` | `unet_no_topology` | yes | 0.306 | 0.030 | 2 | 1 | 0.000 | 0.000 | n/a | 1.220 | 0.885 | 0.178 | 0.289 | bend/corner induced residual |
| `bend_artifact_trace__v46` | `bend_artifact` | `unet_no_topology` | yes | 0.320 | 0.036 | 4 | 3 | 1.000 | 2.236 | n/a | 1.132 | 0.763 | 0.248 | 0.431 | detector threshold sensitivity |
| `bend_artifact_trace__v47` | `bend_artifact` | `unet_no_topology` | yes | 0.213 | 0.028 | 1 | 1 | 0.000 | 2.000 | n/a | 1.119 | 0.544 | 0.189 | 0.343 | bend/corner induced residual |
| `bend_artifact_trace__v48` | `bend_artifact` | `unet_no_topology` | yes | 0.537 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 2.084 | 1.214 | 0.159 | 0.170 | bend/corner induced residual |
| `bend_artifact_trace__v49` | `bend_artifact` | `unet_no_topology` | yes | 0.508 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 1.942 | 1.190 | 0.234 | 0.179 | bend/corner induced residual |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_no_topology` | yes | 0.245 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.776 | 0.962 | 0.188 | 0.420 | bend/corner induced residual |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_no_topology` | yes | 0.432 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.835 | 0.990 | 0.152 | 0.359 | bend/corner induced residual |
| `bend_artifact_trace__v52` | `bend_artifact` | `unet_no_topology` | yes | 0.493 | 0.041 | 3 | 3 | 0.000 | 0.000 | n/a | 1.985 | 1.011 | 0.252 | 0.328 | bend/corner induced residual |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_no_topology` | yes | 0.637 | 0.045 | 2 | 2 | 0.000 | 0.000 | n/a | 2.086 | 0.884 | 0.225 | 0.456 | bend/corner induced residual |
| `bend_artifact_trace__v54` | `bend_artifact` | `unet_no_topology` | yes | 0.584 | 0.047 | 3 | 3 | 0.000 | 0.000 | n/a | 2.182 | 0.828 | 0.248 | 0.573 | bend/corner induced residual |
| `bend_artifact_trace__v55` | `bend_artifact` | `unet_no_topology` | yes | 0.495 | 0.036 | 2 | 1 | 0.000 | 0.000 | n/a | 2.028 | 0.804 | 0.256 | 0.534 | bend/corner induced residual |
| `bend_artifact_trace__v56` | `bend_artifact` | `unet_no_topology` | yes | 0.968 | 0.059 | 1 | 1 | 0.000 | 0.000 | n/a | 2.414 | 1.134 | 0.213 | 0.271 | bend/corner induced residual |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_no_topology` | yes | 0.688 | 0.050 | 2 | 2 | 0.000 | 0.000 | n/a | 2.330 | 0.854 | 0.186 | 0.224 | bend/corner induced residual |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_no_topology` | yes | 0.311 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 2.194 | 1.111 | 0.253 | 0.109 | bend/corner induced residual |
| `bend_artifact_trace__v59` | `bend_artifact` | `unet_no_topology` | yes | 0.340 | 0.032 | 3 | 2 | 1.000 | 1.000 | n/a | 1.737 | 0.922 | 0.180 | 0.498 | bend/corner induced residual |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_no_topology` | yes | 0.358 | 0.035 | 2 | 1 | 0.000 | 0.000 | n/a | 1.226 | 0.880 | 0.194 | 0.167 | bend/corner induced residual |
| `bend_artifact_trace__v61` | `bend_artifact` | `unet_no_topology` | yes | 0.351 | 0.039 | 4 | 3 | 0.000 | 2.000 | n/a | 1.163 | 0.794 | 0.234 | 0.218 | bend/corner induced residual |
| `bend_artifact_trace__v62` | `bend_artifact` | `unet_no_topology` | yes | 0.246 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.126 | 0.645 | 0.233 | 0.248 | bend/corner induced residual |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_no_topology` | yes | 0.369 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 1.540 | 0.822 | 0.222 | 0.381 | bend/corner induced residual |
| `bend_artifact_trace__v64` | `bend_artifact` | `unet_no_topology` | no | 0.191 | 0.023 | 0 | 0 | 1.000 | 2.236 | n/a | 1.680 | 0.719 | 0.162 | 0.347 | no false positive |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_no_topology` | yes | 0.301 | 0.028 | 3 | 3 | 0.000 | 3.000 | n/a | 1.969 | 0.780 | 0.211 | 0.424 | operator mismatch |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_no_topology` | yes | 0.353 | 0.032 | 2 | 2 | 0.000 | 2.000 | n/a | 1.607 | 0.631 | 0.247 | 0.342 | bend/corner induced residual |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_no_topology` | yes | 0.302 | 0.030 | 1 | 1 | 1.000 | 2.236 | n/a | 1.366 | 0.609 | 0.192 | 0.448 | operator mismatch |
| `bend_artifact_trace__v68` | `bend_artifact` | `unet_no_topology` | yes | 0.294 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 1.645 | 0.690 | 0.173 | 0.678 | bend/corner induced residual |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_no_topology` | yes | 0.507 | 0.048 | 4 | 4 | 0.000 | 0.000 | n/a | 1.863 | 0.657 | 0.162 | 0.414 | bend/corner induced residual |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_no_topology` | yes | 0.399 | 0.039 | 3 | 3 | 0.000 | 0.000 | n/a | 1.820 | 0.652 | 0.210 | 0.432 | bend/corner induced residual |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_no_topology` | yes | 0.207 | 0.028 | 1 | 1 | 1.000 | 1.000 | n/a | 1.658 | 0.647 | 0.251 | 0.586 | bend/corner induced residual |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_no_topology` | yes | 0.425 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.548 | 0.951 | 0.218 | 0.147 | bend/corner induced residual |
| `bend_artifact_trace__v73` | `bend_artifact` | `unet_no_topology` | yes | 0.636 | 0.048 | 2 | 1 | 1.000 | 1.000 | n/a | 1.765 | 0.955 | 0.185 | 0.545 | bend/corner induced residual |
| `bend_artifact_trace__v74` | `bend_artifact` | `unet_no_topology` | yes | 0.509 | 0.034 | 1 | 1 | 1.000 | 1.000 | n/a | 2.655 | 1.111 | 0.247 | 0.328 | bend/corner induced residual |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_no_topology` | yes | 0.666 | 0.043 | 1 | 1 | 0.000 | 0.000 | n/a | 2.026 | 0.933 | 0.211 | 0.210 | bend/corner induced residual |
| `bend_artifact_trace__v76` | `bend_artifact` | `unet_no_topology` | yes | 0.501 | 0.038 | 1 | 1 | 0.000 | 0.000 | n/a | 2.039 | 0.830 | 0.257 | 0.684 | bend/corner induced residual |
| `bend_artifact_trace__v77` | `bend_artifact` | `unet_no_topology` | yes | 0.294 | 0.036 | 3 | 2 | 0.000 | 0.000 | n/a | 2.027 | 0.843 | 0.194 | 0.806 | bend/corner induced residual |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_no_topology` | yes | 0.426 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.838 | 0.863 | 0.183 | 0.758 | bend/corner induced residual |
| `bend_artifact_trace__v79` | `bend_artifact` | `unet_no_topology` | yes | 0.456 | 0.039 | 2 | 2 | 1.000 | 1.000 | n/a | 2.218 | 0.830 | 0.204 | 0.819 | bend/corner induced residual |
| `bend_artifact_trace__v80` | `bend_artifact` | `unet_no_topology` | yes | 0.689 | 0.044 | 1 | 1 | 0.000 | 0.000 | n/a | 1.963 | 1.053 | 0.252 | 0.285 | bend/corner induced residual |
| `bend_artifact_trace__v81` | `bend_artifact` | `unet_no_topology` | yes | 0.584 | 0.039 | 1 | 1 | 0.000 | 0.000 | n/a | 2.199 | 1.006 | 0.143 | 0.324 | bend/corner induced residual |
| `bend_artifact_trace__v82` | `bend_artifact` | `unet_no_topology` | yes | 0.392 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 2.106 | 1.157 | 0.206 | 0.450 | bend/corner induced residual |
| `bend_artifact_trace__v83` | `bend_artifact` | `unet_no_topology` | yes | 0.303 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 2.193 | 1.102 | 0.191 | 0.310 | bend/corner induced residual |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_no_topology` | yes | 0.462 | 0.043 | 4 | 4 | 0.000 | 0.000 | n/a | 1.845 | 0.701 | 0.136 | 0.470 | bend/corner induced residual |
| `bend_artifact_trace__v85` | `bend_artifact` | `unet_no_topology` | yes | 0.224 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 1.580 | 0.701 | 0.178 | 0.540 | bend/corner induced residual |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_no_topology` | yes | 0.287 | 0.034 | 3 | 2 | 1.000 | 1.000 | n/a | 1.843 | 0.702 | 0.247 | 0.664 | bend/corner induced residual |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_no_topology` | yes | 0.456 | 0.047 | 4 | 4 | 0.000 | 0.000 | n/a | 2.046 | 0.687 | 0.159 | 0.474 | bend/corner induced residual |
| `bend_artifact_trace__v88` | `bend_artifact` | `unet_no_topology` | yes | 0.506 | 0.037 | 1 | 1 | 0.000 | 0.000 | n/a | 1.366 | 0.774 | 0.256 | 0.833 | bend/corner induced residual |
| `bend_artifact_trace__v89` | `bend_artifact` | `unet_no_topology` | yes | 0.429 | 0.034 | 2 | 2 | 0.000 | 0.000 | n/a | 1.731 | 0.882 | 0.236 | 0.364 | bend/corner induced residual |
| `bend_artifact_trace__v90` | `bend_artifact` | `unet_no_topology` | yes | 0.505 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 1.375 | 0.779 | 0.233 | 0.705 | bend/corner induced residual |
| `bend_artifact_trace__v91` | `bend_artifact` | `unet_no_topology` | yes | 0.273 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.563 | 0.946 | 0.246 | 0.349 | bend/corner induced residual |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_no_topology` | yes | 0.626 | 0.040 | 1 | 1 | 0.000 | 0.000 | n/a | 1.105 | 0.797 | 0.223 | 0.231 | bend/corner induced residual |
| `bend_artifact_trace__v93` | `bend_artifact` | `unet_no_topology` | yes | 0.488 | 0.041 | 2 | 1 | 1.000 | 1.000 | n/a | 1.308 | 0.896 | 0.223 | 0.602 | bend/corner induced residual |
| `bend_artifact_trace__v94` | `bend_artifact` | `unet_no_topology` | no | 0.167 | 0.026 | 0 | 0 | 0.000 | 2.000 | n/a | 1.050 | 0.627 | 0.182 | 0.211 | no false positive |
| `bend_artifact_trace__v95` | `bend_artifact` | `unet_no_topology` | yes | 0.350 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 1.242 | 0.816 | 0.164 | 0.131 | bend/corner induced residual |
| `bend_artifact_trace__v96` | `bend_artifact` | `unet_no_topology` | yes | 0.785 | 0.050 | 2 | 1 | 0.000 | 0.000 | n/a | 2.212 | 1.042 | 0.162 | 0.167 | bend/corner induced residual |
| `bend_artifact_trace__v97` | `bend_artifact` | `unet_no_topology` | yes | 0.561 | 0.039 | 2 | 1 | 0.000 | 0.000 | n/a | 2.065 | 1.052 | 0.217 | 0.181 | bend/corner induced residual |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_no_topology` | yes | 0.549 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 2.367 | 1.092 | 0.208 | 0.453 | bend/corner induced residual |
| `bend_artifact_trace__v99` | `bend_artifact` | `unet_no_topology` | yes | 0.552 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 2.185 | 1.186 | 0.119 | 0.133 | bend/corner induced residual |
| `straight_trace` | `canonical` | `unet_topology_soft_loss` | no | 0.034 | 0.007 | 0 | 0 | 1.000 | n/a | n/a | 0.375 | 1.136 | 0.004 | 0.021 | no false positive |
| `finite_width_trace` | `canonical` | `unet_topology_soft_loss` | no | 0.077 | 0.007 | 0 | 0 | 1.000 | n/a | n/a | 0.280 | 0.961 | 0.194 | 0.179 | no false positive |
| `l_shape_trace` | `canonical` | `unet_topology_soft_loss` | yes | 0.477 | 0.047 | 3 | 2 | 0.000 | 0.000 | n/a | 0.638 | 0.465 | 0.004 | 0.171 | bend/corner induced residual |
| `no_via_background` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.229 | 0.027 | 3 | 1 | 1.000 | 1.000 | n/a | 0.915 | 0.692 | 0.265 | 0.683 | bend/corner induced residual |
| `no_via_background__v01` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.464 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.035 | 0.942 | 0.197 | 0.248 | bend/corner induced residual |
| `no_via_background__v02` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.568 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 0.832 | 0.967 | 0.146 | 0.165 | bend/corner induced residual |
| `no_via_background__v03` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.390 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.642 | 0.881 | 0.146 | 0.156 | bend/corner induced residual |
| `no_via_background__v04` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.435 | 0.036 | 2 | 1 | 1.000 | 1.000 | n/a | 0.929 | 0.934 | 0.231 | 0.470 | bend/corner induced residual |
| `no_via_background__v05` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.379 | 0.034 | 2 | 1 | 0.000 | 0.000 | n/a | 0.972 | 0.901 | 0.215 | 0.281 | bend/corner induced residual |
| `no_via_background__v06` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.602 | 0.039 | 1 | 1 | 1.000 | 1.000 | n/a | 0.989 | 0.912 | 0.214 | 0.479 | bend/corner induced residual |
| `no_via_background__v07` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.649 | 0.042 | 1 | 1 | 0.000 | 0.000 | n/a | 0.856 | 0.727 | 0.171 | 0.196 | bend/corner induced residual |
| `no_via_background__v08` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.350 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.512 | 0.833 | 0.203 | 0.475 | bend/corner induced residual |
| `no_via_background__v09` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.602 | 0.040 | 2 | 2 | 0.000 | 0.000 | n/a | 1.026 | 0.856 | 0.183 | 0.369 | bend/corner induced residual |
| `no_via_background__v10` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.542 | 0.041 | 3 | 2 | 0.000 | 0.000 | n/a | 0.821 | 0.828 | 0.136 | 0.165 | bend/corner induced residual |
| `no_via_background__v11` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.448 | 0.036 | 2 | 1 | 0.000 | 0.000 | n/a | 1.272 | 0.878 | 0.176 | 0.281 | bend/corner induced residual |
| `no_via_background__v12` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.324 | 0.023 | 1 | 1 | 0.000 | 2.000 | n/a | 0.788 | 0.629 | 0.222 | 0.167 | bend/corner induced residual |
| `no_via_background__v13` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.270 | 0.029 | 2 | 2 | 0.000 | 5.000 | n/a | 0.581 | 0.681 | 0.195 | 0.145 | operator mismatch |
| `no_via_background__v14` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.315 | 0.025 | 1 | 1 | 0.000 | 2.000 | n/a | 0.628 | 0.633 | 0.210 | 0.499 | bend/corner induced residual |
| `no_via_background__v15` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.235 | 0.027 | 1 | 1 | 0.000 | 2.000 | n/a | 0.612 | 0.617 | 0.116 | 0.125 | bend/corner induced residual |
| `no_via_background__v16` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.377 | 0.041 | 3 | 3 | 0.000 | 0.000 | n/a | 0.918 | 0.550 | 0.165 | 0.347 | bend/corner induced residual |
| `no_via_background__v17` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.512 | 0.042 | 2 | 2 | 0.000 | 5.000 | n/a | 0.934 | 0.538 | 0.176 | 0.388 | operator mismatch |
| `no_via_background__v18` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.256 | 0.030 | 1 | 1 | 0.000 | 5.000 | n/a | 0.910 | 0.536 | 0.194 | 0.465 | operator mismatch |
| `no_via_background__v19` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.392 | 0.032 | 2 | 2 | 0.000 | 6.000 | n/a | 0.907 | 0.523 | 0.170 | 0.499 | operator mismatch |
| `no_via_background__v20` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.347 | 0.035 | 4 | 3 | 0.000 | 5.000 | n/a | 0.963 | 0.698 | 0.253 | 0.291 | operator mismatch |
| `no_via_background__v21` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.436 | 0.040 | 4 | 4 | 0.000 | 5.000 | n/a | 0.898 | 0.572 | 0.201 | 0.292 | operator mismatch |
| `no_via_background__v22` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.333 | 0.043 | 5 | 4 | 0.000 | 5.000 | n/a | 0.849 | 0.610 | 0.143 | 0.247 | model hallucination |
| `no_via_background__v23` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.439 | 0.047 | 5 | 4 | 1.000 | 3.162 | n/a | 0.890 | 0.597 | 0.174 | 0.496 | operator mismatch |
| `no_via_background__v24` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.595 | 0.038 | 1 | 1 | 0.000 | 0.000 | n/a | 1.145 | 0.890 | 0.165 | 0.400 | bend/corner induced residual |
| `no_via_background__v25` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.655 | 0.042 | 1 | 1 | 0.000 | 0.000 | n/a | 1.056 | 0.816 | 0.194 | 0.314 | bend/corner induced residual |
| `no_via_background__v26` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.460 | 0.044 | 5 | 2 | 0.000 | 0.000 | n/a | 0.854 | 0.836 | 0.210 | 0.448 | bend/corner induced residual |
| `no_via_background__v27` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.456 | 0.043 | 4 | 2 | 0.000 | 0.000 | n/a | 0.866 | 0.811 | 0.171 | 0.178 | bend/corner induced residual |
| `no_via_background__v28` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.333 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.432 | 0.989 | 0.163 | 0.328 | bend/corner induced residual |
| `no_via_background__v29` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.296 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.210 | 0.892 | 0.231 | 0.369 | bend/corner induced residual |
| `no_via_background__v30` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.398 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.000 | 0.757 | 0.146 | 0.379 | bend/corner induced residual |
| `no_via_background__v31` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.203 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.220 | 0.769 | 0.176 | 0.538 | bend/corner induced residual |
| `no_via_background__v32` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.595 | 0.038 | 1 | 1 | 0.000 | 0.000 | n/a | 1.014 | 0.991 | 0.264 | 0.126 | bend/corner induced residual |
| `no_via_background__v33` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.370 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.766 | 0.973 | 0.207 | 0.304 | bend/corner induced residual |
| `no_via_background__v34` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.356 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.889 | 0.856 | 0.248 | 0.534 | bend/corner induced residual |
| `no_via_background__v35` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.512 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 1.086 | 0.684 | 0.209 | 0.648 | bend/corner induced residual |
| `no_via_background__v36` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.316 | 0.037 | 4 | 3 | 0.000 | 0.000 | n/a | 0.946 | 0.655 | 0.165 | 0.355 | bend/corner induced residual |
| `no_via_background__v37` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.441 | 0.039 | 3 | 2 | 0.000 | 5.000 | n/a | 0.827 | 0.513 | 0.160 | 0.322 | operator mismatch |
| `no_via_background__v38` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.397 | 0.037 | 2 | 2 | 0.000 | 0.000 | n/a | 0.868 | 0.678 | 0.185 | 0.427 | bend/corner induced residual |
| `no_via_background__v39` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.450 | 0.049 | 5 | 4 | 0.000 | 6.000 | n/a | 0.906 | 0.558 | 0.177 | 0.237 | operator mismatch |
| `no_via_background__v40` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.316 | 0.030 | 1 | 1 | 0.000 | 5.000 | n/a | 0.789 | 0.522 | 0.223 | 0.340 | operator mismatch |
| `no_via_background__v41` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.294 | 0.031 | 2 | 1 | 1.000 | 3.000 | n/a | 0.642 | 0.618 | 0.202 | 0.144 | operator mismatch |
| `no_via_background__v42` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.467 | 0.036 | 3 | 3 | 0.000 | 0.000 | n/a | 0.651 | 0.769 | 0.143 | 0.176 | bend/corner induced residual |
| `no_via_background__v43` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.315 | 0.035 | 5 | 4 | 0.000 | 0.000 | n/a | 0.716 | 0.610 | 0.179 | 0.181 | bend/corner induced residual |
| `no_via_background__v44` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.281 | 0.032 | 3 | 3 | 0.000 | 0.000 | n/a | 0.684 | 0.643 | 0.211 | 0.515 | bend/corner induced residual |
| `no_via_background__v45` | `no_via_background` | `unet_topology_soft_loss` | no | 0.167 | 0.023 | 0 | 0 | 1.000 | 3.162 | n/a | 0.653 | 0.647 | 0.203 | 0.144 | no false positive |
| `no_via_background__v46` | `no_via_background` | `unet_topology_soft_loss` | no | 0.190 | 0.027 | 0 | 0 | 0.000 | 0.000 | n/a | 0.701 | 0.720 | 0.263 | 0.485 | no false positive |
| `no_via_background__v47` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.220 | 0.024 | 1 | 1 | 0.000 | 6.000 | n/a | 0.680 | 0.724 | 0.151 | 0.094 | operator mismatch |
| `no_via_background__v48` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.207 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.710 | 1.028 | 0.135 | 0.246 | bend/corner induced residual |
| `no_via_background__v49` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.476 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.779 | 0.961 | 0.197 | 0.176 | bend/corner induced residual |
| `no_via_background__v50` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.542 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 0.916 | 0.899 | 0.135 | 0.233 | bend/corner induced residual |
| `no_via_background__v51` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.363 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.789 | 0.790 | 0.109 | 0.229 | bend/corner induced residual |
| `no_via_background__v52` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.808 | 0.049 | 1 | 1 | 0.000 | 0.000 | n/a | 1.366 | 0.778 | 0.234 | 0.629 | bend/corner induced residual |
| `no_via_background__v53` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.456 | 0.037 | 2 | 1 | 0.000 | 0.000 | n/a | 0.918 | 0.787 | 0.170 | 0.506 | bend/corner induced residual |
| `no_via_background__v54` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.322 | 0.029 | 2 | 1 | 0.000 | 0.000 | n/a | 0.926 | 0.831 | 0.263 | 0.730 | bend/corner induced residual |
| `no_via_background__v55` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.401 | 0.035 | 2 | 1 | 0.000 | 0.000 | n/a | 0.865 | 0.684 | 0.239 | 0.522 | bend/corner induced residual |
| `no_via_background__v56` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.871 | 0.054 | 2 | 2 | 0.000 | 0.000 | n/a | 0.951 | 0.752 | 0.211 | 0.785 | bend/corner induced residual |
| `no_via_background__v57` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.426 | 0.039 | 3 | 3 | 0.000 | 0.000 | n/a | 0.912 | 0.832 | 0.211 | 0.170 | bend/corner induced residual |
| `no_via_background__v58` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.678 | 0.043 | 1 | 1 | 0.000 | 0.000 | n/a | 1.000 | 0.777 | 0.185 | 0.552 | bend/corner induced residual |
| `no_via_background__v59` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.568 | 0.039 | 2 | 2 | 0.000 | 0.000 | n/a | 0.948 | 0.721 | 0.176 | 0.631 | bend/corner induced residual |
| `no_via_background__v60` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.311 | 0.031 | 2 | 2 | 0.000 | 5.000 | n/a | 0.792 | 0.700 | 0.221 | 0.114 | operator mismatch |
| `no_via_background__v61` | `no_via_background` | `unet_topology_soft_loss` | no | 0.190 | 0.027 | 0 | 0 | 0.000 | 0.000 | n/a | 0.701 | 0.720 | 0.202 | 0.166 | no false positive |
| `no_via_background__v62` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.233 | 0.027 | 2 | 2 | 0.000 | 5.000 | n/a | 0.605 | 0.631 | 0.143 | 0.113 | model hallucination |
| `no_via_background__v63` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.235 | 0.024 | 1 | 1 | 0.000 | 5.000 | n/a | 0.646 | 0.671 | 0.177 | 0.174 | operator mismatch |
| `no_via_background__v64` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.380 | 0.042 | 5 | 4 | 0.000 | 0.000 | n/a | 0.988 | 0.526 | 0.155 | 0.398 | bend/corner induced residual |
| `no_via_background__v65` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.247 | 0.032 | 3 | 3 | 0.000 | 4.000 | n/a | 0.985 | 0.520 | 0.192 | 0.448 | operator mismatch |
| `no_via_background__v66` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.443 | 0.045 | 4 | 4 | 1.000 | 5.099 | n/a | 0.975 | 0.510 | 0.248 | 0.749 | operator mismatch |
| `no_via_background__v67` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.468 | 0.044 | 3 | 3 | 0.000 | 5.000 | n/a | 0.858 | 0.508 | 0.153 | 0.397 | operator mismatch |
| `no_via_background__v68` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.406 | 0.037 | 3 | 3 | 0.000 | 0.000 | n/a | 0.945 | 0.617 | 0.203 | 0.434 | bend/corner induced residual |
| `no_via_background__v69` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.378 | 0.045 | 5 | 4 | 0.000 | 0.000 | n/a | 0.818 | 0.614 | 0.230 | 0.241 | bend/corner induced residual |
| `no_via_background__v70` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.362 | 0.034 | 2 | 2 | 0.000 | 5.000 | n/a | 0.943 | 0.643 | 0.143 | 0.319 | detector threshold sensitivity |
| `no_via_background__v71` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.365 | 0.034 | 3 | 3 | 0.000 | 0.000 | n/a | 1.201 | 0.696 | 0.218 | 0.421 | bend/corner induced residual |
| `no_via_background__v72` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.536 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 1.114 | 0.822 | 0.262 | 0.402 | bend/corner induced residual |
| `no_via_background__v73` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.576 | 0.037 | 2 | 2 | 0.000 | 0.000 | n/a | 0.942 | 0.759 | 0.205 | 0.584 | bend/corner induced residual |
| `no_via_background__v74` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.602 | 0.040 | 2 | 2 | 0.000 | 0.000 | n/a | 1.026 | 0.856 | 0.248 | 0.516 | bend/corner induced residual |
| `no_via_background__v75` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.790 | 0.049 | 1 | 1 | 0.000 | 0.000 | n/a | 1.094 | 0.818 | 0.091 | 0.097 | bend/corner induced residual |
| `no_via_background__v76` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.347 | 0.026 | 1 | 1 | 1.000 | 1.000 | n/a | 1.251 | 0.966 | 0.263 | 0.836 | bend/corner induced residual |
| `no_via_background__v77` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.467 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.957 | 0.733 | 0.193 | 0.472 | bend/corner induced residual |
| `no_via_background__v78` | `no_via_background` | `unet_topology_soft_loss` | no | 0.199 | 0.022 | 0 | 0 | 0.000 | 0.000 | n/a | 0.883 | 0.833 | 0.166 | 0.405 | no false positive |
| `no_via_background__v79` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.266 | 0.024 | 2 | 1 | 1.000 | 1.000 | n/a | 0.760 | 0.785 | 0.170 | 0.412 | bend/corner induced residual |
| `no_via_background__v80` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.399 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.136 | 1.001 | 0.232 | 0.164 | bend/corner induced residual |
| `no_via_background__v81` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.464 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.035 | 0.942 | 0.197 | 0.248 | bend/corner induced residual |
| `no_via_background__v82` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.568 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 0.832 | 0.967 | 0.146 | 0.165 | bend/corner induced residual |
| `no_via_background__v83` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.390 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.642 | 0.881 | 0.146 | 0.156 | bend/corner induced residual |
| `no_via_background__v84` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.297 | 0.037 | 3 | 2 | 0.000 | 5.000 | n/a | 0.813 | 0.713 | 0.143 | 0.347 | model hallucination |
| `no_via_background__v85` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.308 | 0.032 | 2 | 2 | 0.000 | 5.000 | n/a | 0.994 | 0.683 | 0.203 | 0.367 | detector threshold sensitivity |
| `no_via_background__v86` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.436 | 0.040 | 4 | 4 | 1.000 | 5.099 | n/a | 0.898 | 0.572 | 0.248 | 0.638 | operator mismatch |
| `no_via_background__v87` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.469 | 0.048 | 4 | 4 | 0.000 | 5.000 | n/a | 0.810 | 0.539 | 0.159 | 0.248 | operator mismatch |
| `no_via_background__v88` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.341 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.736 | 0.730 | 0.260 | 0.725 | bend/corner induced residual |
| `no_via_background__v89` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.315 | 0.032 | 3 | 3 | 0.000 | 0.000 | n/a | 0.719 | 0.693 | 0.183 | 0.163 | bend/corner induced residual |
| `no_via_background__v90` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.222 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 0.663 | 0.560 | 0.143 | 0.160 | bend/corner induced residual |
| `no_via_background__v91` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.649 | 0.043 | 1 | 1 | 0.000 | 3.000 | n/a | 0.738 | 0.544 | 0.248 | 0.482 | operator mismatch |
| `no_via_background__v92` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.324 | 0.023 | 1 | 1 | 0.000 | 2.000 | n/a | 0.788 | 0.629 | 0.222 | 0.167 | bend/corner induced residual |
| `no_via_background__v93` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.270 | 0.029 | 2 | 2 | 0.000 | 5.000 | n/a | 0.581 | 0.681 | 0.195 | 0.145 | operator mismatch |
| `no_via_background__v94` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.315 | 0.025 | 1 | 1 | 0.000 | 2.000 | n/a | 0.628 | 0.633 | 0.210 | 0.499 | bend/corner induced residual |
| `no_via_background__v95` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.225 | 0.026 | 1 | 1 | 0.000 | 2.000 | n/a | 0.610 | 0.575 | 0.182 | 0.232 | bend/corner induced residual |
| `no_via_background__v96` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.380 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.050 | 0.964 | 0.155 | 0.165 | bend/corner induced residual |
| `bend_artifact_trace` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.364 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.104 | 0.823 | 0.217 | 0.259 | bend/corner induced residual |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.460 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 1.132 | 0.769 | 0.176 | 0.366 | bend/corner induced residual |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.144 | 0.019 | 0 | 0 | 0.000 | 0.000 | n/a | 1.459 | 0.729 | 0.190 | 0.258 | no false positive |
| `bend_artifact_trace__v03` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.176 | 0.020 | 0 | 0 | 0.000 | 0.000 | n/a | 1.219 | 0.828 | 0.146 | 0.139 | no false positive |
| `bend_artifact_trace__v04` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.536 | 0.040 | 2 | 2 | 0.000 | 0.000 | n/a | 1.386 | 0.635 | 0.196 | 0.619 | bend/corner induced residual |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.441 | 0.034 | 2 | 2 | 0.000 | 0.000 | n/a | 1.294 | 0.787 | 0.229 | 0.538 | bend/corner induced residual |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.511 | 0.039 | 2 | 2 | 0.000 | 0.000 | n/a | 1.174 | 0.573 | 0.134 | 0.712 | bend/corner induced residual |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.433 | 0.037 | 2 | 2 | 0.000 | 0.000 | n/a | 0.890 | 0.511 | 0.207 | 0.710 | bend/corner induced residual |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.524 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 0.969 | 0.711 | 0.173 | 0.235 | bend/corner induced residual |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.402 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.036 | 0.655 | 0.236 | 0.267 | bend/corner induced residual |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.554 | 0.042 | 4 | 3 | 0.000 | 0.000 | n/a | 1.047 | 0.632 | 0.187 | 0.468 | bend/corner induced residual |
| `bend_artifact_trace__v11` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.434 | 0.037 | 2 | 2 | 0.000 | 0.000 | n/a | 1.053 | 0.632 | 0.150 | 0.263 | bend/corner induced residual |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.299 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.873 | 0.895 | 0.223 | 0.221 | bend/corner induced residual |
| `bend_artifact_trace__v13` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.241 | 0.031 | 3 | 2 | 0.000 | 1.000 | n/a | 1.078 | 0.832 | 0.238 | 0.637 | bend/corner induced residual |
| `bend_artifact_trace__v14` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.237 | 0.026 | 2 | 2 | 1.000 | 4.000 | n/a | 0.861 | 0.550 | 0.162 | 0.373 | operator mismatch |
| `bend_artifact_trace__v15` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.217 | 0.029 | 2 | 1 | 0.000 | 3.000 | n/a | 0.899 | 0.626 | 0.164 | 0.337 | operator mismatch |
| `bend_artifact_trace__v16` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.467 | 0.041 | 2 | 2 | 0.000 | 0.000 | n/a | 1.123 | 0.639 | 0.214 | 0.553 | bend/corner induced residual |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.360 | 0.036 | 3 | 3 | 0.000 | 0.000 | n/a | 1.223 | 0.682 | 0.219 | 0.580 | bend/corner induced residual |
| `bend_artifact_trace__v18` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.504 | 0.054 | 4 | 4 | 0.000 | 0.000 | n/a | 0.950 | 0.625 | 0.167 | 0.322 | bend/corner induced residual |
| `bend_artifact_trace__v19` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.578 | 0.051 | 3 | 3 | 0.000 | 0.000 | n/a | 1.190 | 0.621 | 0.204 | 0.468 | bend/corner induced residual |
| `bend_artifact_trace__v20` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.373 | 0.038 | 3 | 2 | 0.000 | 0.000 | n/a | 1.465 | 0.793 | 0.245 | 0.550 | bend/corner induced residual |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.422 | 0.045 | 3 | 3 | 0.000 | 2.000 | n/a | 1.616 | 0.653 | 0.216 | 0.521 | bend/corner induced residual |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.277 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.028 | 0.538 | 0.233 | 0.547 | bend/corner induced residual |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.361 | 0.038 | 4 | 4 | 0.000 | 2.000 | n/a | 1.319 | 0.673 | 0.218 | 0.510 | bend/corner induced residual |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.587 | 0.039 | 1 | 1 | 0.000 | 0.000 | n/a | 1.256 | 0.821 | 0.214 | 0.544 | bend/corner induced residual |
| `bend_artifact_trace__v25` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.255 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.210 | 0.625 | 0.233 | 0.504 | bend/corner induced residual |
| `bend_artifact_trace__v26` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.478 | 0.035 | 2 | 2 | 0.000 | 0.000 | n/a | 1.100 | 0.665 | 0.162 | 0.488 | bend/corner induced residual |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.415 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 0.889 | 0.679 | 0.177 | 0.200 | bend/corner induced residual |
| `bend_artifact_trace__v28` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.346 | 0.037 | 3 | 2 | 0.000 | 0.000 | n/a | 1.108 | 0.843 | 0.222 | 0.825 | bend/corner induced residual |
| `bend_artifact_trace__v29` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.429 | 0.042 | 3 | 3 | 0.000 | 0.000 | n/a | 1.136 | 0.781 | 0.202 | 0.720 | bend/corner induced residual |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.532 | 0.049 | 3 | 3 | 0.000 | 0.000 | n/a | 1.457 | 0.783 | 0.154 | 0.726 | bend/corner induced residual |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.472 | 0.046 | 3 | 3 | 0.000 | 0.000 | n/a | 1.254 | 0.690 | 0.150 | 0.682 | bend/corner induced residual |
| `bend_artifact_trace__v32` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.272 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.423 | 1.018 | 0.229 | 0.144 | bend/corner induced residual |
| `bend_artifact_trace__v33` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.184 | 0.019 | 0 | 0 | 0.000 | 0.000 | n/a | 1.098 | 0.904 | 0.158 | 0.143 | no false positive |
| `bend_artifact_trace__v34` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.328 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.135 | 0.899 | 0.247 | 0.392 | bend/corner induced residual |
| `bend_artifact_trace__v35` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.397 | 0.037 | 2 | 2 | 0.000 | 0.000 | n/a | 1.240 | 0.728 | 0.237 | 0.384 | bend/corner induced residual |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.500 | 0.047 | 5 | 4 | 0.000 | 0.000 | n/a | 1.559 | 0.688 | 0.214 | 0.576 | bend/corner induced residual |
| `bend_artifact_trace__v37` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.287 | 0.029 | 2 | 2 | 0.000 | 3.000 | n/a | 1.239 | 0.527 | 0.240 | 0.596 | operator mismatch |
| `bend_artifact_trace__v38` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.348 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 1.421 | 0.579 | 0.219 | 0.710 | bend/corner induced residual |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.515 | 0.046 | 3 | 3 | 0.000 | 3.000 | n/a | 1.123 | 0.505 | 0.113 | 0.428 | model hallucination |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.585 | 0.047 | 4 | 3 | 0.000 | 0.000 | n/a | 1.199 | 0.732 | 0.222 | 0.447 | bend/corner induced residual |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.466 | 0.039 | 2 | 2 | 0.000 | 0.000 | n/a | 1.392 | 0.665 | 0.234 | 0.483 | bend/corner induced residual |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.342 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 1.024 | 0.729 | 0.210 | 0.254 | bend/corner induced residual |
| `bend_artifact_trace__v43` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.274 | 0.028 | 2 | 2 | 1.000 | 4.000 | n/a | 1.009 | 0.750 | 0.202 | 0.259 | operator mismatch |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.547 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 0.939 | 0.623 | 0.213 | 0.497 | bend/corner induced residual |
| `bend_artifact_trace__v45` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.188 | 0.027 | 0 | 0 | 0.000 | 2.000 | n/a | 0.857 | 0.660 | 0.178 | 0.416 | no false positive |
| `bend_artifact_trace__v46` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.288 | 0.035 | 3 | 2 | 1.000 | 2.236 | n/a | 0.889 | 0.569 | 0.248 | 0.538 | operator mismatch |
| `bend_artifact_trace__v47` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.262 | 0.037 | 4 | 4 | 0.000 | 0.000 | n/a | 0.968 | 0.511 | 0.189 | 0.539 | bend/corner induced residual |
| `bend_artifact_trace__v48` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.229 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 1.115 | 0.965 | 0.159 | 0.143 | bend/corner induced residual |
| `bend_artifact_trace__v49` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.320 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 1.037 | 0.866 | 0.234 | 0.157 | bend/corner induced residual |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.406 | 0.031 | 2 | 1 | 0.000 | 0.000 | n/a | 1.135 | 0.715 | 0.188 | 0.362 | bend/corner induced residual |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.270 | 0.029 | 3 | 2 | 0.000 | 0.000 | n/a | 1.011 | 0.757 | 0.152 | 0.294 | bend/corner induced residual |
| `bend_artifact_trace__v52` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.753 | 0.048 | 1 | 1 | 0.000 | 0.000 | n/a | 1.335 | 0.971 | 0.252 | 0.563 | bend/corner induced residual |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.752 | 0.050 | 2 | 2 | 0.000 | 0.000 | n/a | 1.328 | 0.850 | 0.225 | 0.605 | bend/corner induced residual |
| `bend_artifact_trace__v54` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.528 | 0.040 | 2 | 2 | 0.000 | 0.000 | n/a | 1.351 | 0.683 | 0.248 | 0.657 | bend/corner induced residual |
| `bend_artifact_trace__v55` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.640 | 0.042 | 1 | 1 | 0.000 | 0.000 | n/a | 1.064 | 0.609 | 0.256 | 0.427 | bend/corner induced residual |
| `bend_artifact_trace__v56` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.528 | 0.042 | 2 | 2 | 0.000 | 0.000 | n/a | 1.115 | 0.738 | 0.213 | 0.364 | bend/corner induced residual |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.626 | 0.042 | 1 | 1 | 0.000 | 0.000 | n/a | 0.912 | 0.640 | 0.186 | 0.272 | bend/corner induced residual |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.425 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 1.054 | 0.733 | 0.253 | 0.211 | bend/corner induced residual |
| `bend_artifact_trace__v59` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.278 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 0.875 | 0.617 | 0.180 | 0.556 | bend/corner induced residual |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.364 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 0.951 | 0.727 | 0.194 | 0.381 | bend/corner induced residual |
| `bend_artifact_trace__v61` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.308 | 0.037 | 3 | 2 | 0.000 | 2.000 | n/a | 0.926 | 0.628 | 0.234 | 0.288 | bend/corner induced residual |
| `bend_artifact_trace__v62` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.220 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.992 | 0.506 | 0.233 | 0.405 | bend/corner induced residual |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.208 | 0.030 | 2 | 2 | 1.000 | 1.000 | n/a | 0.953 | 0.603 | 0.222 | 0.386 | bend/corner induced residual |
| `bend_artifact_trace__v64` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.294 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.276 | 0.682 | 0.162 | 0.581 | bend/corner induced residual |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.358 | 0.037 | 3 | 2 | 0.000 | 0.000 | n/a | 1.265 | 0.682 | 0.211 | 0.513 | bend/corner induced residual |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.278 | 0.034 | 3 | 3 | 0.000 | 2.000 | n/a | 1.126 | 0.605 | 0.247 | 0.542 | bend/corner induced residual |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.578 | 0.052 | 4 | 4 | 0.000 | 0.000 | n/a | 1.212 | 0.616 | 0.192 | 0.573 | bend/corner induced residual |
| `bend_artifact_trace__v68` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.210 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.441 | 0.681 | 0.173 | 0.753 | bend/corner induced residual |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.365 | 0.039 | 5 | 4 | 0.000 | 3.000 | n/a | 1.351 | 0.578 | 0.162 | 0.485 | detector threshold sensitivity |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.363 | 0.040 | 4 | 3 | 0.000 | 0.000 | n/a | 1.553 | 0.786 | 0.210 | 0.500 | bend/corner induced residual |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.279 | 0.030 | 2 | 2 | 0.000 | 3.000 | n/a | 1.483 | 0.700 | 0.251 | 0.655 | detector threshold sensitivity |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.592 | 0.039 | 1 | 1 | 0.000 | 0.000 | n/a | 1.014 | 0.724 | 0.218 | 0.259 | bend/corner induced residual |
| `bend_artifact_trace__v73` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.448 | 0.038 | 3 | 2 | 0.000 | 0.000 | n/a | 0.791 | 0.655 | 0.185 | 0.546 | bend/corner induced residual |
| `bend_artifact_trace__v74` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.412 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 1.243 | 0.720 | 0.247 | 0.401 | bend/corner induced residual |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.626 | 0.040 | 1 | 1 | 0.000 | 0.000 | n/a | 1.048 | 0.716 | 0.211 | 0.299 | bend/corner induced residual |
| `bend_artifact_trace__v76` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.564 | 0.044 | 3 | 3 | 0.000 | 0.000 | n/a | 1.257 | 0.736 | 0.257 | 0.674 | bend/corner induced residual |
| `bend_artifact_trace__v77` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.288 | 0.033 | 3 | 2 | 0.000 | 0.000 | n/a | 1.366 | 0.732 | 0.194 | 0.783 | bend/corner induced residual |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.522 | 0.039 | 3 | 3 | 0.000 | 0.000 | n/a | 1.027 | 0.603 | 0.183 | 0.710 | bend/corner induced residual |
| `bend_artifact_trace__v79` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.461 | 0.047 | 3 | 3 | 0.000 | 0.000 | n/a | 1.173 | 0.614 | 0.204 | 0.751 | bend/corner induced residual |
| `bend_artifact_trace__v80` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.362 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 1.107 | 0.985 | 0.252 | 0.260 | bend/corner induced residual |
| `bend_artifact_trace__v81` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.465 | 0.035 | 2 | 2 | 0.000 | 0.000 | n/a | 1.223 | 0.771 | 0.143 | 0.330 | bend/corner induced residual |
| `bend_artifact_trace__v82` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.253 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.148 | 0.886 | 0.206 | 0.429 | bend/corner induced residual |
| `bend_artifact_trace__v83` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.358 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.244 | 0.750 | 0.191 | 0.245 | bend/corner induced residual |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.426 | 0.039 | 3 | 2 | 0.000 | 3.000 | n/a | 1.466 | 0.799 | 0.136 | 0.424 | detector threshold sensitivity |
| `bend_artifact_trace__v85` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.238 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.505 | 0.787 | 0.178 | 0.542 | bend/corner induced residual |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.474 | 0.036 | 1 | 1 | 0.000 | 2.000 | n/a | 1.469 | 0.666 | 0.247 | 0.635 | bend/corner induced residual |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.281 | 0.038 | 6 | 5 | 0.000 | 0.000 | n/a | 1.141 | 0.538 | 0.159 | 0.594 | bend/corner induced residual |
| `bend_artifact_trace__v88` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.277 | 0.036 | 4 | 4 | 0.000 | 0.000 | n/a | 0.854 | 0.634 | 0.256 | 0.742 | bend/corner induced residual |
| `bend_artifact_trace__v89` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.272 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 1.350 | 0.702 | 0.236 | 0.477 | bend/corner induced residual |
| `bend_artifact_trace__v90` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.212 | 0.031 | 3 | 3 | 0.000 | 3.000 | n/a | 0.829 | 0.661 | 0.233 | 0.488 | detector threshold sensitivity |
| `bend_artifact_trace__v91` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.291 | 0.034 | 2 | 1 | 0.000 | 0.000 | n/a | 1.008 | 0.729 | 0.246 | 0.365 | bend/corner induced residual |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.299 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.873 | 0.895 | 0.223 | 0.221 | bend/corner induced residual |
| `bend_artifact_trace__v93` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.234 | 0.031 | 4 | 2 | 0.000 | 1.000 | n/a | 1.036 | 0.826 | 0.223 | 0.603 | bend/corner induced residual |
| `bend_artifact_trace__v94` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.193 | 0.026 | 0 | 0 | 1.000 | 3.000 | n/a | 0.853 | 0.553 | 0.182 | 0.299 | no false positive |
| `bend_artifact_trace__v95` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.217 | 0.029 | 2 | 1 | 0.000 | 3.000 | n/a | 0.899 | 0.626 | 0.164 | 0.337 | operator mismatch |
| `bend_artifact_trace__v96` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.372 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 1.294 | 0.896 | 0.162 | 0.211 | bend/corner induced residual |
| `bend_artifact_trace__v97` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.351 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.112 | 0.930 | 0.217 | 0.190 | bend/corner induced residual |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.235 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.197 | 0.963 | 0.208 | 0.268 | bend/corner induced residual |
| `bend_artifact_trace__v99` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.183 | 0.021 | 0 | 0 | 0.000 | 0.000 | n/a | 1.136 | 0.898 | 0.119 | 0.121 | no false positive |
| `straight_trace` | `canonical` | `unet_topology_two_stage_refined` | no | 0.022 | 0.004 | 0 | 0 | 1.000 | n/a | n/a | 0.389 | 1.137 | 0.004 | 0.021 | no false positive |
| `finite_width_trace` | `canonical` | `unet_topology_two_stage_refined` | no | 0.050 | 0.005 | 0 | 0 | 1.000 | n/a | n/a | 0.274 | 0.961 | 0.194 | 0.179 | no false positive |
| `l_shape_trace` | `canonical` | `unet_topology_two_stage_refined` | yes | 0.310 | 0.031 | 3 | 2 | 0.000 | 0.000 | n/a | 0.495 | 0.463 | 0.004 | 0.171 | bend/corner induced residual |
| `no_via_background` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.149 | 0.018 | 0 | 0 | 1.000 | 1.000 | n/a | 0.912 | 0.691 | 0.265 | 0.683 | no false positive |
| `no_via_background__v01` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.302 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.958 | 0.939 | 0.197 | 0.248 | bend/corner induced residual |
| `no_via_background__v02` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.369 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 0.725 | 0.963 | 0.146 | 0.165 | bend/corner induced residual |
| `no_via_background__v03` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.253 | 0.018 | 1 | 1 | 0.000 | 0.000 | n/a | 0.597 | 0.880 | 0.146 | 0.156 | bend/corner induced residual |
| `no_via_background__v04` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.283 | 0.023 | 2 | 1 | 1.000 | 1.000 | n/a | 0.869 | 0.934 | 0.231 | 0.470 | bend/corner induced residual |
| `no_via_background__v05` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.246 | 0.022 | 2 | 1 | 0.000 | 0.000 | n/a | 0.906 | 0.900 | 0.215 | 0.281 | bend/corner induced residual |
| `no_via_background__v06` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.391 | 0.025 | 1 | 1 | 1.000 | 1.000 | n/a | 0.898 | 0.914 | 0.214 | 0.479 | bend/corner induced residual |
| `no_via_background__v07` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.422 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.721 | 0.728 | 0.171 | 0.196 | bend/corner induced residual |
| `no_via_background__v08` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.287 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.563 | 0.833 | 0.203 | 0.475 | bend/corner induced residual |
| `no_via_background__v09` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.391 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.041 | 0.857 | 0.183 | 0.369 | bend/corner induced residual |
| `no_via_background__v10` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.410 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 0.799 | 0.829 | 0.136 | 0.165 | bend/corner induced residual |
| `no_via_background__v11` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.355 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.285 | 0.877 | 0.176 | 0.281 | bend/corner induced residual |
| `no_via_background__v12` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.210 | 0.015 | 1 | 1 | 0.000 | 2.000 | n/a | 0.768 | 0.628 | 0.222 | 0.167 | bend/corner induced residual |
| `no_via_background__v13` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.176 | 0.019 | 0 | 0 | 0.000 | 5.000 | n/a | 0.544 | 0.679 | 0.195 | 0.145 | no false positive |
| `no_via_background__v14` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.205 | 0.017 | 1 | 1 | 0.000 | 2.000 | n/a | 0.607 | 0.633 | 0.210 | 0.499 | bend/corner induced residual |
| `no_via_background__v15` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.153 | 0.017 | 0 | 0 | 0.000 | 2.000 | n/a | 0.555 | 0.617 | 0.116 | 0.125 | no false positive |
| `no_via_background__v16` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.245 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 0.851 | 0.549 | 0.165 | 0.347 | bend/corner induced residual |
| `no_via_background__v17` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.333 | 0.027 | 2 | 2 | 0.000 | 5.000 | n/a | 0.856 | 0.538 | 0.176 | 0.388 | operator mismatch |
| `no_via_background__v18` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.166 | 0.020 | 0 | 0 | 0.000 | 5.000 | n/a | 0.895 | 0.534 | 0.194 | 0.465 | no false positive |
| `no_via_background__v19` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.255 | 0.021 | 1 | 1 | 0.000 | 6.000 | n/a | 0.905 | 0.522 | 0.170 | 0.499 | operator mismatch |
| `no_via_background__v20` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.226 | 0.023 | 1 | 1 | 0.000 | 5.000 | n/a | 0.930 | 0.698 | 0.253 | 0.291 | operator mismatch |
| `no_via_background__v21` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.283 | 0.026 | 2 | 2 | 0.000 | 5.000 | n/a | 0.791 | 0.570 | 0.201 | 0.292 | operator mismatch |
| `no_via_background__v22` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.217 | 0.028 | 3 | 3 | 0.000 | 5.000 | n/a | 0.755 | 0.608 | 0.143 | 0.247 | model hallucination |
| `no_via_background__v23` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.286 | 0.031 | 2 | 2 | 1.000 | 3.162 | n/a | 0.843 | 0.595 | 0.174 | 0.496 | operator mismatch |
| `no_via_background__v24` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.387 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.172 | 0.890 | 0.165 | 0.400 | bend/corner induced residual |
| `no_via_background__v25` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.476 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.026 | 0.817 | 0.194 | 0.314 | bend/corner induced residual |
| `no_via_background__v26` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.299 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 0.866 | 0.838 | 0.210 | 0.448 | bend/corner induced residual |
| `no_via_background__v27` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.296 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 0.888 | 0.813 | 0.171 | 0.178 | bend/corner induced residual |
| `no_via_background__v28` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.217 | 0.015 | 1 | 1 | 0.000 | 0.000 | n/a | 1.410 | 0.988 | 0.163 | 0.328 | bend/corner induced residual |
| `no_via_background__v29` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.192 | 0.014 | 0 | 0 | 0.000 | 0.000 | n/a | 1.185 | 0.892 | 0.231 | 0.369 | no false positive |
| `no_via_background__v30` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.259 | 0.018 | 1 | 1 | 0.000 | 0.000 | n/a | 1.029 | 0.757 | 0.146 | 0.379 | bend/corner induced residual |
| `no_via_background__v31` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.132 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 1.247 | 0.759 | 0.176 | 0.538 | no false positive |
| `no_via_background__v32` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.387 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.883 | 0.987 | 0.264 | 0.126 | bend/corner induced residual |
| `no_via_background__v33` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.241 | 0.018 | 1 | 1 | 0.000 | 0.000 | n/a | 0.716 | 0.968 | 0.207 | 0.304 | bend/corner induced residual |
| `no_via_background__v34` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.232 | 0.017 | 1 | 1 | 0.000 | 0.000 | n/a | 0.844 | 0.856 | 0.248 | 0.534 | bend/corner induced residual |
| `no_via_background__v35` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.333 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.967 | 0.682 | 0.209 | 0.648 | bend/corner induced residual |
| `no_via_background__v36` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.205 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 0.890 | 0.653 | 0.165 | 0.355 | bend/corner induced residual |
| `no_via_background__v37` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.286 | 0.025 | 1 | 1 | 0.000 | 5.000 | n/a | 0.722 | 0.511 | 0.160 | 0.322 | operator mismatch |
| `no_via_background__v38` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.258 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.863 | 0.674 | 0.185 | 0.427 | bend/corner induced residual |
| `no_via_background__v39` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.293 | 0.032 | 4 | 3 | 0.000 | 6.000 | n/a | 0.768 | 0.557 | 0.177 | 0.237 | operator mismatch |
| `no_via_background__v40` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.205 | 0.020 | 1 | 1 | 0.000 | 5.000 | n/a | 0.741 | 0.522 | 0.223 | 0.340 | operator mismatch |
| `no_via_background__v41` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.191 | 0.020 | 0 | 0 | 1.000 | 3.000 | n/a | 0.631 | 0.618 | 0.202 | 0.144 | no false positive |
| `no_via_background__v42` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.304 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.597 | 0.768 | 0.143 | 0.176 | bend/corner induced residual |
| `no_via_background__v43` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.205 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.636 | 0.608 | 0.179 | 0.181 | bend/corner induced residual |
| `no_via_background__v44` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.183 | 0.021 | 0 | 0 | 0.000 | 0.000 | n/a | 0.672 | 0.643 | 0.211 | 0.515 | no false positive |
| `no_via_background__v45` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.109 | 0.015 | 0 | 0 | 1.000 | 3.162 | n/a | 0.644 | 0.646 | 0.203 | 0.144 | no false positive |
| `no_via_background__v46` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.123 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 0.717 | 0.718 | 0.263 | 0.485 | no false positive |
| `no_via_background__v47` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.143 | 0.016 | 0 | 0 | 0.000 | 6.000 | n/a | 0.653 | 0.723 | 0.151 | 0.094 | no false positive |
| `no_via_background__v48` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.134 | 0.016 | 0 | 0 | 0.000 | 0.000 | n/a | 0.669 | 1.023 | 0.135 | 0.246 | no false positive |
| `no_via_background__v49` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.309 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.702 | 0.958 | 0.197 | 0.176 | bend/corner induced residual |
| `no_via_background__v50` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.352 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.757 | 0.896 | 0.135 | 0.233 | bend/corner induced residual |
| `no_via_background__v51` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.236 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.680 | 0.786 | 0.109 | 0.229 | bend/corner induced residual |
| `no_via_background__v52` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.525 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.345 | 0.772 | 0.234 | 0.629 | bend/corner induced residual |
| `no_via_background__v53` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.296 | 0.024 | 2 | 1 | 0.000 | 0.000 | n/a | 0.841 | 0.785 | 0.170 | 0.506 | bend/corner induced residual |
| `no_via_background__v54` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.210 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.886 | 0.830 | 0.263 | 0.730 | bend/corner induced residual |
| `no_via_background__v55` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.260 | 0.023 | 2 | 1 | 0.000 | 0.000 | n/a | 0.763 | 0.681 | 0.239 | 0.522 | bend/corner induced residual |
| `no_via_background__v56` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.637 | 0.039 | 1 | 1 | 0.000 | 0.000 | n/a | 0.837 | 0.751 | 0.211 | 0.785 | bend/corner induced residual |
| `no_via_background__v57` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.277 | 0.025 | 2 | 2 | 0.000 | 0.000 | n/a | 0.934 | 0.833 | 0.211 | 0.170 | bend/corner induced residual |
| `no_via_background__v58` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.440 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 0.969 | 0.777 | 0.185 | 0.552 | bend/corner induced residual |
| `no_via_background__v59` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.370 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.949 | 0.720 | 0.176 | 0.631 | bend/corner induced residual |
| `no_via_background__v60` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.202 | 0.020 | 1 | 1 | 0.000 | 5.000 | n/a | 0.731 | 0.699 | 0.221 | 0.114 | operator mismatch |
| `no_via_background__v61` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.123 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 0.717 | 0.718 | 0.202 | 0.166 | no false positive |
| `no_via_background__v62` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.151 | 0.017 | 0 | 0 | 0.000 | 5.000 | n/a | 0.566 | 0.630 | 0.143 | 0.113 | no false positive |
| `no_via_background__v63` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.153 | 0.016 | 0 | 0 | 0.000 | 5.000 | n/a | 0.604 | 0.669 | 0.177 | 0.174 | no false positive |
| `no_via_background__v64` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.247 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.922 | 0.524 | 0.155 | 0.398 | bend/corner induced residual |
| `no_via_background__v65` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.160 | 0.021 | 0 | 0 | 0.000 | 4.000 | n/a | 0.912 | 0.519 | 0.192 | 0.448 | no false positive |
| `no_via_background__v66` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.288 | 0.029 | 2 | 2 | 1.000 | 5.099 | n/a | 0.857 | 0.508 | 0.248 | 0.749 | operator mismatch |
| `no_via_background__v67` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.304 | 0.028 | 2 | 2 | 0.000 | 5.000 | n/a | 0.796 | 0.506 | 0.153 | 0.397 | operator mismatch |
| `no_via_background__v68` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.264 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 0.863 | 0.618 | 0.203 | 0.434 | bend/corner induced residual |
| `no_via_background__v69` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.245 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 0.713 | 0.613 | 0.230 | 0.241 | bend/corner induced residual |
| `no_via_background__v70` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.236 | 0.023 | 1 | 1 | 0.000 | 5.000 | n/a | 0.930 | 0.639 | 0.143 | 0.319 | detector threshold sensitivity |
| `no_via_background__v71` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.237 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.202 | 0.698 | 0.218 | 0.421 | bend/corner induced residual |
| `no_via_background__v72` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.349 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.109 | 0.823 | 0.262 | 0.402 | bend/corner induced residual |
| `no_via_background__v73` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.374 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 0.942 | 0.759 | 0.205 | 0.584 | bend/corner induced residual |
| `no_via_background__v74` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.391 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.041 | 0.857 | 0.248 | 0.516 | bend/corner induced residual |
| `no_via_background__v75` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.595 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 0.944 | 0.818 | 0.091 | 0.097 | bend/corner induced residual |
| `no_via_background__v76` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.225 | 0.017 | 1 | 1 | 1.000 | 1.000 | n/a | 1.269 | 0.966 | 0.263 | 0.836 | bend/corner induced residual |
| `no_via_background__v77` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.304 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 0.953 | 0.731 | 0.193 | 0.472 | bend/corner induced residual |
| `no_via_background__v78` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.129 | 0.014 | 0 | 0 | 0.000 | 0.000 | n/a | 0.922 | 0.832 | 0.166 | 0.405 | no false positive |
| `no_via_background__v79` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.173 | 0.015 | 0 | 0 | 1.000 | 1.000 | n/a | 0.765 | 0.784 | 0.170 | 0.412 | no false positive |
| `no_via_background__v80` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.259 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.045 | 0.998 | 0.232 | 0.164 | bend/corner induced residual |
| `no_via_background__v81` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.302 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.958 | 0.939 | 0.197 | 0.248 | bend/corner induced residual |
| `no_via_background__v82` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.369 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 0.725 | 0.963 | 0.146 | 0.165 | bend/corner induced residual |
| `no_via_background__v83` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.253 | 0.018 | 1 | 1 | 0.000 | 0.000 | n/a | 0.597 | 0.880 | 0.146 | 0.156 | bend/corner induced residual |
| `no_via_background__v84` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.193 | 0.024 | 0 | 0 | 0.000 | 5.000 | n/a | 0.777 | 0.711 | 0.143 | 0.347 | no false positive |
| `no_via_background__v85` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.200 | 0.023 | 1 | 1 | 0.000 | 5.000 | n/a | 1.039 | 0.677 | 0.203 | 0.367 | detector threshold sensitivity |
| `no_via_background__v86` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.283 | 0.026 | 2 | 2 | 1.000 | 5.099 | n/a | 0.791 | 0.570 | 0.248 | 0.638 | operator mismatch |
| `no_via_background__v87` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.305 | 0.032 | 3 | 3 | 0.000 | 5.000 | n/a | 0.669 | 0.537 | 0.159 | 0.248 | operator mismatch |
| `no_via_background__v88` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.221 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 0.685 | 0.730 | 0.260 | 0.725 | bend/corner induced residual |
| `no_via_background__v89` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.204 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.676 | 0.693 | 0.183 | 0.163 | bend/corner induced residual |
| `no_via_background__v90` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.145 | 0.019 | 0 | 0 | 0.000 | 0.000 | n/a | 0.638 | 0.560 | 0.143 | 0.160 | no false positive |
| `no_via_background__v91` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.422 | 0.028 | 1 | 1 | 0.000 | 3.000 | n/a | 0.644 | 0.545 | 0.248 | 0.482 | operator mismatch |
| `no_via_background__v92` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.210 | 0.015 | 1 | 1 | 0.000 | 2.000 | n/a | 0.768 | 0.628 | 0.222 | 0.167 | bend/corner induced residual |
| `no_via_background__v93` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.176 | 0.019 | 0 | 0 | 0.000 | 5.000 | n/a | 0.544 | 0.679 | 0.195 | 0.145 | no false positive |
| `no_via_background__v94` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.205 | 0.017 | 1 | 1 | 0.000 | 2.000 | n/a | 0.607 | 0.633 | 0.210 | 0.499 | bend/corner induced residual |
| `no_via_background__v95` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.146 | 0.017 | 0 | 0 | 0.000 | 2.000 | n/a | 0.584 | 0.574 | 0.182 | 0.232 | no false positive |
| `no_via_background__v96` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.247 | 0.018 | 1 | 1 | 0.000 | 0.000 | n/a | 1.014 | 0.962 | 0.155 | 0.165 | bend/corner induced residual |
| `bend_artifact_trace` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.258 | 0.025 | 2 | 2 | 0.000 | 0.000 | n/a | 1.028 | 0.816 | 0.217 | 0.259 | bend/corner induced residual |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.299 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.018 | 0.768 | 0.176 | 0.366 | bend/corner induced residual |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.118 | 0.014 | 0 | 0 | 0.000 | 0.000 | n/a | 1.424 | 0.726 | 0.190 | 0.258 | no false positive |
| `bend_artifact_trace__v03` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.209 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.164 | 0.823 | 0.146 | 0.139 | bend/corner induced residual |
| `bend_artifact_trace__v04` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.348 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 1.291 | 0.632 | 0.196 | 0.619 | bend/corner induced residual |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.286 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.202 | 0.781 | 0.229 | 0.538 | bend/corner induced residual |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.332 | 0.025 | 2 | 2 | 0.000 | 0.000 | n/a | 1.099 | 0.572 | 0.134 | 0.712 | bend/corner induced residual |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.282 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 0.830 | 0.511 | 0.207 | 0.710 | bend/corner induced residual |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.340 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.850 | 0.710 | 0.173 | 0.235 | bend/corner induced residual |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.262 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.948 | 0.654 | 0.236 | 0.267 | bend/corner induced residual |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.360 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.907 | 0.629 | 0.187 | 0.468 | bend/corner induced residual |
| `bend_artifact_trace__v11` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.282 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 0.930 | 0.630 | 0.150 | 0.263 | bend/corner induced residual |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.194 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 0.818 | 0.889 | 0.223 | 0.221 | no false positive |
| `bend_artifact_trace__v13` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.157 | 0.023 | 0 | 0 | 0.000 | 1.000 | n/a | 0.992 | 0.823 | 0.238 | 0.637 | no false positive |
| `bend_artifact_trace__v14` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.154 | 0.017 | 0 | 0 | 1.000 | 4.000 | n/a | 0.831 | 0.551 | 0.162 | 0.373 | no false positive |
| `bend_artifact_trace__v15` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.141 | 0.019 | 0 | 0 | 0.000 | 3.000 | n/a | 0.907 | 0.626 | 0.164 | 0.337 | no false positive |
| `bend_artifact_trace__v16` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.303 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 0.938 | 0.640 | 0.214 | 0.553 | bend/corner induced residual |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.234 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.115 | 0.685 | 0.219 | 0.580 | bend/corner induced residual |
| `bend_artifact_trace__v18` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.327 | 0.036 | 3 | 3 | 0.000 | 0.000 | n/a | 0.734 | 0.624 | 0.167 | 0.322 | bend/corner induced residual |
| `bend_artifact_trace__v19` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.376 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 0.962 | 0.625 | 0.204 | 0.468 | bend/corner induced residual |
| `bend_artifact_trace__v20` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.242 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.307 | 0.782 | 0.245 | 0.550 | bend/corner induced residual |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.274 | 0.030 | 2 | 2 | 0.000 | 2.000 | n/a | 1.383 | 0.643 | 0.216 | 0.521 | bend/corner induced residual |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.180 | 0.023 | 0 | 0 | 0.000 | 0.000 | n/a | 0.931 | 0.539 | 0.233 | 0.547 | no false positive |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.235 | 0.026 | 1 | 1 | 0.000 | 2.000 | n/a | 1.228 | 0.666 | 0.218 | 0.510 | bend/corner induced residual |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.381 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.119 | 0.821 | 0.214 | 0.544 | bend/corner induced residual |
| `bend_artifact_trace__v25` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.166 | 0.015 | 0 | 0 | 0.000 | 0.000 | n/a | 1.193 | 0.624 | 0.233 | 0.504 | no false positive |
| `bend_artifact_trace__v26` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.311 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.046 | 0.664 | 0.162 | 0.488 | bend/corner induced residual |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.270 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 0.818 | 0.677 | 0.177 | 0.200 | bend/corner induced residual |
| `bend_artifact_trace__v28` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.225 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 1.089 | 0.838 | 0.222 | 0.825 | bend/corner induced residual |
| `bend_artifact_trace__v29` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.279 | 0.027 | 3 | 3 | 0.000 | 0.000 | n/a | 1.047 | 0.777 | 0.202 | 0.720 | bend/corner induced residual |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.346 | 0.034 | 3 | 3 | 0.000 | 0.000 | n/a | 1.474 | 0.766 | 0.154 | 0.726 | bend/corner induced residual |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.307 | 0.030 | 3 | 3 | 0.000 | 0.000 | n/a | 1.227 | 0.678 | 0.150 | 0.682 | bend/corner induced residual |
| `bend_artifact_trace__v32` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.267 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.337 | 1.013 | 0.229 | 0.144 | bend/corner induced residual |
| `bend_artifact_trace__v33` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.189 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.035 | 0.900 | 0.158 | 0.143 | no false positive |
| `bend_artifact_trace__v34` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.288 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.062 | 0.896 | 0.247 | 0.392 | bend/corner induced residual |
| `bend_artifact_trace__v35` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.258 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 1.148 | 0.723 | 0.237 | 0.384 | bend/corner induced residual |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.325 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 1.303 | 0.679 | 0.214 | 0.576 | bend/corner induced residual |
| `bend_artifact_trace__v37` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.186 | 0.019 | 0 | 0 | 0.000 | 3.000 | n/a | 1.228 | 0.528 | 0.240 | 0.596 | no false positive |
| `bend_artifact_trace__v38` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.226 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.414 | 0.575 | 0.219 | 0.710 | bend/corner induced residual |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.335 | 0.030 | 1 | 1 | 0.000 | 3.000 | n/a | 0.973 | 0.506 | 0.113 | 0.428 | model hallucination |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.380 | 0.031 | 2 | 2 | 0.000 | 0.000 | n/a | 1.125 | 0.731 | 0.222 | 0.447 | bend/corner induced residual |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.303 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.369 | 0.663 | 0.234 | 0.483 | bend/corner induced residual |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.222 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.984 | 0.728 | 0.210 | 0.254 | bend/corner induced residual |
| `bend_artifact_trace__v43` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.178 | 0.018 | 0 | 0 | 1.000 | 4.000 | n/a | 0.973 | 0.748 | 0.202 | 0.259 | no false positive |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.356 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.835 | 0.622 | 0.213 | 0.497 | bend/corner induced residual |
| `bend_artifact_trace__v45` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.123 | 0.017 | 0 | 0 | 0.000 | 2.000 | n/a | 0.849 | 0.659 | 0.178 | 0.416 | no false positive |
| `bend_artifact_trace__v46` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.187 | 0.023 | 0 | 0 | 1.000 | 2.236 | n/a | 0.841 | 0.569 | 0.248 | 0.538 | no false positive |
| `bend_artifact_trace__v47` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.170 | 0.024 | 0 | 0 | 0.000 | 0.000 | n/a | 0.952 | 0.511 | 0.189 | 0.539 | no false positive |
| `bend_artifact_trace__v48` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.216 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.067 | 0.962 | 0.159 | 0.143 | bend/corner induced residual |
| `bend_artifact_trace__v49` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.212 | 0.022 | 2 | 2 | 0.000 | 0.000 | n/a | 0.972 | 0.863 | 0.234 | 0.157 | bend/corner induced residual |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.264 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.017 | 0.714 | 0.188 | 0.362 | bend/corner induced residual |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.230 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.940 | 0.756 | 0.152 | 0.294 | bend/corner induced residual |
| `bend_artifact_trace__v52` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.489 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 1.228 | 0.960 | 0.252 | 0.563 | bend/corner induced residual |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.489 | 0.035 | 2 | 2 | 0.000 | 0.000 | n/a | 1.162 | 0.837 | 0.225 | 0.605 | bend/corner induced residual |
| `bend_artifact_trace__v54` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.343 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 1.254 | 0.680 | 0.248 | 0.657 | bend/corner induced residual |
| `bend_artifact_trace__v55` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.416 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.925 | 0.607 | 0.256 | 0.427 | bend/corner induced residual |
| `bend_artifact_trace__v56` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.343 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 1.010 | 0.736 | 0.213 | 0.364 | bend/corner induced residual |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.407 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.852 | 0.640 | 0.186 | 0.272 | bend/corner induced residual |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.276 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.946 | 0.733 | 0.253 | 0.211 | bend/corner induced residual |
| `bend_artifact_trace__v59` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.180 | 0.019 | 0 | 0 | 0.000 | 0.000 | n/a | 0.853 | 0.617 | 0.180 | 0.556 | no false positive |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.237 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.901 | 0.723 | 0.194 | 0.381 | bend/corner induced residual |
| `bend_artifact_trace__v61` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.200 | 0.024 | 1 | 1 | 0.000 | 2.000 | n/a | 0.851 | 0.626 | 0.234 | 0.288 | bend/corner induced residual |
| `bend_artifact_trace__v62` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.143 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 0.979 | 0.506 | 0.233 | 0.405 | no false positive |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.135 | 0.019 | 0 | 0 | 1.000 | 1.000 | n/a | 0.935 | 0.603 | 0.222 | 0.386 | no false positive |
| `bend_artifact_trace__v64` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.191 | 0.020 | 0 | 0 | 0.000 | 0.000 | n/a | 1.210 | 0.678 | 0.162 | 0.581 | no false positive |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.232 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.165 | 0.677 | 0.211 | 0.513 | bend/corner induced residual |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.181 | 0.022 | 0 | 0 | 0.000 | 2.000 | n/a | 1.032 | 0.607 | 0.247 | 0.542 | no false positive |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.376 | 0.034 | 2 | 2 | 0.000 | 0.000 | n/a | 0.961 | 0.619 | 0.192 | 0.573 | bend/corner induced residual |
| `bend_artifact_trace__v68` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.137 | 0.019 | 0 | 0 | 0.000 | 0.000 | n/a | 1.420 | 0.675 | 0.173 | 0.753 | no false positive |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.238 | 0.027 | 1 | 1 | 0.000 | 3.000 | n/a | 1.265 | 0.574 | 0.162 | 0.485 | detector threshold sensitivity |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.236 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.472 | 0.772 | 0.210 | 0.500 | bend/corner induced residual |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.181 | 0.021 | 0 | 0 | 0.000 | 3.000 | n/a | 1.458 | 0.696 | 0.251 | 0.655 | no false positive |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.385 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.876 | 0.724 | 0.218 | 0.259 | bend/corner induced residual |
| `bend_artifact_trace__v73` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.291 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 0.750 | 0.655 | 0.185 | 0.546 | bend/corner induced residual |
| `bend_artifact_trace__v74` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.268 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.158 | 0.719 | 0.247 | 0.401 | bend/corner induced residual |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.407 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 0.918 | 0.713 | 0.211 | 0.299 | bend/corner induced residual |
| `bend_artifact_trace__v76` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.366 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.258 | 0.725 | 0.257 | 0.674 | bend/corner induced residual |
| `bend_artifact_trace__v77` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.187 | 0.022 | 0 | 0 | 0.000 | 0.000 | n/a | 1.383 | 0.726 | 0.194 | 0.783 | no false positive |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.339 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.979 | 0.600 | 0.183 | 0.710 | bend/corner induced residual |
| `bend_artifact_trace__v79` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.299 | 0.031 | 3 | 3 | 0.000 | 0.000 | n/a | 1.047 | 0.605 | 0.204 | 0.751 | bend/corner induced residual |
| `bend_artifact_trace__v80` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.320 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.058 | 0.984 | 0.252 | 0.260 | bend/corner induced residual |
| `bend_artifact_trace__v81` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.302 | 0.025 | 2 | 2 | 0.000 | 0.000 | n/a | 1.071 | 0.770 | 0.143 | 0.330 | bend/corner induced residual |
| `bend_artifact_trace__v82` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.248 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.132 | 0.882 | 0.206 | 0.429 | bend/corner induced residual |
| `bend_artifact_trace__v83` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.233 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.279 | 0.749 | 0.191 | 0.245 | bend/corner induced residual |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.277 | 0.028 | 1 | 1 | 0.000 | 3.000 | n/a | 1.422 | 0.791 | 0.136 | 0.424 | detector threshold sensitivity |
| `bend_artifact_trace__v85` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.154 | 0.023 | 0 | 0 | 0.000 | 0.000 | n/a | 1.571 | 0.773 | 0.178 | 0.542 | no false positive |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.308 | 0.025 | 1 | 1 | 0.000 | 2.000 | n/a | 1.400 | 0.657 | 0.247 | 0.635 | bend/corner induced residual |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.183 | 0.025 | 0 | 0 | 0.000 | 0.000 | n/a | 1.046 | 0.533 | 0.159 | 0.594 | no false positive |
| `bend_artifact_trace__v88` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.180 | 0.023 | 0 | 0 | 0.000 | 0.000 | n/a | 0.876 | 0.634 | 0.256 | 0.742 | no false positive |
| `bend_artifact_trace__v89` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.177 | 0.020 | 0 | 0 | 0.000 | 0.000 | n/a | 1.327 | 0.698 | 0.236 | 0.477 | no false positive |
| `bend_artifact_trace__v90` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.138 | 0.021 | 0 | 0 | 0.000 | 3.000 | n/a | 0.806 | 0.659 | 0.233 | 0.488 | no false positive |
| `bend_artifact_trace__v91` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.189 | 0.023 | 0 | 0 | 0.000 | 0.000 | n/a | 0.975 | 0.726 | 0.246 | 0.365 | no false positive |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.194 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 0.818 | 0.889 | 0.223 | 0.221 | no false positive |
| `bend_artifact_trace__v93` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.152 | 0.023 | 0 | 0 | 0.000 | 1.000 | n/a | 0.944 | 0.816 | 0.223 | 0.603 | no false positive |
| `bend_artifact_trace__v94` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.125 | 0.017 | 0 | 0 | 1.000 | 3.000 | n/a | 0.849 | 0.555 | 0.182 | 0.299 | no false positive |
| `bend_artifact_trace__v95` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.141 | 0.019 | 0 | 0 | 0.000 | 3.000 | n/a | 0.907 | 0.626 | 0.164 | 0.337 | no false positive |
| `bend_artifact_trace__v96` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.294 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 1.187 | 0.895 | 0.162 | 0.211 | bend/corner induced residual |
| `bend_artifact_trace__v97` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.319 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.107 | 0.926 | 0.217 | 0.190 | bend/corner induced residual |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.233 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.176 | 0.959 | 0.208 | 0.268 | bend/corner induced residual |
| `bend_artifact_trace__v99` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.191 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 1.097 | 0.897 | 0.119 | 0.121 | no false positive |

Interpretation: these rows classify PyPEEC no-via false positives after inference. They do not tune a PyPEEC-specific detector threshold.
