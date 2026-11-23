# Source: https://github.com/pytorch/pytorch/issues/204339
import gc
import weakref
import torch


def test_issue_204339():
    def run(graph_break):
        torch._dynamo.reset()
        graphs = []

        def compiler(gm, _inputs):
            graphs.append(gm)
            return gm.forward

        def scope():
            p = torch.nn.Parameter(torch.ones(2, 2))
            p.grad = torch.ones_like(p)
            optimizer = torch.optim.Adam([p], lr=0.1, foreach=True)

            def step():
                group = optimizer.param_groups[0]
                params, grads, avgs, sqs, max_sqs, steps = [], [], [], [], [], []
                optimizer._init_group(group, params, grads, avgs, sqs, max_sqs, steps)
                if graph_break:
                    torch._dynamo.graph_break()
                params[0].add_(grads[0], alpha=-0.1)

            with torch.no_grad():
                torch.compile(step, backend=compiler)()
            torch.testing.assert_close(p, torch.full_like(p, 0.9))
            return weakref.ref(p), weakref.ref(optimizer)

        enabled = gc.isenabled()
        gc.disable()
        try:
            p_ref, optimizer_ref = scope()
            return {
                "optimizer_released": optimizer_ref() is None,
                "parameter_released": p_ref() is None,
                "graph_parameters": [list(gm._parameters) for gm in graphs],
            }
        finally:
            graphs.clear()
            torch._dynamo.reset()
            if enabled:
                gc.enable()

    control = run(False)
    actual = run(True)
    assert control["optimizer_released"] and control["parameter_released"], control
    assert actual["optimizer_released"] and not actual["parameter_released"], actual
    assert any("params___0" in group for group in actual["graph_parameters"]), actual
