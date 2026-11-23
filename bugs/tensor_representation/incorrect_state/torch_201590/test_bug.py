import torch
import pytest


def test_issue_201590():
    def true_fn(x, y):
        y.copy_(x * 2.0)
        return x[:4]  # Aliases graph input, which torch.cond disallows.

    def false_fn(x, y):
        y.copy_(x + 1.0)
        return x[:4]

    def model(pred, x, y):
        return torch.cond(pred, true_fn, false_fn, (x, y))

    x = torch.ones(4)
    y = torch.zeros(4)
    with torch.no_grad():
        out = torch.compile(model, backend="aot_eager")(torch.tensor(True), x, y)

    torch.testing.assert_close(out, x, rtol=0, atol=0)
    torch.testing.assert_close(y, 2.0 * x, rtol=0, atol=0)
    # The observed broken invariant: torch.cond accepts an aliased output.
    assert out.data_ptr() == x.data_ptr()
    assert out is not x
    # A no-mutation control is rejected by the same compiler path.
    def no_mut_true(a, b):
        return a[:4]
    def no_mut_false(a, b):
        return a + 1.0
    with pytest.raises((RuntimeError, AssertionError), match=r"(?i)alias"):
        torch.compile(lambda p, a, b: torch.cond(p, no_mut_true, no_mut_false, (a, b)), backend="aot_eager")(
            torch.tensor(True), x.clone(), torch.zeros_like(y)
        )
