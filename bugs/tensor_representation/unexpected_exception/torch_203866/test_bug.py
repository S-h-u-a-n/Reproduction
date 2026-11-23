import io
import pytest
import torch
import torch.distributed as dist
from torch.distributed.device_mesh import init_device_mesh
from torch.distributed.tensor import DTensor, Shard


def test_issue_203866():
    # A single-process CPU Gloo group: no CUDA, network, or randomness needed.
    assert not dist.is_initialized(), "This isolated test requires a fresh process group"
    dist.init_process_group("gloo", store=dist.HashStore(), rank=0, world_size=1)
    try:
        mesh = init_device_mesh("cpu", (1,))
        base = torch.arange(12., dtype=torch.float32)
        zero_offset = DTensor.from_local(base[:4], mesh, [Shard(0)], run_check=False)
        offset_view = DTensor.from_local(base[2:6], mesh, [Shard(0)], run_check=False)
        assert zero_offset.to_local().storage_offset() == 0
        assert offset_view.to_local().storage_offset() == 2
        assert zero_offset.data_ptr() == 0
        assert offset_view.data_ptr() == 2 * base.element_size()

        # Control: a wrapper with zero offset is serialized normally.
        buf = io.BytesIO()
        torch.save(zero_offset, buf)
        assert buf.tell() > 0

        # Signature: wrapper with nonzero offset is mistaken for valid storage.
        with pytest.raises(RuntimeError, match="invalid python storage") as err:
            torch.save(offset_view, io.BytesIO())
        assert "data pointer" in str(err.value)
    finally:
        dist.destroy_process_group()
