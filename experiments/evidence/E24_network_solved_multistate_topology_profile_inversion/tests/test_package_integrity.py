"""Verify E24 package structure and basic imports."""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))


def test_imports():
    import graphs
    import network_solve
    import forward
    import profile_fit
    import margins
    import config
    import run_all
    assert True


def test_configs_exist():
    cfgs = Path(__file__).resolve().parent.parent / "configs"
    assert (cfgs / "smoke.json").exists()
    assert (cfgs / "default.json").exists()


def test_requirements():
    req = Path(__file__).resolve().parent.parent / "requirements.txt"
    assert req.exists()


def test_module_list():
    expected = [
        "__init__.py", "config.py", "graphs.py", "network_solve.py",
        "forward.py", "profile_fit.py", "margins.py", "run_all.py",
    ]
    for f in expected:
        assert (SRC / f).exists(), f"Missing: {f}"
