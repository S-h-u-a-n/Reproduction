import torch


def test_issue_204407():
    z = torch.tensor([[-4j,-1j],[-2j,-3j]],dtype=torch.complex128,requires_grad=True)
    a = z.conj().imag
    assert a.is_neg() and not a.is_conj()
    assert a.dtype == torch.float64 and a.shape == (2,2)
    assert a.stride() == (4,2) and a.storage_offset() == 1
    assert not a.is_contiguous() and torch._C._is_alias_of(a,z)
    # d log|det A| / dA = A^(-T); A=[[4,1],[2,3]], det=10.
    local_reference = torch.tensor([[0.3,-0.2],[-0.1,0.4]],dtype=torch.float64)
    dense = a.detach().resolve_neg().contiguous().requires_grad_()
    torch.linalg.slogdet(dense).logabsdet.backward()
    torch.testing.assert_close(dense.grad,local_reference,rtol=0,atol=1e-12)
    a.retain_grad()
    loss = torch.linalg.slogdet(a).logabsdet
    torch.testing.assert_close(loss,torch.log(torch.tensor(10.,dtype=torch.float64)),rtol=0,atol=1e-12)
    loss.backward()
    # A=-imag(z): apply the chain-rule minus sign.
    reference = -local_reference
    buggy_local = local_reference.t()
    torch.testing.assert_close(a.grad,buggy_local,rtol=0,atol=1e-12)
    torch.testing.assert_close(z.grad.imag,-buggy_local,rtol=0,atol=1e-12)
    torch.testing.assert_close(z.grad.real,torch.zeros_like(reference),rtol=0,atol=0)
    assert not torch.allclose(z.grad.imag,reference,rtol=0,atol=1e-12)
