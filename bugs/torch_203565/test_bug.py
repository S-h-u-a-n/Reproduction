"""PyTorch known bug signature, issue #203565.

pytest PASS means the REPORTED BUG reproduced, NOT that PyTorch is fixed.
"""

import torch
from torch.nn.utils.rnn import pack_padded_sequence

def test_known_bug_signature():
    x = torch.arange(5 * 3 * 4, dtype=torch.float32).reshape(5, 3, 4)
    packed = pack_padded_sequence(x, [6, 1, 3], enforce_sorted=False)
    assert x.size(0) == 5
    assert max([6,1,3]) > x.size(0)
    total_slots = int(packed.batch_sizes.sum().item())
    actual_rows = packed.data.size(0)
    assert packed.batch_sizes.tolist() == [3,2,2,1,1,1]
    assert total_slots == 10 and actual_rows == 9
