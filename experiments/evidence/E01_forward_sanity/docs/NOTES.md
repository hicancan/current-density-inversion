# Stage-1 Notes

## 正演器公式

有限直导线段从 `p0` 到 `p1`，电流从 `p0` 流向 `p1`。对观测点 `r`，定义：

```math
u = \frac{p_1-p_0}{\|p_1-p_0\|},\quad L=\|p_1-p_0\|
```

```math
R=r-p_0,\quad a=R\cdot u,\quad r_\perp=R-a u,\quad \rho=\|r_\perp\|
```

则：

```math
B(r)=\frac{\mu_0 I}{4\pi}(u\times r_\perp)
\left[
\frac{L-a}{\rho^2\sqrt{\rho^2+(L-a)^2}}
+
\frac{a}{\rho^2\sqrt{\rho^2+a^2}}
\right]
```

## 为什么先做有限线段

后续 EDA/Gerber/GDS 或 PCB/FPC 走线可以天然表示为有限矢量线段集合。网格 FFT 正演器适合大规模面电流数据，线段正演器适合最小 sanity check、via 模板和真实走线几何。

## 重要限制

本阶段尚未包含：

- ground plane / return current；
- QDM sensor PSF；
- NV projection noise covariance；
- standoff tilt；
- temperature drift；
- finite wire width and thickness；
- COMSOL/FEM stress test。

这些属于后续阶段的真实物理增强模块。
