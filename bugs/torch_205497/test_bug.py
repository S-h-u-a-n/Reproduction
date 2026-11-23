"""Known-bug signature for pytorch/pytorch#205497 (CPU, torch 2.15.0).

Only the published small SGD numerical example. This test PASSES on the
reported fused optimizer error, not merely on successful execution.
"""

import torch


def _one_sgd_step(gradient, fused):
    parameter = torch.nn.Parameter(torch.zeros((2, 3), dtype=torch.float32))
    parameter.grad = gradient.t().contiguous().t()
    assert parameter.grad.stride() == (1, 2)
    assert not parameter.grad.is_contiguous()
    torch.optim.SGD([parameter], lr=1.0, fused=fused).step()
    return parameter.detach().clone()


def test_issue_205497():
    gradient = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    expected = -gradient
    reported_buggy = torch.tensor([[-1.0, -4.0, -2.0], [-5.0, -3.0, -6.0]])

    reference = _one_sgd_step(gradient, fused=False)
    observed = _one_sgd_step(gradient, fused=True)

    torch.testing.assert_close(reference, expected, rtol=0, atol=0)
    torch.testing.assert_close(observed, reported_buggy, rtol=0, atol=0)
    assert not torch.equal(observed, expected)
