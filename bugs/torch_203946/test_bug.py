"""https://github.com/pytorch/pytorch/issues/203946 — unrecorded norm clamp."""

import torch
import torch.nn.functional as F


def test_issue_203946():
    x2 = torch.tensor([3., 4.], dtype=torch.float64)
    x1 = torch.tensor([2. ** -21, 0.], dtype=torch.float64, requires_grad=True)
    eps = 2. ** -20
    out = F.cosine_similarity(x1, x2, dim=0, eps=eps)
    (actual,) = torch.autograd.grad(out, (x1,))
    assert x1.norm().item() < eps < x2.norm().item()
    torch.testing.assert_close(out, torch.tensor(0.3, dtype=torch.float64), rtol=0, atol=1e-15)
    # In this open region the denominator is constant with respect to x1.
    expected = x2 / (eps * x2.norm())
    buggy = torch.tensor([314572.8, 838860.8], dtype=torch.float64)
    torch.testing.assert_close(actual, buggy, rtol=0, atol=1e-9)
    assert not torch.allclose(actual, expected, rtol=0, atol=1e-9)
    torch.testing.assert_close(
        expected, torch.tensor([629145.6, 838860.8], dtype=torch.float64),
        rtol=0, atol=1e-9,
    )
