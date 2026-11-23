"""PyTorch known bug signature, issue #199258.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch
import pytest
from networkx import NetworkXError
from torch._dynamo.exc import BackendCompilerFailed
from torch.utils.checkpoint import checkpoint

def fn(x):
    return checkpoint(lambda t: t*1.0, x, use_reentrant=False)

def test_known_bug_signature():
    x = torch.arange(1.,17.).reshape(4,4).requires_grad_()
    eager = fn(x)
    torch.testing.assert_close(eager, x, rtol=0, atol=0)
    eager.sum().backward()
    torch.testing.assert_close(x.grad,torch.ones_like(x))
    y = x.detach().clone().requires_grad_()
    compiled = torch.compile(fn, backend="inductor")
    with pytest.raises(BackendCompilerFailed, match=r"backend='inductor' raised:") as exc:
        compiled(y).sum().backward()
    cause = exc.value.__cause__ or exc.value.__context__
    assert isinstance(cause, NetworkXError)
    assert str(cause) == "node source not in graph"
