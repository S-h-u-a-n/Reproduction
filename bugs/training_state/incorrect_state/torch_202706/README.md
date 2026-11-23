# PyTorch #202706 — torch.autocast

- **Cause:** `training_state`
- **Observation:** `incorrect_state`
- **Primary API:** `torch.autocast`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/202706
- **Summary:** Nested calls of an autocast decorator accidentally reuse context state, leaving autocast enabled after exit.
- **Expected:** Autocast state after recursive decorated calls should equal its state before entry.
- **Observed bug signature:** Autocast starts disabled but is left enabled after a recursive call of the same decorated function.
- **Target:** Linux CPU, PyTorch `2.15.0+cpu`, Python `3.14.10`.
- **Benchmark scope:** One original upstream bug symptom, with deterministic inputs and explicit controls.
- **Verification:** New candidate only. Ten independent pytest processes on the target wheel are required before installation.
- **Limitations:** This does not prove root-cause independence or compatibility with other torch versions. Never loosen the assertion to get a PASS.
