# Reproduce E09

## Smoke

```powershell
uv run --with-requirements requirements.txt python src/validate_real_case_metadata.py examples/example_case_template.json
```

## Tests

```powershell
uv run --with-requirements requirements.txt --with pytest pytest -q tests
```

## Boundary

This package is a real-data intake scaffold. It does not include measured
QDM/NV rows and therefore does not produce claim-supporting metrics yet.

