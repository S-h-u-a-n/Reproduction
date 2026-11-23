import torch

def test_issue_198851():
    x = torch.tensor([[True, False, True], [False, True, False]])
    cases = (
        (lambda t: torch.any(t, dim=()), True),
        (lambda t: torch.all(t, dim=()), False),
    )
    for fn, full_reduction in cases:
        eager = fn(x)
        compiled = torch.compile(fn, backend="inductor", fullgraph=True)(x)
        assert eager.shape == (2, 3)
        assert torch.equal(eager, x)
        assert compiled.ndim == 0
        assert compiled.item() is full_reduction
