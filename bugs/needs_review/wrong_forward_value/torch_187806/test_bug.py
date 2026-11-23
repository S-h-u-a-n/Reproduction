"""Known PyTorch bug signature — pytorch/pytorch#187806.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch
import torch.nn.functional as F
import math

def test_known_bug_signature():
    x=torch.tensor([-5.,-6.,-8.],dtype=torch.float32)
    actual=F.gelu(x,approximate='none')
    reference=0.5*x*torch.special.erfc(-x/(2.**0.5))
    # Independent scalar erfc avoids cancellation in 1+erf(x/sqrt(2)).
    scalar_reference = torch.tensor([0.5*v*math.erfc(-v/math.sqrt(2))
                                     for v in x.tolist()], dtype=x.dtype)
    # Float32 argument rounding is magnified in the tail; use relative
    # tolerance only so an underflowed zero can never pass this control.
    torch.testing.assert_close(reference, scalar_reference, rtol=1e-5, atol=0)
    assert torch.isfinite(reference).all()
    assert (reference < 0).all()
    assert reference[1].item()< -1e-9
    assert actual[1].item()==0. and actual[2].item()==0., 'Known issue: builtin GELU loses the representable negative tail'
    assert abs((actual[0]-reference[0]).item()) > 1e-7
