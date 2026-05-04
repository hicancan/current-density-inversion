# 第二阶段：R-MF-CTAS-Ω-BGHOID —— 顶级算法系统

**全称**：Robust Multi-Fidelity Certified Transport-Amortized Structured Omega Bayesian Graph-Hodge Operator Inference and Design  
**中文名**：鲁棒多保真可认证传输摊销结构化 Ω 级贝叶斯图-Hodge算子推断与主动设计  
**阶段定位**：顶级算法系统 / 可运行研究级完整架构  
**一句话定义**：

> R-MF-CTAS-Ω-BGHOID 以 OBGHI 为反演内核，加入拓扑搜索、多保真计算、鲁棒 delayed acceptance、GNN 混合 proposal、HF 审计和主动观测，使算法从局部学术核心升级为可运行的突破级系统。

---

## 1. 为什么需要第二阶段？

OBGHI 解决了“如何在可观测拓扑子空间中进行贝叶斯反演”，但它仍然面临三大问题：

1. **拓扑空间爆炸**：

\[
|\mathcal G|\sim 2^K
\]

2. **证据计算昂贵**：

\[
C_g^{-1}b,\quad \log|C_g|
\]

3. **正演成本过高**：

高保真 Maxwell/FEM/FDTD/BEM 求解器不能在每个粒子、每个拓扑上直接调用。

因此需要第二阶段系统：R-MF-CTAS。

---

## 2. 状态空间

完整状态：

\[
s=(g,z,\theta,\xi)
\]

其中：

- \(g\)：拓扑 motif 组合；
- \(z\)：连续电流系数；
- \(\theta\)：传感器和几何校准参数；
- \(\xi\)：model-gap 参数。

目标后验：

\[
p(g,z,\theta,\xi\mid y)
\propto
p(y\mid g,z,\theta,\xi)
p(z\mid g)
p(g)
p(\theta)
p(\xi)
\]

对 \(z\) 做 Rao-Blackwellization：

\[
\ell(g,\theta,\xi)
=
\int p(y\mid z,g,\theta,\xi)p(z\mid g)\,dz
\]

collapsed target：

\[
\pi_{\rm col}(g,\theta,\xi)
\propto
\ell(g,\theta,\xi)p(g)p(\theta)p(\xi)
\]

---

## 3. Motif 拓扑空间

定义 motif 库：

\[
\mathcal M=
\{
\text{via activation},
\text{return loop},
\text{deep layer segment},
\text{registration artifact},
\text{model-gap patch},
\text{boundary leakage},
\text{fixture current},
\text{unmodeled path}
\}
\]

拓扑：

\[
g=\{(a_i,r_i)\}_{i=1}^{K}
\]

其中：

- \(a_i\in\{0,1\}\)：motif 是否激活；
- \(r_i\)：位置、层、方向、尺度、net、局部几何属性。

先验：

\[
p(g)
\propto
\exp\left[
\sum_i\psi_i+
\sum_{i,j}\psi_{ij}
+
\sum_c\psi_c
\right]
\]

---

## 4. GNN 混合 Proposal

GNN 不直接给后验，只给 proposal：

\[
q_{\rm GNN}(g\mid y,L)
\neq
p(g\mid y)
\]

为了防止 OOD 死锁，必须使用混合 proposal：

\[
q_{\rm mix}
=
\alpha q_{\rm GNN}
+
\beta q_{\rm prior}
+
\gamma q_{\rm residual}
+
\delta q_{\rm local}
+
\epsilon q_{\rm random}
+
\zeta q_{\rm OOD}
\]

这保证：

\[
\operatorname{supp}(\pi)\subseteq\operatorname{supp}(q_{\rm mix})
\]

GNN 负责加速搜索，贝叶斯权重负责校正。

---

## 5. Transport-Amortized SMC

温度序列：

\[
0=\beta_0<\beta_1<\cdots<\beta_T=1
\]

中间分布：

\[
\pi_t(s)
\propto
p(s)\ell(s)^{\beta_t}
\]

粒子：

\[
\{s_i,w_i\}_{i=1}^{N}
\]

权重更新：

\[
w_t^{(i)}
=
w_{t-1}^{(i)}
\ell(s_i)^{\beta_t-\beta_{t-1}}
\]

有效样本数：

\[
{\rm ESS}
=
\frac{(\sum_iw_i)^2}{\sum_iw_i^2}
\]

ESS 低时 resample。

---

## 6. 多保真正演金字塔

构造五层模型：

\[
\mathcal G_0,\mathcal G_1,\mathcal G_2,\mathcal G_3,\mathcal G_4
\]

### L0：Analytic screening

极快筛查：

- 几何是否可行；
- motif 是否违反 topology；
- 是否明显不可观测；
- 是否与 residual map 完全不相关。

### L1：Coarse quasi-static / Biot-Savart

粗网格、粗层深、简化 PSF 的快速正演。

### L2：DEC-preserving ROM

保持：

\[
D_{k+1}D_k=0
\]

的物理结构降阶模型。

### L3：Certified surrogate / neural operator

带不确定性、OOD 检测和物理残差认证的代理模型。

### L4：High-fidelity solver

完整 FEM/BEM/FDTD/Maxwell/high-resolution Biot-Savart 求解。

---

## 7. Robust delayed acceptance

低保真层不能硬拒真解。每级给出：

\[
\log\ell_j(s),\quad \Delta_j(s)
\]

其中 \(\Delta_j\) 是低保真误差或不确定性。

鲁棒晋级规则：

\[
\log\ell_j(s)+\kappa\Delta_j(s)>\tau_j
\Rightarrow
\text{promote}
\]

同时保留随机高保真审计：

\[
P(\text{HF audit}\mid s)\ge p_{\min}
\]

目标是防止：

\[
\text{low fidelity bias}
\Rightarrow
\text{premature rejection of true topology}
\]

---

## 8. 高保真预算调度

定义高保真调用价值：

\[
{\rm VOI}_{\rm HF}(s)
=
\mathbb E[
\Delta \text{posterior accuracy}
\mid
\text{evaluate HF at }s
]
\]

若：

\[
{\rm VOI}_{\rm HF}(s)>c_{\rm HF}
\]

且预算允许，则调用 L4。

否则使用低保真 likelihood，并膨胀误差协方差：

\[
\Gamma_{\rm model}
\leftarrow
\Gamma_{\rm model}
+
\Gamma_{\rm LF-error}
\]

---

## 9. 证据计算加速

使用：

\[
C_g=\Sigma+B_g\Lambda_g^{-1}B_g^\top
\]

Woodbury：

\[
C_g^{-1}
=
\Sigma^{-1}
-
\Sigma^{-1}B_g
(\Lambda_g+B_g^\top\Sigma^{-1}B_g)^{-1}
B_g^\top\Sigma^{-1}
\]

Log-det：

\[
\log|C_g|
=
\log|\Sigma|
+
\log|\Lambda_g+B_g^\top\Sigma^{-1}B_g|
-
\log|\Lambda_g|
\]

大规模时使用：

- matrix-free matvec；
- preconditioned CG；
- stochastic Lanczos quadrature；
- block Schur preconditioner。

---

## 10. Proposal Survival Mechanism

监控：

\[
{\rm ESS}
\]

\[
{\rm MH\ acceptance}
\]

\[
{\rm posterior\ predictive\ failure}
\]

\[
{\rm proposal\ KL}
\]

若 GNN 失败：

\[
{\rm ESS}\downarrow,\quad \alpha_{\rm MH}\downarrow
\]

则自动降低：

\[
\alpha
\]

并提高：

\[
\beta,\gamma,\epsilon,\zeta
\]

即从 GNN 主导切换到 prior / residual / random / OOD rescue。

---

## 11. 主动观测

若当前后验不可辨：

\[
\theta_{\min}<\tau_\theta
\]

或：

\[
|\log{\rm BF}|<\epsilon
\]

则选择下一观测：

\[
m^\star=
\arg\max_m
[
{\rm DUG}(m)
+
\lambda_1\Delta\theta_{\min}(m)
+
\lambda_2\Delta\log{\rm BF}(m)
-
\lambda_3c(m)
]
\]

其中 DUG 是 decision utility gain。

---

## 12. 输出

第二阶段输出：

- posterior current；
- topology posterior；
- model-gap posterior；
- calibrated uncertainty；
- rejected / accepted topology；
- HF budget report；
- proposal diagnostics；
- next best measurement。

---

## 13. 这一阶段的突破性

R-MF-CTAS-Ω-BGHOID 的突破在于：

1. 让 OBGHI 从 ROI 论文算法升级为可扩展系统；
2. 用 GNN 加速拓扑搜索，但不让 GNN 直接决定后验；
3. 用多保真金字塔控制正演算力；
4. 用鲁棒晋级和 HF 审计避免低保真早衰；
5. 用主动观测突破当前观测不可辨识；
6. 用贝叶斯校正保持物理可信。

---

## 14. 边界

本阶段仍不改变观测物理本身。如果磁场观测中某些深层模式已经低于噪声底，算法只能拒判并建议新观测，不能凭空恢复。

因此第二阶段是：

\[
\boxed{
\text{顶级算法系统，但还不是观测物理联合突破。}
}
\]

