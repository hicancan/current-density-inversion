"""Configuration loading and validation for E21 operator-gap ladder."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class GeometryConfig:
    name: str
    enabled: bool = True
    wire_half_length_um: float = 100.0
    loop_radius_um: float = 50.0
    wire_width_um: float = 20.0
    via_height_um: float = 50.0
    via_radius_um: float = 5.0
    layer1_z_um: float = 25.0
    layer2_z_um: float = -25.0
    ground_z_um: float = -75.0
    return_spacing_um: float = 80.0
    n_segments_per_route: int = 3


@dataclass
class GridConfig:
    n: int = 48
    fov_um: float = 200.0
    measurement_z_um: float = 50.0


@dataclass
class OperatorConfig:
    name: str
    enabled: bool = True
    n_width_filaments: int = 5
    n_steps: int = 80
    return_scale: float = 0.8
    depth_shift_um: float = 3.0
    psf_sigma_px: float = 0.0
    noise_std_uT: float = 0.0


@dataclass
class DecisionConfig:
    inverse_method: str = "ridge"
    ridge_alpha: float = 1e-3
    n_train: int = 200
    n_test: int = 50
    current_max_mA: float = 10.0
    noise_std_uT: float = 0.1


@dataclass
class ExternalArtifactConfig:
    enabled: bool = True
    comsol_path: str = ""
    fasthenry_path: str = ""
    require_present: bool = False


@dataclass
class RunConfig:
    seed: int = 42
    case_count: int = 0
    geoms: List[GeometryConfig] = field(default_factory=list)
    grid: GridConfig = field(default_factory=GridConfig)
    operators: List[OperatorConfig] = field(default_factory=list)
    decision: DecisionConfig = field(default_factory=DecisionConfig)
    external_artifacts: ExternalArtifactConfig = field(
        default_factory=ExternalArtifactConfig
    )
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RunConfig":
        geoms = [GeometryConfig(**g) for g in d.get("geoms", [])]
        grid = GridConfig(**d.get("grid", {}))
        operators = [OperatorConfig(**o) for o in d.get("operators", [])]
        decision = DecisionConfig(**d.get("decision", {}))
        ext = ExternalArtifactConfig(**d.get("external_artifacts", {}))
        return cls(
            seed=int(d.get("seed", 42)),
            case_count=0,
            geoms=geoms,
            grid=grid,
            operators=operators,
            decision=decision,
            external_artifacts=ext,
            raw=d,
        )


def load_config(path: Path) -> RunConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return RunConfig.from_dict(raw)


def resolve_path(path_str: str, relative_to: Path = ROOT) -> Path:
    p = Path(path_str)
    if not p.is_absolute():
        p = relative_to / p
    return p.resolve()
