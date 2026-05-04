from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_FILES = {
    "claim": "claim.schema.json",
    "node": "node.schema.json",
    "experiment": "experiment.schema.json",
    "edge": "edge.schema.json",
    "artifact": "artifact.schema.json",
    "agent_queue": "agent_queue.schema.json",
}


def load_schema(root: Path | str, name: str) -> dict[str, Any]:
    repo = Path(root).resolve()
    try:
        filename = SCHEMA_FILES[name]
    except KeyError as exc:
        raise KeyError(f"unknown schema name: {name}") from exc
    return json.loads((repo / "research_graph" / "schemas" / filename).read_text(encoding="utf-8"))


def validate_required_fields(payload: dict[str, Any], required: list[str]) -> list[str]:
    return [field for field in required if field not in payload]


def schema_required_fields(schema: dict[str, Any]) -> list[str]:
    required = schema.get("required", [])
    return list(required) if isinstance(required, list) else []


def validate_against_local_schema(payload: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    missing = validate_required_fields(payload, schema_required_fields(schema))
    return [f"missing required field: {field}" for field in missing]

