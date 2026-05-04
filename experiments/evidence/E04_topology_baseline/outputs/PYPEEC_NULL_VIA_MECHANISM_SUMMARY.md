# Real PyPEEC No-Via Mechanism Summary

This table aggregates only false-positive no-via rows. It quantifies which mechanisms dominate the current PyPEEC mini stress failures without selecting any PyPEEC-specific threshold.

| model | mechanism | count | % FP | mean s1 peak | mean topology MSE | mean B PyPEEC | mean gap | d trace | d bend | d return |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | `bend/corner induced residual` | 155 | 0.833 | 0.493 | 1.806 | 0.912 | 0.200 | 0.110 | 0.168 | n/a |
| `unet_no_topology` | `detector threshold sensitivity` | 16 | 0.086 | 0.370 | 1.358 | 0.803 | 0.191 | 0.062 | 4.015 | n/a |
| `unet_no_topology` | `model hallucination` | 2 | 0.011 | 0.459 | 1.055 | 0.657 | 0.073 | 0.000 | 7.500 | n/a |
| `unet_no_topology` | `operator mismatch` | 13 | 0.070 | 0.315 | 1.329 | 0.677 | 0.200 | 0.154 | 4.563 | n/a |
| `unet_topology_soft_loss` | `bend/corner induced residual` | 146 | 0.764 | 0.436 | 1.022 | 0.726 | 0.199 | 0.103 | 0.219 | n/a |
| `unet_topology_soft_loss` | `detector threshold sensitivity` | 6 | 0.031 | 0.456 | 1.019 | 0.675 | 0.213 | 0.500 | 2.900 | n/a |
| `unet_topology_soft_loss` | `model hallucination` | 7 | 0.037 | 0.461 | 0.758 | 0.619 | 0.134 | 0.000 | 4.714 | n/a |
| `unet_topology_soft_loss` | `operator mismatch` | 32 | 0.168 | 0.408 | 0.782 | 0.592 | 0.197 | 0.062 | 4.850 | n/a |
| `unet_topology_two_stage_refined` | `bend/corner induced residual` | 107 | 0.743 | 0.334 | 0.982 | 0.731 | 0.199 | 0.056 | 0.121 | n/a |
| `unet_topology_two_stage_refined` | `detector threshold sensitivity` | 6 | 0.042 | 0.296 | 0.953 | 0.666 | 0.213 | 0.500 | 2.900 | n/a |
| `unet_topology_two_stage_refined` | `model hallucination` | 5 | 0.035 | 0.348 | 0.712 | 0.618 | 0.136 | 0.000 | 4.200 | n/a |
| `unet_topology_two_stage_refined` | `operator mismatch` | 26 | 0.181 | 0.290 | 0.742 | 0.574 | 0.195 | 0.077 | 4.777 | n/a |

Interpretation: high bend/corner counts mean the dominant false-positive mechanism is local operator/geometric residual rather than random detector noise.
