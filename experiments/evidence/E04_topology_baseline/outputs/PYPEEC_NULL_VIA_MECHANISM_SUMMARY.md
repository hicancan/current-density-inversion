# Real PyPEEC No-Via Mechanism Summary

This table aggregates only false-positive no-via rows. It quantifies which mechanisms dominate the current PyPEEC mini stress failures without selecting any PyPEEC-specific threshold.

| model | mechanism | count | % FP | mean s1 peak | mean topology MSE | mean B PyPEEC | mean gap | d trace | d bend | d return |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | `bend/corner induced residual` | 162 | 0.871 | 0.488 | 1.745 | 0.884 | 0.200 | 0.117 | 0.198 | n/a |
| `unet_no_topology` | `detector threshold sensitivity` | 15 | 0.081 | 0.332 | 1.304 | 0.896 | 0.188 | 0.067 | 4.482 | n/a |
| `unet_no_topology` | `model hallucination` | 2 | 0.011 | 0.469 | 1.144 | 0.632 | 0.073 | 0.000 | 7.500 | n/a |
| `unet_no_topology` | `operator mismatch` | 7 | 0.038 | 0.318 | 1.527 | 0.646 | 0.204 | 0.286 | 3.628 | n/a |
| `unet_topology_soft_loss` | `bend/corner induced residual` | 151 | 0.803 | 0.419 | 1.053 | 0.751 | 0.200 | 0.040 | 0.199 | n/a |
| `unet_topology_soft_loss` | `detector threshold sensitivity` | 6 | 0.032 | 0.326 | 1.178 | 0.677 | 0.188 | 0.000 | 3.667 | n/a |
| `unet_topology_soft_loss` | `model hallucination` | 4 | 0.021 | 0.344 | 0.847 | 0.615 | 0.135 | 0.000 | 4.500 | n/a |
| `unet_topology_soft_loss` | `operator mismatch` | 27 | 0.144 | 0.349 | 0.852 | 0.592 | 0.196 | 0.259 | 4.467 | n/a |
| `unet_topology_two_stage_refined` | `bend/corner induced residual` | 124 | 0.861 | 0.305 | 0.992 | 0.761 | 0.198 | 0.024 | 0.153 | n/a |
| `unet_topology_two_stage_refined` | `detector threshold sensitivity` | 4 | 0.028 | 0.238 | 1.164 | 0.670 | 0.161 | 0.000 | 4.000 | n/a |
| `unet_topology_two_stage_refined` | `model hallucination` | 2 | 0.014 | 0.276 | 0.864 | 0.557 | 0.128 | 0.000 | 4.000 | n/a |
| `unet_topology_two_stage_refined` | `operator mismatch` | 14 | 0.097 | 0.284 | 0.789 | 0.563 | 0.201 | 0.214 | 4.883 | n/a |

Interpretation: high bend/corner counts mean the dominant false-positive mechanism is local operator/geometric residual rather than random detector noise.
