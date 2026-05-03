"""Graph-guided magnetic system identification for Exp08."""

from .types import Segment, CaseRecord, HypothesisResult
from .forward import make_observation_grid, field_from_segments, flatten_field
from .generator import generate_dataset
from .solver import score_hypotheses

__all__ = [
    "Segment",
    "CaseRecord",
    "HypothesisResult",
    "make_observation_grid",
    "field_from_segments",
    "flatten_field",
    "generate_dataset",
    "score_hypotheses",
]
