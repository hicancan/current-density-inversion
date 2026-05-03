# Exp08 P1 global graph-to-field registration diagnostic

| field | mode | 4-way acc | via AUC | no-via FP | median residual | median translation um | median abs rotation deg | median scale delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | base | 1.0000 | 1.0000 | 0.3333 | 0.0011 |  |  |  |
| B_centerline | global_registration_search | 1.0000 | 1.0000 | 0.3333 | 0.0011 | 0.0000 | 0.0000 | 0.0000 |
| B_pypeec | base | 0.7175 | 0.9534 | 0.3367 | 0.1715 |  |  |  |
| B_pypeec | global_registration_search | 0.7250 | 0.9546 | 0.3367 | 0.1666 | 0.0000 | 0.0000 | 0.0150 |

The transform grid is fixed by config and is not selected on PyPEEC labels.
