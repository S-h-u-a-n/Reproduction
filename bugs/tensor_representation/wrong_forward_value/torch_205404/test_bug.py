import torch


def test_issue_205404():
    def f(x, y, c):
        x.add_(1)
        return y + c

    def invoke(fn, c_slice):
        base = torch.arange(8.0)
        return fn(base[:4], torch.zeros(4), base[c_slice])

    # First invocation records the fully-overlapping input storage geometry.
    compiled = torch.compile(f, backend="aot_eager", fullgraph=True)
    all_overlap_eager = invoke(f, slice(0, 4))
    all_overlap_compiled = invoke(compiled, slice(0, 4))
    torch.testing.assert_close(all_overlap_eager, torch.tensor([1., 2., 3., 4.]), rtol=0, atol=0)
    torch.testing.assert_close(all_overlap_compiled, all_overlap_eager, rtol=0, atol=0)

    partial_eager = invoke(f, slice(2, 6))
    partial_compiled = invoke(compiled, slice(2, 6))
    torch.testing.assert_close(partial_eager, torch.tensor([3., 4., 4., 5.]), rtol=0, atol=0)
    # Upstream wrong signature: a guard hit replays the already-compiled FULL-overlap graph.
    torch.testing.assert_close(partial_compiled, all_overlap_eager, rtol=0, atol=0)
    assert not torch.equal(partial_compiled, partial_eager)
