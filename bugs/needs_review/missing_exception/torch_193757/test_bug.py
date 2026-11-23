"""PyTorch known bug signature, issue #193757.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch
import torch.nn.functional as F
import pytest

def fn(target):
    return F.binary_cross_entropy(torch.ones_like(target),target)

def test_known_bug_signature():
    target = torch.full((4,4),1.5)
    with pytest.raises(RuntimeError,match=r"all elements of target should be between 0 and 1"):
        fn(target)
    got = torch.compile(fn,backend='inductor')(target)
    assert torch.isfinite(got).item(), f'Expected erroneous finite compiled BCE, got {got}'
    assert got.item() == -50., f'Expected BCE log-clamp formula on invalid target, got {got}'
