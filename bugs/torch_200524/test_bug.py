"""PyTorch known bug signature, issue #200524.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch
import pytest

def fn(v):
    return torch.full((3,),v)

def test_known_bug_signature():
    v = torch.tensor(1.5,requires_grad=True)
    with pytest.raises(TypeError):
        fn(v)
    out = torch.compile(fn,backend='eager',fullgraph=True)(v)
    assert torch.allclose(out,torch.full((3,),1.5))
    assert out.requires_grad
    out.sum().backward()
    assert v.grad is not None and v.grad.item()==3.0, 'Known invalid fill/backprop acceptance not observed'
