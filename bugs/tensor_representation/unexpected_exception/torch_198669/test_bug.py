"""Regression signature for pytorch/pytorch issue #198669.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
from torch._dynamo.exc import BackendCompilerFailed

def model(a, b): return torch.softmax(torch.div(torch.eq(a, 2.0), b), 0)

def test_known_bug_signature():
    a = torch.arange(64., dtype=torch.float32).reshape(8, 8)
    b = torch.arange(1., 9., dtype=torch.float64)
    expected = model(a, b)
    assert expected.shape == (8, 8) and torch.isfinite(expected).all()
    with pytest.raises(BackendCompilerFailed) as error:
        torch.compile(model, backend='inductor')(a, b)

    assert any(isinstance(e, NotImplementedError) and "bool" in str(e)
               and "neg" in str(e).lower() for e in _exception_chain(error.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
