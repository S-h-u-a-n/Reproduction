"""Regression signature for pytorch/pytorch issue #205112.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
from torch.func import jacrev

def test_known_bug_signature():
    x = torch.tensor([[0.1, 0.7, -1.2], [2.4, -0.5, 0.3], [1.1, 1.9, 3.2], [-0.8, 2.2, 1.6]], dtype=torch.float64)
    y = torch.tensor([[1.7, -2.4, 0.5], [-1.3, 0.2, 1.8], [3.1, 0.6, -0.9], [0.0, -1.0, 2.4], [0.8, 3.4, -2.5]], dtype=torch.float64)
    def f(a): return torch.cdist(a, y, p=1.0)
    expected = torch.autograd.functional.jacobian(f, x)
    got = jacrev(f)(x)
    assert got.shape == expected.shape
    assert torch.isfinite(expected).all()
    torch.testing.assert_close(jacrev(f, chunk_size=1)(x), expected, rtol=0, atol=0)
    repeated_first = expected[0, 0].expand_as(expected)
    assert (expected - repeated_first).abs().max().item() == 2.0
    torch.testing.assert_close(got, repeated_first, rtol=0, atol=0)
