"""Test claim interval computation."""

from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")


def test_interval_matrix_covers_all_pairs():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from hypotheses import build_all_hypothesis_bases, HYPOTHESES
    from quotient import consistent_set_for_case, compute_epsilon_from_policy
    from intervals import aggregate_claim_intervals
    from data import generate_cases

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    eps_values = compute_epsilon_from_policy(float(cfg["noise_sigma"]), bundle.A.shape[0], cfg["epsilon_policy"])
    eps = eps_values[0]
    cases = generate_cases(bundle, cfg)

    results = [consistent_set_for_case(c, bundle, bases, eps) for c in cases]
    intervals = aggregate_claim_intervals(results)

    matrix = intervals["interval_matrix"]
    for truth_h in HYPOTHESES:
        for claim_h in HYPOTHESES:
            key = f"{truth_h}__{claim_h}"
            assert key in matrix, f"Missing key {key}"
            assert matrix[key]["count"] > 0, f"Empty count for {key}"


def test_intervals_are_valid():
    import sys
    sys.path.insert(0, SRC)
    from config import load_config
    from operators import multi_height_operator_stack
    from hypotheses import build_all_hypothesis_bases, HYPOTHESES
    from quotient import consistent_set_for_case, compute_epsilon_from_policy
    from intervals import binary_claim_interval
    from data import generate_oracle_case

    cfg = load_config(ROOT / "configs" / "smoke.json")
    bundle = multi_height_operator_stack(cfg)
    bases = build_all_hypothesis_bases(bundle, cfg)
    eps_values = compute_epsilon_from_policy(float(cfg["noise_sigma"]), bundle.A.shape[0], cfg["epsilon_policy"])
    eps = eps_values[0]
    rng = np.random.default_rng(int(cfg["random_seed"]))

    for truth_h in HYPOTHESES:
        case = generate_oracle_case(bundle, cfg, truth_h, rng, 0)
        result = consistent_set_for_case(case, bundle, bases, eps)
        stats = binary_claim_interval([result], truth_h, truth_h)
        assert stats["count"] == 1
        total = stats["forced_false"] + stats["forced_true"] + stats["unidentifiable"] + stats["empty_consistent"]
        assert total == stats["count"]
