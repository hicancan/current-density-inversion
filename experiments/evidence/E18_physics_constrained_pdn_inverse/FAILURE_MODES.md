# Failure Modes - E18

## Known Failure Modes

### 1. Deep Layer Misallocation
The four-layer stack has significant depth-dependent signal attenuation.
Layers L3 (-160µm) and L4 (-260µm) contribute weaker magnetic fields to
the sensor plane. All methods struggle with deep-layer current recovery.

### 2. No-Via False Positives
When ground truth has no vias, the inverse may hallucinate via signatures
due to residual field patterns. The KCL constraint helps but does not
eliminate this.

### 3. Dense Via Cluster Under-Recovery
Dense via clusters produce overlapping field signatures that are hard to
separate. Via recall drops on these cases.

### 4. Layer Misallocation Trap
Cases with current in L1+L4 only (skipping L2/L3) can fool methods into
allocating current to intermediate layers.

### 5. Return Grid Ambiguity
Bottleneck return paths create field patterns that could be explained by
multiple current distributions. The inverse is not uniquely determined.

### 6. B Residual vs Current Accuracy Trade-off
A low B residual does not guarantee correct current allocation. The inverse
problem is ill-posed, and multiple current distributions can produce similar
fields. Physics constraints help but do not resolve all ambiguity.

### 7. KCL-RMSE Trade-off
Enforcing KCL consistency can increase current RMSE if the true current
distribution has non-zero divergence (e.g., from via source/sink effects
not captured by the simple divergence matrix).

## Mitigation Strategies

- Multi-height measurement (E13) improves layer separability
- Graph/KCL constraints (this work) reduce misallocation
- Via sparsity regularization reduces false positives
- Post-projection enforces physical consistency
