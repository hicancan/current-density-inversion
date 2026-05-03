# Exp08 family-heldout feature-distance refusal audit

| group policy | heldout group | heldout n | train n | raw acc | raw H0 false-any | distance reject | accepted acc | accepted risk | accepted H0 false-any | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| variant_mod5 | canonical | 11 | 389 | 0.9091 | 0.0000 | 0.8182 | 1.0000 | 0.0000 | nan | evaluated_in_class_family |
| variant_mod5 | variant_mod_0 | 75 | 325 | 1.0000 | 0.0000 | 0.1867 | 1.0000 | 0.0000 | 0.0000 | evaluated_in_class_family |
| variant_mod5 | variant_mod_1 | 81 | 319 | 0.9877 | 0.0500 | 0.2840 | 0.9828 | 0.0172 | 0.0625 | evaluated_in_class_family |
| variant_mod5 | variant_mod_2 | 79 | 321 | 1.0000 | 0.0000 | 0.1139 | 1.0000 | 0.0000 | 0.0000 | evaluated_in_class_family |
| variant_mod5 | variant_mod_3 | 77 | 323 | 0.9870 | 0.0526 | 0.1818 | 1.0000 | 0.0000 | 0.0000 | evaluated_in_class_family |
| variant_mod5 | variant_mod_4 | 77 | 323 | 1.0000 | 0.0000 | 0.3636 | 1.0000 | 0.0000 | 0.0000 | evaluated_in_class_family |
| variant_mod5 | AGGREGATE_EVALUATED_FOLDS | 6 | 6 | 0.9806 | 0.0171 | 0.3247 | 0.9971 | 0.0029 | 0.0125 | distance_refusal_aggregate |
| case_family | bend_artifact | 100 | 300 | 0.0000 | nan | 1.0000 | nan | nan | nan | train_missing_eval_class_rejected |
| case_family | canonical | 5 | 395 | 0.8000 | 0.0000 | 1.0000 | nan | nan | nan | evaluated_in_class_family |
| case_family | dense_via_background | 32 | 368 | 0.4688 | nan | 1.0000 | nan | nan | nan | evaluated_in_class_family |
| case_family | l1_jog | 33 | 367 | 0.0000 | nan | 1.0000 | nan | nan | nan | evaluated_in_class_family |
| case_family | multi_via | 33 | 367 | 1.0000 | nan | 0.5152 | 1.0000 | 0.0000 | nan | evaluated_in_class_family |
| case_family | no_via_background | 97 | 303 | 0.0000 | 1.0000 | 1.0000 | nan | nan | nan | evaluated_in_class_family |
| case_family | return_path | 100 | 300 | 0.0000 | nan | 1.0000 | nan | nan | nan | train_missing_eval_class_rejected |
| case_family | AGGREGATE_EVALUATED_FOLDS | 7 | 7 | 0.3241 | 0.5000 | 0.9307 | 1.0000 | 0.0000 | nan | distance_refusal_aggregate |

This table asks whether the feature-distance safety layer makes unseen held-out families safer. High rejection means the system is refusing out-of-family evidence rather than pretending it can classify it; high accepted accuracy is required before calling it cross-family generalization.
