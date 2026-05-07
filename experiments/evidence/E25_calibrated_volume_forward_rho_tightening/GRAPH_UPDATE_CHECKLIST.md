# Graph Update Checklist

- Register `E25_calibrated_volume_forward_rho_tightening` in `research_graph/experiments.yml`.
- Add evidence edge(s) in `research_graph/evidence_edges.yml`.
- Update claims C04, C10, C13 only if evidence changes status or boundaries.
- Register outputs in `research_graph/artifacts.yml` when generated.
- Run `uv run python scripts/validate_graph.py`.
