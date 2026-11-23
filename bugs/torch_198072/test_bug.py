"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/198072 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import math
import torch
import torch.fx


def mask_invalid(x, nan):
    return torch.where(nan, float('nan'), x)


def test_known_bug_signature():
    x = torch.tensor([1., 50., 3.])
    mask = torch.tensor([False, True, False])
    eager = mask_invalid(x, mask)
    assert math.isnan(eager[1].item())
    gm = torch.fx.symbolic_trace(mask_invalid)
    interpreted = torch.fx.Interpreter(gm).run(x, mask)
    assert math.isnan(interpreted[1].item())
    actual = gm(x, mask)
    assert not torch.isnan(actual[1]).item()
    assert actual[1].item() == 1., 'Known bug: generated FX code shadows the NaN literal'
