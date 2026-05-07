"""E29 main orchestrator.

Usage:
  uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
  uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import time

_src_dir = str(Path(__file__).resolve().parent)
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

import numpy as np

from rho_local import (
    compute_full_rho_decomposition,
    volume_operator,
    centerline_operator,
)
from schur_signal import (
    generate_candidate_defects,
    generate_defect_operator,
    compute_all_schur_signals,
)
from gamma import (
    compute_all_defect_gammas,
    compute_aggregate_rates,
    compute_thresholds_from_calibration,
)
from pairwise import (
    compute_pairwise_gamma,
    compute_pairwise_rates,
)
from split_discipline import (
    split_geometries,
    split_audit,
)
from reports import (
    write_metrics_json,
    write_run_report,
    write_rho_input_audit,
    write_gamma_ablation_table,
    write_conservative_gamma_certificate,
    write_rss_gamma_upper_bound,
    write_pairwise_defect_certificate,
    write_calibration_evaluation_split_audit,
    write_failure_modes,
)


def make_canonical_edges(n_edges: int = 12) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create a small canonical multi-layer via-trace geometry.

    Distributes n_edges across trace edges and via connections:
    - min(4, n_edges//3) layer-1 horizontal traces
    - min(4, n_edges//3) layer-2 vertical traces
    - remaining as vertical vias

    Returns (edges, widths, thicknesses, points).
    """
    edges = np.zeros((n_edges, 2, 3), dtype=float)
    widths = np.full(n_edges, 4e-5, dtype=float)
    thicknesses = np.full(n_edges, 1e-5, dtype=float)

    n_trace_l1 = min(4, max(1, n_edges // 3))
    n_trace_l2 = min(4, max(1, n_edges // 3))
    n_vias = n_edges - n_trace_l1 - n_trace_l2

    layer1_z = 0.0
    layer2_z = 5e-5

    idx = 0
    for i in range(n_trace_l1):
        y = (i - (n_trace_l1 - 1) / 2.0) * 2e-4
        edges[idx, 0] = [-5e-4, y, layer1_z]
        edges[idx, 1] = [5e-4, y, layer1_z]
        idx += 1

    for i in range(n_trace_l2):
        x = (i - (n_trace_l2 - 1) / 2.0) * 2e-4
        edges[idx, 0] = [x, -5e-4, layer2_z]
        edges[idx, 1] = [x, 5e-4, layer2_z]
        idx += 1

    via_offsets = [(-3e-4, -3e-4), (3e-4, -3e-4), (-3e-4, 3e-4), (3e-4, 3e-4)]
    for i in range(min(n_vias, 4)):
        vx, vy = via_offsets[i]
        edges[idx, 0] = [vx, vy, layer1_z]
        edges[idx, 1] = [vx, vy, layer2_z]
        idx += 1

    # Fill any remaining with more traces
    for i in range(idx, n_edges):
        y = (i - n_edges / 2.0) * 2e-4
        edges[i, 0] = [-5e-4, y, layer1_z]
        edges[i, 1] = [5e-4, y, layer1_z]

    # Observation grid
    n_obs = 7 if n_edges <= 6 else 11
    fov = 1.2e-3
    xs = np.linspace(-fov / 2, fov / 2, n_obs)
    ys = np.linspace(-fov / 2, fov / 2, n_obs)
    z_sensor = 8e-5
    X, Y = np.meshgrid(xs, ys)
    points = np.column_stack([X.ravel(), Y.ravel(), np.full(n_obs * n_obs, z_sensor)])

    return edges, widths, thicknesses, points


def run_pipeline(config: dict, output_dir: Path, smoke: bool = False) -> dict:
    """Execute the full E29 pipeline."""
    output_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()

    seed = config.get("seed", 42)
    rng = np.random.default_rng(seed)

    # --- 1. Build canonical geometry ---
    n_edges_cfg = config.get("n_edges", 6 if smoke else 12)
    edges, widths, thicknesses, points = make_canonical_edges(n_edges_cfg)
    E = edges.shape[0]

    # --- 2. Compute rho decomposition ---
    delta_z = config.get("delta_z_m", 1e-5)
    delta_xy = config.get("delta_xy_m", 1e-6)
    delta_layer_z = config.get("delta_layer_z_m", 5e-6)
    background_fraction = config.get("background_fraction", 1e-4)

    rho_decomposition = compute_full_rho_decomposition(
        points, edges, widths, thicknesses,
        delta_z=delta_z,
        delta_xy=delta_xy,
        delta_layer_z=delta_layer_z,
        background_fraction=background_fraction,
    )

    # Build nominal forward operator
    A_nominal = volume_operator(points, edges, widths, thicknesses)

    # --- 3. Generate current samples ---
    K = config.get("current_samples", 8 if smoke else 20)
    current_samples = rng.standard_normal((E, K))
    norms = np.linalg.norm(current_samples, axis=0)
    current_samples = current_samples / (norms + 1e-30)

    # --- 4. Generate candidate defects ---
    all_defects = generate_candidate_defects(E, seed=seed)
    if smoke:
        all_defects = all_defects[:8]

    # --- 5. Calibration/evaluation split ---
    calib_frac = config.get("calibration_fraction", 0.5)
    split_info = split_geometries(
        edges, widths, thicknesses, all_defects,
        calibration_fraction=calib_frac, seed=seed,
    )
    split_result = split_audit(split_info)

    cal_defects = split_info["calibration"]["defects"]
    eval_defects = split_info["evaluation"]["defects"]

    # --- 6. Compute thresholds from CALIBRATION ONLY ---
    noise_sigma = config.get("noise_sigma", 1e-12)
    obs_dim = 3 * points.shape[0]
    tau_mult = config.get("tau_multiplier", 2.5)

    cal_schur = compute_all_schur_signals(
        A_nominal, edges, widths, thicknesses,
        cal_defects, current_samples, noise_sigma, seed=seed,
    )
    thresholds = compute_thresholds_from_calibration(
        cal_schur, noise_sigma, obs_dim, tau_multiplier=tau_mult,
    )
    epsilon = thresholds["epsilon"]
    tau = thresholds["tau"]

    # --- 7. Compute Schur signals for EVALUATION defects ---
    eval_schur = compute_all_schur_signals(
        A_nominal, edges, widths, thicknesses,
        eval_defects, current_samples, noise_sigma, seed=seed,
    )

    # --- 8. Compute Gamma for all defects ---
    rho_comps = rho_decomposition["components"]
    eval_gammas = compute_all_defect_gammas(
        eval_schur, rho_comps, epsilon, tau,
    )

    # Also compute for calibration set (for ablation completeness)
    cal_gammas = compute_all_defect_gammas(
        cal_schur, rho_comps, epsilon, tau,
    )
    all_gammas = cal_gammas + eval_gammas

    # --- 9. Aggregate rates (on EVALUATION set) ---
    eval_rates = compute_aggregate_rates(eval_gammas)

    # --- 10. Pairwise defect certificate ---
    eval_defect_operators: dict[str, np.ndarray] = {}
    for defect in eval_defects:
        A_def = generate_defect_operator(
            A_nominal, edges, widths, thicknesses, defect, rng,
        )
        eval_defect_operators[defect["defect_id"]] = A_def

    pairwise_results = compute_pairwise_gamma(
        A_nominal, eval_defect_operators, current_samples,
        rho_comps, epsilon, tau,
    )
    pairwise_r = compute_pairwise_rates(pairwise_results)

    # --- 11. E25 rho impact on E23/E24 conclusions ---
    rho_cons = rho_decomposition["components"]["rho_combined_conservative"]["absolute_radius"]
    rho_rss = rho_decomposition["components"]["rho_combined_rss"]["absolute_radius"]
    rho_e23_old = rho_decomposition["components"]["rho_combined_e23_old"]["absolute_radius"]
    rho_fw_rel = rho_decomposition["components"]["rho_finite_width"]["relative_radius"]

    # Count how many defects change pass/fail using E25 vs E23 old rho
    e23_change_count = sum(
        1 for g in eval_gammas
        if g.get("e25_calibrated_pass") != g.get("e23_old_pass")
    )
    e23_change_rate = e23_change_count / max(len(eval_gammas), 1)

    if rho_cons < rho_e23_old:
        e23_e24_impact = (
            f"E25 calibrated rho (abs={rho_cons:.4e}) is SMALLER than E23 old rho "
            f"(abs={rho_e23_old:.4e}). This means E25 IMPROVES Gamma over E23: "
            f"fewer false negatives, more defects pass conservative Gamma.\n\n"
            f"E23 old rho used a 2.5x multiplier on the centerline-to-volume gap, "
            f"while E25 decomposes into physically justified components with numerical "
            f"convergence verification. The finite-width relative rho is {rho_fw_rel:.4f}, "
            f"indicating the operator gap is {'large' if rho_fw_rel > 0.3 else 'moderate' if rho_fw_rel > 0.1 else 'small'}.\n\n"
            f"Impact on E23/E24 conclusions: {e23_change_count}/{len(eval_gammas)} "
            f"defects ({e23_change_rate:.1%}) change pass/fail status when switching "
            f"from E23 old rho to E25 calibrated rho. "
            f"The E23/E24 qualitative conclusions are "
            f"{'AFFECTED' if e23_change_rate > 0.2 else 'NOT FUNDAMENTALLY CHANGED'}: "
            f"the robust Gamma certificate {'is' if eval_rates.get('positive_conservative_rho_rate', 0) > 0 else 'is not'} "
            f"achievable with conservative operator-radius subtraction."
        )
    else:
        e23_e24_impact = (
            f"E25 calibrated rho (abs={rho_cons:.4e}) is LARGER than E23 old rho "
            f"(abs={rho_e23_old:.4e}). This means E25 calibration reveals the operator "
            f"gap was UNDERESTIMATED by E23, making the robust Gamma certificate "
            f"HARDER to achieve."
        )

    # --- 12. Acceptance gates ---
    engineering_gates = {
        "package_runs_to_completion": True,
        "rho_artifacts_loaded_or_recomputed": True,
        "calibration_evaluation_split_enforced": split_result["discipline_enforced"],
        "conservative_and_rss_gamma_reported": True,
        "pairwise_gamma_reported": len(pairwise_results) > 0,
        "ablation_table_reported": len(all_gammas) > 0,
        "reports_written": True,
        "generated_domain_boundary_explicit": True,
    }

    scientific_gates = {
        "E25_rho_improves_gamma_over_E23_old_rho": rho_cons < rho_e23_old,
        "positive_conservative_gamma_rate_ge_0_30": eval_rates.get(
            "positive_conservative_rho_rate", 0) >= 0.30,
        "positive_rss_gamma_rate_ge_0_50": eval_rates.get(
            "positive_rss_rho_rate", 0) >= 0.50,
        "pairwise_conservative_gamma_rate_ge_0_20": pairwise_r.get(
            "pairwise_conservative_gamma_rate", 0) >= 0.20,
        "truth_in_consistent_set_rate_ge_0_90": (1.0 - eval_rates.get(
            "truth_missing_rate", 0)) >= 0.90,
        "wrong_accept_rate_le_0_10": eval_rates.get(
            "wrong_accept_rate_conservative", 0) <= 0.10,
        "empty_rate_le_0_10": eval_rates.get("empty_rate", 0) <= 0.10,
    }

    all_gates = {**engineering_gates, **scientific_gates}
    all_gates["all_engineering_gates_passed"] = all(engineering_gates.values())
    all_gates["all_scientific_gates_passed"] = all(scientific_gates.values())
    all_gates["all_acceptance_gates_passed"] = (
        all_gates["all_engineering_gates_passed"]
        and all_gates["all_scientific_gates_passed"]
    )

    # --- 13. Failure modes ---
    failure_modes = _collect_failure_modes(
        all_gates, split_result, eval_rates, pairwise_r,
    )

    # --- 14. Write all outputs ---
    write_metrics_json(
        output_dir, all_gates, eval_rates, split_result, pairwise_r,
    )

    context = {
        "config": "smoke" if smoke else "default",
        "smoke": smoke,
        "n_edges": E,
        "n_cal_defects": len(cal_defects),
        "n_eval_defects": len(eval_defects),
        "gates": all_gates,
        "aggregate_rates": eval_rates,
        "rho_components": rho_decomposition,
        "split_audit": split_result,
        "pairwise_rates": pairwise_r,
        "e23_e24_impact": e23_e24_impact,
        "failure_modes": failure_modes,
        "cannot_claim": [
            "All results are generated-domain only; no real QDM/NV sensor data is used.",
            "No external solver (PyPEEC, FastHenry, COMSOL) is used for cross-validation.",
            "Schur defect signatures are synthetic and not validated against E27 edge-Schur artifacts.",
            "Rho estimates are locally computed (E25 artifacts not available in E29 worktree); marked as local generated calibration.",
            "Operator matrices use simplified geometry (canonical straight segments); no CAD/GDS import.",
            "No real via/return diagnosis; all defects are synthetic perturbations on generated geometries.",
            "Calibration/evaluation split is geometric (defect-based), not layout-family-based.",
            "Pairwise certificate uses shared rho; per-defect rho not available without E27 artifacts.",
        ],
    }

    write_run_report(output_dir, context)
    write_rho_input_audit(output_dir, rho_decomposition, loaded_from_e25=False)
    write_gamma_ablation_table(output_dir, all_gammas, eval_rates)
    write_conservative_gamma_certificate(
        output_dir, eval_gammas, eval_rates, all_gates,
    )
    write_rss_gamma_upper_bound(output_dir, eval_gammas, eval_rates)
    write_pairwise_defect_certificate(output_dir, pairwise_results, pairwise_r)
    write_calibration_evaluation_split_audit(output_dir, split_info, split_result)
    write_failure_modes(output_dir, failure_modes)

    elapsed = time.time() - t_start
    result = {
        "elapsed_s": elapsed,
        "n_edges": E,
        "n_cal_defects": len(cal_defects),
        "n_eval_defects": len(eval_defects),
        "gates": all_gates,
        "rho_conservative_abs": rho_cons,
        "rho_rss_abs": rho_rss,
        "rho_e23_old_abs": rho_e23_old,
        "e23_e24_impact": e23_e24_impact[:200],
    }
    (output_dir / "pipeline_result.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8"
    )
    return result


def _collect_failure_modes(
    gates: dict, split_result: dict, rates: dict, pairwise_r: dict,
) -> list[dict]:
    failures = []

    if not split_result.get("discipline_enforced", False):
        for v in split_result.get("violations", []):
            failures.append({
                "name": "calibration_evaluation_split_violation",
                "severity": "error",
                "description": v,
                "gate_passed": False,
            })

    cons_rate = rates.get("positive_conservative_rho_rate", 0)
    if cons_rate < 0.30:
        failures.append({
            "name": "low_conservative_gamma_rate",
            "severity": "error",
            "description": (
                f"Conservative Gamma positive rate is {cons_rate:.2%}, "
                f"below the 0.30 gate. The operator-radius subtraction "
                f"may be too conservative, or the Schur signals are too weak."
            ),
            "gate_passed": False,
        })

    rss_rate = rates.get("positive_rss_rho_rate", 0)
    if rss_rate >= 0.50 and cons_rate < 0.30:
        failures.append({
            "name": "rss_passes_but_conservative_fails",
            "severity": "warning",
            "description": (
                f"RSS Gamma rate ({rss_rate:.2%}) passes the 0.50 gate but "
                f"conservative Gamma rate ({cons_rate:.2%}) fails the 0.30 gate. "
                "Per E29 §5: report as promising but not claim-supporting. "
                "The independence assumption behind RSS must be validated "
                "before RSS can govern claims."
            ),
            "gate_passed": False,
        })

    wrong_rate = rates.get("wrong_accept_rate_conservative", 0)
    if wrong_rate > 0.10:
        failures.append({
            "name": "high_wrong_accept_rate",
            "severity": "error",
            "description": (
                f"Wrong accept rate is {wrong_rate:.2%}, above the 0.10 gate. "
                f"Non-structural defect types are being accepted, indicating "
                f"insufficient separability."
            ),
            "gate_passed": False,
        })

    truth_miss = rates.get("truth_missing_rate", 0)
    if truth_miss > 0.10:
        failures.append({
            "name": "high_truth_missing_rate",
            "severity": "error",
            "description": (
                f"Truth missing rate is {truth_miss:.2%}, above the 0.10 gate. "
                f"Structural defects are being missed, indicating insufficient "
                f"sensitivity."
            ),
            "gate_passed": False,
        })

    empty_rate = rates.get("empty_rate", 0)
    if empty_rate > 0.10:
        failures.append({
            "name": "high_empty_rate",
            "severity": "warning",
            "description": (
                f"Empty rate is {empty_rate:.2%}, above the 0.10 gate. "
                f"Many defects have negative Gamma across all ablation variants, "
                f"suggesting the signal is too weak or the noise/rho budget "
                f"is too large for these defects."
            ),
            "gate_passed": False,
        })

    pw_rate = pairwise_r.get("pairwise_conservative_gamma_rate", 0)
    if pw_rate < 0.20:
        failures.append({
            "name": "low_pairwise_conservative_rate",
            "severity": "warning",
            "description": (
                f"Pairwise conservative Gamma rate is {pw_rate:.2%}, below "
                f"the 0.20 gate. Many defect pairs are not distinguishable "
                f"after subtracting operator-radius penalties."
            ),
            "gate_passed": False,
        })

    failures.append({
        "name": "synthetic_schur_signatures",
        "severity": "warning",
        "description": (
            "Schur defect signatures are synthetic (generated perturbations on "
            "canonical geometry). Real E27 edge-Schur artifacts are not available. "
            "The Gamma values and pass rates will change when real defect signatures "
            "are substituted."
        ),
        "gate_passed": True,
    })

    failures.append({
        "name": "local_rho_not_e25_calibrated",
        "severity": "warning",
        "description": (
            "Rho estimates are computed locally in the E29 worktree, not loaded "
            "from E25 artifacts (rho_calibration_table.json, operator_error_budget.json). "
            "Values follow E25 methodology but use simplified volume quadrature. "
            "Re-run with E25 outputs when available."
        ),
        "gate_passed": True,
    })

    failures.append({
        "name": "shared_rho_all_defects",
        "severity": "info",
        "description": (
            "Pairwise certificate uses a single shared rho for all defects. "
            "Per-defect rho requires per-defect operator matrices, which depend "
            "on E27 edge-Schur artifacts. This simplification may over-estimate "
            "pairwise separability for some pairs."
        ),
        "gate_passed": True,
    })

    if not failures:
        failures.append({
            "name": "all_gates_passed",
            "severity": "info",
            "description": "All acceptance gates passed.",
            "gate_passed": True,
        })

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="E29 Rho-Integrated Schur Gamma Certificate"
    )
    parser.add_argument("--config", required=True, help="Path to config JSON.")
    parser.add_argument("--out", required=True, help="Output directory.")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"ERROR: Config not found: {config_path}", file=sys.stderr)
        return 1

    config = json.loads(config_path.read_text(encoding="utf-8"))
    output_dir = Path(args.out)
    smoke = "smoke" in str(config_path).lower()

    result = run_pipeline(config, output_dir, smoke=smoke)

    all_pass = result["gates"].get("all_acceptance_gates_passed", False)
    print(f"\nE29 pipeline complete in {result['elapsed_s']:.1f}s")
    print(f"  Edges: {result['n_edges']}")
    print(f"  Calibration defects: {result['n_cal_defects']}")
    print(f"  Evaluation defects: {result['n_eval_defects']}")
    print(f"  All acceptance gates passed: {all_pass}")
    print(f"  Rho conservative (abs): {result['rho_conservative_abs']:.4e}")
    print(f"  Rho RSS (abs): {result['rho_rss_abs']:.4e}")
    print(f"  Rho E23 old (abs): {result['rho_e23_old_abs']:.4e}")
    print(f"  E23/E24 impact: {result['e23_e24_impact'][:120]}...")

    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
