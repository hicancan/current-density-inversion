# Null-Via Selective Risk-Coverage

- enabled: `True`
- used for PyPEEC threshold selection: `False`
- boundary: Risk-coverage diagnostic for refusing low-confidence via/no-via decisions using the absolute generative evidence margin.

## Summary

| model | rows | risk @20% coverage | accuracy @20% coverage | full risk | full accuracy |
|---|---:|---:|---:|---:|---:|
| `unet_no_topology` | 400 | 0.300 | 0.700 | 0.450 | 0.550 |
| `unet_topology_soft_loss` | 400 | 0.287 | 0.713 | 0.385 | 0.615 |
| `unet_topology_two_stage_refined` | 400 | 0.312 | 0.688 | 0.455 | 0.545 |

## Risk-Coverage Rows

| model | coverage | selected | risk | accuracy | via precision | via recall | no-via FP selected | mean confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 0.100 | 40 | 0.425 | 0.575 | 0.500 | 0.118 | 0.087 | 0.134 |
| `unet_no_topology` | 0.200 | 80 | 0.300 | 0.700 | 0.727 | 0.276 | 0.059 | 0.117 |
| `unet_no_topology` | 0.350 | 140 | 0.321 | 0.679 | 0.632 | 0.240 | 0.078 | 0.101 |
| `unet_no_topology` | 0.500 | 200 | 0.345 | 0.655 | 0.586 | 0.230 | 0.095 | 0.088 |
| `unet_no_topology` | 0.650 | 260 | 0.392 | 0.608 | 0.571 | 0.257 | 0.139 | 0.076 |
| `unet_no_topology` | 0.800 | 320 | 0.409 | 0.591 | 0.614 | 0.293 | 0.156 | 0.067 |
| `unet_no_topology` | 1.000 | 400 | 0.450 | 0.550 | 0.591 | 0.325 | 0.225 | 0.055 |
| `unet_topology_soft_loss` | 0.100 | 40 | 0.400 | 0.600 | 0.552 | 0.842 | 0.619 | 0.142 |
| `unet_topology_soft_loss` | 0.200 | 80 | 0.287 | 0.713 | 0.696 | 0.780 | 0.359 | 0.108 |
| `unet_topology_soft_loss` | 0.350 | 140 | 0.257 | 0.743 | 0.750 | 0.789 | 0.312 | 0.087 |
| `unet_topology_soft_loss` | 0.500 | 200 | 0.265 | 0.735 | 0.755 | 0.733 | 0.263 | 0.074 |
| `unet_topology_soft_loss` | 0.650 | 260 | 0.296 | 0.704 | 0.739 | 0.657 | 0.246 | 0.064 |
| `unet_topology_soft_loss` | 0.800 | 320 | 0.353 | 0.647 | 0.650 | 0.596 | 0.305 | 0.055 |
| `unet_topology_soft_loss` | 1.000 | 400 | 0.385 | 0.615 | 0.628 | 0.565 | 0.335 | 0.046 |
| `unet_topology_two_stage_refined` | 0.100 | 40 | 0.400 | 0.600 | 0.600 | 1.000 | 1.000 | 0.126 |
| `unet_topology_two_stage_refined` | 0.200 | 80 | 0.312 | 0.688 | 0.692 | 0.982 | 0.960 | 0.099 |
| `unet_topology_two_stage_refined` | 0.350 | 140 | 0.350 | 0.650 | 0.626 | 0.963 | 0.767 | 0.078 |
| `unet_topology_two_stage_refined` | 0.500 | 200 | 0.400 | 0.600 | 0.590 | 0.891 | 0.756 | 0.066 |
| `unet_topology_two_stage_refined` | 0.650 | 260 | 0.381 | 0.619 | 0.592 | 0.875 | 0.661 | 0.057 |
| `unet_topology_two_stage_refined` | 0.800 | 320 | 0.419 | 0.581 | 0.566 | 0.825 | 0.682 | 0.049 |
| `unet_topology_two_stage_refined` | 1.000 | 400 | 0.455 | 0.545 | 0.533 | 0.725 | 0.635 | 0.040 |

Interpretation: selective prediction is a refusal metric. A useful system must report both accuracy and coverage, not only high-confidence examples.
