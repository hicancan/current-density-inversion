# Null-Via Uncertainty And Refusal Diagnostics

- enabled: `True`
- boundary: Refusal labels are diagnostic confidence categories. They do not change the reported frozen model predictions or choose PyPEEC thresholds.

## Summary

| model | rows | high-conf via rate | no-via high-conf false alarm | true-via refusal/low-conf | ambiguous/refusal | mean uncertainty |
|---|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 400 | 0.050 | 0.085 | 0.985 | 0.578 | 0.746 |
| `unet_topology_soft_loss` | 400 | 0.045 | 0.090 | 1.000 | 0.672 | 0.747 |
| `unet_topology_two_stage_refined` | 400 | 0.077 | 0.150 | 0.995 | 0.427 | 0.729 |

## Highest-Uncertainty Rows

| case | type | model | true via | decision | uncertainty | margin | return evidence | selected gate accepted |
|---|---|---|---:|---|---:|---:|---:|---:|
| `two_layer_route_with_via__v31` | `l1_jog` | `unet_no_topology` | yes | `probable_artifact` | 0.998 | -0.002 | 0.003 | no |
| `trace_with_return_path__v01` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.998 | -0.002 | 1.000 | yes |
| `trace_with_return_path__v81` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.998 | -0.002 | 1.000 | yes |
| `trace_with_return_path__v08` | `return_path` | `unet_no_topology` | yes | `probable_artifact` | 0.998 | -0.002 | 0.500 | no |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.998 | -0.002 | 0.001 | no |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.997 | -0.003 | 0.000 | yes |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.997 | 0.003 | 0.000 | yes |
| `dense_via_background__v10` | `dense_via_background` | `unet_no_topology` | yes | `low_confidence_residual` | 0.997 | 0.003 | 0.000 | yes |
| `via_pair` | `canonical` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.996 | -0.004 | 1.000 | yes |
| `finite_width_trace` | `canonical` | `unet_no_topology` | no | `no_candidate` | 0.996 | -0.004 | 0.000 | no |
| `trace_with_return_path__v41` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.993 | -0.007 | 1.000 | yes |
| `trace_with_return_path__v61` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.993 | -0.007 | 1.000 | yes |
| `straight_trace` | `canonical` | `unet_no_topology` | no | `no_candidate` | 0.991 | -0.009 | 0.000 | no |
| `no_via_background__v50` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.991 | 0.009 | 0.000 | yes |
| `bend_artifact_trace__v35` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.989 | 0.011 | 0.000 | yes |
| `trace_with_return_path__v28` | `return_path` | `unet_topology_two_stage_refined` | yes | `no_candidate` | 0.989 | -0.011 | 0.500 | no |
| `no_via_background__v08` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.988 | -0.012 | 7.436e-04 | no |
| `dense_via_background__v30` | `dense_via_background` | `unet_topology_soft_loss` | yes | `low_confidence_residual` | 0.988 | 0.012 | 0.505 | no |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.988 | -0.012 | 1.537e-04 | no |
| `dense_via_background__v25` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `low_confidence_residual` | 0.988 | 0.012 | 0.001 | no |
| `l_shape_trace` | `canonical` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.988 | -0.013 | 0.002 | no |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.987 | -0.013 | 0.000 | yes |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.987 | -0.013 | 0.000 | yes |
| `no_via_background__v68` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.987 | 0.014 | 0.000 | yes |
| `bend_artifact_trace__v26` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.986 | 0.014 | 0.001 | no |
| `trace_with_return_path__v01` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.986 | 0.015 | 1.000 | yes |
| `trace_with_return_path__v81` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.986 | 0.015 | 1.000 | yes |
| `no_via_background__v01` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.986 | -0.015 | 0.000 | yes |
| `no_via_background__v81` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.986 | -0.015 | 0.000 | yes |
| `no_via_background__v35` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.985 | 0.015 | 7.723e-04 | no |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.985 | -0.015 | 0.000 | yes |
| `bend_artifact_trace__v33` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.985 | -0.016 | 0.000 | yes |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.984 | 0.016 | 0.000 | yes |
| `dense_via_background__v08` | `dense_via_background` | `unet_topology_soft_loss` | yes | `low_confidence_residual` | 0.984 | 0.017 | 0.003 | no |
| `no_via_background__v77` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.984 | 0.017 | 0.001 | no |
| `bend_artifact_trace__v57` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.983 | -0.017 | 0.000 | yes |
| `two_layer_route_with_via__v19` | `l1_jog` | `unet_no_topology` | yes | `probable_artifact` | 0.982 | -0.018 | 0.000 | yes |
| `dense_via_background__v11` | `dense_via_background` | `unet_no_topology` | yes | `probable_artifact` | 0.981 | -0.019 | 0.000 | yes |
| `trace_with_return_path__v53` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.981 | -0.020 | 1.000 | yes |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.981 | 0.020 | 3.065e-04 | no |
| `no_via_background__v35` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.980 | -0.021 | 0.003 | no |
| `trace_with_return_path__v29` | `return_path` | `unet_topology_two_stage_refined` | yes | `no_candidate` | 0.980 | -0.021 | 0.500 | no |
| `no_via_background__v44` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.980 | 0.021 | 0.000 | yes |
| `bend_artifact_trace__v55` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.979 | -0.021 | 0.000 | yes |
| `no_via_background__v32` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.979 | -0.022 | 7.795e-04 | no |
| `bend_artifact_trace__v77` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.978 | -0.022 | 0.002 | no |
| `no_via_background` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.978 | 0.022 | 0.000 | yes |
| `multi_via_route__v19` | `multi_via` | `unet_no_topology` | yes | `probable_artifact` | 0.977 | -0.023 | 0.500 | yes |
| `two_layer_route_with_via__v07` | `l1_jog` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.977 | -0.024 | 0.001 | no |
| `trace_with_return_path__v58` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.976 | 0.024 | 1.000 | no |
| `trace_with_return_path__v98` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.976 | 0.024 | 1.000 | no |
| `no_via_background__v68` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.976 | 0.024 | 0.000 | yes |
| `trace_with_return_path__v80` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.975 | -0.026 | 1.000 | yes |
| `multi_via_route__v20` | `multi_via` | `unet_no_topology` | yes | `probable_artifact` | 0.975 | -0.026 | 0.500 | yes |
| `dense_via_background__v27` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.975 | -0.026 | 0.000 | yes |
| `trace_with_return_path__v02` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.975 | -0.026 | 1.000 | yes |
| `trace_with_return_path__v82` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.975 | -0.026 | 1.000 | yes |
| `no_via_background__v30` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.974 | 0.026 | 0.002 | no |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.974 | 0.027 | 0.000 | yes |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.973 | 0.028 | 0.000 | yes |
| `bend_artifact_trace__v67` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.973 | -0.028 | 0.000 | yes |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.972 | -0.028 | 0.000 | yes |
| `bend_artifact_trace__v52` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.972 | 0.029 | 0.000 | yes |
| `trace_with_return_path__v65` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.971 | 0.030 | 1.000 | yes |
| `trace_with_return_path__v85` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.970 | 0.031 | 1.000 | yes |
| `dense_via_background__v26` | `dense_via_background` | `unet_no_topology` | yes | `probable_artifact` | 0.970 | -0.031 | 0.000 | yes |
| `no_via_background__v42` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.970 | 0.031 | 2.727e-05 | no |
| `trace_with_return_path__v85` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.968 | 0.034 | 1.000 | yes |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.967 | 0.034 | 0.000 | yes |
| `dense_via_background__v27` | `dense_via_background` | `unet_no_topology` | yes | `probable_artifact` | 0.967 | -0.034 | 0.002 | no |
| `bend_artifact_trace__v49` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.967 | -0.034 | 0.000 | yes |
| `trace_with_return_path__v68` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.966 | -0.035 | 1.000 | yes |
| `dense_via_background__v09` | `dense_via_background` | `unet_no_topology` | yes | `probable_artifact` | 0.966 | -0.035 | 0.008 | no |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.966 | 0.035 | 0.000 | yes |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.966 | -0.035 | 0.000 | yes |
| `bend_artifact_trace__v27` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.966 | -0.036 | 0.000 | yes |
| `trace_with_return_path__v49` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.965 | -0.036 | 1.003 | no |
| `trace_with_return_path__v05` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.965 | 0.036 | 1.000 | yes |
| `trace_with_return_path__v49` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.964 | -0.038 | 1.007 | no |
| `no_via_background__v02` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.963 | 0.038 | 0.000 | yes |
| `no_via_background__v82` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.963 | 0.038 | 0.000 | yes |
| `no_via_background__v08` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.961 | 0.040 | 0.000 | yes |
| `no_via_background__v07` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.961 | -0.040 | 0.002 | no |
| `bend_artifact_trace__v70` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.961 | -0.040 | 7.071e-04 | no |
| `bend_artifact_trace__v07` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.961 | -0.041 | 0.000 | yes |
| `no_via_background__v33` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.959 | 0.043 | 0.003 | no |
| `no_via_background__v08` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.958 | 0.043 | 0.000 | yes |
| `bend_artifact_trace__v31` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.958 | -0.044 | 0.005 | no |
| `no_via_background__v49` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.957 | -0.045 | 0.000 | yes |
| `trace_with_return_path__v58` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.957 | 0.045 | 1.003 | no |
| `trace_with_return_path__v98` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.957 | 0.045 | 1.003 | no |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.957 | 0.045 | 0.000 | yes |
| `no_via_background__v48` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.957 | -0.045 | 0.002 | no |
| `trace_with_return_path__v11` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.957 | 0.045 | 1.000 | yes |
| `trace_with_return_path__v51` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.957 | 0.045 | 1.000 | yes |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.956 | 0.046 | 0.008 | no |
| `two_layer_route_with_via__v12` | `l1_jog` | `unet_topology_soft_loss` | yes | `probable_artifact` | 0.956 | -0.046 | 6.138e-04 | no |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.956 | -0.046 | 2.042e-04 | no |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.956 | -0.046 | 2.042e-04 | no |
| `trace_with_return_path__v41` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.956 | 0.046 | 1.000 | yes |
| `trace_with_return_path__v61` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.956 | 0.046 | 1.000 | yes |
| `trace_with_return_path__v70` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.954 | -0.048 | 1.000 | yes |
| `trace_with_return_path__v24` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.954 | 0.048 | 1.000 | yes |
| `no_via_background__v54` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.953 | -0.049 | 0.003 | no |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.953 | -0.049 | 0.000 | yes |
| `no_via_background__v44` | `no_via_background` | `unet_no_topology` | no | `probable_artifact` | 0.953 | -0.049 | 0.000 | yes |
| `trace_with_return_path__v41` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.953 | 0.049 | 1.000 | yes |
| `trace_with_return_path__v61` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.953 | 0.049 | 1.000 | yes |
| `via_pair` | `canonical` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.953 | -0.050 | 1.000 | yes |
| `bend_artifact_trace__v11` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.952 | -0.050 | 0.000 | yes |
| `no_via_background__v03` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.952 | -0.050 | 7.233e-04 | no |
| `no_via_background__v83` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.952 | -0.050 | 7.233e-04 | no |
| `trace_with_return_path__v96` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.952 | -0.051 | 1.000 | yes |
| `no_via_background__v34` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.951 | -0.052 | 0.000 | yes |
| `bend_artifact_trace__v19` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.950 | -0.053 | 0.000 | yes |
| `trace_with_return_path__v35` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.949 | -0.054 | 1.000 | yes |
| `trace_with_return_path__v75` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.949 | -0.054 | 1.000 | yes |
| `no_via_background__v51` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.948 | 0.055 | 0.002 | no |
| `trace_with_return_path__v70` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.948 | 0.055 | 1.000 | yes |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.947 | 0.056 | 0.002 | no |

Interpretation: refusal is a reporting layer for ambiguous residuals. It is meant to prevent overclaiming high-confidence via diagnosis from a single passive field.
