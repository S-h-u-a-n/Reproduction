import pytest
from torch._inductor.exc import InductorError
import torch
import torch.nn.functional as F

def test_issue_199350():
    def fn():
        t = torch.zeros(4, 4, 4, 4)
        t = torch.linalg.cholesky_ex(t)[0]
        t = F.adaptive_max_pool2d(t, (2, 2))
        return torch.view_as_complex_copy(t)
    torch.testing.assert_close(fn(), torch.zeros(4,4,2,dtype=torch.complex64), rtol=0, atol=0)
    with torch.no_grad():
        with pytest.raises(InductorError) as error:
            torch.compile(fn, backend="inductor")()

    assert any(isinstance(e, RuntimeError) and "last dimension with stride 1" in str(e)
               for e in _exception_chain(error.value))
    # Identify the failing operator from the exception frames, without relying
    # on generated node names or a version-specific full traceback.
    operators = []
    for exc in _exception_chain(error.value):
        tb = exc.__traceback__
        while tb is not None:
            operators.append(tb.tb_frame.f_locals.get("func"))
            tb = tb.tb_next
    assert any(op is torch.ops.aten.view_as_complex_copy.default for op in operators)


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
