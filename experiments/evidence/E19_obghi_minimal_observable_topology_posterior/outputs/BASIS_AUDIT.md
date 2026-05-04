# E19.1 Basis Audit

## Per-hypothesis column counts

| hypothesis | kept_columns | dropped_columns | total_blocks |
|---|---|---|---:|
| H0_no_via | 12 | 0 | 2 |
| H1_via | 42 | 0 | 4 |
| H2_model_gap | 39 | 0 | 5 |
| H3_return_path | 34 | 0 | 4 |

## Per-block column counts (first case sample)

| hypothesis | block_kind | count |
|---|---:|
| H0_no_via | graph | 8 |
| H0_no_via | residual | 4 |
| H1_via | graph | 8 |
| H1_via | residual | 4 |
| H1_via | via_vertical | 15 |
| H1_via | via_compensation | 15 |
| H2_model_gap | graph | 8 |
| H2_model_gap | residual | 4 |
| H2_model_gap | gap_registration | 6 |
| H2_model_gap | gap_standoff | 12 |
| H2_model_gap | gap_drift | 9 |
| H3_return_path | graph | 8 |
| H3_return_path | residual | 4 |
| H3_return_path | return_loop | 10 |
| H3_return_path | return_edge | 12 |
