# Nuisance Invariance Audit

## Perturbation Types

- height_jitter
- gain_variation

## Per-Hypothesis Nuisance Radii (worst-case across perturbations)

| hypothesis | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|
| H0_no_via | 0.725007 | 0.079539 | 0.025795 | 1.281813 |
| H1_via | 0.643989 | 0.103370 | 0.014836 | 1.087468 |
| H2_model_gap | 0.643692 | 0.103020 | 0.015007 | 1.087398 |
| H3_return_path | 0.587605 | 0.081319 | 0.022853 | 1.032804 |

## Detailed Perturbation Results

| hypothesis | type | magnitude | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|---:|---:|
| H0_no_via | height_jitter | 0.0100 | 0.177172 | 0.012337 | 0.006271 | 0.313505 |
| H0_no_via | height_jitter | 0.0400 | 0.725007 | 0.049569 | 0.025795 | 1.281813 |
| H0_no_via | gain_variation | 0.0100 | 0.177756 | 0.019858 | 0.003446 | 0.317809 |
| H0_no_via | gain_variation | 0.0400 | 0.711025 | 0.079539 | 0.013931 | 1.271236 |
| H1_via | height_jitter | 0.0100 | 0.151393 | 0.025650 | 0.003596 | 0.247555 |
| H1_via | height_jitter | 0.0400 | 0.618696 | 0.103370 | 0.014836 | 1.010413 |
| H1_via | gain_variation | 0.0100 | 0.160997 | 0.020393 | 0.003425 | 0.271867 |
| H1_via | gain_variation | 0.0400 | 0.643989 | 0.081618 | 0.013829 | 1.087468 |
| H2_model_gap | height_jitter | 0.0100 | 0.151340 | 0.025553 | 0.003638 | 0.247708 |
| H2_model_gap | height_jitter | 0.0400 | 0.618484 | 0.103020 | 0.015007 | 1.011071 |
| H2_model_gap | gain_variation | 0.0100 | 0.160923 | 0.020405 | 0.003422 | 0.271850 |
| H2_model_gap | gain_variation | 0.0400 | 0.643692 | 0.081667 | 0.013817 | 1.087398 |
| H3_return_path | height_jitter | 0.0100 | 0.142257 | 0.010309 | 0.005550 | 0.247556 |
| H3_return_path | height_jitter | 0.0400 | 0.582954 | 0.041986 | 0.022853 | 1.013550 |
| H3_return_path | gain_variation | 0.0100 | 0.146901 | 0.020313 | 0.003430 | 0.258201 |
| H3_return_path | gain_variation | 0.0400 | 0.587605 | 0.081319 | 0.013858 | 1.032804 |