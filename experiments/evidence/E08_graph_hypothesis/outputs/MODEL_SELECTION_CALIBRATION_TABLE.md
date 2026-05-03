# Exp08 P0 formal model-selection calibration audit

| basis mode | evidence mode | objective | 4-way acc | H0 acc | H1 acc | H2 acc | false H1 | false H2 | false H3 | median residual | median params | meets H1 floor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finite_width_sheet | h0_conservative | 0.7920 | 0.9150 | 0.9700 | 0.6900 | 1.0000 | 0.0000 | 0.0000 | 0.0300 | 0.1086 | 5.0000 | True |
| finite_width_sheet | extra_count | 0.7240 | 0.8900 | 0.7800 | 0.7800 | 1.0000 | 0.0000 | 0.0600 | 0.1600 | 0.1075 | 5.0000 | True |
| artifact_bank | h0_conservative | 0.5910 | 0.7825 | 0.6600 | 0.4700 | 1.0000 | 0.0000 | 0.1600 | 0.1800 | 0.1712 | 4.0000 | False |
| base | h0_conservative | 0.5540 | 0.7650 | 0.5800 | 0.4800 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 | False |
| artifact_bank | extra_count | 0.5340 | 0.7650 | 0.4800 | 0.5800 | 1.0000 | 0.0000 | 0.3200 | 0.2000 | 0.1680 | 4.0000 | False |
| return_bank | h0_conservative | 0.4910 | 0.7425 | 0.5000 | 0.4700 | 1.0000 | 0.0000 | 0.2800 | 0.2200 | 0.1608 | 5.0000 | False |
| finite_width_sheet | bic_like | 0.4750 | 0.7875 | 0.1500 | 1.0000 | 1.0000 | 0.0200 | 0.2400 | 0.5900 | 0.1042 | 5.0000 | True |
| combined_pypeec_aware | h0_conservative | 0.4510 | 0.7325 | 0.7600 | 0.1700 | 1.0000 | 0.0000 | 0.0000 | 0.2400 | 0.1099 | 9.0000 | False |
| base | extra_count | 0.4470 | 0.7225 | 0.3000 | 0.5900 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 | False |
| finite_width_sheet | default_score | 0.4400 | 0.7700 | 0.0800 | 1.0000 | 1.0000 | 0.0300 | 0.2400 | 0.6500 | 0.1042 | 5.0000 | True |
| finite_width_sheet | parameter_count | 0.4250 | 0.7625 | 0.0500 | 1.0000 | 1.0000 | 0.0500 | 0.2500 | 0.6500 | 0.1042 | 5.0000 | True |
| distributed_via | h0_conservative | 0.4250 | 0.6575 | 0.5800 | 0.0500 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 | False |
| combined_pypeec_aware | extra_count | 0.4220 | 0.7250 | 0.6600 | 0.2400 | 1.0000 | 0.0000 | 0.0000 | 0.3400 | 0.1082 | 9.0000 | False |
| return_bank | extra_count | 0.4020 | 0.7200 | 0.2900 | 0.5900 | 1.0000 | 0.0000 | 0.3300 | 0.3800 | 0.1585 | 6.0000 | False |
| finite_width_sheet | residual_only | 0.4000 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 0.0500 | 0.2700 | 0.6800 | 0.1042 | 5.0000 | True |
| base | bic_like | 0.3930 | 0.7175 | 0.0600 | 0.8100 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1715 | 4.0000 | True |
| base | default_score | 0.3910 | 0.7175 | 0.0500 | 0.8200 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1715 | 4.0000 | True |
| base | parameter_count | 0.3840 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1715 | 4.0000 | True |
| distributed_via | parameter_count | 0.3840 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1711 | 4.0000 | True |
| base | residual_only | 0.3690 | 0.7075 | 0.0000 | 0.8300 | 1.0000 | 0.0100 | 0.3400 | 0.6500 | 0.1715 | 4.0000 | True |
| distributed_via | residual_only | 0.3680 | 0.7150 | 0.0000 | 0.8600 | 1.0000 | 0.0500 | 0.3400 | 0.6100 | 0.1711 | 4.5000 | True |
| distributed_via | default_score | 0.3520 | 0.6850 | 0.0500 | 0.6900 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1724 | 4.0000 | True |
| distributed_via | bic_like | 0.3420 | 0.6750 | 0.0600 | 0.6400 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1724 | 4.0000 | False |
| return_bank | bic_like | 0.3070 | 0.6825 | 0.0400 | 0.6900 | 1.0000 | 0.0000 | 0.5900 | 0.3700 | 0.1573 | 6.0000 | True |
| return_bank | default_score | 0.3020 | 0.6800 | 0.0300 | 0.6900 | 1.0000 | 0.0000 | 0.6200 | 0.3500 | 0.1573 | 6.0000 | True |
| return_bank | parameter_count | 0.3000 | 0.6800 | 0.0200 | 0.7000 | 1.0000 | 0.0000 | 0.6600 | 0.3200 | 0.1573 | 6.0000 | True |
| distributed_via | extra_count | 0.2940 | 0.5950 | 0.3000 | 0.0800 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 | False |
| return_bank | residual_only | 0.2930 | 0.6775 | 0.0000 | 0.7100 | 1.0000 | 0.0000 | 0.7300 | 0.2700 | 0.1573 | 6.0000 | True |
| artifact_bank | default_score | 0.1880 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 | False |
| artifact_bank | bic_like | 0.1880 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 | False |
| artifact_bank | parameter_count | 0.1700 | 0.5550 | 0.0200 | 0.2000 | 1.0000 | 0.0000 | 0.0900 | 0.8900 | 0.1600 | 5.0000 | False |
| combined_pypeec_aware | bic_like | 0.1640 | 0.6150 | 0.0300 | 0.4300 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 | False |
| combined_pypeec_aware | default_score | 0.1580 | 0.6100 | 0.0300 | 0.4100 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 | False |
| combined_pypeec_aware | parameter_count | 0.1560 | 0.6100 | 0.0200 | 0.4200 | 1.0000 | 0.0000 | 0.0200 | 0.9600 | 0.0945 | 9.0000 | False |
| combined_pypeec_aware | residual_only | 0.1550 | 0.6125 | 0.0000 | 0.4500 | 1.0000 | 0.0000 | 0.0400 | 0.9600 | 0.0945 | 9.0000 | False |
| artifact_bank | residual_only | 0.1510 | 0.5425 | 0.0000 | 0.1700 | 1.0000 | 0.0000 | 0.0500 | 0.9500 | 0.1600 | 5.0000 | False |

The objective is a fixed audit formula over PyPEEC frozen rows. It ranks trade-offs for analysis but is not used to tune the current PyPEEC predictions or thresholds.
