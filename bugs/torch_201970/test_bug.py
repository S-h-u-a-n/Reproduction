"""Known PyTorch bug signature — pytorch/pytorch#201970.

PASS means reproduced on this environment; it does not mean fixed.
"""

import os
import torch

def test_known_bug_signature(tmp_path, monkeypatch):
    monkeypatch.setenv('TORCHINDUCTOR_CACHE_DIR',str(tmp_path/'inductor'))
    class Square(torch.autograd.Function):
        @staticmethod
        def forward(ctx,x):
            ctx.save_for_backward(x)
            return x.square()
        @staticmethod
        def backward(ctx,g):
            (x,)=ctx.saved_tensors
            return 2*g*x
    def fn(a,b): return Square.apply(a+b)
    a=torch.ones(1,requires_grad=True)
    b=torch.ones(1)
    torch.compile(fn)(a,b).backward()
    torch._dynamo.reset()
    out=torch.compile(fn)(a,b)
    observed=[]
    for _ in range(2):
        a.grad=None
        out.backward(retain_graph=True)
        observed.append(a.grad.item())
    assert observed == [4.0, 8.0], f'Unexpected gradient sequence: {observed}'
