import torch
import torch.nn.functional as F


def test_issue_204478():
    # Deterministic float64 parameters: no RNG, including no manual_seed calls.
    dtype = torch.float64
    w1 = torch.tensor([[.3], [-.8], [1.2], [.7], [-.5], [.4]], dtype=dtype)
    b1 = torch.tensor([.2, -.1, .3, -.4, .5, .15], dtype=dtype)
    w2 = torch.tensor([[.6, -.2, .7, -.4, .3, .8]], dtype=dtype)
    x0 = torch.linspace(-1., 1., 8, dtype=dtype).reshape(-1, 1)

    def third_order_parameter_grad(use_builtin):
        bias = b1.clone().requires_grad_(True)
        x = x0.clone().requires_grad_(True)
        hidden = F.linear(x, w1, bias)
        if use_builtin:
            hidden = F.layer_norm(hidden, (6,), eps=1e-5)
        else:
            centered = hidden - hidden.mean(-1, keepdim=True)
            hidden = centered * torch.rsqrt(centered.square().mean(-1, keepdim=True) + 1e-5)
        output = F.linear(torch.tanh(hidden), w2)
        first, = torch.autograd.grad(output.sum(), x, create_graph=True)
        second, = torch.autograd.grad(first.sum(), x, create_graph=True)
        derivative, = torch.autograd.grad(second.sum(), bias)
        return derivative

    correct = third_order_parameter_grad(False)
    actual = third_order_parameter_grad(True)
    assert torch.isfinite(correct).all().item() and torch.isfinite(actual).all().item()
    assert abs(correct.sum().item()) < 1e-8, "Translation invariance control failed"
    assert abs(actual.sum().item()) > 1e-2, "Expected layer_norm third-order gradient to violate translation invariance"
    assert (actual - correct).abs().max().item() > 1e-2
