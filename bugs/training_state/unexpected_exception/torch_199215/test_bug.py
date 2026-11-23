"""Known PyTorch bug signature — pytorch/pytorch#199215.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch
import pytest
from torch._dynamo.exc import BackendCompilerFailed
from torch._inductor import config

class M(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.idx=torch.nn.Parameter(torch.tensor([0,2]),requires_grad=False)
    def forward(self,x): return x[:,self.idx]*2

def test_known_bug_signature():
    m=M().eval();x=torch.arange(12.,dtype=torch.float32).reshape(3,4)
    expected=m(x)
    assert m.idx.dtype == torch.int64 and not m.idx.requires_grad
    torch.testing.assert_close(expected, torch.tensor([[0.,4.],[8.,12.],[16.,20.]]), rtol=0, atol=0)
    with torch.no_grad(), config.patch(freezing=True,freezing_discard_parameters=True):
        with pytest.raises(BackendCompilerFailed) as error:
            torch.compile(m,fullgraph=True)(x)

    assert any(isinstance(e, RuntimeError)
               and "only tensors of floating point dtype can require gradients" in str(e).lower()
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
