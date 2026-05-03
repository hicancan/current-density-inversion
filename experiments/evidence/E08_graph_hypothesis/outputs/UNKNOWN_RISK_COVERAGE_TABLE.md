# Exp08 P2 unknown rejection risk-coverage diagnostic

| dataset | coverage | accepted | rejected | accepted acc | accepted risk | median confidence/residual |
| --- | --- | --- | --- | --- | --- | --- |
| clean_ood | 20% | 20 | 80 | 1.0000 | 0.0000 | 1.0844 |
| clean_ood | 40% | 40 | 60 | 0.9500 | 0.0500 | 0.5023 |
| clean_ood | 60% | 60 | 40 | 0.9500 | 0.0500 | 0.2689 |
| clean_ood | 80% | 80 | 20 | 0.9125 | 0.0875 | 0.0812 |
| clean_ood | 100% | 100 | 0 | 0.8800 | 0.1200 | 0.0433 |
| hidden_all | 20% | 19 | 77 | 0.5789 | 0.4211 | 0.0324 |
| hidden_all | 40% | 38 | 58 | 0.5000 | 0.5000 | 0.0131 |
| hidden_all | 60% | 58 | 38 | 0.5000 | 0.5000 | 0.0052 |
| hidden_all | 80% | 77 | 19 | 0.4805 | 0.5195 | 0.0034 |
| hidden_all | 100% | 96 | 0 | 0.4167 | 0.5833 | 0.0027 |
| hidden_combined_true_via_hidden_return | 20% | 5 | 19 | 0.8000 | 0.2000 | 0.0555 |
| hidden_combined_true_via_hidden_return | 40% | 10 | 14 | 0.7000 | 0.3000 | 0.0416 |
| hidden_combined_true_via_hidden_return | 60% | 14 | 10 | 0.7143 | 0.2857 | 0.0385 |
| hidden_combined_true_via_hidden_return | 80% | 19 | 5 | 0.7368 | 0.2632 | 0.0307 |
| hidden_combined_true_via_hidden_return | 100% | 24 | 0 | 0.7917 | 0.2083 | 0.0210 |
| hidden_hidden_return_no_via | 20% | 5 | 19 | 0.0000 | 1.0000 | 0.0253 |
| hidden_hidden_return_no_via | 40% | 10 | 14 | 0.4000 | 0.6000 | 0.0037 |
| hidden_hidden_return_no_via | 60% | 14 | 10 | 0.5714 | 0.4286 | 0.0031 |
| hidden_hidden_return_no_via | 80% | 19 | 5 | 0.6842 | 0.3158 | 0.0028 |
| hidden_hidden_return_no_via | 100% | 24 | 0 | 0.7500 | 0.2500 | 0.0024 |
| hidden_mismatched_artifact | 20% | 5 | 19 | 0.0000 | 1.0000 | 0.0052 |
| hidden_mismatched_artifact | 40% | 10 | 14 | 0.0000 | 1.0000 | 0.0035 |
| hidden_mismatched_artifact | 60% | 14 | 10 | 0.0000 | 1.0000 | 0.0029 |
| hidden_mismatched_artifact | 80% | 19 | 5 | 0.0000 | 1.0000 | 0.0022 |
| hidden_mismatched_artifact | 100% | 24 | 0 | 0.0000 | 1.0000 | 0.0020 |
| hidden_shifted_true_via | 20% | 5 | 19 | 0.4000 | 0.6000 | 0.0044 |
| hidden_shifted_true_via | 40% | 10 | 14 | 0.2000 | 0.8000 | 0.0035 |
| hidden_shifted_true_via | 60% | 14 | 10 | 0.1429 | 0.8571 | 0.0032 |
| hidden_shifted_true_via | 80% | 19 | 5 | 0.1579 | 0.8421 | 0.0022 |
| hidden_shifted_true_via | 100% | 24 | 0 | 0.1250 | 0.8750 | 0.0021 |

Confidence is margin divided by best residual. This is a selective-prediction diagnostic, not a new classifier.
