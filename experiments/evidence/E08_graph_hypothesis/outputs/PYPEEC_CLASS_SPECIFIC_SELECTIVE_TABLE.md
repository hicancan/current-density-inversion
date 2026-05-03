# Exp08 P0 class-specific selective hypothesis audit

| policy | field | basis mode | evidence mode | repeats | coverage mean | coverage std | coverage p10 | coverage p90 | accepted acc mean | accepted acc std | H0 false-any mean | H0 false-any median | H0 accepted-correct mean | H1 accepted-correct mean | H1 acceptance mean | unknown mean | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| class_specific_margin_refusal | B_pypeec | finite_width_sheet | h0_conservative | 31 | 0.7163 | 0.0243 | 0.6850 | 0.7450 | 0.9836 | 0.0121 | 0.0245 | 0.0200 | 0.8633 | 0.9669 | 0.7006 | 0.2837 | h0_safe_but_h1_recall_limited |

This table is the formal audit of the current core bottleneck: class-specific refusal can carve out a trusted-output region, but a reliable detector also needs high true-via acceptance. Thresholds are selected only on calibration folds and evaluated on repeated held-out folds of the PyPEEC mini distribution.
