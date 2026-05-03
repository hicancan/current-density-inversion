# 设计说明

## 为什么 exp05 不是网络训练？

前面 exp04 已经证明 topology soft loss 能显著压低非物理散度残差，但也暴露出单靠拓扑约束并不能自动提升 via 定位。进入更强模型前，必须先把真实传感器链路中的几个基础扰动引入 benchmark：

- standoff tilt；
- PSF / pixel integration；
- correlated channel noise；
- spatially correlated noise；
- pixel confidence map；
- via-scale band-pass detection。

## standoff tilt

从常数距离

```math
z=z_0
```

升级为平面距离场：

```math
z(x,y)=z_0+\alpha x + \beta y
```

在 2 mm FOV 中，`alpha=0.006` 对应约 0.34 度倾角，仍会带来约 12 um 的距离变化。

## QDM-like noise

本实验不直接模拟 ODMR 谱，而是在 Cartesian `Bx,By,Bz` 空间中加入相关噪声。其思想是近似表达：NV 多轴投影反解 Cartesian 分量后，三个通道的噪声不一定独立。

## Via band-pass

裸 Laplacian 会在 Fourier 域乘以 `k^2`，极易放大极高频像素噪声。因此本实验采用 Difference of Gaussians (DoG) 作为尺度可控的 band-pass 预处理，并与 via template matched filter 结合。
