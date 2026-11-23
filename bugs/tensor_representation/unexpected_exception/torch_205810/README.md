# PyTorch #205810 — torch.compile / torch.nn.Conv2d

- **Cause:** `tensor_representation`
- **Observation:** `unexpected_exception`
- **Primary API:** `torch.compile / torch.nn.Conv2d`
- **GitHub source:** https://github.com/pytorch/pytorch/issues/205810
- **Summary:** Compiled Conv2d with replicate padding fails in backward because FakeTensor/meta strides differ from actual channels-last CPU output.
- **Expected:** Compiled Conv2d backward should agree with eager/aot_eager gradients instead of asserting output stride metadata.
- **Observed bug signature:** Inductor backward fails on replication_pad2d_backward with stride/size metadata mismatch for channels-last CPU tensor.
- **Target:** Linux CPU, PyTorch `2.15.0+cpu`, Python `3.14.10`.
- **Benchmark scope:** One original upstream bug symptom, with deterministic inputs and explicit controls.
- **Verification:** New candidate only. Ten independent pytest processes on the target wheel are required before installation.
- **Limitations:** This does not prove root-cause independence or compatibility with other torch versions. Never loosen the assertion to get a PASS.
