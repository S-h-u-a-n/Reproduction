"""Regression signature for pytorch/pytorch issue #199214.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
from torch._dynamo.exc import BackendCompilerFailed

def f(x):
    a = torch.dequantize(x)
    b = torch.trunc_(x)
    return a, b

def test_known_bug_signature():
    eager = f(torch.tensor([1.7]))
    assert all(torch.equal(t, torch.tensor([1.])) for t in eager)
    assert torch._C._is_alias_of(*eager)
    with pytest.raises(BackendCompilerFailed) as error:
        torch.compile(f, backend='inductor')(torch.tensor([1.7]))

    assert any(isinstance(e, AssertionError) and "n=copy_" in str(e)
               and "n.args[0]=dequantize" in str(e) for e in _exception_chain(error.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
