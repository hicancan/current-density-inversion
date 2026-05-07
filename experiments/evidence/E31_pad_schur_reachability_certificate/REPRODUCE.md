# Reproduce E31

From the repository root:

```powershell
cd D:\code\github\hicancan\current-density-inversion\experiments\evidence\E31_pad_schur_reachability_certificate
uv run python src\run_all.py --config configs\default.json --out outputs
uv run python -m pytest -q tests
```

Smoke run:

```powershell
uv run python src\run_all.py --config configs\smoke.json --out outputs_smoke
```

E31 uses CPU-sized dense linear algebra and reuses E30/E28 generated-domain
operator code.

