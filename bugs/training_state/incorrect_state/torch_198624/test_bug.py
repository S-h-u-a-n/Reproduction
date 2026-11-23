import torch


def test_issue_198624():
    def f(x):
        y = x.detach()
        y.add_(x)
        return y

    original = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    eager = f(original)
    assert torch.equal(eager.detach(), torch.tensor([2.0, 4.0, 6.0]))
    assert eager.requires_grad and eager.grad_fn is not None
    grad = torch.autograd.grad(eager.sum(), original)[0]
    torch.testing.assert_close(grad, torch.ones(3))

    other = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    compiled = torch.compile(f, backend="aot_eager")(other)
    assert torch.equal(compiled.detach(), eager.detach())
    assert compiled.requires_grad is False, "Expected AOT detached-alias history loss"
    assert compiled.grad_fn is None, "Expected missing grad_fn from detached alias replay"
