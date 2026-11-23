"""Known PyTorch bug signature — pytorch/pytorch#198868.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch

def f(x):
    idx=torch.arange(2,device=x.device)[:0]
    return x.scatter(0,idx,torch.zeros(idx.shape,dtype=x.dtype,device=x.device))

def test_known_bug_signature():
    x=torch.tensor(7.)
    eager=f(x)
    compiled=torch.compile(f,backend='inductor',fullgraph=True)(x)
    assert eager.shape == torch.Size([]) and eager.item()==7.0
    assert compiled.shape == torch.Size([1]) and compiled[0].item()==7., 'Known issue: compiled scatter changes scalar shape'
