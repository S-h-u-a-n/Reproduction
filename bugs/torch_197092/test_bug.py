import pytest
from torch._dynamo.exc import TorchRuntimeError
import torch
import torch.nn.functional as F

def test_issue_197092():
    x = torch.arange(32.0).reshape(1, 2, 4, 4).requires_grad_()
    F.interpolate(x, scale_factor=2, mode="bilinear").sum().backward()
    torch.testing.assert_close(x.grad, torch.full_like(x, 4.), rtol=0, atol=0)
    x.grad = None
    with pytest.raises(TorchRuntimeError) as error:
        with torch._dynamo.compiled_autograd._enable(torch.compile(backend="eager")):
            F.interpolate(x, scale_factor=2, mode="bilinear").sum().backward()

    message = str(error.value)
    assert "UpsampleBilinear2DBackward0" in message
    assert "isIntList()" in message and "INTERNAL ASSERT FAILED" in message
    assert "IntList" in message and "GenericList" in message
