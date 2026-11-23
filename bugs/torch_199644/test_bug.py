"""PyTorch known bug signature, issue #199644.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

def fn(t):
    value=(t*2).item()
    return torch.full((1,),value,dtype=torch.float64), torch.full((1,),value,dtype=torch.int64)

def test_known_bug_signature():
    with torch._dynamo.config.patch(capture_scalar_outputs=True):
        t=torch.tensor((2**24+3)/2,dtype=torch.float64)
        reference=fn(t)
        assert reference[0].item()==16777219.0 and reference[1].item()==16777219
        got=torch.compile(fn,backend='inductor',fullgraph=True)(t)
        assert got[0].item()==16777220.0 and got[1].item()==16777220, f'Known loss of unbacked scalar precision not seen: {[x.item() for x in got]}'
