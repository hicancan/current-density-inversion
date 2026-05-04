.PHONY: sync validate gates metrics leakage outputs coverage normalize test test-direct evidence-test evidence-smoke evidence-run audit

sync:
	uv sync

validate:
	uv run python scripts/validate_graph.py

gates:
	uv run python scripts/check_claim_gates.py

metrics:
	uv run python scripts/check_metrics_schema.py

leakage:
	uv run python scripts/check_no_leakage.py

outputs:
	uv run python scripts/check_evidence_outputs.py

coverage:
	uv run python scripts/audit_old_new_experiment_coverage.py

normalize:
	uv run python scripts/normalize_metrics_metadata.py

test:
	uv run python -m pytest -q

test-direct:
	uv run pytest -q

evidence-test:
	uv run python scripts/run_evidence.py --all --mode test --continue-on-fail

evidence-smoke:
	uv run python scripts/run_evidence.py --all --mode smoke --continue-on-fail

evidence-run:
	uv run python scripts/run_evidence.py --all --mode run --continue-on-fail

audit: validate gates metrics leakage outputs coverage test
