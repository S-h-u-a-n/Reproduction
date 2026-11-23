"""PyTorch known bug signature, issue #201947.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

def test_known_bug_signature():
    for op in (torch.asinh,torch.acosh):
        x = torch.tensor(1000.,dtype=torch.float16,requires_grad=True)
        y = op(x)
        y.backward()
        exact = 1.0 / ((1000.0**2 + (1 if op is torch.asinh else -1))**0.5)
        assert torch.isfinite(y).item() and exact > 0.00099
        assert x.grad.item() == 0.0, f'Known {op.__name__} backward issue absent: grad={x.grad}'
