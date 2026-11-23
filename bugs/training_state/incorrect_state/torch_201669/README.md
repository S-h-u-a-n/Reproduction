# PyTorch #201669 — torch.optim.SGD.load_state_dict

- **Cause:** `training_state`
- **Observation:** `incorrect_state`
- **Primary API:** `torch.optim.SGD.load_state_dict`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/201669
- **Summary:** Optimizer state reload silently narrows FP32 momentum buffers to bfloat16 because the parameter dtype is bfloat16.
- **Expected:** Reloading optimizer training state should preserve serialized momentum-buffer dtype and values.
- **Observed bug signature:** FP32 momentum buffer [1025,1.00390625] is narrowed to bfloat16 [1024,1.0] after load_state_dict.
- **Target:** Linux CPU, PyTorch `2.15.0+cpu`, Python `3.14.10`.
- **Benchmark scope:** One original upstream bug symptom, with deterministic inputs and explicit controls.
- **Verification:** New candidate only. Ten independent pytest processes on the target wheel are required before installation.
- **Limitations:** This does not prove root-cause independence or compatibility with other torch versions. Never loosen the assertion to get a PASS.
