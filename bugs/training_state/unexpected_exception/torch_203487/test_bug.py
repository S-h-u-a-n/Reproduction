import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path


# This upstream bug requires two independent gloo ranks; the pytest process
# invokes torch.distributed.run in a clean subprocess, not a one-rank mock.
WORKER = r"""
import torch
import torch.nn as nn
import torch.distributed as dist
from torch.distributed.fsdp import fully_shard
from torch.distributed.checkpoint.state_dict import get_optimizer_state_dict

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.full((8, 8), 0.25))

    def forward(self, x):
        return x @ self.weight

try:
    dist.init_process_group('gloo')
    model = Model()
    fully_shard(model)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
    x = torch.arange(32.0).reshape(4, 8) / 32.0
    model(x).sum().backward()
    optimizer.step()
    before = get_optimizer_state_dict(model, optimizer)
    assert before['state'], 'control state should be nonempty'
    with torch.no_grad():
        model(x)
    try:
        get_optimizer_state_dict(model, optimizer)
    except KeyError as exc:
        # Upstream 2.15 signature: stale parameter mapping raises KeyError: 0
        assert exc.args == (0,), f'Unexpected KeyError payload: {exc.args!r}'
    else:
        raise AssertionError('Expected FSDP2 optimizer state KeyError after no-grad forward')
    print('EXPECTED_FSDP2_OPTIMIZER_STATE_FAILURE')
finally:
    if dist.is_initialized():
        dist.destroy_process_group()
"""


def test_issue_203487():
    with tempfile.TemporaryDirectory(prefix='mirage_fsdp2_') as td:
        worker = Path(td) / 'worker.py'
        worker.write_text(WORKER, encoding='utf-8')
        env = os.environ.copy()
        env.update({'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'PYTHONDONTWRITEBYTECODE':'1'})
        cmd = [
            sys.executable, '-m', 'torch.distributed.run',
            '--standalone', '--nnodes=1', '--nproc-per-node=2', str(worker)
        ]
        proc = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, env=env, start_new_session=True)
        try:
            out, err = proc.communicate(timeout=105)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate()
            raise AssertionError('Two-rank FSDP2 reproduction timed out; not a valid bug observation')
        assert proc.returncode == 0, f'2-rank repro failed: {out[-4000:]}\n{err[-4000:]}'
        assert out.count('EXPECTED_FSDP2_OPTIMIZER_STATE_FAILURE') == 2, (
            'Expected both ranks to reproduce the same KeyError: ' + out[-4000:]
        )
