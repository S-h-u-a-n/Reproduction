"""Known PyTorch bug signature — pytorch/pytorch#197889.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch
import torch.nn.functional as F

def test_known_bug_signature():
    x = (torch.arange(16., dtype=torch.float32).reshape(4, 4)+1)/16
    def f(s):
        return F.interpolate((x*s)[None], scale_factor=1.0+s)
    cf = torch.compile(f)
    observations=[]
    for s in (0.9, 0.5, 0.25, 2.0):
        eager=f(s)
        compiled=cf(s)
        observations.append((tuple(eager.shape),tuple(compiled.shape)))
    assert [want for want, _ in observations] == [(1,4,7), (1,4,6), (1,4,5), (1,4,12)]
    assert [got for _, got in observations] == [(1,4,7), (1,4,6), (1,4,6), (1,4,6)]
