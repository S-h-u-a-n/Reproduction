import pytest
import torch


def test_issue_202416():
    def f(x):
        y = (x * 2)[1:]
        return y, y.detach()

    source = torch.tensor([1., 2., 3., 4.], requires_grad=True)
    eager_y, eager_z = f(source)
    torch.testing.assert_close(eager_y, torch.tensor([4., 6., 8.]))
    torch.testing.assert_close(eager_z, eager_y)
    assert eager_y.shape == eager_z.shape == (3,)
    assert eager_y.untyped_storage().data_ptr() == eager_z.untyped_storage().data_ptr()

    compiled = torch.compile(f, backend="inductor", fullgraph=True)
    with pytest.raises(Exception) as raised:
        compiled(source.clone().detach().requires_grad_(True))
    msg = str(raised.value)
    assert "incorrect out shape after application of ViewMeta sequence" in msg, msg
    assert "(2,)" in msg and "(3,)" in msg, msg
