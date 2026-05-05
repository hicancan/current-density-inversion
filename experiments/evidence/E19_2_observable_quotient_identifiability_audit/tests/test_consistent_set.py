"""Test consistent set construction."""

from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def test_consistent_set_nonempty_oracle():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from hypotheses import build_all_hypothesis_bases
    from quotient import consistent_set_for_case, compute_epsilon_from_policy
    from data import generate_oracle_case

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    eps_values = compute_epsilon_from_policy(float(cfg["noise_sigma"]), bundle.A.shape[0], cfg["epsilon_policy"])
    eps = eps_values[0]
    rng = np.random.default_rng(int(cfg["random_seed"]))

    for h in ["H0_no_via", "H1_via", "H2_model_gap", "H3_return_path"]:
        case = generate_oracle_case(bundle, cfg, h, rng, 0)
        result = consistent_set_for_case(case, bundle, bases, eps)
        assert h in result.consistent_hypotheses, f"Oracle {h} must be in consistent set"
        assert len(result.consistent_hypotheses) >= 1


def test_more_flexible_hypothesis_has_lower_residual():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from hypotheses import build_all_hypothesis_bases
    from quotient import fit_hypothesis, compute_epsilon_from_policy
    from data import generate_oracle_case

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    eps_values = compute_epsilon_from_policy(float(cfg["noise_sigma"]), bundle.A.shape[0], cfg["epsilon_policy"])
    eps = eps_values[0]
    rng = np.random.default_rng(int(cfg["random_seed"]))

    case = generate_oracle_case(bundle, cfg, "H0_no_via", rng, 0)
    y = case.field_observed

    # H1 (more dof) should fit at least as well as H0 (fewer dof)
    h0_fit = fit_hypothesis(y, bases["H0_no_via"], eps)
    h1_fit = fit_hypothesis(y, bases["H1_via"], eps)
    # H1's residual should not be larger (more dof should fit as well or better)
    assert h1_fit.residual <= h0_fit.residual * 1.01 or h0_fit.residual < 1e-6
    assert h1_fit.effective_dof >= h0_fit.effective_dof
