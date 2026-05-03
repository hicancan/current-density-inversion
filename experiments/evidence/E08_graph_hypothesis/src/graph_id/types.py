from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Tuple

import numpy as np


ArrayLike3 = Tuple[float, float, float]


@dataclass(frozen=True)
class Segment:
    """A directed current segment used as a graph-current basis element.

    Coordinates are in meters. Current amplitudes are solved separately by the
    identification algorithms; the segment itself only defines geometry and type.
    """

    name: str
    layer: str
    kind: str
    start: ArrayLike3
    end: ArrayLike3
    prior_group: str = "sheet"

    def length(self) -> float:
        return float(np.linalg.norm(np.asarray(self.end, dtype=float) - np.asarray(self.start, dtype=float)))

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CaseRecord:
    """A generated magnetic-system-identification sample."""

    case_id: str
    split: str
    class_label: str
    hypothesis_label: str
    b_clean: np.ndarray
    b_obs: np.ndarray
    sheet_segments: List[Segment]
    via_candidates: List[Segment]
    return_candidates: List[Segment]
    artifact_candidates: List[Segment]
    truth_currents: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def graph_json(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "split": self.split,
            "class_label": self.class_label,
            "hypothesis_label": self.hypothesis_label,
            "sheet_segments": [s.to_json() for s in self.sheet_segments],
            "via_candidates": [s.to_json() for s in self.via_candidates],
            "return_candidates": [s.to_json() for s in self.return_candidates],
            "artifact_candidates": [s.to_json() for s in self.artifact_candidates],
            "truth_currents": dict(self.truth_currents),
            "metadata": dict(self.metadata),
        }


@dataclass
class HypothesisResult:
    """Ridge fit and evidence score for a single graph hypothesis."""

    name: str
    score: float
    residual_rel_l2: float
    coefficients: Dict[str, float]
    n_basis: int
    n_extra_basis: int
    residual_norm: float
    complexity_penalty: float
    l1_penalty: float

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)
