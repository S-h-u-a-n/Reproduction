"""PyTorch known bug signature, issue #203806.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

def swap(a, b):
    torch._foreach_copy_([a, b], [b.clone(), a.clone()])

def test_known_bug_signature():
    a = torch.zeros(3)
    b = torch.ones(3)
    swap(a, b)
    assert a.tolist() == [1.0]*3 and b.tolist() == [0.0]*3
    a = torch.zeros(3)
    b = torch.ones(3)
    torch.compile(swap, backend='inductor')(a,b)
    assert a.tolist() == [1.0]*3
    assert b.tolist() == [1.0]*3, f'Known foreach-copy aliasing bug did not reproduce: b={b}'
