import pytest
from torch._dynamo.exc import TorchRuntimeError
import torch

def test_issue_197097():
    x = torch.empty((0, 5))  # zero elements, no uninitialized values read
    def fn(t):
        return torch.linalg.vector_norm(t, ord=float("inf"), dim=-1)
    eager = fn(x)
    assert x.shape == (0, 5) and x.shape[-1] == 5
    assert eager.shape == (0,) and eager.dtype == x.dtype
    positive = torch.compile(
        lambda t: torch.linalg.vector_norm(t, ord=float("inf"), dim=1),
        backend="eager", fullgraph=True)(x)
    torch.testing.assert_close(positive, eager, rtol=0, atol=0)
    with pytest.raises(TorchRuntimeError) as error:
        torch.compile(fn, backend="eager", fullgraph=True)(x)

    message = str(error.value)
    assert "vector_norm" in message and "inf norm" in message
    assert "dimension -1" in message and "empty" in message
