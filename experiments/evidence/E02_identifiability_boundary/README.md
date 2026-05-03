# exp02-observability-and-bxy-vs-bz

## 目标

本实验对应最终技术路线中的 **MVP-1：可观测性计算器 + 单层 Fourier 反演复现**。
它承接 exp01 的正演 sanity check，回答三个问题：

1. standoff `z` 如何通过 `exp(-kz)` 压制不同空间尺度的信息？
2. 在理想二维面电流模型下，`Bxy = (Bx, By)` 和 `Bz` 反演分别能恢复什么？
3. 有限视场、噪声和 standoff 会如何影响反演误差？

本实验不是神经网络实验，也不是多层拓扑反演实验。

## 实现内容

- 二维薄片电流的 Fourier-domain Biot-Savart 正演；
- `Bxy -> Jx,Jy` 的理想反演；
- `Bz -> Jx,Jy` 的无散电流反演；
- standoff-feature-size 可观测性曲线；
- 反演高频放大曲线；
- 干净全视场反演 sanity check；
- 有限 FOV 截断对 `Bxy` 和 `Bz` 的影响比较；
- 噪声 + standoff 误差扫描；
- pytest 单元测试。

## 快速运行

```bash
pip install -r requirements.txt
python src/experiments/run_all.py
pytest -q
```

## 输出文件

运行后会在 `outputs/` 下生成：

- `01_standoff_feature_attenuation.png`
- `02_observability_heatmap.png`
- `03_inverse_amplification.png`
- `04_forward_Bxyz_from_sheet_current.png`
- `05_full_field_reconstruction_clean.png`
- `06_finite_fov_truncation_bxy_vs_bz.png`
- `07_finite_fov_error_maps.png`
- `08_noise_standoff_error_scan.png`
- `09_two_layer_single_plane_rank_deficiency.png`
- `metrics.json`
- `RUN_REPORT.md`

数据样例保存到 `data/`。

## 阶段验收标准

本实验完成后，应该能证明：

1. 正演和理想 Fourier 逆在无噪、全视场情况下自洽；
2. standoff 会以指数形式压制高频信息；
3. 反演高频会放大噪声；
4. `Bz` 反演存在 `k=0/DC` 与有限视场问题；
5. 后续不能直接训练网络，必须先知道哪些尺度/频率可观测。

当前版本还显式加入了 two-layer single-plane rank gate：单一测量平面上的
`Bxyz` 可以提高模态 SNR，但对于同一 Fourier 模式的两层标签仍是秩亏的；
这条 gate 用来防止把多层问题误判成简单的多通道可逆问题。

## 当前限制

- 使用自由空间薄片电流模型；
- 没有回流/地平面；
- 没有 QDM 传感器链路；
- 没有 NV 四轴投影噪声；
- 没有 topology loss；
- 没有多层/via 反演。

这些限制是有意保留的，因为本实验只负责路线中的第二块地基：可观测性与单层反演理论。
