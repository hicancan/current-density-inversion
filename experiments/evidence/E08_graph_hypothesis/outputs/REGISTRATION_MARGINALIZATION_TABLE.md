# Exp08 P0-next/P1-next via-location marginalization

| family | mode | 4-way acc | H1 acc | via recall | via F1 | no-via FP | median best offset um |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_hidden | base | 0.4167 | 0.4583 | 0.4167 | 0.5882 | 0.0000 |  |
| all_hidden | via_location_marginalized | 0.6250 | 0.8958 | 0.4375 | 0.6087 | 0.0000 | 240.0000 |
| combined_true_via_hidden_return | base | 0.7917 | 0.7917 | 0.7917 | 0.8837 | 0.0000 |  |
| combined_true_via_hidden_return | via_location_marginalized | 0.7917 | 0.7917 | 0.4167 | 0.5882 | 0.0000 | 0.0000 |
| hidden_return_no_via | base | 0.7500 | nan | 0.0000 | 0.0000 | 0.0000 |  |
| hidden_return_no_via | via_location_marginalized | 0.7083 | nan | 0.0000 | 0.0000 | 0.0000 | 339.4113 |
| mismatched_artifact | base | 0.0000 | nan | 0.0000 | 0.0000 | 0.0000 |  |
| mismatched_artifact | via_location_marginalized | 0.0000 | nan | 0.0000 | 0.0000 | 0.0000 | 289.7056 |
| shifted_true_via | base | 0.1250 | 0.1250 | 0.0417 | 0.0800 | 0.0000 |  |
| shifted_true_via | via_location_marginalized | 1.0000 | 1.0000 | 0.4583 | 0.6286 | 0.0000 | 240.0000 |

Via candidate offsets are fixed by config and selected without hidden/PyPEEC labels.
