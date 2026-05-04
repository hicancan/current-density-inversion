# E19 Failure Cases

| case | truth | top | p_top | decision | failure_mode |
|---|---|---|---:|---|---|
| E19_no_via_clean_000 | H0_no_via | H3_return_path | 0.9997 | accept | accepted_wrong_topology |
| E19_no_via_clean_001 | H0_no_via | H3_return_path | 0.9993 | accept | accepted_wrong_topology |
| E19_no_via_clean_002 | H0_no_via | H3_return_path | 0.9992 | accept | accepted_wrong_topology |
| E19_single_via_observable_000 | H1_via | H3_return_path | 0.9996 | accept | accepted_wrong_topology |
| E19_single_via_observable_001 | H1_via | H3_return_path | 0.8402 | accept | accepted_wrong_topology |
| E19_single_via_observable_002 | H1_via | H3_return_path | 0.9989 | accept | accepted_wrong_topology |
| E19_model_gap_registration_000 | H2_model_gap | H3_return_path | 0.9953 | accept | accepted_wrong_topology |
| E19_model_gap_registration_001 | H2_model_gap | H3_return_path | 0.9777 | accept | accepted_wrong_topology |
| E19_model_gap_registration_002 | H2_model_gap | H3_return_path | 0.9928 | accept | accepted_wrong_topology |

Failures are preserved as generated-domain evidence boundaries.
