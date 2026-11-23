import operator
import torch
import torch.fx


def test_issue_197894():
    graph = torch.fx.Graph()
    exponent = graph.placeholder('x')
    graph.output(graph.call_function(operator.pow, (-2, exponent)))
    gm = torch.fx.GraphModule(torch.nn.Module(), graph)
    expected = torch.fx.Interpreter(gm).run(2)
    actual = gm(2)
    assert expected == 4
    assert actual == -4
    assert actual != expected
