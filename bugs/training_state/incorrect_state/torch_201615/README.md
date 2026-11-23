# PyTorch #201615 — torch.optim.SGD / torch.amp.GradScaler

- **Cause:** `training_state`
- **Observation:** `incorrect_state`
- **Primary API:** `torch.optim.SGD / torch.amp.GradScaler`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/201615
- **Summary:** A skipped fused-SGD step creates uninitialized momentum state, making the next valid optimizer update NaN.
- **Expected:** A skipped optimizer step must not initialize momentum; the next real step should produce p=0.75.
- **Observed bug signature:** Fused SGD has a NaN momentum_buffer after a skipped first step and corrupts its first actual update.
- **Target:** Linux CPU, PyTorch `2.15.0+cpu`, Python `3.14.10`.
- **Benchmark scope:** One original upstream bug symptom, with deterministic inputs and explicit controls.
- **Verification:** New candidate only. Ten independent pytest processes on the target wheel are required before installation.
- **Limitations:** This does not prove root-cause independence or compatibility with other torch versions. Never loosen the assertion to get a PASS.
