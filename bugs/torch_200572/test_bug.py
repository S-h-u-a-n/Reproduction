"""Regression signature for pytorch/pytorch issue #200572.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch

class ScaleGradientIdentity(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x): return x.view_as(x)
    @staticmethod
    def backward(ctx, g): return g * 2

def f(x): return ScaleGradientIdentity.apply(x).unsqueeze(0)

def gradient(fn):
    x = torch.ones(4, requires_grad=True)
    fn(x).sum().backward()
    return x.grad

def test_known_bug_signature():
    want = gradient(f)
    assert torch.equal(want, torch.full((4,), 2.))
    got = gradient(torch.compile(f, backend='aot_eager'))
    assert torch.equal(got, torch.ones(4)), 'Known issue: custom Function backward is skipped after output view'
