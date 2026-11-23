"""Known PyTorch bug signature — pytorch/pytorch#197084.

PASS means reproduced on this environment; it does not mean fixed.
"""

import torch

def loss(a): return (torch.linalg.pinv(a).abs()**2).sum()
def grad(fn,a):
    t=a.detach().clone().requires_grad_()
    fn(t).backward()
    return t.grad

def test_known_bug_signature():
    r=torch.tensor([[1.,0.,2.],[0.,3.,1.],[2.,1.,4.],[4.,2.,1.]],dtype=torch.float32)
    im=torch.tensor([[0.5,1.,0.],[-1.,2.,0.5],[1.,-0.5,2.],[0.,1.,-2.]])
    a=torch.complex(r,im)
    want=grad(loss,a)
    ref=grad(loss,a.to(torch.complex128))
    # Full-column-rank loss = tr((A^H A)^-1); its real-loss gradient
    # is -2 A (A^H A)^-2. This avoids using pinv as its own oracle.
    ad = a.to(torch.complex128)
    assert torch.linalg.matrix_rank(ad).item() == 3
    inverse = torch.linalg.inv(ad.mH @ ad)
    reference = -2 * ad @ inverse @ inverse
    torch.testing.assert_close(ref, reference, rtol=1e-10, atol=1e-10)
    # Well-conditioned 4x3 complex64 SVD/matmul roundoff.
    torch.testing.assert_close(want, reference.to(a.dtype), rtol=1e-5, atol=1e-6)
    got=grad(torch.compile(loss,backend='aot_eager'),a)
    # Issue's Sep 22 correction: #198118 drops conjugation in the saved
    # forward pinv. Feed that result into the documented pinv VJP, not
    # into autograd through the SVD (which would test another derivative).
    u, singular, vh = torch.linalg.svd(a, full_matrices=False)
    bad_pinv = (vh.mT / singular) @ u.mH
    upstream = 2 * bad_pinv
    # FunctionsManual.cpp::pinv_backward, m > n branch, at target build.
    k = bad_pinv @ upstream.mH
    phk = bad_pinv.mH @ k
    bad_gradient = (-(k @ bad_pinv).mH
                    + (upstream.mH - a @ k) @ bad_pinv @ bad_pinv.mH
                    + phk - phk @ bad_pinv @ a)
    assert torch.isfinite(got).all()
    torch.testing.assert_close(got, bad_gradient, rtol=1e-5, atol=1e-6)
    assert not torch.allclose(got, want, rtol=1e-5, atol=1e-6)
