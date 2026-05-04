from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


ClaimStatus = Literal[
    "proposed",
    "active",
    "supported",
    "supported_generated",
    "limited",
    "contradicted",
    "blocked",
    "retired",
]

EvidenceStatus = Literal[
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
]

EvidenceRelation = Literal["supports", "limits", "contradicts", "requires", "motivates"]


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    status: ClaimStatus
    supported_by: tuple[str, ...] = ()
    limited_by: tuple[str, ...] = ()
    contradicted_by: tuple[str, ...] = ()
    cannot_claim: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    claim: str
    status: EvidenceStatus
    package_dir: str | None = None
    metrics_files: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceEdgeRecord:
    edge_id: str
    source_evidence: str
    target_claim: str
    relation: EvidenceRelation
    strength: str
    evidence_files: tuple[str, ...] = ()


STATUS_TRANSITIONS: dict[str, set[str]] = {
    "proposed": {"active", "blocked", "retired"},
    "active": {"supported", "supported_generated", "limited", "blocked", "retired"},
    "supported_generated": {"limited", "supported", "blocked", "retired"},
    "supported": {"limited", "contradicted", "retired"},
    "limited": {"active", "supported_generated", "supported", "blocked", "retired"},
    "blocked": {"active", "limited", "retired"},
    "contradicted": {"limited", "retired"},
    "retired": set(),
}


def status_transition_allowed(old: str, new: str) -> bool:
    if old == new:
        return True
    return new in STATUS_TRANSITIONS.get(old, set())


def generated_claim_has_boundaries(claim: dict[str, Any]) -> bool:
    return bool(claim.get("cannot_claim")) and bool(claim.get("limitations"))

