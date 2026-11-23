"""PyTorch known bug signature, issue #198064.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

def scaled(x):
    return x * round(x.shape[0] * 5, -1)

def test_known_bug_signature():
    x = torch.ones(3)
    eager = scaled(x)
    assert eager.tolist() == [20.0] * 3  # round(15,-1) = 20
    compiled = torch.compile(scaled, backend='eager', dynamic=True)(x)
    assert compiled.tolist() == [15.0] * 3, f'Known SymInt.round issue did not reproduce: {compiled}'
