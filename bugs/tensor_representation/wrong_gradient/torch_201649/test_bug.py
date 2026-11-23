"""Known PyTorch bug signature — pytorch/pytorch#201649.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch

@torch.compiler.nested_compile_region
def region(a,b): return a*b

def fn(x,y):
    return region(x,x+1).sum()+region(y,y+1).sum()

def test_known_bug_signature():
    x=torch.arange(1.,17.).reshape(4,4)/7
    y=torch.arange(31.,47.).reshape(4,4)/11
    xc=x.detach().clone().requires_grad_()
    yc=y.detach().clone().requires_grad_()
    out = torch.compile(fn, backend='inductor', fullgraph=True)(xc, yc)
    torch.testing.assert_close(out, fn(x, y))
    out.backward()

    assert torch.allclose(yc.grad,2*y+1,rtol=0,atol=1e-5)
    # The first backward uses the second region's saved y + 1 in place of x + 1.
    torch.testing.assert_close(xc.grad, x + y + 1, rtol=0, atol=1e-5)
