"""Known-bug signature for pytorch/pytorch#205653 (CPU, torch 2.15.0).

No random inputs. This test PASSES on the reported overflow/underflow.
"""

import math
import torch


def _measure_at_scale(exponent):
    scale = 2.0 ** exponent
    x = torch.tensor(3.0 * scale, dtype=torch.float64)
    y = torch.tensor(4.0 * scale, dtype=torch.float64, requires_grad=True)
    forward = torch.hypot(x, y)
    (gradient,) = torch.autograd.grad(
        forward, y, grad_outputs=torch.full_like(y, 1.25 * scale)
    )
    return scale, forward.item(), gradient.item()


def test_issue_205653():
    normal_s, normal_forward, normal_grad = _measure_at_scale(0)
    assert normal_forward == 5.0 * normal_s
    assert math.isclose(normal_grad, normal_s, rel_tol=0, abs_tol=1e-12)

    large_s, large_forward, large_grad = _measure_at_scale(600)
    assert math.isfinite(large_s) and large_s > 0
    assert large_forward == 5.0 * large_s
    assert math.isinf(large_grad) and large_grad > 0

    small_s, small_forward, small_grad = _measure_at_scale(-600)
    assert math.isfinite(small_s) and small_s > 0
    assert small_forward == 5.0 * small_s
    assert small_grad == 0.0  # Expected gradient is small_s, not zero.
