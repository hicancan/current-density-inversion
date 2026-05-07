"""Test operator gap metric computation."""

import numpy as np

from gap_metrics import (
    FieldGap,
    compute_field_gap,
    compute_all_gaps,
    compute_unit_sanity,
)


def test_compute_field_gap_zero():
    """Same field should have zero gap."""
    n = 16
    B = np.random.default_rng(0).normal(size=(n, n, 3))
    gap = compute_field_gap(B, B, dx_m=1e-6, pair_name="self")
    assert gap.rel_rmse < 1e-12
    assert gap.sign_match_rate == 1.0


def test_compute_field_gap_nonzero():
    """Different fields should have nonzero gap."""
    n = 16
    rng = np.random.default_rng(1)
    B_a = rng.normal(size=(n, n, 3))
    B_b = rng.normal(size=(n, n, 3)) * 1.5
    gap = compute_field_gap(B_a, B_b, dx_m=1e-6, pair_name="a_vs_b")
    assert gap.rel_rmse > 0
    assert gap.raw_l2_diff > 0


def test_compute_field_gap_per_component():
    """Per-component metrics should be present."""
    n = 16
    rng = np.random.default_rng(2)
    B_a = rng.normal(size=(n, n, 3))
    B_b = rng.normal(size=(n, n, 3))
    gap = compute_field_gap(B_a, B_b, dx_m=1e-6, pair_name="test")
    assert "Bx" in gap.per_component_rel_rmse
    assert "By" in gap.per_component_rel_rmse
    assert "Bz" in gap.per_component_rel_rmse


def test_compute_all_gaps():
    n = 16
    rng = np.random.default_rng(3)
    maps = {
        "op_a": rng.normal(size=(n, n, 3)),
        "op_b": rng.normal(size=(n, n, 3)) * 1.2,
        "op_c": rng.normal(size=(n, n, 3)) * 0.8,
    }
    gaps = compute_all_gaps(maps, dx_m=1e-6)
    assert len(gaps) == 3  # 3 choose 2 = 3 pairs
    for g in gaps:
        assert g.rel_rmse >= 0


def test_unit_sanity():
    n = 16
    rng = np.random.default_rng(4)
    maps = {
        "op_a": rng.normal(size=(n, n, 3)),
        "op_b": rng.normal(size=(n, n, 3)),
    }
    result = compute_unit_sanity(maps)
    assert result["same_shape"] is True
    assert result["count"] == 2


def test_unit_sanity_mismatch():
    rng = np.random.default_rng(5)
    maps = {
        "op_a": rng.normal(size=(16, 16, 3)),
        "op_b": rng.normal(size=(24, 24, 3)),
    }
    result = compute_unit_sanity(maps)
    assert result["same_shape"] is False


# --- Round 2: Mechanism decision tests ---

def test_generate_mechanism_currents():
    from decision_stability import generate_mechanism_currents
    rng = np.random.default_rng(42)
    currents, labels = generate_mechanism_currents(10, 4, 10.0, rng)
    assert currents.shape == (40, 4)
    assert labels.shape == (40,)
    assert set(labels) == {0, 1, 2, 3}
    # H0 should have near-zero via current
    h0_mask = labels == 0
    via_col = 2
    assert np.all(np.abs(currents[h0_mask, via_col]) < 1e-12)


def test_run_mechanism_decision_stress():
    from decision_stability import run_mechanism_decision_stress
    import numpy as np
    from operators_centerline import make_grid
    from config import GridConfig

    cfg = GridConfig(n=8, fov_um=200.0, measurement_z_um=50.0)
    X, Y, Z, points = make_grid(cfg)

    L = 100e-6
    segments = [
        (np.array([-L, 0.0, 0.0]), np.array([L, 0.0, 0.0]), "I_L1"),
        (np.array([0.0, -L, 0.0]), np.array([0.0, L, 0.0]), "I_L2"),
        (np.array([L, 0.0, 0.0]), np.array([L, 0.0, -50e-6]), "I_via"),
    ]

    rng = np.random.default_rng(42)
    results = run_mechanism_decision_stress(
        points, segments,
        op_names=["centerline_biot_savart", "deep_layer_shift_surrogate"],
        n_per_class=8, current_max_mA=10.0, noise_std_uT=0.0, rng=rng,
    )

    assert len(results) >= 1
    for op_name, mr in results.items():
        assert 0.0 <= mr.same_operator_accuracy <= 1.0
        assert 0.0 <= mr.false_via_rate <= 1.0
        assert len(mr.confusion_matrix) > 0
        # Cross-operator accuracy should differ from same-operator when testing
        # the deep_layer_shift (which has real physics perturbation)
        if op_name == "centerline_biot_savart" and "deep_layer_shift_surrogate" in mr.cross_operator_accuracy:
            cross_acc = mr.cross_operator_accuracy["deep_layer_shift_surrogate"]
            assert cross_acc <= mr.same_operator_accuracy + 0.1, \
                f"Cross-operator acc {cross_acc:.3f} should be <= same-op acc {mr.same_operator_accuracy:.3f}"


# --- Round 3: Template evidence scorer tests ---

def test_template_scorer_fit_predict():
    from decision_stability import TemplateEvidenceScorer
    import numpy as np
    rng = np.random.default_rng(99)
    # Separable data with non-colinear class centers (orthogonal directions)
    X = np.vstack([
        rng.normal(loc=[3, 0], scale=0.3, size=(20, 2)),
        rng.normal(loc=[0, 3], scale=0.3, size=(20, 2)),
    ])
    y = np.array([0] * 20 + [1] * 20)

    scorer = TemplateEvidenceScorer()
    scorer.fit(X, y)
    pred = scorer.predict(X)
    acc = float(np.mean(pred == y))
    assert acc >= 0.90, f"Template scorer should achieve >= 0.90 on separable data, got {acc:.3f}"
    assert scorer.n_classes_ == 2
    assert scorer.templates_.shape == (2, 2)


def test_template_scorer_cross_operator():
    from decision_stability import TemplateEvidenceScorer
    import numpy as np
    rng = np.random.default_rng(100)
    # Train templates on operator A: separable non-colinear classes
    X_A = np.vstack([
        rng.normal(loc=[3, 0], scale=0.3, size=(20, 2)),
        rng.normal(loc=[0, 3], scale=0.3, size=(20, 2)),
    ])
    y_A = np.array([0] * 20 + [1] * 20)

    # Test data from operator B (shifted class centers)
    X_B = np.vstack([
        rng.normal(loc=[2, 0], scale=0.3, size=(20, 2)),   # class 0 contracted
        rng.normal(loc=[0, 2], scale=0.3, size=(20, 2)),   # class 1 contracted
    ])
    y_B = np.array([0] * 20 + [1] * 20)

    scorer = TemplateEvidenceScorer()
    scorer.fit(X_A, y_A)

    # Same-operator accuracy
    pred_same = scorer.predict(X_A)
    acc_same = float(np.mean(pred_same == y_A))
    assert acc_same >= 0.90

    # Cross-operator: build templates from A
    op_templates = {0: X_A[y_A == 0].mean(axis=0), 1: X_A[y_A == 1].mean(axis=0)}
    pred_cross = scorer.predict_cross_operator(X_B, op_templates)
    acc_cross = float(np.mean(pred_cross == y_B))
    # Cross-operator accuracy should be lower due to shift
    assert acc_cross <= acc_same, f"Cross {acc_cross:.3f} should be <= same {acc_same:.3f}"


def test_run_template_mechanism_stress():
    from decision_stability import run_template_mechanism_stress
    import numpy as np
    from operators_centerline import make_grid
    from config import GridConfig

    cfg = GridConfig(n=8, fov_um=200.0, measurement_z_um=50.0)
    X, Y, Z, points = make_grid(cfg)

    L = 100e-6
    segments = [
        (np.array([-L, 0.0, 0.0]), np.array([L, 0.0, 0.0]), "I_L1"),
        (np.array([0.0, -L, 0.0]), np.array([0.0, L, 0.0]), "I_L2"),
        (np.array([L, 0.0, 0.0]), np.array([L, 0.0, -50e-6]), "I_via"),
    ]

    rng = np.random.default_rng(42)
    results = run_template_mechanism_stress(
        points, segments,
        op_names=["centerline_biot_savart", "deep_layer_shift_surrogate"],
        n_per_class=8, current_max_mA=10.0, noise_std_uT=0.0, rng=rng,
    )

    assert len(results) >= 1
    for op_name, tr in results.items():
        assert tr.scorer_name == "template_evidence"
        assert 0.0 <= tr.same_operator_accuracy <= 1.0
        assert 0.0 <= tr.false_via_rate <= 1.0
        assert len(tr.confusion_matrix) > 0
        # Verify cross-operator metrics exist
        assert len(tr.cross_operator_accuracy) >= 1
        assert len(tr.instability_ratio) >= 1


# --- Round 4: Ridge evidence scorer tests ---

def test_ridge_evidence_scorer_fit_predict():
    from decision_stability import RidgeEvidenceScorer
    import numpy as np
    rng = np.random.default_rng(101)
    X = np.vstack([
        rng.normal(loc=[3, 0], scale=0.3, size=(20, 2)),
        rng.normal(loc=[0, 3], scale=0.3, size=(20, 2)),
    ])
    y = np.array([0] * 20 + [1] * 20)

    scorer = RidgeEvidenceScorer()
    scorer.fit(X, y)
    assert scorer.best_lambda > 0
    assert scorer.n_classes_ == 2

    pred = scorer.predict(X)
    acc = float(np.mean(pred == y))
    assert acc >= 0.80, f"Ridge scorer should achieve >= 0.80, got {acc:.3f}"


def test_ridge_evidence_scorer_margin():
    from decision_stability import RidgeEvidenceScorer
    import numpy as np
    rng = np.random.default_rng(102)
    X = np.vstack([
        rng.normal(loc=[3, 0], scale=0.3, size=(20, 2)),
        rng.normal(loc=[0, 3], scale=0.3, size=(20, 2)),
    ])
    y = np.array([0] * 20 + [1] * 20)

    scorer = RidgeEvidenceScorer()
    scorer.fit(X, y)
    margins = scorer.decision_margin(X)
    assert margins.shape == (40,)
    assert np.all(margins >= 0), "Margins should be non-negative"


def test_run_ridge_evidence_stress():
    from decision_stability import run_ridge_evidence_stress
    import numpy as np
    from operators_centerline import make_grid
    from config import GridConfig

    cfg = GridConfig(n=8, fov_um=200.0, measurement_z_um=50.0)
    X, Y, Z, points = make_grid(cfg)

    L = 100e-6
    segments = [
        (np.array([-L, 0.0, 0.0]), np.array([L, 0.0, 0.0]), "I_L1"),
        (np.array([0.0, -L, 0.0]), np.array([0.0, L, 0.0]), "I_L2"),
        (np.array([L, 0.0, 0.0]), np.array([L, 0.0, -50e-6]), "I_via"),
    ]

    rng = np.random.default_rng(42)
    ridge_res, margin_res = run_ridge_evidence_stress(
        points, segments,
        op_names=["centerline_biot_savart", "deep_layer_shift_surrogate"],
        n_per_class=8, current_max_mA=10.0, noise_std_uT=0.0, rng=rng,
    )

    assert len(ridge_res) >= 1
    assert len(margin_res) >= 1
    for op_name, rr in ridge_res.items():
        assert rr.scorer_name == "ridge_evidence"
        assert rr.best_lambda > 0
        assert 0.0 <= rr.same_operator_accuracy <= 1.0
        assert len(rr.confusion_matrix_same) > 0
        assert len(rr.cross_operator_accuracy) >= 1
    for op_name, mr in margin_res.items():
        assert mr.margin_threshold >= 0
        assert 0.0 <= mr.accepted_rate_same <= 1.0
        assert len(mr.accepted_rate_cross) >= 1


# --- Round 5: Multi-basis and margin-shift certificate tests ---

def test_multibasis_scorer_fit_predict():
    from decision_stability import MultiBasisEvidenceScorer
    import numpy as np
    rng = np.random.default_rng(200)
    X = np.vstack([
        rng.normal(loc=[3, 0, 0, 0, 0], scale=0.3, size=(20, 5)),
        rng.normal(loc=[0, 3, 0, 0, 0], scale=0.3, size=(20, 5)),
    ])
    y = np.array([0] * 20 + [1] * 20)

    scorer = MultiBasisEvidenceScorer(k_components=2)
    scorer.fit(X, y)
    assert scorer.effective_k_ >= 1
    assert scorer.n_classes_ == 2

    pred = scorer.predict(X)
    acc = float(np.mean(pred == y))
    assert acc >= 0.80, f"Multi-basis should achieve >= 0.80, got {acc:.3f}"


def test_multibasis_scorer_margin():
    from decision_stability import MultiBasisEvidenceScorer
    import numpy as np
    rng = np.random.default_rng(201)
    X = np.vstack([
        rng.normal(loc=[3, 0, 0], scale=0.3, size=(20, 3)),
        rng.normal(loc=[0, 3, 0], scale=0.3, size=(20, 3)),
    ])
    y = np.array([0] * 20 + [1] * 20)

    scorer = MultiBasisEvidenceScorer(k_components=2)
    scorer.fit(X, y)
    margins = scorer.decision_margin(X)
    assert margins.shape == (40,)
    assert np.all(margins >= 0)


def test_margin_shift_certificate():
    from decision_stability import compute_margin_shift_certificate
    import numpy as np
    from operators_centerline import make_grid
    from config import GridConfig

    cfg = GridConfig(n=8, fov_um=200.0, measurement_z_um=50.0)
    X, Y, Z, points = make_grid(cfg)

    L = 100e-6
    segments = [
        (np.array([-L, 0.0, 0.0]), np.array([L, 0.0, 0.0]), "I_L1"),
        (np.array([0.0, -L, 0.0]), np.array([0.0, L, 0.0]), "I_L2"),
        (np.array([L, 0.0, 0.0]), np.array([L, 0.0, -50e-6]), "I_via"),
    ]

    rng = np.random.default_rng(42)
    cert = compute_margin_shift_certificate(
        points, segments,
        op_names=["centerline_biot_savart", "deep_layer_shift_surrogate", "missing_return_surrogate"],
        n_per_class=8, current_max_mA=10.0, rng=rng,
    )

    assert cert.interclass_delta_min > 0
    assert cert.operator_shift_radius_max > 0
    assert cert.gap_to_margin_ratio > 0
    assert isinstance(cert.stable_classification_possible_by_margin, bool)
    assert len(cert.interclass_delta_by_pair) > 0
    assert len(cert.operator_shift_radius_by_hypothesis) > 0


def test_run_multibasis_stress():
    from decision_stability import run_multibasis_stress
    import numpy as np
    from operators_centerline import make_grid
    from config import GridConfig

    cfg = GridConfig(n=8, fov_um=200.0, measurement_z_um=50.0)
    X, Y, Z, points = make_grid(cfg)

    L = 100e-6
    segments = [
        (np.array([-L, 0.0, 0.0]), np.array([L, 0.0, 0.0]), "I_L1"),
        (np.array([0.0, -L, 0.0]), np.array([0.0, L, 0.0]), "I_L2"),
        (np.array([L, 0.0, 0.0]), np.array([L, 0.0, -50e-6]), "I_via"),
    ]

    rng = np.random.default_rng(42)
    results = run_multibasis_stress(
        points, segments,
        op_names=["centerline_biot_savart", "deep_layer_shift_surrogate"],
        n_per_class=8, current_max_mA=10.0, noise_std_uT=0.0, k_components=2, rng=rng,
    )

    assert len(results) >= 1
    for op_name, mr in results.items():
        assert mr.scorer_name == "multibasis_evidence"
        assert mr.k_components >= 1
        assert 0.0 <= mr.same_operator_accuracy <= 1.0
        assert len(mr.confusion_matrix_same) > 0
        assert len(mr.cross_operator_accuracy) >= 1
        assert mr.cross_operator_drop >= -1.0
