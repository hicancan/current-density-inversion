from pathlib import Path

from research_ssot import load_graph, validate_graph


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


def test_pdn_kcl_node_is_high_priority_missing_node() -> None:
    graph = load_graph(ROOT)
    claim = graph.claims["C10_pdn_kcl_distribution_need"]
    node = graph.nodes["D08_pdn_kcl_circuit_graph"]
    assert claim["status"] == "active"
    assert node["status"] == "missing"
    assert "M04_kcl_residual" in node["required_metrics"]

