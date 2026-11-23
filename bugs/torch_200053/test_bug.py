"""PyTorch known bug signature, issue #200053.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch
import pytest

def test_known_bug_signature():
    p = torch.nn.Parameter(torch.ones(2))
    with pytest.raises(ValueError):
        torch.optim.Adadelta([p], rho=1.5)
    opt = torch.optim.RMSprop([p], alpha=1.5)
    p.grad = torch.ones(2)
    opt.step()
    square_avg = opt.state[p]['square_avg']
    torch.testing.assert_close(square_avg,torch.full_like(p,-0.5),rtol=0,atol=0)
    assert torch.isnan(p).all(), f'Expected invalid alpha to produce NaN weights, got {p}'
