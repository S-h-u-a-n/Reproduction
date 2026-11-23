"""Regression signature for pytorch/pytorch issue #192639.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import torch.autograd.forward_ad as fwAD
from torch._subclasses.functional_tensor import dispatch_functionalize

def probe(t): return fwAD.unpack_dual(t).tangent is not None

def test_known_bug_signature():
    x = torch.tensor([1., 2., 3., 4.])
    v = torch.ones(4)
    with fwAD.dual_level():
        dual = fwAD.make_dual(x, v)
        assert probe(dual) is True
        observed = dispatch_functionalize(probe)(dual)
        assert observed is False, 'Known issue: functionalization loses forward-AD tangent metadata'
