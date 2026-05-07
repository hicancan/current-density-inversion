# Standard Inversion Audit

This package compares a strict full least-squares inverse against the certified
observable projection.

| method | total RMSE | stable RMSE | dark hallucination norm |
|---|---:|---:|---:|
| full naive inverse | 720.7362501 | 0.1164511532 | 8649.239996 |
| ridge shrinkage | 0.4542784679 | 0.1182864903 | 0.4650431412 |
| certified projection | 0.4657956787 | 0.1164511532 | 0 |

Ridge shrinkage can reduce full-map error by suppressing unstable modes, but
without an explicit certificate it can still be misread as full current
recovery. E33 makes the projection/refusal boundary explicit.
