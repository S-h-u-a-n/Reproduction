import itertools

import torch
import torch.nn.functional as F


def _scatter_reference(inputs, output_indices, grad_output):
    """Use logical indices to scatter output gradients into input positions."""
    expected = torch.zeros_like(inputs)
    rows, channels, depth, height, width = inputs.shape
    for n in range(rows):
        for c in range(channels):
            for pos in itertools.product(*[range(d) for d in output_indices.shape[2:]]):
                linear = int(output_indices[(n, c, *pos)].item())
                assert 0 <= linear < depth * height * width
                d, rem = divmod(linear, height * width)
                h, w = divmod(rem, width)
                expected[n, c, d, h, w] += grad_output[(n, c, *pos)]
    return expected


def test_issue_197888():
    # Permutation with fixed values, instead of the source issue's randperm.
    x = ((torch.arange(240) * 37) % 240).float().reshape(1, 4, 4, 3, 5)
    y, indices = F.adaptive_max_pool3d(x, (2, 3, 5), return_indices=True)
    grad_output = torch.arange(1.0, y.numel() + 1).reshape(y.shape)
    noncontiguous_indices = indices.contiguous(memory_format=torch.channels_last_3d)

    assert indices.is_contiguous()
    assert not noncontiguous_indices.is_contiguous()
    assert noncontiguous_indices.is_contiguous(memory_format=torch.channels_last_3d)
    torch.testing.assert_close(indices, noncontiguous_indices, rtol=0, atol=0)

    correct = _scatter_reference(x, indices, grad_output)
    native_contiguous = torch.ops.aten.adaptive_max_pool3d_backward(grad_output, x, indices)
    torch.testing.assert_close(native_contiguous, correct, rtol=0, atol=0)

    actual = torch.ops.aten.adaptive_max_pool3d_backward(
        grad_output, x, noncontiguous_indices
    )
    assert torch.isfinite(actual).all().item()
    assert not torch.equal(actual, correct), (
        "This target build does not reproduce the noncontiguous-indices bug"
    )

    # The reported root cause: the native kernel consumes the raw index storage
    # in contiguous order, ignoring its logical channels_last_3d strides.
    strides = []
    step = 1
    for dim in reversed(noncontiguous_indices.shape):
        strides.append(step)
        step *= dim
    storage_order = noncontiguous_indices.as_strided(
        noncontiguous_indices.shape, tuple(reversed(strides))
    )
    assert not torch.equal(indices, storage_order)
    expected_bug = _scatter_reference(x, storage_order, grad_output)
    torch.testing.assert_close(actual, expected_bug, rtol=0, atol=0)
