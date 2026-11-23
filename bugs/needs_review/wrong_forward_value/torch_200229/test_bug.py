import torch

def test_issue_200229():
    x = torch.tensor([1e200, 1e200], dtype=torch.float64)
    eager = x.var()
    compiled = torch.compile(lambda z: z.var(), backend="inductor")(x)
    assert eager.item() == 0.0
    assert torch.isnan(compiled).item()
