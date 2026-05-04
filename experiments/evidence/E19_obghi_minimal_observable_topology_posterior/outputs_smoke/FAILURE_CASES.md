# E19 Failure Cases

| case | truth | top | p_top | decision | failure_mode |
|---|---|---|---:|---|---|
| E19_no_via_clean_000 | H0_no_via | H1_via | 0.6294 | accept | accepted_wrong_topology |
| E19_no_via_clean_001 | H0_no_via | H1_via | 0.5640 | need_next_measurement | insufficient_posterior_separation |
| E19_no_via_clean_002 | H0_no_via | H1_via | 0.6679 | accept | accepted_wrong_topology |
| E19_single_via_observable_001 | H1_via | H1_via | 0.5340 | need_next_measurement | insufficient_posterior_separation |
| E19_model_gap_registration_000 | H2_model_gap | H1_via | 0.5779 | need_next_measurement | insufficient_posterior_separation |
| E19_model_gap_registration_001 | H2_model_gap | H1_via | 0.6721 | accept | accepted_wrong_topology |
| E19_model_gap_registration_002 | H2_model_gap | H1_via | 0.6059 | need_next_measurement | insufficient_posterior_separation |
| E19_return_path_deep_loop_000 | H3_return_path | H1_via | 0.6274 | accept | accepted_wrong_topology |
| E19_return_path_deep_loop_001 | H3_return_path | H1_via | 0.6183 | need_next_measurement | insufficient_posterior_separation |
| E19_return_path_deep_loop_002 | H3_return_path | H1_via | 0.5503 | need_next_measurement | insufficient_posterior_separation |

Failures are preserved as generated-domain evidence boundaries.
