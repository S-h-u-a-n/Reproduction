import torch

def test_issue_195451():
    def fn(x, src):
        updated = torch.slice_scatter(x, src, 0, 0, 1)
        x.copy_(updated)
        return updated
    def run(callable_fn):
        x = torch.tensor([1.0, 2.0])
        out = callable_fn(x, torch.tensor([10.0]))
        torch.testing.assert_close(x, torch.tensor([10.0, 2.0]))
        torch.testing.assert_close(out, torch.tensor([10.0, 2.0]))
        return x, out
    eager_x, eager_out = run(fn)
    assert not torch._C._is_alias_of(eager_x, eager_out)
    eager_out.add_(100)
    torch.testing.assert_close(eager_x, torch.tensor([10.0, 2.0]))

    compiled_x, compiled_out = run(torch.compile(fn, backend="inductor", fullgraph=True))
    assert torch._C._is_alias_of(compiled_x, compiled_out)
    compiled_out.add_(100)
    torch.testing.assert_close(compiled_x, torch.tensor([110.0, 102.0]))
