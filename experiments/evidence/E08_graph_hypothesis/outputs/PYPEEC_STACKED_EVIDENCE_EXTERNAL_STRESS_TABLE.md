# Exp08 P3 stacked evidence external/operator stress

| stress field | repeats | n cases | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | H0 false-any |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_finite | 31 | 400 | 0.9981 | 1.0000 | 0.9923 | 1.0000 | 1.0000 | 0.0000 |
| B_centerline | 31 | 400 | 0.9981 | 1.0000 | 0.9923 | 1.0000 | 1.0000 | 0.0000 |
| hidden_mechanism | 31 | 96 | 0.4382 | 0.9973 | 0.3777 | nan | 0.0000 | 0.0027 |

The calibrator is trained on PyPEEC calibration folds and evaluated on operator-shifted or hidden-mechanism fields. These are stress proxies, not real CAD/FEM/QDM validation.
