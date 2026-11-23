"""PyTorch known bug signature, issue #198071.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

def fn(t):
    return torch.clamp(t,max=300)

def test_known_bug_signature():
    x = torch.tensor([-128,-3,0,5,127],dtype=torch.int8)
    compiled = torch.compile(fn,backend='inductor')(x)
    assert compiled.tolist()==[-128,-3,0,5,44], f'Known int8 clamp overflow issue absent: {compiled.tolist()}'
    # Target 2.15.0+cpu keeps x; do not swallow other versions' errors.
    eager = fn(x.clone())
    torch.testing.assert_close(eager, x, rtol=0, atol=0)
    assert compiled.shape == x.shape and compiled.dtype == torch.int8
