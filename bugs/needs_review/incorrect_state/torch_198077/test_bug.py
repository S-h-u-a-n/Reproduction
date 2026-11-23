"""PyTorch known bug signature, issue #198077.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import operator
import pickle
import torch
import torch.fx

def build():
    g = torch.fx.Graph()
    x = g.placeholder('x')
    g.output(g.call_function(operator.iadd, (x, 1)))
    return torch.fx.GraphModule(torch.nn.Module(), g)

def test_known_bug_signature():
    gm = build()
    original_input = torch.zeros(3)
    original_output = gm(original_input)
    assert original_input.tolist() == [1.0] * 3
    assert original_output.tolist() == [1.0] * 3
    restored = pickle.loads(pickle.dumps(gm))  # local, generated GraphModule only
    restored_input = torch.zeros(3)
    restored_output = restored(restored_input)
    assert restored_output.tolist() == [1.0] * 3
    assert restored_input.tolist() == [0.0] * 3, 'Known bug: serialized FX graph loses iadd side effect'
