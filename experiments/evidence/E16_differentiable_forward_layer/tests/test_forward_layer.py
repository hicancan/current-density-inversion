from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for name in list(sys.modules):
    if name == "forward" or name.startswith("forward."):
        del sys.modules[name]
sys.path.insert(0, str(ROOT / "src"))
from forward.differentiable_biot_savart import BiotSavartForwardLayer, MU0, _check_torch_available

def rel_l2(a, b):
    return float(np.linalg.norm((a-b).ravel())/max(np.linalg.norm(b.ravel()),1e-30))

def test_current_reversal_antisymmetry():
    l = BiotSavartForwardLayer(32,32,1e-5,1e-5)
    Jx=np.full((32,32),10.0); Jy=np.full((32,32),5.0)
    Bp=l.sheet_to_B(Jx,Jy,-5e-5,1e-4); Bn=l.sheet_to_B(-Jx,-Jy,-5e-5,1e-4)
    assert np.max(np.abs(Bp[0]+Bn[0]))<1e-15
    assert np.max(np.abs(Bp[1]+Bn[1]))<1e-15
    assert np.max(np.abs(Bp[2]+Bn[2]))<1e-15

def test_superposition_linearity():
    l=BiotSavartForwardLayer(32,32,1e-5,1e-5)
    rng=np.random.RandomState(42)
    Ja_x,Ja_y=rng.randn(32,32)*5,rng.randn(32,32)*5
    Jb_x,Jb_y=rng.randn(32,32)*3,rng.randn(32,32)*3
    Ba=l.sheet_to_B(Ja_x,Ja_y,-5e-5,1e-4); Bb=l.sheet_to_B(Jb_x,Jb_y,-5e-5,1e-4)
    Bab=l.sheet_to_B(Ja_x+Jb_x,Ja_y+Jb_y,-5e-5,1e-4)
    for c in range(3): assert rel_l2(Bab[c],Ba[c]+Bb[c])<1e-12

def test_standoff_decay():
    l=BiotSavartForwardLayer(32,32,1e-5,1e-5)
    rng=np.random.RandomState(7)
    Jx,Jy=rng.randn(32,32)*10,rng.randn(32,32)*10
    pv=None
    for h in [2e-5,5e-5,1e-4,2e-4,5e-4]:
        B=l.sheet_to_B(Jx,Jy,-5e-5,h)
        v=float(np.max(np.sqrt(B[0]**2+B[1]**2+B[2]**2)))
        if pv is not None: assert pv>=v*0.999
        pv=v

def test_k0_handling_uniform_current():
    l=BiotSavartForwardLayer(32,32,1e-5,1e-5)
    Jy=np.full((32,32),100.0)
    B=l.sheet_to_B(np.zeros_like(Jy),Jy,-5e-5,1e-4)
    interior=B[0][8:-8,8:-8]; e=0.5*MU0*100
    assert np.abs(np.mean(interior)-e)<1e-6*abs(e)
    assert np.max(np.abs(B[1][8:-8,8:-8]))<1e-14
    assert np.max(np.abs(B[2][8:-8,8:-8]))<1e-14

def test_padding_cropping_documented():
    l=BiotSavartForwardLayer(32,32,1e-5,1e-5)
    rng=np.random.RandomState(99)
    Jx,Jy=rng.randn(32,32)*10,rng.randn(32,32)*10
    Bp=l.sheet_to_B(Jx,Jy,-5e-5,1e-4,padding_factor=2)
    Bn=l.sheet_to_B(Jx,Jy,-5e-5,1e-4,padding_factor=1)
    for c in range(3):
        assert Bp[c].shape==(32,32); assert Bn[c].shape==(32,32)
        assert np.all(np.isfinite(Bp[c])); assert np.all(np.isfinite(Bn[c]))
    Br=l.sheet_to_B(Jx,Jy,-5e-5,1e-4,padding_factor=2,return_padded=True)
    assert Br[0].shape==(64,64)

def test_multilayer_summation():
    l=BiotSavartForwardLayer(32,32,1e-5,1e-5)
    rng=np.random.RandomState(11)
    B1=l.sheet_to_B(rng.randn(32,32)*5,rng.randn(32,32)*5,-5e-5,1e-4)
    B2=l.sheet_to_B(rng.randn(32,32)*3,rng.randn(32,32)*3,-1e-4,1e-4)
    Bs=l.multilayer_sum_B([B1,B2])
    assert all(c.shape==(32,32) for c in Bs)

def test_via_bxy_strong():
    l=BiotSavartForwardLayer(32,32,1e-5,1e-5)
    sl=np.zeros((32,32)); sl[16,16]=0.001
    B=l.via_to_Bxy(sl,-1e-4,-3e-5,1e-4)
    assert np.max(np.sqrt(B[0]**2+B[1]**2))>1e-10

def test_via_bz_near_zero():
    l=BiotSavartForwardLayer(32,32,1e-5,1e-5)
    sl=np.zeros((32,32)); sl[16,16]=0.001; sl[21,19]=-0.0003
    B=l.via_to_Bxy(sl,-1e-4,-3e-5,1e-4)
    assert np.max(np.sqrt(B[0]**2+B[1]**2))>1e-12

def test_cpu_fallback_no_torch():
    l=BiotSavartForwardLayer(16,16,1e-6,1e-6)
    B=l.sheet_to_B(np.ones((16,16)),np.zeros((16,16)),-5e-6,1e-4)
    assert B[0].shape==(16,16) and np.all(np.isfinite(B[0])) and np.all(np.isfinite(B[1])) and np.all(np.isfinite(B[2]))

def test_torch_gradient_check():
    l=BiotSavartForwardLayer(16,16,1e-5,1e-5)
    if not l.torch_available:
        import pytest; pytest.skip("torch not available")
    import torch
    rng=np.random.RandomState(123)
    Jxn=rng.randn(16,16).astype(np.float64)*5; Jyn=rng.randn(16,16).astype(np.float64)*5
    Bn=l.sheet_to_B(Jxn.copy(),Jyn.copy(),-5e-5,1e-4)
    Jxt=torch.tensor(Jxn,dtype=torch.float64,requires_grad=True)
    Jyt=torch.tensor(Jyn,dtype=torch.float64,requires_grad=True)
    Bt=l.sheet_to_B_torch(Jxt,Jyt,-5e-5,1e-4)
    assert torch.allclose(Bt[0],torch.tensor(Bn[0]),rtol=1e-10,atol=1e-15)
    assert torch.allclose(Bt[1],torch.tensor(Bn[1]),rtol=1e-10,atol=1e-15)
    assert torch.allclose(Bt[2],torch.tensor(Bn[2]),rtol=1e-10,atol=1e-15)
    (Bt[0]**2+Bt[1]**2+Bt[2]**2).sum().backward()
    assert Jxt.grad is not None and torch.all(torch.isfinite(Jxt.grad))
    assert Jyt.grad is not None and torch.all(torch.isfinite(Jyt.grad))

def test_reference_outputs_pass_acceptance_gates():
    mp=ROOT/"outputs"/"metrics.json"
    assert mp.exists()
    m=json.loads(mp.read_text(encoding="utf-8"))
    assert m.get("all_acceptance_gates_passed") is True
    assert (ROOT/"outputs"/"RUN_REPORT.md").exists()
