from decimal import Decimal, localcontext
import torch


def test_issue_204679():
    value = 1.0 + 2.0**-7
    x = torch.full((1000,),value,dtype=torch.bfloat16)
    assert torch.equal(x.double(),torch.full((1000,),value,dtype=torch.float64))
    with localcontext() as context:
        context.prec = 60
        reference = float((Decimal(129)/Decimal(128))**1000)
    assert torch.tensor(reference,dtype=torch.bfloat16).item() == 2400.
    # Float64 accumulation control over exactly the same factors.
    torch.testing.assert_close(x.prod(dtype=torch.float64),
                               torch.tensor(reference,dtype=torch.float64),rtol=1e-12,atol=0)
    actual = x.prod()
    assert actual.dtype == torch.bfloat16 and actual.shape == ()
    # Published dense CPU signature, measured on this AVX512 build.
    # Not claimed for another SIMD reduction tree or sparse CSR.
    assert actual.item() == 1632., f"Different signature on {torch.backends.cpu.get_cpu_capability()}: {actual}"
