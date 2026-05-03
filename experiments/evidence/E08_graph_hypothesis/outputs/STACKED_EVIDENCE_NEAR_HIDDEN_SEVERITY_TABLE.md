# Exp08 near-boundary hidden severity sweep

| policy | severity | repeats | clean reject | accepted clean acc | hidden reject | hidden accept | accepted hidden acc | accepted hidden risk | median unknown signal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| confidence_margin | 0.25 | 31 | 0.1706 | 0.9979 | 0.7077 | 0.2923 | 0.8718 | 0.1282 | -0.4981 |
| confidence_margin | 0.50 | 31 | 0.1706 | 0.9979 | 0.7833 | 0.2167 | 0.9534 | 0.0466 | -0.4474 |
| confidence_margin | 1.00 | 31 | 0.1706 | 0.9979 | 0.7450 | 0.2550 | 0.9835 | 0.0165 | -0.3815 |
| confidence_margin | 1.50 | 31 | 0.1706 | 0.9979 | 0.7440 | 0.2560 | 1.0000 | 0.0000 | -0.3368 |
| feature_distance | 0.25 | 31 | 0.1802 | 0.9984 | 0.9990 | 0.0010 | 1.0000 | 0.0000 | 0.7813 |
| feature_distance | 0.50 | 31 | 0.1802 | 0.9984 | 0.9345 | 0.0655 | 1.0000 | 0.0000 | 0.7115 |
| feature_distance | 1.00 | 31 | 0.1802 | 0.9984 | 0.8659 | 0.1341 | 1.0000 | 0.0000 | 0.6735 |
| feature_distance | 1.50 | 31 | 0.1802 | 0.9984 | 0.8165 | 0.1835 | 1.0000 | 0.0000 | 0.6161 |

This sweep varies near-boundary hidden strength and displacement. It reports how refusal and accepted risk change as hidden mechanisms move closer to or farther from the calibrated evidence manifold.
