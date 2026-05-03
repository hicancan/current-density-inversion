# exp01-biot-savart-forward-sanity

## 目标

这是多层电流反演项目的第一阶段实验：**先验证最小 Biot-Savart 正演器是否正确**。

本阶段只做正问题：

```math
J \rightarrow B_x,B_y,B_z
```

暂时不做神经网络、不做反演、不做拓扑 loss、不做 QDM 复杂噪声、不做 COMSOL。只有当这个正演器通过 sanity check 后，才进入可观测性计算器与两层 toy benchmark。

## 为什么这是第一步

整个项目后续的数据集、物理一致性损失、拓扑散度约束、多层解混叠，都依赖正演器。如果正演器方向、符号、单位或数量级错了，后面的网络会系统性学错。

## 本实验包含内容

```text
exp01-biot-savart-forward-sanity/
  ├── src/
  │   ├── forward/
  │   │   ├── constants.py
  │   │   ├── grid.py
  │   │   ├── segments.py
  │   │   └── analytic.py
  │   └── experiments/
  │       ├── plotting.py
  │       └── run_all.py
  ├── tests/
  │   └── test_forward_segments.py
  ├── configs/
  │   └── default.json
  ├── outputs/        # 运行后生成图像和 metrics.json
  ├── data/           # 本阶段预留缓存目录
  ├── requirements.txt
  └── README.md
```

## 已实现的物理源

1. 有限水平直导线
2. 矩形回路
3. 有限竖直 via 电流

所有代码使用 SI 单位：

- 长度：m
- 电流：A
- 磁场：T

## 安装

建议使用 Python 3.10+。

```bash
cd exp01-biot-savart-forward-sanity
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 运行实验

```bash
python src/experiments/run_all.py --out outputs
```

运行后会生成：

- `outputs/01_single_wire_Bxyz.png`
- `outputs/02_wire_vs_infinite_reference.png`
- `outputs/03_rect_loop_Bxyz.png`
- `outputs/04_single_via_Bxyz.png`
- `outputs/05_standoff_scan.png`
- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `outputs/fields_stage1_examples.npz`

## 运行测试

```bash
PYTHONPATH=src pytest -q
```

测试包括：

1. 电流反向时磁场严格反号；
2. 长有限导线在中心区域接近无限长导线解析解；
3. 理想竖直 via 的 `Bz` 近似为 0，主要产生面内环绕磁场 `Bx, By`。

## 完成标准

本阶段完成不以“代码写完”为标准，而以 sanity check 图和指标为标准：

1. 单根水平导线的 `Bx, By, Bz` 符合右手定则；
2. 有限长导线中心区域接近无限长导线解析解；
3. 矩形回路体现线性叠加；
4. 竖直 via 主要产生环绕面内磁场，`Bz` 近似为 0；
5. standoff 增大时磁场幅值下降且空间结构变平滑。

`metrics.json` 中包含 `acceptance_gates` 和
`all_acceptance_gates_passed`，这些 gates 是本实验是否可作为后续数据
生成与物理 loss 地基的硬验收标准。

## 下一阶段

通过本实验后，进入：

1. 可观测性计算器；
2. 单层 Fourier 反演复现；
3. 两层 + via toy benchmark；
4. topology soft loss 验证。
