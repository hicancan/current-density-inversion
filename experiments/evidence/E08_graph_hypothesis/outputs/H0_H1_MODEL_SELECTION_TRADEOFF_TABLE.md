# Exp08 P1 H0/H1 model-selection trade-off table

| basis mode | evidence mode | heldout H0 acc | heldout H1 acc | heldout 4-way acc | heldout H0 false H1 | heldout H0 false H2 | heldout H0 false H3 | heldout median residual | heldout median params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finite_width_sheet | h0_conservative | 0.9400 | 1.0000 | 0.9850 | 0.0000 | 0.0000 | 0.0600 | 0.1061 | 5.0000 |
| combined_pypeec_aware | h0_conservative | 0.8000 | 0.3000 | 0.7750 | 0.0000 | 0.0000 | 0.2000 | 0.1097 | 9.0000 |
| finite_width_sheet | extra_count | 0.7600 | 1.0000 | 0.9400 | 0.0000 | 0.0400 | 0.2000 | 0.1050 | 5.0000 |
| artifact_bank | h0_conservative | 0.7400 | 0.6200 | 0.8400 | 0.0000 | 0.1400 | 0.1200 | 0.1772 | 4.0000 |
| combined_pypeec_aware | extra_count | 0.7000 | 0.4400 | 0.7850 | 0.0000 | 0.0000 | 0.3000 | 0.1074 | 9.0000 |
| base | h0_conservative | 0.6200 | 0.6400 | 0.8150 | 0.0000 | 0.1000 | 0.2800 | 0.1766 | 4.0000 |
| distributed_via | h0_conservative | 0.6200 | 0.0800 | 0.6750 | 0.0000 | 0.1000 | 0.2800 | 0.1766 | 3.0000 |
| artifact_bank | extra_count | 0.5600 | 0.8200 | 0.8450 | 0.0000 | 0.2800 | 0.1600 | 0.1766 | 4.0000 |
| return_bank | h0_conservative | 0.5000 | 0.6200 | 0.7800 | 0.0000 | 0.2800 | 0.2200 | 0.1614 | 5.0000 |
| base | extra_count | 0.4200 | 0.8400 | 0.8150 | 0.0000 | 0.2200 | 0.3600 | 0.1766 | 4.0000 |
| distributed_via | extra_count | 0.4200 | 0.1400 | 0.6400 | 0.0000 | 0.2200 | 0.3600 | 0.1766 | 4.0000 |
| return_bank | extra_count | 0.3800 | 0.8200 | 0.8000 | 0.0000 | 0.3200 | 0.3000 | 0.1605 | 5.0000 |
| finite_width_sheet | bic_like | 0.2000 | 1.0000 | 0.8000 | 0.0200 | 0.1600 | 0.6200 | 0.1042 | 5.0000 |
| finite_width_sheet | default_score | 0.1200 | 1.0000 | 0.7800 | 0.0400 | 0.1600 | 0.6800 | 0.1042 | 5.0000 |
| base | bic_like | 0.0800 | 0.9000 | 0.7450 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| base | default_score | 0.0800 | 0.9000 | 0.7450 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| distributed_via | default_score | 0.0800 | 0.8600 | 0.7350 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| distributed_via | bic_like | 0.0800 | 0.8000 | 0.7200 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| finite_width_sheet | parameter_count | 0.0600 | 1.0000 | 0.7650 | 0.0800 | 0.1800 | 0.6800 | 0.1042 | 5.0000 |
| return_bank | bic_like | 0.0600 | 0.7800 | 0.7100 | 0.0000 | 0.6200 | 0.3200 | 0.1594 | 6.0000 |
| base | parameter_count | 0.0400 | 0.9000 | 0.7350 | 0.0000 | 0.3400 | 0.6200 | 0.1766 | 4.0000 |
| distributed_via | parameter_count | 0.0400 | 0.9000 | 0.7350 | 0.0000 | 0.3400 | 0.6200 | 0.1766 | 4.0000 |
| return_bank | default_score | 0.0400 | 0.7800 | 0.7050 | 0.0000 | 0.6600 | 0.3000 | 0.1589 | 6.0000 |
| return_bank | parameter_count | 0.0200 | 0.7800 | 0.7000 | 0.0000 | 0.7000 | 0.2800 | 0.1589 | 6.0000 |
| combined_pypeec_aware | bic_like | 0.0200 | 0.6200 | 0.6600 | 0.0000 | 0.0200 | 0.9600 | 0.0970 | 9.0000 |
| combined_pypeec_aware | default_score | 0.0200 | 0.5800 | 0.6500 | 0.0000 | 0.0200 | 0.9600 | 0.0970 | 9.0000 |
| combined_pypeec_aware | parameter_count | 0.0200 | 0.5600 | 0.6450 | 0.0000 | 0.0000 | 0.9800 | 0.0970 | 9.0000 |
| artifact_bank | bic_like | 0.0200 | 0.3000 | 0.5800 | 0.0000 | 0.0600 | 0.9200 | 0.1710 | 5.0000 |
| artifact_bank | default_score | 0.0200 | 0.3000 | 0.5800 | 0.0000 | 0.0600 | 0.9200 | 0.1710 | 5.0000 |
| artifact_bank | parameter_count | 0.0200 | 0.2200 | 0.5600 | 0.0000 | 0.0200 | 0.9600 | 0.1710 | 5.0000 |
| finite_width_sheet | residual_only | 0.0000 | 1.0000 | 0.7500 | 0.0800 | 0.1800 | 0.7400 | 0.1042 | 5.0000 |
| base | residual_only | 0.0000 | 0.9000 | 0.7250 | 0.0200 | 0.3400 | 0.6400 | 0.1766 | 4.0000 |
| distributed_via | residual_only | 0.0000 | 0.9000 | 0.7250 | 0.0800 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| return_bank | residual_only | 0.0000 | 0.7800 | 0.6950 | 0.0000 | 0.7600 | 0.2400 | 0.1589 | 6.0000 |
| combined_pypeec_aware | residual_only | 0.0000 | 0.5600 | 0.6400 | 0.0000 | 0.0200 | 0.9800 | 0.0970 | 9.0000 |
| artifact_bank | residual_only | 0.0000 | 0.2200 | 0.5550 | 0.0000 | 0.0000 | 1.0000 | 0.1710 | 5.0000 |

This table treats H0/no-via safety and H1/true-via recall as primary endpoints rather than secondary columns hidden inside overall accuracy.
