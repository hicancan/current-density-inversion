# Exp08 P0 stacked evidence group-heldout stress

| group policy | heldout group | heldout n | train n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | H0 false-any | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| variant_mod5 | canonical | 11 | 389 | 0.9091 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 0.0000 | evaluated |
| variant_mod5 | variant_mod_0 | 75 | 325 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | evaluated |
| variant_mod5 | variant_mod_1 | 81 | 319 | 0.9877 | 0.9500 | 1.0000 | 1.0000 | 1.0000 | 0.0500 | evaluated |
| variant_mod5 | variant_mod_2 | 79 | 321 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | evaluated |
| variant_mod5 | variant_mod_3 | 77 | 323 | 0.9870 | 0.9474 | 1.0000 | 1.0000 | 1.0000 | 0.0526 | evaluated |
| variant_mod5 | variant_mod_4 | 77 | 323 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | evaluated |
| variant_mod5 | AGGREGATE_EVALUATED_FOLDS | 6 | 6 | 0.9806 | 0.9829 | 0.9667 | 1.0000 | 1.0000 | 0.0171 | std_acc=0.0325 |
| case_family | bend_artifact | 100 | 300 | nan | nan | nan | nan | nan | nan | skipped_train_missing_eval_class |
| case_family | canonical | 5 | 395 | 0.8000 | 1.0000 | 0.5000 | nan | nan | 0.0000 | evaluated |
| case_family | dense_via_background | 32 | 368 | 0.4688 | nan | 0.4688 | nan | nan | nan | evaluated |
| case_family | l1_jog | 33 | 367 | 0.0000 | nan | 0.0000 | nan | nan | nan | evaluated |
| case_family | multi_via | 33 | 367 | 1.0000 | nan | 1.0000 | nan | nan | nan | evaluated |
| case_family | no_via_background | 97 | 303 | 0.0000 | 0.0000 | nan | nan | nan | 1.0000 | evaluated |
| case_family | return_path | 100 | 300 | nan | nan | nan | nan | nan | nan | skipped_train_missing_eval_class |
| case_family | AGGREGATE_EVALUATED_FOLDS | 7 | 5 | 0.4537 | 0.5000 | 0.4922 | nan | nan | 0.5000 | std_acc=0.4075 |

This table tests whether the stacked calibrator survives stricter group-heldout splits. Variant-mod folds are evaluable for all classes; pure family leaveout is skipped when the training set would lose the held-out class entirely.
