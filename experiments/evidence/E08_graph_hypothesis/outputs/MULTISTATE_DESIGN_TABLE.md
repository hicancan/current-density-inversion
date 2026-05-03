# Exp08 P3-next synthetic multi-state design scan

| method | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | median joint margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| single_state | 100 | 0.8800 | 0.7200 | 0.8000 | 1.0000 | 1.0000 |  |
| joint_random_independent | 100 | 0.9200 | 0.7600 | 0.9200 | 1.0000 | 1.0000 | 0.0109 |
| joint_sheet_rescale | 100 | 0.9300 | 0.7600 | 0.9600 | 1.0000 | 1.0000 | 0.0092 |
| joint_extra_boost | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0232 |
| joint_extra_sign_flip | 100 | 0.9200 | 0.7600 | 0.9200 | 1.0000 | 1.0000 | 0.0098 |
| joint_low_noise_repeat | 100 | 0.9200 | 0.7600 | 0.9200 | 1.0000 | 1.0000 | 0.0077 |
| joint_h0_disambiguation | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0530 |
| joint_h1_h2_separation | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0153 |
| joint_max_expected_margin | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0497 |
| joint_min_expected_entropy | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0245 |

Second excitation is synthetic and generated from the same graph; this is not active-measurement data.
