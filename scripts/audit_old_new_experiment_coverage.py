from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_ROOT = ROOT.parent / "current-density-inversion-old"
sys.path.insert(0, str(ROOT / "src"))

from research_ssot import load_graph, metrics_gate_status


MAPPING = [
    {
        "old": "exp01-biot-savart-forward-sanity",
        "responsibility": "finite-line Biot-Savart signs, units, linearity, via direction, standoff trend",
        "gates": "finite wire reference; current reversal; loop superposition; via Bz/Bxy; standoff monotone",
        "metrics": "field sanity gates",
        "tests": "forward segment tests",
        "run": "python src/experiments/run_all.py",
        "evidence": "E01_canonical_forward_sanity",
        "package": "experiments/evidence/E01_forward_sanity",
        "claim": "C01_forward_sanity",
    },
    {
        "old": "exp02-observability-and-bxy-vs-bz",
        "responsibility": "Fourier observability, Bxy/Bz finite-FOV difference, noise/standoff, two-layer rank",
        "gates": "clean inverse; Bz finite-FOV worse than Bxy; rank deficiency",
        "metrics": "observability and rank gates",
        "tests": "spectral operator tests",
        "run": "python src/experiments/run_all.py",
        "evidence": "E02_observability_bxy_bz",
        "package": "experiments/evidence/E02_identifiability_boundary",
        "claim": "C02_single_plane_identifiability_boundary",
    },
    {
        "old": "exp03-two-layer-via-toy-benchmark",
        "responsibility": "two-layer via benchmark, route diversity, topology residual, OOD cases, surrogate gap",
        "gates": "split counts; truth channels; recoverability; finite-width/return gap",
        "metrics": "dataset and topology gates",
        "tests": "toy benchmark tests",
        "run": "python src/experiments/run_all.py --config configs/default.json",
        "evidence": "E03_two_layer_via_topology",
        "package": "experiments/evidence/E03_two_layer_via_topology",
        "claim": "C02_single_plane_identifiability_boundary; C03_unet_topology_baseline_boundary",
    },
    {
        "old": "exp04-topology-aware-inverse-benchmark",
        "responsibility": "U-Net-lite topology benchmark, stress, lambda sweep, PyPEEC frozen bridge, null-via and return diagnostics",
        "gates": "topology/l2/stress/multiseed; residual detector; PyPEEC bridge; H0/H1/refusal/return diagnostics",
        "metrics": "topology, current, detector, operator, PyPEEC frozen-inference gates",
        "tests": "exp04 regression tests",
        "run": "python src/run_all.py --config configs/default.json",
        "evidence": "E04_topology_baseline_and_failures",
        "package": "experiments/evidence/E04_topology_baseline",
        "claim": "C03_unet_topology_baseline_boundary; C04_inverse_crime_and_operator_gap; C11_mechanism_level_explanation",
    },
    {
        "old": "exp05-realistic-noise-and-standoff-tilt",
        "responsibility": "PSF, correlated noise, confidence, standoff tilt, NV projection, axis gain mismatch",
        "gates": "noise covariance; PSF high-frequency loss; tilt mismatch; residual detector; NV rank/gain",
        "metrics": "sensor proxy gates",
        "tests": "sensor stress tests",
        "run": "python src/run_all.py",
        "evidence": "E05_qdm_like_observation_stress",
        "package": "experiments/evidence/E05_qdm_like_observation_stress",
        "claim": "C13_calibration_protocol_reality",
    },
    {
        "old": "exp06-anti-inverse-crime-multifidelity-validation",
        "responsibility": "anti-inverse-crime multifidelity operator gap and PyPEEC read-only bridge",
        "gates": "same-operator overoptimism; operator basis gap; calibration improvement; PyPEEC bridge",
        "metrics": "operator gap gates",
        "tests": "operator gap tests",
        "run": "python src/run_all.py",
        "evidence": "E06_multifidelity_operator_gap",
        "package": "experiments/evidence/E06_operator_gap",
        "claim": "C04_inverse_crime_and_operator_gap",
    },
    {
        "old": "exp07-pypeec-solver-cross-validation",
        "responsibility": "real PyPEEC API bridge, canonical and exp03-like connected routes, 400-case target",
        "gates": "run_mesher_data/run_solver_data; no proxy fallback; convergence; mini dataset export",
        "metrics": "solver cross-validation gates",
        "tests": "pypeec availability and no-fallback tests",
        "run": "python src/run_all.py",
        "evidence": "E07_pypeec_solver_bridge",
        "package": "experiments/evidence/E07_solver_bridge",
        "claim": "C05_pypeec_solver_bridge",
    },
    {
        "old": "exp08-graph-system-identification",
        "responsibility": "H0/H1/H2/H3 graph scoring, PyPEEC bridge, hidden stress, calibration, refusal, active design",
        "gates": "4-way accuracy; AUC/F1/FP; model selection; unknown safety; few-shot; registration/standoff",
        "metrics": "all_scientific_gates_passed and graph-system-id tables",
        "tests": "graph ID tests",
        "run": "python src/run_all.py",
        "evidence": "E08_graph_hypothesis_system_id",
        "package": "experiments/evidence/E08_graph_hypothesis",
        "claim": "C06-C09; C11; C13",
    },
    {
        "old": "exp09-real-qdm-nv-data-interface",
        "responsibility": "real QDM/NV intake interface scaffold, metadata validator, NPZ loader, plotting/background/simple-wire utilities",
        "gates": "metadata, strict paths off by default, units/component/background validation, no real rows",
        "metrics": "interface scaffold metrics",
        "tests": "interface tests",
        "run": "python src/run_all.py",
        "evidence": "E09_real_data_intake_gate",
        "package": "experiments/evidence/E09_real_data_intake_gate",
        "claim": "C12_real_qdm_nv_validation; C13_calibration_protocol_reality",
    },
]


def _metrics_summary(path: Path) -> tuple[str, str]:
    status = metrics_gate_status(path)
    if not path.exists():
        return "missing", status.gate
    data = json.loads(path.read_text(encoding="utf-8"))
    run_audit = data.get("run_audit") if isinstance(data, dict) else None
    if isinstance(run_audit, dict) and run_audit.get("fresh_full_run_completed") is True:
        return "fresh_full_run", status.gate
    if data.get("full_run_completed") is True:
        return "fresh_full_run", status.gate
    if data.get("run_mode") in {"scaffold", "interface"}:
        return str(data.get("run_mode")), status.gate
    return "preserved_or_fresh_artifact", status.gate


def main() -> int:
    graph = load_graph(ROOT)
    rows = [
        "# Old-To-New Migration Coverage Matrix",
        "",
        "| Old experiment | Old responsibility | Old gates | Old outputs | Old metrics | Old tests | Old run command | New evidence | New package | Migration status | Runnable status | Full-run status | Gaps | Required fixes |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    failures: list[str] = []
    for item in MAPPING:
        package = ROOT / item["package"]
        evidence = graph.experiments[item["evidence"]]
        runtime = evidence.get("runtime") or {}
        metrics_files = runtime.get("metrics_files", [])
        metrics_path = ROOT / metrics_files[0] if metrics_files else package / "outputs" / "metrics.json"
        run_mode, gate = _metrics_summary(metrics_path)
        report = package / "outputs" / "RUN_REPORT.md"
        old_path = OLD_ROOT / "experiments" / item["old"]
        old_outputs = "present" if (old_path / "outputs").exists() else "missing"
        migration = "covered" if package.exists() and report.exists() and metrics_path.exists() else "gap"
        runnable = "registered" if runtime.get("run_command") and runtime.get("test_command") else "missing command"
        status = evidence.get("status")
        full = "completed" if status == "passed" and run_mode == "fresh_full_run" else "not-fresh-full-audited"
        if status in {"partial", "planned", "passed_scaffold", "passed_interface"}:
            full = str(status)
        gaps = "-"
        fixes = "-"
        if migration != "covered":
            gaps = "contract files or outputs missing"
            fixes = "restore package outputs and metrics"
            failures.append(f"{item['evidence']}: migration gap")
        elif status in {"partial", "planned"}:
            gaps = "fresh full run not completed or evidence intentionally limited"
            fixes = "run full command or keep partial with explicit blocker"
        rows.append(
            "| `{old}` | {responsibility} | {gates} | {old_outputs} | {metrics} | {tests} | `{run}` | `{evidence}` | `{package}` | {migration} | {runnable} | {full} (`{gate}`) | {gaps} | {fixes} |".format(
                old=item["old"],
                responsibility=item["responsibility"],
                gates=item["gates"],
                old_outputs=old_outputs,
                metrics=item["metrics"],
                tests=item["tests"],
                run=item["run"],
                evidence=item["evidence"],
                package=item["package"],
                migration=migration,
                runnable=runnable,
                full=full,
                gate=gate,
                gaps=gaps,
                fixes=fixes,
            )
        )
    rows.append("")
    out = ROOT / "outputs" / "migration_coverage_matrix.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(rows), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
