"""Regression signature for pytorch/pytorch issue #199941.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest

def test_known_bug_signature():
    a = torch.tensor([1., 2., 3.], requires_grad=True)
    torch.linalg.vander(a, N=3).sum().backward()
    torch.testing.assert_close(a.grad,torch.tensor([3.,5.,7.]),rtol=0,atol=0)
    b = torch.tensor([1., 2., 3.], requires_grad=True)
    with pytest.raises(RuntimeError, match="modified by an inplace operation"):
        torch.vander(b, N=3).sum().backward()
