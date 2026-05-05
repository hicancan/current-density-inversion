from __future__ import annotations

from dataclasses import dataclass
import json
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
EVIDENCE_STATUSES = {
    "planned",
    "running",
    "passed",
    "passed_scaffold",
    "passed_interface",
    "failed",
    "partial",
    "blocked",
    "blocked_by_dependency",
    "obsolete",
}
EDGE_RELATIONS = {"supports", "limits", "contradicts", "requires", "motivates"}
EDGE_STRENGTHS = {"weak", "medium", "strong"}
ARTIFACT_KINDS = {"generated", "external", "raw", "metrics", "report", "figure", "protocol", "schema"}
ARTIFACT_ROLES = {
    "generated",
    "external",
    "raw",
    "metrics",
    "report",
    "figure",
    "protocol",
    "scaffold",
    "calibration",
    "heldout",
    "hidden",
    "real",
}
QUEUE_STATUSES = {"proposed", "active", "blocked", "done", "obsolete"}
SCOPE_NODE_TYPES = {
    "data": "data_distribution",
    "physics": "physics_constraint",
    "forward": "forward_solver",
    "observation": "observation_model",
    "representation": "representation",
    "algorithm": "algorithm",
    "protocol": "protocol",
    "metrics": "metric",
}
STANDARD_EVIDENCE_FILES = {
    "README.md",
    "REPRODUCE.md",
    "METRICS_SCHEMA.md",
    "FAILURE_MODES.md",
}
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
class MetricsGateStatus:
    path: Path
    ok: bool
    gate: str
    message: str = ""


@dataclass(frozen=True)
class EvidencePackageInspection:
    evidence_id: str
    package_dir: Path
    exists: bool
    missing_standard_files: tuple[str, ...]
    has_config: bool
    has_tests: bool
    has_metrics: bool


@dataclass(frozen=True)
class ResearchGraph:
    root: Path
    claims: dict[str, dict[str, Any]]
    nodes: dict[str, dict[str, Any]]
    experiments: dict[str, dict[str, Any]]
    evidence_edges: list[dict[str, Any]]
    artifacts: list[dict[str, Any]]
    agent_queue: list[dict[str, Any]]

    @property
    def graph_dir(self) -> Path:
        return self.root / "research_graph"


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    return data


def _read_optional_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    data = _read_yaml(path)
    return default if data is None else data


def load_graph(root: Path | str) -> ResearchGraph:
    repo = Path(root).resolve()
    graph_dir = repo / "research_graph"
    return ResearchGraph(
        root=repo,
        claims=_read_yaml(graph_dir / "claims.yml"),
        nodes=_read_yaml(graph_dir / "nodes.yml"),
        experiments=_read_yaml(graph_dir / "experiments.yml"),
        evidence_edges=_read_yaml(graph_dir / "evidence_edges.yml"),
        artifacts=_read_optional_yaml(graph_dir / "artifacts.yml", []),
        agent_queue=_read_optional_yaml(graph_dir / "agent_queue.yml", []),
    )


def metrics_gate_status(path: Path | str) -> MetricsGateStatus:
    metrics_path = Path(path)
    if not metrics_path.exists():
        return MetricsGateStatus(metrics_path, False, "missing", "metrics file is missing")
    try:
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return MetricsGateStatus(metrics_path, False, "invalid_json", str(exc))
    if not isinstance(metrics, dict) or not metrics:
        return MetricsGateStatus(metrics_path, False, "empty_or_not_object", "metrics JSON must be a non-empty object")
    if "all_acceptance_gates_passed" in metrics:
        return MetricsGateStatus(metrics_path, bool(metrics["all_acceptance_gates_passed"]), "all_acceptance_gates_passed")
    gates = metrics.get("acceptance_gates")
    if isinstance(gates, dict) and "all_acceptance_gates_passed" in gates:
        return MetricsGateStatus(
            metrics_path,
            bool(gates["all_acceptance_gates_passed"]),
            "acceptance_gates.all_acceptance_gates_passed",
        )
    if isinstance(gates, dict) and "all_scientific_gates_passed" in gates:
        return MetricsGateStatus(
            metrics_path,
            bool(gates["all_scientific_gates_passed"]),
            "acceptance_gates.all_scientific_gates_passed",
        )
    if isinstance(gates, dict) and gates:
        bool_values = [value for value in gates.values() if isinstance(value, bool)]
        if bool_values:
            return MetricsGateStatus(metrics_path, all(bool_values), "all boolean acceptance_gates")
    return MetricsGateStatus(metrics_path, False, "no_recognized_gate", "no recognized gate field")


def inspect_evidence_packages(graph: ResearchGraph) -> list[EvidencePackageInspection]:
    inspections: list[EvidencePackageInspection] = []
    for evidence_id, evidence in graph.experiments.items():
        runtime = evidence.get("runtime") or {}
        package_dir_value = runtime.get("package_dir")
        if not package_dir_value:
            continue
        package_dir = graph.root / package_dir_value
        missing = tuple(sorted(name for name in STANDARD_EVIDENCE_FILES if not (package_dir / name).exists()))
        metrics_files = runtime.get("metrics_files") or []
        inspections.append(
            EvidencePackageInspection(
                evidence_id=evidence_id,
                package_dir=package_dir,
                exists=package_dir.exists(),
                missing_standard_files=missing,
                has_config=(package_dir / "configs" / "default.json").exists(),
                has_tests=(package_dir / "tests").exists(),
                has_metrics=bool(metrics_files) and all((graph.root / path).exists() for path in metrics_files),
            )
        )
    return inspections


def next_agent_tasks(graph: ResearchGraph) -> list[dict[str, Any]]:
    def sort_key(item: dict[str, Any]) -> tuple[int, str]:
        return int(item.get("priority", 9999)), str(item.get("id", ""))

    return sorted(
        [item for item in graph.agent_queue if item.get("status") in {"active", "proposed", "blocked"}],
        key=sort_key,
    )


def readiness_score(graph: ResearchGraph) -> tuple[int, list[str]]:
    issues = validate_graph(graph)
    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    inspections = inspect_evidence_packages(graph)
    standard_file_gaps = sum(len(item.missing_standard_files) for item in inspections)
    metrics_total = 0
    metrics_ok = 0
    for evidence in graph.experiments.values():
        for rel_path in (evidence.get("runtime") or {}).get("metrics_files", []) or []:
            metrics_total += 1
            if metrics_gate_status(graph.root / rel_path).ok:
                metrics_ok += 1

    score = 100
    score -= min(60, len(errors) * 20)
    score -= min(20, len(warnings) * 2)
    score -= min(15, standard_file_gaps)
    if not next_agent_tasks(graph):
        score -= 10
    if metrics_total and metrics_ok < metrics_total:
        score -= min(20, (metrics_total - metrics_ok) * 5)

    notes = [
        f"errors={len(errors)} warnings={len(warnings)}",
        f"standard_file_gaps={standard_file_gaps}",
        f"metrics_gates={metrics_ok}/{metrics_total}",
        f"agent_queue_ready={bool(next_agent_tasks(graph))}",
    ]
    return max(score, 0), notes


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
        "artifacts.yml",
        "agent_queue.yml",
        "open_questions.md",
        "overclaim_guardrails.md",
        "update_log.md",
    ]:
        if not (graph.graph_dir / required).exists():
            error(f"research_graph/{required}", "required SSOT file is missing")

    for schema_name in [
        "claim.schema.json",
        "node.schema.json",
        "experiment.schema.json",
        "edge.schema.json",
        "artifact.schema.json",
        "agent_queue.schema.json",
    ]:
        if not (graph.graph_dir / "schemas" / schema_name).exists():
            error(f"research_graph/schemas/{schema_name}", "required schema file is missing")

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
        if status == "supported_generated" and not claim.get("limitations"):
            error(f"claims.yml:{claim_id}", "generated-domain claim must define limitations")
        if status in {"supported", "supported_generated", "limited"} and not claim.get("next_required_evidence"):
            warn(f"claims.yml:{claim_id}", "claim has no next_required_evidence")

        for field in ["supported_by", "limited_by", "contradicted_by"]:
            for evidence_id in claim.get(field, []):
                if evidence_id not in evidence_ids:
                    error(f"claims.yml:{claim_id}.{field}", f"unknown evidence {evidence_id}")

        scope = claim.get("scope", {})
        for scope_name, values in scope.items():
            expected_type = SCOPE_NODE_TYPES.get(scope_name)
            for node_ref in values or []:
                if node_ref not in node_ids:
                    error(f"claims.yml:{claim_id}.scope.{scope_name}", f"unknown node {node_ref}")
                elif expected_type and graph.nodes[node_ref].get("type") != expected_type:
                    error(
                        f"claims.yml:{claim_id}.scope.{scope_name}",
                        f"node {node_ref} has type {graph.nodes[node_ref].get('type')!r}, expected {expected_type!r}",
                    )

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
            expected_type = SCOPE_NODE_TYPES[field]
            for node_ref in evidence.get(field, []) or []:
                if node_ref not in node_ids:
                    error(f"experiments.yml:{evidence_id}.{field}", f"unknown node {node_ref}")
                elif graph.nodes[node_ref].get("type") != expected_type:
                    error(
                        f"experiments.yml:{evidence_id}.{field}",
                        f"node {node_ref} has type {graph.nodes[node_ref].get('type')!r}, expected {expected_type!r}",
                    )

        for output in evidence.get("outputs", []) or []:
            output_path = graph.root / output
            if not output_path.exists():
                error(f"experiments.yml:{evidence_id}.outputs", f"missing output file {output}")

        runtime = evidence.get("runtime") or {}
        package_dir_value = runtime.get("package_dir")
        if package_dir_value:
            package_dir = graph.root / package_dir_value
            if not package_dir.exists():
                error(f"experiments.yml:{evidence_id}.runtime.package_dir", "runtime package is missing")
            else:
                for standard_file in sorted(STANDARD_EVIDENCE_FILES):
                    if not (package_dir / standard_file).exists():
                        warn(
                            f"experiments.yml:{evidence_id}.runtime.package_dir",
                            f"runtime package missing standard file {standard_file}",
                        )
                if status != "planned" and not (package_dir / "configs" / "default.json").exists():
                    warn(f"experiments.yml:{evidence_id}.runtime.package_dir", "runtime package missing configs/default.json")
                if not (package_dir / "tests").exists():
                    warn(f"experiments.yml:{evidence_id}.runtime.package_dir", "runtime package missing tests directory")
        metrics_files = runtime.get("metrics_files") or []
        report_path = package_dir / "outputs" / "RUN_REPORT.md" if package_dir_value else None
        metrics_path = package_dir / "outputs" / "metrics.json" if package_dir_value else None
        if package_dir_value and status not in {"planned", "blocked", "blocked_by_dependency", "obsolete"}:
            if not (package_dir / "requirements.txt").exists() and not (package_dir / "pyproject.toml").exists():
                error(f"experiments.yml:{evidence_id}.runtime.package_dir", "runtime package missing requirements.txt or pyproject.toml")
            if not report_path or not report_path.exists():
                error(f"experiments.yml:{evidence_id}.runtime.package_dir", "runtime package missing outputs/RUN_REPORT.md")
            if not metrics_path or not metrics_path.exists():
                error(f"experiments.yml:{evidence_id}.runtime.package_dir", "runtime package missing outputs/metrics.json")
        if status not in {"planned", "blocked", "blocked_by_dependency", "obsolete"} and not metrics_files:
            error(f"experiments.yml:{evidence_id}.runtime.metrics_files", "non-planned evidence has no metrics_files")
        for rel_path in metrics_files:
            status_info = metrics_gate_status(graph.root / rel_path)
            if not status_info.ok:
                if status == "partial":
                    warn(
                        f"experiments.yml:{evidence_id}.runtime.metrics_files",
                        f"metrics gate failed for {rel_path}: {status_info.gate} {status_info.message} (expected for partial evidence)".strip(),
                    )
                else:
                    error(
                        f"experiments.yml:{evidence_id}.runtime.metrics_files",
                        f"metrics gate failed for {rel_path}: {status_info.gate} {status_info.message}".strip(),
                    )

    edge_ids: set[str] = set()
    edge_evidence_files = {
        evidence_file
        for edge in graph.evidence_edges
        for evidence_file in (edge.get("evidence_files", []) or [])
    }
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

    for evidence_id, evidence in graph.experiments.items():
        for output in evidence.get("outputs", []) or []:
            if output not in edge_evidence_files:
                warn(f"experiments.yml:{evidence_id}.outputs", f"output {output} is not referenced by an evidence edge")

    edge_targets = {edge.get("to") for edge in graph.evidence_edges}
    for claim_id, claim in graph.claims.items():
        if claim.get("supported_by") and claim_id not in edge_targets:
            warn(f"claims.yml:{claim_id}", "claim has supported_by but no incoming evidence edge")

    _validate_claim_edge_consistency(graph, error, warn)

    _validate_artifacts(graph, claim_ids, evidence_ids, error)
    _validate_agent_queue(graph, claim_ids, node_ids, evidence_ids, error, warn)

    return issues


def _validate_claim_edge_consistency(graph: ResearchGraph, error: Any, warn: Any) -> None:
    incoming = {}
    for edge in graph.evidence_edges:
        incoming.setdefault((edge.get("from"), edge.get("to")), set()).add(edge.get("relation"))

    for claim_id, claim in graph.claims.items():
        status = claim.get("status")
        for evidence_id in claim.get("supported_by", []) or []:
            relations = incoming.get((evidence_id, claim_id), set())
            if not relations:
                error(f"claims.yml:{claim_id}.supported_by", f"{evidence_id} has no evidence edge to claim")
        for evidence_id in claim.get("limited_by", []) or []:
            relations = incoming.get((evidence_id, claim_id), set())
            if "limits" not in relations:
                error(f"claims.yml:{claim_id}.limited_by", f"{evidence_id} must have a limits edge to claim")
        for evidence_id in claim.get("contradicted_by", []) or []:
            relations = incoming.get((evidence_id, claim_id), set())
            if "contradicts" not in relations:
                error(f"claims.yml:{claim_id}.contradicted_by", f"{evidence_id} must have a contradicts edge to claim")

        real_scope = set((claim.get("scope") or {}).get("data", []) or []) | set((claim.get("scope") or {}).get("forward", []) or [])
        if status in {"supported", "supported_generated"} and {"D10_real_qdm_nv", "F07_real_measurement"} & real_scope:
            error(
                f"claims.yml:{claim_id}",
                "real-measurement validation claim cannot be supported without measured rows and real-data gates",
            )
        if status == "supported" and any("generated" in str(item).lower() for item in claim.get("limitations", []) or []):
            warn(f"claims.yml:{claim_id}", "supported claim still carries generated-domain limitation text")


def _validate_artifacts(
    graph: ResearchGraph,
    claim_ids: set[str],
    evidence_ids: set[str],
    error: Any,
) -> None:
    artifact_ids: set[str] = set()
    if not isinstance(graph.artifacts, list):
        error("artifacts.yml", "artifacts root must be a list")
        return
    for index, artifact in enumerate(graph.artifacts):
        location = f"artifacts.yml[{index}]"
        artifact_id = artifact.get("id")
        if not artifact_id:
            error(location, "artifact id is required")
        elif artifact_id in artifact_ids:
            error(location, f"duplicate artifact id {artifact_id}")
        else:
            artifact_ids.add(artifact_id)
        if artifact.get("kind") not in ARTIFACT_KINDS:
            error(location, f"unknown artifact kind {artifact.get('kind')!r}")
        if artifact.get("role") not in ARTIFACT_ROLES:
            error(location, f"unknown artifact role {artifact.get('role')!r}")
        if artifact.get("claim") not in claim_ids:
            error(location, f"unknown claim {artifact.get('claim')}")
        evidence_ref = artifact.get("evidence")
        if evidence_ref and evidence_ref not in evidence_ids:
            error(location, f"unknown evidence {evidence_ref}")
        artifact_path = artifact.get("path")
        if not artifact_path:
            error(location, "artifact path is required")
        elif not (graph.root / artifact_path).exists():
            error(location, f"artifact path is missing: {artifact_path}")
        if "calibration_allowed" not in artifact:
            error(location, "calibration_allowed is required")
        if "tracked" not in artifact:
            error(location, "tracked is required")


def _validate_agent_queue(
    graph: ResearchGraph,
    claim_ids: set[str],
    node_ids: set[str],
    evidence_ids: set[str],
    error: Any,
    warn: Any,
) -> None:
    if not isinstance(graph.agent_queue, list):
        error("agent_queue.yml", "agent_queue root must be a list")
        return
    queue_ids: set[str] = set()
    for index, item in enumerate(graph.agent_queue):
        location = f"agent_queue.yml[{index}]"
        queue_id = item.get("id")
        if not queue_id:
            error(location, "queue id is required")
        elif queue_id in queue_ids:
            error(location, f"duplicate queue id {queue_id}")
        else:
            queue_ids.add(queue_id)
        if item.get("status") not in QUEUE_STATUSES:
            error(location, f"unknown queue status {item.get('status')!r}")
        if item.get("affected_claim") not in claim_ids:
            error(location, f"unknown affected claim {item.get('affected_claim')}")
        evidence_ref = item.get("recommended_evidence_id")
        if evidence_ref and evidence_ref not in evidence_ids:
            error(location, f"unknown recommended evidence {evidence_ref}")
        for node_ref in item.get("required_nodes", []) or []:
            if node_ref not in node_ids:
                error(location, f"unknown required node {node_ref}")
        if not item.get("acceptance_gates"):
            warn(location, "queue item has no acceptance_gates")
        if not item.get("cannot_claim"):
            warn(location, "queue item has no cannot_claim boundaries")


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
