"""Known PyTorch bug signature — pytorch/pytorch#197399.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch
import pytest

def f(base):
    y=base[1:,0]
    x=torch.empty(0)
    x.set_(y)
    return x[0]

def test_known_bug_signature():
    base=torch.tensor([[0.,1.],[2.,3.]],dtype=torch.float32)
    view = base[1:, 0]
    rebound = torch.empty(0)
    rebound.set_(view)
    assert rebound.shape == view.shape == (1,)
    assert rebound.stride() == view.stride() == (2,)
    assert rebound.storage_offset() == view.storage_offset() == 2
    assert torch._C._is_alias_of(rebound, base)
    assert f(base.clone()).item()==2.0
    with pytest.raises(IndexError) as error:
        torch.compile(f,backend='inductor')(base.clone())

    message = str(error.value)
    assert "getitem" in message
    assert "index 0 is out of bounds for dimension 0 with size 0" in message
    assert any(isinstance(e, IndexError) for e in _exception_chain(error.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
