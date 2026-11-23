"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/198190 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import types
import torch


def make(x):
    def gen():
        yield x * 1
        yield x * 2
        return 'done'
    return gen()


def consume(g):
    numbers = []
    try:
        while True:
            numbers.append(next(g).sum().item())
    except StopIteration as e:
        return numbers, e.value


def test_known_bug_signature():
    x = torch.ones(2)
    plain = make(x)
    assert isinstance(plain, types.GeneratorType)
    assert consume(plain) == ([2., 4.], 'done')
    result = torch.compile(make, backend='eager')(x)
    values, ret = consume(result)
    assert values == [2., 4.]
    assert not isinstance(result, types.GeneratorType)
    assert ret is None, 'Known bug: compiled generator loses StopIteration.value'
