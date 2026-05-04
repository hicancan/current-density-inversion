# E13 Identifiability Gain Table

Gain ratios relative to single-height / single-state / Bz-only baseline.

| Heights | N States | Components | Margin Gain | Rank Gain | Cond Ratio | Via AUC Gain | Layer Err Reduction |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| single | 1 | Bz | 1.000x | 1.0x | 1.000x | 1.000x | 1.402x |
| single | 1 | Bxy | 1.049x | 1.0x | 0.681x | 1.329x | 1.465x |
| single | 1 | Bxyz | 0.826x | 1.0x | 0.635x | 1.305x | 1.444x |
| single | 2 | Bz | 1.034x | 1.0x | 1.000x | 1.207x | 1.420x |
| single | 2 | Bxy | 0.905x | 1.0x | 0.681x | 1.232x | 1.397x |
| single | 2 | Bxyz | 0.969x | 1.0x | 0.635x | 1.085x | 1.418x |
| single | 4 | Bz | 0.969x | 1.0x | 1.000x | 1.305x | 1.382x |
| single | 4 | Bxy | 0.932x | 1.0x | 0.681x | 1.793x | 1.387x |
| single | 4 | Bxyz | 0.846x | 1.0x | 0.635x | 1.317x | 1.369x |
| dual | 1 | Bz | 0.629x | 1.0x | 1.100x | 1.159x | 1.441x |
| dual | 1 | Bxy | 0.772x | 1.0x | 0.764x | 1.500x | 1.372x |
| dual | 1 | Bxyz | 0.964x | 1.0x | 0.707x | 1.146x | 1.390x |
| dual | 2 | Bz | 1.069x | 1.0x | 1.100x | 1.024x | 1.405x |
| dual | 2 | Bxy | 0.912x | 1.0x | 0.764x | 0.793x | 1.389x |
| dual | 2 | Bxyz | 0.847x | 1.0x | 0.707x | 1.695x | 1.385x |
| dual | 4 | Bz | 1.024x | 1.0x | 1.100x | 1.402x | 1.401x |
| dual | 4 | Bxy | 0.745x | 1.0x | 0.764x | 1.134x | 1.421x |
| dual | 4 | Bxyz | 1.191x | 1.0x | 0.707x | 1.732x | 1.384x |
| triple | 1 | Bz | 0.859x | 1.0x | 1.135x | 1.622x | 1.403x |
| triple | 1 | Bxy | 0.930x | 1.0x | 0.806x | 1.171x | 1.423x |
| triple | 1 | Bxyz | 1.068x | 1.0x | 0.742x | 1.134x | 1.427x |
| triple | 2 | Bz | 0.999x | 1.0x | 1.135x | 1.866x | 1.386x |
| triple | 2 | Bxy | 0.946x | 1.0x | 0.806x | 1.390x | 1.383x |
| triple | 2 | Bxyz | 0.953x | 1.0x | 0.742x | 0.622x | 1.410x |
| triple | 4 | Bz | 0.920x | 1.0x | 1.135x | 1.341x | 1.400x |
| triple | 4 | Bxy | 1.004x | 1.0x | 0.806x | 1.378x | 1.432x |
| triple | 4 | Bxyz | 1.003x | 1.0x | 0.742x | 1.256x | 1.407x |

Gain > 1.0x indicates improvement over baseline. Layer error reduction > 1.0x means graph prior helps.

All results are generated-domain only.
