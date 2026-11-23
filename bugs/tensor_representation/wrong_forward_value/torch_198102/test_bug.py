import torch

def test_issue_198102():
    def fn(x):
        view = x.unfold(1, 1, 5)
        view.add_(view)
        return x

    x = torch.arange(1, 25, dtype=torch.int64).reshape(4, 6)
    expected = fn(x.clone())
    compiled = torch.compile(fn, backend="aot_eager")(x.clone())
    assert torch.equal(expected[:, 1:5], x[:, 1:5])
    assert torch.equal(compiled[:, 0], expected[:, 0])
    assert torch.equal(compiled[:, 5], expected[:, 5])
    assert torch.equal(compiled[:, 1:5], torch.zeros_like(compiled[:, 1:5]))
    assert not torch.equal(compiled, expected)
