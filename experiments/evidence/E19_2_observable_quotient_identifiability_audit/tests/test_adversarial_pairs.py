"""Test adversarial pair generation and OQCI handling."""

from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def test_adversarial_pairs_generated():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from data import generate_adversarial_pairs

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    pairs = generate_adversarial_pairs(bundle, cfg)

    assert len(pairs) >= 1
    for pair in pairs:
        assert pair.forward_distance >= 0
        assert pair.label_a != pair.label_b


def test_adversarial_pairs_have_different_labels():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from data import generate_adversarial_pairs

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    pairs = generate_adversarial_pairs(bundle, cfg)

    label_pairs = [(p.label_a, p.label_b) for p in pairs]
    for la, lb in label_pairs:
        assert la != lb, "Adversarial pairs must have different labels"


def test_oracle_cases_consistent():
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
        assert len(result.consistent_hypotheses) >= 1, f"Oracle {h} empty consistent set"
        assert h in result.consistent_hypotheses, f"Oracle {h} truth not consistent"
