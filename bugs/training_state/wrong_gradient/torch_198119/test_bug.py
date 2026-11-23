import torch
import torch.nn.functional as F

def test_issue_198119():
    def fn(x):
        return F.avg_pool1d(x, 3, stride=2, ceil_mode=True)
    x = torch.arange(6.0).reshape(1, 1, 6)
    eager = x.clone().requires_grad_()
    compiled = x.clone().requires_grad_()
    y_eager = fn(eager)
    y_compiled = torch.compile(fn, backend="inductor")(compiled)
    torch.testing.assert_close(y_eager, y_compiled)
    y_eager.sum().backward()
    y_compiled.sum().backward()
    reference = torch.tensor([1/3,1/3,2/3,1/3,5/6,1/2]).reshape_as(x)
    buggy = torch.tensor([1/3,1/3,2/3,1/3,2/3,1/3]).reshape_as(x)
    # Float32 fractions and a few additions: at most a few ULPs.
    torch.testing.assert_close(eager.grad, reference, rtol=0, atol=1e-6)
    torch.testing.assert_close(compiled.grad, buggy, rtol=0, atol=1e-6)
