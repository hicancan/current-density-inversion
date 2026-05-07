# Invariant Definitions and Sanity Checks

## 1. Column-Space Projector

```math
P_h = Q_h Q_h^T,    Q_h = orth(T_{y,h})
d_P(h,g) = ||P_h - P_g||_F / sqrt(2)
```

Properties:
- P^2 = P (idempotent)
- P^T = P (symmetric)
- Range [0, 1]
- Invariant to invertible mixing of columns (T -> T M for invertible M)
- Invariant to global scale (T -> alpha T)

## 2. Whitened Gram Matrix

```math
G_h = T_{y,h}^T T_{y,h}
G_bar_h = diag(G_h)^{-1/2} G_h diag(G_h)^{-1/2}
d_G(h,g) = ||G_bar_h - G_bar_g||_F
```

Properties:
- diag(G_bar_h) = 1 (whitened)
- Cancels per-state amplitude scale
- Invariant to per-column scaling

## 3. Differential Common-Mode Cancellation

```math
Delta T_h = T_h - T_h[:, 0]  (reference column subtraction)
Delta T_h_pairwise = [T_h[:, a] - T_h[:, b] for a < b]
```

Properties:
- Cancels common-mode signal present in all states
- Highlight topology-dependent differences between excitation states

## Sanity Checks

All invariant representations passed idempotence, symmetry, whitening,
and reference-zero sanity checks.