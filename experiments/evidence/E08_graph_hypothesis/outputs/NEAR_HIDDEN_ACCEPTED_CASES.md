# Exp08 accepted near-boundary hidden case audit

| case id | hidden family | primary truth | predicted | feature distance | distance threshold | confidence margin | mechanism status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hidden_near_corner_shadow_no_via_ood_15018_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2388 | 0.3508 | 1.0535 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15013_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2427 | 0.3508 | 1.0746 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15004_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2433 | 0.3508 | 1.0754 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15007_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2487 | 0.3508 | 1.0859 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15023_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2710 | 0.3508 | 1.0751 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15000_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2710 | 0.3508 | 0.9854 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15002_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2786 | 0.3508 | 1.0838 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15006_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2810 | 0.3508 | 1.0425 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15022_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2833 | 0.3508 | 0.9869 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15014_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2836 | 0.3508 | 1.0856 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15015_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.2903 | 0.3508 | 1.0927 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15019_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.3090 | 0.3508 | 0.9619 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15016_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.3098 | 0.3508 | 1.1374 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15017_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.3143 | 0.3508 | 0.9664 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15001_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.3189 | 0.3508 | 0.9632 | primary_label_correct_but_artifact_unexplained |
| hidden_near_corner_shadow_no_via_ood_15003_no_via | near_corner_shadow_no_via | H0_sheet_only | H0_sheet_only | 0.3384 | 0.3508 | 0.9546 | primary_label_correct_but_artifact_unexplained |

Accepted near-hidden rows are audited separately because primary-label correctness is weaker than mechanism-level explanation. A wrong-layer or shifted via can be primary-label correct while still indicating an incomplete graph/candidate model.
