import math
import torch

def test_issue_194347():
    def fn(x, y):
        return torch.minimum(x, y)
    x = torch.tensor([-0.0], dtype=torch.float64)
    y = torch.tensor([0.0], dtype=torch.float64)
    eager = fn(x, y).item()
    compiled = torch.compile(fn, backend="inductor")(x, y).item()
    assert eager == compiled == 0.0
    assert math.copysign(1.0, eager) == -1.0
    assert math.copysign(1.0, compiled) == 1.0
