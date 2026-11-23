import torch
from torch._inductor import config as inductor_config
from torch.utils.checkpoint import create_selective_checkpoint_contexts


def test_issue_201158():
    def fn(x, weight):
        z = torch.view_as_complex(x.sin())
        y = torch.view_as_real(z).reshape(64, 128)
        return y.cos() @ weight

    # Deterministic fixed input; no RNG calls, seeded or unseeded.
    x = (torch.arange(64*64*2, dtype=torch.float32).reshape(64, 64, 2) - 4096) / 4096
    weight = torch.arange(128*128, dtype=torch.float32).reshape(128, 128) / 16384
    op = torch.ops.aten.view_as_complex.default
    expected_saved = torch.view_as_complex(x.sin())
    expected_output = fn(x, weight)

    with inductor_config.patch(memory_planning=True, memory_pool="combined"):
        compiled = torch.compile(fn, backend="inductor", fullgraph=True)
        forward, replay = create_selective_checkpoint_contexts([op])
        with forward:
            got = compiled(x, weight)
        torch.testing.assert_close(got, expected_output, rtol=1e-5, atol=1e-5)
        cached = forward.storage[op][0].val
        assert cached.shape == expected_saved.shape
        assert torch.isfinite(cached.real).all().item()
        assert not torch.allclose(cached, expected_saved, rtol=1e-5, atol=1e-5), "Saved checkpoint activation should be overwritten by buffer reuse"
