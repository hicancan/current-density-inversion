# Exp08 stacked-evidence space diagnostics

| dataset | n | median feature distance | p90 feature distance | pc1 mean | pc1 std | pc2 mean | pc2 std | label counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_library_pypeec | 400 | 0.1925 | 0.4064 | 0.0000 | 13.1223 | 5.684e-16 | 9.4895 | H0_sheet_only:100, H1_sheet_via:100, H2_sheet_return:100, H3_sheet_artifact:100 |
| base_hidden | 96 | 1.4049 | 2.4390 | 9.2475 | 1.4390 | 2.3968 | 3.2112 | H0_sheet_only:24, H1_sheet_via:48, H2_sheet_return:0, H3_sheet_artifact:24 |
| near_boundary_hidden | 96 | 0.6678 | 1.0957 | 9.1238 | 1.9415 | 1.8101 | 5.1288 | H0_sheet_only:48, H1_sheet_via:48, H2_sheet_return:0, H3_sheet_artifact:0 |

The companion `stacked_evidence_space_pca.png` projects in-library PyPEEC, base hidden, and near-boundary hidden evidence vectors into the first two PCA axes of the in-library stacked-evidence space. The table reports feature-distance separation; the plot is explanatory only and is not used to tune thresholds.
