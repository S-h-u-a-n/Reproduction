"""Known PyTorch bug signature — pytorch/pytorch#198994.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch
import torch.nn.functional as F

def f(x,y):
    return F.soft_margin_loss(x.sum(dim=1),y,reduction='none')

def test_known_bug_signature():
    x=torch.tensor([[0.25,0.5],[-0.5,0.25]],dtype=torch.float32)
    y=torch.tensor([1.,-1.],dtype=torch.float64)
    eager=f(x,y)
    assert eager.dtype==torch.float32
    compiled=torch.compile(f,backend='inductor',fullgraph=True)(x,y)
    assert compiled.shape==eager.shape
    assert compiled.dtype==torch.float64, 'Known issue: compiled mixed-dtype loss has wrong output dtype'
