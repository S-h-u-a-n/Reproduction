"""Known PyTorch bug signature — pytorch/pytorch#203852.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch
import pytest

def test_known_bug_signature():
    x=torch.zeros(2,2,dtype=torch.int64)
    idx=torch.tensor([1])
    src=torch.full((1,2),4,dtype=torch.int64)
    got=x.index_add(0,idx,src,alpha=2.5)
    assert got.tolist()==[[0,0],[8,8]], 'Known issue: integer index_add silently truncates float alpha'
    z=torch.zeros(3,dtype=torch.int64).index_add(0,torch.tensor([0,1]),torch.tensor([4,4]),alpha=0.5)
    assert torch.equal(z,torch.zeros(3,dtype=torch.int64))
    with pytest.raises(RuntimeError,match=r"[Ff]or integral input tensors, argument alpha must not be a floating point number"):
        torch.add(torch.zeros(2,dtype=torch.int64),torch.tensor([4,4]),alpha=2.5)
