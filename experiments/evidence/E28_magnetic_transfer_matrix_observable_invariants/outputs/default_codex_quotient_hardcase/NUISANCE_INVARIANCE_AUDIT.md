# Nuisance Invariance Audit

## Perturbation Types

- height_jitter
- gain_variation

## Per-Hypothesis Nuisance Radii (worst-case across perturbations)

| hypothesis | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|
| H0_no_via | 0.798817 | 0.053393 | 0.035270 | 1.234101 |
| H1_via | 0.613093 | 0.088068 | 0.025192 | 0.899365 |
| H2_model_gap | 0.612718 | 0.087726 | 0.025291 | 0.899986 |
| H3_return_path | 0.626245 | 0.053452 | 0.037428 | 0.987856 |

## Detailed Perturbation Results

| hypothesis | type | magnitude | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|---:|---:|
| H0_no_via | height_jitter | 0.0020 | 0.081803 | 0.005032 | 0.003629 | 0.126509 |
| H0_no_via | height_jitter | 0.0050 | 0.203695 | 0.012551 | 0.009028 | 0.314959 |
| H0_no_via | height_jitter | 0.0100 | 0.404702 | 0.025009 | 0.017914 | 0.625583 |
| H0_no_via | height_jitter | 0.0200 | 0.798817 | 0.049655 | 0.035270 | 1.234101 |
| H0_no_via | gain_variation | 0.0020 | 0.048697 | 0.005342 | 0.000799 | 0.073267 |
| H0_no_via | gain_variation | 0.0050 | 0.121741 | 0.013354 | 0.001997 | 0.183167 |
| H0_no_via | gain_variation | 0.0100 | 0.243483 | 0.026704 | 0.003990 | 0.366334 |
| H0_no_via | gain_variation | 0.0200 | 0.486965 | 0.053393 | 0.007962 | 0.732667 |
| H1_via | height_jitter | 0.0020 | 0.062669 | 0.008953 | 0.002595 | 0.091921 |
| H1_via | height_jitter | 0.0050 | 0.156098 | 0.022330 | 0.006455 | 0.228964 |
| H1_via | height_jitter | 0.0100 | 0.310293 | 0.044468 | 0.012804 | 0.455151 |
| H1_via | height_jitter | 0.0200 | 0.613093 | 0.088068 | 0.025192 | 0.899365 |
| H1_via | gain_variation | 0.0020 | 0.041086 | 0.005368 | 0.000840 | 0.060695 |
| H1_via | gain_variation | 0.0050 | 0.102716 | 0.013419 | 0.002099 | 0.151737 |
| H1_via | gain_variation | 0.0100 | 0.205432 | 0.026834 | 0.004192 | 0.303474 |
| H1_via | gain_variation | 0.0200 | 0.410865 | 0.053646 | 0.008404 | 0.606949 |
| H2_model_gap | height_jitter | 0.0020 | 0.062631 | 0.008921 | 0.002605 | 0.091988 |
| H2_model_gap | height_jitter | 0.0050 | 0.156003 | 0.022249 | 0.006480 | 0.229127 |
| H2_model_gap | height_jitter | 0.0100 | 0.310104 | 0.044303 | 0.012854 | 0.455473 |
| H2_model_gap | height_jitter | 0.0200 | 0.612718 | 0.087726 | 0.025291 | 0.899986 |
| H2_model_gap | gain_variation | 0.0020 | 0.041058 | 0.005372 | 0.000843 | 0.060702 |
| H2_model_gap | gain_variation | 0.0050 | 0.102645 | 0.013428 | 0.002107 | 0.151755 |
| H2_model_gap | gain_variation | 0.0100 | 0.205290 | 0.026852 | 0.004209 | 0.303511 |
| H2_model_gap | gain_variation | 0.0200 | 0.410580 | 0.053682 | 0.008395 | 0.607022 |
| H3_return_path | height_jitter | 0.0020 | 0.064205 | 0.004421 | 0.003844 | 0.101387 |
| H3_return_path | height_jitter | 0.0050 | 0.159842 | 0.011019 | 0.009568 | 0.252363 |
| H3_return_path | height_jitter | 0.0100 | 0.317469 | 0.021929 | 0.018993 | 0.501082 |
| H3_return_path | height_jitter | 0.0200 | 0.626245 | 0.043427 | 0.037428 | 0.987856 |
| H3_return_path | gain_variation | 0.0020 | 0.039131 | 0.005348 | 0.000836 | 0.059615 |
| H3_return_path | gain_variation | 0.0050 | 0.097826 | 0.013368 | 0.002091 | 0.149038 |
| H3_return_path | gain_variation | 0.0100 | 0.195653 | 0.026734 | 0.004190 | 0.298076 |
| H3_return_path | gain_variation | 0.0200 | 0.391305 | 0.053452 | 0.008406 | 0.596151 |