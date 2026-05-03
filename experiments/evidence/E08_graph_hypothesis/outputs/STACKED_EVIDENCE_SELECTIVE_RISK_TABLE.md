# Exp08 P4 stacked evidence selective-risk table

| policy | coverage | repeats | accepted acc | accepted H0 acc | accepted H1 acc | accepted H0 false-any | H1 acceptance | reject rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fixed_alpha=100_confidence_margin | 0.2000 | 31 | 0.9919 | 1.0000 | 0.9787 | 0.0000 | 0.3116 | 0.8000 |
| fixed_alpha=100_confidence_margin | 0.5000 | 31 | 0.9965 | 1.0000 | 0.9834 | 0.0000 | 0.4310 | 0.5000 |
| fixed_alpha=100_confidence_margin | 0.8000 | 31 | 0.9978 | 1.0000 | 0.9877 | 0.0000 | 0.5794 | 0.2000 |
| fixed_alpha=100_confidence_margin | 1.0000 | 31 | 0.9963 | 0.9935 | 0.9916 | 0.0065 | 1.0000 | 0.0000 |

This table keeps refusal in the final diagnostic path. A strong calibrator should still expose coverage/risk rather than forcing every ambiguous residual into a hard label.
