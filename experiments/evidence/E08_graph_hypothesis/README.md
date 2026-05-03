# exp08-graph-system-identification

Exp08 是从 `pixel-map inverse` 进入 `graph/CAD-like magnetic system
identification` 的第一版交付实验。这里的 graph 是合成的
route/candidate graph，不是真实 CAD/Gerber 导入。

它不再把任务定义为：

```text
Bxyz image -> J1x/J1y/J2x/J2y/s1 pixel map
```

而是定义为：

```text
Bxyz magnetic image + route graph + via candidates + return/artifact hypotheses
-> H0/H1/H2/H3 physical explanation scoring
```

## 研究问题

现有 exp04/exp07 已经暴露：no-via false positive、return-path 失败和 operator mismatch 不是继续调 U-Net/threshold 就能根治的问题。Exp08 的目标是验证：显式图结构与物理假设评分是否比 raw/pixel-style via template 更接近下一阶段最优路线。

## 假设空间

- `H0_sheet_only`: 只有层内 sheet/trace currents。
- `H1_sheet_via`: 层内 trace + true via/source。
- `H2_sheet_return`: 层内 trace + return path。
- `H3_sheet_artifact`: 层内 trace + bend/corner/finite-width artifact。

每个 hypothesis 都通过同一套 graph-level Biot-Savart forward matrix 拟合 `Bxyz`，并使用 residual、复杂度惩罚和 extra-basis L1 惩罚组成 evidence score。

## 与 exp1-7 的关系

- exp01：验证正演基本物理。
- exp02：说明多层单平面反演存在可观测性边界。
- exp03：给出两层/via benchmark 思路。
- exp04：证明 topology-aware pixel inverse 是强 baseline，但 no-via/return-path 未解决。
- exp05：传感器非理想 proxy。
- exp06：防止 inverse crime。
- exp07：PyPEEC 外部求解器压力测试。
- exp08：把任务从 pixel-map reconstruction 升级为 graph-level hypothesis testing。

## 目录

```text
configs/default.json          默认 smoke-scale 配置
src/graph_id/                 自包含 graph identification package
src/run_all.py                一键生成数据、调参、评估、写报告
tests/                        单元测试
data/                         运行后生成 npz/jsonl 数据
outputs/                      运行后生成 metrics/report/tables/figures
```

## 一键运行

```bash
cd experiments/evidence/E08_graph_hypothesis
uv run --with-requirements requirements.txt python src/run_all.py
```

运行后会生成：

```text
data/exp08_graph_id_dataset.npz
data/exp08_cases.jsonl
outputs/metrics.json
outputs/RUN_REPORT.md
outputs/HYPOTHESIS_IDENTIFICATION_TABLE.md
outputs/HYPOTHESIS_PER_CLASS_TABLE.md
outputs/VIA_HYPOTHESIS_TEST_TABLE.md
outputs/SELECTIVE_RISK_TABLE.md
outputs/FAILURE_CASES_TABLE.md
outputs/PYPEEC_GRAPH_BRIDGE_TABLE.md
outputs/HIDDEN_MECHANISM_STRESS_TABLE.md
outputs/MULTISTATE_IDENTIFICATION_TABLE.md
outputs/PYPEEC_BRIDGE_REGISTRATION_TABLE.md
outputs/PYPEEC_AWARE_BASIS_TABLE.md
outputs/MODEL_EVIDENCE_SELECTION_TABLE.md
outputs/PYPEEC_MODEL_BANK_EVIDENCE_TABLE.md
outputs/MODEL_SELECTION_CALIBRATION_TABLE.md
outputs/PYPEEC_MODEL_BANK_ALLOWED_BASIS_TABLE.md
outputs/PYPEEC_HELDOUT_SPLIT_TABLE.md
outputs/PYPEEC_HELDOUT_MODEL_SELECTION_TABLE.md
outputs/H0_H1_MODEL_SELECTION_TRADEOFF_TABLE.md
outputs/PYPEEC_MODEL_SELECTION_STABILITY_TABLE.md
outputs/PYPEEC_CLASS_SPECIFIC_SELECTIVE_TABLE.md
outputs/PYPEEC_STACKED_EVIDENCE_CALIBRATOR_TABLE.md
outputs/PYPEEC_STACKED_EVIDENCE_GROUP_HELDOUT_TABLE.md
outputs/STACKED_EVIDENCE_FEATURE_ABLATION_TABLE.md
outputs/STACKED_EVIDENCE_UNKNOWN_SAFETY_TABLE.md
outputs/PYPEEC_STACKED_EVIDENCE_EXTERNAL_STRESS_TABLE.md
outputs/STACKED_EVIDENCE_SELECTIVE_RISK_TABLE.md
outputs/PYPEEC_DISTRIBUTION_GAP_TABLE.md
outputs/H0_HARD_NEGATIVE_TABLE.md
outputs/PYPEEC_BRIDGE_GLOBAL_REGISTRATION_TABLE.md
outputs/REGISTRATION_MARGINALIZATION_TABLE.md
outputs/UNKNOWN_REJECTION_TABLE.md
outputs/UNKNOWN_RISK_COVERAGE_TABLE.md
outputs/UNKNOWN_DETECTOR_ABLATION_TABLE.md
outputs/UNKNOWN_SAFETY_BENCHMARK.md
outputs/UNKNOWN_ACCEPTED_HIDDEN_RISK_TABLE.md
outputs/UNKNOWN_PHYSICAL_EVIDENCE_ABLATION_TABLE.md
outputs/MULTISTATE_DESIGN_TABLE.md
outputs/MULTISTATE_EXPERIMENTAL_DESIGN_TABLE.md
outputs/ACTIVE_DESIGN_OBJECTIVE_TABLE.md
outputs/ACTIVE_DESIGN_CONSTRAINT_TABLE.md
outputs/REGISTRATION_STRESS_CURVE.md
outputs/*.png
```

## 关键指标

- `4-way hypothesis accuracy`
- `H1/H0 via AUC`
- `no-via false positive rate`
- `true-via recall/F1`
- `selective-risk accuracy`
- `median best forward residual`
- per-class H0/H1/H2/H3 OOD accuracy
- graph-vs-raw/residual via evidence comparison
- exp07 centerline-versus-PyPEEC graph bridge
- hidden-mechanism OOD stress
- synthetic two-state joint scoring
- via-location marginalization / registration sensitivity
- unknown / out-of-library rejection
- multi-state design scan
- PyPEEC-aware basis-bank residual/classification trade-off
- model-evidence / model-selection scoring
- held-out PyPEEC model-selection pilot
- H0/H1 endpoint trade-off curve
- repeated-split PyPEEC model-selection stability
- PyPEEC distribution target coverage
- H0/no-via hard negatives
- global graph-to-field registration search
- unknown risk-coverage
- unknown detector ablation
- unknown safety benchmark under a clean false-reject budget
- accepted-hidden risk after unknown/refusal screening
- physical-evidence unknown/OOD ablation
- label-free active-measurement design utility
- constrained active-measurement design utility
- synthetic registration/standoff/tilt stress curve

## 科学 gate

Exp08 明确区分 engineering gate 和 scientific gate。核心科学 gate 包括：

1. graph hypothesis accuracy 高于 4-way random baseline。
2. graph H1/H0 AUC 不弱于 raw via template。
3. graph no-via FP 不高于 raw via template。
4. selective 20% coverage accuracy 不低于 full coverage accuracy。
5. residual baseline 被显式报告，不能隐藏失败模式。
6. OOD no-via、true-via 和 return-path per-class accuracy 不能崩。
7. graph H1/H0 在 OOD 上不能弱于 sheet-residual template。
8. exp07 centerline graph bridge 必须自洽，而 PyPEEC bridge 必须暴露真实 solver gap。
9. hidden-mechanism stress 必须非平凡，不能又变成同源满分任务。
10. synthetic two-state joint scoring 不能比 single-state 更差。
11. via-location marginalization 必须显式报告收益和代价。
12. unknown rejection 必须能识别 hidden/out-of-library stress。
13. multi-state 设计必须扫描多个 second-excitation policy，而不是只报一个点。
14. PyPEEC-aware basis bank 必须显式报告 residual/classification trade-off。
15. model evidence 必须显式比较 residual-only 与复杂度惩罚后的假设选择。
16. H0/no-via hard negative 必须单独报告，不允许被 overall acc 掩盖。
17. global registration 必须独立于 via-local marginalization 报告。
18. unknown rejection 必须升级为 risk-coverage 和 detector ablation，不能只报一个拒判率。
19. multi-state 设计必须报告 label-free margin/residual utility 和 active-design objective。
20. registration stress curve 必须报告 translation/rotation/scale/standoff/tilt
    误配准下的退化。
21. model-selection calibration 必须把 H0 保护、true-via recall、return
    识别、误解释率和参数复杂度同时列出，不能只看 residual。
22. disciplined model bank 必须写清哪些 basis 可以服务于 H0/H1/H2/H3，
    哪些只能作为 nuisance 或 refusal 证据。
23. unknown safety 必须区分 usable screen、diagnostic-only 和违反 clean
    false-reject budget 的信号。
24. active design 必须经过合成 feasibility constraints，而不是只按
    label-free utility 排名。
25. PyPEEC held-out pilot 必须把 calibration-selected ranking 与 held-out
    metrics 分开报告，不能把同一批 PyPEEC rows 同时当选择和证明。
26. H0/H1 trade-off 必须把 no-via safety 和 true-via recall 作为主端点。
27. unknown/OOD 必须加入更物理的 evidence signals，而不只依赖 margin 或
    residual。
28. PyPEEC model-selection 不能只报一次 split；必须报告 repeated split
    stability 和 ranking 方差。
29. PyPEEC distribution 的 H0/H1/H2/H3 样本量目标必须显式列出；当前
    mini distribution 即使达到每类 100，也不能包装成最终 CAD/QDM
    distribution。
30. unknown safety 必须报告 accepted-hidden risk；只看 hidden reject rate
    不够。

## 重要限制

Exp08 是 synthetic graph-identification prototype，不是：

- 真实 QDM 验证；
- 真实 CAD/Gerber/GDS 验证；
- 完整 PyPEEC distribution validation；
- no-via/return-path 问题最终解决方案。

它的作用是建立下一阶段的范式与代码接口：graph labels、candidate hypotheses、H0/H1/H2/H3 scoring、uncertainty/refusal。

## 当前代表性结果

默认配置下，`outputs/RUN_REPORT.md` 报告：

- test 4-way hypothesis accuracy: `1.000`
- OOD 4-way hypothesis accuracy: `0.880`
- OOD graph H1/H0 via AUC: `0.969`
- OOD graph H1/H0 via F1: `0.889`
- OOD graph H1/H0 no-via FP: `0.000`
- OOD per-class accuracy: H0 `0.720`, H1 `0.800`, H2 `1.000`,
  H3 `1.000`
- exp07 centerline bridge 4-way accuracy: `1.000`
- exp07 PyPEEC bridge 4-way accuracy: `0.695`
- exp07 PyPEEC bridge H1/H0 via AUC: `0.940`
- hidden-mechanism stress 4-way accuracy: `0.417`
- hidden shifted-via accuracy after via-location marginalization: `1.000`
- hidden unknown rejection rate: `1.000`
- best synthetic two-state OOD accuracy: `0.940` versus single-state `0.880`

这些结果说明 graph/hypothesis framing 在 synthetic graph setting 下显著
优于 raw via template，也略优于 sheet-residual template。但这仍是合成
graph prototype；真实 CAD/PyPEEC/QDM 需要后续实验。

P0/P1 的结果也说明这个范式还没有“解决真实问题”：PyPEEC fields 让
4-way accuracy 从 centerline bridge 的 `1.000` 降到 `0.695`，hidden
mechanisms 也会明显击穿同源假设库。它的价值在于把这些失败暴露为可审计的
system-identification 问题，而不是继续掩盖在 pixel threshold 后处理里。

P0-next/P1-next 的结果进一步说明：via-location marginalization 可以修复
candidate registration 偏移型失败，例如 shifted-via 从 `0.125` 提高到
`1.000`；但它没有解决 PyPEEC bridge，`B_pypeec` 的 via AUC 反而从 `0.940`
降到 `0.573`，说明 PyPEEC gap 不是单纯 via 坐标偏移。P2-next 的 unknown
rejection 会把 hidden stress 全部拒判为 out-of-library，这是诚实但保守的
行为。P3-next 的 design scan 显示 `extra_boost` policy 当前最好，synthetic
OOD 4-way accuracy 为 `0.940`。

P0/P1 的下一轮结果把两个关键边界进一步拆开：`finite_width_sheet`
basis 让 PyPEEC bridge 4-way accuracy 从 `0.695` 提高到 `0.810`，combined
PyPEEC-aware basis 把 median residual 从 `0.135` 降到 `0.074`，但 combined
mode 的 4-way accuracy 只有 `0.476`。这说明更丰富的 basis 可以解释磁场，
但也可能破坏假设可辨识性。global registration search 只把 PyPEEC accuracy
从 `0.695` 提到 `0.724`、median residual 从 `0.135` 降到 `0.132`，所以
PyPEEC gap 仍主要是 physics/operator/basis mismatch，不是全局坐标误差。
P2 的 risk-coverage 表显示 clean OOD 在 20% coverage 上 accuracy 为 `1.000`，
但 hidden stress 在 20% coverage 只有 `0.579`，mismatched artifact 仍为
`0.000`，说明 refusal 需要成为 selective-prediction 问题。P3 的
label-free utility 仍选择 `extra_boost`，与最高 4-way accuracy 一致。

P0-P5 的进一步推进把 exp08 推成 model-selection benchmark。model evidence
表显示 residual-only 在 centerline/PyPEEC 上会过度选择 extra hypotheses，而
`finite_width_sheet + extra_count` 在 PyPEEC 上达到约 `0.829` 4-way accuracy，
同时 H0 acc 达到约 `0.783`；`finite_width_sheet + h0_conservative` 可把
PyPEEC no-via H0 acc 提到 `1.000`，但 H1 acc 降到约 `0.694`，说明 H0 保护
和 true-via recall 存在真实 trade-off。H0 hard-negative 表把 PyPEEC no-via
从 overall bridge 中单独剥离出来：base/default H0 acc 只有 `0.087`，而
finite-width/h0-conservative 可到 `1.000`，但这不能被包装成最终 detector。
unknown detector ablation 显示 combined unknown score 在固定 clean false reject
`0.20` 时 hidden reject 约 `0.677`，accepted hidden acc 约 `0.774`。active
design objective 选择 `h0_disambiguation`，比原来的 `extra_boost` 有更高
label-free utility，但所有 active rows 仍是 synthetic。registration stress
curve 显示 80 µm 平移会把 base accuracy 降到 `0.594`，global search 可恢复到
`1.000`；120 µm 超出搜索半径后仍只恢复到 `0.812`，说明真实配准必须显式建模。

最新 P0-P5 结果进一步把这些 trade-off 固化为正式 artifacts：
`MODEL_SELECTION_CALIBRATION_TABLE.md` 的固定 audit objective 排名第一的是
`finite_width_sheet + h0_conservative`，objective `0.6663`，H0 acc `1.000`，
H1 acc `0.6935`；排名第二的是 `finite_width_sheet + extra_count`，objective
`0.6025`，4-way acc `0.8286`，H0 acc `0.7826`，H1 acc `0.7903`。这说明当前
最强结果不是“一个模型全赢”，而是正式暴露了 no-via safety 和 true-via recall
之间的 Pareto trade-off。`UNKNOWN_SAFETY_BENCHMARK.md` 显示只有
`combined_unknown_score` 达到 `usable_screen`：clean false reject `0.200`，
hidden reject `0.677`，accepted hidden acc `0.774`。`ACTIVE_DESIGN_CONSTRAINT_TABLE.md`
显示 `h0_disambiguation` 在约束后仍是 allowed 且 utility 最高，4-way acc
`0.940`；`max_expected_margin` 和 `extra_boost` 被标为 constraint-limited。
`REGISTRATION_STRESS_CURVE.md` 已扩展到 standoff/tilt：15 µm standoff 让 base
accuracy 降到 `0.406`，30 µm standoff 降到 `0.312`，而 global registration
无法恢复；10/20 mrad tilt 相对较轻，accuracy 分别约 `0.844`/`0.812`。这说明
standoff/tilt 是传感器几何 nuisance，不应被误认为普通 xy registration。

推进6/8 把 model-selection 从 audit 又推进到一个合法的 PyPEEC held-out pilot。
当前 `PYPEEC_HELDOUT_SPLIT_TABLE.md` 将 400 个 PyPEEC mini cases 按真值假设
分成 calibration/held-out，并且每个 H0/H1/H2/H3 hypothesis 都有 100 个
unique bridge cases。`PYPEEC_HELDOUT_MODEL_SELECTION_TABLE.md` 用 calibration
objective 排名、held-out 只评估；这说明当前 mini split 已经比上一轮 pilot
稳得多，但仍不能把 held-out pilot 包装成最终可泛化规则。`H0_H1_MODEL_SELECTION_TRADEOFF_TABLE.md`
明确把 held-out H0 acc、H1 acc 和 H0 false H1/H2/H3 并列为主端点。
`UNKNOWN_PHYSICAL_EVIDENCE_ABLATION_TABLE.md`
显示 physical-evidence signals 有价值但仍不够部署：`combined_physical_unknown_score`
在 clean false reject `0.200` 下 hidden reject `0.698`，accepted hidden acc
约 `0.655`，比 combined unknown score 更会拒绝 hidden，但 accepted hidden
风险仍偏高。

推进7/8 把 held-out pilot 进一步升级为 repeated-split stability audit，并补齐
PyPEEC target distribution。当前
`PYPEEC_MODEL_SELECTION_STABILITY_TABLE.md` 显示 `finite_width_sheet +
h0_conservative` 在 31 次 stratified split 中被 calibration objective 选为
top-1 的频率为 `1.000`，heldout objective mean `0.783 ± 0.019`，heldout
H0 mean `0.965`，H1 mean `0.677`；`finite_width_sheet + extra_count` 不再
成为 top-1，但 heldout H1 mean 更高 `0.765`，H0 mean `0.782`。这说明 H0
safety 与 true-via recall 的 trade-off 是稳定存在的，不是单次 split 偶然。
`PYPEEC_DISTRIBUTION_GAP_TABLE.md` 同时明确当前 PyPEEC bridge 已经达到 H0/H1/H2/H3
各 `100/100`，包括 explicit `bend_artifact` H3 rows；这解决了上一轮 H3 缺失
的硬缺口，但仍不是最终 CAD/FEM/QDM 分布。`UNKNOWN_ACCEPTED_HIDDEN_RISK_TABLE.md`
把 unknown safety 的主端点改成 accepted-hidden risk：`combined_unknown_score`
的 hidden accept rate `0.323`、accepted hidden risk `0.226`，而
`combined_physical_unknown_score` hidden accept rate `0.302` 但 accepted hidden
risk `0.345`。因此当前更好的结论不是“unknown 已解决”，而是拒判信号存在
不同的 hidden-accept/risk trade-off，仍需要真实或更高保真 held-out 验证。

本轮进一步把核心瓶颈明确成可复现实验对象：`PYPEEC_CLASS_SPECIFIC_SELECTIVE_TABLE.md`
不再问“哪个单点 gate 数字最好看”，而是问 class-specific margin refusal 在
repeated PyPEEC calibration/held-out split 下是否能形成可信输出区域。该表单独报告
coverage、accepted accuracy、H0 false-any、H0 accepted-correct、H1
accepted-correct 和 H1 acceptance。这个结果的解释重点不是宣布 detector 已解决，而是
区分两件事：H0/no-via safety 是否可以通过拒判变安全，以及 H1/true-via recall 是否仍然
是当前单场、无 CAD 条件下的硬瓶颈。

最新的 breakthrough audit 是 `PYPEEC_STACKED_EVIDENCE_CALIBRATOR_TABLE.md`。它不再
手写一个 basis/evidence 规则，而是把所有 frozen basis/evidence scores 作为特征，
在 PyPEEC calibration folds 上训练一个简单 ridge evidence-fusion calibrator，再只在
held-out folds 上评估。这个结果属于明确的 PyPEEC calibration/held-out experiment，不是
原先 frozen no-calibration claim；它用来回答一个更本质的问题：现有 evidence bank 是否
已经包含足够区分 H0/H1/H2/H3 的信息，只是规则融合太粗。

P0-P4 将该突破继续审计到底：`PYPEEC_STACKED_EVIDENCE_GROUP_HELDOUT_TABLE.md`
显示 variant-mod group heldout 仍较强，但 pure family leaveout 会暴露 family-specific
generalization failure；`STACKED_EVIDENCE_FEATURE_ABLATION_TABLE.md` 证明
`h0_conservative_all_basis`、`all_features` 和 finite-width evidence 是主要贡献；
`STACKED_EVIDENCE_UNKNOWN_SAFETY_TABLE.md` 显示 confidence gating 在 clean heldout
上很准，但 hidden accepted risk 仍高。最新 unknown-safety audit 进一步加入
feature-distance OOD signal：它不看分类器 margin，而是判断 stacked-evidence vector
是否偏离 calibration folds 中 H0/H1/H2/H3 的 in-library manifold；在当前 hidden
stress 上，feature-distance row 在约 `0.180` clean reject 下达到 `1.000` hidden
reject 和约 `0.998` accepted-clean accuracy。这是一个实质 hidden-safety mitigation
突破。随后 `STACKED_EVIDENCE_NEAR_BOUNDARY_HIDDEN_TABLE.md` 将 hidden stress 变得更
靠近已知 return/via/artifact 候选，feature-distance 仍拒绝约 `0.851` near-hidden
rows，接受的 near-hidden primary labels 没有错误；`PYPEEC_STACKED_EVIDENCE_GROUP_DISTANCE_REFUSAL_TABLE.md`
显示 pure family leaveout 的 raw accuracy 仍低，但 distance layer 会把多数 out-of-family
evidence 转为拒判。`STACKED_EVIDENCE_SPACE_DIAGNOSTICS_TABLE.md` 和
`stacked_evidence_space_pca.png` 进一步显示 near-hidden median feature distance
约 `0.668`，介于 in-library PyPEEC 的 `0.193` 和 base hidden 的 `1.405` 之间。
`PYPEEC_FAMILY_FEWSHOT_ADAPTATION_TABLE.md` 则把 family-heldout 从“安全拒判”
推进到“少量校准可适应”：0-shot aggregate raw accuracy 约 `0.324`，5-shot
升到 `0.938`，10-shot 升到 `0.983`，accepted risk 约 `0.000`-`0.003`。
`STACKED_EVIDENCE_NEAR_HIDDEN_SEVERITY_TABLE.md` 将 near-hidden 变成强度曲线：
feature-distance hidden reject 从 severity `0.25` 的 `0.999` 下降到 severity
`1.50` 的 `0.817`，但 accepted primary-label risk 仍为 `0.000`。这些是
safety/refusal/adaptation 层的突破，不是 CAD/FEM/QDM/真实 unknown 安全证明；
`PYPEEC_STACKED_EVIDENCE_EXTERNAL_STRESS_TABLE.md`
显示 B_finite/B_centerline operator transfer 很强，但 hidden mechanism 仍差；
`STACKED_EVIDENCE_SELECTIVE_RISK_TABLE.md` 保留 risk-coverage 输出，避免把强 calibrator
包装成无拒判的部署 detector。

