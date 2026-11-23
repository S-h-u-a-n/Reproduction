# PyTorch #199229 — torch.Tensor.set_ / torch.compile

- **Cause:** `tensor_representation`
- **Observation:** `wrong_forward_value`
- **Primary API:** `torch.Tensor.set_ / torch.compile`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/199229
- **Summary:** Compiled Tensor.set_ storage rebinding incorrectly retains a dependency on mutated old storage.
- **Expected:** Rebinding dest to a distinct source must isolate it from later changes to the original backing storage.
- **Observed bug signature:** Compiled output is 10.0 instead of the eager 7.0 after Tensor.set_ then mutation of old storage.
- **Target:** Linux CPU, PyTorch `2.15.0+cpu`, Python `3.14.10`.
- **Benchmark scope:** One original upstream bug symptom, with deterministic inputs and explicit controls.
- **Verification:** New candidate only. Ten independent pytest processes on the target wheel are required before installation.
- **Limitations:** This does not prove root-cause independence or compatibility with other torch versions. Never loosen the assertion to get a PASS.
