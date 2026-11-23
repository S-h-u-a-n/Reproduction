# Source: https://github.com/pytorch/pytorch/issues/201268
import torch


def test_issue_201268():
    crow = torch.tensor([0, 1, 2], dtype=torch.int64)
    cols = torch.tensor([0, 1], dtype=torch.int64)
    lhs = torch.sparse_csr_tensor(crow.clone(), cols.clone(), torch.tensor([1., 2.]), size=(2, 2), check_invariants=True)
    rhs = torch.sparse_csr_tensor(crow.clone(), cols.clone(), torch.tensor([10., 20.]), size=(2, 2), check_invariants=True)

    contiguous = torch.sparse_csr_tensor(crow.clone(), cols.clone(), torch.full((2,), -99.), size=(2, 2), check_invariants=True)
    torch.add(lhs, rhs, out=contiguous)
    torch.testing.assert_close(contiguous.values(), torch.tensor([11., 22.]), rtol=0, atol=0)

    backing = torch.tensor([-99., -88., -99., -77.])
    out = torch.sparse_csr_tensor(crow.clone(), cols.clone(), backing[::2], size=(2, 2), check_invariants=True)
    assert out.values().stride() == (2,)
    torch.add(lhs, rhs, out=out)
    torch.testing.assert_close(out.values(), torch.tensor([11., -99.]), rtol=0, atol=0)
    torch.testing.assert_close(backing, torch.tensor([11., 22., -99., -77.]), rtol=0, atol=0)
    assert not torch.equal(out.values(), contiguous.values())
