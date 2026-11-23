import pytest
import torch


def test_issue_205134():
    unchanged = torch.tensor([1.,2.],requires_grad=True)
    (unchanged * unchanged).sum().backward()
    torch.testing.assert_close(unchanged.grad,torch.tensor([2.,4.]),rtol=0,atol=0)
    # After mutation of a saved tensor, the contract is an error, not [2,4].
    control = torch.tensor([1.,2.],requires_grad=True)
    control_loss = (control * control).sum()
    control_alias = control.detach()
    before = control._version
    control_alias.mul_(10)
    assert control._version == control_alias._version == before + 1
    with pytest.raises(RuntimeError,match="modified by an inplace operation"):
        control_loss.backward()
    x = torch.tensor([1.,2.],requires_grad=True)
    loss = (x*x).sum()
    alias = x.detach()
    assert torch._C._is_alias_of(alias,x)
    before = x._version
    alias.apply_(lambda v:v*10)
    torch.testing.assert_close(x,torch.tensor([10.,20.]),rtol=0,atol=0)
    assert x._version == alias._version == before
    loss.backward()  # Bug: succeeds instead of rejecting the saved-tensor mutation.
    torch.testing.assert_close(x.grad,torch.tensor([20.,40.]),rtol=0,atol=0)
