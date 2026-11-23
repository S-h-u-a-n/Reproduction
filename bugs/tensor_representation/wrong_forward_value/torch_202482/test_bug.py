"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/202482 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch
import torch.nn.functional as F


def f(a, x, w, idx_a, idx_b):
    b = F.linear(x, w)
    out = torch.cat([a, b], dim=0)
    out[idx_a] = a
    out[idx_b] = b
    return out


def test_known_bug_signature():
    a = torch.arange(1., 19.).reshape(6, 3) / 5
    x = torch.arange(1., 21.).reshape(4, 5) / 11
    w = torch.arange(1., 16.).reshape(3, 5) / 7
    # Fixed permutation: places cat's linear-result region into index_put writes.
    idx_a = torch.tensor([6, 0, 8, 2, 4, 9], dtype=torch.int64)
    idx_b = torch.tensor([1, 3, 5, 7], dtype=torch.int64)
    expected = f(a, x, w, idx_a, idx_b)
    # Fresh input tensors avoid carrying any mutation between calls.
    got = torch.compile(f, backend='inductor', fullgraph=True)(
        a.clone(), x.clone(), w.clone(), idx_a, idx_b
    )
    linear = (x.double() @ w.double().t()).float()
    reference = torch.empty_like(expected)
    reference[idx_a] = a
    reference[idx_b] = linear
    # Float32 length-5 dot products allow accumulation/FMA rounding.
    torch.testing.assert_close(expected, reference, rtol=1e-5, atol=1e-6)
    # The documented b view aliases cat's rows 6..9 and is overwritten.
    overwritten = torch.cat((a, linear))
    overwritten[idx_a] = a
    aliased_b = overwritten[6:].clone()
    buggy = overwritten.clone()
    buggy[idx_b] = aliased_b
    torch.testing.assert_close(got, buggy, rtol=1e-5, atol=1e-6)
    changed_rows = (~torch.isclose(got, reference, rtol=1e-5, atol=1e-6)).any(dim=1)
    assert changed_rows.tolist() == [False,True,False,False,False,True,False,True,False,False]
