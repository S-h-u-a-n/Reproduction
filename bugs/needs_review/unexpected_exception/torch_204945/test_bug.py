# Source: https://github.com/pytorch/pytorch/issues/204945
import pytest
import torch


def test_issue_204945():
    def f(w):
        p = torch.nn.Parameter(w)
        return w + 1 if type(p) is torch.nn.Parameter else w

    w = torch.zeros(3)
    torch.testing.assert_close(f(w), torch.ones(3))
    with pytest.raises(Exception) as caught:
        torch.compile(f, backend="eager")(w)
    chain = []
    e = caught.value
    while e is not None and len(chain) < 8:
        chain.append(type(e).__name__ + ": " + str(e))
        e = e.__cause__ or e.__context__
    details = "\n".join(chain)
    assert "SYNTHETIC_LOCAL" in details and "NameError" in details, details
    assert "InternalTorchDynamoError" in details or "guard" in details.lower(), details
