import sys; from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np
from run_all import BASELINES, CHANNEL_NAMES, LAYER_IDS, build_forward_operator, gates_fn, eval_all, generate_all_cases, run_experiment

def _cfg():
    return {"seed":20260504,"layer_depths":{"L1":-0.02,"L2":-0.08,"L3":-0.16,"L4":-0.26},"grid_size":8,"sensor_grid_size":10,"sensor_z":0.06,"in_plane_extent":[-0.32,0.32,-0.32,0.32],"families":["nominal_via_chain","no_via_hard_negative","dense_via_cluster","deep_layer_only","layer_misallocation_trap"],"variants_per_family":2,"seed_per_variant_step":7,"ridge_alpha":0.01,"kcl_constraint_weight":0.5}

def test_dataset_generated():
    A,vb=build_forward_operator(_cfg()); cases=generate_all_cases(_cfg(),A,vb); assert len(cases)==10

def test_channels_11():
    assert len(CHANNEL_NAMES)==11

def test_forward_shape():
    A,vb=build_forward_operator(_cfg()); assert A.shape==(300,704)

def test_baselines_finite():
    cfg=_cfg(); A,vb=build_forward_operator(cfg); cases=generate_all_cases(cfg,A,vb)
    for n,fn in BASELINES.items():
        for c in cases:
            p=fn(c,A,vb,cfg); assert bool(np.all(np.isfinite(p)))

def test_gates_pass():
    cfg=_cfg(); A,vb=build_forward_operator(cfg); cases=generate_all_cases(cfg,A,vb)
    be=eval_all(cases,A,vb,cfg)
    m={"case_count":len(cases),"family_count":5,"output_channels":11}
    gates=gates_fn(m,be,cfg); assert gates["all_acceptance_gates_passed"]

def test_run_writes_outputs(tmp_path):
    m=run_experiment(_cfg(),tmp_path/"outputs")
    assert m["all_acceptance_gates_passed"]
    assert (tmp_path/"outputs"/"metrics.json").exists()
    assert (tmp_path/"outputs"/"RUN_REPORT.md").exists()
