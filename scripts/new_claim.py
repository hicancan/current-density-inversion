from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Print a conservative claim YAML stub.")
    parser.add_argument("claim_id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--status", default="proposed")
    args = parser.parse_args()

    stub = {
        args.claim_id: {
            "title": args.title,
            "short_name": args.claim_id.lower(),
            "status": args.status,
            "scope": {
                "data": [],
                "forward": [],
                "observation": [],
                "representation": [],
                "algorithm": [],
                "protocol": [],
                "metrics": [],
            },
            "supported_by": [],
            "limited_by": [],
            "contradicted_by": [],
            "cannot_claim": ["not yet evidenced"],
            "limitations": ["New claim stub; no evidence package has been run."],
            "next_required_evidence": ["Create a linked evidence package before opening a study."],
            "last_updated": "YYYY-MM-DD",
        }
    }
    yaml.safe_dump(stub, sys.stdout, sort_keys=False, allow_unicode=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

