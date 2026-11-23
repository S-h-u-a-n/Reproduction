import math
import torch
from torch.distributions import Normal, kl_divergence


def test_issue_201082():
    scale = torch.tensor(1e-4, dtype=torch.float16, requires_grad=True)
    p = Normal(torch.zeros_like(scale), scale)
    q = Normal(torch.zeros_like(scale), torch.ones_like(scale))
    loss = kl_divergence(p, q)
    (grad,) = torch.autograd.grad(loss, scale)
    s = scale.detach().double()
    reference_loss = (s.square() - 1) / 2 - s.log()
    reference_grad = s - 1 / s
    assert math.isfinite(reference_loss.item())
    assert math.isfinite(reference_grad.item())
    assert torch.isposinf(loss).item()
    assert torch.isneginf(grad).item()
