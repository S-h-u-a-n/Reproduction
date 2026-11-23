"""Known PyTorch bug signature — pytorch/pytorch#198081.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch

def f(x): return torch.any(x)*200+100

def test_known_bug_signature():
    x=torch.tensor([[0,3],[0,0]],dtype=torch.uint8)
    e=f(x)
    assert e.dtype==torch.uint8 and e.item()==44
    got=torch.compile(f,backend='inductor')(x)
    assert got.dtype==torch.int64 and got.item()==300, 'Known issue: compiled uint8 any yields different arithmetic'
