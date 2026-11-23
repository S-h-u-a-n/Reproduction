# Source: https://github.com/pytorch/pytorch/issues/204188
from pathlib import Path
import tempfile
import torch
import torch.distributed.checkpoint as dcp
from torch.distributed.checkpoint import DefaultSavePlanner


def test_issue_204188():
    # Two same-shape tensors, same element width but different dtypes.
    old = torch.tensor([[1024., 1.], [1., 255.]], dtype=torch.bfloat16)
    new = torch.tensor([[1025., 1.], [1.00390625, 255.]], dtype=torch.float16)
    with tempfile.TemporaryDirectory(prefix="mirage-dcp-") as temp:
        first = Path(temp) / "first"
        second = Path(temp) / "second"
        dcp.save({"x": old}, checkpoint_id=first, planner=DefaultSavePlanner(enable_plan_caching=True), no_dist=True)
        meta = dcp.save({"x": new}, checkpoint_id=second, planner=DefaultSavePlanner(enable_plan_caching=True), no_dist=True)
        actual_dtype = meta.state_dict_metadata["x"].properties.dtype
        # The second checkpoint is fp16; reusing the bf16 metadata is the bug.
        assert actual_dtype == torch.bfloat16, f"Different metadata: {actual_dtype}"
        assert actual_dtype != new.dtype
        # Control: a fresh planner without caching preserves the correct dtype.
        fresh = Path(temp) / "fresh"
        cold = dcp.save({"x": new}, checkpoint_id=fresh, planner=DefaultSavePlanner(enable_plan_caching=False), no_dist=True)
        assert cold.state_dict_metadata["x"].properties.dtype == torch.float16
