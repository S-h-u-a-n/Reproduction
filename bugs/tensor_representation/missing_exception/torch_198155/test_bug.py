"""Regression signature for pytorch/pytorch issue #198155.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest

def f(x): return torch.softmax(x, dim=1)

def test_known_bug_signature():
    x = torch.tensor([[1,-2,3],[4,0,-6]], dtype=torch.int64)
    with pytest.raises(
        NotImplementedError,
        match=r"softmax_lastdim_kernel_impl.*not implemented for.*Long",
    ):
        f(x)
    got = torch.compile(f, backend='inductor')(x)
    assert isinstance(got, torch.Tensor)
    assert got.dtype == torch.int64 and got.shape == x.shape, 'Known issue: compiled integer softmax erroneously executes'
    assert torch.equal(got, torch.zeros_like(x))
