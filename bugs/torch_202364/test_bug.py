# Source: https://github.com/pytorch/pytorch/issues/202364
import torch


def test_issue_202364():
    def fn(x):
        a = x * 2
        b = a[1:]
        b.as_strided_((2,), (1,), 1)
        b.mul_(3)
        return a

    def run(backend):
        x = torch.tensor([1., 2., 3., 4.], requires_grad=True)
        out = torch.compile(fn, backend=backend)(x)
        out.sum().backward()
        return out.detach(), x.grad.detach()

    eager_out, eager_grad = run("eager")
    got_out, got_grad = run("inductor")
    expected_out = torch.tensor([2., 12., 18., 8.])
    torch.testing.assert_close(eager_out, expected_out, rtol=0, atol=0)
    torch.testing.assert_close(got_out, expected_out, rtol=0, atol=0)
    torch.testing.assert_close(eager_grad, torch.tensor([2., 6., 6., 2.]), rtol=0, atol=0)
    torch.testing.assert_close(got_grad, torch.tensor([2., 6., 6., 6.]), rtol=0, atol=0)
    assert not torch.equal(got_grad, eager_grad)
