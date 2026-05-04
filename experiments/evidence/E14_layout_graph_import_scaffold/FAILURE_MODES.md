# FAILURE_MODES - E14 Layout Graph Import Scaffold

## Known Limitations

1. **No real CAD import**: The layout schema is simplified JSON, not real Gerber/GDS/OASIS/BRL-CAD.
2. **No real conductor physics**: Resistance proxy is crude (R = L / (sigma * W * t)). No skin effect, no inductance, no capacitance.
3. **No routing import**: Does not parse actual CAD routing files; schema is hand-authored.
4. **No external solver validation**: No COMSOL/FastHenry/FEM comparison.
5. **Hypothesis candidates are scripted**: H0-H3 modifications are hardcoded, not derived from real defect distributions.
6. **KCL proxy is not a real circuit solve**: Currents are `1/R`, not from nodal analysis.
7. **No frequency dependence**: DC-like resistance only.

## Mitigations

- Gates ensure the scaffold passes all structural checks.
- Expanded in a future E## with real CAD parsing.
