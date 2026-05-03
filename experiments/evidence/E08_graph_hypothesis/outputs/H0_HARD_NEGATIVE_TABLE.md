# Exp08 P1 H0/no-via hard-negative diagnostic

| dataset | mode | n | H0 acc | false H1 rate | false H2 rate | false H3 rate | 4-way acc | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pypeec_no_via | base/default_score | 100 | 0.0500 | 0.0000 | 0.3300 | 0.6200 | 0.0500 | 0.1709 |
| pypeec_no_via | base/h0_conservative | 100 | 0.5800 | 0.0000 | 0.1400 | 0.2800 | 0.5800 | 0.1742 |
| pypeec_no_via | finite_width_sheet/default_score | 100 | 0.0800 | 0.0300 | 0.2400 | 0.6500 | 0.0800 | 0.1004 |
| pypeec_no_via | finite_width_sheet/h0_conservative | 100 | 0.9700 | 0.0000 | 0.0000 | 0.0300 | 0.9700 | 0.1015 |
| pypeec_no_via | return_bank/default_score | 100 | 0.0300 | 0.0000 | 0.6200 | 0.3500 | 0.0300 | 0.1609 |
| pypeec_no_via | return_bank/h0_conservative | 100 | 0.5000 | 0.0000 | 0.2800 | 0.2200 | 0.5000 | 0.1633 |
| pypeec_no_via | artifact_bank/default_score | 100 | 0.0200 | 0.0000 | 0.1300 | 0.8500 | 0.0200 | 0.1588 |
| pypeec_no_via | artifact_bank/h0_conservative | 100 | 0.6600 | 0.0000 | 0.1600 | 0.1800 | 0.6600 | 0.1642 |
| pypeec_no_via | distributed_via/default_score | 100 | 0.0500 | 0.0000 | 0.3300 | 0.6200 | 0.0500 | 0.1709 |
| pypeec_no_via | distributed_via/h0_conservative | 100 | 0.5800 | 0.0000 | 0.1400 | 0.2800 | 0.5800 | 0.1742 |
| pypeec_no_via | combined_pypeec_aware/default_score | 100 | 0.0300 | 0.0000 | 0.0300 | 0.9400 | 0.0300 | 0.0807 |
| pypeec_no_via | combined_pypeec_aware/h0_conservative | 100 | 0.7600 | 0.0000 | 0.0000 | 0.2400 | 0.7600 | 0.0947 |
| clean_ood_no_via | base/default_score | 25 | 0.7200 | 0.0000 | 0.2800 | 0.0000 | 0.7200 | 0.1256 |
| hidden_return_no_via | base/default_score | 24 | 0.7500 | 0.0000 | 0.2500 | 0.0000 | 0.7500 | 0.1782 |

H0/no-via is the hard negative class: a reliable system must avoid explaining every residual as via, return, or artifact.
