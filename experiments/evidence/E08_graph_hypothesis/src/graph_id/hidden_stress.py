from __future__ import annotations

from dataclasses import replace
from typing import List

import numpy as np

from .forward import field_from_segments, make_observation_grid
from .generator import _make_case
from .types import CaseRecord, Segment


def _with_extra_field(record: CaseRecord, cfg: dict, segment: Segment, current_a: float, family: str) -> CaseRecord:
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    extra = field_from_segments(
        [segment],
        {segment.name: current_a},
        obs_grid,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )
    metadata = dict(record.metadata)
    metadata.update(
        {
            "hidden_mechanism_family": family,
            "hidden_segment": segment.to_json(),
            "hidden_current_a": float(current_a),
            "claim_boundary": "Hidden mechanism is deliberately absent or mismatched in the scorer candidate library.",
        }
    )
    truth = dict(record.truth_currents)
    truth[segment.name] = float(current_a)
    return replace(
        record,
        split="hidden",
        case_id=f"hidden_{family}_{record.case_id}",
        b_clean=record.b_clean + extra,
        b_obs=record.b_obs + extra,
        truth_currents=truth,
        metadata=metadata,
    )


def _local_span(record: CaseRecord) -> tuple[float, float, float, float, float]:
    pts = []
    for group in [record.sheet_segments, record.via_candidates, record.return_candidates, record.artifact_candidates]:
        for seg in group:
            pts.append(seg.start)
            pts.append(seg.end)
    arr = np.asarray(pts, dtype=float)
    return (
        float(np.min(arr[:, 0])),
        float(np.max(arr[:, 0])),
        float(np.min(arr[:, 1])),
        float(np.max(arr[:, 1])),
        float(np.min(arr[:, 2])),
    )


def generate_hidden_mechanism_records(cfg: dict) -> List[CaseRecord]:
    """Generate OOD cases whose true field is not exactly in the hypothesis bank."""

    rng = np.random.default_rng(int(cfg["seed"]) + 808)
    out: List[CaseRecord] = []
    n_per_family = int(cfg.get("hidden_stress", {}).get("n_per_family", 24))
    fov = float(cfg["grid"]["fov_m"])
    for idx in range(n_per_family):
        # H0 label, but add a broad hidden return not in the candidate graph.
        base = _make_case(8000 + idx, "ood", "no_via", rng, cfg)
        x0, x1, y0, _, zmin = _local_span(base)
        hidden_return = Segment(
            name=f"hidden_return_{idx:03d}",
            layer="HIDDEN_RETURN",
            kind="return",
            start=(x1, y0 - 0.20 * fov, zmin - 90e-6),
            end=(x0, y0 - 0.20 * fov, zmin - 90e-6),
            prior_group="hidden",
        )
        scale = 0.45 * max(abs(v) for v in base.truth_currents.values())
        out.append(_with_extra_field(base, cfg, hidden_return, scale, "hidden_return_no_via"))

        # H1 label, but the true via is shifted away from the candidate via.
        base = _make_case(9000 + idx, "ood", "true_via", rng, cfg)
        cand = base.via_candidates[0]
        shift = (0.08 + 0.06 * rng.random()) * fov
        shifted = Segment(
            name=f"shifted_true_via_{idx:03d}",
            layer=cand.layer,
            kind="via",
            start=(cand.start[0] + shift, cand.start[1], cand.start[2]),
            end=(cand.end[0] + shift, cand.end[1], cand.end[2]),
            prior_group="hidden",
        )
        # Remove the original true candidate's current from the observation and
        # replace it with an off-candidate via; the scorer still sees the old candidate.
        original_current = next(
            (float(base.truth_currents.get(seg.name, 0.0)) for seg in base.via_candidates if seg.name in base.truth_currents),
            0.0,
        )
        obs_grid = make_observation_grid(int(cfg["grid"]["n"]), float(cfg["grid"]["fov_m"]), float(cfg["grid"].get("obs_z_m", 0.0)))
        remove = field_from_segments([cand], {cand.name: original_current}, obs_grid, int(cfg["geometry"]["edge_discretization"]), int(cfg["geometry"]["via_discretization"]))
        replaced = _with_extra_field(base, cfg, shifted, original_current, "shifted_true_via")
        out.append(replace(replaced, b_clean=replaced.b_clean - remove, b_obs=replaced.b_obs - remove))

        # H3 label, but artifact orientation/position is mismatched.
        base = _make_case(10000 + idx, "ood", "bend_artifact", rng, cfg)
        artifact = base.artifact_candidates[0]
        dx = artifact.end[0] - artifact.start[0]
        dy = artifact.end[1] - artifact.start[1]
        center = (
            0.5 * (artifact.start[0] + artifact.end[0]),
            0.5 * (artifact.start[1] + artifact.end[1]),
            0.5 * (artifact.start[2] + artifact.end[2]),
        )
        mismatch = Segment(
            name=f"mismatched_artifact_{idx:03d}",
            layer=artifact.layer,
            kind="artifact",
            start=(center[0] - 0.5 * dy, center[1] + 0.5 * dx, center[2]),
            end=(center[0] + 0.5 * dy, center[1] - 0.5 * dx, center[2]),
            prior_group="hidden",
        )
        art_current = next(
            (float(base.truth_currents.get(seg.name, 0.0)) for seg in base.artifact_candidates if seg.name in base.truth_currents),
            0.0,
        )
        obs_grid = make_observation_grid(int(cfg["grid"]["n"]), float(cfg["grid"]["fov_m"]), float(cfg["grid"].get("obs_z_m", 0.0)))
        remove = field_from_segments([artifact], {artifact.name: art_current}, obs_grid, int(cfg["geometry"]["edge_discretization"]), int(cfg["geometry"]["via_discretization"]))
        replaced = _with_extra_field(base, cfg, mismatch, art_current, "mismatched_artifact")
        out.append(replace(replaced, b_clean=replaced.b_clean - remove, b_obs=replaced.b_obs - remove))

        # H1 primary label plus a hidden return: a deliberate multi-mechanism case.
        base = _make_case(11000 + idx, "ood", "true_via", rng, cfg)
        x0, x1, y0, _, zmin = _local_span(base)
        hidden_return = Segment(
            name=f"combined_hidden_return_{idx:03d}",
            layer="HIDDEN_RETURN",
            kind="return",
            start=(x1, y0 - 0.16 * fov, zmin - 85e-6),
            end=(x0, y0 - 0.16 * fov, zmin - 85e-6),
            prior_group="hidden",
        )
        scale = 0.35 * max(abs(v) for v in base.truth_currents.values())
        out.append(_with_extra_field(base, cfg, hidden_return, scale, "combined_true_via_hidden_return"))
    return out


def generate_near_boundary_hidden_records(cfg: dict) -> List[CaseRecord]:
    """Generate harder hidden cases that sit close to the known hypothesis bank.

    The base hidden stress above intentionally contains mechanisms that can be
    far from the in-library H0/H1/H2/H3 evidence manifold. These cases are
    designed to be more dangerous: their fields are close to existing return,
    via, or bend/artifact candidates, so a distance-based refusal layer must
    prove that it can handle near-boundary unknowns rather than only obvious
    outliers.
    """

    rng = np.random.default_rng(int(cfg["seed"]) + 1808)
    out: List[CaseRecord] = []
    n_per_family = int(cfg.get("hidden_stress", {}).get("n_per_family", 24))
    fov = float(cfg["grid"]["fov_m"])
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=fov,
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    edge_steps = int(cfg["geometry"]["edge_discretization"])
    via_steps = int(cfg["geometry"]["via_discretization"])

    for idx in range(n_per_family):
        # H0 label with a weak nearby return-like current that is close to the
        # return candidate family but should not be interpreted as a true via.
        base = _make_case(12000 + idx, "ood", "no_via", rng, cfg)
        cand_return = base.return_candidates[0]
        dy = (0.025 + 0.025 * rng.random()) * fov * rng.choice([-1.0, 1.0])
        hidden_return = Segment(
            name=f"near_boundary_return_shadow_{idx:03d}",
            layer="NEAR_BOUNDARY_RETURN",
            kind="return",
            start=(cand_return.start[0], cand_return.start[1] + dy, cand_return.start[2] - 15e-6),
            end=(cand_return.end[0], cand_return.end[1] + dy, cand_return.end[2] - 15e-6),
            prior_group="hidden",
        )
        scale = 0.18 * max(abs(v) for v in base.truth_currents.values())
        out.append(_with_extra_field(base, cfg, hidden_return, scale, "near_return_shadow_no_via"))

        # H1 label with a true via just outside the candidate position. This is
        # a near-boundary version of shifted_true_via and is intentionally much
        # closer to the candidate than the base hidden stress.
        base = _make_case(13000 + idx, "ood", "true_via", rng, cfg)
        cand = base.via_candidates[0]
        shift = (0.018 + 0.018 * rng.random()) * fov * rng.choice([-1.0, 1.0])
        shifted = Segment(
            name=f"near_shifted_true_via_{idx:03d}",
            layer=cand.layer,
            kind="via",
            start=(cand.start[0] + shift, cand.start[1], cand.start[2]),
            end=(cand.end[0] + shift, cand.end[1], cand.end[2]),
            prior_group="hidden",
        )
        original_current = next(
            (float(base.truth_currents.get(seg.name, 0.0)) for seg in base.via_candidates if seg.name in base.truth_currents),
            0.0,
        )
        remove = field_from_segments([cand], {cand.name: original_current}, obs_grid, edge_steps, via_steps)
        replaced = _with_extra_field(base, cfg, shifted, original_current, "near_shifted_true_via")
        out.append(replace(replaced, b_clean=replaced.b_clean - remove, b_obs=replaced.b_obs - remove))

        # H1 label with a via at the candidate x/y but wrong depth span. This
        # tests whether a wrong-layer vertical current is treated as known H1 or
        # flagged as out-of-library geometry.
        base = _make_case(14000 + idx, "ood", "true_via", rng, cfg)
        cand = base.via_candidates[0]
        z_shift = (18e-6 + 10e-6 * rng.random()) * rng.choice([-1.0, 1.0])
        wrong_layer = Segment(
            name=f"wrong_layer_true_via_{idx:03d}",
            layer="WRONG_LAYER_VIA",
            kind="via",
            start=(cand.start[0], cand.start[1], cand.start[2] + z_shift),
            end=(cand.end[0], cand.end[1], cand.end[2] + z_shift),
            prior_group="hidden",
        )
        original_current = next(
            (float(base.truth_currents.get(seg.name, 0.0)) for seg in base.via_candidates if seg.name in base.truth_currents),
            0.0,
        )
        remove = field_from_segments([cand], {cand.name: original_current}, obs_grid, edge_steps, via_steps)
        replaced = _with_extra_field(base, cfg, wrong_layer, original_current, "wrong_layer_true_via")
        out.append(replace(replaced, b_clean=replaced.b_clean - remove, b_obs=replaced.b_obs - remove))

        # H0 label with a weak local bend/corner shadow near the artifact
        # candidate. This is deliberately close to H3 but should be treated as
        # ambiguous/unknown under a safety screen rather than a confident via.
        base = _make_case(15000 + idx, "ood", "no_via", rng, cfg)
        artifact = base.artifact_candidates[0]
        dx = artifact.end[0] - artifact.start[0]
        dy = artifact.end[1] - artifact.start[1]
        scale_xy = 0.65 + 0.2 * rng.random()
        shadow = Segment(
            name=f"near_corner_shadow_{idx:03d}",
            layer="NEAR_BOUNDARY_ARTIFACT",
            kind="artifact",
            start=(artifact.start[0] + 0.12 * dy, artifact.start[1] - 0.12 * dx, artifact.start[2] - 8e-6),
            end=(
                artifact.start[0] + 0.12 * dy + scale_xy * dx,
                artifact.start[1] - 0.12 * dx + scale_xy * dy,
                artifact.end[2] - 8e-6,
            ),
            prior_group="hidden",
        )
        scale = 0.16 * max(abs(v) for v in base.truth_currents.values())
        out.append(_with_extra_field(base, cfg, shadow, scale, "near_corner_shadow_no_via"))
    return out


def generate_near_boundary_hidden_severity_records(cfg: dict) -> List[CaseRecord]:
    """Generate a severity sweep for near-boundary hidden mechanisms."""

    rng = np.random.default_rng(int(cfg["seed"]) + 2808)
    out: List[CaseRecord] = []
    n_per_level = max(6, int(cfg.get("hidden_stress", {}).get("n_per_family", 24)) // 3)
    severity_levels = [0.25, 0.50, 1.00, 1.50]
    fov = float(cfg["grid"]["fov_m"])
    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=fov,
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    edge_steps = int(cfg["geometry"]["edge_discretization"])
    via_steps = int(cfg["geometry"]["via_discretization"])

    def tag(record: CaseRecord, severity: float, family: str) -> CaseRecord:
        metadata = dict(record.metadata)
        metadata["hidden_severity"] = float(severity)
        metadata["hidden_mechanism_family"] = f"severity_{severity:.2f}_{family}"
        metadata["near_boundary_sweep"] = True
        return replace(record, metadata=metadata)

    for severity in severity_levels:
        s_tag = f"s{int(round(severity * 100)):03d}"
        for idx in range(n_per_level):
            base = _make_case(16000 + int(severity * 1000) + idx, "ood", "no_via", rng, cfg)
            cand_return = base.return_candidates[0]
            dy = severity * (0.012 + 0.016 * rng.random()) * fov * rng.choice([-1.0, 1.0])
            hidden_return = Segment(
                name=f"{s_tag}_return_shadow_{idx:03d}",
                layer="SEVERITY_RETURN",
                kind="return",
                start=(cand_return.start[0], cand_return.start[1] + dy, cand_return.start[2] - severity * 12e-6),
                end=(cand_return.end[0], cand_return.end[1] + dy, cand_return.end[2] - severity * 12e-6),
                prior_group="hidden",
            )
            scale = (0.08 + 0.10 * severity) * max(abs(v) for v in base.truth_currents.values())
            out.append(tag(_with_extra_field(base, cfg, hidden_return, scale, f"{s_tag}_near_return_shadow_no_via"), severity, "near_return_shadow_no_via"))

            base = _make_case(17000 + int(severity * 1000) + idx, "ood", "true_via", rng, cfg)
            cand = base.via_candidates[0]
            shift = severity * (0.008 + 0.010 * rng.random()) * fov * rng.choice([-1.0, 1.0])
            shifted = Segment(
                name=f"{s_tag}_shifted_true_via_{idx:03d}",
                layer=cand.layer,
                kind="via",
                start=(cand.start[0] + shift, cand.start[1], cand.start[2]),
                end=(cand.end[0] + shift, cand.end[1], cand.end[2]),
                prior_group="hidden",
            )
            current = next((float(base.truth_currents.get(seg.name, 0.0)) for seg in base.via_candidates if seg.name in base.truth_currents), 0.0)
            remove = field_from_segments([cand], {cand.name: current}, obs_grid, edge_steps, via_steps)
            replaced = _with_extra_field(base, cfg, shifted, current, f"{s_tag}_near_shifted_true_via")
            out.append(tag(replace(replaced, b_clean=replaced.b_clean - remove, b_obs=replaced.b_obs - remove), severity, "near_shifted_true_via"))

            base = _make_case(18000 + int(severity * 1000) + idx, "ood", "true_via", rng, cfg)
            cand = base.via_candidates[0]
            z_shift = severity * (8e-6 + 8e-6 * rng.random()) * rng.choice([-1.0, 1.0])
            wrong_layer = Segment(
                name=f"{s_tag}_wrong_layer_true_via_{idx:03d}",
                layer="SEVERITY_WRONG_LAYER_VIA",
                kind="via",
                start=(cand.start[0], cand.start[1], cand.start[2] + z_shift),
                end=(cand.end[0], cand.end[1], cand.end[2] + z_shift),
                prior_group="hidden",
            )
            current = next((float(base.truth_currents.get(seg.name, 0.0)) for seg in base.via_candidates if seg.name in base.truth_currents), 0.0)
            remove = field_from_segments([cand], {cand.name: current}, obs_grid, edge_steps, via_steps)
            replaced = _with_extra_field(base, cfg, wrong_layer, current, f"{s_tag}_wrong_layer_true_via")
            out.append(tag(replace(replaced, b_clean=replaced.b_clean - remove, b_obs=replaced.b_obs - remove), severity, "wrong_layer_true_via"))

            base = _make_case(19000 + int(severity * 1000) + idx, "ood", "no_via", rng, cfg)
            artifact = base.artifact_candidates[0]
            dx = artifact.end[0] - artifact.start[0]
            dy = artifact.end[1] - artifact.start[1]
            scale_xy = 0.55 + 0.18 * severity
            shadow = Segment(
                name=f"{s_tag}_corner_shadow_{idx:03d}",
                layer="SEVERITY_ARTIFACT",
                kind="artifact",
                start=(artifact.start[0] + 0.10 * dy, artifact.start[1] - 0.10 * dx, artifact.start[2] - severity * 6e-6),
                end=(
                    artifact.start[0] + 0.10 * dy + scale_xy * dx,
                    artifact.start[1] - 0.10 * dx + scale_xy * dy,
                    artifact.end[2] - severity * 6e-6,
                ),
                prior_group="hidden",
            )
            scale = (0.07 + 0.09 * severity) * max(abs(v) for v in base.truth_currents.values())
            out.append(tag(_with_extra_field(base, cfg, shadow, scale, f"{s_tag}_near_corner_shadow_no_via"), severity, "near_corner_shadow_no_via"))
    return out
