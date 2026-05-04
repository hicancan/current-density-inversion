# Reproduction

`ash
cd experiments/evidence/E15_four_layer_via_chain_benchmark
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
`
