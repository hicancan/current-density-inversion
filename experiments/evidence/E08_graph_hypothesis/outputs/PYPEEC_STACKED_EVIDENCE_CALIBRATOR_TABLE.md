# Exp08 P0 PyPEEC stacked evidence calibrator

| calibration policy | repeats | heldout 4-way mean | heldout 4-way std | heldout H0 mean | heldout H1 mean | heldout H2 mean | heldout H3 mean | heldout H0 false-any mean | heldout objective mean | heldout objective std | alpha counts | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inner_split_selected_alpha | 31 | 0.9897 | 0.0087 | 0.9684 | 0.9903 | 1.0000 | 1.0000 | 0.0316 | 3.6240 | 0.1800 | 0.0001:13, 0.001:1, 0.01:3, 0.1:1, 1:1, 10:3, 100:8, 300:1 | breakthrough_candidate |
| fixed_alpha=0.001 | 31 | 0.9844 | 0.0076 | 0.9606 | 0.9768 | 1.0000 | 1.0000 | 0.0394 | 3.5675 | 0.1674 |  | breakthrough_candidate |
| fixed_alpha=0.0001 | 31 | 0.9840 | 0.0078 | 0.9600 | 0.9761 | 1.0000 | 1.0000 | 0.0400 | 3.5634 | 0.1653 |  | breakthrough_candidate |
| fixed_alpha=0.01 | 31 | 0.9861 | 0.0062 | 0.9645 | 0.9800 | 1.0000 | 1.0000 | 0.0355 | 3.5915 | 0.1426 |  | breakthrough_candidate |
| fixed_alpha=0.1 | 31 | 0.9898 | 0.0068 | 0.9697 | 0.9897 | 1.0000 | 1.0000 | 0.0303 | 3.6299 | 0.1267 |  | breakthrough_candidate |
| fixed_alpha=1 | 31 | 0.9910 | 0.0061 | 0.9716 | 0.9923 | 1.0000 | 1.0000 | 0.0284 | 3.6431 | 0.1242 |  | breakthrough_candidate |
| fixed_alpha=10 | 31 | 0.9918 | 0.0058 | 0.9748 | 0.9923 | 1.0000 | 1.0000 | 0.0252 | 3.6599 | 0.1142 |  | breakthrough_candidate |
| fixed_alpha=100 | 31 | 0.9963 | 0.0036 | 0.9935 | 0.9916 | 1.0000 | 1.0000 | 0.0065 | 3.7564 | 0.0552 |  | breakthrough_candidate |
| fixed_alpha=1000 | 31 | 0.9890 | 0.0085 | 1.0000 | 0.9561 | 1.0000 | 1.0000 | 0.0000 | 3.7474 | 0.0406 |  | breakthrough_candidate |
| fixed_alpha=300 | 31 | 0.9929 | 0.0061 | 1.0000 | 0.9716 | 1.0000 | 1.0000 | 0.0000 | 3.7659 | 0.0291 |  | breakthrough_candidate |

This is the first explicit PyPEEC calibration/held-out evidence-fusion experiment in exp08. It trains a simple ridge one-vs-rest calibrator on calibration folds using all frozen basis/evidence scores as features, then evaluates held-out folds. It is not a frozen no-calibration claim; it tests whether the current evidence bank already contains enough information once legal calibration is allowed.
