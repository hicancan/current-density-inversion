# Prompt for opencode / Codex

You are working in `experiments/evidence/E19_obghi_minimal_observable_topology_posterior`.

Follow repository `AGENTS.md` strictly.

## Goal

Run and debug E19 OBGHI minimal observable topology posterior evidence. Do not
upgrade claims until metrics are audited.

## Commands

```bash
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Expected outputs

- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `outputs/POSTERIOR_TABLE.md`
- `outputs/FAILURE_CASES.md`
- `outputs/ACCEPTANCE_GATES.md`

## Fixing rules

- Keep the package CPU-only.
- Do not hard-code CUDA.
- Do not import project-private code unless needed.
- Preserve generated-domain cannot-claim boundaries.
- If acceptance gates fail, keep failure modes and update `RUN_REPORT.md`; do not hide failures.
- Do not change `claims.yml` status from unrun code.
- If registering E19 into the graph, first inspect `outputs/metrics.json` and then adapt `research_graph_patch/E19_research_graph_snippets.md`.

## Specific debugging priorities

1. Ensure via forward columns are nonzero.
2. Ensure H1/H2/H3 posterior probabilities differ on generated families.
3. Ensure accept/reject/need-next-measurement decisions are present.
4. Compare OBGHI top1/accepted risk against ridge-map baseline.
5. Preserve failures as evidence boundaries rather than overfitting gates.
