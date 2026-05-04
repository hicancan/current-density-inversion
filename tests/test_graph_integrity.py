from pathlib import Path

from research_ssot import ResearchGraph, load_graph, metrics_gate_status, next_agent_tasks, validate_graph


ROOT = Path(__file__).resolve().parents[1]


def test_research_graph_has_no_validation_errors() -> None:
    graph = load_graph(ROOT)
    issues = validate_graph(graph)
    errors = [issue for issue in issues if issue.severity == "error"]
    assert errors == []


def test_all_supported_generated_claims_have_boundaries() -> None:
    graph = load_graph(ROOT)
    for claim_id, claim in graph.claims.items():
        if claim["status"] == "supported_generated":
            assert claim["cannot_claim"], claim_id
            assert claim["limitations"], claim_id


def test_real_validation_claim_is_blocked() -> None:
    graph = load_graph(ROOT)
    claim = graph.claims["C12_real_qdm_nv_validation"]
    assert claim["status"] == "blocked"
    assert any("real data has been validated" in item for item in claim["cannot_claim"])


def test_pdn_kcl_node_has_generated_prototype_boundary() -> None:
    graph = load_graph(ROOT)
    claim = graph.claims["C10_pdn_kcl_distribution_need"]
    node = graph.nodes["D08_pdn_kcl_circuit_graph"]
    chip_like_node = graph.nodes["D11_chip_like_generated_pdn_family"]
    assert claim["status"] == "supported_generated"
    assert node["status"] == "partial"
    assert chip_like_node["status"] == "implemented"
    assert "E10_pdn_kcl_distribution" in claim["supported_by"]
    assert "E11_chip_like_pdn_distribution" in claim["supported_by"]
    assert "E12_pdn_physics_learning" in claim["supported_by"]
    assert "M04_kcl_residual" in node["required_metrics"]
    assert any("real CAD/Gerber/GDS validation" in item for item in claim["cannot_claim"])


def test_registered_runtime_packages_exist() -> None:
    graph = load_graph(ROOT)
    for evidence_id, evidence in graph.experiments.items():
        runtime = evidence.get("runtime")
        if runtime:
            package_dir = ROOT / runtime["package_dir"]
            assert package_dir.exists(), evidence_id
            assert (package_dir / "requirements.txt").exists() or (package_dir / "pyproject.toml").exists()
            if evidence["status"] not in {"planned", "blocked", "blocked_by_dependency", "obsolete"}:
                assert (package_dir / "outputs" / "metrics.json").exists(), evidence_id
                assert (package_dir / "outputs" / "RUN_REPORT.md").exists(), evidence_id


def test_agent_queue_keeps_pdn_external_bridge_first_after_generated_closure() -> None:
    graph = load_graph(ROOT)
    task = next_agent_tasks(graph)[0]
    assert task["affected_claim"] == "C10_pdn_kcl_distribution_need"
    assert task["id"] == "AQ04_external_pdn_layout_bridge"
    assert task["status"] == "blocked"


def test_e10_metrics_gate_passes() -> None:
    path = ROOT / "experiments/evidence/E10_pdn_kcl_distribution/outputs/metrics.json"
    status = metrics_gate_status(path)
    assert status.ok
    assert status.gate == "all_acceptance_gates_passed"


def test_e11_e12_metrics_gates_pass() -> None:
    for rel_path in [
        "experiments/evidence/E11_chip_like_pdn_distribution/outputs/metrics.json",
        "experiments/evidence/E12_pdn_physics_learning/outputs/metrics.json",
    ]:
        status = metrics_gate_status(ROOT / rel_path)
        assert status.ok, rel_path
        assert status.gate == "all_acceptance_gates_passed"


def test_all_registered_metrics_have_schema_and_leakage_audit() -> None:
    graph = load_graph(ROOT)
    import json

    for evidence_id, evidence in graph.experiments.items():
        for rel_path in (evidence.get("runtime") or {}).get("metrics_files", []) or []:
            data = json.loads((ROOT / rel_path).read_text(encoding="utf-8"))
            assert data["schema_version"] == "research-ssot-metrics-v1", evidence_id
            assert isinstance(data["leakage_audit"], dict), evidence_id


def test_e09_is_interface_only_and_c12_remains_blocked() -> None:
    graph = load_graph(ROOT)
    evidence = graph.experiments["E09_real_data_intake_gate"]
    claim = graph.claims["C12_real_qdm_nv_validation"]
    assert evidence["status"] == "passed_interface"
    assert claim["status"] == "blocked"
    status = metrics_gate_status(ROOT / "experiments/evidence/E09_real_data_intake_gate/outputs/metrics.json")
    assert status.ok


def test_missing_artifact_path_is_validation_error() -> None:
    graph = load_graph(ROOT)
    broken_artifacts = list(graph.artifacts)
    broken = dict(broken_artifacts[0])
    broken["id"] = "artifact_missing_path_test"
    broken["path"] = "missing/artifact.txt"
    broken_artifacts.append(broken)
    broken_graph = ResearchGraph(
        root=graph.root,
        claims=graph.claims,
        nodes=graph.nodes,
        experiments=graph.experiments,
        evidence_edges=graph.evidence_edges,
        artifacts=broken_artifacts,
        agent_queue=graph.agent_queue,
    )
    issues = validate_graph(broken_graph)
    assert any(issue.severity == "error" and "artifact path is missing" in issue.message for issue in issues)
