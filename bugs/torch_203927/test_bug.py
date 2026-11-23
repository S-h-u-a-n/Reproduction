"""Regression signature for pytorch/pytorch issue #203927.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
from torch._dynamo.exc import UncapturedHigherOrderOpError, Unsupported

def test_known_bug_signature():
    x = torch.ones(3)
    g = torch.ones_like(x)
    _, vjp_fn = torch.func.vjp(torch.tanh, x)
    expected = g.clone()
    for _ in range(8):
        expected = g + vjp_fn(expected)[0]
    # u_0=1 and u_(k+1)=1+d*u_k, where d=tanh'(1).
    derivative = 1 - torch.tanh(x).square()
    reference = sum(derivative.pow(j) for j in range(9))
    torch.testing.assert_close(expected, reference, rtol=1e-6, atol=1e-6)
    with pytest.raises(UncapturedHigherOrderOpError) as error:
        torch.while_loop(lambda i,u: i < 8,
                         lambda i,u: (i + 1, g + vjp_fn(u)[0]),
                         (torch.tensor(0), g.clone()))

    assert "_autograd_grad" in str(error.value)
    assert any(isinstance(e, Unsupported) and "_autograd_grad" in str(e)
               and "grad_fn" in str(e) for e in _exception_chain(error.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
