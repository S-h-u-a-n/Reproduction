"""Regression signature for pytorch/pytorch issue #202862.

A PASS here means reproducing a known issue, not verifying its fix.
"""

import torch
import pytest
import traceback

def f(x): return torch.ops.aten.unsqueeze_.default(x, 0)

def test_known_bug_signature():
    x = torch.ones(4, 4)
    eager = f(x.clone())
    assert eager.shape == (1, 4, 4)
    with pytest.raises(IndexError) as error:
        torch.compile(f, fullgraph=True)(x.clone())

    assert "list index out of range" in str(error.value)
    assert any(f.name == "produce_guards_verbose"
               for f in traceback.extract_tb(error.value.__traceback__))
