import torch


def test_issue_204442():
    base = torch.tensor([[1., 0., 2.], [0., 3., 0.], [0., 0., 5.]])
    a = base.to_sparse_csr()
    expected = base + base
    control = torch.empty_like(a)
    torch.add(a, a, out=control)
    torch.testing.assert_close(control.to_dense(), expected, rtol=0, atol=0)

    out = torch.zeros(3, 3).to_sparse_csc()
    torch.add(a, a, out=out)
    got = out.to_dense()
    assert got.layout == torch.strided
    torch.testing.assert_close(got, expected.T, rtol=0, atol=0)
    assert not torch.equal(got, expected)
