"""Regression signature for pytorch/pytorch issue #197810.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
from torch._inductor.exc import InductorError

def f(x): return x + float(x.shape[0] % 2 == 0)

def test_known_bug_signature():
    x = torch.arange(18., dtype=torch.float32).reshape(6, 3)
    assert torch.equal(f(x), x + 1)
    with pytest.raises(InductorError) as error:
        torch.compile(f, dynamic=True, fullgraph=True)(x)

    assert any(isinstance(e, AssertionError) and "ToFloat(False)" in str(e)
               for e in _exception_chain(error.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
