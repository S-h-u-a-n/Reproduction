import pytest
import torch
import torch.nn.functional as F

def test_issue_203485():
    # Fixed, non-random data; the error is in gradient layout, not its values.
    offsets = torch.tensor([3, 8], dtype=torch.int32)
    a = torch.ones((8, 16), requires_grad=True)
    b = torch.ones((2, 16, 32), requires_grad=True)
    result = F.grouped_mm(a, b, offs=offsets)
    # Explicit materialized upstream gradient is accepted.
    (result * torch.ones_like(result)).sum().backward()
    torch.testing.assert_close(result, torch.full((8,32),16.), rtol=0, atol=0)
    torch.testing.assert_close(a.grad, torch.full_like(a,32.), rtol=0, atol=0)
    torch.testing.assert_close(b.grad[0], torch.full_like(b[0],3.), rtol=0, atol=0)
    torch.testing.assert_close(b.grad[1], torch.full_like(b[1],5.), rtol=0, atol=0)
    a.grad = None
    b.grad = None
    result2 = F.grouped_mm(a, b, offs=offsets)
    with pytest.raises(RuntimeError, match=r"Invalid strides/sizes, got \[0, 0\] for strides and \[8, 32\] for sizes"):
        result2.sum().backward()
