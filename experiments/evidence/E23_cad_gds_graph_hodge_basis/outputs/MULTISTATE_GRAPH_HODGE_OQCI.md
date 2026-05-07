# E23 Multi-State Graph-Hodge OQCI Report

## Excitation States
- baseline: VDD=1.0, GND=1.0 (nominal)
- via_sensitive: VDD=2.0, GND=1.0 (stress via paths)
- return_sensitive: VDD=1.0, GND=2.0 (stress return paths)
- differential: VDD=1.5, GND=0.5 (asymmetric)

## H1/H2 Distance per Protocol
| Protocol | H1/H2 Distance | Wrong Accepts |
|----------|---------------|---------------|
| 1s1h | 0.154353 | 2 |
| multi-state | 0.736487 | 2 |
| multi-state+multi-height | 0.710205 | 2 |

## Multi-State Efficacy
- H1/H2 improved (multi-state): True
- H1/H2 improved (ms+mh): True
- Wrong accepts reduced (multi-state): False
- Wrong accepts reduced (ms+mh): False
- H1/H2 >= 0.20 (multi-state): True
- H1/H2 >= 0.20 (ms+mh): True