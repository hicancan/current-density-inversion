# Exp08 P4 constrained active-design audit

| policy | constraint status | label-free utility | 4-way acc | H0 acc | median joint margin | median margin gain | median joint best score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| h0_disambiguation | allowed | 0.0653 | 0.9400 | 0.7600 | 0.0530 | 0.0456 | 0.1050 |
| max_expected_margin | constraint_limited | 0.0602 | 0.9400 | 0.7600 | 0.0497 | 0.0420 | 0.1053 |
| min_expected_entropy | allowed | 0.0225 | 0.9400 | 0.7600 | 0.0245 | 0.0164 | 0.1026 |
| extra_boost | constraint_limited | 0.0218 | 0.9400 | 0.7600 | 0.0232 | 0.0179 | 0.1037 |
| h1_h2_separation | allowed | 0.0067 | 0.9400 | 0.7600 | 0.0153 | 0.0030 | 0.1012 |
| random_independent | allowed | 0.0019 | 0.9200 | 0.7600 | 0.0109 | 0.0025 | 0.1026 |
| extra_sign_flip | not_allowed | 6.285e-04 | 0.9200 | 0.7600 | 0.0098 | 0.0020 | 0.1019 |
| sheet_rescale | allowed | -6.133e-05 | 0.9300 | 0.7600 | 0.0092 | 0.0012 | 0.0990 |
| low_noise_repeat | not_allowed | -0.0018 | 0.9200 | 0.7600 | 0.0077 | 0.0016 | 0.1022 |

The constraints are synthetic feasibility screens for current gain, sheet-current perturbation, and allowed excitation families. They do not represent real hardware limits yet.
