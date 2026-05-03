# Null-Via Uncertainty And Refusal Diagnostics

- enabled: `True`
- boundary: Refusal labels are diagnostic confidence categories. They do not change the reported frozen model predictions or choose PyPEEC thresholds.

## Summary

| model | rows | high-conf via rate | no-via high-conf false alarm | true-via refusal/low-conf | ambiguous/refusal | mean uncertainty |
|---|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 400 | 0.062 | 0.105 | 0.980 | 0.578 | 0.737 |
| `unet_topology_soft_loss` | 400 | 0.025 | 0.050 | 1.000 | 0.627 | 0.757 |
| `unet_topology_two_stage_refined` | 400 | 0.033 | 0.060 | 0.995 | 0.430 | 0.759 |

## Highest-Uncertainty Rows

| case | type | model | true via | decision | uncertainty | margin | return evidence | selected gate accepted |
|---|---|---|---:|---|---:|---:|---:|---:|
| `no_via_background__v68` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 1.000 | 4.192e-04 | 0.000 | yes |
| `trace_with_return_path__v70` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.999 | -6.342e-04 | 1.000 | yes |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.999 | -0.001 | 0.000 | yes |
| `no_via_background__v72` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.997 | 0.003 | 0.000 | yes |
| `no_via_background__v03` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.997 | 0.003 | 0.001 | no |
| `no_via_background__v83` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.997 | 0.003 | 0.001 | no |
| `trace_with_return_path__v10` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.997 | 0.003 | 1.000 | yes |
| `trace_with_return_path__v50` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.997 | 0.003 | 1.000 | yes |
| `trace_with_return_path__v96` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.996 | -0.004 | 1.000 | yes |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.995 | -0.005 | 0.001 | no |
| `dense_via_background__v27` | `dense_via_background` | `unet_topology_soft_loss` | yes | `probable_artifact` | 0.995 | -0.005 | 0.001 | no |
| `bend_artifact_trace__v82` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.995 | 0.005 | 0.002 | no |
| `no_via_background__v57` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.994 | -0.006 | 0.000 | yes |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.993 | 0.007 | 0.011 | no |
| `trace_with_return_path__v10` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.993 | -0.007 | 1.000 | yes |
| `trace_with_return_path__v50` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.993 | -0.007 | 1.000 | yes |
| `trace_with_return_path__v96` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.993 | 0.007 | 1.000 | yes |
| `no_via_background__v38` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.993 | 0.007 | 0.000 | yes |
| `trace_with_return_path__v95` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.992 | 0.008 | 1.000 | yes |
| `bend_artifact_trace__v41` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.990 | 0.010 | 0.000 | yes |
| `bend_artifact_trace__v44` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.989 | 0.011 | 0.000 | yes |
| `trace_with_return_path__v27` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.989 | 0.011 | 1.000 | yes |
| `multi_via_route__v13` | `multi_via` | `unet_no_topology` | yes | `low_confidence_residual` | 0.989 | 0.011 | 0.500 | yes |
| `bend_artifact_trace__v78` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.988 | 0.012 | 0.002 | no |
| `two_layer_route_with_via__v04` | `l1_jog` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.988 | -0.012 | 0.000 | yes |
| `bend_artifact_trace__v12` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.987 | -0.013 | 0.000 | yes |
| `bend_artifact_trace__v92` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.987 | -0.013 | 0.000 | yes |
| `trace_with_return_path__v59` | `return_path` | `unet_no_topology` | yes | `no_candidate` | 0.985 | -0.015 | 0.000 | no |
| `trace_with_return_path__v18` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.985 | -0.015 | 1.000 | yes |
| `no_via_background__v35` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.985 | 0.015 | 0.002 | no |
| `dense_via_background__v02` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `low_confidence_residual` | 0.985 | 0.016 | 0.000 | yes |
| `trace_with_return_path__v18` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.984 | 0.016 | 1.000 | yes |
| `bend_artifact_trace__v10` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.984 | -0.016 | 0.001 | no |
| `dense_via_background__v03` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `low_confidence_residual` | 0.983 | 0.017 | 0.000 | yes |
| `two_layer_route_with_via__v12` | `l1_jog` | `unet_no_topology` | yes | `low_confidence_residual` | 0.983 | 0.018 | 0.000 | yes |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.982 | -0.018 | 0.000 | yes |
| `no_via_background__v26` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.982 | -0.019 | 0.000 | yes |
| `bend_artifact_trace__v51` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.982 | 0.019 | 0.000 | yes |
| `no_via_background__v01` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.981 | 0.019 | 4.992e-04 | no |
| `no_via_background__v81` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.981 | 0.019 | 4.992e-04 | no |
| `trace_with_return_path__v25` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.980 | -0.021 | 1.000 | yes |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.979 | -0.021 | 0.001 | no |
| `trace_with_return_path__v24` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.979 | -0.021 | 1.000 | yes |
| `bend_artifact_trace__v60` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.979 | -0.021 | 0.000 | yes |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.979 | -0.021 | 0.000 | yes |
| `multi_via_route__v13` | `multi_via` | `unet_topology_soft_loss` | yes | `probable_artifact` | 0.979 | -0.022 | 0.500 | yes |
| `two_layer_route_with_via__v06` | `l1_jog` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.978 | -0.022 | 0.000 | yes |
| `bend_artifact_trace__v53` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.976 | 0.024 | 0.000 | yes |
| `no_via_background__v77` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.976 | -0.024 | 6.638e-04 | no |
| `trace_with_return_path__v35` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.976 | -0.024 | 1.000 | yes |
| `trace_with_return_path__v75` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.976 | -0.024 | 1.000 | yes |
| `multi_via_route__v18` | `multi_via` | `unet_no_topology` | yes | `probable_artifact` | 0.976 | -0.025 | 0.506 | no |
| `trace_with_return_path__v85` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.976 | 0.025 | 1.000 | yes |
| `dense_via_background__v08` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.975 | -0.026 | 0.000 | yes |
| `bend_artifact_trace__v76` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.974 | -0.027 | 0.006 | no |
| `dense_via_background__v08` | `dense_via_background` | `unet_no_topology` | yes | `low_confidence_residual` | 0.973 | 0.027 | 9.131e-05 | no |
| `bend_artifact_trace__v06` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.973 | 0.027 | 0.000 | yes |
| `trace_with_return_path__v04` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.972 | -0.029 | 1.000 | yes |
| `bend_artifact_trace__v24` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.971 | -0.029 | 0.000 | yes |
| `no_via_background__v49` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.970 | -0.031 | 0.000 | yes |
| `trace_with_return_path__v01` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.969 | -0.032 | 1.000 | yes |
| `trace_with_return_path__v81` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.969 | -0.032 | 1.000 | yes |
| `two_layer_route_with_via__v05` | `l1_jog` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.969 | -0.032 | 0.000 | yes |
| `no_via_background__v27` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.969 | -0.032 | 0.000 | yes |
| `bend_artifact_trace__v72` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.969 | -0.032 | 0.000 | yes |
| `trace_with_return_path__v52` | `return_path` | `unet_topology_two_stage_refined` | yes | `no_candidate` | 0.968 | -0.033 | 0.293 | no |
| `bend_artifact_trace__v30` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.967 | 0.034 | 0.004 | no |
| `dense_via_background__v10` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `low_confidence_residual` | 0.966 | 0.036 | 0.000 | yes |
| `trace_with_return_path__v46` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.965 | -0.036 | 1.000 | yes |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.965 | 0.036 | 0.000 | yes |
| `no_via_background__v50` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.965 | 0.036 | 0.003 | no |
| `no_via_background__v01` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.965 | 0.036 | 6.771e-04 | no |
| `no_via_background__v81` | `no_via_background` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.965 | 0.036 | 6.771e-04 | no |
| `no_via_background__v05` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.965 | -0.037 | 0.000 | yes |
| `no_via_background__v08` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.964 | -0.037 | 0.000 | yes |
| `no_via_background__v30` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.964 | -0.037 | 0.000 | yes |
| `trace_with_return_path__v57` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.963 | -0.038 | 1.000 | yes |
| `no_via_background__v35` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.963 | 0.038 | 0.000 | yes |
| `bend_artifact_trace__v58` | `bend_artifact` | `unet_no_topology` | no | `low_confidence_residual` | 0.963 | 0.038 | 0.000 | yes |
| `no_via_background__v29` | `no_via_background` | `unet_no_topology` | no | `probable_artifact` | 0.963 | -0.039 | 7.685e-04 | no |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.963 | -0.039 | 0.003 | no |
| `bend_artifact_trace__v75` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.962 | 0.039 | 0.002 | no |
| `bend_artifact_trace__v80` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.962 | -0.039 | 0.000 | yes |
| `bend_artifact_trace__v98` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.962 | 0.039 | 0.000 | yes |
| `two_layer_route_with_via__v27` | `l1_jog` | `unet_topology_soft_loss` | yes | `probable_artifact` | 0.962 | -0.039 | 0.500 | yes |
| `trace_with_return_path__v45` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.962 | -0.040 | 1.000 | yes |
| `multi_via_route__v23` | `multi_via` | `unet_topology_soft_loss` | yes | `probable_artifact` | 0.962 | -0.040 | 0.500 | yes |
| `trace_with_return_path__v11` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.961 | -0.040 | 1.000 | yes |
| `trace_with_return_path__v51` | `return_path` | `unet_topology_soft_loss` | yes | `return_path_ambiguous` | 0.961 | -0.040 | 1.000 | yes |
| `bend_artifact_trace__v50` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.961 | -0.040 | 2.587e-04 | no |
| `bend_artifact_trace__v40` | `bend_artifact` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.961 | -0.040 | 0.000 | yes |
| `no_via_background__v02` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.961 | 0.041 | 0.000 | yes |
| `no_via_background__v82` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.961 | 0.041 | 0.000 | yes |
| `no_via_background__v42` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.961 | 0.041 | 0.000 | yes |
| `no_via_background__v53` | `no_via_background` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.960 | -0.041 | 4.454e-04 | no |
| `trace_with_return_path__v29` | `return_path` | `unet_topology_two_stage_refined` | yes | `no_candidate` | 0.960 | -0.042 | 0.500 | no |
| `no_via_background__v33` | `no_via_background` | `unet_topology_soft_loss` | no | `probable_artifact` | 0.959 | -0.043 | 0.002 | no |
| `bend_artifact_trace__v83` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.959 | -0.043 | 0.000 | yes |
| `dense_via_background__v11` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.958 | -0.043 | 0.000 | yes |
| `trace_with_return_path__v28` | `return_path` | `unet_topology_two_stage_refined` | yes | `no_candidate` | 0.958 | -0.044 | 0.500 | no |
| `bend_artifact_trace__v05` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.957 | -0.045 | 0.000 | yes |
| `dense_via_background__v26` | `dense_via_background` | `unet_topology_two_stage_refined` | yes | `probable_artifact` | 0.957 | -0.045 | 0.000 | yes |
| `trace_with_return_path__v40` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.957 | 0.045 | 1.000 | yes |
| `trace_with_return_path__v60` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.957 | 0.045 | 1.000 | yes |
| `trace_with_return_path__v55` | `return_path` | `unet_topology_two_stage_refined` | yes | `return_path_ambiguous` | 0.957 | -0.045 | 1.000 | yes |
| `trace_with_return_path__v91` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.956 | -0.046 | 1.000 | yes |
| `no_via_background__v32` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.956 | 0.046 | 0.000 | yes |
| `bend_artifact_trace__v08` | `bend_artifact` | `unet_topology_soft_loss` | no | `low_confidence_residual` | 0.955 | 0.047 | 0.000 | yes |
| `trace_with_return_path__v80` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.954 | -0.049 | 1.000 | yes |
| `bend_artifact_trace__v15` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.954 | -0.049 | 0.000 | yes |
| `bend_artifact_trace__v95` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.954 | -0.049 | 0.000 | yes |
| `trace_with_return_path__v33` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.953 | 0.049 | 1.000 | yes |
| `trace_with_return_path__v73` | `return_path` | `unet_no_topology` | yes | `return_path_ambiguous` | 0.953 | 0.049 | 1.000 | yes |
| `dense_via_background__v27` | `dense_via_background` | `unet_no_topology` | yes | `probable_artifact` | 0.953 | -0.049 | 0.002 | no |
| `bend_artifact_trace__v09` | `bend_artifact` | `unet_no_topology` | no | `probable_artifact` | 0.953 | -0.050 | 0.000 | yes |
| `no_via_background__v02` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.952 | 0.050 | 0.002 | no |
| `no_via_background__v82` | `no_via_background` | `unet_no_topology` | no | `low_confidence_residual` | 0.952 | 0.050 | 0.002 | no |
| `no_via_background__v05` | `no_via_background` | `unet_no_topology` | no | `probable_artifact` | 0.952 | -0.051 | 0.000 | yes |
| `bend_artifact_trace__v01` | `bend_artifact` | `unet_topology_two_stage_refined` | no | `probable_artifact` | 0.951 | -0.051 | 0.000 | yes |
| `no_via_background__v72` | `no_via_background` | `unet_topology_two_stage_refined` | no | `low_confidence_residual` | 0.951 | 0.051 | 0.000 | yes |

Interpretation: refusal is a reporting layer for ambiguous residuals. It is meant to prevent overclaiming high-confidence via diagnosis from a single passive field.
