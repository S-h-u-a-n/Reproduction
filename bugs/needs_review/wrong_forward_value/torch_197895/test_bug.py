import torch
from fractions import Fraction


def test_issue_197895():
    a = torch.tensor([1.0, 0.5, 6.0, 1.0], dtype=torch.float64)
    b = torch.tensor([0.1, 0.1, 0.2, 1.0 / 3.0], dtype=torch.float64)
    fn = lambda x, y: torch.floor_divide(x, y)
    eager = fn(a, b)
    # Exact rational values of the binary64 inputs; no rounded division.
    reference = torch.tensor([float(Fraction(x) // Fraction(y))
                              for x, y in zip(a.tolist(), b.tolist())], dtype=a.dtype)
    torch.testing.assert_close(eager, reference, rtol=0, atol=0)
    torch._dynamo.reset()
    actual = torch.compile(fn, backend='inductor')(a, b)
    # Reported lowering floors an already-rounded binary64 quotient.
    rounded = torch.tensor([float(x / y) for x, y in zip(a.tolist(), b.tolist())], dtype=a.dtype).floor()
    torch.testing.assert_close(actual, rounded, rtol=0, atol=0)
    assert not torch.equal(actual, eager)
