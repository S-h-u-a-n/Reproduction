"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/205823 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch
import pytest
import re
from torch._dynamo.exc import BackendCompilerFailed
from torch._inductor import config


class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = torch.nn.Parameter(torch.ones(2, 2, dtype=torch.bfloat16))
        self.scale = torch.nn.Parameter(torch.full((2,), 3., dtype=torch.bfloat16))

    def forward(self, x):
        y = torch.nn.functional.linear(x, self.weight)
        return y * self.scale.reciprocal()


def test_known_bug_signature():
    model = Model().eval()
    x = torch.ones(2, 2, 2, dtype=torch.bfloat16)
    with torch.no_grad(), config.patch(freezing=True, enable_linear_binary_folding=True):
        expected = model(x)
        assert torch.isfinite(expected).all()
        compiled = torch.compile(model, backend='inductor', fullgraph=True)
        with pytest.raises(BackendCompilerFailed, match=r"backend='inductor' raised") as exc:
            compiled(x)

    assert any(isinstance(e, RuntimeError)
               and re.search(r"Node reshape\w* referenced nonexistent value reciprocal\w*!", str(e))
               for e in _exception_chain(exc.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
