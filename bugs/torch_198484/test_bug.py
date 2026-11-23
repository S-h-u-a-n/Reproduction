import torch

def test_issue_198484():
    inf, nan = float("inf"), float("nan")
    needle = torch.tensor([inf])
    haystack = torch.tensor([0.0, 1.0, -1.0, inf, -inf, nan,
                             1e-38, 3.4e38, 0.5, -0.5, 0.0, 1.0])
    def fn(a, b):
        return torch.isin(a, b)
    eager = fn(needle, haystack)
    compiled = torch.compile(fn, backend="inductor", fullgraph=True)(needle, haystack)
    assert eager.shape == compiled.shape == (1,)
    assert eager.item() is True
    assert compiled.item() is False
