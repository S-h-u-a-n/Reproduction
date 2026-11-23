"""Known-bug signature test for https://github.com/pytorch/pytorch/issues/199571 .

PASS means the issue is reproduced, not that the underlying PyTorch bug is fixed.
"""

import torch
import pytest



def f(a, b):
    return torch.imag(torch.linalg.solve(a, b, left=False))


def test_known_bug_signature():
    a = torch.tensor([[3+1j, 0.5+0.3j], [0.2-0.1j, 2+1j]], dtype=torch.complex64)
    b = torch.tensor([[2+0.2j, 1-0.5j], [0.1+0.3j, 4-1j]], dtype=torch.complex64)
    eager = f(a, b)
    assert eager.shape == (2, 2) and torch.isfinite(eager).all()
    # Solve X A = B with the analytic 2x2 inverse in higher precision.
    ad, bd = a.to(torch.complex128), b.to(torch.complex128)
    det = ad[0,0]*ad[1,1] - ad[0,1]*ad[1,0]
    inverse = torch.stack((ad[1,1], -ad[0,1], -ad[1,0], ad[0,0])).reshape(2,2) / det
    # Small well-conditioned float32 system: allow solve rounding.
    torch.testing.assert_close(eager, (bd @ inverse).imag.float(), rtol=1e-5, atol=1e-6)
    compiled = torch.compile(f, backend='aot_eager', fullgraph=True)
    with pytest.raises(RuntimeError) as error:
        compiled(a, b)

    assert "view_as_real" in str(error.value)
    assert "unresolved conjugated tensor" in str(error.value)
