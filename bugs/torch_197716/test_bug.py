"""Regression signature for pytorch/pytorch issue #197716.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
from torch._dynamo.exc import BackendCompilerFailed

def f(x, k): return x + float(k % 3)

def test_known_bug_signature():
    x = torch.arange(12., dtype=torch.float32).reshape(4, 3)
    expected = f(x, 5)
    assert torch.equal(expected, x + 2)
    with pytest.raises(BackendCompilerFailed) as error:
        torch.compile(f, dynamic=True, fullgraph=True)(x, 5)

    assert any(isinstance(e, AttributeError) and "TensorReferenceAnalysis" in str(e)
               and "python_mod" in str(e) for e in _exception_chain(error.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
