# Source: https://github.com/pytorch/pytorch/issues/200925
import torch
from torch._dynamo.testing import CompileCounterWithBackend


def test_issue_200925():
    def fn(x, y):
        x.add_(1)
        y.mul_(2)
        return x + y

    torch._dynamo.reset()
    counter = CompileCounterWithBackend("aot_eager")
    compiled = torch.compile(fn, backend=counter, dynamic=False, fullgraph=True)
    with torch.no_grad(), torch._functorch.config.patch(enable_autograd_cache=False), torch._inductor.config.patch(fx_graph_cache=False):
        warm = torch.arange(1., 6.)
        compiled(warm[:4], warm[1:5])
        eager_base = torch.arange(1., 6.)
        compiled_base = eager_base.clone()
        expected = fn(eager_base[:4], eager_base[:4]).clone()
        actual = compiled(compiled_base[:4], compiled_base[:4]).clone()

    torch.testing.assert_close(expected, torch.tensor([8., 12., 16., 20.]), rtol=0, atol=0)
    torch.testing.assert_close(actual, torch.tensor([8., 14., 18., 20.]), rtol=0, atol=0)
    torch.testing.assert_close(eager_base, torch.tensor([4., 6., 8., 10., 5.]), rtol=0, atol=0)
    torch.testing.assert_close(compiled_base, torch.tensor([2., 6., 8., 10., 10.]), rtol=0, atol=0)
    assert counter.frame_count == 1, f"cache reuse not proven: {counter.frame_count}"
