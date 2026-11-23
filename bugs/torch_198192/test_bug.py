"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/198192 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch
import pytest


def guarded(x):
    try:
        return x.sum(dim=5)
    except IndexError:
        return x.sum(dim=-1)


def test_known_bug_signature():
    x = torch.ones(3, 4)
    expected = guarded(x)
    assert torch.equal(expected, torch.full((3,), 4.))
    compiled = torch.compile(guarded, backend='eager', fullgraph=True)
    with pytest.raises(
        IndexError,
        match=r"^Dimension out of range \(expected to be in range of \[-2, 1\], but got 5\)",
    ):
        compiled(x)
