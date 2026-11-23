import torch


def test_issue_199020():
    source = torch.tensor([3, 1, 4, 1, 5], dtype=torch.int64)
    expected = torch.cummax(source, dim=0)
    torch.testing.assert_close(expected.values, torch.tensor([3, 3, 4, 4, 5]), rtol=0, atol=0)
    torch.testing.assert_close(expected.indices, torch.tensor([0, 0, 2, 2, 4]), rtol=0, atol=0)

    # Out arguments intentionally alias. The correct behavior would be to
    # reject overlap, or avoid silently destroying values via a temporary.
    shared = torch.empty(0, dtype=torch.int64)
    got = torch.cummax(source.clone(), dim=0, out=(shared, shared))
    assert got.values.data_ptr() == got.indices.data_ptr()
    torch.testing.assert_close(got.indices, expected.indices, rtol=0, atol=0)
    torch.testing.assert_close(got.values, expected.indices, rtol=0, atol=0)
    assert not torch.equal(got.values, expected.values)
