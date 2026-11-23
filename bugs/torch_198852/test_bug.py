"""Known PyTorch bug signature — pytorch/pytorch#198852.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch

def f(x,y):
    empty=torch.empty((0,2),dtype=torch.float64,device=x.device)
    return torch.cat((empty,x,y),dim=0)

def test_known_bug_signature():
    x=torch.tensor([[1.,2.]],dtype=torch.float32)
    y=torch.tensor([[3.,4.]],dtype=torch.float32)
    eager=f(x,y)
    got=torch.compile(f,backend='inductor',fullgraph=True)(x,y)
    assert eager.dtype==torch.float64 and eager.shape==(2,2)
    assert torch.equal(got.to(torch.float64),eager)
    assert got.dtype==torch.float32, 'Known issue: compiled cat loses float64 dtype promotion'
