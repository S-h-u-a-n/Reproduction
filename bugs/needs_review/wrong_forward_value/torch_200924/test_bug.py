"""PyTorch known bug signature, issue #200924.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

def fn(x,d):
    empty=not d
    return x+(0 if empty else 1)

def test_known_bug_signature():
    x=torch.zeros(1)
    cf=torch.compile(fn,backend='eager',fullgraph=True)
    torch.testing.assert_close(cf(x,{}),torch.zeros(1))
    expected=fn(x,{'a':1})
    assert expected.item()==1.0
    actual=cf(x,{'a':1})
    assert actual.item()==0.0, f'Known missing dict-emptiness guard not reproduced: {actual}'
