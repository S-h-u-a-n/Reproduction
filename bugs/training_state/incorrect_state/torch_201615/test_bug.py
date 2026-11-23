import torch


def test_issue_201615():
    old_determinism = torch.are_deterministic_algorithms_enabled()
    old_fill = torch.utils.deterministic.fill_uninitialized_memory
    try:
        torch.use_deterministic_algorithms(True)
        torch.utils.deterministic.fill_uninitialized_memory = True

        def run(fused):
            p = torch.nn.Parameter(torch.tensor([1.0]))
            opt = torch.optim.SGD([p], lr=0.25, momentum=0.5, fused=fused)
            scaler = torch.amp.GradScaler('cpu', init_scale=2.0**127)
            snapshots = []
            for coef in (2.0, 1.0):
                opt.zero_grad(set_to_none=True)
                scaler.scale(coef * p.sum()).backward()
                scaler.step(opt)
                scaler.update()
                snapshots.append({k: v.detach().clone() if isinstance(v, torch.Tensor) else v
                                  for k, v in opt.state[p].items()})
            return p.detach().clone(), snapshots

        correct_p, correct_states = run(False)
        torch.testing.assert_close(correct_p, torch.tensor([0.75]), rtol=0, atol=0)
        assert correct_states[0] == {}
        torch.testing.assert_close(correct_states[1]['momentum_buffer'], torch.tensor([1.0]), rtol=0, atol=0)

        wrong_p, wrong_states = run(True)
        assert 'momentum_buffer' in wrong_states[0]
        assert torch.isnan(wrong_states[0]['momentum_buffer']).all().item()
        assert torch.isnan(wrong_p).all().item()
        assert torch.isnan(wrong_states[1]['momentum_buffer']).all().item()
    finally:
        torch.utils.deterministic.fill_uninitialized_memory = old_fill
        torch.use_deterministic_algorithms(old_determinism)
