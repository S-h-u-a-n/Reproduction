"""Known PyTorch bug signature — pytorch/pytorch#198624.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch

def f(x):
    y=x.detach()
    y.add_(x)
    return y

def test_known_bug_signature():
    x=torch.ones(3,requires_grad=True)
    eager=f(x)
    assert eager.requires_grad and eager.grad_fn is not None
    assert torch._C._is_alias_of(eager,x)
    torch.testing.assert_close(eager,torch.full_like(x,2.),rtol=0,atol=0)
    eager.sum().backward()
    torch.testing.assert_close(x.grad,torch.ones_like(x),rtol=0,atol=0)
    torch._dynamo.reset()
    y=torch.ones(3,requires_grad=True)
    result=torch.compile(f,backend='aot_eager')(y)
    torch.testing.assert_close(result,torch.full_like(y,2.),rtol=0,atol=0)
    assert torch._C._is_alias_of(result,y)
    assert result.shape == eager.shape
    assert not result.requires_grad and result.grad_fn is None, 'Known bug: compiled alias wrongly loses grad history'
