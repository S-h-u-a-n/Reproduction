"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/198189 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

from collections import OrderedDict
import torch


def touch(cache, x):
    cache.move_to_end('a')
    return x + 1


def test_known_bug_signature():
    x = torch.tensor([1., 2.])
    eager = OrderedDict(a=1, b=2, c=3)
    touch(eager, x)
    assert list(eager) == ['b', 'c', 'a']
    actual = OrderedDict(a=1, b=2, c=3)
    out = torch.compile(touch, backend='eager', fullgraph=True)(actual, x)
    assert torch.equal(out, x + 1)
    assert list(actual) == ['a', 'b', 'c'], (
        'Known bug: compiled move_to_end does not replay state mutation'
    )
