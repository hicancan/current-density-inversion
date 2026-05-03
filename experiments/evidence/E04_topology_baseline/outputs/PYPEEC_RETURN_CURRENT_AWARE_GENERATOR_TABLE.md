# Return-Current-Aware Generator Diagnostic

- enabled: `True`
- mode: `oracle_signal_plus_scalar_return_current_generator`
- used for model prediction: `False`
- boundary: Oracle diagnostic only: it uses known return-current labels to test whether a signal-plus-return-current basis can explain PyPEEC return-path fields. It is not an inference model and does not alter predictions.

## Summary

- return-path cases: `100`
- mean centerline residual: `1.942`
- mean return-current-aware residual: `1.699`
- mean improvement over centerline: `0.243`
- median fitted return alpha: `1.436`

## Case Rows

| case | type | alpha | centerline B | signal-only B | signal+alpha return B | shape B | scalar fit | improvement |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `trace_with_return_path` | `return_path` | 1.372 | 1.376 | 2.897 | 1.174 | 0.503 | 0.449 | 0.202 |
| `trace_with_return_path__v01` | `return_path` | 1.450 | 2.308 | 4.159 | 2.013 | 0.766 | 0.257 | 0.295 |
| `trace_with_return_path__v02` | `return_path` | 1.445 | 2.331 | 4.203 | 2.038 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v03` | `return_path` | 1.446 | 2.334 | 4.205 | 2.040 | 0.782 | 0.249 | 0.294 |
| `trace_with_return_path__v04` | `return_path` | 1.381 | 1.334 | 2.782 | 1.136 | 0.482 | 0.460 | 0.198 |
| `trace_with_return_path__v05` | `return_path` | 1.375 | 1.370 | 2.875 | 1.168 | 0.496 | 0.451 | 0.202 |
| `trace_with_return_path__v06` | `return_path` | 1.434 | 2.172 | 3.937 | 1.905 | 0.754 | 0.273 | 0.267 |
| `trace_with_return_path__v07` | `return_path` | 1.419 | 1.801 | 3.213 | 1.603 | 0.820 | 0.294 | 0.199 |
| `trace_with_return_path__v08` | `return_path` | 1.445 | 1.880 | 3.300 | 1.663 | 0.829 | 0.280 | 0.217 |
| `trace_with_return_path__v09` | `return_path` | 1.450 | 2.308 | 4.159 | 2.013 | 0.766 | 0.257 | 0.295 |
| `trace_with_return_path__v10` | `return_path` | 1.447 | 2.332 | 4.218 | 2.033 | 0.771 | 0.253 | 0.298 |
| `trace_with_return_path__v11` | `return_path` | 1.442 | 2.337 | 4.247 | 2.039 | 0.772 | 0.252 | 0.298 |
| `trace_with_return_path__v12` | `return_path` | 1.457 | 2.314 | 4.124 | 2.021 | 0.776 | 0.253 | 0.293 |
| `trace_with_return_path__v13` | `return_path` | 1.438 | 1.887 | 3.334 | 1.670 | 0.829 | 0.278 | 0.217 |
| `trace_with_return_path__v14` | `return_path` | 1.422 | 1.783 | 3.159 | 1.589 | 0.821 | 0.296 | 0.195 |
| `trace_with_return_path__v15` | `return_path` | 1.443 | 2.352 | 4.257 | 2.056 | 0.784 | 0.246 | 0.297 |
| `trace_with_return_path__v16` | `return_path` | 1.362 | 1.233 | 2.621 | 1.056 | 0.462 | 0.483 | 0.177 |
| `trace_with_return_path__v17` | `return_path` | 1.386 | 1.706 | 3.167 | 1.520 | 0.716 | 0.342 | 0.186 |
| `trace_with_return_path__v18` | `return_path` | 1.445 | 2.317 | 4.195 | 2.022 | 0.770 | 0.255 | 0.295 |
| `trace_with_return_path__v19` | `return_path` | 1.434 | 1.894 | 3.363 | 1.677 | 0.831 | 0.276 | 0.218 |
| `trace_with_return_path__v20` | `return_path` | 1.394 | 1.713 | 3.156 | 1.525 | 0.716 | 0.341 | 0.188 |
| `trace_with_return_path__v21` | `return_path` | 1.361 | 1.256 | 2.680 | 1.074 | 0.467 | 0.478 | 0.182 |
| `trace_with_return_path__v22` | `return_path` | 1.446 | 2.334 | 4.205 | 2.040 | 0.782 | 0.249 | 0.294 |
| `trace_with_return_path__v23` | `return_path` | 1.419 | 1.801 | 3.213 | 1.603 | 0.820 | 0.294 | 0.199 |
| `trace_with_return_path__v24` | `return_path` | 1.362 | 1.233 | 2.621 | 1.056 | 0.462 | 0.483 | 0.177 |
| `trace_with_return_path__v25` | `return_path` | 1.391 | 1.475 | 3.025 | 1.255 | 0.532 | 0.427 | 0.219 |
| `trace_with_return_path__v26` | `return_path` | 1.422 | 1.783 | 3.159 | 1.589 | 0.821 | 0.296 | 0.195 |
| `trace_with_return_path__v27` | `return_path` | 1.444 | 2.315 | 4.194 | 2.021 | 0.767 | 0.255 | 0.295 |
| `trace_with_return_path__v28` | `return_path` | 1.428 | 1.785 | 3.135 | 1.591 | 0.823 | 0.295 | 0.195 |
| `trace_with_return_path__v29` | `return_path` | 1.425 | 1.801 | 3.191 | 1.603 | 0.821 | 0.293 | 0.199 |
| `trace_with_return_path__v30` | `return_path` | 1.444 | 2.315 | 4.194 | 2.021 | 0.767 | 0.255 | 0.295 |
| `trace_with_return_path__v31` | `return_path` | 1.442 | 2.337 | 4.247 | 2.039 | 0.772 | 0.252 | 0.298 |
| `trace_with_return_path__v32` | `return_path` | 1.457 | 2.314 | 4.124 | 2.021 | 0.776 | 0.253 | 0.293 |
| `trace_with_return_path__v33` | `return_path` | 1.436 | 2.199 | 3.967 | 1.930 | 0.765 | 0.267 | 0.269 |
| `trace_with_return_path__v34` | `return_path` | 1.375 | 1.370 | 2.875 | 1.168 | 0.496 | 0.451 | 0.202 |
| `trace_with_return_path__v35` | `return_path` | 1.355 | 1.244 | 2.693 | 1.062 | 0.452 | 0.481 | 0.182 |
| `trace_with_return_path__v36` | `return_path` | 1.364 | 1.245 | 2.637 | 1.066 | 0.467 | 0.480 | 0.179 |
| `trace_with_return_path__v37` | `return_path` | 1.450 | 2.326 | 4.170 | 2.032 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v38` | `return_path` | 1.434 | 1.904 | 3.382 | 1.685 | 0.831 | 0.275 | 0.220 |
| `trace_with_return_path__v39` | `return_path` | 1.445 | 2.317 | 4.195 | 2.022 | 0.770 | 0.255 | 0.295 |
| `trace_with_return_path__v40` | `return_path` | 1.458 | 2.319 | 4.128 | 2.025 | 0.779 | 0.251 | 0.294 |
| `trace_with_return_path__v41` | `return_path` | 1.377 | 1.350 | 2.819 | 1.152 | 0.498 | 0.455 | 0.198 |
| `trace_with_return_path__v42` | `return_path` | 1.445 | 2.331 | 4.203 | 2.038 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v43` | `return_path` | 1.433 | 1.892 | 3.362 | 1.675 | 0.830 | 0.277 | 0.217 |
| `trace_with_return_path__v44` | `return_path` | 1.441 | 1.908 | 3.370 | 1.686 | 0.829 | 0.276 | 0.222 |
| `trace_with_return_path__v45` | `return_path` | 1.450 | 2.326 | 4.170 | 2.032 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v46` | `return_path` | 1.374 | 1.362 | 2.861 | 1.161 | 0.497 | 0.453 | 0.201 |
| `trace_with_return_path__v47` | `return_path` | 1.383 | 1.713 | 3.196 | 1.526 | 0.719 | 0.340 | 0.187 |
| `trace_with_return_path__v48` | `return_path` | 1.457 | 2.299 | 4.115 | 2.004 | 0.765 | 0.258 | 0.295 |
| `trace_with_return_path__v49` | `return_path` | 1.438 | 1.887 | 3.334 | 1.670 | 0.829 | 0.278 | 0.217 |
| `trace_with_return_path__v50` | `return_path` | 1.447 | 2.332 | 4.218 | 2.033 | 0.771 | 0.253 | 0.298 |
| `trace_with_return_path__v51` | `return_path` | 1.442 | 2.337 | 4.247 | 2.039 | 0.772 | 0.252 | 0.298 |
| `trace_with_return_path__v52` | `return_path` | 1.458 | 2.319 | 4.128 | 2.025 | 0.779 | 0.251 | 0.294 |
| `trace_with_return_path__v53` | `return_path` | 1.450 | 2.326 | 4.170 | 2.032 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v54` | `return_path` | 1.374 | 1.362 | 2.861 | 1.161 | 0.497 | 0.453 | 0.201 |
| `trace_with_return_path__v55` | `return_path` | 1.371 | 1.345 | 2.839 | 1.146 | 0.486 | 0.457 | 0.198 |
| `trace_with_return_path__v56` | `return_path` | 1.441 | 1.908 | 3.370 | 1.686 | 0.829 | 0.276 | 0.222 |
| `trace_with_return_path__v57` | `return_path` | 1.446 | 2.330 | 4.217 | 2.033 | 0.769 | 0.254 | 0.298 |
| `trace_with_return_path__v58` | `return_path` | 1.434 | 1.904 | 3.382 | 1.685 | 0.831 | 0.275 | 0.220 |
| `trace_with_return_path__v59` | `return_path` | 1.419 | 1.806 | 3.216 | 1.607 | 0.822 | 0.292 | 0.198 |
| `trace_with_return_path__v60` | `return_path` | 1.458 | 2.319 | 4.128 | 2.025 | 0.779 | 0.251 | 0.294 |
| `trace_with_return_path__v61` | `return_path` | 1.377 | 1.350 | 2.819 | 1.152 | 0.498 | 0.455 | 0.198 |
| `trace_with_return_path__v62` | `return_path` | 1.384 | 1.723 | 3.216 | 1.535 | 0.718 | 0.339 | 0.188 |
| `trace_with_return_path__v63` | `return_path` | 1.444 | 2.315 | 4.194 | 2.021 | 0.767 | 0.255 | 0.295 |
| `trace_with_return_path__v64` | `return_path` | 1.441 | 1.908 | 3.370 | 1.686 | 0.829 | 0.276 | 0.222 |
| `trace_with_return_path__v65` | `return_path` | 1.389 | 1.721 | 3.190 | 1.532 | 0.719 | 0.339 | 0.189 |
| `trace_with_return_path__v66` | `return_path` | 1.375 | 1.370 | 2.875 | 1.168 | 0.496 | 0.451 | 0.202 |
| `trace_with_return_path__v67` | `return_path` | 1.431 | 2.201 | 3.994 | 1.933 | 0.764 | 0.266 | 0.268 |
| `trace_with_return_path__v68` | `return_path` | 1.445 | 1.880 | 3.300 | 1.663 | 0.829 | 0.280 | 0.217 |
| `trace_with_return_path__v69` | `return_path` | 1.436 | 2.186 | 3.959 | 1.917 | 0.756 | 0.271 | 0.270 |
| `trace_with_return_path__v70` | `return_path` | 1.445 | 2.331 | 4.203 | 2.038 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v71` | `return_path` | 1.371 | 1.345 | 2.839 | 1.146 | 0.486 | 0.457 | 0.198 |
| `trace_with_return_path__v72` | `return_path` | 1.457 | 2.314 | 4.124 | 2.021 | 0.776 | 0.253 | 0.293 |
| `trace_with_return_path__v73` | `return_path` | 1.436 | 2.199 | 3.967 | 1.930 | 0.765 | 0.267 | 0.269 |
| `trace_with_return_path__v74` | `return_path` | 1.375 | 1.370 | 2.875 | 1.168 | 0.496 | 0.451 | 0.202 |
| `trace_with_return_path__v75` | `return_path` | 1.355 | 1.244 | 2.693 | 1.062 | 0.452 | 0.481 | 0.182 |
| `trace_with_return_path__v76` | `return_path` | 1.441 | 1.908 | 3.370 | 1.686 | 0.829 | 0.276 | 0.222 |
| `trace_with_return_path__v77` | `return_path` | 1.449 | 2.008 | 3.549 | 1.767 | 0.842 | 0.258 | 0.241 |
| `trace_with_return_path__v78` | `return_path` | 1.446 | 2.330 | 4.217 | 2.033 | 0.769 | 0.254 | 0.298 |
| `trace_with_return_path__v79` | `return_path` | 1.434 | 1.894 | 3.363 | 1.677 | 0.831 | 0.276 | 0.218 |
| `trace_with_return_path__v80` | `return_path` | 1.457 | 2.299 | 4.115 | 2.004 | 0.765 | 0.258 | 0.295 |
| `trace_with_return_path__v81` | `return_path` | 1.450 | 2.308 | 4.159 | 2.013 | 0.766 | 0.257 | 0.295 |
| `trace_with_return_path__v82` | `return_path` | 1.445 | 2.331 | 4.203 | 2.038 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v83` | `return_path` | 1.446 | 2.334 | 4.205 | 2.040 | 0.782 | 0.249 | 0.294 |
| `trace_with_return_path__v84` | `return_path` | 1.451 | 2.324 | 4.184 | 2.026 | 0.768 | 0.255 | 0.298 |
| `trace_with_return_path__v85` | `return_path` | 1.450 | 2.326 | 4.170 | 2.032 | 0.779 | 0.250 | 0.293 |
| `trace_with_return_path__v86` | `return_path` | 1.375 | 1.370 | 2.875 | 1.168 | 0.496 | 0.451 | 0.202 |
| `trace_with_return_path__v87` | `return_path` | 1.431 | 2.201 | 3.994 | 1.933 | 0.764 | 0.266 | 0.268 |
| `trace_with_return_path__v88` | `return_path` | 1.428 | 1.785 | 3.135 | 1.591 | 0.823 | 0.295 | 0.195 |
| `trace_with_return_path__v89` | `return_path` | 1.438 | 1.887 | 3.334 | 1.670 | 0.829 | 0.278 | 0.217 |
| `trace_with_return_path__v90` | `return_path` | 1.446 | 2.334 | 4.205 | 2.040 | 0.782 | 0.249 | 0.294 |
| `trace_with_return_path__v91` | `return_path` | 1.355 | 1.244 | 2.693 | 1.062 | 0.452 | 0.481 | 0.182 |
| `trace_with_return_path__v92` | `return_path` | 1.394 | 1.713 | 3.156 | 1.525 | 0.716 | 0.341 | 0.188 |
| `trace_with_return_path__v93` | `return_path` | 1.437 | 2.191 | 3.965 | 1.921 | 0.758 | 0.270 | 0.271 |
| `trace_with_return_path__v94` | `return_path` | 1.422 | 1.783 | 3.159 | 1.589 | 0.821 | 0.296 | 0.195 |
| `trace_with_return_path__v95` | `return_path` | 1.382 | 1.739 | 3.255 | 1.548 | 0.723 | 0.335 | 0.191 |
| `trace_with_return_path__v96` | `return_path` | 1.451 | 2.324 | 4.184 | 2.026 | 0.768 | 0.255 | 0.298 |
| `trace_with_return_path__v97` | `return_path` | 1.435 | 1.912 | 3.396 | 1.691 | 0.831 | 0.274 | 0.221 |
| `trace_with_return_path__v98` | `return_path` | 1.434 | 1.904 | 3.382 | 1.685 | 0.831 | 0.275 | 0.220 |
| `trace_with_return_path__v99` | `return_path` | 1.430 | 2.190 | 3.988 | 1.921 | 0.756 | 0.270 | 0.269 |

Interpretation: this table asks whether an explicit `signal current + scalar return current` basis can explain PyPEEC return-path fields. It is an oracle diagnostic, not a deployed inference head.
