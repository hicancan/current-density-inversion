# exp05-realistic-noise-and-standoff-tilt

## 实验定位

本实验对应最终路线中的 **MVP-4：实验非理想增强 / QDM-like sensor nonidealities**。

它不是神经网络训练实验，而是把前面 exp01–exp04 的理想物理链路推进到更接近真实 QDM 测量的观测模型。核心目标是验证：

1. standoff 不能继续被假设为全局常数，倾斜会造成空间变化的距离场；
2. 观测磁场不能只加独立同分布白噪声，`Bx, By, Bz` 噪声应允许通道相关和空间相关；
3. QDM/相机链路会引入近似 PSF 模糊和像素级信心下降；
4. 四 NV 轴投影在理想标定下可恢复 `Bxyz`，但单轴观测秩亏、轴增益失配会引入可量化误差；
5. via 检测不能裸用 Laplacian/高通，需要尺度匹配的 band-pass / DoG / matched filter；
6. 在非理想观测下，via 检测应优先基于 sheet-background residual，而不是直接从 total field 硬捞。

## 本实验回答的问题

> 在两层 + via toy geometry 上，加入 PSF、相关噪声、pixel confidence 和 standoff tilt 后，via 检测和前向模型会受到多大影响？哪些非理想因素必须进入后续 exp06/真实 QDM 数据闭环？

## 主要输出

运行：

```bash
python src/run_all.py
python -m unittest discover -s tests
```

生成：

- `outputs/01_sensor_model_pipeline.png`
- `outputs/02_noise_covariance.png`
- `outputs/03_tilt_effect.png`
- `outputs/04_via_detection.png`
- `outputs/05_bandpass_and_standoff.png`
- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `data/exp05_sensor_nonidealities.npz`

## 成功标准

- 相关噪声的经验相关矩阵接近配置目标；
- PSF 模糊降低高频能量；
- standoff tilt 造成非零且可量化的 forward mismatch；
- residual matched filter 的 via 定位明显优于/不劣于 raw total field；
- DoG / band-pass 能压制低频背景且不过度放大像素级噪声。
- 四轴 NV projection rank 为 3，单轴 rank deficient，轴增益失配会产生可测误差。

`metrics.json` 中包含 `acceptance_gates`，用于硬性检查相关噪声、PSF 高频压制、
tilt forward mismatch、residual via detection、hard-case 定位和 NV projection 风险是否达标。

## 边界说明

本实验仍然不是完整 QDM 模型。它尚未包含：

- 四 NV 轴 ODMR 谱线级拟合；
- 离轴猝灭的真实 Hamiltonian 模型；
- 温度/应力/微波场联合漂移；
- COMSOL / Ansys / FastHenry 异源正演器；
- 真实 FPC/QDM 数据。

这些属于后续实验与真实数据闭环阶段。
