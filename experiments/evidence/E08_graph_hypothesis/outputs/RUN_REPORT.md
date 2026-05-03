# Exp08 Run Report — Graph-guided Magnetic System Identification

## Purpose

Exp08 is the first-stage successor to the pixel-map inverse pipeline. It tests whether a synthetic graph/CAD-like candidate space and explicit H0/H1/H2/H3 hypothesis scoring can reduce the false confidence of via detection under no-via, return-path, and bend/artifact ambiguity.

This experiment is self-contained and synthetic. It is not a real QDM/CAD/PyPEEC validation. Its role is to establish the code path, metrics, and scientific gates for the next graph-guided stage.

## Frozen protocol

- Random seed: `20260430`
- Grid: `25 × 25` over `0.002 m` FOV
- Classes: `no_via, true_via, return_path, bend_artifact`
- Hypotheses: `H0_sheet_only, H1_sheet_via, H2_sheet_return, H3_sheet_artifact`
- Selected complexity penalty from validation split: `0.0005`
- Via H1/H0 threshold selected only on validation split: `0.0006490222470557083`

## Main results

### Hypothesis identification

| split | 4-way accuracy | median best residual L2 | acc@20% coverage | acc@50% coverage |
| --- | --- | --- | --- | --- |
| val | 1.0000 | 0.0428 | 1.0000 | 1.0000 |
| test | 1.0000 | 0.0413 | 1.0000 | 1.0000 |
| ood | 0.8800 | 0.1176 | 1.0000 | 0.9400 |


### Per-class hypothesis accuracy

| split | true hypothesis | accuracy |
| --- | --- | --- |
| val | H0_sheet_only | 1.0000 |
| val | H1_sheet_via | 1.0000 |
| val | H2_sheet_return | 1.0000 |
| val | H3_sheet_artifact | 1.0000 |
| test | H0_sheet_only | 1.0000 |
| test | H1_sheet_via | 1.0000 |
| test | H2_sheet_return | 1.0000 |
| test | H3_sheet_artifact | 1.0000 |
| ood | H0_sheet_only | 0.7200 |
| ood | H1_sheet_via | 0.8000 |
| ood | H2_sheet_return | 1.0000 |
| ood | H3_sheet_artifact | 1.0000 |


### Selective risk / refusal

| split | coverage | selected | accuracy | risk |
| --- | --- | --- | --- | --- |
| val | 20% | 24 | 1.0000 | 0.0000 |
| val | 50% | 60 | 1.0000 | 0.0000 |
| val | 80% | 96 | 1.0000 | 0.0000 |
| val | 100% | 120 | 1.0000 | 0.0000 |
| test | 20% | 40 | 1.0000 | 0.0000 |
| test | 50% | 100 | 1.0000 | 0.0000 |
| test | 80% | 160 | 1.0000 | 0.0000 |
| test | 100% | 200 | 1.0000 | 0.0000 |
| ood | 20% | 20 | 1.0000 | 0.0000 |
| ood | 50% | 50 | 0.9400 | 0.0600 |
| ood | 80% | 80 | 0.9000 | 0.1000 |
| ood | 100% | 100 | 0.8800 | 0.1200 |


### Via hypothesis test

| method | split | AUC | precision | recall | F1 | no-via FP rate | threshold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| raw_template | val | 0.5656 | 0.3846 | 0.3333 | 0.3571 | 0.1778 | 0.0802 |
| raw_template | test | 0.4848 | 0.2683 | 0.2200 | 0.2418 | 0.2000 | 0.0802 |
| raw_template | ood | 0.5461 | 0.3182 | 0.2800 | 0.2979 | 0.2000 | 0.0802 |
| sheet_residual_template | val | 0.9893 | 0.9333 | 0.9333 | 0.9333 | 0.0222 | 0.0167 |
| sheet_residual_template | test | 0.9925 | 0.9057 | 0.9600 | 0.9320 | 0.0333 | 0.0167 |
| sheet_residual_template | ood | 0.9584 | 0.7692 | 0.8000 | 0.7843 | 0.0800 | 0.0167 |
| graph_h1_h0 | val | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 6.490e-04 |
| graph_h1_h0 | test | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 6.490e-04 |
| graph_h1_h0 | ood | 0.9691 | 1.0000 | 0.8000 | 0.8889 | 0.0000 | 6.490e-04 |


### Misclassified cases

| split | case | class | true H | pred H | margin | via evidence | true residual | pred residual | raw via score | sheet-residual score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ood | ood_00323_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0525 | -4.970e-04 | 0.2010 | 0.1479 | 0.0451 | 0.0012 |
| ood | ood_00337_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0304 | -4.903e-04 | 0.2533 | 0.2224 | 0.0809 | 0.0023 |
| ood | ood_00327_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0120 | -3.103e-04 | 0.2405 | 0.2279 | 0.0203 | 0.0096 |
| ood | ood_00328_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0048 | -4.999e-04 | 0.2184 | 0.2130 | 0.0162 | 2.934e-04 |
| ood | ood_00330_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0048 | -4.545e-04 | 0.2115 | 0.2061 | 0.0119 | 0.0045 |
| ood | ood_00369_true_via | true_via | H1_sheet_via | H2_sheet_return | 0.0026 | 0.0028 | 0.1946 | 0.1920 | 0.0471 | 0.0363 |
| ood | ood_00338_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0017 | -4.998e-04 | 0.1786 | 0.1763 | 0.0481 | 3.514e-04 |
| ood | ood_00358_true_via | true_via | H1_sheet_via | H2_sheet_return | 0.0010 | 0.0027 | 0.2199 | 0.2189 | 0.0277 | 0.0378 |
| ood | ood_00352_true_via | true_via | H1_sheet_via | H0_sheet_only | 4.009e-04 | -4.009e-04 | 0.2810 | 0.2811 | 0.1167 | 0.0076 |
| ood | ood_00346_true_via | true_via | H1_sheet_via | H0_sheet_only | 3.264e-04 | -3.264e-04 | 0.0838 | 0.0840 | 1.972e-04 | 0.0054 |
| ood | ood_00340_no_via | no_via | H0_sheet_only | H2_sheet_return | 1.549e-04 | -4.563e-04 | 0.1900 | 0.1893 | 0.0411 | 0.0042 |
| ood | ood_00347_true_via | true_via | H1_sheet_via | H0_sheet_only | 1.221e-04 | -1.221e-04 | 0.0905 | 0.0909 | 0.0263 | 0.0083 |


Total misclassified cases: `12`.


### P0: exp07 PyPEEC graph bridge

# Exp08 graph scorer on exp07 centerline and PyPEEC fields

| field | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | via AUC | via recall | via F1 | no-via FP | median margin | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.3333 | 0.5201 | 0.0011 |
| B_pypeec | 400 | 0.7175 | 0.0500 | 0.8200 | 1.0000 | 1.0000 | 0.9534 | 0.9900 | 0.6600 | 0.3367 | 0.1546 | 0.1715 |

Boundary: exp07 metadata is converted to an approximate graph; this is not real CAD import.


# Exp08 exp07-PyPEEC bridge failure cases

| case | case type | exp03-like | class | true H | pred H | margin | via evidence | true residual | pred residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finite_width_trace | canonical | False | no_via | H0_sheet_only | H2_sheet_return | 0.0213 | -5.000e-04 | 0.1806 | 0.1585 |
| two_layer_route_with_via__v16 | l1_jog | True | true_via | H1_sheet_via | H2_sheet_return | 0.0178 | 0.0085 | 0.1284 | 0.1106 |
| two_layer_route_with_via__v18 | l1_jog | True | true_via | H1_sheet_via | H3_sheet_artifact | 0.0029 | 0.0118 | 0.1111 | 0.1082 |
| two_layer_route_with_via__v19 | l1_jog | True | true_via | H1_sheet_via | H2_sheet_return | 0.0055 | 0.0085 | 0.1370 | 0.1315 |
| dense_via_background__v03 | dense_via_background | True | true_via | H1_sheet_via | H3_sheet_artifact | 4.414e-04 | 0.0038 | 0.1229 | 0.1240 |
| dense_via_background__v07 | dense_via_background | True | true_via | H1_sheet_via | H3_sheet_artifact | 0.0096 | 0.0014 | 0.1827 | 0.1746 |
| dense_via_background__v09 | dense_via_background | True | true_via | H1_sheet_via | H3_sheet_artifact | 0.0086 | 0.0011 | 0.1656 | 0.1584 |
| dense_via_background__v10 | dense_via_background | True | true_via | H1_sheet_via | H3_sheet_artifact | 0.0071 | 0.0019 | 0.1578 | 0.1522 |
| dense_via_background__v16 | dense_via_background | True | true_via | H1_sheet_via | H3_sheet_artifact | 0.0181 | 0.0019 | 0.1707 | 0.1541 |
| dense_via_background__v17 | dense_via_background | True | true_via | H1_sheet_via | H3_sheet_artifact | 0.0106 | 5.419e-04 | 0.1617 | 0.1526 |
| dense_via_background__v18 | dense_via_background | True | true_via | H1_sheet_via | H3_sheet_artifact | 4.986e-05 | 0.0036 | 0.1328 | 0.1327 |
| dense_via_background__v19 | dense_via_background | True | true_via | H1_sheet_via | H2_sheet_return | 0.0021 | 0.0055 | 0.1426 | 0.1420 |
| no_via_background | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0128 | -4.722e-04 | 0.2526 | 0.2284 |
| no_via_background__v01 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 4.341e-04 | -3.372e-04 | 0.1886 | 0.1877 |
| no_via_background__v02 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0016 | -4.879e-04 | 0.1357 | 0.1303 |
| no_via_background__v03 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0030 | -4.709e-04 | 0.1328 | 0.1257 |
| no_via_background__v04 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0246 | 6.625e-04 | 0.2257 | 0.1999 |
| no_via_background__v05 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 9.686e-04 | -3.483e-04 | 0.2093 | 0.1952 |
| no_via_background__v06 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0119 | -1.685e-04 | 0.2087 | 0.1963 |
| no_via_background__v07 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0087 | -4.140e-04 | 0.1612 | 0.1462 |
| no_via_background__v08 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0175 | -4.204e-04 | 0.1943 | 0.1751 |
| no_via_background__v09 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0149 | -4.989e-04 | 0.1758 | 0.1574 |
| no_via_background__v10 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0038 | -4.740e-04 | 0.1251 | 0.1201 |
| no_via_background__v11 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0139 | -4.856e-04 | 0.1664 | 0.1494 |
| no_via_background__v12 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0076 | -5.495e-05 | 0.2087 | 0.1994 |
| no_via_background__v13 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0087 | -3.817e-04 | 0.1876 | 0.1783 |
| no_via_background__v14 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0115 | -4.296e-04 | 0.2054 | 0.1918 |
| no_via_background__v15 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0012 | -4.077e-04 | 0.1127 | 0.1110 |
| no_via_background__v16 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0060 | -4.874e-04 | 0.1586 | 0.1514 |
| no_via_background__v17 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 4.716e-05 | -4.759e-04 | 0.1733 | 0.1727 |
| no_via_background__v18 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0237 | -1.848e-04 | 0.1892 | 0.1620 |
| no_via_background__v19 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0018 | -4.895e-04 | 0.1613 | 0.1554 |
| no_via_background__v20 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0209 | -1.160e-04 | 0.2342 | 0.2128 |
| no_via_background__v21 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 6.345e-04 | -4.356e-04 | 0.1960 | 0.1788 |
| no_via_background__v22 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0022 | -4.657e-04 | 0.1330 | 0.1296 |
| no_via_background__v23 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0088 | -4.707e-04 | 0.1643 | 0.1549 |
| no_via_background__v24 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0070 | -4.874e-04 | 0.1586 | 0.1478 |
| no_via_background__v25 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0150 | -4.850e-04 | 0.1889 | 0.1682 |
| no_via_background__v26 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0064 | -4.296e-04 | 0.2054 | 0.1980 |
| no_via_background__v27 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0035 | -4.502e-04 | 0.1626 | 0.1582 |
| no_via_background__v28 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0059 | -1.158e-04 | 0.1605 | 0.1541 |
| no_via_background__v29 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0101 | -1.232e-04 | 0.2232 | 0.2120 |
| no_via_background__v30 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0033 | -4.879e-04 | 0.1357 | 0.1319 |
| no_via_background__v31 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 6.502e-04 | -4.856e-04 | 0.1664 | 0.1633 |
| no_via_background__v32 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0087 | -7.803e-06 | 0.2544 | 0.2377 |
| no_via_background__v33 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0027 | -1.508e-04 | 0.2050 | 0.2002 |
| no_via_background__v34 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0038 | -4.400e-04 | 0.2403 | 0.2254 |
| no_via_background__v35 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0111 | -4.834e-04 | 0.1932 | 0.1746 |
| no_via_background__v36 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0096 | -4.874e-04 | 0.1586 | 0.1478 |
| no_via_background__v37 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0032 | -3.673e-04 | 0.1514 | 0.1431 |
| no_via_background__v38 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0077 | -4.677e-04 | 0.1788 | 0.1691 |
| no_via_background__v39 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0159 | -3.610e-04 | 0.1682 | 0.1497 |
| no_via_background__v40 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0022 | -1.960e-05 | 0.2097 | 0.2057 |
| no_via_background__v41 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0166 | -4.290e-04 | 0.1967 | 0.1795 |
| no_via_background__v42 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0026 | -4.872e-04 | 0.1334 | 0.1303 |
| no_via_background__v43 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0051 | -4.676e-04 | 0.1641 | 0.1585 |
| no_via_background__v44 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0066 | 8.383e-05 | 0.2020 | 0.1940 |
| no_via_background__v45 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0058 | -2.195e-04 | 0.1943 | 0.1874 |
| no_via_background__v46 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0216 | -4.497e-04 | 0.2557 | 0.2334 |
| no_via_background__v47 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0046 | -4.837e-04 | 0.1397 | 0.1346 |
| no_via_background__v49 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0010 | -4.155e-04 | 0.1948 | 0.1930 |
| no_via_background__v50 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0018 | -4.783e-04 | 0.1236 | 0.1204 |
| no_via_background__v51 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0025 | -3.284e-04 | 0.1056 | 0.1011 |
| no_via_background__v52 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0089 | -3.038e-04 | 0.2202 | 0.2067 |
| no_via_background__v53 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 4.658e-04 | -4.988e-04 | 0.1669 | 0.1659 |
| no_via_background__v54 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0022 | -4.497e-04 | 0.2557 | 0.2303 |
| no_via_background__v55 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0032 | -4.605e-04 | 0.2286 | 0.2019 |
| no_via_background__v56 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0052 | 8.383e-05 | 0.2020 | 0.1898 |
| no_via_background__v57 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 4.922e-04 | -4.693e-04 | 0.2090 | 0.2080 |
| no_via_background__v58 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 7.127e-04 | -4.677e-04 | 0.1788 | 0.1768 |
| no_via_background__v59 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0132 | -3.035e-04 | 0.1665 | 0.1486 |
| no_via_background__v60 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 9.834e-05 | -4.694e-04 | 0.2124 | 0.2109 |
| no_via_background__v61 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0138 | -4.290e-04 | 0.1967 | 0.1823 |
| no_via_background__v62 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 1.279e-04 | -4.566e-04 | 0.1326 | 0.1307 |
| no_via_background__v63 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0011 | -3.580e-04 | 0.1620 | 0.1585 |
| no_via_background__v64 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0028 | -4.939e-04 | 0.1521 | 0.1486 |
| no_via_background__v65 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 8.991e-04 | -4.990e-04 | 0.1798 | 0.1783 |
| no_via_background__v66 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0095 | -4.400e-04 | 0.2403 | 0.2293 |
| no_via_background__v67 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 5.873e-04 | -4.939e-04 | 0.1439 | 0.1428 |
| no_via_background__v68 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 3.615e-05 | -4.204e-04 | 0.1943 | 0.1751 |
| no_via_background__v69 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0145 | -3.867e-04 | 0.2281 | 0.2120 |
| no_via_background__v70 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0026 | -4.872e-04 | 0.1334 | 0.1303 |
| no_via_background__v71 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0228 | -4.601e-04 | 0.1887 | 0.1623 |
| no_via_background__v72 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0011 | 5.236e-05 | 0.2523 | 0.2506 |
| no_via_background__v74 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0316 | -4.400e-04 | 0.2403 | 0.1973 |
| no_via_background__v75 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0047 | -4.973e-04 | 0.0781 | 0.0729 |
| no_via_background__v76 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0065 | -1.989e-04 | 0.2592 | 0.2472 |
| no_via_background__v78 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0034 | -3.184e-04 | 0.1591 | 0.1546 |
| no_via_background__v79 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0030 | -4.895e-04 | 0.1613 | 0.1554 |
| no_via_background__v80 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0069 | -2.630e-04 | 0.2178 | 0.2043 |
| no_via_background__v81 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 4.341e-04 | -3.372e-04 | 0.1886 | 0.1877 |
| no_via_background__v82 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0016 | -4.879e-04 | 0.1357 | 0.1303 |
| no_via_background__v83 | no_via_background | True | no_via | H0_sheet_only | H2_sheet_return | 0.0030 | -4.709e-04 | 0.1328 | 0.1257 |
| no_via_background__v84 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 4.713e-04 | -4.999e-04 | 0.1425 | 0.1407 |
| no_via_background__v85 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 1.421e-04 | -2.195e-04 | 0.1943 | 0.1912 |
| no_via_background__v86 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0414 | -4.400e-04 | 0.2403 | 0.1973 |
| no_via_background__v87 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0169 | -2.654e-04 | 0.1475 | 0.1298 |
| no_via_background__v88 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0135 | -4.945e-04 | 0.2570 | 0.2421 |
| no_via_background__v89 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0165 | -4.989e-04 | 0.1758 | 0.1574 |
| no_via_background__v90 | no_via_background | True | no_via | H0_sheet_only | H3_sheet_artifact | 0.0017 | -4.657e-04 | 0.1330 | 0.1296 |

Total PyPEEC bridge misclassified cases: `113`.


### P0: PyPEEC-aware basis bank

# Exp08 P0 PyPEEC-aware graph basis-bank diagnostic

| field | basis mode | 4-way acc | H0 acc | H1 acc | H2 acc | via AUC | no-via FP | median residual | residual delta vs base |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | finite_width_sheet | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 0.0011 | -1.353e-05 |
| B_centerline | return_bank | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 0.0011 | 0.0000 |
| B_centerline | artifact_bank | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 0.0011 | 0.0000 |
| B_centerline | distributed_via | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4133 | 0.0010 | -3.351e-05 |
| B_centerline | combined_pypeec_aware | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4133 | 0.0010 | -4.942e-05 |
| B_pypeec | finite_width_sheet | 0.7700 | 0.0800 | 1.0000 | 1.0000 | 0.9998 | 0.3400 | 0.1042 | -0.0672 |
| B_pypeec | return_bank | 0.6800 | 0.0300 | 0.6900 | 1.0000 | 0.9534 | 0.3367 | 0.1573 | -0.0142 |
| B_pypeec | artifact_bank | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 0.9534 | 0.3367 | 0.1603 | -0.0111 |
| B_pypeec | distributed_via | 0.6850 | 0.0500 | 0.6900 | 1.0000 | 0.7441 | 0.4300 | 0.1724 | 9.800e-04 |
| B_pypeec | combined_pypeec_aware | 0.6100 | 0.0300 | 0.4100 | 1.0000 | 0.9798 | 0.4633 | 0.0945 | -0.0770 |

Basis-bank modes are fixed diagnostics: finite-width sheet, return bank, artifact bank, distributed via, and a combined mode. They do not use PyPEEC labels for selection.


# Exp08 P0 model-evidence selection diagnostic

| field | basis mode | evidence mode | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | false H1 rate | false H2 rate | false H3 rate | median residual | median params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | base | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0100 | 0.7200 | 0.2700 | 0.0011 | 4.0000 |
| B_centerline | base | default_score | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | base | parameter_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | base | extra_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | base | bic_like | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | base | h0_conservative | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | finite_width_sheet | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0400 | 0.6900 | 0.2700 | 0.0011 | 5.0000 |
| B_centerline | finite_width_sheet | default_score | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | finite_width_sheet | parameter_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | finite_width_sheet | extra_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | finite_width_sheet | bic_like | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | finite_width_sheet | h0_conservative | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | return_bank | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0100 | 0.9700 | 0.0200 | 0.0011 | 6.0000 |
| B_centerline | return_bank | default_score | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | return_bank | parameter_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | return_bank | extra_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | return_bank | bic_like | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | return_bank | h0_conservative | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 5.0000 |
| B_centerline | artifact_bank | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0100 | 0.1700 | 0.8200 | 0.0010 | 5.0000 |
| B_centerline | artifact_bank | default_score | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | artifact_bank | parameter_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | artifact_bank | extra_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | artifact_bank | bic_like | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | artifact_bank | h0_conservative | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0011 | 3.0000 |
| B_centerline | distributed_via | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4400 | 0.5100 | 0.0500 | 0.0010 | 5.0000 |
| B_centerline | distributed_via | default_score | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0010 | 4.0000 |
| B_centerline | distributed_via | parameter_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0010 | 4.0000 |
| B_centerline | distributed_via | extra_count | 400 | 0.9200 | 1.0000 | 0.6800 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 4.0000 |
| B_centerline | distributed_via | bic_like | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0010 | 4.0000 |
| B_centerline | distributed_via | h0_conservative | 400 | 0.9200 | 1.0000 | 0.6800 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 4.0000 |
| B_centerline | combined_pypeec_aware | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0100 | 0.3900 | 0.6000 | 9.600e-04 | 9.0000 |
| B_centerline | combined_pypeec_aware | default_score | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0010 | 9.0000 |
| B_centerline | combined_pypeec_aware | parameter_count | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0010 | 9.0000 |
| B_centerline | combined_pypeec_aware | extra_count | 400 | 0.9200 | 1.0000 | 0.6800 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 9.0000 |
| B_centerline | combined_pypeec_aware | bic_like | 400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0010 | 9.0000 |
| B_centerline | combined_pypeec_aware | h0_conservative | 400 | 0.9200 | 1.0000 | 0.6800 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0014 | 9.0000 |
| B_pypeec | base | residual_only | 400 | 0.7075 | 0.0000 | 0.8300 | 1.0000 | 1.0000 | 0.0100 | 0.3400 | 0.6500 | 0.1715 | 4.0000 |
| B_pypeec | base | default_score | 400 | 0.7175 | 0.0500 | 0.8200 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1715 | 4.0000 |
| B_pypeec | base | parameter_count | 400 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1715 | 4.0000 |
| B_pypeec | base | extra_count | 400 | 0.7225 | 0.3000 | 0.5900 | 1.0000 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 |
| B_pypeec | base | bic_like | 400 | 0.7175 | 0.0600 | 0.8100 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1715 | 4.0000 |
| B_pypeec | base | h0_conservative | 400 | 0.7650 | 0.5800 | 0.4800 | 1.0000 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 |
| B_pypeec | finite_width_sheet | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0500 | 0.2700 | 0.6800 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | default_score | 400 | 0.7700 | 0.0800 | 1.0000 | 1.0000 | 1.0000 | 0.0300 | 0.2400 | 0.6500 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | parameter_count | 400 | 0.7625 | 0.0500 | 1.0000 | 1.0000 | 1.0000 | 0.0500 | 0.2500 | 0.6500 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | extra_count | 400 | 0.8900 | 0.7800 | 0.7800 | 1.0000 | 1.0000 | 0.0000 | 0.0600 | 0.1600 | 0.1075 | 5.0000 |
| B_pypeec | finite_width_sheet | bic_like | 400 | 0.7875 | 0.1500 | 1.0000 | 1.0000 | 1.0000 | 0.0200 | 0.2400 | 0.5900 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | h0_conservative | 400 | 0.9150 | 0.9700 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0300 | 0.1086 | 5.0000 |
| B_pypeec | return_bank | residual_only | 400 | 0.6775 | 0.0000 | 0.7100 | 1.0000 | 1.0000 | 0.0000 | 0.7300 | 0.2700 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | default_score | 400 | 0.6800 | 0.0300 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.6200 | 0.3500 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | parameter_count | 400 | 0.6800 | 0.0200 | 0.7000 | 1.0000 | 1.0000 | 0.0000 | 0.6600 | 0.3200 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | extra_count | 400 | 0.7200 | 0.2900 | 0.5900 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.3800 | 0.1585 | 6.0000 |
| B_pypeec | return_bank | bic_like | 400 | 0.6825 | 0.0400 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.5900 | 0.3700 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | h0_conservative | 400 | 0.7425 | 0.5000 | 0.4700 | 1.0000 | 1.0000 | 0.0000 | 0.2800 | 0.2200 | 0.1608 | 5.0000 |
| B_pypeec | artifact_bank | residual_only | 400 | 0.5425 | 0.0000 | 0.1700 | 1.0000 | 1.0000 | 0.0000 | 0.0500 | 0.9500 | 0.1600 | 5.0000 |
| B_pypeec | artifact_bank | default_score | 400 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 |
| B_pypeec | artifact_bank | parameter_count | 400 | 0.5550 | 0.0200 | 0.2000 | 1.0000 | 1.0000 | 0.0000 | 0.0900 | 0.8900 | 0.1600 | 5.0000 |
| B_pypeec | artifact_bank | extra_count | 400 | 0.7650 | 0.4800 | 0.5800 | 1.0000 | 1.0000 | 0.0000 | 0.3200 | 0.2000 | 0.1680 | 4.0000 |
| B_pypeec | artifact_bank | bic_like | 400 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 |
| B_pypeec | artifact_bank | h0_conservative | 400 | 0.7825 | 0.6600 | 0.4700 | 1.0000 | 1.0000 | 0.0000 | 0.1600 | 0.1800 | 0.1712 | 4.0000 |
| B_pypeec | distributed_via | residual_only | 400 | 0.7150 | 0.0000 | 0.8600 | 1.0000 | 1.0000 | 0.0500 | 0.3400 | 0.6100 | 0.1711 | 4.5000 |
| B_pypeec | distributed_via | default_score | 400 | 0.6850 | 0.0500 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1724 | 4.0000 |
| B_pypeec | distributed_via | parameter_count | 400 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1711 | 4.0000 |
| B_pypeec | distributed_via | extra_count | 400 | 0.5950 | 0.3000 | 0.0800 | 1.0000 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 |
| B_pypeec | distributed_via | bic_like | 400 | 0.6750 | 0.0600 | 0.6400 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1724 | 4.0000 |
| B_pypeec | distributed_via | h0_conservative | 400 | 0.6575 | 0.5800 | 0.0500 | 1.0000 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 |
| B_pypeec | combined_pypeec_aware | residual_only | 400 | 0.6125 | 0.0000 | 0.4500 | 1.0000 | 1.0000 | 0.0000 | 0.0400 | 0.9600 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | default_score | 400 | 0.6100 | 0.0300 | 0.4100 | 1.0000 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | parameter_count | 400 | 0.6100 | 0.0200 | 0.4200 | 1.0000 | 1.0000 | 0.0000 | 0.0200 | 0.9600 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | extra_count | 400 | 0.7250 | 0.6600 | 0.2400 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.3400 | 0.1082 | 9.0000 |
| B_pypeec | combined_pypeec_aware | bic_like | 400 | 0.6150 | 0.0300 | 0.4300 | 1.0000 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | h0_conservative | 400 | 0.7325 | 0.7600 | 0.1700 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.2400 | 0.1099 | 9.0000 |

Evidence modes reuse the same fitted basis matrices and change only model-selection scoring. They are diagnostics, not PyPEEC-calibrated thresholds.


# Exp08 P2 disciplined PyPEEC model-bank evidence table

| field | basis mode | evidence mode | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | false H1 rate | false H2 rate | false H3 rate | median residual | median params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_pypeec | base | residual_only | 400 | 0.7075 | 0.0000 | 0.8300 | 1.0000 | 1.0000 | 0.0100 | 0.3400 | 0.6500 | 0.1715 | 4.0000 |
| B_pypeec | base | default_score | 400 | 0.7175 | 0.0500 | 0.8200 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1715 | 4.0000 |
| B_pypeec | base | parameter_count | 400 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1715 | 4.0000 |
| B_pypeec | base | extra_count | 400 | 0.7225 | 0.3000 | 0.5900 | 1.0000 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 |
| B_pypeec | base | bic_like | 400 | 0.7175 | 0.0600 | 0.8100 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1715 | 4.0000 |
| B_pypeec | base | h0_conservative | 400 | 0.7650 | 0.5800 | 0.4800 | 1.0000 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 |
| B_pypeec | finite_width_sheet | residual_only | 400 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0500 | 0.2700 | 0.6800 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | default_score | 400 | 0.7700 | 0.0800 | 1.0000 | 1.0000 | 1.0000 | 0.0300 | 0.2400 | 0.6500 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | parameter_count | 400 | 0.7625 | 0.0500 | 1.0000 | 1.0000 | 1.0000 | 0.0500 | 0.2500 | 0.6500 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | extra_count | 400 | 0.8900 | 0.7800 | 0.7800 | 1.0000 | 1.0000 | 0.0000 | 0.0600 | 0.1600 | 0.1075 | 5.0000 |
| B_pypeec | finite_width_sheet | bic_like | 400 | 0.7875 | 0.1500 | 1.0000 | 1.0000 | 1.0000 | 0.0200 | 0.2400 | 0.5900 | 0.1042 | 5.0000 |
| B_pypeec | finite_width_sheet | h0_conservative | 400 | 0.9150 | 0.9700 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0300 | 0.1086 | 5.0000 |
| B_pypeec | return_bank | residual_only | 400 | 0.6775 | 0.0000 | 0.7100 | 1.0000 | 1.0000 | 0.0000 | 0.7300 | 0.2700 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | default_score | 400 | 0.6800 | 0.0300 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.6200 | 0.3500 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | parameter_count | 400 | 0.6800 | 0.0200 | 0.7000 | 1.0000 | 1.0000 | 0.0000 | 0.6600 | 0.3200 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | extra_count | 400 | 0.7200 | 0.2900 | 0.5900 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.3800 | 0.1585 | 6.0000 |
| B_pypeec | return_bank | bic_like | 400 | 0.6825 | 0.0400 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.5900 | 0.3700 | 0.1573 | 6.0000 |
| B_pypeec | return_bank | h0_conservative | 400 | 0.7425 | 0.5000 | 0.4700 | 1.0000 | 1.0000 | 0.0000 | 0.2800 | 0.2200 | 0.1608 | 5.0000 |
| B_pypeec | artifact_bank | residual_only | 400 | 0.5425 | 0.0000 | 0.1700 | 1.0000 | 1.0000 | 0.0000 | 0.0500 | 0.9500 | 0.1600 | 5.0000 |
| B_pypeec | artifact_bank | default_score | 400 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 |
| B_pypeec | artifact_bank | parameter_count | 400 | 0.5550 | 0.0200 | 0.2000 | 1.0000 | 1.0000 | 0.0000 | 0.0900 | 0.8900 | 0.1600 | 5.0000 |
| B_pypeec | artifact_bank | extra_count | 400 | 0.7650 | 0.4800 | 0.5800 | 1.0000 | 1.0000 | 0.0000 | 0.3200 | 0.2000 | 0.1680 | 4.0000 |
| B_pypeec | artifact_bank | bic_like | 400 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 |
| B_pypeec | artifact_bank | h0_conservative | 400 | 0.7825 | 0.6600 | 0.4700 | 1.0000 | 1.0000 | 0.0000 | 0.1600 | 0.1800 | 0.1712 | 4.0000 |
| B_pypeec | distributed_via | residual_only | 400 | 0.7150 | 0.0000 | 0.8600 | 1.0000 | 1.0000 | 0.0500 | 0.3400 | 0.6100 | 0.1711 | 4.5000 |
| B_pypeec | distributed_via | default_score | 400 | 0.6850 | 0.0500 | 0.6900 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1724 | 4.0000 |
| B_pypeec | distributed_via | parameter_count | 400 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1711 | 4.0000 |
| B_pypeec | distributed_via | extra_count | 400 | 0.5950 | 0.3000 | 0.0800 | 1.0000 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 |
| B_pypeec | distributed_via | bic_like | 400 | 0.6750 | 0.0600 | 0.6400 | 1.0000 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1724 | 4.0000 |
| B_pypeec | distributed_via | h0_conservative | 400 | 0.6575 | 0.5800 | 0.0500 | 1.0000 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 |
| B_pypeec | combined_pypeec_aware | residual_only | 400 | 0.6125 | 0.0000 | 0.4500 | 1.0000 | 1.0000 | 0.0000 | 0.0400 | 0.9600 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | default_score | 400 | 0.6100 | 0.0300 | 0.4100 | 1.0000 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | parameter_count | 400 | 0.6100 | 0.0200 | 0.4200 | 1.0000 | 1.0000 | 0.0000 | 0.0200 | 0.9600 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | extra_count | 400 | 0.7250 | 0.6600 | 0.2400 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.3400 | 0.1082 | 9.0000 |
| B_pypeec | combined_pypeec_aware | bic_like | 400 | 0.6150 | 0.0300 | 0.4300 | 1.0000 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 |
| B_pypeec | combined_pypeec_aware | h0_conservative | 400 | 0.7325 | 0.7600 | 0.1700 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.2400 | 0.1099 | 9.0000 |

This table audits which fixed basis/evidence combinations improve classification and which merely reduce residual by over-expanding the model space.


# Exp08 P0 formal model-selection calibration audit

| basis mode | evidence mode | objective | 4-way acc | H0 acc | H1 acc | H2 acc | false H1 | false H2 | false H3 | median residual | median params | meets H1 floor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finite_width_sheet | h0_conservative | 0.7920 | 0.9150 | 0.9700 | 0.6900 | 1.0000 | 0.0000 | 0.0000 | 0.0300 | 0.1086 | 5.0000 | True |
| finite_width_sheet | extra_count | 0.7240 | 0.8900 | 0.7800 | 0.7800 | 1.0000 | 0.0000 | 0.0600 | 0.1600 | 0.1075 | 5.0000 | True |
| artifact_bank | h0_conservative | 0.5910 | 0.7825 | 0.6600 | 0.4700 | 1.0000 | 0.0000 | 0.1600 | 0.1800 | 0.1712 | 4.0000 | False |
| base | h0_conservative | 0.5540 | 0.7650 | 0.5800 | 0.4800 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 | False |
| artifact_bank | extra_count | 0.5340 | 0.7650 | 0.4800 | 0.5800 | 1.0000 | 0.0000 | 0.3200 | 0.2000 | 0.1680 | 4.0000 | False |
| return_bank | h0_conservative | 0.4910 | 0.7425 | 0.5000 | 0.4700 | 1.0000 | 0.0000 | 0.2800 | 0.2200 | 0.1608 | 5.0000 | False |
| finite_width_sheet | bic_like | 0.4750 | 0.7875 | 0.1500 | 1.0000 | 1.0000 | 0.0200 | 0.2400 | 0.5900 | 0.1042 | 5.0000 | True |
| combined_pypeec_aware | h0_conservative | 0.4510 | 0.7325 | 0.7600 | 0.1700 | 1.0000 | 0.0000 | 0.0000 | 0.2400 | 0.1099 | 9.0000 | False |
| base | extra_count | 0.4470 | 0.7225 | 0.3000 | 0.5900 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 | False |
| finite_width_sheet | default_score | 0.4400 | 0.7700 | 0.0800 | 1.0000 | 1.0000 | 0.0300 | 0.2400 | 0.6500 | 0.1042 | 5.0000 | True |
| finite_width_sheet | parameter_count | 0.4250 | 0.7625 | 0.0500 | 1.0000 | 1.0000 | 0.0500 | 0.2500 | 0.6500 | 0.1042 | 5.0000 | True |
| distributed_via | h0_conservative | 0.4250 | 0.6575 | 0.5800 | 0.0500 | 1.0000 | 0.0000 | 0.1400 | 0.2800 | 0.1730 | 4.0000 | False |
| combined_pypeec_aware | extra_count | 0.4220 | 0.7250 | 0.6600 | 0.2400 | 1.0000 | 0.0000 | 0.0000 | 0.3400 | 0.1082 | 9.0000 | False |
| return_bank | extra_count | 0.4020 | 0.7200 | 0.2900 | 0.5900 | 1.0000 | 0.0000 | 0.3300 | 0.3800 | 0.1585 | 6.0000 | False |
| finite_width_sheet | residual_only | 0.4000 | 0.7500 | 0.0000 | 1.0000 | 1.0000 | 0.0500 | 0.2700 | 0.6800 | 0.1042 | 5.0000 | True |
| base | bic_like | 0.3930 | 0.7175 | 0.0600 | 0.8100 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1715 | 4.0000 | True |
| base | default_score | 0.3910 | 0.7175 | 0.0500 | 0.8200 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1715 | 4.0000 | True |
| base | parameter_count | 0.3840 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1715 | 4.0000 | True |
| distributed_via | parameter_count | 0.3840 | 0.7150 | 0.0300 | 0.8300 | 1.0000 | 0.0000 | 0.3300 | 0.6400 | 0.1711 | 4.0000 | True |
| base | residual_only | 0.3690 | 0.7075 | 0.0000 | 0.8300 | 1.0000 | 0.0100 | 0.3400 | 0.6500 | 0.1715 | 4.0000 | True |
| distributed_via | residual_only | 0.3680 | 0.7150 | 0.0000 | 0.8600 | 1.0000 | 0.0500 | 0.3400 | 0.6100 | 0.1711 | 4.5000 | True |
| distributed_via | default_score | 0.3520 | 0.6850 | 0.0500 | 0.6900 | 1.0000 | 0.0000 | 0.3300 | 0.6200 | 0.1724 | 4.0000 | True |
| distributed_via | bic_like | 0.3420 | 0.6750 | 0.0600 | 0.6400 | 1.0000 | 0.0000 | 0.3300 | 0.6100 | 0.1724 | 4.0000 | False |
| return_bank | bic_like | 0.3070 | 0.6825 | 0.0400 | 0.6900 | 1.0000 | 0.0000 | 0.5900 | 0.3700 | 0.1573 | 6.0000 | True |
| return_bank | default_score | 0.3020 | 0.6800 | 0.0300 | 0.6900 | 1.0000 | 0.0000 | 0.6200 | 0.3500 | 0.1573 | 6.0000 | True |
| return_bank | parameter_count | 0.3000 | 0.6800 | 0.0200 | 0.7000 | 1.0000 | 0.0000 | 0.6600 | 0.3200 | 0.1573 | 6.0000 | True |
| distributed_via | extra_count | 0.2940 | 0.5950 | 0.3000 | 0.0800 | 1.0000 | 0.0000 | 0.2600 | 0.4400 | 0.1725 | 4.0000 | False |
| return_bank | residual_only | 0.2930 | 0.6775 | 0.0000 | 0.7100 | 1.0000 | 0.0000 | 0.7300 | 0.2700 | 0.1573 | 6.0000 | True |
| artifact_bank | default_score | 0.1880 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 | False |
| artifact_bank | bic_like | 0.1880 | 0.5700 | 0.0200 | 0.2600 | 1.0000 | 0.0000 | 0.1300 | 0.8500 | 0.1603 | 5.0000 | False |
| artifact_bank | parameter_count | 0.1700 | 0.5550 | 0.0200 | 0.2000 | 1.0000 | 0.0000 | 0.0900 | 0.8900 | 0.1600 | 5.0000 | False |
| combined_pypeec_aware | bic_like | 0.1640 | 0.6150 | 0.0300 | 0.4300 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 | False |
| combined_pypeec_aware | default_score | 0.1580 | 0.6100 | 0.0300 | 0.4100 | 1.0000 | 0.0000 | 0.0300 | 0.9400 | 0.0945 | 9.0000 | False |
| combined_pypeec_aware | parameter_count | 0.1560 | 0.6100 | 0.0200 | 0.4200 | 1.0000 | 0.0000 | 0.0200 | 0.9600 | 0.0945 | 9.0000 | False |
| combined_pypeec_aware | residual_only | 0.1550 | 0.6125 | 0.0000 | 0.4500 | 1.0000 | 0.0000 | 0.0400 | 0.9600 | 0.0945 | 9.0000 | False |
| artifact_bank | residual_only | 0.1510 | 0.5425 | 0.0000 | 0.1700 | 1.0000 | 0.0000 | 0.0500 | 0.9500 | 0.1600 | 5.0000 | False |

The objective is a fixed audit formula over PyPEEC frozen rows. It ranks trade-offs for analysis but is not used to tune the current PyPEEC predictions or thresholds.


# Exp08 P3 disciplined model-bank allowed-basis table

| hypothesis | allowed evidence/basis | restricted basis | reason |
| --- | --- | --- | --- |
| H0_sheet_only | sheet + finite_width_sheet | return_bank / artifact_bank / distributed_via | Protect no-via against residual-only over-explanation. |
| H1_sheet_via | sheet + finite_width_sheet + compact/distributed via | artifact_bank unless explicitly diagnosed | Keep true-via evidence separate from bend/corner artifacts. |
| H2_sheet_return | sheet + finite_width_sheet + return_bank | distributed_via as a first explanation | Return-current mismatch is a physical nuisance, not a via by default. |
| H3_sheet_artifact | sheet + finite_width_sheet + artifact_bank | return_bank unless route metadata supports it | Bend/corner residuals should compete with via, not silently become via. |
| unknown/refusal | all evidence families as diagnostic scores | label-changing calibration on PyPEEC frozen rows | Reject or defer when model evidence is not identifiable. |

This table states the model-bank discipline explicitly: richer bases must compete as hypotheses and should not be silently admitted to every class.


# Exp08 P0 held-out PyPEEC model-selection split

| true hypothesis | n cases | calibration | heldout |
| --- | --- | --- | --- |
| H0_sheet_only | 100 | 50 | 50 |
| H1_sheet_via | 100 | 50 | 50 |
| H2_sheet_return | 100 | 50 | 50 |
| H3_sheet_artifact | 100 | 50 | 50 |

This deterministic split is used only for the pilot held-out model-selection audit. The frozen bridge tables above remain no-calibration results.


# Exp08 P0 held-out PyPEEC model-selection pilot

| basis mode | evidence mode | cal objective | heldout objective | cal n | heldout n | cal 4-way acc | heldout 4-way acc | cal H0 acc | heldout H0 acc | cal H1 acc | heldout H1 acc | heldout H2 acc | heldout H0 false H1 | heldout H0 false H2 | heldout H0 false H3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finite_width_sheet | h0_conservative | 0.7140 | 0.8700 | 200 | 200 | 0.8450 | 0.9850 | 1.0000 | 0.9400 | 0.3800 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0600 |
| finite_width_sheet | extra_count | 0.6680 | 0.7800 | 200 | 200 | 0.8400 | 0.9400 | 0.8000 | 0.7600 | 0.5600 | 1.0000 | 1.0000 | 0.0000 | 0.0400 | 0.2000 |
| artifact_bank | h0_conservative | 0.4860 | 0.6760 | 200 | 200 | 0.7250 | 0.8400 | 0.5800 | 0.7400 | 0.3200 | 0.6200 | 1.0000 | 0.0000 | 0.1400 | 0.1200 |
| base | h0_conservative | 0.4760 | 0.6220 | 200 | 200 | 0.7150 | 0.8150 | 0.5400 | 0.6200 | 0.3200 | 0.6400 | 1.0000 | 0.0000 | 0.1000 | 0.2800 |
| finite_width_sheet | bic_like | 0.4500 | 0.5000 | 200 | 200 | 0.7750 | 0.8000 | 0.1000 | 0.2000 | 1.0000 | 1.0000 | 1.0000 | 0.0200 | 0.1600 | 0.6200 |
| return_bank | h0_conservative | 0.4260 | 0.5360 | 200 | 200 | 0.7050 | 0.7800 | 0.5000 | 0.5000 | 0.3200 | 0.6200 | 1.0000 | 0.0000 | 0.2800 | 0.2200 |
| finite_width_sheet | default_score | 0.4200 | 0.4600 | 200 | 200 | 0.7600 | 0.7800 | 0.0400 | 0.1200 | 1.0000 | 1.0000 | 1.0000 | 0.0400 | 0.1600 | 0.6800 |
| finite_width_sheet | parameter_count | 0.4200 | 0.4300 | 200 | 200 | 0.7600 | 0.7650 | 0.0400 | 0.0600 | 1.0000 | 1.0000 | 1.0000 | 0.0800 | 0.1800 | 0.6800 |
| artifact_bank | extra_count | 0.4020 | 0.6460 | 200 | 200 | 0.6850 | 0.8450 | 0.4000 | 0.5600 | 0.3400 | 0.8200 | 1.0000 | 0.0000 | 0.2800 | 0.1600 |
| finite_width_sheet | residual_only | 0.4000 | 0.4000 | 200 | 200 | 0.7500 | 0.7500 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0800 | 0.1800 | 0.7400 |
| combined_pypeec_aware | h0_conservative | 0.3920 | 0.5100 | 200 | 200 | 0.6900 | 0.7750 | 0.7200 | 0.8000 | 0.0400 | 0.3000 | 1.0000 | 0.0000 | 0.0000 | 0.2000 |
| distributed_via | h0_conservative | 0.3860 | 0.4740 | 200 | 200 | 0.6400 | 0.6750 | 0.5400 | 0.6200 | 0.0200 | 0.0800 | 1.0000 | 0.0000 | 0.1000 | 0.2800 |
| base | parameter_count | 0.3480 | 0.4100 | 200 | 200 | 0.6950 | 0.7350 | 0.0200 | 0.0400 | 0.7600 | 0.9000 | 1.0000 | 0.0000 | 0.3400 | 0.6200 |
| distributed_via | parameter_count | 0.3480 | 0.4100 | 200 | 200 | 0.6950 | 0.7350 | 0.0200 | 0.0400 | 0.7600 | 0.9000 | 1.0000 | 0.0000 | 0.3400 | 0.6200 |
| base | bic_like | 0.3460 | 0.4300 | 200 | 200 | 0.6900 | 0.7450 | 0.0400 | 0.0800 | 0.7200 | 0.9000 | 1.0000 | 0.0000 | 0.3400 | 0.5800 |
| distributed_via | residual_only | 0.3460 | 0.3900 | 200 | 200 | 0.7050 | 0.7250 | 0.0000 | 0.0000 | 0.8200 | 0.9000 | 1.0000 | 0.0800 | 0.3400 | 0.5800 |
| base | default_score | 0.3420 | 0.4300 | 200 | 200 | 0.6900 | 0.7450 | 0.0200 | 0.0800 | 0.7400 | 0.9000 | 1.0000 | 0.0000 | 0.3400 | 0.5800 |
| combined_pypeec_aware | extra_count | 0.3420 | 0.5020 | 200 | 200 | 0.6650 | 0.7850 | 0.6200 | 0.7000 | 0.0400 | 0.4400 | 1.0000 | 0.0000 | 0.0000 | 0.3000 |
| base | residual_only | 0.3380 | 0.3900 | 200 | 200 | 0.6900 | 0.7250 | 0.0000 | 0.0000 | 0.7600 | 0.9000 | 1.0000 | 0.0200 | 0.3400 | 0.6400 |
| base | extra_count | 0.3020 | 0.5820 | 200 | 200 | 0.6300 | 0.8150 | 0.1800 | 0.4200 | 0.3400 | 0.8400 | 1.0000 | 0.0000 | 0.2200 | 0.3600 |
| return_bank | extra_count | 0.2880 | 0.5360 | 200 | 200 | 0.6400 | 0.8000 | 0.2000 | 0.3800 | 0.3600 | 0.8200 | 1.0000 | 0.0000 | 0.3200 | 0.3000 |
| distributed_via | default_score | 0.2760 | 0.4180 | 200 | 200 | 0.6350 | 0.7350 | 0.0200 | 0.0800 | 0.5200 | 0.8600 | 1.0000 | 0.0000 | 0.3400 | 0.5800 |
| distributed_via | bic_like | 0.2740 | 0.4000 | 200 | 200 | 0.6300 | 0.7200 | 0.0400 | 0.0800 | 0.4800 | 0.8000 | 1.0000 | 0.0000 | 0.3400 | 0.5800 |
| return_bank | parameter_count | 0.2660 | 0.3240 | 200 | 200 | 0.6600 | 0.7000 | 0.0200 | 0.0200 | 0.6200 | 0.7800 | 1.0000 | 0.0000 | 0.7000 | 0.2800 |
| return_bank | residual_only | 0.2620 | 0.3140 | 200 | 200 | 0.6600 | 0.6950 | 0.0000 | 0.0000 | 0.6400 | 0.7800 | 1.0000 | 0.0000 | 0.7600 | 0.2400 |
| return_bank | bic_like | 0.2600 | 0.3440 | 200 | 200 | 0.6550 | 0.7100 | 0.0200 | 0.0600 | 0.6000 | 0.7800 | 1.0000 | 0.0000 | 0.6200 | 0.3200 |
| return_bank | default_score | 0.2600 | 0.3340 | 200 | 200 | 0.6550 | 0.7050 | 0.0200 | 0.0400 | 0.6000 | 0.7800 | 1.0000 | 0.0000 | 0.6600 | 0.3000 |
| distributed_via | extra_count | 0.2060 | 0.3720 | 200 | 200 | 0.5500 | 0.6400 | 0.1800 | 0.4200 | 0.0200 | 0.1400 | 1.0000 | 0.0000 | 0.2200 | 0.3600 |
| artifact_bank | bic_like | 0.1760 | 0.2000 | 200 | 200 | 0.5600 | 0.5800 | 0.0200 | 0.0200 | 0.2200 | 0.3000 | 1.0000 | 0.0000 | 0.0600 | 0.9200 |
| artifact_bank | default_score | 0.1760 | 0.2000 | 200 | 200 | 0.5600 | 0.5800 | 0.0200 | 0.0200 | 0.2200 | 0.3000 | 1.0000 | 0.0000 | 0.0600 | 0.9200 |
| artifact_bank | parameter_count | 0.1640 | 0.1760 | 200 | 200 | 0.5500 | 0.5600 | 0.0200 | 0.0200 | 0.1800 | 0.2200 | 1.0000 | 0.0000 | 0.0200 | 0.9600 |
| artifact_bank | residual_only | 0.1360 | 0.1660 | 200 | 200 | 0.5300 | 0.5550 | 0.0000 | 0.0000 | 0.1200 | 0.2200 | 1.0000 | 0.0000 | 0.0000 | 1.0000 |
| combined_pypeec_aware | residual_only | 0.1220 | 0.1880 | 200 | 200 | 0.5850 | 0.6400 | 0.0000 | 0.0000 | 0.3400 | 0.5600 | 1.0000 | 0.0000 | 0.0200 | 0.9800 |
| combined_pypeec_aware | parameter_count | 0.1140 | 0.1980 | 200 | 200 | 0.5750 | 0.6450 | 0.0200 | 0.0200 | 0.2800 | 0.5600 | 1.0000 | 0.0000 | 0.0000 | 0.9800 |
| combined_pypeec_aware | bic_like | 0.1120 | 0.2160 | 200 | 200 | 0.5700 | 0.6600 | 0.0400 | 0.0200 | 0.2400 | 0.6200 | 1.0000 | 0.0000 | 0.0200 | 0.9600 |
| combined_pypeec_aware | default_score | 0.1120 | 0.2040 | 200 | 200 | 0.5700 | 0.6500 | 0.0400 | 0.0200 | 0.2400 | 0.5800 | 1.0000 | 0.0000 | 0.0200 | 0.9600 |

Rows are ranked by calibration objective and evaluated on held-out PyPEEC cases. This is a pilot split on the current mini distribution, not broad CAD/FEM validation.


# Exp08 P1 H0/H1 model-selection trade-off table

| basis mode | evidence mode | heldout H0 acc | heldout H1 acc | heldout 4-way acc | heldout H0 false H1 | heldout H0 false H2 | heldout H0 false H3 | heldout median residual | heldout median params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finite_width_sheet | h0_conservative | 0.9400 | 1.0000 | 0.9850 | 0.0000 | 0.0000 | 0.0600 | 0.1061 | 5.0000 |
| combined_pypeec_aware | h0_conservative | 0.8000 | 0.3000 | 0.7750 | 0.0000 | 0.0000 | 0.2000 | 0.1097 | 9.0000 |
| finite_width_sheet | extra_count | 0.7600 | 1.0000 | 0.9400 | 0.0000 | 0.0400 | 0.2000 | 0.1050 | 5.0000 |
| artifact_bank | h0_conservative | 0.7400 | 0.6200 | 0.8400 | 0.0000 | 0.1400 | 0.1200 | 0.1772 | 4.0000 |
| combined_pypeec_aware | extra_count | 0.7000 | 0.4400 | 0.7850 | 0.0000 | 0.0000 | 0.3000 | 0.1074 | 9.0000 |
| base | h0_conservative | 0.6200 | 0.6400 | 0.8150 | 0.0000 | 0.1000 | 0.2800 | 0.1766 | 4.0000 |
| distributed_via | h0_conservative | 0.6200 | 0.0800 | 0.6750 | 0.0000 | 0.1000 | 0.2800 | 0.1766 | 3.0000 |
| artifact_bank | extra_count | 0.5600 | 0.8200 | 0.8450 | 0.0000 | 0.2800 | 0.1600 | 0.1766 | 4.0000 |
| return_bank | h0_conservative | 0.5000 | 0.6200 | 0.7800 | 0.0000 | 0.2800 | 0.2200 | 0.1614 | 5.0000 |
| base | extra_count | 0.4200 | 0.8400 | 0.8150 | 0.0000 | 0.2200 | 0.3600 | 0.1766 | 4.0000 |
| distributed_via | extra_count | 0.4200 | 0.1400 | 0.6400 | 0.0000 | 0.2200 | 0.3600 | 0.1766 | 4.0000 |
| return_bank | extra_count | 0.3800 | 0.8200 | 0.8000 | 0.0000 | 0.3200 | 0.3000 | 0.1605 | 5.0000 |
| finite_width_sheet | bic_like | 0.2000 | 1.0000 | 0.8000 | 0.0200 | 0.1600 | 0.6200 | 0.1042 | 5.0000 |
| finite_width_sheet | default_score | 0.1200 | 1.0000 | 0.7800 | 0.0400 | 0.1600 | 0.6800 | 0.1042 | 5.0000 |
| base | bic_like | 0.0800 | 0.9000 | 0.7450 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| base | default_score | 0.0800 | 0.9000 | 0.7450 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| distributed_via | default_score | 0.0800 | 0.8600 | 0.7350 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| distributed_via | bic_like | 0.0800 | 0.8000 | 0.7200 | 0.0000 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| finite_width_sheet | parameter_count | 0.0600 | 1.0000 | 0.7650 | 0.0800 | 0.1800 | 0.6800 | 0.1042 | 5.0000 |
| return_bank | bic_like | 0.0600 | 0.7800 | 0.7100 | 0.0000 | 0.6200 | 0.3200 | 0.1594 | 6.0000 |
| base | parameter_count | 0.0400 | 0.9000 | 0.7350 | 0.0000 | 0.3400 | 0.6200 | 0.1766 | 4.0000 |
| distributed_via | parameter_count | 0.0400 | 0.9000 | 0.7350 | 0.0000 | 0.3400 | 0.6200 | 0.1766 | 4.0000 |
| return_bank | default_score | 0.0400 | 0.7800 | 0.7050 | 0.0000 | 0.6600 | 0.3000 | 0.1589 | 6.0000 |
| return_bank | parameter_count | 0.0200 | 0.7800 | 0.7000 | 0.0000 | 0.7000 | 0.2800 | 0.1589 | 6.0000 |
| combined_pypeec_aware | bic_like | 0.0200 | 0.6200 | 0.6600 | 0.0000 | 0.0200 | 0.9600 | 0.0970 | 9.0000 |
| combined_pypeec_aware | default_score | 0.0200 | 0.5800 | 0.6500 | 0.0000 | 0.0200 | 0.9600 | 0.0970 | 9.0000 |
| combined_pypeec_aware | parameter_count | 0.0200 | 0.5600 | 0.6450 | 0.0000 | 0.0000 | 0.9800 | 0.0970 | 9.0000 |
| artifact_bank | bic_like | 0.0200 | 0.3000 | 0.5800 | 0.0000 | 0.0600 | 0.9200 | 0.1710 | 5.0000 |
| artifact_bank | default_score | 0.0200 | 0.3000 | 0.5800 | 0.0000 | 0.0600 | 0.9200 | 0.1710 | 5.0000 |
| artifact_bank | parameter_count | 0.0200 | 0.2200 | 0.5600 | 0.0000 | 0.0200 | 0.9600 | 0.1710 | 5.0000 |
| finite_width_sheet | residual_only | 0.0000 | 1.0000 | 0.7500 | 0.0800 | 0.1800 | 0.7400 | 0.1042 | 5.0000 |
| base | residual_only | 0.0000 | 0.9000 | 0.7250 | 0.0200 | 0.3400 | 0.6400 | 0.1766 | 4.0000 |
| distributed_via | residual_only | 0.0000 | 0.9000 | 0.7250 | 0.0800 | 0.3400 | 0.5800 | 0.1766 | 4.0000 |
| return_bank | residual_only | 0.0000 | 0.7800 | 0.6950 | 0.0000 | 0.7600 | 0.2400 | 0.1589 | 6.0000 |
| combined_pypeec_aware | residual_only | 0.0000 | 0.5600 | 0.6400 | 0.0000 | 0.0200 | 0.9800 | 0.0970 | 9.0000 |
| artifact_bank | residual_only | 0.0000 | 0.2200 | 0.5550 | 0.0000 | 0.0000 | 1.0000 | 0.1710 | 5.0000 |

This table treats H0/no-via safety and H1/true-via recall as primary endpoints rather than secondary columns hidden inside overall accuracy.


# Exp08 P0 repeated-split PyPEEC model-selection stability

| basis mode | evidence mode | repeats | top-1 selected | top-1 rate | heldout obj mean | heldout obj std | heldout obj CI low | heldout obj CI high | heldout 4-way mean | heldout 4-way std | heldout H0 mean | heldout H0 std | heldout H1 mean | heldout H1 std | heldout H2 mean | heldout H0 false-any mean | heldout params mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| finite_width_sheet | h0_conservative | 31 | 31 | 1.0000 | 0.7832 | 0.0188 | 0.7540 | 0.8120 | 0.9105 | 0.0130 | 0.9645 | 0.0195 | 0.6774 | 0.0473 | 1.0000 | 0.0355 | 5.1129 |
| finite_width_sheet | extra_count | 31 | 0 | 0.0000 | 0.7183 | 0.0235 | 0.6830 | 0.7530 | 0.8868 | 0.0142 | 0.7819 | 0.0331 | 0.7652 | 0.0451 | 1.0000 | 0.2181 | 5.1129 |
| artifact_bank | h0_conservative | 31 | 0 | 0.0000 | 0.5863 | 0.0266 | 0.5500 | 0.6270 | 0.7790 | 0.0165 | 0.6606 | 0.0414 | 0.4555 | 0.0560 | 1.0000 | 0.3394 | 4.0323 |
| base | h0_conservative | 31 | 0 | 0.0000 | 0.5496 | 0.0221 | 0.5200 | 0.5880 | 0.7615 | 0.0146 | 0.5794 | 0.0398 | 0.4665 | 0.0550 | 1.0000 | 0.4206 | 4.0000 |
| artifact_bank | extra_count | 31 | 0 | 0.0000 | 0.5253 | 0.0253 | 0.4900 | 0.5700 | 0.7592 | 0.0165 | 0.4761 | 0.0423 | 0.5606 | 0.0625 | 1.0000 | 0.5239 | 4.0484 |
| return_bank | h0_conservative | 31 | 0 | 0.0000 | 0.4802 | 0.0219 | 0.4490 | 0.5180 | 0.7373 | 0.0137 | 0.4935 | 0.0388 | 0.4555 | 0.0542 | 1.0000 | 0.5065 | 5.1613 |
| finite_width_sheet | bic_like | 31 | 0 | 0.0000 | 0.4742 | 0.0181 | 0.4450 | 0.5000 | 0.7882 | 0.0086 | 0.1529 | 0.0343 | 1.0000 | 0.0000 | 1.0000 | 0.8471 | 5.1129 |
| combined_pypeec_aware | h0_conservative | 31 | 0 | 0.0000 | 0.4523 | 0.0272 | 0.4180 | 0.4930 | 0.7324 | 0.0150 | 0.7671 | 0.0560 | 0.1626 | 0.0436 | 1.0000 | 0.2329 | 9.0000 |
| finite_width_sheet | default_score | 31 | 0 | 0.0000 | 0.4371 | 0.0171 | 0.4200 | 0.4600 | 0.7697 | 0.0069 | 0.0787 | 0.0278 | 1.0000 | 0.0000 | 1.0000 | 0.9213 | 5.1129 |
| base | extra_count | 31 | 0 | 0.0000 | 0.4357 | 0.0254 | 0.3930 | 0.4800 | 0.7150 | 0.0171 | 0.2884 | 0.0399 | 0.5716 | 0.0603 | 1.0000 | 0.7116 | 4.0000 |
| distributed_via | h0_conservative | 31 | 0 | 0.0000 | 0.4223 | 0.0219 | 0.3890 | 0.4580 | 0.6553 | 0.0122 | 0.5794 | 0.0398 | 0.0419 | 0.0246 | 1.0000 | 0.4206 | 4.0000 |
| finite_width_sheet | parameter_count | 31 | 0 | 0.0000 | 0.4223 | 0.0177 | 0.4050 | 0.4400 | 0.7624 | 0.0061 | 0.0497 | 0.0243 | 1.0000 | 0.0000 | 1.0000 | 0.9503 | 5.1290 |
| combined_pypeec_aware | extra_count | 31 | 0 | 0.0000 | 0.4200 | 0.0213 | 0.3890 | 0.4540 | 0.7229 | 0.0121 | 0.6626 | 0.0494 | 0.2290 | 0.0484 | 1.0000 | 0.3374 | 9.0000 |
| finite_width_sheet | residual_only | 31 | 0 | 0.0000 | 0.3965 | 0.0103 | 0.3800 | 0.4000 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 5.1774 |
| return_bank | extra_count | 31 | 0 | 0.0000 | 0.3964 | 0.0293 | 0.3660 | 0.4490 | 0.7124 | 0.0167 | 0.2800 | 0.0387 | 0.5697 | 0.0586 | 1.0000 | 0.7200 | 5.7258 |
| base | bic_like | 31 | 0 | 0.0000 | 0.3903 | 0.0142 | 0.3680 | 0.4120 | 0.7155 | 0.0102 | 0.0587 | 0.0215 | 0.8032 | 0.0397 | 1.0000 | 0.9413 | 4.0000 |
| base | default_score | 31 | 0 | 0.0000 | 0.3894 | 0.0138 | 0.3660 | 0.4120 | 0.7161 | 0.0098 | 0.0503 | 0.0209 | 0.8142 | 0.0374 | 1.0000 | 0.9497 | 4.0000 |
| base | parameter_count | 31 | 0 | 0.0000 | 0.3850 | 0.0126 | 0.3680 | 0.4050 | 0.7150 | 0.0092 | 0.0348 | 0.0183 | 0.8252 | 0.0366 | 1.0000 | 0.9652 | 4.0000 |
| distributed_via | parameter_count | 31 | 0 | 0.0000 | 0.3848 | 0.0131 | 0.3680 | 0.4080 | 0.7148 | 0.0097 | 0.0348 | 0.0183 | 0.8245 | 0.0383 | 1.0000 | 0.9652 | 4.0000 |
| distributed_via | residual_only | 31 | 0 | 0.0000 | 0.3690 | 0.0101 | 0.3550 | 0.3840 | 0.7145 | 0.0079 | 0.0000 | 0.0000 | 0.8581 | 0.0315 | 1.0000 | 1.0000 | 4.4194 |
| base | residual_only | 31 | 0 | 0.0000 | 0.3675 | 0.0110 | 0.3480 | 0.3810 | 0.7063 | 0.0092 | 0.0000 | 0.0000 | 0.8252 | 0.0366 | 1.0000 | 1.0000 | 4.0000 |
| distributed_via | default_score | 31 | 0 | 0.0000 | 0.3476 | 0.0163 | 0.3230 | 0.3720 | 0.6813 | 0.0122 | 0.0503 | 0.0209 | 0.6748 | 0.0476 | 1.0000 | 0.9497 | 4.0000 |
| distributed_via | bic_like | 31 | 0 | 0.0000 | 0.3354 | 0.0167 | 0.3130 | 0.3640 | 0.6697 | 0.0124 | 0.0587 | 0.0215 | 0.6200 | 0.0477 | 1.0000 | 0.9413 | 4.0000 |
| return_bank | bic_like | 31 | 0 | 0.0000 | 0.3025 | 0.0149 | 0.2840 | 0.3310 | 0.6784 | 0.0110 | 0.0419 | 0.0199 | 0.6716 | 0.0418 | 1.0000 | 0.9581 | 6.0000 |
| return_bank | default_score | 31 | 0 | 0.0000 | 0.2966 | 0.0130 | 0.2830 | 0.3210 | 0.6755 | 0.0102 | 0.0303 | 0.0160 | 0.6716 | 0.0418 | 1.0000 | 0.9697 | 6.0000 |
| return_bank | parameter_count | 31 | 0 | 0.0000 | 0.2964 | 0.0126 | 0.2780 | 0.3180 | 0.6765 | 0.0100 | 0.0232 | 0.0135 | 0.6826 | 0.0409 | 1.0000 | 0.9768 | 6.0000 |
| return_bank | residual_only | 31 | 0 | 0.0000 | 0.2879 | 0.0119 | 0.2690 | 0.3050 | 0.6732 | 0.0099 | 0.0000 | 0.0000 | 0.6929 | 0.0395 | 1.0000 | 1.0000 | 6.0000 |
| distributed_via | extra_count | 31 | 0 | 0.0000 | 0.2863 | 0.0231 | 0.2500 | 0.3190 | 0.5905 | 0.0133 | 0.2884 | 0.0399 | 0.0735 | 0.0289 | 1.0000 | 0.7116 | 4.0000 |
| artifact_bank | bic_like | 31 | 0 | 0.0000 | 0.1859 | 0.0142 | 0.1630 | 0.2040 | 0.5677 | 0.0111 | 0.0232 | 0.0135 | 0.2477 | 0.0436 | 1.0000 | 0.9768 | 5.0000 |
| artifact_bank | default_score | 31 | 0 | 0.0000 | 0.1859 | 0.0142 | 0.1630 | 0.2040 | 0.5677 | 0.0111 | 0.0232 | 0.0135 | 0.2477 | 0.0436 | 1.0000 | 0.9768 | 5.0000 |
| artifact_bank | parameter_count | 31 | 0 | 0.0000 | 0.1699 | 0.0129 | 0.1480 | 0.1890 | 0.5544 | 0.0101 | 0.0232 | 0.0135 | 0.1942 | 0.0397 | 1.0000 | 0.9768 | 5.0000 |
| combined_pypeec_aware | bic_like | 31 | 0 | 0.0000 | 0.1649 | 0.0186 | 0.1330 | 0.1900 | 0.6160 | 0.0124 | 0.0335 | 0.0164 | 0.4303 | 0.0465 | 1.0000 | 0.9665 | 9.0484 |
| combined_pypeec_aware | default_score | 31 | 0 | 0.0000 | 0.1603 | 0.0195 | 0.1300 | 0.1860 | 0.6121 | 0.0131 | 0.0335 | 0.0164 | 0.4148 | 0.0495 | 1.0000 | 0.9665 | 9.0484 |
| combined_pypeec_aware | parameter_count | 31 | 0 | 0.0000 | 0.1584 | 0.0168 | 0.1330 | 0.1810 | 0.6123 | 0.0118 | 0.0232 | 0.0135 | 0.4258 | 0.0472 | 1.0000 | 0.9768 | 9.0484 |
| combined_pypeec_aware | residual_only | 31 | 0 | 0.0000 | 0.1547 | 0.0157 | 0.1340 | 0.1820 | 0.6131 | 0.0118 | 0.0000 | 0.0000 | 0.4523 | 0.0470 | 1.0000 | 1.0000 | 9.0484 |
| artifact_bank | residual_only | 31 | 0 | 0.0000 | 0.1486 | 0.0109 | 0.1330 | 0.1600 | 0.5405 | 0.0091 | 0.0000 | 0.0000 | 0.1619 | 0.0364 | 1.0000 | 1.0000 | 5.0000 |

Rows use repeated stratified calibration/held-out splits of the same PyPEEC mini distribution. The table estimates ranking stability; it does not create a final model-selection claim.


# Exp08 P0 class-specific selective hypothesis audit

| policy | field | basis mode | evidence mode | repeats | coverage mean | coverage std | coverage p10 | coverage p90 | accepted acc mean | accepted acc std | H0 false-any mean | H0 false-any median | H0 accepted-correct mean | H1 accepted-correct mean | H1 acceptance mean | unknown mean | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| class_specific_margin_refusal | B_pypeec | finite_width_sheet | h0_conservative | 31 | 0.7163 | 0.0243 | 0.6850 | 0.7450 | 0.9836 | 0.0121 | 0.0245 | 0.0200 | 0.8633 | 0.9669 | 0.7006 | 0.2837 | h0_safe_but_h1_recall_limited |

This table is the formal audit of the current core bottleneck: class-specific refusal can carve out a trusted-output region, but a reliable detector also needs high true-via acceptance. Thresholds are selected only on calibration folds and evaluated on repeated held-out folds of the PyPEEC mini distribution.


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


# Exp08 P1 stacked evidence feature ablation

| feature policy | n features | repeats | heldout 4-way mean | heldout 4-way std | heldout H0 mean | heldout H1 mean | heldout H2 mean | heldout H3 mean | heldout H0 false-any mean | heldout objective mean | heldout objective std | alpha counts | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| h0_conservative_all_basis | 66 | 31 | 0.9958 | 0.0058 | 1.0000 | 0.9832 | 1.0000 | 1.0000 | 0.0000 | 3.7799 | 0.0280 |  | breakthrough_candidate |
| all_features | 396 | 31 | 0.9963 | 0.0036 | 0.9935 | 0.9916 | 1.0000 | 1.0000 | 0.0065 | 3.7564 | 0.0552 |  | breakthrough_candidate |
| no_return_bank | 330 | 31 | 0.9956 | 0.0038 | 0.9903 | 0.9923 | 1.0000 | 1.0000 | 0.0097 | 3.7404 | 0.0641 |  | breakthrough_candidate |
| no_distributed_via | 330 | 31 | 0.9956 | 0.0035 | 0.9903 | 0.9923 | 1.0000 | 1.0000 | 0.0097 | 3.7404 | 0.0628 |  | breakthrough_candidate |
| no_artifact_bank | 330 | 31 | 0.9950 | 0.0036 | 0.9877 | 0.9923 | 1.0000 | 1.0000 | 0.0123 | 3.7270 | 0.0665 |  | breakthrough_candidate |
| no_finite_width_sheet | 330 | 31 | 0.9795 | 0.0118 | 1.0000 | 0.9181 | 1.0000 | 1.0000 | 0.0000 | 3.7017 | 0.0566 |  | breakthrough_candidate |
| finite_width_all_evidence | 66 | 31 | 0.9927 | 0.0046 | 0.9787 | 0.9923 | 1.0000 | 1.0000 | 0.0213 | 3.6800 | 0.0833 |  | breakthrough_candidate |
| finite_width_h0_conservative_only | 11 | 31 | 0.9648 | 0.0435 | 0.9826 | 0.8768 | 1.0000 | 1.0000 | 0.0174 | 3.5615 | 0.2664 |  | h1_recall_limited |
| margin_residual_nbasis_only | 108 | 31 | 0.9342 | 0.0249 | 0.9994 | 0.7374 | 1.0000 | 1.0000 | 6.452e-04 | 3.4815 | 0.1188 |  | h1_recall_limited |
| scores_plus_margin | 180 | 31 | 0.9210 | 0.0194 | 1.0000 | 0.6839 | 1.0000 | 1.0000 | 0.0000 | 3.4206 | 0.0929 |  | h1_recall_limited |
| scores_only | 144 | 31 | 0.9116 | 0.0177 | 1.0000 | 0.6465 | 1.0000 | 1.0000 | 0.0000 | 3.3757 | 0.0850 |  | h1_recall_limited |
| pred_one_hot_only | 144 | 31 | 0.9773 | 0.0066 | 0.9103 | 0.9987 | 1.0000 | 1.0000 | 0.0897 | 3.3321 | 0.1423 |  | h0_safety_watch |
| scores_plus_residual | 180 | 31 | 0.8918 | 0.0173 | 0.7206 | 0.8465 | 1.0000 | 1.0000 | 0.2794 | 2.1631 | 0.3528 |  | h1_recall_limited |

All rows use fixed alpha=100 and repeated PyPEEC calibration/held-out splits. This ablation identifies whether the breakthrough comes from scores, margins, predicted one-hot outputs, or specific basis families.


# Exp08 P2 stacked evidence unknown-safety stress

| policy | clean false reject target | repeats | clean reject | accepted clean acc | hidden reject | hidden accept | accepted hidden acc | accepted hidden risk | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fixed_alpha=100_inner_feature_distance | 0.2000 | 31 | 0.1802 | 0.9984 | 1.0000 | 0.0000 | nan | nan | low_hidden_exposure_candidate |
| fixed_alpha=100_inner_confidence_plus_distance | 0.2000 | 31 | 0.1777 | 0.9990 | 0.9318 | 0.0682 | 0.0526 | 0.9474 | strong_hidden_rejection_but_risk_tail |
| fixed_alpha=100_inner_confidence_margin | 0.2000 | 31 | 0.1706 | 0.9979 | 0.6791 | 0.3209 | 0.2197 | 0.7803 | diagnostic_only |

Each threshold is selected only inside the PyPEEC calibration fold and then applied to held-out PyPEEC and hidden-mechanism stress. Confidence-margin rejection tests classifier uncertainty; feature-distance rejection tests whether a stacked-evidence vector is outside the calibrated in-library class manifold; the combined row is an ablation rather than a tuned production rule.


# Exp08 near-boundary hidden stress with stacked-evidence OOD screens

| policy | clean false reject target | repeats | clean reject | accepted clean acc | near-hidden reject | near-hidden accept | accepted near-hidden acc | accepted near-hidden risk | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fixed_alpha=100_inner_feature_distance | 0.2000 | 31 | 0.1802 | 0.9984 | 0.8508 | 0.1492 | 1.0000 | 0.0000 | low_accepted_hidden_risk_candidate |
| fixed_alpha=100_inner_confidence_plus_distance | 0.2000 | 31 | 0.1777 | 0.9990 | 0.8051 | 0.1949 | 1.0000 | 0.0000 | low_accepted_hidden_risk_candidate |
| fixed_alpha=100_inner_confidence_margin | 0.2000 | 31 | 0.1706 | 0.9979 | 0.7792 | 0.2208 | 0.9705 | 0.0295 | low_accepted_hidden_risk_candidate |

Near-boundary hidden cases are intentionally closer to known return/via/artifact candidates than the base hidden stress. This table tests whether the distance screen only rejects obvious outliers or also protects against harder near-manifold unknowns.


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


# Exp08 stacked-evidence space diagnostics

| dataset | n | median feature distance | p90 feature distance | pc1 mean | pc1 std | pc2 mean | pc2 std | label counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| in_library_pypeec | 400 | 0.1925 | 0.4064 | 0.0000 | 13.1223 | 5.684e-16 | 9.4895 | H0_sheet_only:100, H1_sheet_via:100, H2_sheet_return:100, H3_sheet_artifact:100 |
| base_hidden | 96 | 1.4049 | 2.4390 | 9.2475 | 1.4390 | 2.3968 | 3.2112 | H0_sheet_only:24, H1_sheet_via:48, H2_sheet_return:0, H3_sheet_artifact:24 |
| near_boundary_hidden | 96 | 0.6678 | 1.0957 | 9.1238 | 1.9415 | 1.8101 | 5.1288 | H0_sheet_only:48, H1_sheet_via:48, H2_sheet_return:0, H3_sheet_artifact:0 |

The companion `stacked_evidence_space_pca.png` projects in-library PyPEEC, base hidden, and near-boundary hidden evidence vectors into the first two PCA axes of the in-library stacked-evidence space. The table reports feature-distance separation; the plot is explanatory only and is not used to tune thresholds.


# Exp08 P3 stacked evidence external/operator stress

| stress field | repeats | n cases | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | H0 false-any |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_finite | 31 | 400 | 0.9981 | 1.0000 | 0.9923 | 1.0000 | 1.0000 | 0.0000 |
| B_centerline | 31 | 400 | 0.9981 | 1.0000 | 0.9923 | 1.0000 | 1.0000 | 0.0000 |
| hidden_mechanism | 31 | 96 | 0.4382 | 0.9973 | 0.3777 | nan | 0.0000 | 0.0027 |

The calibrator is trained on PyPEEC calibration folds and evaluated on operator-shifted or hidden-mechanism fields. These are stress proxies, not real CAD/FEM/QDM validation.


# Exp08 P4 stacked evidence selective-risk table

| policy | coverage | repeats | accepted acc | accepted H0 acc | accepted H1 acc | accepted H0 false-any | H1 acceptance | reject rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fixed_alpha=100_confidence_margin | 0.2000 | 31 | 0.9919 | 1.0000 | 0.9787 | 0.0000 | 0.3116 | 0.8000 |
| fixed_alpha=100_confidence_margin | 0.5000 | 31 | 0.9965 | 1.0000 | 0.9834 | 0.0000 | 0.4310 | 0.5000 |
| fixed_alpha=100_confidence_margin | 0.8000 | 31 | 0.9978 | 1.0000 | 0.9877 | 0.0000 | 0.5794 | 0.2000 |
| fixed_alpha=100_confidence_margin | 1.0000 | 31 | 0.9963 | 0.9935 | 0.9916 | 0.0065 | 1.0000 | 0.0000 |

This table keeps refusal in the final diagnostic path. A strong calibrator should still expose coverage/risk rather than forcing every ambiguous residual into a hard label.


# Exp08 P1 PyPEEC distribution target coverage

| true hypothesis | current unique cases | target cases | gap to target | observed families | status |
| --- | --- | --- | --- | --- | --- |
| H0_sheet_only | 100 | 100 | 0 | canonical, no_via_background | meets_target |
| H1_sheet_via | 100 | 100 | 0 | canonical, dense_via_background, l1_jog, multi_via | meets_target |
| H2_sheet_return | 100 | 100 | 0 | return_path | meets_target |
| H3_sheet_artifact | 100 | 100 | 0 | bend_artifact | meets_target |

This table audits the current PyPEEC model-selection target coverage. Meeting the mini-distribution targets is necessary for stronger model-selection stress, but it is still not a claim that CAD/FEM/QDM distribution coverage has been solved.


### P1: H0/no-via hard negatives

# Exp08 P1 H0/no-via hard-negative diagnostic

| dataset | mode | n | H0 acc | false H1 rate | false H2 rate | false H3 rate | 4-way acc | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pypeec_no_via | base/default_score | 100 | 0.0500 | 0.0000 | 0.3300 | 0.6200 | 0.0500 | 0.1709 |
| pypeec_no_via | base/h0_conservative | 100 | 0.5800 | 0.0000 | 0.1400 | 0.2800 | 0.5800 | 0.1742 |
| pypeec_no_via | finite_width_sheet/default_score | 100 | 0.0800 | 0.0300 | 0.2400 | 0.6500 | 0.0800 | 0.1004 |
| pypeec_no_via | finite_width_sheet/h0_conservative | 100 | 0.9700 | 0.0000 | 0.0000 | 0.0300 | 0.9700 | 0.1015 |
| pypeec_no_via | return_bank/default_score | 100 | 0.0300 | 0.0000 | 0.6200 | 0.3500 | 0.0300 | 0.1609 |
| pypeec_no_via | return_bank/h0_conservative | 100 | 0.5000 | 0.0000 | 0.2800 | 0.2200 | 0.5000 | 0.1633 |
| pypeec_no_via | artifact_bank/default_score | 100 | 0.0200 | 0.0000 | 0.1300 | 0.8500 | 0.0200 | 0.1588 |
| pypeec_no_via | artifact_bank/h0_conservative | 100 | 0.6600 | 0.0000 | 0.1600 | 0.1800 | 0.6600 | 0.1642 |
| pypeec_no_via | distributed_via/default_score | 100 | 0.0500 | 0.0000 | 0.3300 | 0.6200 | 0.0500 | 0.1709 |
| pypeec_no_via | distributed_via/h0_conservative | 100 | 0.5800 | 0.0000 | 0.1400 | 0.2800 | 0.5800 | 0.1742 |
| pypeec_no_via | combined_pypeec_aware/default_score | 100 | 0.0300 | 0.0000 | 0.0300 | 0.9400 | 0.0300 | 0.0807 |
| pypeec_no_via | combined_pypeec_aware/h0_conservative | 100 | 0.7600 | 0.0000 | 0.0000 | 0.2400 | 0.7600 | 0.0947 |
| clean_ood_no_via | base/default_score | 25 | 0.7200 | 0.0000 | 0.2800 | 0.0000 | 0.7200 | 0.1256 |
| hidden_return_no_via | base/default_score | 24 | 0.7500 | 0.0000 | 0.2500 | 0.0000 | 0.7500 | 0.1782 |

H0/no-via is the hard negative class: a reliable system must avoid explaining every residual as via, return, or artifact.


### P0-next/P1-next: registration marginalization

# Exp08 P0-next PyPEEC bridge with via-location marginalization

| field | mode | 4-way acc | H1 acc | via AUC | via recall | via F1 | no-via FP | median best offset um |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | base | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.3333 |  |
| B_centerline | via_location_marginalized | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 0.6667 | 240.0000 |
| B_pypeec | base | 0.7175 | 0.8200 | 0.9534 | 0.9900 | 0.6600 | 0.3367 |  |
| B_pypeec | via_location_marginalized | 0.7100 | 0.8200 | 0.5223 | 0.8600 | 0.4332 | 0.7033 | 240.0000 |

Offsets are fixed by configuration and are not selected on PyPEEC labels.


# Exp08 P1 global graph-to-field registration diagnostic

| field | mode | 4-way acc | via AUC | no-via FP | median residual | median translation um | median abs rotation deg | median scale delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B_centerline | base | 1.0000 | 1.0000 | 0.3333 | 0.0011 |  |  |  |
| B_centerline | global_registration_search | 1.0000 | 1.0000 | 0.3333 | 0.0011 | 0.0000 | 0.0000 | 0.0000 |
| B_pypeec | base | 0.7175 | 0.9534 | 0.3367 | 0.1715 |  |  |  |
| B_pypeec | global_registration_search | 0.7250 | 0.9546 | 0.3367 | 0.1666 | 0.0000 | 0.0000 | 0.0150 |

The transform grid is fixed by config and is not selected on PyPEEC labels.


# Exp08 P0-next/P1-next via-location marginalization

| family | mode | 4-way acc | H1 acc | via recall | via F1 | no-via FP | median best offset um |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_hidden | base | 0.4167 | 0.4583 | 0.4167 | 0.5882 | 0.0000 |  |
| all_hidden | via_location_marginalized | 0.6250 | 0.8958 | 0.4375 | 0.6087 | 0.0000 | 240.0000 |
| combined_true_via_hidden_return | base | 0.7917 | 0.7917 | 0.7917 | 0.8837 | 0.0000 |  |
| combined_true_via_hidden_return | via_location_marginalized | 0.7917 | 0.7917 | 0.4167 | 0.5882 | 0.0000 | 0.0000 |
| hidden_return_no_via | base | 0.7500 | nan | 0.0000 | 0.0000 | 0.0000 |  |
| hidden_return_no_via | via_location_marginalized | 0.7083 | nan | 0.0000 | 0.0000 | 0.0000 | 339.4113 |
| mismatched_artifact | base | 0.0000 | nan | 0.0000 | 0.0000 | 0.0000 |  |
| mismatched_artifact | via_location_marginalized | 0.0000 | nan | 0.0000 | 0.0000 | 0.0000 | 289.7056 |
| shifted_true_via | base | 0.1250 | 0.1250 | 0.0417 | 0.0800 | 0.0000 |  |
| shifted_true_via | via_location_marginalized | 1.0000 | 1.0000 | 0.4583 | 0.6286 | 0.0000 | 240.0000 |

Via candidate offsets are fixed by config and selected without hidden/PyPEEC labels.


### P1: hidden-mechanism OOD stress

# Exp08 hidden-mechanism OOD stress

| family | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | via AUC | via recall | via F1 | no-via FP | median margin | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all_hidden | 96 | 0.4167 | 0.7500 | 0.4583 | nan | 0.0000 | 0.9288 | 0.4167 | 0.5882 | 0.0000 | 4.485e-04 | 0.1529 |
| combined_true_via_hidden_return | 24 | 0.7917 | nan | 0.7917 | nan | nan | nan | 0.7917 | 0.8837 | 0.0000 | 0.0033 | 0.1513 |
| hidden_return_no_via | 24 | 0.7500 | 0.7500 | nan | nan | nan | nan | 0.0000 | 0.0000 | 0.0000 | 4.703e-04 | 0.1782 |
| mismatched_artifact | 24 | 0.0000 | nan | nan | nan | 0.0000 | nan | 0.0000 | 0.0000 | 0.0000 | 3.450e-04 | 0.1427 |
| shifted_true_via | 24 | 0.1250 | nan | 0.1250 | nan | nan | nan | 0.0417 | 0.0800 | 0.0000 | 2.773e-04 | 0.1157 |

Hidden mechanisms are deliberately missing or mismatched in the candidate library; perfect accuracy is not expected.


# Exp08 hidden-mechanism failure cases

| case | family | class | true H | pred H | margin | via evidence | true residual | pred residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hidden_shifted_true_via_ood_09000_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 9.572e-05 | -1.379e-04 | 0.1764 | 0.1768 |
| hidden_mismatched_artifact_ood_10000_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 4.665e-04 | -4.869e-04 | 0.2096 | 0.2096 |
| hidden_hidden_return_no_via_ood_08001_no_via | hidden_return_no_via | no_via | H0_sheet_only | H2_sheet_return | 7.840e-04 | -4.943e-04 | 0.2764 | 0.2751 |
| hidden_shifted_true_via_ood_09001_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 4.693e-04 | -4.693e-04 | 0.2166 | 0.2166 |
| hidden_mismatched_artifact_ood_10001_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 3.791e-04 | -5.000e-04 | 0.1393 | 0.1395 |
| hidden_hidden_return_no_via_ood_08002_no_via | hidden_return_no_via | no_via | H0_sheet_only | H2_sheet_return | 8.541e-04 | -4.802e-04 | 0.2050 | 0.2036 |
| hidden_shifted_true_via_ood_09002_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 4.044e-04 | -4.674e-04 | 0.1960 | 0.1960 |
| hidden_mismatched_artifact_ood_10002_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H2_sheet_return | 5.618e-04 | -4.609e-04 | 0.1547 | 0.1540 |
| hidden_shifted_true_via_ood_09003_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 1.865e-05 | -1.865e-05 | 0.1029 | 0.1034 |
| hidden_mismatched_artifact_ood_10003_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 3.131e-04 | -4.526e-04 | 0.1822 | 0.1824 |
| hidden_hidden_return_no_via_ood_08004_no_via | hidden_return_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0053 | -4.949e-04 | 0.1686 | 0.1628 |
| hidden_shifted_true_via_ood_09004_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 8.890e-05 | -3.070e-04 | 0.1136 | 0.1138 |
| hidden_mismatched_artifact_ood_10004_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 4.782e-04 | -5.000e-04 | 0.0878 | 0.0878 |
| hidden_shifted_true_via_ood_09005_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 4.512e-04 | -4.773e-04 | 0.1024 | 0.1024 |
| hidden_mismatched_artifact_ood_10005_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 2.585e-04 | -2.585e-04 | 0.1347 | 0.1347 |
| hidden_combined_true_via_hidden_return_ood_11005_true_via | combined_true_via_hidden_return | true_via | H1_sheet_via | H2_sheet_return | 0.0075 | 1.737e-04 | 0.2517 | 0.2442 |
| hidden_shifted_true_via_ood_09006_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 3.948e-04 | -4.123e-04 | 0.1150 | 0.1151 |
| hidden_mismatched_artifact_ood_10006_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 2.380e-04 | -3.926e-04 | 0.1289 | 0.1291 |
| hidden_shifted_true_via_ood_09007_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 3.094e-04 | -3.094e-04 | 0.2254 | 0.2256 |
| hidden_mismatched_artifact_ood_10007_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 2.074e-05 | -4.865e-04 | 0.1054 | 0.1055 |
| hidden_hidden_return_no_via_ood_08008_no_via | hidden_return_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0041 | -4.837e-04 | 0.1656 | 0.1610 |
| hidden_shifted_true_via_ood_09008_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 2.943e-04 | -2.943e-04 | 0.1947 | 0.1949 |
| hidden_mismatched_artifact_ood_10008_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 6.849e-05 | -4.946e-04 | 0.2148 | 0.2150 |
| hidden_combined_true_via_hidden_return_ood_11008_true_via | combined_true_via_hidden_return | true_via | H1_sheet_via | H2_sheet_return | 0.0045 | 0.0044 | 0.1476 | 0.1431 |
| hidden_shifted_true_via_ood_09009_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 8.904e-05 | -4.921e-04 | 0.1249 | 0.1249 |
| hidden_mismatched_artifact_ood_10009_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H2_sheet_return | 6.579e-04 | -4.414e-04 | 0.1329 | 0.1319 |
| hidden_mismatched_artifact_ood_10010_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 3.284e-04 | -3.284e-04 | 0.1460 | 0.1460 |
| hidden_combined_true_via_hidden_return_ood_11010_true_via | combined_true_via_hidden_return | true_via | H1_sheet_via | H2_sheet_return | 0.0569 | 0.0010 | 0.3934 | 0.3364 |
| hidden_shifted_true_via_ood_09011_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 3.536e-04 | -4.699e-04 | 0.1204 | 0.1204 |
| hidden_mismatched_artifact_ood_10011_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 4.577e-04 | -4.577e-04 | 0.0886 | 0.0886 |
| hidden_shifted_true_via_ood_09012_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 4.321e-04 | -4.321e-04 | 0.1130 | 0.1131 |
| hidden_mismatched_artifact_ood_10012_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 1.081e-04 | -4.823e-04 | 0.1073 | 0.1073 |
| hidden_hidden_return_no_via_ood_08013_no_via | hidden_return_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0053 | -3.497e-04 | 0.1590 | 0.1532 |
| hidden_shifted_true_via_ood_09013_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 2.379e-04 | -2.432e-04 | 0.1160 | 0.1163 |
| hidden_mismatched_artifact_ood_10013_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H2_sheet_return | 0.0012 | -4.975e-04 | 0.2067 | 0.2051 |
| hidden_shifted_true_via_ood_09014_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 3.206e-04 | -3.206e-04 | 0.0902 | 0.0903 |
| hidden_mismatched_artifact_ood_10014_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 4.859e-04 | -4.948e-04 | 0.1963 | 0.1963 |
| hidden_combined_true_via_hidden_return_ood_11014_true_via | combined_true_via_hidden_return | true_via | H1_sheet_via | H2_sheet_return | 0.0033 | -4.932e-04 | 0.1910 | 0.1872 |
| hidden_shifted_true_via_ood_09015_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 1.636e-04 | -2.773e-04 | 0.1819 | 0.1821 |
| hidden_mismatched_artifact_ood_10015_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H2_sheet_return | 8.573e-05 | -4.952e-04 | 0.1118 | 0.1112 |
| hidden_shifted_true_via_ood_09016_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 7.013e-05 | -7.013e-05 | 0.0988 | 0.0992 |
| hidden_mismatched_artifact_ood_10016_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 3.616e-04 | -4.969e-04 | 0.1210 | 0.1210 |
| hidden_mismatched_artifact_ood_10017_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 1.015e-04 | -4.692e-04 | 0.1765 | 0.1765 |
| hidden_shifted_true_via_ood_09018_true_via | shifted_true_via | true_via | H1_sheet_via | H3_sheet_artifact | 3.870e-05 | -3.081e-05 | 0.0833 | 0.0833 |
| hidden_mismatched_artifact_ood_10018_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 3.781e-04 | -3.781e-04 | 0.1887 | 0.1887 |
| hidden_shifted_true_via_ood_09019_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 2.603e-04 | -2.603e-04 | 0.1258 | 0.1260 |
| hidden_mismatched_artifact_ood_10019_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 3.724e-04 | -3.724e-04 | 0.2353 | 0.2353 |
| hidden_shifted_true_via_ood_09020_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 2.477e-04 | -3.958e-04 | 0.2336 | 0.2337 |
| hidden_mismatched_artifact_ood_10020_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H2_sheet_return | 2.744e-05 | -4.987e-04 | 0.1174 | 0.1171 |
| hidden_combined_true_via_hidden_return_ood_11020_true_via | combined_true_via_hidden_return | true_via | H1_sheet_via | H2_sheet_return | 0.0024 | -9.589e-06 | 0.3718 | 0.3694 |
| hidden_hidden_return_no_via_ood_08021_no_via | hidden_return_no_via | no_via | H0_sheet_only | H2_sheet_return | 0.0060 | -3.790e-04 | 0.2890 | 0.2825 |
| hidden_shifted_true_via_ood_09021_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 1.937e-04 | -1.937e-04 | 0.0855 | 0.0858 |
| hidden_mismatched_artifact_ood_10021_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 4.219e-04 | -4.905e-04 | 0.1253 | 0.1254 |
| hidden_mismatched_artifact_ood_10022_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 1.609e-04 | -4.659e-04 | 0.1938 | 0.1938 |
| hidden_shifted_true_via_ood_09023_true_via | shifted_true_via | true_via | H1_sheet_via | H0_sheet_only | 3.074e-04 | -3.676e-04 | 0.0890 | 0.0891 |
| hidden_mismatched_artifact_ood_10023_bend_artifact | mismatched_artifact | bend_artifact | H3_sheet_artifact | H0_sheet_only | 2.485e-04 | -4.596e-04 | 0.2344 | 0.2345 |

Total hidden-stress misclassified cases: `56`.


### P2-next: unknown / out-of-library rejection

# Exp08 P2-next unknown / out-of-library rejection

| dataset | n | accepted | rejected | unknown rate | full acc | accepted acc | median margin | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hidden_all | 96 | 0 | 96 | 1.0000 | 0.4167 | nan | 4.485e-04 | 0.1529 |
| hidden_combined_true_via_hidden_return | 24 | 0 | 24 | 1.0000 | 0.7917 | nan | 0.0033 | 0.1513 |
| hidden_hidden_return_no_via | 24 | 0 | 24 | 1.0000 | 0.7500 | nan | 4.703e-04 | 0.1782 |
| hidden_mismatched_artifact | 24 | 0 | 24 | 1.0000 | 0.0000 | nan | 3.450e-04 | 0.1427 |
| hidden_shifted_true_via | 24 | 0 | 24 | 1.0000 | 0.1250 | nan | 2.773e-04 | 0.1157 |

Validation thresholds: min_margin=`0.000464637`, max_residual=`0.0809604`.


# Exp08 P2 unknown rejection risk-coverage diagnostic

| dataset | coverage | accepted | rejected | accepted acc | accepted risk | median confidence/residual |
| --- | --- | --- | --- | --- | --- | --- |
| clean_ood | 20% | 20 | 80 | 1.0000 | 0.0000 | 1.0844 |
| clean_ood | 40% | 40 | 60 | 0.9500 | 0.0500 | 0.5023 |
| clean_ood | 60% | 60 | 40 | 0.9500 | 0.0500 | 0.2689 |
| clean_ood | 80% | 80 | 20 | 0.9125 | 0.0875 | 0.0812 |
| clean_ood | 100% | 100 | 0 | 0.8800 | 0.1200 | 0.0433 |
| hidden_all | 20% | 19 | 77 | 0.5789 | 0.4211 | 0.0324 |
| hidden_all | 40% | 38 | 58 | 0.5000 | 0.5000 | 0.0131 |
| hidden_all | 60% | 58 | 38 | 0.5000 | 0.5000 | 0.0052 |
| hidden_all | 80% | 77 | 19 | 0.4805 | 0.5195 | 0.0034 |
| hidden_all | 100% | 96 | 0 | 0.4167 | 0.5833 | 0.0027 |
| hidden_combined_true_via_hidden_return | 20% | 5 | 19 | 0.8000 | 0.2000 | 0.0555 |
| hidden_combined_true_via_hidden_return | 40% | 10 | 14 | 0.7000 | 0.3000 | 0.0416 |
| hidden_combined_true_via_hidden_return | 60% | 14 | 10 | 0.7143 | 0.2857 | 0.0385 |
| hidden_combined_true_via_hidden_return | 80% | 19 | 5 | 0.7368 | 0.2632 | 0.0307 |
| hidden_combined_true_via_hidden_return | 100% | 24 | 0 | 0.7917 | 0.2083 | 0.0210 |
| hidden_hidden_return_no_via | 20% | 5 | 19 | 0.0000 | 1.0000 | 0.0253 |
| hidden_hidden_return_no_via | 40% | 10 | 14 | 0.4000 | 0.6000 | 0.0037 |
| hidden_hidden_return_no_via | 60% | 14 | 10 | 0.5714 | 0.4286 | 0.0031 |
| hidden_hidden_return_no_via | 80% | 19 | 5 | 0.6842 | 0.3158 | 0.0028 |
| hidden_hidden_return_no_via | 100% | 24 | 0 | 0.7500 | 0.2500 | 0.0024 |
| hidden_mismatched_artifact | 20% | 5 | 19 | 0.0000 | 1.0000 | 0.0052 |
| hidden_mismatched_artifact | 40% | 10 | 14 | 0.0000 | 1.0000 | 0.0035 |
| hidden_mismatched_artifact | 60% | 14 | 10 | 0.0000 | 1.0000 | 0.0029 |
| hidden_mismatched_artifact | 80% | 19 | 5 | 0.0000 | 1.0000 | 0.0022 |
| hidden_mismatched_artifact | 100% | 24 | 0 | 0.0000 | 1.0000 | 0.0020 |
| hidden_shifted_true_via | 20% | 5 | 19 | 0.4000 | 0.6000 | 0.0044 |
| hidden_shifted_true_via | 40% | 10 | 14 | 0.2000 | 0.8000 | 0.0035 |
| hidden_shifted_true_via | 60% | 14 | 10 | 0.1429 | 0.8571 | 0.0032 |
| hidden_shifted_true_via | 80% | 19 | 5 | 0.1579 | 0.8421 | 0.0022 |
| hidden_shifted_true_via | 100% | 24 | 0 | 0.1250 | 0.8750 | 0.0021 |

Confidence is margin divided by best residual. This is a selective-prediction diagnostic, not a new classifier.


# Exp08 P3 unknown/OOD detector ablation

| signal | clean threshold | clean false reject | hidden reject | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| margin_only | -4.869e-04 | 0.2000 | 0.6354 | 80 | 35 | 0.9000 | 0.6000 |
| residual_only | 0.1921 | 0.2000 | 0.2812 | 80 | 69 | 0.9250 | 0.4493 |
| margin_over_residual | -0.0049 | 0.2000 | 0.6771 | 80 | 31 | 0.9125 | 0.5806 |
| registration_instability | 3.394e-04 | 0.4700 | 0.3333 | 53 | 64 | 0.8868 | 0.4375 |
| prediction_disagreement | 0.0000 | 1.0000 | 1.0000 | 0 | 0 | nan | nan |
| evidence_entropy | 0.5801 | 0.2000 | 0.6354 | 80 | 35 | 0.9375 | 0.5714 |
| residual_gap_ambiguity | 3.897e+03 | 0.2000 | 0.5208 | 80 | 46 | 0.8750 | 0.5000 |
| h0_h1_score_ambiguity | -3.066e-04 | 0.2000 | 0.1458 | 80 | 82 | 0.8625 | 0.4634 |
| residual_score_disagreement | 1.0000 | 0.2100 | 0.5938 | 79 | 39 | 0.8861 | 0.5641 |
| combined_unknown_score | 1.1972 | 0.2000 | 0.6771 | 80 | 31 | 0.9375 | 0.7742 |
| combined_physical_unknown_score | 1.5819 | 0.2000 | 0.6979 | 80 | 29 | 0.9000 | 0.6552 |

Thresholds target the configured clean false-reject rate on clean OOD rows. Hidden rows are never used to select thresholds.


# Exp08 P2 unknown-safety benchmark

| signal | safety status | clean false reject | hidden reject | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| margin_only | diagnostic_only | 0.2000 | 0.6354 | 80 | 35 | 0.9000 | 0.6000 |
| residual_only | diagnostic_only | 0.2000 | 0.2812 | 80 | 69 | 0.9250 | 0.4493 |
| margin_over_residual | diagnostic_only | 0.2000 | 0.6771 | 80 | 31 | 0.9125 | 0.5806 |
| registration_instability | fails_clean_reject_budget | 0.4700 | 0.3333 | 53 | 64 | 0.8868 | 0.4375 |
| prediction_disagreement | fails_clean_reject_budget | 1.0000 | 1.0000 | 0 | 0 | nan | nan |
| evidence_entropy | diagnostic_only | 0.2000 | 0.6354 | 80 | 35 | 0.9375 | 0.5714 |
| residual_gap_ambiguity | diagnostic_only | 0.2000 | 0.5208 | 80 | 46 | 0.8750 | 0.5000 |
| h0_h1_score_ambiguity | diagnostic_only | 0.2000 | 0.1458 | 80 | 82 | 0.8625 | 0.4634 |
| residual_score_disagreement | fails_clean_reject_budget | 0.2100 | 0.5938 | 79 | 39 | 0.8861 | 0.5641 |
| combined_unknown_score | usable_screen | 0.2000 | 0.6771 | 80 | 31 | 0.9375 | 0.7742 |
| combined_physical_unknown_score | diagnostic_only | 0.2000 | 0.6979 | 80 | 29 | 0.9000 | 0.6552 |

A usable screen must stay within the clean false-reject budget while rejecting many hidden mechanisms and preserving accepted-case accuracy. This is a safety diagnostic, not a deployed refusal policy.


# Exp08 P2 accepted-hidden risk endpoint

| signal | risk status | clean false reject | hidden reject | hidden accept rate | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc | accepted hidden risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| prediction_disagreement | fails_clean_budget | 1.0000 | 1.0000 | 0.0000 | 0 | 0 | nan | nan | nan |
| combined_physical_unknown_score | rejects_many_but_accepted_hidden_risky | 0.2000 | 0.6979 | 0.3021 | 80 | 29 | 0.9000 | 0.6552 | 0.3448 |
| combined_unknown_score | rejects_many_but_accepted_hidden_risky | 0.2000 | 0.6771 | 0.3229 | 80 | 31 | 0.9375 | 0.7742 | 0.2258 |
| margin_over_residual | rejects_many_but_accepted_hidden_risky | 0.2000 | 0.6771 | 0.3229 | 80 | 31 | 0.9125 | 0.5806 | 0.4194 |
| margin_only | diagnostic_only | 0.2000 | 0.6354 | 0.3646 | 80 | 35 | 0.9000 | 0.6000 | 0.4000 |
| evidence_entropy | diagnostic_only | 0.2000 | 0.6354 | 0.3646 | 80 | 35 | 0.9375 | 0.5714 | 0.4286 |
| residual_score_disagreement | fails_clean_budget | 0.2100 | 0.5938 | 0.4062 | 79 | 39 | 0.8861 | 0.5641 | 0.4359 |
| residual_gap_ambiguity | diagnostic_only | 0.2000 | 0.5208 | 0.4792 | 80 | 46 | 0.8750 | 0.5000 | 0.5000 |
| registration_instability | fails_clean_budget | 0.4700 | 0.3333 | 0.6667 | 53 | 64 | 0.8868 | 0.4375 | 0.5625 |
| residual_only | diagnostic_only | 0.2000 | 0.2812 | 0.7188 | 80 | 69 | 0.9250 | 0.4493 | 0.5507 |
| h0_h1_score_ambiguity | diagnostic_only | 0.2000 | 0.1458 | 0.8542 | 80 | 82 | 0.8625 | 0.4634 | 0.5366 |

The primary safety question is not only how many hidden mechanisms are rejected, but how risky the hidden mechanisms are after they are accepted. Thresholds are still selected from clean rows only.


# Exp08 P2 accepted-risk objective ranking

| signal | objective status | risk objective | clean false reject | hidden accept rate | accepted hidden risk | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| combined_unknown_score | diagnostic_only | 0.5974 | 0.2000 | 0.3229 | 0.2258 | 0.9375 | 0.7742 |
| combined_physical_unknown_score | diagnostic_only | 0.7938 | 0.2000 | 0.3021 | 0.3448 | 0.9000 | 0.6552 |
| margin_over_residual | diagnostic_only | 0.9846 | 0.2000 | 0.3229 | 0.4194 | 0.9125 | 0.5806 |
| margin_only | diagnostic_only | 1.0292 | 0.2000 | 0.3646 | 0.4000 | 0.9000 | 0.6000 |
| evidence_entropy | diagnostic_only | 1.0864 | 0.2000 | 0.3646 | 0.4286 | 0.9375 | 0.5714 |
| residual_score_disagreement | fails_clean_budget | 1.2142 | 0.2100 | 0.4062 | 0.4359 | 0.8861 | 0.5641 |
| residual_gap_ambiguity | diagnostic_only | 1.4584 | 0.2000 | 0.4792 | 0.5000 | 0.8750 | 0.5000 |
| residual_only | diagnostic_only | 2.0390 | 0.2000 | 0.7188 | 0.5507 | 0.9250 | 0.4493 |
| h0_h1_score_ambiguity | diagnostic_only | 2.2816 | 0.2000 | 0.8542 | 0.5366 | 0.8625 | 0.4634 |
| registration_instability | fails_clean_budget | 2.7684 | 0.4700 | 0.6667 | 0.5625 | 0.8868 | 0.4375 |
| prediction_disagreement | fails_clean_budget | nan | 1.0000 | 0.0000 | nan | nan | nan |

Rows rank fixed clean-thresholded unknown signals by accepted-hidden risk, hidden accept rate, and clean false-reject budget. Hidden rows are not used to choose thresholds; they only evaluate the frozen signals.


# Exp08 P2 physical-evidence unknown/OOD ablation

| signal | clean threshold | clean false reject | hidden reject | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| evidence_entropy | 0.5801 | 0.2000 | 0.6354 | 80 | 35 | 0.9375 | 0.5714 |
| residual_gap_ambiguity | 3.897e+03 | 0.2000 | 0.5208 | 80 | 46 | 0.8750 | 0.5000 |
| h0_h1_score_ambiguity | -3.066e-04 | 0.2000 | 0.1458 | 80 | 82 | 0.8625 | 0.4634 |
| residual_score_disagreement | 1.0000 | 0.2100 | 0.5938 | 79 | 39 | 0.8861 | 0.5641 |
| combined_physical_unknown_score | 1.5819 | 0.2000 | 0.6979 | 80 | 29 | 0.9000 | 0.6552 |

These signals use model-evidence entropy, residual ambiguity, H0/H1 score ambiguity, and residual-vs-score disagreement. Thresholds are still clean-validation only.


### P3: synthetic two-state identification

# Exp08 synthetic two-state identification

| method | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc |
| --- | --- | --- | --- | --- | --- | --- |
| single_state | 100 | 0.8800 | 0.7200 | 0.8000 | 1.0000 | 1.0000 |
| joint_h0_disambiguation | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 |

Best synthetic design policy: `h0_disambiguation`.


# Exp08 P3-next synthetic multi-state design scan

| method | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | median joint margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| single_state | 100 | 0.8800 | 0.7200 | 0.8000 | 1.0000 | 1.0000 |  |
| joint_random_independent | 100 | 0.9200 | 0.7600 | 0.9200 | 1.0000 | 1.0000 | 0.0109 |
| joint_sheet_rescale | 100 | 0.9300 | 0.7600 | 0.9600 | 1.0000 | 1.0000 | 0.0092 |
| joint_extra_boost | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0232 |
| joint_extra_sign_flip | 100 | 0.9200 | 0.7600 | 0.9200 | 1.0000 | 1.0000 | 0.0098 |
| joint_low_noise_repeat | 100 | 0.9200 | 0.7600 | 0.9200 | 1.0000 | 1.0000 | 0.0077 |
| joint_h0_disambiguation | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0530 |
| joint_h1_h2_separation | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0153 |
| joint_max_expected_margin | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0497 |
| joint_min_expected_entropy | 100 | 0.9400 | 0.7600 | 1.0000 | 1.0000 | 1.0000 | 0.0245 |

Second excitation is synthetic and generated from the same graph; this is not active-measurement data.


# Exp08 P3 active-measurement design utility diagnostic

| policy | label-free utility | 4-way acc | H0 acc | median joint margin | median margin gain | median joint best score |
| --- | --- | --- | --- | --- | --- | --- |
| h0_disambiguation | 0.0653 | 0.9400 | 0.7600 | 0.0530 | 0.0456 | 0.1050 |
| max_expected_margin | 0.0602 | 0.9400 | 0.7600 | 0.0497 | 0.0420 | 0.1053 |
| min_expected_entropy | 0.0225 | 0.9400 | 0.7600 | 0.0245 | 0.0164 | 0.1026 |
| extra_boost | 0.0218 | 0.9400 | 0.7600 | 0.0232 | 0.0179 | 0.1037 |
| h1_h2_separation | 0.0067 | 0.9400 | 0.7600 | 0.0153 | 0.0030 | 0.1012 |
| random_independent | 0.0019 | 0.9200 | 0.7600 | 0.0109 | 0.0025 | 0.1026 |
| extra_sign_flip | 6.285e-04 | 0.9200 | 0.7600 | 0.0098 | 0.0020 | 0.1019 |
| sheet_rescale | -6.133e-05 | 0.9300 | 0.7600 | 0.0092 | 0.0012 | 0.0990 |
| low_noise_repeat | -0.0018 | 0.9200 | 0.7600 | 0.0077 | 0.0016 | 0.1022 |

Best label-free synthetic policy: `h0_disambiguation`. The utility uses margins and residual scores, not labels, but evaluation columns are reported for audit.


# Exp08 P4 active-design objective table

| policy | label-free utility | 4-way acc | H0 acc | median joint margin | median margin gain | median joint best score |
| --- | --- | --- | --- | --- | --- | --- |
| h0_disambiguation | 0.0653 | 0.9400 | 0.7600 | 0.0530 | 0.0456 | 0.1050 |
| max_expected_margin | 0.0602 | 0.9400 | 0.7600 | 0.0497 | 0.0420 | 0.1053 |
| min_expected_entropy | 0.0225 | 0.9400 | 0.7600 | 0.0245 | 0.0164 | 0.1026 |
| extra_boost | 0.0218 | 0.9400 | 0.7600 | 0.0232 | 0.0179 | 0.1037 |
| h1_h2_separation | 0.0067 | 0.9400 | 0.7600 | 0.0153 | 0.0030 | 0.1012 |
| random_independent | 0.0019 | 0.9200 | 0.7600 | 0.0109 | 0.0025 | 0.1026 |
| extra_sign_flip | 6.285e-04 | 0.9200 | 0.7600 | 0.0098 | 0.0020 | 0.1019 |
| sheet_rescale | -6.133e-05 | 0.9300 | 0.7600 | 0.0092 | 0.0012 | 0.0990 |
| low_noise_repeat | -0.0018 | 0.9200 | 0.7600 | 0.0077 | 0.0016 | 0.1022 |

The objective is a synthetic proxy for expected evidence separation. It does not include real port, voltage, heating, or return-network constraints.


# Exp08 P4 constrained active-design audit

| policy | constraint status | label-free utility | 4-way acc | H0 acc | median joint margin | median margin gain | median joint best score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| h0_disambiguation | allowed | 0.0653 | 0.9400 | 0.7600 | 0.0530 | 0.0456 | 0.1050 |
| max_expected_margin | constraint_limited | 0.0602 | 0.9400 | 0.7600 | 0.0497 | 0.0420 | 0.1053 |
| min_expected_entropy | allowed | 0.0225 | 0.9400 | 0.7600 | 0.0245 | 0.0164 | 0.1026 |
| extra_boost | constraint_limited | 0.0218 | 0.9400 | 0.7600 | 0.0232 | 0.0179 | 0.1037 |
| h1_h2_separation | allowed | 0.0067 | 0.9400 | 0.7600 | 0.0153 | 0.0030 | 0.1012 |
| random_independent | allowed | 0.0019 | 0.9200 | 0.7600 | 0.0109 | 0.0025 | 0.1026 |
| extra_sign_flip | not_allowed | 6.285e-04 | 0.9200 | 0.7600 | 0.0098 | 0.0020 | 0.1019 |
| sheet_rescale | allowed | -6.133e-05 | 0.9300 | 0.7600 | 0.0092 | 0.0012 | 0.0990 |
| low_noise_repeat | not_allowed | -0.0018 | 0.9200 | 0.7600 | 0.0077 | 0.0016 | 0.1022 |

The constraints are synthetic feasibility screens for current gain, sheet-current perturbation, and allowed excitation families. They do not represent real hardware limits yet.


### P5: synthetic registration stress curve

# Exp08 P5 synthetic registration stress curve

| stress | mode | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | no-via FP | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| identity | base | 32 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.009e-06 |
| identity | global_registered | 32 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.009e-06 |
| translation_40um | base | 32 | 0.8125 | 0.6250 | 0.6250 | 1.0000 | 1.0000 | 0.1250 | 0.1596 |
| translation_40um | global_registered | 32 | 0.7812 | 0.5000 | 0.6250 | 1.0000 | 1.0000 | 0.0417 | 0.1588 |
| translation_80um | base | 32 | 0.5938 | 0.1250 | 0.3750 | 1.0000 | 0.8750 | 0.3750 | 0.3020 |
| translation_80um | global_registered | 32 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.008e-06 |
| translation_120um | base | 32 | 0.3750 | 0.0000 | 0.0000 | 1.0000 | 0.5000 | 0.5000 | 0.4192 |
| translation_120um | global_registered | 32 | 0.8125 | 0.6250 | 0.6250 | 1.0000 | 1.0000 | 0.1250 | 0.1593 |
| rotation_1.0deg | base | 32 | 0.7812 | 0.3750 | 0.7500 | 1.0000 | 1.0000 | 0.0000 | 0.0657 |
| rotation_1.0deg | global_registered | 32 | 0.9375 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0331 |
| rotation_2.0deg | base | 32 | 0.6250 | 0.1250 | 0.5000 | 1.0000 | 0.8750 | 0.0000 | 0.1307 |
| rotation_2.0deg | global_registered | 32 | 0.9062 | 0.6250 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0333 |
| scale_0.010 | base | 32 | 0.8438 | 0.3750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0225 |
| scale_0.010 | global_registered | 32 | 0.9688 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0111 |
| scale_0.020 | base | 32 | 0.7812 | 0.2500 | 0.8750 | 1.0000 | 1.0000 | 0.0000 | 0.0447 |
| scale_0.020 | global_registered | 32 | 0.9688 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0110 |
| standoff_15um | base | 32 | 0.4062 | 0.0000 | 0.3750 | 1.0000 | 0.2500 | 0.0000 | 0.0916 |
| standoff_15um | global_registered | 32 | 0.3750 | 0.0000 | 0.3750 | 0.8750 | 0.2500 | 0.0000 | 0.0916 |
| standoff_30um | base | 32 | 0.3125 | 0.0000 | 0.0000 | 1.0000 | 0.2500 | 0.0000 | 0.1568 |
| standoff_30um | global_registered | 32 | 0.3125 | 0.0000 | 0.0000 | 1.0000 | 0.2500 | 0.0000 | 0.1554 |
| tilt_10mrad | base | 32 | 0.8438 | 0.3750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0382 |
| tilt_10mrad | global_registered | 32 | 0.8438 | 0.3750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0382 |
| tilt_20mrad | base | 32 | 0.8125 | 0.2500 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0770 |
| tilt_20mrad | global_registered | 32 | 0.8125 | 0.2500 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0770 |

The stressed observation field is generated from transformed graph geometry while the scorer sees the original graph. This is a synthetic registration sensitivity curve, not real CAD alignment.


## Scientific gates

| gate | passed |
| --- | --- |
| graph_hypothesis_accuracy_above_random_4way | True |
| graph_test_accuracy_is_high | True |
| graph_ood_accuracy_is_material | True |
| graph_ood_no_via_accuracy_is_material | True |
| graph_ood_true_via_accuracy_is_material | True |
| graph_ood_return_path_accuracy_is_material | True |
| graph_auc_not_worse_than_raw_template | True |
| graph_ood_auc_not_worse_than_residual_template | True |
| graph_no_via_fp_below_raw_template | True |
| graph_ood_no_via_fp_below_residual_template | True |
| graph_selective_accuracy_20pct_above_full_accuracy | True |
| graph_ood_selective_accuracy_20pct_above_full_accuracy | True |
| residual_baseline_reported_not_hidden | True |
| pypeec_graph_bridge_available | True |
| pypeec_centerline_bridge_accuracy_is_high | True |
| pypeec_bridge_exposes_solver_gap | True |
| pypeec_bridge_via_auc_is_material | True |
| hidden_mechanism_stress_is_evaluated | True |
| hidden_mechanism_is_nontrivial | True |
| hidden_selective_accuracy_not_worse_than_full | True |
| via_location_marginalization_is_evaluated | True |
| via_location_marginalization_improves_shifted_via | True |
| pypeec_aware_basis_bank_is_evaluated | True |
| pypeec_aware_basis_residual_not_worse_than_base | True |
| model_selection_calibration_is_evaluated | True |
| pypeec_heldout_model_selection_is_evaluated | True |
| h0_h1_tradeoff_curve_is_evaluated | True |
| pypeec_model_selection_stability_is_evaluated | True |
| pypeec_class_specific_selective_is_evaluated | True |
| pypeec_stacked_evidence_calibrator_is_evaluated | True |
| pypeec_stacked_group_heldout_is_evaluated | True |
| pypeec_stacked_group_distance_refusal_is_evaluated | True |
| pypeec_family_fewshot_adaptation_is_evaluated | True |
| stacked_evidence_feature_ablation_is_evaluated | True |
| stacked_evidence_unknown_safety_is_evaluated | True |
| stacked_evidence_distance_ood_is_evaluated | True |
| stacked_evidence_near_boundary_hidden_is_evaluated | True |
| stacked_evidence_near_hidden_severity_is_evaluated | True |
| near_hidden_accepted_cases_are_audited | True |
| stacked_evidence_space_diagnostics_are_evaluated | True |
| pypeec_stacked_external_stress_is_evaluated | True |
| stacked_evidence_selective_risk_is_evaluated | True |
| pypeec_distribution_gap_is_evaluated | True |
| disciplined_model_bank_is_documented | True |
| global_registration_search_is_evaluated | True |
| unknown_rejection_catches_hidden_mechanisms | True |
| unknown_risk_coverage_is_evaluated | True |
| unknown_detector_ablation_is_evaluated | True |
| unknown_safety_benchmark_is_evaluated | True |
| unknown_accepted_hidden_risk_is_evaluated | True |
| unknown_risk_objective_is_evaluated | True |
| unknown_physical_evidence_ablation_is_evaluated | True |
| h0_hard_negatives_are_evaluated | True |
| multistate_identification_is_evaluated | True |
| multistate_joint_not_worse_than_single | True |
| multistate_design_scan_is_evaluated | True |
| multistate_label_free_design_is_evaluated | True |
| active_design_objective_is_evaluated | True |
| active_design_constraints_are_evaluated | True |
| registration_stress_curve_is_evaluated | True |
| registration_standoff_tilt_stress_is_evaluated | True |
| all_scientific_gates_passed | True |


## Interpretation

- The graph scorer is not another pixel-threshold detector. It compares explicit physical explanations: sheet-only, sheet+via, sheet+return, and sheet+artifact.
- The raw template and sheet-residual template are intentionally kept as baselines to prevent the graph method from hiding behind polished metrics.
- The exp07 bridge intentionally tests the same graph scorer on real PyPEEC fields. Centerline bridge performance is expected to be easier; a PyPEEC drop is evidence of solver/operator mismatch, not a failed run.
- Hidden-mechanism rows deliberately put some true field components outside the hypothesis library. They are designed to expose ambiguity and selective-risk behavior, not to inflate accuracy.
- The two-state table is a synthetic active-measurement prototype. It validates the joint-scoring code path, not real multi-excitation hardware.
- Via-location marginalization is a registration-uncertainty diagnostic. It is useful only if it improves shifted/bridge behavior without hiding false-positive trade-offs.
- The PyPEEC-aware basis-bank table tests whether finite-width, return-bank, artifact-bank, distributed-via, or combined graph bases reduce solver residuals. It is not a PyPEEC-calibrated model.
- Model-evidence rows test whether complexity-aware selection can preserve identifiability when richer basis banks lower residuals.
- The model-selection calibration table ranks PyPEEC frozen trade-offs with a fixed audit objective. It is not used to alter frozen predictions.
- The allowed-basis table makes the model-bank discipline explicit: H0, H1, return, artifact, and refusal explanations should not share every nuisance basis by default.
- The held-out PyPEEC model-selection table is a pilot calibration/held-out split on the current mini distribution. It is separate from the frozen no-calibration bridge and is not broad CAD/FEM validation.
- The H0/H1 trade-off table treats no-via safety and true-via recall as primary endpoints.
- The repeated-split stability table estimates model-selection rank stability under many stratified mini-distribution splits. It is not a substitute for a larger PyPEEC distribution.
- The PyPEEC distribution table states current H0/H1/H2/H3 target coverage before any final model-selection claim is made.
- H0 hard-negative rows isolate the hardest practical diagnostic: not over-explaining no-via fields.
- Global registration search tests coarse CAD-to-field translation/rotation/scale uncertainty. It is intentionally kept separate from PyPEEC physics mismatch.
- Unknown rejection is calibrated from clean validation rows and then applied to hidden stress. It is a refusal mechanism, not a new classifier.
- Unknown risk-coverage reports whether refusal can become selective prediction rather than simply rejecting every hard case.
- Unknown-detector ablations compare margin, residual, margin/residual, registration instability, prediction disagreement, and combined unknown scores.
- The unknown-safety benchmark labels each refusal signal as a usable screen or diagnostic-only under a clean false-reject budget.
- The accepted-hidden risk table makes the safety endpoint sharper: a rejection signal is not enough if the hidden cases that remain accepted are still frequently wrong.
- The accepted-risk objective table ranks fixed refusal signals by clean-budget compliance, hidden acceptance, and accepted-hidden tail risk; hidden rows still do not choose thresholds.
- Physical-evidence unknown ablations add evidence entropy, residual-gap ambiguity, H0/H1 ambiguity, and residual-vs-score disagreement signals.
- The multi-state design scan compares synthetic excitation policies. It is an information-gain study, not a hardware protocol.
- The active-design utility table ranks policies using label-free margin/residual proxies and audits the resulting label accuracy.
- The constrained active-design table applies first-order feasibility screens to the label-free active policies.
- The registration stress curve measures how synthetic graph-to-field misregistration, standoff shift, and sensor tilt degrade identification and whether the fixed global search can recover geometric parts of the mismatch.
- A pass means the graph-identification framing is promising enough to replace further U-Net/pixel-output tuning as the next research direction. It does not mean no-via/return-path ambiguity is solved in real data.
