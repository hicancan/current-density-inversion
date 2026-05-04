# Real PyPEEC No-Via False-Positive Diagnostics

- no-via cases: `200`
- presence threshold: `2.666667`
- boundary: Diagnostic only. No PyPEEC no-via threshold is selected from these rows.

## Summary

| model | cases | FP rate | mean s1 peak | mean topology MSE | mean physical B PyPEEC | mean leakage | dominant failure modes |
|---|---:|---:|---:|---:|---:|---:|---|
| `unet_no_topology` | 200 | 0.930 | 0.447 | 1.680 | 0.875 | 0.350 | bend/corner induced residual: 155, detector threshold sensitivity: 16, model hallucination: 2, no false positive: 14, operator mismatch: 13 |
| `unet_topology_soft_loss` | 200 | 0.955 | 0.420 | 0.962 | 0.700 | 0.428 | bend/corner induced residual: 146, detector threshold sensitivity: 6, model hallucination: 7, no false positive: 9, operator mismatch: 32 |
| `unet_topology_two_stage_refined` | 200 | 0.720 | 0.279 | 0.907 | 0.696 | 0.428 | bend/corner induced residual: 107, detector threshold sensitivity: 6, model hallucination: 5, no false positive: 56, operator mismatch: 26 |

## Per-Case Rows

| case | type | model | FP | s1 peak | s1 rms | via px | comp | d trace | d bend | d return | topology MSE | B PyPEEC | gap | leakage | failure mode |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `straight_trace` | `canonical` | `unet_no_topology` | no | 0.040 | 0.004 | 0 | 0 | 2.000 | n/a | n/a | 0.814 | 1.136 | 0.004 | 0.008 | no false positive |
| `finite_width_trace` | `canonical` | `unet_no_topology` | no | 0.046 | 0.006 | 0 | 0 | 2.000 | n/a | n/a | 0.797 | 1.057 | 0.194 | 0.416 | no false positive |
| `l_shape_trace` | `canonical` | `unet_no_topology` | yes | 0.490 | 0.041 | 3 | 2 | 0.000 | 10.000 | n/a | 0.852 | 0.562 | 0.004 | 0.113 | model hallucination |
| `no_via_background` | `no_via_background` | `unet_no_topology` | yes | 0.332 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.623 | 0.782 | 0.265 | 0.706 | bend/corner induced residual |
| `no_via_background__v01` | `no_via_background` | `unet_no_topology` | yes | 0.447 | 0.031 | 2 | 2 | 0.000 | 0.000 | n/a | 1.503 | 1.035 | 0.197 | 0.263 | bend/corner induced residual |
| `no_via_background__v02` | `no_via_background` | `unet_no_topology` | yes | 0.510 | 0.034 | 2 | 2 | 0.000 | 0.000 | n/a | 1.316 | 1.006 | 0.146 | 0.315 | bend/corner induced residual |
| `no_via_background__v03` | `no_via_background` | `unet_no_topology` | yes | 0.439 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.479 | 1.161 | 0.146 | 0.267 | bend/corner induced residual |
| `no_via_background__v04` | `no_via_background` | `unet_no_topology` | yes | 0.227 | 0.024 | 1 | 1 | 1.000 | 1.000 | n/a | 1.677 | 1.095 | 0.231 | 0.361 | bend/corner induced residual |
| `no_via_background__v05` | `no_via_background` | `unet_no_topology` | yes | 0.216 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.619 | 1.037 | 0.215 | 0.222 | bend/corner induced residual |
| `no_via_background__v06` | `no_via_background` | `unet_no_topology` | yes | 0.358 | 0.029 | 2 | 2 | 1.000 | 1.000 | n/a | 1.342 | 0.896 | 0.214 | 0.393 | bend/corner induced residual |
| `no_via_background__v07` | `no_via_background` | `unet_no_topology` | yes | 0.241 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.289 | 1.005 | 0.171 | 0.252 | bend/corner induced residual |
| `no_via_background__v08` | `no_via_background` | `unet_no_topology` | yes | 0.653 | 0.048 | 3 | 2 | 0.000 | 0.000 | n/a | 2.762 | 0.986 | 0.203 | 0.274 | bend/corner induced residual |
| `no_via_background__v09` | `no_via_background` | `unet_no_topology` | yes | 1.166 | 0.070 | 1 | 1 | 0.000 | 0.000 | n/a | 2.815 | 0.972 | 0.183 | 0.173 | bend/corner induced residual |
| `no_via_background__v10` | `no_via_background` | `unet_no_topology` | yes | 0.928 | 0.056 | 1 | 1 | 0.000 | 0.000 | n/a | 1.963 | 0.994 | 0.136 | 0.364 | bend/corner induced residual |
| `no_via_background__v11` | `no_via_background` | `unet_no_topology` | yes | 0.528 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 2.487 | 1.028 | 0.176 | 0.327 | bend/corner induced residual |
| `no_via_background__v12` | `no_via_background` | `unet_no_topology` | yes | 0.329 | 0.026 | 1 | 1 | 0.000 | 5.000 | n/a | 1.249 | 0.996 | 0.222 | 0.115 | detector threshold sensitivity |
| `no_via_background__v13` | `no_via_background` | `unet_no_topology` | yes | 0.350 | 0.034 | 2 | 2 | 0.000 | 5.000 | n/a | 1.147 | 0.804 | 0.195 | 0.080 | operator mismatch |
| `no_via_background__v14` | `no_via_background` | `unet_no_topology` | yes | 0.297 | 0.030 | 2 | 2 | 1.000 | 1.000 | n/a | 1.314 | 0.994 | 0.210 | 0.631 | bend/corner induced residual |
| `no_via_background__v15` | `no_via_background` | `unet_no_topology` | no | 0.175 | 0.021 | 0 | 0 | 0.000 | 2.000 | n/a | 0.781 | 0.723 | 0.116 | 0.117 | no false positive |
| `no_via_background__v16` | `no_via_background` | `unet_no_topology` | yes | 0.266 | 0.028 | 3 | 3 | 0.000 | 5.000 | n/a | 1.162 | 0.508 | 0.165 | 0.360 | operator mismatch |
| `no_via_background__v17` | `no_via_background` | `unet_no_topology` | yes | 0.273 | 0.027 | 1 | 1 | 0.000 | 5.000 | n/a | 1.313 | 0.536 | 0.176 | 0.407 | operator mismatch |
| `no_via_background__v18` | `no_via_background` | `unet_no_topology` | no | 0.167 | 0.023 | 0 | 0 | 0.000 | 2.000 | n/a | 1.012 | 0.540 | 0.194 | 0.398 | no false positive |
| `no_via_background__v19` | `no_via_background` | `unet_no_topology` | no | 0.197 | 0.022 | 0 | 0 | 0.000 | 6.000 | n/a | 0.970 | 0.528 | 0.170 | 0.299 | no false positive |
| `no_via_background__v20` | `no_via_background` | `unet_no_topology` | yes | 0.278 | 0.031 | 2 | 2 | 0.000 | 4.000 | n/a | 1.477 | 0.752 | 0.253 | 0.299 | operator mismatch |
| `no_via_background__v21` | `no_via_background` | `unet_no_topology` | yes | 0.390 | 0.041 | 4 | 3 | 0.000 | 0.000 | n/a | 1.498 | 0.670 | 0.201 | 0.279 | bend/corner induced residual |
| `no_via_background__v22` | `no_via_background` | `unet_no_topology` | yes | 0.376 | 0.041 | 4 | 3 | 0.000 | 0.000 | n/a | 1.236 | 0.645 | 0.143 | 0.246 | bend/corner induced residual |
| `no_via_background__v23` | `no_via_background` | `unet_no_topology` | yes | 0.373 | 0.039 | 3 | 2 | 0.000 | 0.000 | n/a | 1.312 | 0.604 | 0.174 | 0.480 | bend/corner induced residual |
| `no_via_background__v24` | `no_via_background` | `unet_no_topology` | yes | 1.192 | 0.071 | 1 | 1 | 0.000 | 0.000 | n/a | 2.953 | 1.044 | 0.165 | 0.191 | bend/corner induced residual |
| `no_via_background__v25` | `no_via_background` | `unet_no_topology` | yes | 1.131 | 0.068 | 1 | 1 | 0.000 | 0.000 | n/a | 2.495 | 0.944 | 0.194 | 0.195 | bend/corner induced residual |
| `no_via_background__v26` | `no_via_background` | `unet_no_topology` | yes | 1.108 | 0.066 | 1 | 1 | 0.000 | 0.000 | n/a | 2.213 | 0.992 | 0.210 | 0.633 | bend/corner induced residual |
| `no_via_background__v27` | `no_via_background` | `unet_no_topology` | yes | 1.129 | 0.067 | 1 | 1 | 0.000 | 0.000 | n/a | 2.254 | 0.991 | 0.171 | 0.307 | bend/corner induced residual |
| `no_via_background__v28` | `no_via_background` | `unet_no_topology` | yes | 0.208 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.826 | 1.046 | 0.163 | 0.464 | bend/corner induced residual |
| `no_via_background__v29` | `no_via_background` | `unet_no_topology` | yes | 0.319 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.550 | 1.006 | 0.231 | 0.372 | bend/corner induced residual |
| `no_via_background__v30` | `no_via_background` | `unet_no_topology` | yes | 0.209 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.853 | 0.932 | 0.146 | 0.487 | bend/corner induced residual |
| `no_via_background__v31` | `no_via_background` | `unet_no_topology` | yes | 0.231 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 2.035 | 0.975 | 0.176 | 0.624 | bend/corner induced residual |
| `no_via_background__v32` | `no_via_background` | `unet_no_topology` | yes | 0.603 | 0.039 | 1 | 1 | 0.000 | 0.000 | n/a | 1.684 | 1.182 | 0.264 | 0.313 | bend/corner induced residual |
| `no_via_background__v33` | `no_via_background` | `unet_no_topology` | yes | 0.394 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.507 | 1.201 | 0.207 | 0.436 | bend/corner induced residual |
| `no_via_background__v34` | `no_via_background` | `unet_no_topology` | yes | 0.415 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 1.315 | 1.018 | 0.248 | 0.517 | bend/corner induced residual |
| `no_via_background__v35` | `no_via_background` | `unet_no_topology` | yes | 0.503 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.851 | 0.777 | 0.209 | 0.710 | bend/corner induced residual |
| `no_via_background__v36` | `no_via_background` | `unet_no_topology` | yes | 0.404 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.537 | 0.765 | 0.165 | 0.320 | bend/corner induced residual |
| `no_via_background__v37` | `no_via_background` | `unet_no_topology` | yes | 0.431 | 0.034 | 2 | 2 | 0.000 | 5.000 | n/a | 1.317 | 0.614 | 0.160 | 0.351 | operator mismatch |
| `no_via_background__v38` | `no_via_background` | `unet_no_topology` | yes | 0.362 | 0.037 | 3 | 2 | 0.000 | 0.000 | n/a | 1.421 | 0.652 | 0.185 | 0.418 | bend/corner induced residual |
| `no_via_background__v39` | `no_via_background` | `unet_no_topology` | yes | 0.429 | 0.048 | 4 | 3 | 0.000 | 0.000 | n/a | 1.421 | 0.607 | 0.177 | 0.239 | bend/corner induced residual |
| `no_via_background__v40` | `no_via_background` | `unet_no_topology` | yes | 0.417 | 0.032 | 2 | 2 | 0.000 | 5.000 | n/a | 1.276 | 0.883 | 0.223 | 0.259 | detector threshold sensitivity |
| `no_via_background__v41` | `no_via_background` | `unet_no_topology` | no | 0.199 | 0.026 | 0 | 0 | 0.000 | 2.000 | n/a | 0.826 | 0.678 | 0.202 | 0.107 | no false positive |
| `no_via_background__v42` | `no_via_background` | `unet_no_topology` | yes | 0.288 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 0.991 | 0.877 | 0.143 | 0.096 | bend/corner induced residual |
| `no_via_background__v43` | `no_via_background` | `unet_no_topology` | yes | 0.266 | 0.027 | 1 | 1 | 0.000 | 5.000 | n/a | 1.010 | 0.928 | 0.179 | 0.130 | detector threshold sensitivity |
| `no_via_background__v44` | `no_via_background` | `unet_no_topology` | yes | 0.418 | 0.035 | 2 | 2 | 0.000 | 0.000 | n/a | 1.138 | 0.930 | 0.211 | 0.383 | bend/corner induced residual |
| `no_via_background__v45` | `no_via_background` | `unet_no_topology` | yes | 0.201 | 0.022 | 1 | 1 | 0.000 | 5.000 | n/a | 1.018 | 0.815 | 0.203 | 0.161 | detector threshold sensitivity |
| `no_via_background__v46` | `no_via_background` | `unet_no_topology` | yes | 0.301 | 0.032 | 2 | 2 | 1.000 | 6.083 | n/a | 1.054 | 0.769 | 0.263 | 0.442 | operator mismatch |
| `no_via_background__v47` | `no_via_background` | `unet_no_topology` | yes | 0.317 | 0.032 | 2 | 2 | 0.000 | 6.000 | n/a | 1.157 | 0.938 | 0.151 | 0.099 | detector threshold sensitivity |
| `no_via_background__v48` | `no_via_background` | `unet_no_topology` | no | 0.154 | 0.021 | 0 | 0 | 1.414 | 1.414 | n/a | 1.130 | 1.139 | 0.135 | 0.256 | no false positive |
| `no_via_background__v49` | `no_via_background` | `unet_no_topology` | yes | 0.403 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 1.257 | 1.009 | 0.197 | 0.295 | bend/corner induced residual |
| `no_via_background__v50` | `no_via_background` | `unet_no_topology` | yes | 0.573 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 1.678 | 1.035 | 0.135 | 0.210 | bend/corner induced residual |
| `no_via_background__v51` | `no_via_background` | `unet_no_topology` | yes | 0.423 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.482 | 1.062 | 0.109 | 0.203 | bend/corner induced residual |
| `no_via_background__v52` | `no_via_background` | `unet_no_topology` | yes | 0.455 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 2.010 | 1.120 | 0.234 | 0.468 | bend/corner induced residual |
| `no_via_background__v53` | `no_via_background` | `unet_no_topology` | yes | 0.336 | 0.031 | 2 | 2 | 0.000 | 0.000 | n/a | 1.247 | 0.850 | 0.170 | 0.368 | bend/corner induced residual |
| `no_via_background__v54` | `no_via_background` | `unet_no_topology` | yes | 0.205 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 2.113 | 1.160 | 0.263 | 0.758 | bend/corner induced residual |
| `no_via_background__v55` | `no_via_background` | `unet_no_topology` | yes | 0.209 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.226 | 0.851 | 0.239 | 0.441 | bend/corner induced residual |
| `no_via_background__v56` | `no_via_background` | `unet_no_topology` | yes | 0.921 | 0.056 | 1 | 1 | 0.000 | 0.000 | n/a | 2.107 | 1.019 | 0.211 | 0.653 | bend/corner induced residual |
| `no_via_background__v57` | `no_via_background` | `unet_no_topology` | yes | 1.140 | 0.068 | 1 | 1 | 0.000 | 0.000 | n/a | 2.481 | 1.052 | 0.211 | 0.275 | bend/corner induced residual |
| `no_via_background__v58` | `no_via_background` | `unet_no_topology` | yes | 1.127 | 0.068 | 1 | 1 | 0.000 | 0.000 | n/a | 2.103 | 0.841 | 0.185 | 0.415 | bend/corner induced residual |
| `no_via_background__v59` | `no_via_background` | `unet_no_topology` | yes | 1.157 | 0.070 | 1 | 1 | 0.000 | 0.000 | n/a | 2.530 | 0.851 | 0.176 | 0.407 | bend/corner induced residual |
| `no_via_background__v60` | `no_via_background` | `unet_no_topology` | yes | 0.314 | 0.031 | 2 | 2 | 0.000 | 5.000 | n/a | 1.179 | 0.829 | 0.221 | 0.068 | operator mismatch |
| `no_via_background__v61` | `no_via_background` | `unet_no_topology` | yes | 0.301 | 0.032 | 2 | 2 | 0.000 | 6.000 | n/a | 1.054 | 0.769 | 0.202 | 0.119 | operator mismatch |
| `no_via_background__v62` | `no_via_background` | `unet_no_topology` | yes | 0.440 | 0.036 | 2 | 2 | 0.000 | 5.000 | n/a | 1.335 | 1.034 | 0.143 | 0.097 | detector threshold sensitivity |
| `no_via_background__v63` | `no_via_background` | `unet_no_topology` | yes | 0.273 | 0.024 | 1 | 1 | 0.000 | 5.000 | n/a | 1.110 | 0.864 | 0.177 | 0.183 | detector threshold sensitivity |
| `no_via_background__v64` | `no_via_background` | `unet_no_topology` | yes | 0.364 | 0.034 | 4 | 4 | 0.000 | 5.000 | n/a | 1.354 | 0.508 | 0.155 | 0.404 | operator mismatch |
| `no_via_background__v65` | `no_via_background` | `unet_no_topology` | yes | 0.360 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.606 | 0.685 | 0.192 | 0.466 | bend/corner induced residual |
| `no_via_background__v66` | `no_via_background` | `unet_no_topology` | yes | 0.242 | 0.029 | 4 | 4 | 0.000 | 0.000 | n/a | 1.249 | 0.498 | 0.248 | 0.729 | bend/corner induced residual |
| `no_via_background__v67` | `no_via_background` | `unet_no_topology` | yes | 0.308 | 0.036 | 3 | 3 | 0.000 | 3.000 | n/a | 1.355 | 0.518 | 0.153 | 0.402 | operator mismatch |
| `no_via_background__v68` | `no_via_background` | `unet_no_topology` | yes | 0.684 | 0.047 | 3 | 3 | 0.000 | 0.000 | n/a | 1.892 | 0.721 | 0.203 | 0.403 | bend/corner induced residual |
| `no_via_background__v69` | `no_via_background` | `unet_no_topology` | yes | 0.422 | 0.043 | 4 | 3 | 0.000 | 0.000 | n/a | 1.269 | 0.655 | 0.230 | 0.260 | bend/corner induced residual |
| `no_via_background__v70` | `no_via_background` | `unet_no_topology` | yes | 0.281 | 0.033 | 4 | 3 | 0.000 | 0.000 | n/a | 1.395 | 0.663 | 0.143 | 0.258 | bend/corner induced residual |
| `no_via_background__v71` | `no_via_background` | `unet_no_topology` | yes | 0.310 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 1.452 | 0.713 | 0.218 | 0.527 | bend/corner induced residual |
| `no_via_background__v72` | `no_via_background` | `unet_no_topology` | yes | 1.181 | 0.071 | 1 | 1 | 0.000 | 0.000 | n/a | 2.833 | 1.006 | 0.262 | 0.193 | bend/corner induced residual |
| `no_via_background__v73` | `no_via_background` | `unet_no_topology` | yes | 1.063 | 0.064 | 1 | 1 | 0.000 | 0.000 | n/a | 2.097 | 0.853 | 0.205 | 0.471 | bend/corner induced residual |
| `no_via_background__v74` | `no_via_background` | `unet_no_topology` | yes | 1.166 | 0.070 | 1 | 1 | 0.000 | 0.000 | n/a | 2.815 | 0.972 | 0.248 | 0.371 | bend/corner induced residual |
| `no_via_background__v75` | `no_via_background` | `unet_no_topology` | yes | 0.879 | 0.053 | 1 | 1 | 0.000 | 0.000 | n/a | 2.128 | 0.986 | 0.091 | 0.111 | bend/corner induced residual |
| `no_via_background__v76` | `no_via_background` | `unet_no_topology` | yes | 0.258 | 0.022 | 1 | 1 | 1.000 | 1.000 | n/a | 1.616 | 0.979 | 0.263 | 0.811 | bend/corner induced residual |
| `no_via_background__v77` | `no_via_background` | `unet_no_topology` | yes | 0.437 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.536 | 0.864 | 0.193 | 0.439 | bend/corner induced residual |
| `no_via_background__v78` | `no_via_background` | `unet_no_topology` | yes | 0.261 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.561 | 0.880 | 0.166 | 0.469 | bend/corner induced residual |
| `no_via_background__v79` | `no_via_background` | `unet_no_topology` | yes | 0.306 | 0.025 | 1 | 1 | 1.000 | 1.000 | n/a | 1.233 | 0.854 | 0.170 | 0.442 | bend/corner induced residual |
| `no_via_background__v80` | `no_via_background` | `unet_no_topology` | yes | 0.479 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.586 | 1.156 | 0.232 | 0.199 | bend/corner induced residual |
| `no_via_background__v81` | `no_via_background` | `unet_no_topology` | yes | 0.447 | 0.031 | 2 | 2 | 0.000 | 0.000 | n/a | 1.503 | 1.035 | 0.197 | 0.263 | bend/corner induced residual |
| `no_via_background__v82` | `no_via_background` | `unet_no_topology` | yes | 0.510 | 0.034 | 2 | 2 | 0.000 | 0.000 | n/a | 1.316 | 1.006 | 0.146 | 0.315 | bend/corner induced residual |
| `no_via_background__v83` | `no_via_background` | `unet_no_topology` | yes | 0.439 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.479 | 1.161 | 0.146 | 0.267 | bend/corner induced residual |
| `no_via_background__v84` | `no_via_background` | `unet_no_topology` | yes | 0.428 | 0.045 | 4 | 3 | 0.000 | 5.000 | n/a | 1.258 | 0.752 | 0.143 | 0.390 | model hallucination |
| `no_via_background__v85` | `no_via_background` | `unet_no_topology` | yes | 0.299 | 0.040 | 5 | 4 | 1.000 | 1.000 | n/a | 1.416 | 0.676 | 0.203 | 0.312 | bend/corner induced residual |
| `no_via_background__v86` | `no_via_background` | `unet_no_topology` | yes | 0.390 | 0.041 | 4 | 3 | 0.000 | 0.000 | n/a | 1.498 | 0.670 | 0.248 | 0.619 | bend/corner induced residual |
| `no_via_background__v87` | `no_via_background` | `unet_no_topology` | yes | 0.420 | 0.043 | 4 | 4 | 0.000 | 0.000 | n/a | 1.127 | 0.593 | 0.159 | 0.211 | bend/corner induced residual |
| `no_via_background__v88` | `no_via_background` | `unet_no_topology` | yes | 0.257 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 0.837 | 0.821 | 0.260 | 0.575 | bend/corner induced residual |
| `no_via_background__v89` | `no_via_background` | `unet_no_topology` | yes | 0.220 | 0.023 | 2 | 2 | 0.000 | 0.000 | n/a | 0.715 | 0.750 | 0.183 | 0.129 | bend/corner induced residual |
| `no_via_background__v90` | `no_via_background` | `unet_no_topology` | no | 0.199 | 0.024 | 0 | 0 | 0.000 | 0.000 | n/a | 1.098 | 0.855 | 0.143 | 0.137 | no false positive |
| `no_via_background__v91` | `no_via_background` | `unet_no_topology` | yes | 0.421 | 0.030 | 1 | 1 | 0.000 | 3.000 | n/a | 0.924 | 0.675 | 0.248 | 0.343 | detector threshold sensitivity |
| `no_via_background__v92` | `no_via_background` | `unet_no_topology` | yes | 0.329 | 0.026 | 1 | 1 | 0.000 | 5.000 | n/a | 1.249 | 0.996 | 0.222 | 0.115 | detector threshold sensitivity |
| `no_via_background__v93` | `no_via_background` | `unet_no_topology` | yes | 0.350 | 0.034 | 2 | 2 | 0.000 | 5.000 | n/a | 1.147 | 0.804 | 0.195 | 0.080 | operator mismatch |
| `no_via_background__v94` | `no_via_background` | `unet_no_topology` | yes | 0.297 | 0.030 | 2 | 2 | 1.000 | 1.000 | n/a | 1.314 | 0.994 | 0.210 | 0.631 | bend/corner induced residual |
| `no_via_background__v95` | `no_via_background` | `unet_no_topology` | no | 0.181 | 0.023 | 0 | 0 | 1.000 | 1.000 | n/a | 0.761 | 0.702 | 0.182 | 0.183 | no false positive |
| `no_via_background__v96` | `no_via_background` | `unet_no_topology` | yes | 0.421 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.390 | 1.062 | 0.155 | 0.160 | bend/corner induced residual |
| `bend_artifact_trace` | `bend_artifact` | `unet_no_topology` | yes | 0.805 | 0.050 | 1 | 1 | 0.000 | 0.000 | n/a | 2.029 | 0.993 | 0.217 | 0.291 | bend/corner induced residual |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_no_topology` | yes | 0.620 | 0.040 | 1 | 1 | 1.000 | 1.000 | n/a | 2.104 | 1.043 | 0.176 | 0.358 | bend/corner induced residual |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_no_topology` | yes | 0.216 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 2.437 | 1.115 | 0.190 | 0.200 | bend/corner induced residual |
| `bend_artifact_trace__v03` | `bend_artifact` | `unet_no_topology` | yes | 0.532 | 0.038 | 1 | 1 | 0.000 | 0.000 | n/a | 2.128 | 0.935 | 0.146 | 0.187 | bend/corner induced residual |
| `bend_artifact_trace__v04` | `bend_artifact` | `unet_no_topology` | yes | 0.471 | 0.043 | 3 | 3 | 0.000 | 0.000 | n/a | 1.749 | 0.798 | 0.196 | 0.365 | bend/corner induced residual |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_no_topology` | yes | 0.289 | 0.034 | 3 | 3 | 0.000 | 0.000 | n/a | 1.665 | 0.838 | 0.229 | 0.354 | bend/corner induced residual |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_no_topology` | yes | 0.479 | 0.043 | 2 | 2 | 0.000 | 0.000 | n/a | 1.703 | 0.749 | 0.134 | 0.428 | bend/corner induced residual |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_no_topology` | yes | 0.496 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 1.293 | 0.611 | 0.207 | 0.594 | bend/corner induced residual |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_no_topology` | yes | 0.667 | 0.046 | 2 | 2 | 0.000 | 0.000 | n/a | 2.465 | 1.236 | 0.173 | 0.143 | bend/corner induced residual |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_no_topology` | yes | 0.549 | 0.040 | 2 | 2 | 0.000 | 0.000 | n/a | 2.789 | 1.194 | 0.236 | 0.208 | bend/corner induced residual |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_no_topology` | yes | 0.496 | 0.045 | 4 | 3 | 0.000 | 0.000 | n/a | 2.171 | 0.950 | 0.187 | 0.286 | bend/corner induced residual |
| `bend_artifact_trace__v11` | `bend_artifact` | `unet_no_topology` | yes | 0.778 | 0.050 | 2 | 2 | 0.000 | 0.000 | n/a | 2.735 | 0.996 | 0.150 | 0.261 | bend/corner induced residual |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_no_topology` | yes | 0.288 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.202 | 0.936 | 0.223 | 0.172 | bend/corner induced residual |
| `bend_artifact_trace__v13` | `bend_artifact` | `unet_no_topology` | yes | 0.333 | 0.032 | 2 | 1 | 1.000 | 1.000 | n/a | 1.519 | 0.934 | 0.238 | 0.734 | bend/corner induced residual |
| `bend_artifact_trace__v14` | `bend_artifact` | `unet_no_topology` | no | 0.141 | 0.019 | 0 | 0 | 0.000 | 2.000 | n/a | 1.065 | 0.687 | 0.162 | 0.300 | no false positive |
| `bend_artifact_trace__v15` | `bend_artifact` | `unet_no_topology` | yes | 0.205 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.109 | 0.747 | 0.164 | 0.138 | bend/corner induced residual |
| `bend_artifact_trace__v16` | `bend_artifact` | `unet_no_topology` | yes | 0.345 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 1.743 | 0.661 | 0.214 | 0.500 | bend/corner induced residual |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_no_topology` | yes | 0.407 | 0.037 | 3 | 3 | 0.000 | 0.000 | n/a | 1.873 | 0.621 | 0.219 | 0.513 | bend/corner induced residual |
| `bend_artifact_trace__v18` | `bend_artifact` | `unet_no_topology` | yes | 0.466 | 0.037 | 1 | 1 | 0.000 | 3.000 | n/a | 1.538 | 0.663 | 0.167 | 0.227 | detector threshold sensitivity |
| `bend_artifact_trace__v19` | `bend_artifact` | `unet_no_topology` | yes | 0.416 | 0.039 | 3 | 3 | 0.000 | 0.000 | n/a | 1.720 | 0.599 | 0.204 | 0.404 | bend/corner induced residual |
| `bend_artifact_trace__v20` | `bend_artifact` | `unet_no_topology` | yes | 0.201 | 0.025 | 1 | 1 | 0.000 | 2.000 | n/a | 1.321 | 0.572 | 0.245 | 0.611 | bend/corner induced residual |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_no_topology` | yes | 0.342 | 0.041 | 4 | 4 | 0.000 | 1.000 | n/a | 1.950 | 0.658 | 0.216 | 0.619 | bend/corner induced residual |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_no_topology` | yes | 0.607 | 0.044 | 2 | 2 | 0.000 | 0.000 | n/a | 1.796 | 0.617 | 0.233 | 0.500 | bend/corner induced residual |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_no_topology` | yes | 0.317 | 0.037 | 4 | 4 | 0.000 | 2.000 | n/a | 1.486 | 0.672 | 0.218 | 0.554 | bend/corner induced residual |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_no_topology` | yes | 0.473 | 0.044 | 3 | 3 | 0.000 | 0.000 | n/a | 2.396 | 1.084 | 0.214 | 0.360 | bend/corner induced residual |
| `bend_artifact_trace__v25` | `bend_artifact` | `unet_no_topology` | yes | 0.538 | 0.043 | 2 | 2 | 1.000 | 1.000 | n/a | 2.819 | 1.162 | 0.233 | 0.239 | bend/corner induced residual |
| `bend_artifact_trace__v26` | `bend_artifact` | `unet_no_topology` | yes | 0.836 | 0.053 | 2 | 2 | 0.000 | 0.000 | n/a | 2.754 | 1.116 | 0.162 | 0.363 | bend/corner induced residual |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_no_topology` | yes | 0.617 | 0.045 | 2 | 2 | 0.000 | 0.000 | n/a | 2.627 | 1.000 | 0.177 | 0.180 | bend/corner induced residual |
| `bend_artifact_trace__v28` | `bend_artifact` | `unet_no_topology` | yes | 0.300 | 0.036 | 3 | 3 | 0.000 | 0.000 | n/a | 1.845 | 1.115 | 0.222 | 0.657 | bend/corner induced residual |
| `bend_artifact_trace__v29` | `bend_artifact` | `unet_no_topology` | yes | 0.279 | 0.036 | 3 | 3 | 0.000 | 0.000 | n/a | 1.943 | 1.037 | 0.202 | 0.403 | bend/corner induced residual |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_no_topology` | yes | 0.360 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 2.098 | 0.918 | 0.154 | 0.592 | bend/corner induced residual |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_no_topology` | yes | 0.328 | 0.034 | 3 | 3 | 0.000 | 0.000 | n/a | 2.081 | 0.893 | 0.150 | 0.573 | bend/corner induced residual |
| `bend_artifact_trace__v32` | `bend_artifact` | `unet_no_topology` | yes | 0.735 | 0.045 | 1 | 1 | 0.000 | 0.000 | n/a | 2.684 | 1.301 | 0.229 | 0.092 | bend/corner induced residual |
| `bend_artifact_trace__v33` | `bend_artifact` | `unet_no_topology` | yes | 0.293 | 0.026 | 2 | 1 | 0.000 | 0.000 | n/a | 1.781 | 1.009 | 0.158 | 0.124 | bend/corner induced residual |
| `bend_artifact_trace__v34` | `bend_artifact` | `unet_no_topology` | yes | 0.832 | 0.051 | 1 | 1 | 0.000 | 0.000 | n/a | 2.392 | 1.026 | 0.247 | 0.386 | bend/corner induced residual |
| `bend_artifact_trace__v35` | `bend_artifact` | `unet_no_topology` | yes | 0.859 | 0.053 | 1 | 1 | 0.000 | 0.000 | n/a | 2.631 | 1.027 | 0.237 | 0.454 | bend/corner induced residual |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_no_topology` | yes | 0.369 | 0.044 | 6 | 6 | 0.000 | 3.000 | n/a | 1.796 | 0.649 | 0.214 | 0.648 | detector threshold sensitivity |
| `bend_artifact_trace__v37` | `bend_artifact` | `unet_no_topology` | yes | 0.211 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 1.520 | 0.578 | 0.240 | 0.532 | bend/corner induced residual |
| `bend_artifact_trace__v38` | `bend_artifact` | `unet_no_topology` | yes | 0.450 | 0.041 | 2 | 2 | 0.000 | 2.000 | n/a | 1.636 | 0.753 | 0.219 | 0.541 | bend/corner induced residual |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_no_topology` | yes | 0.497 | 0.050 | 5 | 4 | 0.000 | 3.000 | n/a | 1.636 | 0.579 | 0.113 | 0.290 | detector threshold sensitivity |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_no_topology` | yes | 0.898 | 0.057 | 1 | 1 | 0.000 | 0.000 | n/a | 2.039 | 0.981 | 0.222 | 0.238 | bend/corner induced residual |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_no_topology` | yes | 0.526 | 0.039 | 2 | 2 | 0.000 | 0.000 | n/a | 1.709 | 0.805 | 0.234 | 0.289 | bend/corner induced residual |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_no_topology` | yes | 0.290 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.226 | 0.775 | 0.210 | 0.155 | bend/corner induced residual |
| `bend_artifact_trace__v43` | `bend_artifact` | `unet_no_topology` | yes | 0.231 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.347 | 0.923 | 0.202 | 0.144 | bend/corner induced residual |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_no_topology` | yes | 0.492 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 1.374 | 0.813 | 0.213 | 0.340 | bend/corner induced residual |
| `bend_artifact_trace__v45` | `bend_artifact` | `unet_no_topology` | yes | 0.242 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.142 | 0.824 | 0.178 | 0.325 | bend/corner induced residual |
| `bend_artifact_trace__v46` | `bend_artifact` | `unet_no_topology` | yes | 0.254 | 0.026 | 1 | 1 | 1.000 | 2.236 | n/a | 0.949 | 0.706 | 0.248 | 0.327 | detector threshold sensitivity |
| `bend_artifact_trace__v47` | `bend_artifact` | `unet_no_topology` | yes | 0.334 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.134 | 0.591 | 0.189 | 0.392 | bend/corner induced residual |
| `bend_artifact_trace__v48` | `bend_artifact` | `unet_no_topology` | yes | 0.641 | 0.041 | 1 | 1 | 0.000 | 0.000 | n/a | 2.339 | 1.249 | 0.159 | 0.147 | bend/corner induced residual |
| `bend_artifact_trace__v49` | `bend_artifact` | `unet_no_topology` | yes | 0.660 | 0.042 | 1 | 1 | 0.000 | 0.000 | n/a | 2.179 | 1.059 | 0.234 | 0.139 | bend/corner induced residual |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_no_topology` | yes | 0.312 | 0.028 | 2 | 1 | 0.000 | 0.000 | n/a | 1.901 | 0.958 | 0.188 | 0.343 | bend/corner induced residual |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_no_topology` | yes | 0.654 | 0.041 | 1 | 1 | 0.000 | 0.000 | n/a | 1.937 | 0.940 | 0.152 | 0.308 | bend/corner induced residual |
| `bend_artifact_trace__v52` | `bend_artifact` | `unet_no_topology` | yes | 0.403 | 0.035 | 2 | 2 | 0.000 | 0.000 | n/a | 1.776 | 1.000 | 0.252 | 0.232 | bend/corner induced residual |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_no_topology` | yes | 0.515 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 1.692 | 0.910 | 0.225 | 0.326 | bend/corner induced residual |
| `bend_artifact_trace__v54` | `bend_artifact` | `unet_no_topology` | yes | 0.473 | 0.044 | 3 | 3 | 0.000 | 0.000 | n/a | 1.627 | 0.763 | 0.248 | 0.402 | bend/corner induced residual |
| `bend_artifact_trace__v55` | `bend_artifact` | `unet_no_topology` | yes | 0.351 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 1.738 | 0.890 | 0.256 | 0.417 | bend/corner induced residual |
| `bend_artifact_trace__v56` | `bend_artifact` | `unet_no_topology` | yes | 1.043 | 0.064 | 2 | 2 | 0.000 | 0.000 | n/a | 2.913 | 1.205 | 0.213 | 0.328 | bend/corner induced residual |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_no_topology` | yes | 0.591 | 0.047 | 2 | 2 | 0.000 | 0.000 | n/a | 2.235 | 0.829 | 0.186 | 0.254 | bend/corner induced residual |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_no_topology` | yes | 0.725 | 0.049 | 2 | 2 | 0.000 | 0.000 | n/a | 2.704 | 1.222 | 0.253 | 0.154 | bend/corner induced residual |
| `bend_artifact_trace__v59` | `bend_artifact` | `unet_no_topology` | yes | 0.452 | 0.040 | 3 | 3 | 1.000 | 1.000 | n/a | 1.838 | 1.000 | 0.180 | 0.564 | bend/corner induced residual |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_no_topology` | yes | 0.215 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.099 | 0.861 | 0.194 | 0.154 | bend/corner induced residual |
| `bend_artifact_trace__v61` | `bend_artifact` | `unet_no_topology` | yes | 0.269 | 0.031 | 2 | 2 | 0.000 | 2.000 | n/a | 0.965 | 0.765 | 0.234 | 0.156 | bend/corner induced residual |
| `bend_artifact_trace__v62` | `bend_artifact` | `unet_no_topology` | no | 0.172 | 0.025 | 0 | 0 | 0.000 | 0.000 | n/a | 1.251 | 0.673 | 0.233 | 0.356 | no false positive |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_no_topology` | yes | 0.222 | 0.030 | 2 | 2 | 1.000 | 1.000 | n/a | 1.384 | 0.750 | 0.222 | 0.363 | bend/corner induced residual |
| `bend_artifact_trace__v64` | `bend_artifact` | `unet_no_topology` | no | 0.170 | 0.024 | 0 | 0 | 0.000 | 0.000 | n/a | 1.647 | 0.663 | 0.162 | 0.343 | no false positive |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_no_topology` | yes | 0.238 | 0.028 | 2 | 2 | 0.000 | 3.000 | n/a | 2.108 | 0.750 | 0.211 | 0.485 | operator mismatch |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_no_topology` | yes | 0.320 | 0.031 | 2 | 2 | 1.000 | 2.236 | n/a | 1.608 | 0.633 | 0.247 | 0.326 | operator mismatch |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_no_topology` | yes | 0.389 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.638 | 0.578 | 0.192 | 0.452 | bend/corner induced residual |
| `bend_artifact_trace__v68` | `bend_artifact` | `unet_no_topology` | yes | 0.203 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.546 | 0.733 | 0.173 | 0.591 | bend/corner induced residual |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_no_topology` | yes | 0.537 | 0.050 | 4 | 4 | 0.000 | 3.000 | n/a | 1.884 | 0.676 | 0.162 | 0.362 | detector threshold sensitivity |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_no_topology` | yes | 0.289 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 1.561 | 0.722 | 0.210 | 0.362 | bend/corner induced residual |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_no_topology` | yes | 0.242 | 0.031 | 2 | 2 | 0.000 | 3.000 | n/a | 1.712 | 0.731 | 0.251 | 0.461 | detector threshold sensitivity |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_no_topology` | yes | 0.395 | 0.042 | 3 | 2 | 0.000 | 0.000 | n/a | 1.773 | 1.021 | 0.218 | 0.190 | bend/corner induced residual |
| `bend_artifact_trace__v73` | `bend_artifact` | `unet_no_topology` | yes | 0.774 | 0.056 | 3 | 2 | 1.000 | 1.000 | n/a | 1.966 | 1.039 | 0.185 | 0.626 | bend/corner induced residual |
| `bend_artifact_trace__v74` | `bend_artifact` | `unet_no_topology` | yes | 0.737 | 0.049 | 2 | 2 | 1.000 | 1.000 | n/a | 3.201 | 1.243 | 0.247 | 0.380 | bend/corner induced residual |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_no_topology` | yes | 0.688 | 0.049 | 3 | 3 | 0.000 | 0.000 | n/a | 2.286 | 1.025 | 0.211 | 0.182 | bend/corner induced residual |
| `bend_artifact_trace__v76` | `bend_artifact` | `unet_no_topology` | yes | 0.436 | 0.037 | 1 | 1 | 0.000 | 0.000 | n/a | 1.903 | 0.928 | 0.257 | 0.570 | bend/corner induced residual |
| `bend_artifact_trace__v77` | `bend_artifact` | `unet_no_topology` | yes | 0.285 | 0.030 | 2 | 1 | 0.000 | 0.000 | n/a | 2.281 | 0.967 | 0.194 | 0.741 | bend/corner induced residual |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_no_topology` | yes | 0.365 | 0.041 | 3 | 3 | 0.000 | 0.000 | n/a | 1.938 | 0.882 | 0.183 | 0.696 | bend/corner induced residual |
| `bend_artifact_trace__v79` | `bend_artifact` | `unet_no_topology` | yes | 0.413 | 0.040 | 3 | 3 | 1.000 | 1.000 | n/a | 2.184 | 0.814 | 0.204 | 0.737 | bend/corner induced residual |
| `bend_artifact_trace__v80` | `bend_artifact` | `unet_no_topology` | yes | 0.668 | 0.041 | 1 | 1 | 0.000 | 0.000 | n/a | 1.892 | 1.098 | 0.252 | 0.231 | bend/corner induced residual |
| `bend_artifact_trace__v81` | `bend_artifact` | `unet_no_topology` | yes | 0.546 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 2.012 | 1.014 | 0.143 | 0.246 | bend/corner induced residual |
| `bend_artifact_trace__v82` | `bend_artifact` | `unet_no_topology` | yes | 0.583 | 0.038 | 1 | 1 | 0.000 | 0.000 | n/a | 2.244 | 1.095 | 0.206 | 0.435 | bend/corner induced residual |
| `bend_artifact_trace__v83` | `bend_artifact` | `unet_no_topology` | yes | 0.414 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 2.249 | 1.038 | 0.191 | 0.229 | bend/corner induced residual |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_no_topology` | yes | 0.568 | 0.048 | 3 | 3 | 0.000 | 3.000 | n/a | 1.894 | 0.717 | 0.136 | 0.422 | detector threshold sensitivity |
| `bend_artifact_trace__v85` | `bend_artifact` | `unet_no_topology` | no | 0.161 | 0.023 | 0 | 0 | 1.000 | 3.162 | n/a | 1.621 | 0.734 | 0.178 | 0.486 | no false positive |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_no_topology` | yes | 0.230 | 0.034 | 3 | 3 | 1.000 | 1.000 | n/a | 1.731 | 0.730 | 0.247 | 0.572 | bend/corner induced residual |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_no_topology` | yes | 0.486 | 0.049 | 4 | 4 | 0.000 | 0.000 | n/a | 2.101 | 0.646 | 0.159 | 0.420 | bend/corner induced residual |
| `bend_artifact_trace__v88` | `bend_artifact` | `unet_no_topology` | yes | 0.483 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 1.174 | 0.737 | 0.256 | 0.804 | bend/corner induced residual |
| `bend_artifact_trace__v89` | `bend_artifact` | `unet_no_topology` | yes | 0.310 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.353 | 0.794 | 0.236 | 0.342 | bend/corner induced residual |
| `bend_artifact_trace__v90` | `bend_artifact` | `unet_no_topology` | yes | 0.302 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.227 | 0.782 | 0.233 | 0.524 | bend/corner induced residual |
| `bend_artifact_trace__v91` | `bend_artifact` | `unet_no_topology` | yes | 0.228 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.280 | 0.871 | 0.246 | 0.312 | bend/corner induced residual |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_no_topology` | yes | 0.288 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.202 | 0.936 | 0.223 | 0.172 | bend/corner induced residual |
| `bend_artifact_trace__v93` | `bend_artifact` | `unet_no_topology` | yes | 0.348 | 0.033 | 2 | 1 | 1.000 | 1.000 | n/a | 1.461 | 0.897 | 0.223 | 0.706 | bend/corner induced residual |
| `bend_artifact_trace__v94` | `bend_artifact` | `unet_no_topology` | no | 0.161 | 0.026 | 0 | 0 | 0.000 | 0.000 | n/a | 1.076 | 0.673 | 0.182 | 0.246 | no false positive |
| `bend_artifact_trace__v95` | `bend_artifact` | `unet_no_topology` | yes | 0.205 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.109 | 0.747 | 0.164 | 0.138 | bend/corner induced residual |
| `bend_artifact_trace__v96` | `bend_artifact` | `unet_no_topology` | yes | 0.889 | 0.055 | 1 | 1 | 0.000 | 0.000 | n/a | 2.308 | 1.069 | 0.162 | 0.116 | bend/corner induced residual |
| `bend_artifact_trace__v97` | `bend_artifact` | `unet_no_topology` | yes | 0.704 | 0.046 | 2 | 1 | 0.000 | 0.000 | n/a | 2.297 | 1.093 | 0.217 | 0.109 | bend/corner induced residual |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_no_topology` | yes | 0.669 | 0.042 | 1 | 1 | 0.000 | 0.000 | n/a | 2.484 | 1.077 | 0.208 | 0.384 | bend/corner induced residual |
| `bend_artifact_trace__v99` | `bend_artifact` | `unet_no_topology` | yes | 0.716 | 0.044 | 1 | 1 | 0.000 | 0.000 | n/a | 2.679 | 1.214 | 0.119 | 0.143 | bend/corner induced residual |
| `straight_trace` | `canonical` | `unet_topology_soft_loss` | no | 0.058 | 0.008 | 0 | 0 | 1.000 | n/a | n/a | 0.357 | 1.219 | 0.004 | 0.036 | no false positive |
| `finite_width_trace` | `canonical` | `unet_topology_soft_loss` | no | 0.077 | 0.008 | 0 | 0 | 1.000 | n/a | n/a | 0.314 | 1.004 | 0.194 | 0.193 | no false positive |
| `l_shape_trace` | `canonical` | `unet_topology_soft_loss` | yes | 0.457 | 0.042 | 3 | 2 | 0.000 | 0.000 | n/a | 0.503 | 0.410 | 0.004 | 0.177 | bend/corner induced residual |
| `no_via_background` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.274 | 0.022 | 1 | 1 | 1.000 | 1.000 | n/a | 0.913 | 0.753 | 0.265 | 0.811 | bend/corner induced residual |
| `no_via_background__v01` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.572 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 1.079 | 0.981 | 0.197 | 0.445 | bend/corner induced residual |
| `no_via_background__v02` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.601 | 0.037 | 1 | 1 | 0.000 | 0.000 | n/a | 0.923 | 0.953 | 0.146 | 0.428 | bend/corner induced residual |
| `no_via_background__v03` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.498 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.912 | 0.946 | 0.146 | 0.419 | bend/corner induced residual |
| `no_via_background__v04` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.291 | 0.029 | 3 | 2 | 1.000 | 1.000 | n/a | 0.977 | 0.769 | 0.231 | 0.633 | bend/corner induced residual |
| `no_via_background__v05` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.282 | 0.028 | 3 | 2 | 0.000 | 0.000 | n/a | 0.940 | 0.745 | 0.215 | 0.422 | bend/corner induced residual |
| `no_via_background__v06` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.470 | 0.034 | 1 | 1 | 1.000 | 1.000 | n/a | 0.902 | 0.680 | 0.214 | 0.595 | bend/corner induced residual |
| `no_via_background__v07` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.447 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 0.828 | 0.682 | 0.171 | 0.333 | bend/corner induced residual |
| `no_via_background__v08` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.475 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.422 | 0.874 | 0.203 | 0.575 | bend/corner induced residual |
| `no_via_background__v09` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.883 | 0.055 | 1 | 1 | 0.000 | 0.000 | n/a | 1.086 | 0.825 | 0.183 | 0.493 | bend/corner induced residual |
| `no_via_background__v10` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.782 | 0.052 | 2 | 2 | 0.000 | 0.000 | n/a | 1.046 | 0.777 | 0.136 | 0.271 | bend/corner induced residual |
| `no_via_background__v11` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.303 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.355 | 0.933 | 0.176 | 0.288 | bend/corner induced residual |
| `no_via_background__v12` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.217 | 0.021 | 2 | 2 | 0.000 | 2.000 | n/a | 0.693 | 0.711 | 0.222 | 0.074 | bend/corner induced residual |
| `no_via_background__v13` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.400 | 0.030 | 1 | 1 | 0.000 | 5.000 | n/a | 0.618 | 0.692 | 0.195 | 0.150 | operator mismatch |
| `no_via_background__v14` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.211 | 0.022 | 1 | 1 | 0.000 | 6.000 | n/a | 0.602 | 0.681 | 0.210 | 0.456 | operator mismatch |
| `no_via_background__v15` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.252 | 0.027 | 1 | 1 | 0.000 | 6.000 | n/a | 0.537 | 0.617 | 0.116 | 0.151 | model hallucination |
| `no_via_background__v16` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.455 | 0.039 | 3 | 3 | 0.000 | 5.000 | n/a | 0.872 | 0.538 | 0.165 | 0.379 | operator mismatch |
| `no_via_background__v17` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.500 | 0.039 | 2 | 2 | 0.000 | 5.000 | n/a | 0.980 | 0.516 | 0.176 | 0.473 | operator mismatch |
| `no_via_background__v18` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.312 | 0.032 | 2 | 2 | 0.000 | 6.000 | n/a | 0.729 | 0.466 | 0.194 | 0.475 | operator mismatch |
| `no_via_background__v19` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.482 | 0.035 | 1 | 1 | 0.000 | 6.000 | n/a | 0.710 | 0.494 | 0.170 | 0.421 | operator mismatch |
| `no_via_background__v20` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.525 | 0.039 | 2 | 2 | 0.000 | 5.000 | n/a | 0.767 | 0.671 | 0.253 | 0.312 | operator mismatch |
| `no_via_background__v21` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.525 | 0.044 | 2 | 2 | 0.000 | 5.000 | n/a | 0.800 | 0.571 | 0.201 | 0.342 | operator mismatch |
| `no_via_background__v22` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.298 | 0.037 | 4 | 3 | 0.000 | 6.000 | n/a | 0.755 | 0.602 | 0.143 | 0.292 | model hallucination |
| `no_via_background__v23` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.306 | 0.039 | 5 | 4 | 1.000 | 1.000 | n/a | 0.862 | 0.616 | 0.174 | 0.531 | bend/corner induced residual |
| `no_via_background__v24` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.866 | 0.054 | 1 | 1 | 0.000 | 0.000 | n/a | 1.218 | 0.846 | 0.165 | 0.509 | bend/corner induced residual |
| `no_via_background__v25` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.853 | 0.054 | 1 | 1 | 0.000 | 0.000 | n/a | 1.020 | 0.747 | 0.194 | 0.471 | bend/corner induced residual |
| `no_via_background__v26` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.706 | 0.047 | 2 | 2 | 0.000 | 0.000 | n/a | 1.027 | 0.855 | 0.210 | 0.477 | bend/corner induced residual |
| `no_via_background__v27` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.711 | 0.048 | 2 | 2 | 0.000 | 0.000 | n/a | 0.969 | 0.844 | 0.171 | 0.223 | bend/corner induced residual |
| `no_via_background__v28` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.307 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.455 | 0.947 | 0.163 | 0.425 | bend/corner induced residual |
| `no_via_background__v29` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.228 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.256 | 0.819 | 0.231 | 0.487 | bend/corner induced residual |
| `no_via_background__v30` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.287 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.053 | 0.800 | 0.146 | 0.496 | bend/corner induced residual |
| `no_via_background__v31` | `no_via_background` | `unet_topology_soft_loss` | no | 0.148 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.300 | 0.853 | 0.176 | 0.660 | no false positive |
| `no_via_background__v32` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.596 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 1.134 | 1.009 | 0.264 | 0.343 | bend/corner induced residual |
| `no_via_background__v33` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.472 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.012 | 1.033 | 0.207 | 0.574 | bend/corner induced residual |
| `no_via_background__v34` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.529 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 1.097 | 0.891 | 0.248 | 0.589 | bend/corner induced residual |
| `no_via_background__v35` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.388 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.014 | 0.762 | 0.209 | 0.766 | bend/corner induced residual |
| `no_via_background__v36` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.389 | 0.041 | 3 | 2 | 0.000 | 5.000 | n/a | 0.813 | 0.658 | 0.165 | 0.333 | operator mismatch |
| `no_via_background__v37` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.389 | 0.035 | 3 | 2 | 0.000 | 5.000 | n/a | 0.646 | 0.518 | 0.160 | 0.355 | operator mismatch |
| `no_via_background__v38` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.288 | 0.035 | 4 | 3 | 0.000 | 5.000 | n/a | 0.920 | 0.676 | 0.185 | 0.437 | operator mismatch |
| `no_via_background__v39` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.348 | 0.042 | 6 | 4 | 0.000 | 6.000 | n/a | 0.817 | 0.538 | 0.177 | 0.316 | operator mismatch |
| `no_via_background__v40` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.425 | 0.030 | 1 | 1 | 0.000 | 5.000 | n/a | 0.747 | 0.600 | 0.223 | 0.324 | operator mismatch |
| `no_via_background__v41` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.242 | 0.024 | 1 | 1 | 0.000 | 2.000 | n/a | 0.566 | 0.623 | 0.202 | 0.174 | bend/corner induced residual |
| `no_via_background__v42` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.370 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 0.573 | 0.683 | 0.143 | 0.138 | bend/corner induced residual |
| `no_via_background__v43` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.263 | 0.030 | 3 | 3 | 0.000 | 0.000 | n/a | 0.619 | 0.603 | 0.179 | 0.203 | bend/corner induced residual |
| `no_via_background__v44` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.208 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.715 | 0.668 | 0.211 | 0.503 | bend/corner induced residual |
| `no_via_background__v45` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.216 | 0.024 | 2 | 2 | 0.000 | 5.000 | n/a | 0.647 | 0.677 | 0.203 | 0.129 | operator mismatch |
| `no_via_background__v46` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.314 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 0.681 | 0.666 | 0.263 | 0.588 | bend/corner induced residual |
| `no_via_background__v47` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.324 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 0.708 | 0.627 | 0.151 | 0.168 | bend/corner induced residual |
| `no_via_background__v48` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.204 | 0.018 | 1 | 1 | 0.000 | 0.000 | n/a | 0.863 | 1.054 | 0.135 | 0.491 | bend/corner induced residual |
| `no_via_background__v49` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.506 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.892 | 0.959 | 0.197 | 0.414 | bend/corner induced residual |
| `no_via_background__v50` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.655 | 0.040 | 1 | 1 | 0.000 | 0.000 | n/a | 1.044 | 0.996 | 0.135 | 0.460 | bend/corner induced residual |
| `no_via_background__v51` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.440 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 0.909 | 0.942 | 0.109 | 0.490 | bend/corner induced residual |
| `no_via_background__v52` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.653 | 0.040 | 1 | 1 | 0.000 | 0.000 | n/a | 1.453 | 0.814 | 0.234 | 0.610 | bend/corner induced residual |
| `no_via_background__v53` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.301 | 0.027 | 2 | 1 | 0.000 | 0.000 | n/a | 1.084 | 0.724 | 0.170 | 0.597 | bend/corner induced residual |
| `no_via_background__v54` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.323 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.037 | 0.831 | 0.263 | 0.735 | bend/corner induced residual |
| `no_via_background__v55` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.283 | 0.031 | 3 | 2 | 0.000 | 0.000 | n/a | 0.840 | 0.682 | 0.239 | 0.546 | bend/corner induced residual |
| `no_via_background__v56` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.799 | 0.049 | 2 | 2 | 0.000 | 0.000 | n/a | 0.988 | 0.773 | 0.211 | 0.797 | bend/corner induced residual |
| `no_via_background__v57` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.670 | 0.044 | 2 | 2 | 0.000 | 0.000 | n/a | 1.080 | 0.840 | 0.211 | 0.220 | bend/corner induced residual |
| `no_via_background__v58` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.875 | 0.056 | 2 | 2 | 0.000 | 0.000 | n/a | 1.018 | 0.722 | 0.185 | 0.651 | bend/corner induced residual |
| `no_via_background__v59` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.878 | 0.057 | 2 | 2 | 0.000 | 0.000 | n/a | 1.077 | 0.694 | 0.176 | 0.698 | bend/corner induced residual |
| `no_via_background__v60` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.378 | 0.034 | 2 | 2 | 0.000 | 0.000 | n/a | 0.716 | 0.658 | 0.221 | 0.127 | bend/corner induced residual |
| `no_via_background__v61` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.314 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 0.681 | 0.666 | 0.202 | 0.195 | bend/corner induced residual |
| `no_via_background__v62` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.316 | 0.027 | 2 | 2 | 0.000 | 5.000 | n/a | 0.606 | 0.657 | 0.143 | 0.127 | model hallucination |
| `no_via_background__v63` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.356 | 0.028 | 2 | 2 | 0.000 | 5.000 | n/a | 0.618 | 0.687 | 0.177 | 0.179 | operator mismatch |
| `no_via_background__v64` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.460 | 0.041 | 4 | 4 | 0.000 | 5.000 | n/a | 0.946 | 0.538 | 0.155 | 0.420 | operator mismatch |
| `no_via_background__v65` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.387 | 0.033 | 2 | 2 | 0.000 | 5.000 | n/a | 0.968 | 0.547 | 0.192 | 0.510 | operator mismatch |
| `no_via_background__v66` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.410 | 0.040 | 3 | 3 | 1.000 | 5.099 | n/a | 0.879 | 0.511 | 0.248 | 0.732 | operator mismatch |
| `no_via_background__v67` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.459 | 0.040 | 3 | 3 | 0.000 | 5.000 | n/a | 0.825 | 0.499 | 0.153 | 0.434 | operator mismatch |
| `no_via_background__v68` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.596 | 0.049 | 2 | 2 | 0.000 | 0.000 | n/a | 0.817 | 0.635 | 0.203 | 0.414 | bend/corner induced residual |
| `no_via_background__v69` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.344 | 0.039 | 5 | 3 | 0.000 | 6.000 | n/a | 0.722 | 0.596 | 0.230 | 0.296 | operator mismatch |
| `no_via_background__v70` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.445 | 0.037 | 4 | 3 | 0.000 | 5.000 | n/a | 0.745 | 0.590 | 0.143 | 0.343 | model hallucination |
| `no_via_background__v71` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.294 | 0.034 | 3 | 3 | 0.000 | 0.000 | n/a | 0.921 | 0.623 | 0.218 | 0.532 | bend/corner induced residual |
| `no_via_background__v72` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.843 | 0.052 | 1 | 1 | 0.000 | 0.000 | n/a | 1.113 | 0.812 | 0.262 | 0.569 | bend/corner induced residual |
| `no_via_background__v73` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.800 | 0.052 | 2 | 2 | 0.000 | 0.000 | n/a | 0.970 | 0.716 | 0.205 | 0.697 | bend/corner induced residual |
| `no_via_background__v74` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.883 | 0.055 | 1 | 1 | 0.000 | 0.000 | n/a | 1.086 | 0.825 | 0.248 | 0.630 | bend/corner induced residual |
| `no_via_background__v75` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.832 | 0.051 | 1 | 1 | 0.000 | 0.000 | n/a | 1.177 | 0.769 | 0.091 | 0.227 | bend/corner induced residual |
| `no_via_background__v76` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.313 | 0.026 | 1 | 1 | 1.000 | 1.000 | n/a | 1.178 | 0.876 | 0.263 | 0.830 | bend/corner induced residual |
| `no_via_background__v77` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.272 | 0.025 | 2 | 1 | 0.000 | 0.000 | n/a | 0.930 | 0.708 | 0.193 | 0.531 | bend/corner induced residual |
| `no_via_background__v78` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.224 | 0.025 | 1 | 1 | 1.000 | 1.000 | n/a | 0.887 | 0.748 | 0.166 | 0.455 | bend/corner induced residual |
| `no_via_background__v79` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.242 | 0.024 | 2 | 1 | 1.000 | 1.000 | n/a | 0.769 | 0.684 | 0.170 | 0.471 | bend/corner induced residual |
| `no_via_background__v80` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.502 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 1.195 | 1.126 | 0.232 | 0.399 | bend/corner induced residual |
| `no_via_background__v81` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.572 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 1.079 | 0.981 | 0.197 | 0.445 | bend/corner induced residual |
| `no_via_background__v82` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.601 | 0.037 | 1 | 1 | 0.000 | 0.000 | n/a | 0.923 | 0.953 | 0.146 | 0.428 | bend/corner induced residual |
| `no_via_background__v83` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.498 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.912 | 0.946 | 0.146 | 0.419 | bend/corner induced residual |
| `no_via_background__v84` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.540 | 0.045 | 3 | 3 | 0.000 | 5.000 | n/a | 0.745 | 0.687 | 0.143 | 0.327 | model hallucination |
| `no_via_background__v85` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.436 | 0.036 | 2 | 2 | 0.000 | 5.000 | n/a | 0.758 | 0.636 | 0.203 | 0.347 | operator mismatch |
| `no_via_background__v86` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.525 | 0.044 | 2 | 2 | 1.000 | 5.099 | n/a | 0.800 | 0.571 | 0.248 | 0.739 | operator mismatch |
| `no_via_background__v87` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.460 | 0.043 | 4 | 4 | 0.000 | 5.000 | n/a | 0.728 | 0.545 | 0.159 | 0.292 | operator mismatch |
| `no_via_background__v88` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.238 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.688 | 0.671 | 0.260 | 0.784 | bend/corner induced residual |
| `no_via_background__v89` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.245 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 0.651 | 0.640 | 0.183 | 0.179 | bend/corner induced residual |
| `no_via_background__v90` | `no_via_background` | `unet_topology_soft_loss` | no | 0.163 | 0.024 | 0 | 0 | 0.000 | 2.000 | n/a | 0.521 | 0.606 | 0.143 | 0.119 | no false positive |
| `no_via_background__v91` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.517 | 0.036 | 1 | 1 | 0.000 | 3.000 | n/a | 0.623 | 0.555 | 0.248 | 0.427 | operator mismatch |
| `no_via_background__v92` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.217 | 0.021 | 2 | 2 | 0.000 | 2.000 | n/a | 0.693 | 0.711 | 0.222 | 0.074 | bend/corner induced residual |
| `no_via_background__v93` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.400 | 0.030 | 1 | 1 | 0.000 | 5.000 | n/a | 0.618 | 0.692 | 0.195 | 0.150 | operator mismatch |
| `no_via_background__v94` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.211 | 0.022 | 1 | 1 | 0.000 | 6.000 | n/a | 0.602 | 0.681 | 0.210 | 0.456 | operator mismatch |
| `no_via_background__v95` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.236 | 0.026 | 1 | 1 | 0.000 | 6.000 | n/a | 0.532 | 0.603 | 0.182 | 0.203 | operator mismatch |
| `no_via_background__v96` | `no_via_background` | `unet_topology_soft_loss` | yes | 0.520 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 1.212 | 1.010 | 0.155 | 0.318 | bend/corner induced residual |
| `bend_artifact_trace` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.441 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.080 | 0.772 | 0.217 | 0.295 | bend/corner induced residual |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.361 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 1.178 | 0.711 | 0.176 | 0.554 | bend/corner induced residual |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.228 | 0.024 | 1 | 1 | 1.000 | 1.000 | n/a | 1.477 | 0.795 | 0.190 | 0.337 | bend/corner induced residual |
| `bend_artifact_trace__v03` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.221 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.068 | 0.747 | 0.146 | 0.247 | bend/corner induced residual |
| `bend_artifact_trace__v04` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.419 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.244 | 0.576 | 0.196 | 0.576 | bend/corner induced residual |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.414 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 1.215 | 0.725 | 0.229 | 0.507 | bend/corner induced residual |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.426 | 0.033 | 2 | 2 | 0.000 | 0.000 | n/a | 1.168 | 0.524 | 0.134 | 0.682 | bend/corner induced residual |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.332 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 0.898 | 0.504 | 0.207 | 0.670 | bend/corner induced residual |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.437 | 0.043 | 3 | 2 | 0.000 | 0.000 | n/a | 1.143 | 0.708 | 0.173 | 0.337 | bend/corner induced residual |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.318 | 0.034 | 3 | 2 | 0.000 | 0.000 | n/a | 1.190 | 0.726 | 0.236 | 0.340 | bend/corner induced residual |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.531 | 0.045 | 5 | 2 | 0.000 | 0.000 | n/a | 1.049 | 0.588 | 0.187 | 0.453 | bend/corner induced residual |
| `bend_artifact_trace__v11` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.677 | 0.046 | 2 | 2 | 0.000 | 0.000 | n/a | 1.200 | 0.602 | 0.150 | 0.379 | bend/corner induced residual |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.501 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 1.015 | 0.713 | 0.223 | 0.234 | bend/corner induced residual |
| `bend_artifact_trace__v13` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.518 | 0.040 | 3 | 2 | 1.000 | 1.000 | n/a | 0.858 | 0.667 | 0.238 | 0.578 | bend/corner induced residual |
| `bend_artifact_trace__v14` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.185 | 0.021 | 0 | 0 | 1.000 | 4.000 | n/a | 0.760 | 0.551 | 0.162 | 0.385 | no false positive |
| `bend_artifact_trace__v15` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.207 | 0.026 | 1 | 1 | 0.000 | 2.000 | n/a | 0.751 | 0.611 | 0.164 | 0.271 | bend/corner induced residual |
| `bend_artifact_trace__v16` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.422 | 0.042 | 3 | 3 | 0.000 | 0.000 | n/a | 0.938 | 0.638 | 0.214 | 0.493 | bend/corner induced residual |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.368 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.120 | 0.651 | 0.219 | 0.550 | bend/corner induced residual |
| `bend_artifact_trace__v18` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.598 | 0.054 | 3 | 3 | 0.000 | 3.000 | n/a | 0.895 | 0.595 | 0.167 | 0.358 | operator mismatch |
| `bend_artifact_trace__v19` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.487 | 0.043 | 4 | 3 | 0.000 | 0.000 | n/a | 1.117 | 0.631 | 0.204 | 0.545 | bend/corner induced residual |
| `bend_artifact_trace__v20` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.379 | 0.039 | 3 | 2 | 1.000 | 2.236 | n/a | 0.962 | 0.746 | 0.245 | 0.461 | detector threshold sensitivity |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.458 | 0.045 | 5 | 5 | 0.000 | 2.000 | n/a | 1.196 | 0.628 | 0.216 | 0.463 | bend/corner induced residual |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.335 | 0.040 | 3 | 3 | 0.000 | 0.000 | n/a | 0.894 | 0.548 | 0.233 | 0.512 | bend/corner induced residual |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.385 | 0.039 | 4 | 4 | 0.000 | 2.000 | n/a | 0.808 | 0.622 | 0.218 | 0.482 | bend/corner induced residual |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.434 | 0.030 | 1 | 1 | 0.000 | 0.000 | n/a | 1.208 | 0.789 | 0.214 | 0.558 | bend/corner induced residual |
| `bend_artifact_trace__v25` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.136 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.315 | 0.616 | 0.233 | 0.536 | no false positive |
| `bend_artifact_trace__v26` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.618 | 0.045 | 2 | 2 | 0.000 | 0.000 | n/a | 1.286 | 0.654 | 0.162 | 0.563 | bend/corner induced residual |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.460 | 0.041 | 3 | 2 | 0.000 | 0.000 | n/a | 1.278 | 0.684 | 0.177 | 0.256 | bend/corner induced residual |
| `bend_artifact_trace__v28` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.350 | 0.033 | 3 | 3 | 0.000 | 0.000 | n/a | 1.004 | 0.721 | 0.222 | 0.723 | bend/corner induced residual |
| `bend_artifact_trace__v29` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.479 | 0.038 | 2 | 2 | 0.000 | 0.000 | n/a | 0.935 | 0.628 | 0.202 | 0.583 | bend/corner induced residual |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.416 | 0.040 | 3 | 3 | 0.000 | 0.000 | n/a | 1.504 | 0.711 | 0.154 | 0.631 | bend/corner induced residual |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.460 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.160 | 0.612 | 0.150 | 0.589 | bend/corner induced residual |
| `bend_artifact_trace__v32` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.427 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.285 | 0.878 | 0.229 | 0.174 | bend/corner induced residual |
| `bend_artifact_trace__v33` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.202 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.116 | 0.775 | 0.158 | 0.207 | bend/corner induced residual |
| `bend_artifact_trace__v34` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.384 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.013 | 0.820 | 0.247 | 0.390 | bend/corner induced residual |
| `bend_artifact_trace__v35` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.577 | 0.040 | 2 | 2 | 0.000 | 0.000 | n/a | 1.191 | 0.716 | 0.237 | 0.472 | bend/corner induced residual |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.541 | 0.047 | 3 | 3 | 0.000 | 3.000 | n/a | 1.104 | 0.665 | 0.214 | 0.544 | detector threshold sensitivity |
| `bend_artifact_trace__v37` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.355 | 0.031 | 2 | 2 | 0.000 | 3.000 | n/a | 0.869 | 0.544 | 0.240 | 0.460 | operator mismatch |
| `bend_artifact_trace__v38` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.370 | 0.039 | 4 | 4 | 0.000 | 3.000 | n/a | 0.856 | 0.642 | 0.219 | 0.502 | detector threshold sensitivity |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.644 | 0.052 | 5 | 5 | 0.000 | 3.000 | n/a | 0.883 | 0.510 | 0.113 | 0.405 | model hallucination |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.373 | 0.041 | 3 | 2 | 0.000 | 0.000 | n/a | 0.955 | 0.602 | 0.222 | 0.518 | bend/corner induced residual |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.292 | 0.033 | 3 | 2 | 0.000 | 0.000 | n/a | 1.169 | 0.652 | 0.234 | 0.406 | bend/corner induced residual |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.188 | 0.022 | 0 | 0 | 0.000 | 0.000 | n/a | 0.666 | 0.594 | 0.210 | 0.244 | no false positive |
| `bend_artifact_trace__v43` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.319 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.750 | 0.599 | 0.202 | 0.295 | bend/corner induced residual |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.594 | 0.040 | 1 | 1 | 0.000 | 0.000 | n/a | 0.912 | 0.498 | 0.213 | 0.481 | bend/corner induced residual |
| `bend_artifact_trace__v45` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.192 | 0.026 | 0 | 0 | 0.000 | 0.000 | n/a | 0.799 | 0.598 | 0.178 | 0.391 | no false positive |
| `bend_artifact_trace__v46` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.292 | 0.033 | 3 | 2 | 0.000 | 0.000 | n/a | 0.709 | 0.542 | 0.248 | 0.614 | bend/corner induced residual |
| `bend_artifact_trace__v47` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.299 | 0.037 | 3 | 2 | 0.000 | 0.000 | n/a | 0.835 | 0.559 | 0.189 | 0.355 | bend/corner induced residual |
| `bend_artifact_trace__v48` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.322 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 1.132 | 0.901 | 0.159 | 0.172 | bend/corner induced residual |
| `bend_artifact_trace__v49` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.297 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.115 | 0.794 | 0.234 | 0.273 | bend/corner induced residual |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.272 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 1.137 | 0.678 | 0.188 | 0.505 | bend/corner induced residual |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.372 | 0.032 | 3 | 2 | 0.000 | 0.000 | n/a | 1.050 | 0.739 | 0.152 | 0.471 | bend/corner induced residual |
| `bend_artifact_trace__v52` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.595 | 0.039 | 2 | 2 | 0.000 | 0.000 | n/a | 1.144 | 0.810 | 0.252 | 0.454 | bend/corner induced residual |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.596 | 0.041 | 2 | 2 | 0.000 | 0.000 | n/a | 1.122 | 0.688 | 0.225 | 0.542 | bend/corner induced residual |
| `bend_artifact_trace__v54` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.421 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.243 | 0.593 | 0.248 | 0.629 | bend/corner induced residual |
| `bend_artifact_trace__v55` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.547 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 0.913 | 0.569 | 0.256 | 0.400 | bend/corner induced residual |
| `bend_artifact_trace__v56` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.814 | 0.054 | 2 | 2 | 0.000 | 0.000 | n/a | 1.240 | 0.640 | 0.213 | 0.520 | bend/corner induced residual |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.524 | 0.042 | 2 | 2 | 0.000 | 0.000 | n/a | 1.117 | 0.601 | 0.186 | 0.294 | bend/corner induced residual |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.489 | 0.041 | 3 | 2 | 0.000 | 0.000 | n/a | 1.256 | 0.749 | 0.253 | 0.309 | bend/corner induced residual |
| `bend_artifact_trace__v59` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.287 | 0.030 | 3 | 2 | 1.000 | 1.000 | n/a | 1.020 | 0.637 | 0.180 | 0.631 | bend/corner induced residual |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.274 | 0.030 | 2 | 1 | 0.000 | 0.000 | n/a | 0.833 | 0.669 | 0.194 | 0.269 | bend/corner induced residual |
| `bend_artifact_trace__v61` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.344 | 0.036 | 3 | 2 | 0.000 | 0.000 | n/a | 0.741 | 0.602 | 0.234 | 0.322 | bend/corner induced residual |
| `bend_artifact_trace__v62` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.251 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.865 | 0.519 | 0.233 | 0.336 | bend/corner induced residual |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.206 | 0.027 | 2 | 2 | 1.000 | 1.000 | n/a | 0.825 | 0.548 | 0.222 | 0.451 | bend/corner induced residual |
| `bend_artifact_trace__v64` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.352 | 0.039 | 3 | 3 | 0.000 | 0.000 | n/a | 1.144 | 0.640 | 0.162 | 0.496 | bend/corner induced residual |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.504 | 0.044 | 3 | 3 | 0.000 | 3.000 | n/a | 1.158 | 0.673 | 0.211 | 0.440 | operator mismatch |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.378 | 0.041 | 4 | 4 | 0.000 | 1.000 | n/a | 1.017 | 0.602 | 0.247 | 0.444 | bend/corner induced residual |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.517 | 0.043 | 4 | 4 | 0.000 | 0.000 | n/a | 1.089 | 0.626 | 0.192 | 0.590 | bend/corner induced residual |
| `bend_artifact_trace__v68` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.424 | 0.038 | 2 | 1 | 1.000 | 3.000 | n/a | 0.936 | 0.647 | 0.173 | 0.576 | detector threshold sensitivity |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.649 | 0.051 | 5 | 5 | 0.000 | 3.000 | n/a | 0.930 | 0.555 | 0.162 | 0.375 | operator mismatch |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.315 | 0.039 | 3 | 3 | 0.000 | 0.000 | n/a | 1.097 | 0.682 | 0.210 | 0.390 | bend/corner induced residual |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.643 | 0.048 | 2 | 2 | 0.000 | 3.000 | n/a | 1.262 | 0.641 | 0.251 | 0.474 | detector threshold sensitivity |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.532 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 0.961 | 0.683 | 0.218 | 0.270 | bend/corner induced residual |
| `bend_artifact_trace__v73` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.603 | 0.048 | 3 | 2 | 0.000 | 0.000 | n/a | 0.919 | 0.590 | 0.185 | 0.597 | bend/corner induced residual |
| `bend_artifact_trace__v74` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.507 | 0.041 | 3 | 2 | 1.000 | 1.000 | n/a | 1.530 | 0.742 | 0.247 | 0.497 | bend/corner induced residual |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.633 | 0.039 | 1 | 1 | 0.000 | 0.000 | n/a | 1.160 | 0.664 | 0.211 | 0.334 | bend/corner induced residual |
| `bend_artifact_trace__v76` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.359 | 0.038 | 3 | 3 | 0.000 | 0.000 | n/a | 1.083 | 0.597 | 0.257 | 0.569 | bend/corner induced residual |
| `bend_artifact_trace__v77` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.238 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.403 | 0.717 | 0.194 | 0.759 | bend/corner induced residual |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.584 | 0.042 | 2 | 2 | 0.000 | 0.000 | n/a | 1.070 | 0.604 | 0.183 | 0.762 | bend/corner induced residual |
| `bend_artifact_trace__v79` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.519 | 0.043 | 3 | 3 | 0.000 | 0.000 | n/a | 1.143 | 0.595 | 0.204 | 0.757 | bend/corner induced residual |
| `bend_artifact_trace__v80` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.418 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 0.961 | 0.860 | 0.252 | 0.286 | bend/corner induced residual |
| `bend_artifact_trace__v81` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.388 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 1.165 | 0.699 | 0.143 | 0.457 | bend/corner induced residual |
| `bend_artifact_trace__v82` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.285 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.128 | 0.848 | 0.206 | 0.495 | bend/corner induced residual |
| `bend_artifact_trace__v83` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.263 | 0.028 | 2 | 2 | 1.000 | 1.000 | n/a | 1.270 | 0.774 | 0.191 | 0.355 | bend/corner induced residual |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.736 | 0.052 | 3 | 3 | 0.000 | 3.000 | n/a | 1.032 | 0.672 | 0.136 | 0.317 | model hallucination |
| `bend_artifact_trace__v85` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.379 | 0.035 | 2 | 1 | 1.000 | 3.162 | n/a | 0.993 | 0.708 | 0.178 | 0.435 | detector threshold sensitivity |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.559 | 0.041 | 1 | 1 | 0.000 | 2.000 | n/a | 1.093 | 0.622 | 0.247 | 0.514 | bend/corner induced residual |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.321 | 0.040 | 6 | 4 | 0.000 | 0.000 | n/a | 0.961 | 0.500 | 0.159 | 0.455 | bend/corner induced residual |
| `bend_artifact_trace__v88` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.325 | 0.030 | 2 | 2 | 1.000 | 1.000 | n/a | 0.897 | 0.577 | 0.256 | 0.759 | bend/corner induced residual |
| `bend_artifact_trace__v89` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.246 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 0.996 | 0.635 | 0.236 | 0.481 | bend/corner induced residual |
| `bend_artifact_trace__v90` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.268 | 0.031 | 2 | 2 | 0.000 | 3.000 | n/a | 0.878 | 0.614 | 0.233 | 0.551 | operator mismatch |
| `bend_artifact_trace__v91` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.266 | 0.031 | 3 | 2 | 0.000 | 0.000 | n/a | 0.896 | 0.700 | 0.246 | 0.357 | bend/corner induced residual |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.501 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 1.015 | 0.713 | 0.223 | 0.234 | bend/corner induced residual |
| `bend_artifact_trace__v93` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.518 | 0.040 | 3 | 2 | 1.000 | 1.000 | n/a | 0.844 | 0.641 | 0.223 | 0.562 | bend/corner induced residual |
| `bend_artifact_trace__v94` | `bend_artifact` | `unet_topology_soft_loss` | no | 0.199 | 0.026 | 0 | 0 | 0.000 | 0.000 | n/a | 0.710 | 0.542 | 0.182 | 0.247 | no false positive |
| `bend_artifact_trace__v95` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.207 | 0.026 | 1 | 1 | 0.000 | 2.000 | n/a | 0.751 | 0.611 | 0.164 | 0.271 | bend/corner induced residual |
| `bend_artifact_trace__v96` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.393 | 0.036 | 2 | 2 | 0.000 | 0.000 | n/a | 1.173 | 0.792 | 0.162 | 0.250 | bend/corner induced residual |
| `bend_artifact_trace__v97` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.429 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 1.104 | 0.905 | 0.217 | 0.222 | bend/corner induced residual |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.255 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.046 | 0.831 | 0.208 | 0.311 | bend/corner induced residual |
| `bend_artifact_trace__v99` | `bend_artifact` | `unet_topology_soft_loss` | yes | 0.222 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.130 | 0.854 | 0.119 | 0.162 | bend/corner induced residual |
| `straight_trace` | `canonical` | `unet_topology_two_stage_refined` | no | 0.128 | 0.012 | 0 | 0 | 1.000 | n/a | n/a | 0.334 | 1.216 | 0.004 | 0.036 | no false positive |
| `finite_width_trace` | `canonical` | `unet_topology_two_stage_refined` | no | 0.118 | 0.008 | 0 | 0 | 1.000 | n/a | n/a | 0.307 | 1.003 | 0.194 | 0.193 | no false positive |
| `l_shape_trace` | `canonical` | `unet_topology_two_stage_refined` | yes | 0.297 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 0.457 | 0.408 | 0.004 | 0.177 | bend/corner induced residual |
| `no_via_background` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.178 | 0.014 | 0 | 0 | 1.000 | 1.000 | n/a | 0.941 | 0.752 | 0.265 | 0.811 | no false positive |
| `no_via_background__v01` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.372 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.005 | 0.972 | 0.197 | 0.445 | bend/corner induced residual |
| `no_via_background__v02` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.391 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.855 | 0.946 | 0.146 | 0.428 | bend/corner induced residual |
| `no_via_background__v03` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.324 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.855 | 0.940 | 0.146 | 0.419 | bend/corner induced residual |
| `no_via_background__v04` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.189 | 0.019 | 0 | 0 | 1.000 | 1.000 | n/a | 0.971 | 0.767 | 0.231 | 0.633 | no false positive |
| `no_via_background__v05` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.183 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 0.925 | 0.743 | 0.215 | 0.422 | no false positive |
| `no_via_background__v06` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.305 | 0.022 | 1 | 1 | 1.000 | 1.000 | n/a | 0.832 | 0.680 | 0.214 | 0.595 | bend/corner induced residual |
| `no_via_background__v07` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.291 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.733 | 0.680 | 0.171 | 0.333 | bend/corner induced residual |
| `no_via_background__v08` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.309 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.470 | 0.873 | 0.203 | 0.575 | bend/corner induced residual |
| `no_via_background__v09` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.574 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 1.059 | 0.822 | 0.183 | 0.493 | bend/corner induced residual |
| `no_via_background__v10` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.509 | 0.034 | 2 | 2 | 0.000 | 0.000 | n/a | 1.007 | 0.777 | 0.136 | 0.271 | bend/corner induced residual |
| `no_via_background__v11` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.260 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.388 | 0.932 | 0.176 | 0.288 | bend/corner induced residual |
| `no_via_background__v12` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.141 | 0.014 | 0 | 0 | 0.000 | 2.000 | n/a | 0.676 | 0.712 | 0.222 | 0.074 | no false positive |
| `no_via_background__v13` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.260 | 0.019 | 1 | 1 | 0.000 | 5.000 | n/a | 0.586 | 0.691 | 0.195 | 0.150 | operator mismatch |
| `no_via_background__v14` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.137 | 0.014 | 0 | 0 | 0.000 | 6.000 | n/a | 0.586 | 0.680 | 0.210 | 0.456 | no false positive |
| `no_via_background__v15` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.164 | 0.017 | 0 | 0 | 0.000 | 6.000 | n/a | 0.517 | 0.616 | 0.116 | 0.151 | no false positive |
| `no_via_background__v16` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.296 | 0.026 | 2 | 2 | 0.000 | 5.000 | n/a | 0.822 | 0.534 | 0.165 | 0.379 | operator mismatch |
| `no_via_background__v17` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.325 | 0.026 | 1 | 1 | 0.000 | 5.000 | n/a | 0.884 | 0.511 | 0.176 | 0.473 | operator mismatch |
| `no_via_background__v18` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.203 | 0.021 | 1 | 1 | 0.000 | 6.000 | n/a | 0.744 | 0.462 | 0.194 | 0.475 | operator mismatch |
| `no_via_background__v19` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.313 | 0.023 | 1 | 1 | 0.000 | 6.000 | n/a | 0.661 | 0.490 | 0.170 | 0.421 | operator mismatch |
| `no_via_background__v20` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.341 | 0.026 | 1 | 1 | 0.000 | 5.000 | n/a | 0.707 | 0.669 | 0.253 | 0.312 | operator mismatch |
| `no_via_background__v21` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.341 | 0.028 | 2 | 2 | 0.000 | 5.000 | n/a | 0.672 | 0.567 | 0.201 | 0.342 | operator mismatch |
| `no_via_background__v22` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.193 | 0.024 | 0 | 0 | 0.000 | 6.000 | n/a | 0.749 | 0.600 | 0.143 | 0.292 | no false positive |
| `no_via_background__v23` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.199 | 0.026 | 0 | 0 | 1.000 | 1.000 | n/a | 0.840 | 0.612 | 0.174 | 0.531 | no false positive |
| `no_via_background__v24` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.563 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 1.153 | 0.846 | 0.165 | 0.509 | bend/corner induced residual |
| `no_via_background__v25` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.554 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 0.938 | 0.746 | 0.194 | 0.471 | bend/corner induced residual |
| `no_via_background__v26` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.459 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 1.014 | 0.855 | 0.210 | 0.477 | bend/corner induced residual |
| `no_via_background__v27` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.462 | 0.031 | 1 | 1 | 0.000 | 0.000 | n/a | 0.973 | 0.845 | 0.171 | 0.223 | bend/corner induced residual |
| `no_via_background__v28` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.199 | 0.015 | 0 | 0 | 0.000 | 0.000 | n/a | 1.456 | 0.945 | 0.163 | 0.425 | no false positive |
| `no_via_background__v29` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.148 | 0.014 | 0 | 0 | 0.000 | 0.000 | n/a | 1.252 | 0.818 | 0.231 | 0.487 | no false positive |
| `no_via_background__v30` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.187 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.098 | 0.794 | 0.146 | 0.496 | no false positive |
| `no_via_background__v31` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.113 | 0.021 | 0 | 0 | 2.000 | 2.000 | n/a | 1.389 | 0.833 | 0.176 | 0.660 | no false positive |
| `no_via_background__v32` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.387 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.050 | 1.002 | 0.264 | 0.343 | bend/corner induced residual |
| `no_via_background__v33` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.307 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.042 | 1.020 | 0.207 | 0.574 | bend/corner induced residual |
| `no_via_background__v34` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.344 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.944 | 0.887 | 0.248 | 0.589 | bend/corner induced residual |
| `no_via_background__v35` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.252 | 0.017 | 1 | 1 | 0.000 | 0.000 | n/a | 1.001 | 0.759 | 0.209 | 0.766 | bend/corner induced residual |
| `no_via_background__v36` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.253 | 0.027 | 2 | 2 | 0.000 | 5.000 | n/a | 0.766 | 0.653 | 0.165 | 0.333 | operator mismatch |
| `no_via_background__v37` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.253 | 0.023 | 1 | 1 | 0.000 | 5.000 | n/a | 0.574 | 0.515 | 0.160 | 0.355 | operator mismatch |
| `no_via_background__v38` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.187 | 0.023 | 0 | 0 | 0.000 | 5.000 | n/a | 0.906 | 0.674 | 0.185 | 0.437 | no false positive |
| `no_via_background__v39` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.226 | 0.027 | 1 | 1 | 0.000 | 6.000 | n/a | 0.769 | 0.537 | 0.177 | 0.316 | operator mismatch |
| `no_via_background__v40` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.276 | 0.019 | 1 | 1 | 0.000 | 5.000 | n/a | 0.722 | 0.600 | 0.223 | 0.324 | operator mismatch |
| `no_via_background__v41` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.157 | 0.015 | 0 | 0 | 0.000 | 2.000 | n/a | 0.563 | 0.624 | 0.202 | 0.174 | no false positive |
| `no_via_background__v42` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.240 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 0.538 | 0.683 | 0.143 | 0.138 | bend/corner induced residual |
| `no_via_background__v43` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.171 | 0.019 | 0 | 0 | 0.000 | 0.000 | n/a | 0.604 | 0.601 | 0.179 | 0.203 | no false positive |
| `no_via_background__v44` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.191 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 0.713 | 0.668 | 0.211 | 0.503 | no false positive |
| `no_via_background__v45` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.140 | 0.016 | 0 | 0 | 0.000 | 5.000 | n/a | 0.634 | 0.678 | 0.203 | 0.129 | no false positive |
| `no_via_background__v46` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.204 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.650 | 0.664 | 0.263 | 0.588 | bend/corner induced residual |
| `no_via_background__v47` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.210 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.646 | 0.625 | 0.151 | 0.168 | bend/corner induced residual |
| `no_via_background__v48` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.133 | 0.016 | 0 | 0 | 0.000 | 5.000 | n/a | 0.917 | 1.038 | 0.135 | 0.491 | no false positive |
| `no_via_background__v49` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.329 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.846 | 0.952 | 0.197 | 0.414 | bend/corner induced residual |
| `no_via_background__v50` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.426 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 0.955 | 0.988 | 0.135 | 0.460 | bend/corner induced residual |
| `no_via_background__v51` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.197 | 0.021 | 0 | 0 | 0.000 | 0.000 | n/a | 0.894 | 0.924 | 0.109 | 0.490 | no false positive |
| `no_via_background__v52` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.424 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.442 | 0.806 | 0.234 | 0.610 | bend/corner induced residual |
| `no_via_background__v53` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.196 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.074 | 0.720 | 0.170 | 0.597 | no false positive |
| `no_via_background__v54` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.210 | 0.018 | 1 | 1 | 0.000 | 0.000 | n/a | 1.018 | 0.825 | 0.263 | 0.735 | bend/corner induced residual |
| `no_via_background__v55` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.184 | 0.020 | 0 | 0 | 0.000 | 0.000 | n/a | 0.813 | 0.679 | 0.239 | 0.546 | no false positive |
| `no_via_background__v56` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.520 | 0.032 | 1 | 1 | 0.000 | 0.000 | n/a | 0.919 | 0.773 | 0.211 | 0.797 | bend/corner induced residual |
| `no_via_background__v57` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.436 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.076 | 0.840 | 0.211 | 0.220 | bend/corner induced residual |
| `no_via_background__v58` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.569 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 0.934 | 0.720 | 0.185 | 0.651 | bend/corner induced residual |
| `no_via_background__v59` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.570 | 0.037 | 1 | 1 | 0.000 | 0.000 | n/a | 1.036 | 0.690 | 0.176 | 0.698 | bend/corner induced residual |
| `no_via_background__v60` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.245 | 0.022 | 2 | 2 | 0.000 | 0.000 | n/a | 0.643 | 0.658 | 0.221 | 0.127 | bend/corner induced residual |
| `no_via_background__v61` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.204 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.650 | 0.664 | 0.202 | 0.195 | bend/corner induced residual |
| `no_via_background__v62` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.205 | 0.018 | 1 | 1 | 0.000 | 5.000 | n/a | 0.556 | 0.655 | 0.143 | 0.127 | model hallucination |
| `no_via_background__v63` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.232 | 0.018 | 1 | 1 | 0.000 | 5.000 | n/a | 0.588 | 0.686 | 0.177 | 0.179 | operator mismatch |
| `no_via_background__v64` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.299 | 0.027 | 1 | 1 | 0.000 | 5.000 | n/a | 0.921 | 0.532 | 0.155 | 0.420 | operator mismatch |
| `no_via_background__v65` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.251 | 0.021 | 1 | 1 | 0.000 | 5.000 | n/a | 0.967 | 0.543 | 0.192 | 0.510 | operator mismatch |
| `no_via_background__v66` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.267 | 0.026 | 2 | 2 | 1.000 | 5.099 | n/a | 0.803 | 0.505 | 0.248 | 0.732 | operator mismatch |
| `no_via_background__v67` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.298 | 0.026 | 1 | 1 | 0.000 | 5.000 | n/a | 0.762 | 0.492 | 0.153 | 0.434 | operator mismatch |
| `no_via_background__v68` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.387 | 0.032 | 2 | 2 | 0.000 | 0.000 | n/a | 0.695 | 0.635 | 0.203 | 0.414 | bend/corner induced residual |
| `no_via_background__v69` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.223 | 0.025 | 1 | 1 | 0.000 | 6.000 | n/a | 0.706 | 0.594 | 0.230 | 0.296 | operator mismatch |
| `no_via_background__v70` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.289 | 0.024 | 1 | 1 | 0.000 | 5.000 | n/a | 0.664 | 0.586 | 0.143 | 0.343 | model hallucination |
| `no_via_background__v71` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.191 | 0.022 | 0 | 0 | 0.000 | 0.000 | n/a | 0.887 | 0.623 | 0.218 | 0.532 | no false positive |
| `no_via_background__v72` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.548 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 1.081 | 0.811 | 0.262 | 0.569 | bend/corner induced residual |
| `no_via_background__v73` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.520 | 0.034 | 1 | 1 | 0.000 | 0.000 | n/a | 0.930 | 0.714 | 0.205 | 0.697 | bend/corner induced residual |
| `no_via_background__v74` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.574 | 0.036 | 1 | 1 | 0.000 | 0.000 | n/a | 1.059 | 0.822 | 0.248 | 0.630 | bend/corner induced residual |
| `no_via_background__v75` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.541 | 0.033 | 1 | 1 | 0.000 | 0.000 | n/a | 0.983 | 0.769 | 0.091 | 0.227 | bend/corner induced residual |
| `no_via_background__v76` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.203 | 0.017 | 1 | 1 | 1.000 | 1.000 | n/a | 1.205 | 0.875 | 0.263 | 0.830 | bend/corner induced residual |
| `no_via_background__v77` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.177 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 0.973 | 0.705 | 0.193 | 0.531 | no false positive |
| `no_via_background__v78` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.145 | 0.016 | 0 | 0 | 1.000 | 1.000 | n/a | 0.907 | 0.746 | 0.166 | 0.455 | no false positive |
| `no_via_background__v79` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.157 | 0.015 | 0 | 0 | 1.000 | 1.000 | n/a | 0.768 | 0.683 | 0.170 | 0.471 | no false positive |
| `no_via_background__v80` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.327 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.124 | 1.120 | 0.232 | 0.399 | bend/corner induced residual |
| `no_via_background__v81` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.372 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.005 | 0.972 | 0.197 | 0.445 | bend/corner induced residual |
| `no_via_background__v82` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.391 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 0.855 | 0.946 | 0.146 | 0.428 | bend/corner induced residual |
| `no_via_background__v83` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.324 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 0.855 | 0.940 | 0.146 | 0.419 | bend/corner induced residual |
| `no_via_background__v84` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.351 | 0.029 | 2 | 2 | 0.000 | 5.000 | n/a | 0.686 | 0.684 | 0.143 | 0.327 | model hallucination |
| `no_via_background__v85` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.283 | 0.023 | 1 | 1 | 0.000 | 5.000 | n/a | 0.732 | 0.633 | 0.203 | 0.347 | operator mismatch |
| `no_via_background__v86` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.341 | 0.028 | 2 | 2 | 1.000 | 5.099 | n/a | 0.672 | 0.567 | 0.248 | 0.739 | operator mismatch |
| `no_via_background__v87` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.299 | 0.028 | 2 | 2 | 0.000 | 5.000 | n/a | 0.612 | 0.541 | 0.159 | 0.292 | operator mismatch |
| `no_via_background__v88` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.155 | 0.015 | 0 | 0 | 0.000 | 0.000 | n/a | 0.662 | 0.671 | 0.260 | 0.784 | no false positive |
| `no_via_background__v89` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.159 | 0.016 | 0 | 0 | 0.000 | 0.000 | n/a | 0.630 | 0.639 | 0.183 | 0.179 | no false positive |
| `no_via_background__v90` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.106 | 0.016 | 0 | 0 | 0.000 | 2.000 | n/a | 0.519 | 0.607 | 0.143 | 0.119 | no false positive |
| `no_via_background__v91` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.336 | 0.023 | 1 | 1 | 0.000 | 3.000 | n/a | 0.592 | 0.555 | 0.248 | 0.427 | operator mismatch |
| `no_via_background__v92` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.141 | 0.014 | 0 | 0 | 0.000 | 2.000 | n/a | 0.676 | 0.712 | 0.222 | 0.074 | no false positive |
| `no_via_background__v93` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.260 | 0.019 | 1 | 1 | 0.000 | 5.000 | n/a | 0.586 | 0.691 | 0.195 | 0.150 | operator mismatch |
| `no_via_background__v94` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.137 | 0.014 | 0 | 0 | 0.000 | 6.000 | n/a | 0.586 | 0.680 | 0.210 | 0.456 | no false positive |
| `no_via_background__v95` | `no_via_background` | `unet_topology_two_stage_refined` | no | 0.154 | 0.017 | 0 | 0 | 0.000 | 6.000 | n/a | 0.515 | 0.603 | 0.182 | 0.203 | no false positive |
| `no_via_background__v96` | `no_via_background` | `unet_topology_two_stage_refined` | yes | 0.338 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.134 | 1.004 | 0.155 | 0.318 | bend/corner induced residual |
| `bend_artifact_trace` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.291 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 1.012 | 0.768 | 0.217 | 0.295 | bend/corner induced residual |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.235 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 1.110 | 0.711 | 0.176 | 0.554 | bend/corner induced residual |
| `bend_artifact_trace__v02` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.148 | 0.016 | 0 | 0 | 1.000 | 1.000 | n/a | 1.440 | 0.791 | 0.190 | 0.337 | no false positive |
| `bend_artifact_trace__v03` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.218 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 1.055 | 0.742 | 0.146 | 0.247 | bend/corner induced residual |
| `bend_artifact_trace__v04` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.272 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 1.203 | 0.575 | 0.196 | 0.576 | bend/corner induced residual |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.269 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.147 | 0.724 | 0.229 | 0.507 | bend/corner induced residual |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.277 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.142 | 0.523 | 0.134 | 0.682 | bend/corner induced residual |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.216 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 0.886 | 0.505 | 0.207 | 0.670 | bend/corner induced residual |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.354 | 0.030 | 3 | 2 | 0.000 | 0.000 | n/a | 0.993 | 0.707 | 0.173 | 0.337 | bend/corner induced residual |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.250 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 1.107 | 0.725 | 0.236 | 0.340 | bend/corner induced residual |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.345 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 0.884 | 0.586 | 0.187 | 0.453 | bend/corner induced residual |
| `bend_artifact_trace__v11` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.440 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.081 | 0.601 | 0.150 | 0.379 | bend/corner induced residual |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.326 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.888 | 0.710 | 0.223 | 0.234 | bend/corner induced residual |
| `bend_artifact_trace__v13` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.337 | 0.027 | 1 | 1 | 1.000 | 1.000 | n/a | 0.708 | 0.659 | 0.238 | 0.578 | bend/corner induced residual |
| `bend_artifact_trace__v14` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.120 | 0.014 | 0 | 0 | 1.000 | 4.000 | n/a | 0.731 | 0.551 | 0.162 | 0.385 | no false positive |
| `bend_artifact_trace__v15` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.135 | 0.018 | 0 | 0 | 0.000 | 2.000 | n/a | 0.751 | 0.607 | 0.164 | 0.271 | no false positive |
| `bend_artifact_trace__v16` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.274 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 0.813 | 0.637 | 0.214 | 0.493 | bend/corner induced residual |
| `bend_artifact_trace__v17` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.239 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.004 | 0.652 | 0.219 | 0.550 | bend/corner induced residual |
| `bend_artifact_trace__v18` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.389 | 0.035 | 2 | 2 | 0.000 | 3.000 | n/a | 0.725 | 0.594 | 0.167 | 0.358 | operator mismatch |
| `bend_artifact_trace__v19` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.316 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 0.967 | 0.632 | 0.204 | 0.545 | bend/corner induced residual |
| `bend_artifact_trace__v20` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.246 | 0.027 | 1 | 1 | 1.000 | 2.236 | n/a | 0.853 | 0.736 | 0.245 | 0.461 | detector threshold sensitivity |
| `bend_artifact_trace__v21` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.297 | 0.030 | 1 | 1 | 0.000 | 2.000 | n/a | 1.056 | 0.617 | 0.216 | 0.463 | bend/corner induced residual |
| `bend_artifact_trace__v22` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.218 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 0.778 | 0.542 | 0.233 | 0.512 | bend/corner induced residual |
| `bend_artifact_trace__v23` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.250 | 0.026 | 2 | 2 | 0.000 | 2.000 | n/a | 0.758 | 0.614 | 0.218 | 0.482 | bend/corner induced residual |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.282 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.142 | 0.790 | 0.214 | 0.558 | bend/corner induced residual |
| `bend_artifact_trace__v25` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.088 | 0.012 | 0 | 0 | 0.000 | 0.000 | n/a | 1.325 | 0.615 | 0.233 | 0.536 | no false positive |
| `bend_artifact_trace__v26` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.402 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.189 | 0.652 | 0.162 | 0.563 | bend/corner induced residual |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.299 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 1.078 | 0.683 | 0.177 | 0.256 | bend/corner induced residual |
| `bend_artifact_trace__v28` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.227 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.964 | 0.717 | 0.222 | 0.723 | bend/corner induced residual |
| `bend_artifact_trace__v29` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.311 | 0.025 | 2 | 2 | 0.000 | 0.000 | n/a | 0.856 | 0.625 | 0.202 | 0.583 | bend/corner induced residual |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.271 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 1.470 | 0.697 | 0.154 | 0.631 | bend/corner induced residual |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.299 | 0.025 | 1 | 1 | 0.000 | 0.000 | n/a | 1.098 | 0.604 | 0.150 | 0.589 | bend/corner induced residual |
| `bend_artifact_trace__v32` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.349 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 1.286 | 0.876 | 0.229 | 0.174 | bend/corner induced residual |
| `bend_artifact_trace__v33` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.195 | 0.019 | 0 | 0 | 0.000 | 0.000 | n/a | 1.070 | 0.772 | 0.158 | 0.207 | no false positive |
| `bend_artifact_trace__v34` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.313 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.983 | 0.819 | 0.247 | 0.390 | bend/corner induced residual |
| `bend_artifact_trace__v35` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.431 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.139 | 0.713 | 0.237 | 0.472 | bend/corner induced residual |
| `bend_artifact_trace__v36` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.352 | 0.031 | 3 | 3 | 0.000 | 3.000 | n/a | 1.029 | 0.659 | 0.214 | 0.544 | detector threshold sensitivity |
| `bend_artifact_trace__v37` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.231 | 0.020 | 1 | 1 | 0.000 | 3.000 | n/a | 0.845 | 0.539 | 0.240 | 0.460 | operator mismatch |
| `bend_artifact_trace__v38` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.241 | 0.026 | 1 | 1 | 0.000 | 3.000 | n/a | 0.840 | 0.634 | 0.219 | 0.502 | detector threshold sensitivity |
| `bend_artifact_trace__v39` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.419 | 0.034 | 1 | 1 | 0.000 | 3.000 | n/a | 0.715 | 0.504 | 0.113 | 0.405 | model hallucination |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.242 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 0.906 | 0.598 | 0.222 | 0.518 | bend/corner induced residual |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.190 | 0.023 | 0 | 0 | 0.000 | 0.000 | n/a | 1.060 | 0.639 | 0.234 | 0.406 | no false positive |
| `bend_artifact_trace__v42` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.122 | 0.015 | 0 | 0 | 0.000 | 0.000 | n/a | 0.668 | 0.592 | 0.210 | 0.244 | no false positive |
| `bend_artifact_trace__v43` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.207 | 0.020 | 1 | 1 | 0.000 | 0.000 | n/a | 0.693 | 0.596 | 0.202 | 0.295 | bend/corner induced residual |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.386 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 0.764 | 0.495 | 0.213 | 0.481 | bend/corner induced residual |
| `bend_artifact_trace__v45` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.125 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 0.763 | 0.597 | 0.178 | 0.391 | no false positive |
| `bend_artifact_trace__v46` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.190 | 0.022 | 0 | 0 | 0.000 | 0.000 | n/a | 0.631 | 0.538 | 0.248 | 0.614 | no false positive |
| `bend_artifact_trace__v47` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.194 | 0.024 | 0 | 0 | 0.000 | 0.000 | n/a | 0.789 | 0.557 | 0.189 | 0.355 | no false positive |
| `bend_artifact_trace__v48` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.212 | 0.022 | 2 | 2 | 0.000 | 0.000 | n/a | 1.084 | 0.896 | 0.159 | 0.172 | bend/corner induced residual |
| `bend_artifact_trace__v49` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.193 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.055 | 0.790 | 0.234 | 0.273 | no false positive |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.176 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.081 | 0.677 | 0.188 | 0.505 | no false positive |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.242 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.030 | 0.739 | 0.152 | 0.471 | bend/corner induced residual |
| `bend_artifact_trace__v52` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.387 | 0.028 | 2 | 2 | 0.000 | 0.000 | n/a | 1.038 | 0.803 | 0.252 | 0.454 | bend/corner induced residual |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.388 | 0.029 | 1 | 1 | 0.000 | 0.000 | n/a | 1.034 | 0.683 | 0.225 | 0.542 | bend/corner induced residual |
| `bend_artifact_trace__v54` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.274 | 0.023 | 2 | 2 | 0.000 | 0.000 | n/a | 1.210 | 0.592 | 0.248 | 0.629 | bend/corner induced residual |
| `bend_artifact_trace__v55` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.355 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.821 | 0.568 | 0.256 | 0.400 | bend/corner induced residual |
| `bend_artifact_trace__v56` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.529 | 0.035 | 1 | 1 | 0.000 | 0.000 | n/a | 1.037 | 0.639 | 0.213 | 0.520 | bend/corner induced residual |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.341 | 0.027 | 2 | 2 | 0.000 | 0.000 | n/a | 0.969 | 0.601 | 0.186 | 0.294 | bend/corner induced residual |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.393 | 0.030 | 2 | 2 | 0.000 | 0.000 | n/a | 1.113 | 0.746 | 0.253 | 0.309 | bend/corner induced residual |
| `bend_artifact_trace__v59` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.186 | 0.019 | 0 | 0 | 1.000 | 1.000 | n/a | 1.047 | 0.637 | 0.180 | 0.631 | no false positive |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.178 | 0.020 | 0 | 0 | 0.000 | 0.000 | n/a | 0.755 | 0.665 | 0.194 | 0.269 | no false positive |
| `bend_artifact_trace__v61` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.224 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.653 | 0.598 | 0.234 | 0.322 | bend/corner induced residual |
| `bend_artifact_trace__v62` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.163 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 0.828 | 0.519 | 0.233 | 0.336 | no false positive |
| `bend_artifact_trace__v63` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.134 | 0.018 | 0 | 0 | 1.000 | 1.000 | n/a | 0.801 | 0.544 | 0.222 | 0.451 | no false positive |
| `bend_artifact_trace__v64` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.229 | 0.025 | 2 | 2 | 0.000 | 0.000 | n/a | 1.036 | 0.638 | 0.162 | 0.496 | bend/corner induced residual |
| `bend_artifact_trace__v65` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.327 | 0.029 | 2 | 2 | 0.000 | 3.000 | n/a | 1.049 | 0.671 | 0.211 | 0.440 | operator mismatch |
| `bend_artifact_trace__v66` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.246 | 0.027 | 1 | 1 | 0.000 | 1.000 | n/a | 0.874 | 0.601 | 0.247 | 0.444 | bend/corner induced residual |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.336 | 0.028 | 1 | 1 | 0.000 | 0.000 | n/a | 0.940 | 0.628 | 0.192 | 0.590 | bend/corner induced residual |
| `bend_artifact_trace__v68` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.275 | 0.026 | 1 | 1 | 1.000 | 3.000 | n/a | 0.908 | 0.635 | 0.173 | 0.576 | detector threshold sensitivity |
| `bend_artifact_trace__v69` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.422 | 0.033 | 1 | 1 | 0.000 | 3.000 | n/a | 0.832 | 0.546 | 0.162 | 0.375 | operator mismatch |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.205 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.055 | 0.673 | 0.210 | 0.390 | bend/corner induced residual |
| `bend_artifact_trace__v71` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.418 | 0.032 | 2 | 2 | 0.000 | 3.000 | n/a | 1.106 | 0.633 | 0.251 | 0.474 | detector threshold sensitivity |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.346 | 0.023 | 1 | 1 | 0.000 | 0.000 | n/a | 0.832 | 0.684 | 0.218 | 0.270 | bend/corner induced residual |
| `bend_artifact_trace__v73` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.392 | 0.034 | 2 | 1 | 0.000 | 0.000 | n/a | 0.821 | 0.587 | 0.185 | 0.597 | bend/corner induced residual |
| `bend_artifact_trace__v74` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.386 | 0.029 | 2 | 2 | 1.000 | 1.000 | n/a | 1.372 | 0.742 | 0.247 | 0.497 | bend/corner induced residual |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.412 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 1.055 | 0.662 | 0.211 | 0.334 | bend/corner induced residual |
| `bend_artifact_trace__v76` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.233 | 0.024 | 2 | 2 | 0.000 | 0.000 | n/a | 1.024 | 0.593 | 0.257 | 0.569 | bend/corner induced residual |
| `bend_artifact_trace__v77` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.155 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 1.410 | 0.700 | 0.194 | 0.759 | no false positive |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.380 | 0.027 | 1 | 1 | 0.000 | 0.000 | n/a | 1.022 | 0.598 | 0.183 | 0.762 | bend/corner induced residual |
| `bend_artifact_trace__v79` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.338 | 0.029 | 2 | 2 | 0.000 | 0.000 | n/a | 1.056 | 0.581 | 0.204 | 0.757 | bend/corner induced residual |
| `bend_artifact_trace__v80` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.348 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 0.938 | 0.859 | 0.252 | 0.286 | bend/corner induced residual |
| `bend_artifact_trace__v81` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.252 | 0.023 | 2 | 2 | 0.000 | 0.000 | n/a | 1.066 | 0.698 | 0.143 | 0.457 | bend/corner induced residual |
| `bend_artifact_trace__v82` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.253 | 0.021 | 1 | 1 | 0.000 | 0.000 | n/a | 1.107 | 0.845 | 0.206 | 0.495 | bend/corner induced residual |
| `bend_artifact_trace__v83` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.171 | 0.019 | 0 | 0 | 1.000 | 1.000 | n/a | 1.326 | 0.772 | 0.191 | 0.355 | no false positive |
| `bend_artifact_trace__v84` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.478 | 0.034 | 1 | 1 | 0.000 | 3.000 | n/a | 0.939 | 0.663 | 0.136 | 0.317 | model hallucination |
| `bend_artifact_trace__v85` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.246 | 0.024 | 1 | 1 | 1.000 | 3.162 | n/a | 0.982 | 0.698 | 0.178 | 0.435 | detector threshold sensitivity |
| `bend_artifact_trace__v86` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.363 | 0.027 | 1 | 1 | 0.000 | 2.000 | n/a | 1.047 | 0.613 | 0.247 | 0.514 | bend/corner induced residual |
| `bend_artifact_trace__v87` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.209 | 0.026 | 1 | 1 | 0.000 | 0.000 | n/a | 0.823 | 0.495 | 0.159 | 0.455 | bend/corner induced residual |
| `bend_artifact_trace__v88` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.211 | 0.019 | 1 | 1 | 1.000 | 1.000 | n/a | 0.905 | 0.576 | 0.256 | 0.759 | bend/corner induced residual |
| `bend_artifact_trace__v89` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.160 | 0.018 | 0 | 0 | 0.000 | 0.000 | n/a | 0.917 | 0.627 | 0.236 | 0.481 | no false positive |
| `bend_artifact_trace__v90` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.174 | 0.020 | 0 | 0 | 0.000 | 3.000 | n/a | 0.844 | 0.612 | 0.233 | 0.551 | no false positive |
| `bend_artifact_trace__v91` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.173 | 0.020 | 0 | 0 | 0.000 | 0.000 | n/a | 0.855 | 0.698 | 0.246 | 0.357 | no false positive |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.326 | 0.022 | 1 | 1 | 0.000 | 0.000 | n/a | 0.888 | 0.710 | 0.223 | 0.234 | bend/corner induced residual |
| `bend_artifact_trace__v93` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.336 | 0.027 | 1 | 1 | 1.000 | 1.000 | n/a | 0.691 | 0.633 | 0.223 | 0.562 | bend/corner induced residual |
| `bend_artifact_trace__v94` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.129 | 0.017 | 0 | 0 | 0.000 | 0.000 | n/a | 0.687 | 0.541 | 0.182 | 0.247 | no false positive |
| `bend_artifact_trace__v95` | `bend_artifact` | `unet_topology_two_stage_refined` | no | 0.135 | 0.018 | 0 | 0 | 0.000 | 2.000 | n/a | 0.751 | 0.607 | 0.164 | 0.271 | no false positive |
| `bend_artifact_trace__v96` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.321 | 0.026 | 2 | 2 | 0.000 | 0.000 | n/a | 1.071 | 0.791 | 0.162 | 0.250 | bend/corner induced residual |
| `bend_artifact_trace__v97` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.357 | 0.024 | 1 | 1 | 0.000 | 0.000 | n/a | 1.104 | 0.903 | 0.217 | 0.222 | bend/corner induced residual |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.232 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.034 | 0.828 | 0.208 | 0.311 | bend/corner induced residual |
| `bend_artifact_trace__v99` | `bend_artifact` | `unet_topology_two_stage_refined` | yes | 0.202 | 0.019 | 1 | 1 | 0.000 | 0.000 | n/a | 1.082 | 0.851 | 0.119 | 0.162 | bend/corner induced residual |

Interpretation: these rows classify PyPEEC no-via false positives after inference. They do not tune a PyPEEC-specific detector threshold.
