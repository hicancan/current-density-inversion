# Exp08 near-boundary hidden stress with stacked-evidence OOD screens

| policy | clean false reject target | repeats | clean reject | accepted clean acc | near-hidden reject | near-hidden accept | accepted near-hidden acc | accepted near-hidden risk | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fixed_alpha=100_inner_feature_distance | 0.2000 | 31 | 0.1802 | 0.9984 | 0.8508 | 0.1492 | 1.0000 | 0.0000 | low_accepted_hidden_risk_candidate |
| fixed_alpha=100_inner_confidence_plus_distance | 0.2000 | 31 | 0.1777 | 0.9990 | 0.8051 | 0.1949 | 1.0000 | 0.0000 | low_accepted_hidden_risk_candidate |
| fixed_alpha=100_inner_confidence_margin | 0.2000 | 31 | 0.1706 | 0.9979 | 0.7792 | 0.2208 | 0.9705 | 0.0295 | low_accepted_hidden_risk_candidate |

Near-boundary hidden cases are intentionally closer to known return/via/artifact candidates than the base hidden stress. This table tests whether the distance screen only rejects obvious outliers or also protects against harder near-manifold unknowns.
