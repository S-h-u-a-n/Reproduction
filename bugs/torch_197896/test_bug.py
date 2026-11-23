"""PyTorch known bug signature, issue #197896.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch

def make():
    state = []
    class Helper:
        def touch(self):
            state.append(1)
    def fn(x):
        Helper().touch()
        return x + 1
    return fn, state

def test_known_bug_signature():
    eager, eager_state = make()
    x = torch.ones(1)
    eager(x)
    eager(x)
    assert eager_state == [1,1]
    fn, state = make()
    compiled = torch.compile(fn, backend='eager', fullgraph=True)
    assert compiled(x).item() == 2.0
    assert compiled(x).item() == 2.0
    assert state == [], f'Known closure-state issue did not reproduce: {state}'
