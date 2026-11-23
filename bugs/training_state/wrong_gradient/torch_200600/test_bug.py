"""Known PyTorch bug signature — pytorch/pytorch#200600.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch
from torch.autograd import forward_ad as fw

def tangent_of_grad(wrt,create_graph=False):
    a0=torch.tensor([[2.]],dtype=torch.float64,requires_grad=True)
    b0=torch.tensor([[1.]],dtype=torch.float64,requires_grad=True)
    with fw.dual_level():
        a=fw.make_dual(a0,torch.ones_like(a0))
        out=torch.linalg.solve(a,b0)
        g,=torch.autograd.grad(out.sum(),{'A':a0,'B':b0}[wrt],create_graph=create_graph)
        tangent=fw.unpack_dual(g).tangent
        return None if tangent is None else tangent.detach().clone()

def test_known_bug_signature():
    good_b=tangent_of_grad('B',create_graph=True)
    good_a=tangent_of_grad('A',create_graph=True)
    assert good_b is not None and torch.allclose(good_b,torch.tensor([[-0.25]],dtype=torch.float64))
    assert good_a is not None and torch.allclose(good_a,torch.tensor([[0.25]],dtype=torch.float64))
    bad_b=tangent_of_grad('B')
    bad_a=tangent_of_grad('A')
    assert bad_b is None, 'Known issue: backward unexpectedly preserved A tangent for B gradient'
    assert bad_a is not None and torch.allclose(bad_a,torch.tensor([[0.125]],dtype=torch.float64)), 'Known issue: A gradient tangent is halved'
