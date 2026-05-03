# exp06-anti-inverse-crime-multifidelity-validation

## 实验定位

本实验对应最终路线中的：

> **MVP-5 / 多保真验证与反演犯罪闸门（anti-inverse-crime gate）**

前几个实验已经完成了：

- exp01：自由空间有限线段 Biot-Savart 正演 sanity check；
- exp02：可观测性与 `Bxy` vs `Bz`；
- exp03：两层 + via toy benchmark；
- exp04：topology soft loss network；
- exp05：真实噪声、PSF、standoff tilt 等实验非理想增强。

exp06 的目标不是追求更复杂的神经网络，而是验证一个逆问题中非常关键的风险：

> 如果训练、验证、测试全部由同一个解析正演器生成，模型可能只是在“自洽的数学世界”里表现很好；一旦真实物理正演器不同，性能可能明显下降。

这就是逆问题中的 **反演犯罪（inverse crime）**。

## 核心问题

本实验回答：

1. 同一个低保真解析正演器生成的数据上，物理解码器是否几乎完美？
2. 换成一个 intermediate “中保真代理正演器”后，误差是否开始上升？
3. 换成一个不同的“高保真代理正演器”后，误差是否明显上升？
4. 用少量高保真校准样本做 domain adaptation，能否缩小这种 gap？
5. 因此，后续真实实验前是否必须引入异源正演器 / FEM / QDM 数据做 stress test？

## 三类正演器

### 1. Low-fidelity operator

低保真正演器是理想自由空间线段 Biot-Savart：

- 两层中心线走线；
- 一个竖直 via；
- 不考虑有限线宽；
- 不考虑地平面回流；
- 不考虑 PSF；
- 不加噪声。

它代表网络/物理 loss 内嵌的快速解析算子。

### 2. Medium-fidelity surrogate operator

中保真代理只加入有限线宽、轻微层深偏移和弱 PSF，不加入地平面回流。
它用于形成 low → medium → high 的多保真阶梯，而不是只做二元对比。

### 3. High-fidelity surrogate operator

高保真代理正演器不是 COMSOL，但故意引入低保真算子没有建模的真实因素：

- 有限线宽：每根线由多个平行细丝近似；
- 地平面回流：加入反向回流电流的简化 image/return current；
- 层深偏移：模拟制造或建模误差；
- via 半径/簇：用多个竖直细丝近似有限半径 via；
- QDM-like PSF：对磁场图做空间模糊；
- 噪声：加入 μT 级观测噪声。

它不是最终真实物理，但足以作为“异源算子 stress test”。

## 实验输出

运行后会生成：

- `outputs/01_operator_mismatch.png`：同一个电流样本下 low/high/difference 磁场对比；
- `outputs/02_inverse_crime_gap.png`：低保真测试、高保真测试、校准后测试误差对比；
- `outputs/03_current_scatter.png`：真实电流 vs 预测电流散点图；
- `outputs/04_calibration_curve.png`：少量高保真校准样本数量与误差的关系；
- `outputs/05_residual_maps.png`：低保真解码器在高保真观测上的残差图；
- `outputs/06_fidelity_ladder.png`：low/medium/high 多保真误差阶梯；
- `outputs/PYPEEC_BRIDGE_TABLE.md`：从 exp07 导入的 real PyPEEC
  read-only fidelity bridge；
- `outputs/metrics.json`：关键定量指标；
- `outputs/RUN_REPORT.md`：gate 级别验收报告；
- `data/exp06_multifidelity_examples.npz`：示例数据、基函数与预测结果。

## 如何运行

```bash
pip install -r requirements.txt
python src/run_all.py
pytest -q
```

## 验收标准

本实验不是证明某个网络“最强”，而是证明路线中的 anti-inverse-crime gate 是必要的。验收标准：

1. low-fidelity test error 很低；
2. low → medium → high 的 operator gap 和 decoder error 单调上升；
3. high-fidelity test error 明显高于 low-fidelity test error；
4. 少量 high-fidelity calibration 可以显著降低 high-fidelity test error；
5. 输出图和 metrics 能清楚展示：**同源正演器测试不能代表真实泛化能力。**

`metrics.json` 中包含 `acceptance_gates` 和 `all_acceptance_gates_passed`。
这些 gates 是后续声称“模型能走向真实数据”之前的最低多保真验证门槛。

## 当前局限

- high-fidelity operator 仍是代理模型，不是真正 COMSOL/Ansys/FastHenry；
- PyPEEC bridge 只是导入 exp07 的真实 solver gap 作为外部 fidelity 信号，
  不使用 PyPEEC 样本做校准或训练；
- PyPEEC mini dataset 的冻结模型推理由 exp04 负责；exp06 只维护
  fidelity/operator-gap bridge；
- 未包含真实 QDM ODMR 谱线级噪声；
- 未包含温度/应力/微波不均匀；
- 未包含真实 FPC/GDS/Gerber 版图；
- 目标是验证方法论风险，而不是完成真实实验闭环。

下一阶段应扩展 PyPEEC/CAD-like 几何覆盖，或引入 FEM/FastHenry/QDM/PCB/FPC
外部证据。
