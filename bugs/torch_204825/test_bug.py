import math
import torch

def test_issue_204825():
    class Mul(torch.autograd.Function):
        @staticmethod
        def forward(ctx, x, w):
            ctx.save_for_backward(x, w)
            return x * w
        @staticmethod
        def backward(ctx, grad):
            x, w = ctx.saved_tensors
            return grad * w, grad * x

    def fn(x, w):
        y = (Mul.apply(x, w).sin() + x * w).sum()
        (gx,) = torch.autograd.grad(y, x, create_graph=True)
        return gx.sum()

    old_value = torch._dynamo.config.trace_autograd_ops
    try:
        torch._dynamo.config.trace_autograd_ops = True
        x = torch.tensor(1.0, requires_grad=True)
        w = torch.tensor(2.0, requires_grad=True)
        (eager_grad,) = torch.autograd.grad(fn(x, w), w)
        (compiled_grad,) = torch.autograd.grad(torch.compile(fn, backend="eager", fullgraph=True)(x, w), w)
    finally:
        torch._dynamo.config.trace_autograd_ops = old_value
    analytic = math.cos(2.0) - 2 * math.sin(2.0) + 1.0
    assert abs(eager_grad.item() - analytic) < 1e-5
    assert abs(compiled_grad.item() - 1.0) < 1e-5
    assert abs(compiled_grad.item() - analytic) > 1.0
