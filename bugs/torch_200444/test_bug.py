import contextlib
import pytest
from torch._dynamo.exc import InternalTorchDynamoError
import torch
from torch.utils.checkpoint import checkpoint

def test_issue_200444():
    def g(x):
        class Ctx:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
        def context_fn():
            return Ctx(), contextlib.nullcontext()
        return checkpoint(lambda t: t.sin(), x, use_reentrant=False, context_fn=context_fn)
    x = torch.tensor(1.0, requires_grad=True)
    torch.testing.assert_close(g(x), x.sin())
    with pytest.raises(InternalTorchDynamoError) as error:
        torch.compile(g, backend="eager")(x)

    assert any(isinstance(e, NotImplementedError) and "NestedUserFunctionVariable" in str(e)
               and "context_fn" in str(e) for e in _exception_chain(error.value))


def _exception_chain(error):
    pending, seen = [error], set()
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        pending.extend((current.__cause__, current.__context__))
