import pytest
import torch


def test_issue_204544():
    def f(x, w):
        return torch.sin(x @ w).sum()

    w_base = torch.arange(64, dtype=torch.float32).reshape(8, 8) / 128
    x = torch.arange(24, dtype=torch.float32).reshape(3, 8) / 64
    w_static = w_base.clone().requires_grad_(True)
    static_out = torch.compile(f, backend="inductor", dynamic=False)(x, w_static)
    static_out.backward(retain_graph=True)
    static_out.backward()
    assert w_static.grad is not None and torch.isfinite(w_static.grad).all().item()

    torch._dynamo.reset()
    w_dynamic = w_base.clone().requires_grad_(True)
    dynamic_out = torch.compile(f, backend="inductor", dynamic=True)(x, w_dynamic)
    with pytest.raises(RuntimeError, match="donated buffers|retain_graph"):
        dynamic_out.backward(retain_graph=True)
