# Exp08 P2 stacked evidence unknown-safety stress

| policy | clean false reject target | repeats | clean reject | accepted clean acc | hidden reject | hidden accept | accepted hidden acc | accepted hidden risk | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fixed_alpha=100_inner_feature_distance | 0.2000 | 31 | 0.1802 | 0.9984 | 1.0000 | 0.0000 | nan | nan | low_hidden_exposure_candidate |
| fixed_alpha=100_inner_confidence_plus_distance | 0.2000 | 31 | 0.1777 | 0.9990 | 0.9318 | 0.0682 | 0.0526 | 0.9474 | strong_hidden_rejection_but_risk_tail |
| fixed_alpha=100_inner_confidence_margin | 0.2000 | 31 | 0.1706 | 0.9979 | 0.6791 | 0.3209 | 0.2197 | 0.7803 | diagnostic_only |

Each threshold is selected only inside the PyPEEC calibration fold and then applied to held-out PyPEEC and hidden-mechanism stress. Confidence-margin rejection tests classifier uncertainty; feature-distance rejection tests whether a stacked-evidence vector is outside the calibrated in-library class manifold; the combined row is an ablation rather than a tuned production rule.
