"""Known PyTorch bug signature — pytorch/pytorch#197399.

PASS means reproduced on this environment; it does not mean fixed.
"""

import pytest
import torch

def f(base):
    y = base[1:, 0]
    x = torch.empty(0)
    x.set_(y)
    return x[0]

def test_known_bug_signature():
    base = torch.tensor(
        [[0.0, 1.0], [2.0, 3.0]],
        dtype=torch.float32,
    )

    # Eager: set_ changes x from empty to shape (1,), containing 2.
    assert f(base.clone()).item() == 2.0

    # Known bug: compiled tracing still treats x as size 0.
    with pytest.raises(
        IndexError,
        match=r"index 0 is out of bounds for dimension 0 with size 0",
    ) as error:
        torch.compile(f, backend="inductor")(base.clone())

    assert "getitem" in str(error.value)