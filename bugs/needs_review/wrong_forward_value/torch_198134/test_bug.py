import math
import torch

def test_issue_198134():
    x = torch.full((8,), 1e200, dtype=torch.float64)
    eager = torch.acosh(x)
    compiled = torch.compile(torch.acosh, backend="inductor")(x)
    torch.testing.assert_close(eager, torch.full_like(x,math.acosh(1e200)), rtol=0, atol=1e-10)
    assert compiled.shape == x.shape and compiled.dtype == x.dtype
    assert torch.isposinf(compiled).all().item()
