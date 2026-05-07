# Reproduce E30

From the repository root:

```powershell
cd D:\code\github\hicancan\current-density-inversion\experiments\evidence\E30_dual_schur_active_defect_certificate
uv run python src\run_all.py --config configs\default.json --out outputs
uv run python -m pytest -q tests
```

Smoke run:

```powershell
uv run python src\run_all.py --config configs\smoke.json --out outputs_smoke
```

E30 is CPU-sized. It reuses E28's generated operator modules and does not use
real QDM/NV, CAD/GDS, PyPEEC, FastHenry, COMSOL, or external held-out rows.

