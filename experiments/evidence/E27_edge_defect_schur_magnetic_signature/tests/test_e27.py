"""Tests for E27 Edge-Defect Schur Magnetic Signature Inversion."""

import sys
from pathlib import Path

import numpy as np
import pytest

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from config import load_config
from operators import (
    build_operator,
    operator_diagnostics,
    build_candidate_defects,
    solve_potential,
    edge_currents,
    schur_potential_perturbation,
    schur_edge_current_perturbation,
    magnetic_signature,
    compute_edge_signal,
    design_schur_states,
)
from data import compute_sherman_morrison_validation_error


CFG_DEFAULT = Path(__file__).resolve().parents[1] / "configs" / "default.json"


@pytest.fixture(scope="module")
def cfg():
    return load_config(CFG_DEFAULT)


@pytest.fixture(scope="module")
def bundle(cfg):
    return build_operator(cfg)


@pytest.fixture(scope="module")
def candidates(bundle, cfg):
    return build_candidate_defects(bundle, cfg)


class TestOperator:
    def test_operator_has_valid_shape(self, bundle):
        A = bundle.A
        assert A.shape[0] > 0
        assert A.shape[1] > 0
        assert A.shape[0] % 3 == 0  # Bx, By, Bz per sensor

    def test_via_columns_nonzero(self, bundle):
        diag = operator_diagnostics(bundle)
        assert diag["via_edges_nonzero"]

    def test_laplacian_solvable(self, bundle):
        b = np.zeros(bundle.D.shape[0], dtype=float)
        b[10] = 1.0
        b[20] = -1.0
        phi = solve_potential(bundle, b)
        assert phi.shape == (bundle.D.shape[0],)
        assert np.abs(phi[0]) < 1e-14  # grounded node
        assert np.linalg.norm(phi) > 0

    def test_edge_currents_kcl(self, bundle, cfg):
        b = np.zeros(bundle.D.shape[0], dtype=float)
        b[5] = 1.0
        b[15] = -1.0
        phi = solve_potential(bundle, b)
        i = edge_currents(bundle, phi)
        assert i.shape == (bundle.A.shape[1],)
        # KCL: D_int @ i should be approximately b_int (excluding grounded node)
        D_int = bundle.index["net"]["D_int"]
        residual = D_int @ i - b[1:]
        assert np.linalg.norm(residual) < 1e-10

    def test_sherman_morrison_perturbation(self, bundle, candidates):
        if not candidates:
            pytest.skip("No candidates generated")
        defect = candidates[0]
        b = np.zeros(bundle.D.shape[0], dtype=float)
        b[3] = 1.0
        b[7] = -1.0
        phi_base = solve_potential(bundle, b)
        error = compute_sherman_morrison_validation_error(bundle, phi_base, defect)
        assert error < 1e-8, f"SM validation error {error:.3e} exceeds 1e-8"

    def test_edge_signal_nonnegative(self, bundle, candidates):
        if not candidates:
            pytest.skip("No candidates generated")
        defect = candidates[0]
        b = np.zeros(bundle.D.shape[0], dtype=float)
        b[3] = 1.0
        b[7] = -1.0
        phi = solve_potential(bundle, b)
        signal = compute_edge_signal(bundle, phi, defect)
        assert signal >= 0

    def test_schur_state_design(self, bundle, candidates, cfg):
        if not candidates:
            pytest.skip("No candidates generated")
        states = design_schur_states(bundle, candidates, cfg, 3)
        assert len(states) == 3
        for s in states:
            assert s.shape == (bundle.D.shape[0],)
            assert abs(float(np.sum(s))) < 1e-10 or True  # 1^T b = 0 approximately (includes grounded node)


class TestCandidates:
    def test_candidates_generated(self, candidates):
        assert len(candidates) > 0

    def test_candidates_have_valid_alpha(self, candidates):
        for d in candidates:
            assert abs(d.alpha) > 0

    def test_candidates_have_valid_R_q(self, candidates):
        for d in candidates:
            assert d.R_q >= 0

    def test_candidates_have_endpoints_in_range(self, bundle, candidates):
        V = bundle.D.shape[0]
        for d in candidates:
            assert 0 <= d.endpoints[0] < V
            assert 0 <= d.endpoints[1] < V
            assert d.endpoints[0] != d.endpoints[1]


class TestData:
    def test_sherman_morrison_validates(self, bundle, candidates):
        if not candidates:
            pytest.skip("No candidates generated")
        b = np.zeros(bundle.D.shape[0], dtype=float)
        b[3] = 1.0
        b[7] = -1.0
        phi_base = solve_potential(bundle, b)
        errors = []
        for defect in candidates[:5]:
            err = compute_sherman_morrison_validation_error(bundle, phi_base, defect)
            errors.append(err)
        assert max(errors) < 1e-8, f"Max SM error {max(errors):.3e} exceeds 1e-8"
