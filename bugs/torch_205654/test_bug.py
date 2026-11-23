"""Known-bug signature for pytorch/pytorch#205654 (CPU, torch 2.15.0).

Fixed float64 tail inputs; checks reference control and reported gradients.
"""

import math
import torch


def _gradient_for_negative_input(magnitude):
    x = torch.tensor(-magnitude, dtype=torch.float64, requires_grad=True)
    output = torch.special.log_ndtr(x)
    (gradient,) = torch.autograd.grad(output, x)
    return output.item(), gradient.item()


def test_issue_205654():
    control_out, control_grad = _gradient_for_negative_input(0.0)
    assert math.isfinite(control_out)
    assert math.isclose(control_grad, math.sqrt(2.0 / math.pi), rel_tol=1e-12)

    tail_out, tail_grad = _gradient_for_negative_input(2.0 ** 30)
    assert math.isfinite(tail_out)
    # Model cancellation using the measured forward, not a libm-specific constant.
    cancelled = -0.5*(2.0**30)**2 - tail_out
    predicted = math.exp(cancelled)/math.sqrt(2*math.pi)
    assert math.isfinite(tail_grad) and tail_grad > 0
    assert math.isclose(tail_grad,predicted,rel_tol=1e-12)
    # Mills bounds: u < phi(u)/Phi(-u) < u+1/u; both bounds round to u.
    assert float(2.0**30 + 2.0**-30) == 2.0**30
    assert not math.isclose(tail_grad, 2.0 ** 30, rel_tol=1e-6)

    extreme_out, extreme_grad = _gradient_for_negative_input(2.0 ** 35)
    assert math.isfinite(extreme_out)
    assert math.isinf(extreme_grad) and extreme_grad > 0
