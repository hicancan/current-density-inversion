from __future__ import annotations

import argparse
import sys

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Print a conservative evidence YAML stub.")
    parser.add_argument("evidence_id")
    parser.add_argument("--claim", required=True)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    stub = {
        args.evidence_id: {
            "title": args.title,
            "claim": args.claim,
            "secondary_claims": [],
            "data": [],
            "physics": [],
            "forward": [],
            "observation": [],
            "representation": [],
            "algorithm": [],
            "protocol": [],
            "metrics": [],
            "outputs": [],
            "runtime": {
                "package_dir": args.package_dir,
                "run_command": "uv run --with-requirements requirements.txt python src/run_all.py",
                "smoke_command": "uv run --with-requirements requirements.txt python src/run_all.py --smoke",
                "test_command": "uv run --with-requirements requirements.txt --with pytest pytest -q tests",
                "metrics_files": [f"{args.package_dir}/outputs/metrics.json"],
            },
            "result_summary": "Planned evidence package; no claim upgrade until metrics and RUN_REPORT are non-empty.",
            "status": "planned",
            "last_run": None,
        }
    }
    yaml.safe_dump(stub, sys.stdout, sort_keys=False, allow_unicode=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

