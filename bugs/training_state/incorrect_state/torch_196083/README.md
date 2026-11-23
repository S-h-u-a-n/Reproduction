# PyTorch #196083 — torch.optim.Optimizer.state_dict / load_state_dict

- **Cause:** `training_state`
- **Observation:** `incorrect_state`
- **Primary API:** `torch.optim.Optimizer.state_dict / load_state_dict`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/196083
- **Summary:** In-process optimizer state transfer aliases SGD momentum buffers; updating the new optimizer mutates the original optimizer state.
- **Expected:** Independent optimizers should not share mutable momentum state after load_state_dict.
- **Observed bug signature:** SGD momentum_buffer shares data_ptr across optimizers and a destination step modifies the source buffer.
- **Target:** Linux CPU, PyTorch `2.15.0+cpu`, Python `3.14.10`.
- **Benchmark scope:** One original upstream bug symptom, with deterministic inputs and explicit controls.
- **Verification:** New candidate only. Ten independent pytest processes on the target wheel are required before installation.
- **Limitations:** This does not prove root-cause independence or compatibility with other torch versions. Never loosen the assertion to get a PASS.
