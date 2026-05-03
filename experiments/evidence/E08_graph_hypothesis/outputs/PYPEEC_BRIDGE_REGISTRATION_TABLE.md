# Exp08 P0-next PyPEEC bridge with via-location marginalization

| field | mode | 4-way acc | H1 acc | via AUC | via recall | via F1 | no-via FP | median best offset um |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | base | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.3333 |  |
| B_centerline | via_location_marginalized | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 0.6667 | 240.0000 |
| B_pypeec | base | 0.7175 | 0.8200 | 0.9534 | 0.9900 | 0.6600 | 0.3367 |  |
| B_pypeec | via_location_marginalized | 0.7100 | 0.8200 | 0.5223 | 0.8600 | 0.4332 | 0.7033 | 240.0000 |

Offsets are fixed by configuration and are not selected on PyPEEC labels.
