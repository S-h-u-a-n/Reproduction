"""Regression signature for pytorch/pytorch issue #197087.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
from torch._inductor.exc import CppCompileError, InductorError

def f(x, m): return (x + m).argmin()

def test_known_bug_signature():
    x = torch.arange(48., dtype=torch.float32).reshape(3, 4, 4)
    m = torch.tensor([[[0.,1.,2.,3.], [1.,0.,3.,2.], [2.,3.,0.,1.], [3.,2.,1.,0.]]])
    eager = f(x, m)
    assert eager.ndim == 0
    assert eager.item() == 0
    with pytest.raises(InductorError, match=r"CppCompileError: C\+\+ compile error") as error:
        torch.compile(f, backend='inductor', dynamic=True)(x, m)

    cause = error.value.__cause__ or error.value.__context__
    assert isinstance(cause, CppCompileError)
    message = str(cause)
    # Preserve the malformed C++ expression, not GCC-specific wording.
    assert any("argmin_combine" in line and "**2" in line for line in message.splitlines())
