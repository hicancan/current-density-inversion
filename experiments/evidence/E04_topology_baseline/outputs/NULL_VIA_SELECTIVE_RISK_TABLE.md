# Null-Via Selective Risk-Coverage

- enabled: `True`
- used for PyPEEC threshold selection: `False`
- boundary: Risk-coverage diagnostic for refusing low-confidence via/no-via decisions using the absolute generative evidence margin.

## Summary

| model | rows | risk @20% coverage | accuracy @20% coverage | full risk | full accuracy |
|---|---:|---:|---:|---:|---:|
| `unet_no_topology` | 400 | 0.338 | 0.662 | 0.455 | 0.545 |
| `unet_topology_soft_loss` | 400 | 0.287 | 0.713 | 0.307 | 0.693 |
| `unet_topology_two_stage_refined` | 400 | 0.200 | 0.800 | 0.398 | 0.603 |

## Risk-Coverage Rows

| model | coverage | selected | risk | accuracy | via precision | via recall | no-via FP selected | mean confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 0.100 | 40 | 0.325 | 0.675 | 0.833 | 0.294 | 0.043 | 0.141 |
| `unet_no_topology` | 0.200 | 80 | 0.338 | 0.662 | 0.800 | 0.242 | 0.043 | 0.121 |
| `unet_no_topology` | 0.350 | 140 | 0.371 | 0.629 | 0.583 | 0.250 | 0.119 | 0.104 |
| `unet_no_topology` | 0.500 | 200 | 0.395 | 0.605 | 0.528 | 0.235 | 0.143 | 0.089 |
| `unet_no_topology` | 0.650 | 260 | 0.404 | 0.596 | 0.560 | 0.252 | 0.148 | 0.078 |
| `unet_no_topology` | 0.800 | 320 | 0.438 | 0.562 | 0.545 | 0.247 | 0.172 | 0.068 |
| `unet_no_topology` | 1.000 | 400 | 0.455 | 0.545 | 0.596 | 0.280 | 0.190 | 0.056 |
| `unet_topology_soft_loss` | 0.100 | 40 | 0.200 | 0.800 | 0.900 | 0.844 | 0.375 | 0.139 |
| `unet_topology_soft_loss` | 0.200 | 80 | 0.287 | 0.713 | 0.820 | 0.745 | 0.360 | 0.115 |
| `unet_topology_soft_loss` | 0.350 | 140 | 0.286 | 0.714 | 0.770 | 0.713 | 0.283 | 0.095 |
| `unet_topology_soft_loss` | 0.500 | 200 | 0.295 | 0.705 | 0.760 | 0.670 | 0.253 | 0.081 |
| `unet_topology_soft_loss` | 0.650 | 260 | 0.281 | 0.719 | 0.769 | 0.674 | 0.230 | 0.071 |
| `unet_topology_soft_loss` | 0.800 | 320 | 0.287 | 0.713 | 0.741 | 0.669 | 0.242 | 0.062 |
| `unet_topology_soft_loss` | 1.000 | 400 | 0.307 | 0.693 | 0.708 | 0.655 | 0.270 | 0.052 |
| `unet_topology_two_stage_refined` | 0.100 | 40 | 0.075 | 0.925 | 0.949 | 0.974 | 1.000 | 0.125 |
| `unet_topology_two_stage_refined` | 0.200 | 80 | 0.200 | 0.800 | 0.829 | 0.955 | 0.929 | 0.101 |
| `unet_topology_two_stage_refined` | 0.350 | 140 | 0.293 | 0.707 | 0.721 | 0.926 | 0.756 | 0.082 |
| `unet_topology_two_stage_refined` | 0.500 | 200 | 0.345 | 0.655 | 0.650 | 0.898 | 0.695 | 0.069 |
| `unet_topology_two_stage_refined` | 0.650 | 260 | 0.350 | 0.650 | 0.641 | 0.864 | 0.628 | 0.059 |
| `unet_topology_two_stage_refined` | 0.800 | 320 | 0.381 | 0.619 | 0.600 | 0.821 | 0.605 | 0.052 |
| `unet_topology_two_stage_refined` | 1.000 | 400 | 0.398 | 0.603 | 0.574 | 0.795 | 0.590 | 0.042 |

Interpretation: selective prediction is a refusal metric. A useful system must report both accuracy and coverage, not only high-confidence examples.
