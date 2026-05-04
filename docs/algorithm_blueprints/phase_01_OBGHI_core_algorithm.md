# 第一阶段：OBGHI —— 顶级学术核心算法

**全称**：Observable Bayesian Graph-Hodge Inversion  
**中文名**：可观测贝叶斯图-Hodge电流反演  
**阶段定位**：顶级学术核心 / 论文级最锋利内核  
**对应目标**：解释并解决近场磁场电流反演中的“拓扑不可辨识”和“错误自信输出”问题。  
**一句话定义**：

> OBGHI 不是完整工业系统，而是整个算法体系的最小顶级理论内核：只在物理可行且磁场可观测的拓扑子空间中进行贝叶斯反演，并在不可辨识时拒判。

---

## 1. 为什么这是第一阶段？

第一阶段的目标不是工业落地，也不是构建完整 AI/EDA 平台，而是回答一个最根本的科学问题：

\[
\text{在 Biot-Savart 低通观测下，哪些电流拓扑是可辨识的？}
\]

传统反演方法通常求：

\[
\hat x=\arg\min_x \|Ax-b\|^2+\lambda R(x)
\]

或者加入 KCL：

\[
\hat x=\arg\min_x \|Ax-b\|^2+\lambda\|Kx\|^2
\]

但问题在于：

\[
A
\]

是强低通算子，很多内部电流模式在磁场观测中几乎不可见。更严重的是，若离散图模型漏建 via、return path、边界泄漏或传感器配准误差，则强制 \(Kx=0\) 会把真实解投影到错误子空间。

OBGHI 的核心改写是：

\[
x=H_gz
\]

其中 \(H_g\) 是由 layout、Graph-Hodge、candidate via、return loop、observable harmonic modes 和 model-gap basis 构成的物理生成基。

---

## 2. 核心数学模型

观测模型：

\[
b=A_\theta H_gz+U_{\rm gap}\xi+\varepsilon
\]

其中：

- \(b\)：磁场观测；
- \(A_\theta\)：带校准参数的 Biot-Savart / Maxwell 正演；
- \(H_g\)：拓扑 \(g\) 下的物理电流基；
- \(z\)：低维电流系数；
- \(U_{\rm gap}\xi\)：模型误差，如配准、高度、PSF、层深、漏建路径；
- \(\varepsilon\sim \mathcal N(0,\Sigma)\)：观测噪声。

贝叶斯后验：

\[
p(z,g,\theta,\xi\mid b)
\propto
p(b\mid z,g,\theta,\xi)
p(z\mid g)
p(g)
p(\theta)
p(\xi)
\]

---

## 3. Graph-Hodge 物理基

\[
H_g=[
H_{\rm graph},
H_{\rm via},
H_{\rm loop},
H_{\rm harm,obs},
H_{\rm port},
H_{\rm gap},
H_{\rm res}
]
\]

含义：

- \(H_{\rm graph}\)：版图 trace / plane / net 上的正常电流模式；
- \(H_{\rm via}\)：候选过孔、跨层通量、source-sink 模式；
- \(H_{\rm loop}\)：无散 return loop；
- \(H_{\rm harm,obs}\)：可观测 harmonic / boundary / hole mode；
- \(H_{\rm port}\)：已知激励与端口约束；
- \(H_{\rm gap}\)：结构性模型误差基；
- \(H_{\rm res}\)：off-layout / unknown residual path，用于避免 \(H_g\) 先验过硬。

---

## 4. 可观测拓扑压缩

完整 harmonic 空间可能很大，但并非所有模式都能被磁场观测支持。定义：

\[
F_{\rm harm}
=
H_{\rm harm}^{\top}A^{\top}\Sigma^{-1}AH_{\rm harm}
\]

\[
R_{\rm harm}
=
H_{\rm harm}^{\top}RH_{\rm harm}
\]

求广义特征问题：

\[
F_{\rm harm}v_i=\lambda_iR_{\rm harm}v_i
\]

仅保留：

\[
\lambda_i>\tau_{\rm obs}
\]

得到：

\[
H_{\rm harm,obs}=H_{\rm harm}[v_1,\dots,v_K]
\]

核心原则：

\[
\boxed{
\text{只估计磁场观测可支持的拓扑模式，不在不可观测拓扑上硬判。}
}
\]

---

## 5. Bayesian Evidence 与 ARD

固定拓扑 \(g\)：

\[
b=B_gz+\varepsilon,\quad B_g=A_\theta H_g
\]

\[
z\sim \mathcal N(0,\Lambda_g^{-1})
\]

后验：

\[
\Sigma_{z,g}=(B_g^\top\Sigma^{-1}B_g+\Lambda_g)^{-1}
\]

\[
\mu_{z,g}=\Sigma_{z,g}B_g^\top\Sigma^{-1}b
\]

边缘似然：

\[
p(b\mid g)=\mathcal N(0,C_g)
\]

\[
C_g=\Sigma+B_g\Lambda_g^{-1}B_g^\top
\]

\[
\log p(b\mid g)
=
-\frac12b^\top C_g^{-1}b
-\frac12\log|C_g|
-\frac m2\log(2\pi)
\]

拓扑后验：

\[
p(g\mid b)\propto p(b\mid g)p(g)
\]

---

## 6. 不可辨识诊断

定义白化子空间：

\[
\tilde S_{\rm via}=\operatorname{span}(\Sigma^{-1/2}AH_{\rm via})
\]

\[
\tilde S_{\rm gap}=\operatorname{span}(\Sigma^{-1/2}U_{\rm gap})
\]

最小主角：

\[
\theta_{\min}
=
\angle_{\min}(\tilde S_{\rm via},\tilde S_{\rm gap})
\]

若：

\[
\theta_{\min}<\tau_\theta
\]

说明 via 与 model-gap 在当前观测下不可分。

Bayes factor：

\[
{\rm BF}_{\rm via/gap}
=
\frac{p(b\mid H_{\rm via})}{p(b\mid H_{\rm gap})}
\]

若：

\[
|\log{\rm BF}_{\rm via/gap}|<\epsilon
\]

则 evidence 不足，应拒判。

---

## 7. 输出

OBGHI 输出：

\[
\mathbb E[x\mid b]
\]

\[
\operatorname{Cov}(x\mid b)
\]

\[
p(g\mid b)
\]

\[
P(\text{via}_q\mid b)
\]

\[
P(\text{model-gap explanation}\mid b)
\]

\[
P(\text{unmodeled path}\mid b)
\]

以及：

\[
\text{accept / reject / need next measurement}
\]

---

## 8. 这一阶段的突破性

OBGHI 的突破在于：

1. 把电流反演从像素优化变成拓扑后验推断；
2. 把 KCL 从外部 penalty 变成物理生成基；
3. 把“数学存在的拓扑模式”与“磁场可观测的拓扑模式”分开；
4. 把错误自信输出替换为 posterior / uncertainty / rejection；
5. 让不可辨识成为算法输出的一部分，而不是失败后的解释。

---

## 9. 边界

OBGHI 不是完整系统。它不解决：

- 整芯片指数级拓扑搜索；
- 大规模多保真正演成本；
- GNN proposal；
- SMC/MH 全后验采样；
- NV 量子传感观测模型；
- 工业 FA/EDA 工作流。

因此：

\[
\boxed{
\text{OBGHI = 顶级学术核心，不是最终突破级完整系统。}
}
\]

---

## 10. 适用价值

OBGHI 是后续所有阶段的算法内核。没有 OBGHI，后续阶段只是工程堆叠；有了 OBGHI，后续系统才有清晰的物理、拓扑和贝叶斯基础。

