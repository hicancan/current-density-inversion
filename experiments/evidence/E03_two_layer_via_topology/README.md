# exp03-two-layer-via-toy-benchmark

## 实验定位

本实验对应最终研究路线中的 **MVP-2：两层 + via toy benchmark**。

它不是神经网络实验，也不是完整真实 QDM 实验；它的目标是在进入 topology loss 网络之前，先把最小多层问题跑通：

\[
B_{total}=F_1(J_1)+F_2(J_2)+G(s_1)
\]

并验证最核心的 2.5D 拓扑守恒关系：

\[
\nabla_{xy}\cdot J_1=-s_1,\qquad
\nabla_{xy}\cdot J_2=+s_1
\]

更一般地，后续多层形式为：

\[
\nabla_{xy}\cdot J_l=s_{l-1}-s_l
\]

## 本实验回答的问题

1. 两层面电流与一个竖直 via 的 Biot-Savart 线性叠加是否正确？
2. 理想竖直 via 是否主要产生面内环绕磁场，且 \(B_z\) 接近 0？
3. 在已知 sheet 背景扣除后，via 模板匹配能否定位 via？
4. 在不扣除 sheet 背景时，via 信号是否容易被强背景淹没？
5. 离散有限体积形式下，内部 via 位置的 topology residual 是否为 0？
6. 两层深度接近时，层间磁场模板是否高度相似，从而提示 layer mixing 风险？
7. 当前 centerline synthetic benchmark 和 finite-width/return-current surrogate
   之间是否存在可量化 forward gap？

## 目录结构

```text
exp03-two-layer-via-toy-benchmark/
  configs/default.json
  src/
    forward/segments.py
    geometry/toy_circuit.py
    detection/matched_filter.py
    experiments/run_all.py
    experiments/plotting.py
  tests/test_exp03.py
  outputs/
  data/
  docs/NOTES.md
  requirements.txt
  README.md
```

## 快速运行

```bash
pip install -r requirements.txt
python src/experiments/run_all.py --config configs/default.json
pytest -q
```

运行后会生成：

```text
outputs/01_two_layer_geometry.png
outputs/02_field_decomposition_Bxyz.png
outputs/03_via_template_matched_filter.png
outputs/04_topology_constraint_residual.png
outputs/05_layer_mixing_and_snr.png
outputs/06_toy_dataset_samples.png
outputs/07_background_swamping_stress.png
outputs/08_benchmark_dataset_examples.png
outputs/metrics.json
outputs/RUN_REPORT.md
data/two_layer_via_example.npz
data/toy_dataset_small.npz
data/two_layer_via_benchmark.npz
```

## 验收标准

本实验完成后，至少应满足：

- superposition relative L2 error 接近 0；
- via 的 \(B_z / B_{xy}\) 比值接近 0；
- oracle residual via matched filter 能在 1-2 个像素内定位 via；
- raw matched filter 明显劣于 residual matched filter，用于提示背景淹没风险；
- topology residual 在内部 via 位置接近 0；
- 层间模板相似度随层间距减小而升高，提示多层解混叠的病态性。

`outputs/metrics.json` 还包含 `acceptance_gates`。当前版本新增了
`background_swamping_stress` 难例：在强 sheet 背景下直接从 total field
做 via 模板匹配应被误导，而 oracle residual 模板匹配应在 2 个像素内定位 via。

当前版本还生成正式 benchmark 数据包 `data/two_layer_via_benchmark.npz`：

- `B_clean` / `B_obs`：clean 与 noisy 的 `Bxyz`；
- `truth`：`J1x,J1y,J2x,J2y,s1` 五通道标签；
- `split`：`train/val/test/ood`；
- `metadata_json`：每个样本的 via、端口、电流和场景元数据。

ID split 中包含 `straight`、`l1_jog`、`l2_jog`、`both_jog`、
`multi_via`、`no_via` 六类路由，避免正式 test set 的 `J_y` 通道全为
0，并开始覆盖多 via / 无 via 情况；OOD split 使用
`both_jog_background`、`dense_via_background`、`no_via_background`
场景，并保留更强背景与更高噪声。`metrics.json` 会报告
`truth_channel_l2_norms_by_split` 与 `route_kind_counts`，并用 gate
检查方向多样性。当前版本还报告 `recoverability_summary` 和
`forward_realism_probe`，分别用于记录 split 健康状态和有限线宽/弱回流
surrogate 相对中心线算子的 forward gap。

这些 truth maps 是 raster label maps，用于后续模型 benchmark；有限体积拓扑守恒仍由本实验的独立 topology gate 验证。

## 注意边界

本实验仍然是理想 toy benchmark，尚未包含：

- 有限线宽/厚度和 ground/power plane 回流目前只是 surrogate probe，
  不是 benchmark truth 或 FEM 结论；
- QDM PSF 与 NV 投影噪声；
- standoff tilt；
- CAD soft mask；
- FEM/COMSOL 异源验证；
- 神经网络训练。

这些属于后续实验。
