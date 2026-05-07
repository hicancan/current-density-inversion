# E23 Per-Layout H1/H2 Audit

## Hard-Case Summary
- Hardcase: four_layer_pdn_layout.json (gain=0.673286)
- Min H1/H2 (1s1h): 0.006987
- Min H1/H2 (multi-state): 0.680306
- Min gain: 0.673286
- WA any (1s1h): True
- WA any (ms): False

## Per-Layout Table
| Layout | d(1s1h) min | d(ms) min | Gain min | WA(1s1h) | WA(ms) | PF states |
|--------|------------|-----------|----------|----------|--------|-----------|
| simple_two_layer_layout.json | 0.154351 | 0.154352 | 0.000000 | False | False | 4 |
| four_layer_pdn_layout.json | 0.006987 | 0.680306 | 0.673286 | True | False | 4 |