import pytest
import torch

def test_issue_197887():
    def f(x, w):
        return x @ w

    x = torch.arange(6.0).reshape(2, 3) / 7
    w = (torch.arange(9.0).reshape(3, 3) / 5).requires_grad_()
    correct_forward_gradient = x.t() @ torch.ones(2, 3)
    eager_x = x.clone()
    eager_w = w.detach().clone().requires_grad_()
    eager_out = f(eager_x, eager_w)
    eager_x.add_(1)
    with pytest.raises(RuntimeError, match="modified by an inplace operation"):
        eager_out.sum().backward()

    compiled_x = x.clone()
    compiled_w = w.detach().clone().requires_grad_()
    out = torch.compile(f, backend="inductor")(compiled_x, compiled_w)
    compiled_x.add_(1)
    out.sum().backward()
    wrong_gradient = compiled_w.grad
    expected_wrong = (x + 1).t() @ torch.ones(2, 3)
    torch.testing.assert_close(wrong_gradient, expected_wrong)
    assert not torch.allclose(wrong_gradient, correct_forward_gradient)
