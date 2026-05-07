# Nuisance Invariance Audit

## Perturbation Types

- height_jitter
- gain_variation

## Per-Hypothesis Nuisance Radii (worst-case across perturbations)

| hypothesis | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|
| H0_no_via | 1.072278 | 0.066934 | 0.047263 | 1.655915 |
| H1_via | 0.823572 | 0.118377 | 0.033742 | 1.208167 |
| H2_model_gap | 0.823066 | 0.117904 | 0.033874 | 1.208989 |
| H3_return_path | 0.840283 | 0.058430 | 0.050187 | 1.324930 |

## Detailed Perturbation Results

| hypothesis | type | magnitude | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|---:|---:|
| H0_no_via | height_jitter | 0.0020 | 0.110727 | 0.006814 | 0.004911 | 0.171231 |
| H0_no_via | height_jitter | 0.0050 | 0.275328 | 0.016982 | 0.012198 | 0.425676 |
| H0_no_via | height_jitter | 0.0100 | 0.545748 | 0.033796 | 0.024135 | 0.843439 |
| H0_no_via | height_jitter | 0.0200 | 1.072278 | 0.066934 | 0.047263 | 1.655915 |
| H0_no_via | gain_variation | 0.0020 | 0.043918 | 0.004910 | 0.000789 | 0.066495 |
| H0_no_via | gain_variation | 0.0050 | 0.109796 | 0.012276 | 0.001976 | 0.166238 |
| H0_no_via | gain_variation | 0.0100 | 0.219592 | 0.024556 | 0.003965 | 0.332475 |
| H0_no_via | gain_variation | 0.0200 | 0.439185 | 0.049127 | 0.007981 | 0.664951 |
| H1_via | height_jitter | 0.0020 | 0.084834 | 0.012124 | 0.003511 | 0.124432 |
| H1_via | height_jitter | 0.0050 | 0.211030 | 0.030209 | 0.008720 | 0.309542 |
| H1_via | height_jitter | 0.0100 | 0.418586 | 0.060050 | 0.017247 | 0.614015 |
| H1_via | height_jitter | 0.0200 | 0.823572 | 0.118377 | 0.033742 | 1.208167 |
| H1_via | gain_variation | 0.0020 | 0.036864 | 0.004901 | 0.000792 | 0.054923 |
| H1_via | gain_variation | 0.0050 | 0.092160 | 0.012254 | 0.001985 | 0.137308 |
| H1_via | gain_variation | 0.0100 | 0.184320 | 0.024515 | 0.003983 | 0.274616 |
| H1_via | gain_variation | 0.0200 | 0.368640 | 0.049050 | 0.008021 | 0.549232 |
| H2_model_gap | height_jitter | 0.0020 | 0.084782 | 0.012080 | 0.003525 | 0.124521 |
| H2_model_gap | height_jitter | 0.0050 | 0.210901 | 0.030099 | 0.008754 | 0.309762 |
| H2_model_gap | height_jitter | 0.0100 | 0.418331 | 0.059823 | 0.017314 | 0.614445 |
| H2_model_gap | height_jitter | 0.0200 | 0.823066 | 0.117904 | 0.033874 | 1.208989 |
| H2_model_gap | gain_variation | 0.0020 | 0.036835 | 0.004900 | 0.000789 | 0.054914 |
| H2_model_gap | gain_variation | 0.0050 | 0.092087 | 0.012252 | 0.001977 | 0.137286 |
| H2_model_gap | gain_variation | 0.0100 | 0.184174 | 0.024509 | 0.003969 | 0.274572 |
| H2_model_gap | gain_variation | 0.0200 | 0.368348 | 0.049039 | 0.007992 | 0.549143 |
| H3_return_path | height_jitter | 0.0020 | 0.086902 | 0.005986 | 0.005203 | 0.137222 |
| H3_return_path | height_jitter | 0.0050 | 0.216027 | 0.014903 | 0.012928 | 0.341034 |
| H3_return_path | height_jitter | 0.0100 | 0.428016 | 0.029606 | 0.025597 | 0.675423 |
| H3_return_path | height_jitter | 0.0200 | 0.840283 | 0.058430 | 0.050187 | 1.324930 |
| H3_return_path | gain_variation | 0.0020 | 0.035105 | 0.004901 | 0.000906 | 0.053658 |
| H3_return_path | gain_variation | 0.0050 | 0.087763 | 0.012254 | 0.002268 | 0.134146 |
| H3_return_path | gain_variation | 0.0100 | 0.175525 | 0.024513 | 0.004547 | 0.268292 |
| H3_return_path | gain_variation | 0.0200 | 0.351051 | 0.049044 | 0.009142 | 0.536583 |