# Exp08 few-shot family adaptation audit

| heldout family | shots from family | train n | eval n | raw acc | raw H0 false-any | distance reject | accepted acc | accepted risk | accepted H0 false-any | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bend_artifact | 0 | 300 | 100 | 0.0000 | nan | 1.0000 | nan | nan | nan | zero_shot_family_refusal_baseline |
| bend_artifact | 2 | 302 | 98 | 1.0000 | nan | 0.4796 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| bend_artifact | 5 | 305 | 95 | 1.0000 | nan | 0.4105 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| bend_artifact | 10 | 310 | 90 | 1.0000 | nan | 0.3667 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| canonical | 0 | 395 | 5 | 0.8000 | 0.0000 | 1.0000 | nan | nan | nan | zero_shot_family_refusal_baseline |
| canonical | 2 | 397 | 3 | 1.0000 | 0.0000 | 1.0000 | nan | nan | nan | still_mostly_refusal |
| canonical | 5 | 399 | 1 | 1.0000 | 0.0000 | 1.0000 | nan | nan | nan | still_mostly_refusal |
| canonical | 10 | 399 | 1 | 1.0000 | 0.0000 | 1.0000 | nan | nan | nan | still_mostly_refusal |
| dense_via_background | 0 | 368 | 32 | 0.4688 | nan | 1.0000 | nan | nan | nan | zero_shot_family_refusal_baseline |
| dense_via_background | 2 | 370 | 30 | 0.7000 | nan | 1.0000 | nan | nan | nan | still_mostly_refusal |
| dense_via_background | 5 | 373 | 27 | 0.7407 | nan | 1.0000 | nan | nan | nan | still_mostly_refusal |
| dense_via_background | 10 | 378 | 22 | 1.0000 | nan | 1.0000 | nan | nan | nan | still_mostly_refusal |
| l1_jog | 0 | 367 | 33 | 0.0000 | nan | 1.0000 | nan | nan | nan | zero_shot_family_refusal_baseline |
| l1_jog | 2 | 369 | 31 | 0.7097 | nan | 1.0000 | nan | nan | nan | still_mostly_refusal |
| l1_jog | 5 | 372 | 28 | 0.8571 | nan | 1.0000 | nan | nan | nan | still_mostly_refusal |
| l1_jog | 10 | 377 | 23 | 0.9130 | nan | 1.0000 | nan | nan | nan | still_mostly_refusal |
| multi_via | 0 | 367 | 33 | 1.0000 | nan | 0.5152 | 1.0000 | 0.0000 | nan | zero_shot_family_refusal_baseline |
| multi_via | 2 | 369 | 31 | 1.0000 | nan | 0.4516 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| multi_via | 5 | 372 | 28 | 1.0000 | nan | 0.5000 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| multi_via | 10 | 377 | 23 | 1.0000 | nan | 0.4783 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| no_via_background | 0 | 303 | 97 | 0.0000 | 1.0000 | 1.0000 | nan | nan | nan | zero_shot_family_refusal_baseline |
| no_via_background | 2 | 305 | 95 | 0.4632 | 0.5368 | 0.8737 | 0.8333 | 0.1667 | 0.1667 | still_mostly_refusal |
| no_via_background | 5 | 308 | 92 | 0.9674 | 0.0326 | 0.5000 | 1.0000 | 0.0000 | 0.0000 | fewshot_adaptation_candidate |
| no_via_background | 10 | 313 | 87 | 0.9655 | 0.0345 | 0.1264 | 0.9868 | 0.0132 | 0.0132 | fewshot_adaptation_candidate |
| return_path | 0 | 300 | 100 | 0.0000 | nan | 1.0000 | nan | nan | nan | zero_shot_family_refusal_baseline |
| return_path | 2 | 302 | 98 | 1.0000 | nan | 0.5000 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| return_path | 5 | 305 | 95 | 1.0000 | nan | 0.4842 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| return_path | 10 | 310 | 90 | 1.0000 | nan | 0.3778 | 1.0000 | 0.0000 | nan | fewshot_adaptation_candidate |
| AGGREGATE_FAMILIES | 0 | 7 | 7 | 0.3241 | nan | 0.9307 | 1.0000 | 0.0000 | nan | fewshot_aggregate |
| AGGREGATE_FAMILIES | 2 | 7 | 7 | 0.8390 | nan | 0.7578 | 0.9583 | 0.0417 | 0.1667 | fewshot_aggregate |
| AGGREGATE_FAMILIES | 5 | 7 | 7 | 0.9379 | nan | 0.6992 | 1.0000 | 0.0000 | 0.0000 | fewshot_aggregate |
| AGGREGATE_FAMILIES | 10 | 7 | 7 | 0.9827 | nan | 0.6213 | 0.9967 | 0.0033 | 0.0132 | fewshot_aggregate |

This table tests whether an unseen generated family can move from safe refusal toward useful diagnosis after a small number of family-specific calibration samples. Shots are added only to the calibration side; the remaining family rows are evaluated held out.
