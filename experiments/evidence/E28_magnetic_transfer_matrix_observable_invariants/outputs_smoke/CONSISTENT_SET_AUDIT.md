# Consistent Set Audit

Epsilon threshold: **1.122369**

| metric | value |
|---|---:|
| n_cases | 4 |
| nonempty rate | 1.0000 |
| ambiguity rate | 0.5000 |
| empty rate | 0.0000 |
| truth-in-consistent rate | 1.0000 |
| singleton correct rate | 0.5000 |

## Per-Case Details

| case_id | family | truth | consistent | non_consistent |
|---|---|---|---|---|
| E28_no_via_clean_000 | no_via_clean | H0_no_via | H0_no_via | H1_via, H2_model_gap, H3_return_path |
| E28_single_via_observable_000 | single_via_observable | H1_via | H1_via, H2_model_gap | H0_no_via, H3_return_path |
| E28_model_gap_registration_000 | model_gap_registration | H2_model_gap | H1_via, H2_model_gap | H0_no_via, H3_return_path |
| E28_return_path_deep_loop_000 | return_path_deep_loop | H3_return_path | H3_return_path | H0_no_via, H1_via, H2_model_gap |