import pytest
import torch

def test_issue_199211():
    elements = torch.tensor([0.0, 5.0, 9.0])
    test_elements = torch.arange(4.0).reshape(2, 2).t()
    expected = torch.tensor([True, False, False])
    assert not test_elements.is_contiguous()
    assert torch.equal(torch.isin(elements, test_elements.contiguous()), expected)
    with pytest.raises(RuntimeError, match="view size is not compatible"):
        torch.isin(elements, test_elements)
