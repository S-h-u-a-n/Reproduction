"""Known PyTorch bug signature — pytorch/pytorch#197089.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch

def calc(fn,x):
    t=x.detach().clone().requires_grad_()
    y=fn(t)
    (g,)=torch.autograd.grad(y,t)
    return y,g

def test_known_bug_signature():
    x=torch.tensor([-2.,-1.,0.5,1.5,3.],dtype=torch.float32)*1e-30
    expected,eg=calc(torch.std,x)
    # Evaluate variance in float64 to avoid squaring underflow in float32.
    xd = x.double()
    centered = xd - xd.mean()
    reference_std = (centered.square().sum() / (x.numel()-1)).sqrt()
    reference_grad = centered / ((x.numel()-1) * reference_std)
    torch.testing.assert_close(expected, reference_std.float(), rtol=1e-5, atol=0)
    torch.testing.assert_close(eg, reference_grad.float(), rtol=1e-5, atol=1e-7)
    assert expected.item()>0 and torch.isfinite(eg).all() and eg.abs().max().item()>0.01
    got,gg=calc(torch.compile(torch.std,backend='inductor'),x)
    assert got.item()==0. and torch.count_nonzero(gg)==0, 'Known bug: compiled std backward underflows'
