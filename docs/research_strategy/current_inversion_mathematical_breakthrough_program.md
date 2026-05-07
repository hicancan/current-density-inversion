# Mathematical Breakthrough Program for Magnetic-Field-to-Current Inversion

Status: top-level research design. This document is not evidence.

Central goal:

```text
Recover decision-relevant current structure from magnetic field measurements,
with explicit certificates for what is observable, what is unobservable, and
what additional excitation/measurement would break the ambiguity.
```

This program is written to guide Claude worktree workers. It is not an
implementation and must not be used to upgrade claims by itself.

## 1. Physical Inverse Problem

Let the chip current density be `J(r)` and let magnetic observations be sampled
on sensor surfaces `Omega_m` under excitation states `s = 1,...,S`.

The forward map is the quasi-static Biot-Savart operator:

```math
B_s(r)
= {\mu_0 \over 4\pi}
  \int_D {J_s(r') \times (r-r') \over \|r-r'\|^3}\,dr',
\qquad r \in \Omega_m .
```

After discretization:

```math
y_s = A_s i_s + \eta_s ,
```

where:

- `i_s in R^E` is an edge-current vector;
- `A_s in R^{M_s x E}` is the sensor/forward matrix;
- `eta_s` is measurement noise and model residual.

For a planar sheet at height `z_l`, the Fourier-domain normal field contains:

```math
\widehat{B_z}(k,z_0)
= {\mu_0 \over 2} e^{-|k|(z_0-z_l)}
   i(k_x \widehat{J_y}(k,z_l)-k_y \widehat{J_x}(k,z_l)).
```

This formula exposes the first-principles bottleneck:

```math
Only weighted curl-like components are directly visible; high spatial
frequencies and depth-separated layers are exponentially attenuated.
```

Therefore a breakthrough cannot come from unconstrained inversion alone. It
must add information through at least one of:

```text
1. stronger admissible current spaces,
2. multi-state or active excitation,
3. multi-height/vector observation,
4. forward-operator calibration,
5. decision-level quotienting and refusal,
6. external/real validation.
```

## 2. Graph-Hodge Current Model

Let a layout-derived current graph be:

```math
G_h = (V_h, E_h),
```

where hypothesis `h` changes the graph, layer coupling, via/return topology, or
allowed current subspace.

Let `D_h in R^{|V_h| x |E_h|}` be the oriented incidence matrix. Under excitation
state `s`, KCL imposes:

```math
D_h i_{h,s} = b_s ,
\qquad {\bf 1}^T b_s = 0 .
```

If `b_s` is feasible, all KCL-compatible currents form an affine space:

```math
\mathcal{I}_{h,s}
= i^0_{h,s} + \ker(D_h)
= i^0_{h,s} + N_h z_s ,
```

where:

```math
D_h i^0_{h,s} = b_s,\qquad D_h N_h = 0 .
```

The graph-Hodge split is:

```math
R^{E_h}
= \operatorname{im}(D_h^T)
  \oplus \ker(D_h)
```

with an affine source/sink component plus a cycle-space component. For internal
nodes, valid physical current candidates must keep KCL residual:

```math
\|D_{h,\mathrm{int}} i_{h,s}\|_2 \le \epsilon_{\mathrm{KCL}} .
```

The SVD nullspace projection used in E23 is mathematically:

```math
D_{h,\mathrm{int}}
= U \Sigma V^T,\qquad
N_h = V_{[:,r+1:E]},
```

where `r` is the numerical rank. For a raw mode `v`, the KCL-compatible
projection is:

```math
\Pi_{\ker D} v = N_h N_h^T v .
```

This is the minimum Euclidean perturbation that enforces internal KCL:

```math
\Pi_{\ker D}v
= \arg\min_{u:D_{\mathrm{int}}u=0} \|u-v\|_2^2 .
```

## 3. Observation Manifolds and OQCI

For a stacked multi-state observation:

```math
Y =
\begin{bmatrix}
y_1 \\
\vdots \\
y_S
\end{bmatrix},
\qquad
\eta =
\begin{bmatrix}
\eta_1 \\
\vdots \\
\eta_S
\end{bmatrix},
```

define the hypothesis observation manifold:

```math
\mathcal{M}_h(U)
=
\left\{
\begin{bmatrix}
A_1(i^0_{h,1}+N_h z_1)\\
\vdots\\
A_S(i^0_{h,S}+N_h z_S)
\end{bmatrix}
: z_s \in R^{q_h}
\right\}.
```

Here `U=[b_1,...,b_S]` is the excitation design matrix. With shared latent
parameters `theta`, a tighter model is:

```math
\mathcal{M}_h(U)
= \{ a_h(U) + B_h(U)\theta : \theta \in \Theta_h \}.
```

The OQCI accepted set is:

```math
\mathcal{C}(Y)
=
\{ h : d_h(Y)^2 \le \tau_h^2 \},
```

where the regularized weighted distance is:

```math
d_h(Y)^2
=
\min_\theta
\|W(Y-a_h-B_h\theta)\|_2^2
+ \lambda \|L_h\theta\|_2^2 .
```

The closed-form solution is:

```math
\hat{\theta}_h
=
(B_h^T W^T W B_h + \lambda L_h^T L_h)^{-1}
B_h^T W^T W (Y-a_h),
```

and the residual is:

```math
r_h(Y)=Y-a_h-B_h\hat{\theta}_h .
```

The key decision is not "recover every current vector." It is:

```math
Does \mathcal{C}(Y) contain one decision-equivalent hypothesis, and does it
contain the truth under calibrated noise?
```

## 4. Pairwise Separability

For two hypotheses `h` and `g`, define the directed deterministic separation:

```math
\delta_{h\to g}(U)
=
\inf_{\theta_h \in \Theta_h}
 d_g(a_h(U)+B_h(U)\theta_h).
```

For linear subspaces through zero, with orthonormal bases `Q_h,Q_g`, the
minimum principal angle satisfies:

```math
\sin \theta_{\min}(h,g)
=
\sigma_{\min}((I-Q_g Q_g^T) Q_h).
```

If `sin theta_min = 0`, the two subspaces intersect and no zero-noise
measurement in that protocol can distinguish all currents in the intersection.

For affine manifolds, the separation is:

```math
\delta_{hg}(U)^2
=
\min_{\theta_h,\theta_g}
\|W[(a_h-a_g)+B_h\theta_h-B_g\theta_g]\|_2^2 .
```

Let:

```math
C_{hg}=[B_h,-B_g],\qquad c_{hg}=a_h-a_g.
```

Then:

```math
\delta_{hg}(U)^2
=
\|W c_{hg} - W C_{hg}
   (C_{hg}^T W^T W C_{hg})^\dagger
   C_{hg}^T W^T W c_{hg}\|_2^2 .
```

This is the core certificate: a pair is distinguishable only if its affine
observation manifolds have positive weighted distance after quotienting
nuisance degrees of freedom.

## 5. Noise and Operator-Perturbation Robustness

Assume:

```math
Y = (A+\Delta A)i_h + \eta,
\qquad
\|W\eta\|_2 \le \epsilon,
\qquad
\|W\Delta A i\|_2 \le \rho_h(U)
```

for all admissible `i in \mathcal{I}_h(U)`.

If truth is `h`, then `h` remains accepted when:

```math
\tau_h \ge \epsilon + \rho_h(U).
```

A wrong hypothesis `g` is rejected when:

```math
\delta_{hg}(U) > \tau_g + \epsilon + \rho_h(U)+\rho_g(U).
```

Therefore define the robust pair margin:

```math
\Gamma_{hg}(U)
=
\delta_{hg}(U)
- \tau_g
- \epsilon
- \rho_h(U)-\rho_g(U).
```

The generated-domain breakthrough certificate should require:

```math
\Gamma_{hg}(U) > 0
```

for the target pairs, and ideally for all decision-critical pairs. This is
stronger than reporting a raw distance increase.

An empirical perturbation ladder estimates:

```math
\rho_h(U)
\approx
\max_{\Delta A \in \mathcal{D}}
\max_{i\in\mathcal{I}_h(U),\|i\|\le R_h}
\|W\Delta A i\|_2 .
```

The current E23 finite-width/registration/deep-layer tests are first
surrogates for `\mathcal{D}`. Round 5 must turn them into margins, not only
distances.

## 6. Why Multi-State Can Break H1/H2 When Multi-Height Fails

Single-state observation uses:

```math
\mathcal{M}_h(b_1)
= a_h(b_1)+B_h(b_1)\Theta_h .
```

If H1 and H2 share a near-null direction:

```math
v \in \mathcal{M}_{H1}(b_1) \cap \mathcal{M}_{H2}(b_1),
```

then a second sensor height may still fail if it applies a similar smoothing
operator:

```math
A_{z_2} \approx S A_{z_1},
```

so that:

```math
(A_{z_1}v,A_{z_2}v)
```

remains nearly common to both manifolds.

Multi-state excitation changes the boundary condition:

```math
D_h i_{h,s}=b_s .
```

The stacked ambiguity requires a common explanation for every state:

```math
Y(U) \in
\mathcal{M}_{H1}(U)\cap\mathcal{M}_{H2}(U)
=
\bigcap_{s=1}^S
\left[
\mathcal{M}_{H1}(b_s)\cap\mathcal{M}_{H2}(b_s)
\right].
```

If the near-null H1/H2 ambiguity depends on the port-flow pattern, adding
linearly independent `b_s` reduces the intersection dimension:

```math
\dim(\mathcal{M}_{H1}(U)\cap\mathcal{M}_{H2}(U))
<
\dim(\mathcal{M}_{H1}(b_1)\cap\mathcal{M}_{H2}(b_1)).
```

This is the mathematical reason E23 is the current main route: selective
port-feasible states alter the current-flow topology, while extra heights often
only rescale already visible spatial modes.

## 7. Active Excitation Design

Let the feasible port-excitation set be:

```math
\mathcal{U}
=
\{U=[b_1,\ldots,b_S]:
{\bf 1}^T b_s=0,\;
\|b_s\|_1 \le I_{\max},\;
b_s \text{ obeys hardware port constraints}\}.
```

The robust minimax design problem is:

```math
U^*
=
\arg\max_{U\in\mathcal{U}}
\min_{(h,g)\in\mathcal{P}_{crit}}
\Gamma_{hg}(U)
- c(U).
```

If a probability model is available, an alternative is Chernoff-style design:

```math
U^*
=
\arg\max_{U\in\mathcal{U}}
\min_{h\ne g}
C_{hg}(U),
```

where for Gaussian observations with equal covariance `Sigma`:

```math
C_{hg}(U)
= {1\over 8}
(\mu_h(U)-\mu_g(U))^T
\Sigma^{-1}
(\mu_h(U)-\mu_g(U)).
```

For composite linear manifolds, replace means with the residual gap:

```math
C^{GLRT}_{hg}(U)
= {1\over 2}
\left[
d_g(Y_h(U))^2-d_h(Y_h(U))^2
\right].
```

The sequential next-measurement policy is:

```math
b_{S+1}^*
=
\arg\max_{b\in\mathcal{U}_1}
\mathbb{E}_{Y_b|Y_{1:S}}
\left[
|\mathcal{C}(Y_{1:S})|
-|\mathcal{C}(Y_{1:S},Y_b)|
-\alpha\,\mathbf{1}\{\text{truth missing}\}
\right].
```

Round 5 should use the robust margin `Gamma`, not raw interval width, as the
primary acquisition score.

## 8. Breakthrough Definition

A generated-domain breakthrough candidate needs all of:

```text
1. KCL-compatible current basis with numerical residual below tolerance.
2. Positive robust margin for critical topology pairs after noise/operator
   perturbation.
3. Port-feasible excitation design, not only ideal internal actuation.
4. Truth-containing consistent sets with low empty rate and low wrong-accept
   rate.
5. Scaling across a layout ensemble, not one hand-picked layout.
6. Explicit cannot-claim boundary against real QDM/NV, real CAD/GDS, and
   external solvers until those packages exist.
```

The current strongest hypothesis is:

```text
Selective port-feasible multi-state excitation plus SVD-projected Graph-Hodge
current bases creates a robust observable quotient for via/return-like
topology decisions that single-state and multi-height measurements cannot
separate.
```

Round 5 must either certify this hypothesis with robust margins and layout
ensemble scaling, or falsify it cleanly.

