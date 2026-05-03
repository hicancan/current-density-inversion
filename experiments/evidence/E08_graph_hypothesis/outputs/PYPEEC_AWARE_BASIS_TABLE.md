# Exp08 P0 PyPEEC-aware graph basis-bank diagnostic

| field | basis mode | 4-way acc | H0 acc | H1 acc | H2 acc | via AUC | no-via FP | median residual | residual delta vs base |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | finite_width_sheet | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 0.0011 | -1.353e-05 |
| B_centerline | return_bank | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 0.0011 | 0.0000 |
| B_centerline | artifact_bank | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 0.0011 | 0.0000 |
| B_centerline | distributed_via | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4133 | 0.0010 | -3.351e-05 |
| B_centerline | combined_pypeec_aware | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4133 | 0.0010 | -4.942e-05 |
| B_pypeec | finite_width_sheet | 0.7700 | 0.0800 | 1.0000 | 1.0000 | 0.9998 | 0.3400 | 0.1042 | -0.0672 |
| B_pypeec | return_bank | 0.6800 | 0.0300 | 0.6900 | 1.0000 | 0.9534 | 0.3367 | 0.1573 | -0.0142 |
| B_pypeec | artifact_bank | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 0.9534 | 0.3367 | 0.1603 | -0.0111 |
| B_pypeec | distributed_via | 0.6850 | 0.0500 | 0.6900 | 1.0000 | 0.7441 | 0.4300 | 0.1724 | 9.800e-04 |
| B_pypeec | combined_pypeec_aware | 0.6100 | 0.0300 | 0.4100 | 1.0000 | 0.9798 | 0.4633 | 0.0945 | -0.0770 |

Basis-bank modes are fixed diagnostics: finite-width sheet, return bank, artifact bank, distributed via, and a combined mode. They do not use PyPEEC labels for selection.
