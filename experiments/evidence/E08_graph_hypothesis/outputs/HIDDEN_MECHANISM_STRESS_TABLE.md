# Exp08 hidden-mechanism OOD stress

| family | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | via AUC | via recall | via F1 | no-via FP | median margin | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all_hidden | 96 | 0.4167 | 0.7500 | 0.4583 | nan | 0.0000 | 0.9288 | 0.4167 | 0.5882 | 0.0000 | 4.485e-04 | 0.1529 |
| combined_true_via_hidden_return | 24 | 0.7917 | nan | 0.7917 | nan | nan | nan | 0.7917 | 0.8837 | 0.0000 | 0.0033 | 0.1513 |
| hidden_return_no_via | 24 | 0.7500 | 0.7500 | nan | nan | nan | nan | 0.0000 | 0.0000 | 0.0000 | 4.703e-04 | 0.1782 |
| mismatched_artifact | 24 | 0.0000 | nan | nan | nan | 0.0000 | nan | 0.0000 | 0.0000 | 0.0000 | 3.450e-04 | 0.1427 |
| shifted_true_via | 24 | 0.1250 | nan | 0.1250 | nan | nan | nan | 0.0417 | 0.0800 | 0.0000 | 2.773e-04 | 0.1157 |

Hidden mechanisms are deliberately missing or mismatched in the candidate library; perfect accuracy is not expected.
