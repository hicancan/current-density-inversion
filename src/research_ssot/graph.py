from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


CLAIM_STATUSES = {
    "proposed",
    "active",
    "supported",
    "supported_generated",
    "limited",
    "contradicted",
    "blocked",
    "retired",
}

EVIDENCE_STATUSES = {"planned", "running", "passed", "failed", "partial", "obsolete"}
EDGE_RELATIONS = {"supports", "limits", "contradicts", "requires", "motivates"}
EDGE_STRENGTHS = {"weak", "medium", "strong"}
NODE_TYPES = {
    "claim",
    "data_distribution",
    "physics_constraint",
    "forward_solver",
    "observation_model",
    "representation",
    "algorithm",
    "protocol",
    "metric",
    "external_resource",
}


@dataclass(frozen=True)
class GraphIssue:
    severity: str
    location: str
    message: str


@dataclass(frozen=True)
class ResearchGraph:
    root: Path
    claims: dict[str, dict[str, Any]]
    nodes: dict[str, dict[str, Any]]
    experiments: dict[str, dict[str, Any]]
    evidence_edges: list[dict[str, Any]]

    @property
    def graph_dir(self) -> Path:
        return self.root / "research_graph"


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    return data


def load_graph(root: Path | str) -> ResearchGraph:
    repo = Path(root).resolve()
    graph_dir = repo / "research_graph"
    return ResearchGraph(
        root=repo,
        claims=_read_yaml(graph_dir / "claims.yml"),
        nodes=_read_yaml(graph_dir / "nodes.yml"),
        experiments=_read_yaml(graph_dir / "experiments.yml"),
        evidence_edges=_read_yaml(graph_dir / "evidence_edges.yml"),
    )


def validate_graph(graph: ResearchGraph) -> list[GraphIssue]:
    issues: list[GraphIssue] = []

    def error(location: str, message: str) -> None:
        issues.append(GraphIssue("error", location, message))

    def warn(location: str, message: str) -> None:
        issues.append(GraphIssue("warning", location, message))

    for required in [
        "README.md",
        "claims.yml",
        "nodes.yml",
        "experiments.yml",
        "evidence_edges.yml",
        "open_questions.md",
        "overclaim_guardrails.md",
        "update_log.md",
    ]:
        if not (graph.graph_dir / required).exists():
            error(f"research_graph/{required}", "required SSOT file is missing")

    for node_id, node in graph.nodes.items():
        node_type = node.get("type")
        if node_type not in NODE_TYPES:
            error(f"nodes.yml:{node_id}", f"unknown node type {node_type!r}")

    evidence_ids = set(graph.experiments)
    claim_ids = set(graph.claims)
    node_ids = set(graph.nodes)

    for claim_id, claim in graph.claims.items():
        status = claim.get("status")
        if status not in CLAIM_STATUSES:
            error(f"claims.yml:{claim_id}", f"unknown claim status {status!r}")
        if not claim.get("title"):
            error(f"claims.yml:{claim_id}", "claim title is required")
        if status in {"supported", "supported_generated", "limited"} and not claim.get("supported_by"):
            warn(f"claims.yml:{claim_id}", "supported or limited claim has no supporting evidence")
        if status == "supported_generated" and not claim.get("cannot_claim"):
            error(f"claims.yml:{claim_id}", "generated-domain claim must define cannot_claim boundaries")

        for field in ["supported_by", "limited_by", "contradicted_by"]:
            for evidence_id in claim.get(field, []):
                if evidence_id not in evidence_ids:
                    error(f"claims.yml:{claim_id}.{field}", f"unknown evidence {evidence_id}")

        scope = claim.get("scope", {})
        for scope_name, values in scope.items():
            for node_ref in values or []:
                if node_ref not in node_ids:
                    error(f"claims.yml:{claim_id}.scope.{scope_name}", f"unknown node {node_ref}")

    experiment_node_fields = [
        "data",
        "physics",
        "forward",
        "observation",
        "representation",
        "algorithm",
        "protocol",
        "metrics",
    ]
    for evidence_id, evidence in graph.experiments.items():
        claim = evidence.get("claim")
        if claim not in claim_ids:
            error(f"experiments.yml:{evidence_id}.claim", f"unknown claim {claim}")
        for secondary in evidence.get("secondary_claims", []) or []:
            if secondary not in claim_ids:
                error(f"experiments.yml:{evidence_id}.secondary_claims", f"unknown claim {secondary}")
        status = evidence.get("status")
        if status not in EVIDENCE_STATUSES:
            error(f"experiments.yml:{evidence_id}", f"unknown evidence status {status!r}")
        if not evidence.get("result_summary"):
            warn(f"experiments.yml:{evidence_id}", "result_summary is empty")

        for field in experiment_node_fields:
            for node_ref in evidence.get(field, []) or []:
                if node_ref not in node_ids:
                    error(f"experiments.yml:{evidence_id}.{field}", f"unknown node {node_ref}")

        for output in evidence.get("outputs", []) or []:
            output_path = graph.root / output
            if not output_path.exists():
                error(f"experiments.yml:{evidence_id}.outputs", f"missing output file {output}")

    edge_ids: set[str] = set()
    for index, edge in enumerate(graph.evidence_edges):
        location = f"evidence_edges.yml[{index}]"
        edge_id = edge.get("id")
        if not edge_id:
            error(location, "edge id is required")
        elif edge_id in edge_ids:
            error(location, f"duplicate edge id {edge_id}")
        else:
            edge_ids.add(edge_id)

        if edge.get("from") not in evidence_ids:
            error(location, f"unknown evidence {edge.get('from')}")
        if edge.get("to") not in claim_ids:
            error(location, f"unknown claim {edge.get('to')}")
        if edge.get("relation") not in EDGE_RELATIONS:
            error(location, f"unknown relation {edge.get('relation')!r}")
        if edge.get("strength") not in EDGE_STRENGTHS:
            error(location, f"unknown strength {edge.get('strength')!r}")
        if not edge.get("scope"):
            warn(location, "edge scope is empty")
        if not edge.get("caveat"):
            warn(location, "edge caveat is empty")
        for evidence_file in edge.get("evidence_files", []) or []:
            if not (graph.root / evidence_file).exists():
                error(location, f"missing evidence file {evidence_file}")

    edge_targets = {edge.get("to") for edge in graph.evidence_edges}
    for claim_id, claim in graph.claims.items():
        if claim.get("supported_by") and claim_id not in edge_targets:
            warn(f"claims.yml:{claim_id}", "claim has supported_by but no incoming evidence edge")

    return issues


def claim_matrix_markdown(graph: ResearchGraph) -> str:
    rows = [
        "# Claim Matrix",
        "",
        "| Claim | Status | Supported by | Cannot claim | Next required evidence |",
        "|---|---|---|---|---|",
    ]
    for claim_id, claim in graph.claims.items():
        supported_by = ", ".join(claim.get("supported_by", []) or []) or "-"
        cannot_claim = "<br>".join(claim.get("cannot_claim", []) or []) or "-"
        next_evidence = "<br>".join(claim.get("next_required_evidence", []) or []) or "-"
        rows.append(
            f"| `{claim_id}` | `{claim.get('status')}` | {supported_by} | {cannot_claim} | {next_evidence} |"
        )
    rows.append("")
    return "\n".join(rows)


def evidence_edge_table_markdown(graph: ResearchGraph) -> str:
    rows = [
        "# Evidence Edge Table",
        "",
        "| Evidence | Relation | Claim | Strength | Scope | Caveat |",
        "|---|---|---|---|---|---|",
    ]
    for edge in graph.evidence_edges:
        rows.append(
            "| `{from_id}` | `{relation}` | `{to_id}` | `{strength}` | {scope} | {caveat} |".format(
                from_id=edge.get("from"),
                relation=edge.get("relation"),
                to_id=edge.get("to"),
                strength=edge.get("strength"),
                scope=edge.get("scope"),
                caveat=edge.get("caveat"),
            )
        )
    rows.append("")
    return "\n".join(rows)

