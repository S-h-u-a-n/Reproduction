# Mirage PyTorch Benchmark

本專案收集 PyTorch 已知問題的候選測試。案例位於 [bugs/](bugs/)。
pytest PASS 只代表測試斷言通過；是否對應原 Issue 的錯誤特徵、目標版本與獨立根因，仍須審查。

目標環境為 Arch Linux x86-64、Python 3.14.10、PyTorch 2.15.0+cpu；
這是目標設定，不代表本次已確認實際執行環境。

## 執行入口

[專案規範](AGENTS.md) 優先適用。以下介紹既有批次流程，不構成執行授權。
Phase 1 僅能在指定副本依 review_targets.txt 與 runtime_context.txt 執行，
每案一次、240 秒、停用 bytecode/pytest cache，並將輸出與快取導向指定位置。
此批次入口保留歷史 180 秒流程，不能代替 Phase 1 執行程序。

取得適用的執行授權後，批次入口格式為：

```sh
bash run.sh 04 1
```

第一個參數必填，支援 04～09；第二個參數為正整數，預設 1。
各批次案例數依序為 19、12、13、15、15、15，共 89 個既有批次項目，
不是整個專案的全部案例。沒有預設全套執行。
每案每輪各啟動一個 pytest process；優先使用專案虛擬環境，否則使用 PATH 中的 python。
需要 Bash、timeout、pytest 與案例本身所需依賴；本文件不安裝或更新環境。

日誌沿用 reports/batchNN/<issue>_runN.log。再次執行相同批次與輪次會覆寫同名日誌；
目前規範禁止修改既有批次報告，因此不可直接重跑。
腳本保留既有行為：逐案顯示結果，FAIL 後繼續；最終程序退出碼不代表全部案例通過。
10 輪或完整套件須另外核准；不自動更新 Metadata 或驗證狀態。

## 檔案用途

| 檔案／目錄 | 用途 |
|---|---|
| [README.md](README.md) | 統一操作說明、Schema 說明、批次來源與限制、檔案索引。 |
| [run.sh](run.sh) | 統一 Batch 04～09 的案例清單與批次執行邏輯。 |
| [AGENTS.md](AGENTS.md) | 資料保存、審查、核准與執行規範。 |
| [tools/validate_metadata.py](tools/validate_metadata.py) | 只驗證 Metadata Schema，不執行案例或證明研究正確性。 |
| [tools/run_isolated_test.sh](tools/run_isolated_test.sh) | bubblewrap 隔離單一測試，唯讀掛載、停用網路與外掛自動載入，60 秒逾時。與批次流程不同，獨立保留。 |
| [batch06_manifest.json](batch06_manifest.json) | Batch 06 的 13 筆 Issue、URL、來源版本證據與分類歷史清單。 |
| [batch09_manifest.json](batch09_manifest.json) | Batch 09 的 15 筆 ID、目標版本與加入批次時的摘要。 |
| [verification/numerical_correctness_203078_200599.json](verification/numerical_correctness_203078_200599.json) | 兩案各 10 次隔離執行的歷史輸出與退出碼；非本次執行證據。 |
| [reports/](reports/) | 既有 Batch 04～09 原始日誌，共 890 份；保留、不重寫。每份為對應 Issue 與輪次的 pytest 輸出。 |
| [bugs/](bugs/) | 候選案例、Metadata 與既有快取；全部保持原樣。 |
| [.venv/](.venv/) | 既有 Python 執行環境與套件。 |
| [.pytest_cache/](.pytest_cache/) | 既有 pytest 執行快取。 |
| [review_artifacts/](review_artifacts/) | 審查與整理提案；不屬於測試來源或正式驗證結果。 |

環境管理用隱藏目錄不納入本次整理，也不讀取其機密內容。

## 格式驗證

[驗證工具](tools/validate_metadata.py) 僅使用 Python 標準函式庫，不匯入或執行案例：

```sh
python3 tools/validate_metadata.py
# 也可指定個別檔案
python3 tools/validate_metadata.py bugs/torch_204407/metadata.json
```

成功回傳 0，格式錯誤回傳 1。

## Schema v1

- `schema_version`：整數 `1`。
- `bug_id`、`issue_url`：符合案例目錄與官方 Issue 編號。
- `target_api`、`bug_type`、`expected_behavior`、`bug_signature`：非空字串。
- `primary_category`：限定 `tensor_layout`、`storage_aliasing`、`tensor_metadata`、`materialization`、`autograd`、`checkpointing`、`graph_lifecycle`、`optimizer_state`、`compilation`、`other`。
- `tags`：不重複的非空字串陣列。
- `environment`：包含 `torch`、`python`、`platform`、`device`，皆為非空字串；僅 `python` 可為 `null`（原紀錄未提供）。
- `randomness`：必須為 `false`。
- `verification`：整數 `runs`、`passes` 滿足 `0 <= passes <= runs`；`review` 為 `pending`、`approved` 或 `rejected`。

不接受額外欄位、重複 JSON 鍵或非標準 JSON 數值常數。
格式驗證不代替根因、隨機行為或復現結果的實際審查。

## 既有資料遷移

兩案的 `10/10` 保留自原 Metadata，本次未重新執行 pytest。
`review: approved` 依使用者提供的人工確認狀態設定。
`torch_204407` 原紀錄未提供 Python 版本，因此為 `null`，不以目前環境推定歷史環境。

`torch_204407` 以反向傳播梯度錯誤歸類 `autograd`，標籤保留非連續布局與共軛 view 條件；
`torch_205134` 以版本計數器未更新歸類 `tensor_metadata`。
原本的梯度、資料型別與錯誤描述整合至 `expected_behavior` 與 `bug_signature`。

## 歷史批次來源與限制

以下從原批次文件保留。版本、pending/0/0、案例總數與驗證聲明均為加入批次時的歷史敘述，
不是目前狀態或本次重新驗證結果；上游 Issue 本次未連線核實。
共通安裝流程原為檢查 ZIP 後以 unzip -n 解壓、啟用既有環境，再呼叫批次腳本；
現在統一入口如上。不得依歷史安裝說明覆寫本專案受保護資料。


## Batch 04

This archive adds **19 new candidate issue folders** to `bugs/`. Existing files are not included.
The goal is 11 existing candidates + these 19 = **30 candidate folders** if the local count is unchanged.

**Important**: tests are *known-bug signature reproducers*. A pytest PASS means the reported incorrect behavior was observed; it does NOT mean PyTorch passes a correctness test. All Metadata uses review=pending, verification=0/0 until Arch Linux 2.15.0+cpu is tested. Some issues were only reported on 2.15 nightlies or other builds; they may fail on your exact release, and should be excluded or investigated rather than forcing assertions to pass.
## Selection notes

- Inputs are fixed numerical tensors; no `torch.rand`, `torch.randn` or seed-based sampling.
- The issue URLs are in each `metadata.json`.
- Several test cases involve `torch.compile`; their CPU compiler dependencies and behavior need checking on Arch Linux.
- #203485 replaces the Issue's random tensors with fixed ones; treat as an adaptation requiring confirmation.
- #204679 only uses a dense BF16 numerical case from the Issue and does not exercise its sparse CSR variant.
- #199350 and #195451 have weaker proof for an exact stock 2.15.0 CPU wheel; flag them for review if not reproduced.
- This batch deliberately excludes cases whose core reproducer directly aborts the interpreter or depends on stochastic operations.
- **Check root-cause overlap before declaring 30 independent accepted bugs**. Issue-count is not the same as independent bug count.

## Candidates

| Issue | Classification | Original-report evidence |
|---|---|---|
| [199211](https://github.com/pytorch/pytorch/issues/199211) | tensor_layout | 2.15.0.dev20260925+cpu, CPU; 2.15.0 release not independently confirmed |
| [198102](https://github.com/pytorch/pytorch/issues/198102) | storage_aliasing | 2.15.0.dev20260921+cpu, CPU; release build pending |
| [202806](https://github.com/pytorch/pytorch/issues/202806) | storage_aliasing | Issue verified PyTorch 2.15.0 CPU |
| [197887](https://github.com/pytorch/pytorch/issues/197887) | tensor_metadata | 2.14.0+cpu and 2.15 nightly CPU; release build pending |
| [198119](https://github.com/pytorch/pytorch/issues/198119) | compilation | 2.15.0.dev20260911+cpu Linux; release pending |
| [200229](https://github.com/pytorch/pytorch/issues/200229) | compilation | 2.15.0.dev20260923+cpu, CPU; release pending |
| [198484](https://github.com/pytorch/pytorch/issues/198484) | compilation | 2.15.0.dev20260923+cpu Linux; release pending |
| [203485](https://github.com/pytorch/pytorch/issues/203485) | tensor_layout | PyTorch 2.15.0+cpu confirmed in Issue; fixed inputs are an adaptation, local validation needed |
| [204679](https://github.com/pytorch/pytorch/issues/204679) | other | Issue reports stock 2.15.0+cpu wheel output, CPU |
| [200444](https://github.com/pytorch/pytorch/issues/200444) | checkpointing | 2.15.0.dev20260909+cpu Linux; release pending |
| [197092](https://github.com/pytorch/pytorch/issues/197092) | compilation | 2.15.0.dev20260912+cpu Linux; release pending |
| [198095](https://github.com/pytorch/pytorch/issues/198095) | storage_aliasing | 2.15.0.dev20260921+cpu reported; release pending |
| [195451](https://github.com/pytorch/pytorch/issues/195451) | storage_aliasing | Issue tested editable runtime on CPU, release 2.15 status uncertain |
| [194347](https://github.com/pytorch/pytorch/issues/194347) | compilation | 2.15.0.dev20260820 CPU, release pending |
| [198134](https://github.com/pytorch/pytorch/issues/198134) | compilation | 2.14.0 CPU and 2.15 nightly Linux; release pending |
| [198851](https://github.com/pytorch/pytorch/issues/198851) | compilation | 2.15.0.dev20260922, CPU also reported; release pending |
| [197097](https://github.com/pytorch/pytorch/issues/197097) | compilation | 2.14.0 CPU and 2.15 nightly CPU; release pending |
| [199350](https://github.com/pytorch/pytorch/issues/199350) | tensor_layout | Issue tested CPU torch 2.14.0, release 2.15 uncertain |
| [204825](https://github.com/pytorch/pytorch/issues/204825) | graph_lifecycle | 2.15.0+cu132 and 2.16 nightly CPU; 2.15 CPU wheel pending |

## Batch 05

These tests are **known-bug signature checks**: pytest PASS means the reported bad behavior was reproduced, **not** that PyTorch's operation is correct.

Generated from public pytorch/pytorch issues; all test inputs are explicit and contain no random draws. All metadata records use Schema v1 and keep `verification` at `0/0`, `review=pending` pending independent execution on target 2.15.0+cpu.
## Issue provenance / version confidence

- **2.15.0+cpu release reported**: 205620, 205616, 204181, 202967.
- **Earlier release, 2.15 relevant code inspected but not confirmed**: 201082.
- **2.15 nightly reported, final 2.15 release unconfirmed**: 197811, 197893, 198070, 198057, 197895, 197894, 198183.

**Do not count a candidate in the final 100 until actual local reproducibility and correctness of assertions are reviewed.** Some compiler-dependent cases may fail or time out under different compiler versions/CPUs. No existing issue directories are included in this ZIP.

## All issues

- [205620](https://github.com/pytorch/pytorch/issues/205620): torch.linalg.solve_triangular; 2.15.0+cpu release reported
- [205616](https://github.com/pytorch/pytorch/issues/205616): torch.amax; 2.15.0+cpu release reported
- [204181](https://github.com/pytorch/pytorch/issues/204181): torch.Tensor.fill_diagonal_; 2.15.0+cpu release reported
- [202967](https://github.com/pytorch/pytorch/issues/202967): torch.distributions.kl_divergence; 2.15.0+cpu release reported
- [201082](https://github.com/pytorch/pytorch/issues/201082): torch.distributions.kl_divergence(Normal, Normal); 2.13.0 CPU example; 2.15.0 source reported unchanged, release needs verification
- [197811](https://github.com/pytorch/pytorch/issues/197811): torch.compile / captured Tensor descriptors; 2.15.0.dev20260919+cpu nightly reported; release needs verification
- [197893](https://github.com/pytorch/pytorch/issues/197893): torch.compile / division by 1; 2.15.0.dev20260920 nightly Linux CPU reported; release needs verification
- [198070](https://github.com/pytorch/pytorch/issues/198070): torch.compile / Tensor.item NaN guard; 2.15.0.dev20260921 nightly Linux reported; release needs verification
- [198057](https://github.com/pytorch/pytorch/issues/198057): torch.remainder / torch.compile; 2.15.0.dev20260920 nightly Linux reported; release needs verification
- [197895](https://github.com/pytorch/pytorch/issues/197895): torch.floor_divide / torch.compile; 2.15.0.dev20260920 nightly Linux reported; release needs verification
- [197894](https://github.com/pytorch/pytorch/issues/197894): torch.fx.GraphModule / operator.pow; 2.15.0.dev20260921 nightly Linux reported; release needs verification
- [198183](https://github.com/pytorch/pytorch/issues/198183): torch.erf / torch.compile; 2.15.0.dev20260922 nightly Linux reported; release needs verification

## Batch 06

These tests are **known-bug signature checks**: `pytest PASS` means the observed issue was reproduced, **not** that the bug has been fixed. Case inputs are fixed and do not call any random number generators (even with a fixed seed).
## Source version evidence

- **2.15.0+cpu release reported**: 205682, 202966, 205823.
- **2.15.0 nightly CPU reported, release behavior to verify locally**: 196596, 202482, 198118, 199571, 198072, 198189, 198190, 198192, 198052.
- **2.15.0 release not demonstrated in source (2.14.1 CPU and 2.16 nightly evidence)**: 202726.

`environment` in metadata describes the **target** validation environment. `verification.runs=0`, `passes=0`, `review=pending` must be updated only after actual user execution and quality review. Original GitHub issues may include additional variants; each file isolates one or two simple signatures. No duplicate issue IDs from Batches 02–05.

## Candidate issues

- [#205682](https://github.com/pytorch/pytorch/issues/205682) — torch.cat / Tensor.split / torch.compile: Inductor split result aliases a source tensor and mutating the split changes its input; mixed-dtype splits also preserve incorrect dtype.
- [#202966](https://github.com/pytorch/pytorch/issues/202966) — torch.distributions.kl_divergence / Wishart: Batched KL differs from per-item KL for fixed valid Wishart distributions.
- [#196596](https://github.com/pytorch/pytorch/issues/196596) — torch.addmm / torch.compile: Compiled addmm propagates NaNs from the ignored beta=0 input.
- [#202482](https://github.com/pytorch/pytorch/issues/202482) — torch.cat / torch.nn.functional.linear / index_put: Inductor aliases a linear output into cat storage, which gets overwritten before being reused.
- [#198118](https://github.com/pytorch/pytorch/issues/198118) — torch.linalg.pinv / TorchDispatchMode: Pass-through dispatch mode produces an incorrect complex pseudoinverse.
- [#199571](https://github.com/pytorch/pytorch/issues/199571) — torch.linalg.solve / torch.imag / torch.compile: AOTAutograd raises unresolved conjugate view_as_real error for solve(left=False).imag.
- [#198072](https://github.com/pytorch/pytorch/issues/198072) — torch.fx.symbolic_trace / torch.where: FX generated forward shadows NaN constant with same-named boolean argument.
- [#198189](https://github.com/pytorch/pytorch/issues/198189) — torch.compile / OrderedDict.move_to_end: Dynamo fails to replay the OrderedDict reordering side effect.
- [#198190](https://github.com/pytorch/pytorch/issues/198190) — torch.compile / generator: Compiled output is a tuple_iterator and loses the generator return value.
- [#198192](https://github.com/pytorch/pytorch/issues/198192) — torch.compile / Tensor.sum: Dynamo leaks IndexError out of compiled function instead of executing except fallback.
- [#198052](https://github.com/pytorch/pytorch/issues/198052) — torch.compile / numpy.fix: Compiled NumPy fix performs rounding instead of truncation.
- [#205823](https://github.com/pytorch/pytorch/issues/205823) — torch.compile / torch._inductor.config / F.linear: Freezing and binary folding reorder FX nodes and cause reciprocal use-before-definition error.
- [#202726](https://github.com/pytorch/pytorch/issues/202726) — torch.compile / __torch_function__ / Tensor.real: Dynamo assertion in __torch_function__ subclass handling of .real.

## Important notes

- The full batch is heterogeneous; some compiler tests can take longer to compile than eager tests.
- For issue #205823, this test deliberately runs a known *compile error*, not a crash of the Python interpreter. A timeout or different exception should be recorded as a failure, not a verified reproduction.
- For #198052 the test requires NumPy, already installed in the user's working environment.
- `unzip -n` does not overwrite existing files. If a folder is already present, check its contents manually rather than assume it was updated.
- A reproduction alone is not final benchmark acceptance: compare each assertion with the original issue during later QA, and check root-cause uniqueness.

## Batch 07

Each testcase asserts the **known bug signature**. A passing test means bug reproduced; it does not indicate that PyTorch is fixed.
## Issue-by-issue source notes

Source versions are evidence from issue descriptions, **not local confirmation on PyTorch 2.15.0**. Every metadata review remains pending.

### [#205112](https://github.com/pytorch/pytorch/issues/205112)
- API: torch.func.jacrev / torch.cdist
- Primary category: `autograd`
- Reported build evidence: **other** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: jacrev(f) and autograd.functional.jacobian(f) must agree for cdist p=1.
- Signature: The jacrev Jacobian differs from the unbatched autograd reference for fixed noncoincident points.
- Caveat: Issue contains RNG in its original reproducer; replaced by fixed noncoincident input tensors.

### [#199941](https://github.com/pytorch/pytorch/issues/199941)
- API: torch.vander / torch.linalg.vander
- Primary category: `autograd`
- Reported build evidence: **other** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: torch.vander backward should succeed as does torch.linalg.vander backward.
- Signature: torch.vander backward raises a saved-tensor in-place modification RuntimeError.

### [#200572](https://github.com/pytorch/pytorch/issues/200572)
- API: torch.compile / torch.autograd.Function / view
- Primary category: `graph_lifecycle`
- Reported build evidence: **other** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: A custom autograd.Function scaling its gradient by 2 must remain active when a view is returned from a compiled region.
- Signature: AOTAutograd drops custom backward after returning a view of the Function output.

### [#197716](https://github.com/pytorch/pytorch/issues/197716)
- API: torch.compile(dynamic=True) / SymPy modulo
- Primary category: `compilation`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: Dynamic symbolic modulo in a valid function should compile like eager.
- Signature: TorchInductor/Dynamo crashes because TensorReferenceAnalysis lacks symbolic modulo handling.

### [#197810](https://github.com/pytorch/pytorch/issues/197810)
- API: torch.compile(dynamic=True) / symbolic boolean modulo
- Primary category: `compilation`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: float(shape[0] % 2 == 0) should compile and evaluate identically to eager.
- Signature: Inductor fails with ToFloat(False) for a symbolic modulo comparison.

### [#198669](https://github.com/pytorch/pytorch/issues/198669)
- API: torch.compile / torch.softmax / torch.eq
- Primary category: `compilation`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: Softmax of a boolean-divided floating tensor should run under compile.
- Signature: Inductor attempts invalid boolean negation while lowering softmax.

### [#197087](https://github.com/pytorch/pytorch/issues/197087)
- API: torch.compile(dynamic=True) / argmin
- Primary category: `compilation`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: Dynamic argmin on fixed broadcast inputs should produce the eager index.
- Signature: Inductor emits Python ** into generated C++ and fails compilation for equal-sized inner dimensions.

### [#199214](https://github.com/pytorch/pytorch/issues/199214)
- API: torch.dequantize / torch.trunc_ / torch.compile
- Primary category: `compilation`
- Reported build evidence: **other** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: Dequantize a normal float tensor followed by in-place truncation should compile and run.
- Signature: AOTAutograd functionalization assertion when graph input is dequantized then mutated.

### [#199920](https://github.com/pytorch/pytorch/issues/199920)
- API: aten._fused_moving_avg_obs_fq_helper_functional / FakeTensorMode
- Primary category: `tensor_metadata`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: The fake-tensor observer state shapes must match the real per-channel observer updates.
- Signature: The meta implementation leaves min/max buffers at size 0 and scale/zero-point at size 1 rather than 8.
- Caveat: Observer operator is internal; acceptance depends on whether Mirage benchmark scope permits internal APIs.

### [#198056](https://github.com/pytorch/pytorch/issues/198056)
- API: torch.compile / NumPy cumsum(int8)
- Primary category: `compilation`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: Compiling NumPy cumsum on int8 must preserve NumPy int64 accumulation semantics.
- Signature: Compiled cumsum retains int8 accumulation and wraps past 127.
- Caveat: Same high-level torch._numpy translation area as earlier #198052; mark for later root-cause deduplication.

### [#198155](https://github.com/pytorch/pytorch/issues/198155)
- API: torch.compile / torch.softmax(int64)
- Primary category: `compilation`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: Eager rejects integer softmax; compiling it should not silently run an unsupported dtype kernel.
- Signature: Compiled softmax(int64) silently returns an integer tensor instead of raising.
- Caveat: Umbrella Issue reports many unsupported operator/dtype combinations; use only integer softmax representative.

### [#202862](https://github.com/pytorch/pytorch/issues/202862)
- API: torch.ops.aten.unsqueeze_.default / torch.compile
- Primary category: `tensor_metadata`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: A supported tracing fallback or an explicit Dynamo graph break should occur, not an internal IndexError.
- Signature: OpOverload in-place view of input triggers guard creation IndexError.
- Caveat: The author only verified a pre-Oct-17 2.15 nightly; may be fixed by 2.15 release.

### [#194593](https://github.com/pytorch/pytorch/issues/194593)
- API: torch.distributions.kl_divergence / Binomial / torch.compile
- Primary category: `compilation`
- Reported build evidence: **nightly** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: fullgraph=True Binomial KL with tensor counts should compile and return infinity.
- Signature: Dynamo fails to capture Binomial KL even though eager returns +inf.
- Caveat: Tests compile-support mismatch rather than a numerical wrong-output issue.

### [#203927](https://github.com/pytorch/pytorch/issues/203927)
- API: torch.func.vjp / torch.while_loop
- Primary category: `graph_lifecycle`
- Reported build evidence: **release** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: A cached VJP reused inside while_loop should match eight eager VJP iterations.
- Signature: Capturing a while_loop body containing a cached vjp_fn raises an internal error.

### [#192639](https://github.com/pytorch/pytorch/issues/192639)
- API: torch.autograd.forward_ad / dispatch_functionalize
- Primary category: `autograd`
- Reported build evidence: **other** (`release` means issue reported a release/build of 2.15; `nightly` means 2.15 dev; `other` means no direct 2.15 proof).
- Expected: A dual tensor must expose its forward-mode tangent through a functionalization wrapper.
- Signature: dispatch_functionalize hides a present forward-mode tangent from unpack_dual.
- Caveat: Uses internal Python functionalization API; confirm eligibility in Mirage benchmark scope.

## Scope and limitations

- Fixed literal tensors only; no `rand`, `randn`, `randperm`, `manual_seed`, or implicit sampling in test code.
- No GPU required. Some tests use internal PyTorch APIs or third-party NumPy and should be separately flagged during curation.
- This is a candidate batch, not a 15/15 reproduction claim.
- Distinct issue IDs do not imply distinct root causes; root cause deduplication remains required.

## Batch 08

15 candidate issues; target total 85. Each pytest test asserts the reported **bug signature**, not a fixed implementation.
## Status and source evidence

No verification fields were filled automatically. *Source version evidence* is from GitHub Issue descriptions; not a claim that our runner verified 2.15.0+cpu.

| Issue | Category | Issue test environment evidence |
|---|---|---|
| [#197889](https://github.com/pytorch/pytorch/issues/197889) | `compilation` | 2.15 nightly |
| [#198624](https://github.com/pytorch/pytorch/issues/198624) | `storage_aliasing` | 2.15 nightly |
| [#201970](https://github.com/pytorch/pytorch/issues/201970) | `graph_lifecycle` | 2.14 CPU; 2.15 unconfirmed |
| [#199215](https://github.com/pytorch/pytorch/issues/199215) | `compilation` | 2.14 CPU; 2.15 unconfirmed |
| [#187806](https://github.com/pytorch/pytorch/issues/187806) | `other` | 2.15-era CPU; issue compares against a high-precision reference |
| [#197084](https://github.com/pytorch/pytorch/issues/197084) | `autograd` | 2.15 nightly |
| [#197089](https://github.com/pytorch/pytorch/issues/197089) | `autograd` | 2.15 nightly |
| [#201649](https://github.com/pytorch/pytorch/issues/201649) | `graph_lifecycle` | 2.14 CPU; 2.15 unconfirmed |
| [#203852](https://github.com/pytorch/pytorch/issues/203852) | `tensor_metadata` | 2.15 release CPU |
| [#198994](https://github.com/pytorch/pytorch/issues/198994) | `tensor_metadata` | 2.15 nightly CPU and CUDA |
| [#198868](https://github.com/pytorch/pytorch/issues/198868) | `tensor_metadata` | 2.15 nightly CPU and CUDA |
| [#198852](https://github.com/pytorch/pytorch/issues/198852) | `tensor_metadata` | 2.15 nightly CPU and CUDA |
| [#200600](https://github.com/pytorch/pytorch/issues/200600) | `autograd` | 2.15 release test channel |
| [#198081](https://github.com/pytorch/pytorch/issues/198081) | `tensor_metadata` | 2.15 nightly CPU and CUDA |
| [#197399](https://github.com/pytorch/pytorch/issues/197399) | `storage_aliasing` | 2.15 alpha CPU |

## Detailed provenance and limitations

### [#197889](https://github.com/pytorch/pytorch/issues/197889)
- API: torch.compile / F.interpolate(scale_factor=dynamic float)
- Expected: A changing Python scale factor must change the output interpolation shape.
- Known signature: After multiple calls, the cached compiled graph keeps an obsolete interpolation output shape.
- Source version: 2.15 nightly
- Caveat: Cached-graph behavior may depend on compile cache configuration; one issue rather than multiple scale-factor cases.

### [#198624](https://github.com/pytorch/pytorch/issues/198624)
- API: torch.compile / detach / add_ / output grad_fn
- Expected: Returning a detached alias modified using differentiable data must preserve its restored autograd history.
- Known signature: Eager result has an AddBackward grad_fn, while AOTAutograd regenerates a detached output with no grad_fn.
- Source version: 2.15 nightly

### [#201970](https://github.com/pytorch/pytorch/issues/201970)
- API: torch.compile / FX graph cache / retain_graph
- Expected: Repeated backward with retain_graph=True must return the same gradient, 4, on each pass.
- Known signature: Reusing a cached compiled backward with donated buffers clobbers saved values and yields an incorrect second gradient.
- Source version: 2.14 CPU; 2.15 unconfirmed
- Caveat: Depends on FX graph-cache reuse and may be sensitive to cache settings; inspect logs if not reproduced.

### [#199215](https://github.com/pytorch/pytorch/issues/199215)
- API: torch.compile / freezing_discard_parameters
- Expected: An integer parameter with requires_grad=False can be read in an inference module.
- Known signature: Freezing with discard_parameters incorrectly tries to enable autograd on an integer parameter.
- Source version: 2.14 CPU; 2.15 unconfirmed
- Caveat: Inference-only freezing configuration, not a training gradient bug.

### [#187806](https://github.com/pytorch/pytorch/issues/187806)
- API: torch.nn.functional.gelu / torch.special.erfc
- Expected: GELU for a negative input must retain the tiny representable nonzero value.
- Known signature: Float32 builtin GELU zeros the negative tail through cancellation, whereas the equivalent erfc formula stays nonzero.
- Source version: 2.15-era CPU; issue compares against a high-precision reference
- Caveat: Numerical precision issue in eager CPU; not tensor representation. Filter by final Mirage scope.

### [#197084](https://github.com/pytorch/pytorch/issues/197084)
- API: torch.linalg.pinv / complex autograd / torch.compile
- Expected: Complex pseudoinverse gradients should match eager and complex128 references.
- Known signature: AOTAutograd compiled path computes an inconsistent complex pseudoinverse gradient.
- Source version: 2.15 nightly
- Caveat: Possible shared root cause with earlier #198118; keep the issue distinct until final dedup.

### [#197089](https://github.com/pytorch/pytorch/issues/197089)
- API: torch.compile / torch.std / float32 accumulation
- Expected: Very small nonconstant float32 values have nonzero standard deviation and nonzero gradients.
- Known signature: Inductor float32 accumulation underflows to zero, giving zero std and zero gradient.
- Source version: 2.15 nightly
- Caveat: May overlap root cause with Batch04 #200229 (variance implementation); review later.

### [#201649](https://github.com/pytorch/pytorch/issues/201649)
- API: torch.compiler.nested_compile_region / saved buffers
- Expected: Each region output gradient must equal 2*x+1 and 2*y+1.
- Known signature: Compiled nested regions reuse a saved buffer, and the first input gradient instead depends on y.
- Source version: 2.14 CPU; 2.15 unconfirmed
- Caveat: Author showed CPU buffer reuse on 2.14; actual 2.15 behavior requires verification.

### [#203852](https://github.com/pytorch/pytorch/issues/203852)
- API: torch.Tensor.index_add / float alpha on integer tensors
- Expected: An integer-tensor index_add must reject a floating-point alpha just as torch.add does.
- Known signature: index_add(alpha=2.5) truncates alpha to 2 silently; alpha=0.5 becomes zero.
- Source version: 2.15 release CPU

### [#198994](https://github.com/pytorch/pytorch/issues/198994)
- API: torch.compile / F.soft_margin_loss mixed input-target dtype
- Expected: The compiled soft-margin-loss result should retain the eager float32 dtype.
- Known signature: Inductor promotes float32 input and float64 target loss to float64 incorrectly.
- Source version: 2.15 nightly CPU and CUDA

### [#198868](https://github.com/pytorch/pytorch/issues/198868)
- API: torch.compile / scalar scatter with empty index
- Expected: Scatter with an empty index must preserve scalar shape ().
- Known signature: Inductor changes a scalar tensor output into a one-element tensor with shape (1,).
- Source version: 2.15 nightly CPU and CUDA

### [#198852](https://github.com/pytorch/pytorch/issues/198852)
- API: torch.compile / torch.cat empty higher-precision tensor
- Expected: Concatenating an empty float64 input with float32 nonempty inputs should preserve float64 promotion.
- Known signature: Compiled cat silently drops the empty input contribution to output dtype.
- Source version: 2.15 nightly CPU and CUDA

### [#200600](https://github.com/pytorch/pytorch/issues/200600)
- API: torch.linalg.solve / forward over reverse AD
- Expected: With A=2,B=1, the tangent d/dA(dX/dB) equals -0.25 and d/dA(dX/dA) equals 0.25.
- Known signature: Default reverse backward silently drops or halves forward-mode tangents; create_graph=True is correct.
- Source version: 2.15 release test channel

### [#198081](https://github.com/pytorch/pytorch/issues/198081)
- API: torch.compile / torch.any uint8 dtype
- Expected: Reduction any() on uint8 input preserves uint8 dtype like eager, including uint8 arithmetic.
- Known signature: Compiled reduction returns bool and subsequent arithmetic changes from uint8 wraparound to int64 300.
- Source version: 2.15 nightly CPU and CUDA

### [#197399](https://github.com/pytorch/pytorch/issues/197399)
- API: torch.Tensor.set_ storage rebind / torch.compile
- Expected: A valid storage rebind from a zero-element tensor to a length-one view must either be modeled or graph-broken cleanly.
- Known signature: Fake-tensor tracing fails to update the rebound size and raises IndexError when reading x[0].
- Source version: 2.15 alpha CPU

## Screening notes

- Never interpret pytest PASS as a *fix*; these are bug-reproduction tests.
- Keep failed or timed-out tests as candidates pending diagnosis, not as verified known bugs.
- Candidates labelled `2.16 nightly only` are high-risk for PyTorch 2.15.0.
- Root-cause deduplication is intentionally deferred.
- Test programs use fixed literal tensor values, with no user-authored random generator calls.
- Some tests use private PyTorch APIs, which must be reviewed for final dataset eligibility.

## Batch 09

15 fresh candidate issues, increasing the collection from 85 to 100 **candidates**, not 100 independently audited bugs.
## Data interpretation

- PASS = known issue bug **signature** reproduced; it does **not** mean fixed.
- FAIL, timeout, or a different exception may indicate version differences or a test implementation problem; inspect logs.
- Every `metadata.json` has `verification = {runs:0, passes:0, review:"pending"}` until your local results are recorded.
- All cases have fixed non-random inputs; no explicit or seeded RNG calls (including model constructors with random initialization).
- Source-version evidence is only what the upstream issue author claimed. Your target is PyTorch 2.15.0+cpu.
- Issue statuses may include closed/fixed-after-release; this is a historical version-pinned benchmark.
- Some cases deliberately supply invalid inputs and may be excluded by final Mirage selection.

## Issue index

| Issue | Category | Upstream version evidence |
|---|---|---|
| [#202526](https://github.com/pytorch/pytorch/issues/202526) | `compilation` | 2.15.0+cpu release |
| [#198064](https://github.com/pytorch/pytorch/issues/198064) | `tensor_metadata` | 2.14 CPU and 2.15 nightly CPU |
| [#198077](https://github.com/pytorch/pytorch/issues/198077) | `graph_lifecycle` | 2.14 CPU and 2.15 nightly CPU |
| [#197896](https://github.com/pytorch/pytorch/issues/197896) | `graph_lifecycle` | 2.14 CPU and 2.15 nightly CPU |
| [#205991](https://github.com/pytorch/pytorch/issues/205991) | `graph_lifecycle` | 2.15 stable CPU (author tested) |
| [#203806](https://github.com/pytorch/pytorch/issues/203806) | `storage_aliasing` | 2.14.1 CPU; 2.15 unconfirmed |
| [#200053](https://github.com/pytorch/pytorch/issues/200053) | `optimizer_state` | 2.15 nightly CPU |
| [#203565](https://github.com/pytorch/pytorch/issues/203565) | `tensor_metadata` | 2.10.0 and 2.12.0+cpu; 2.15 unconfirmed |
| [#201947](https://github.com/pytorch/pytorch/issues/201947) | `autograd` | 2.14.1 CPU; issue closed Nov 2026, release 2.15 unconfirmed |
| [#193757](https://github.com/pytorch/pytorch/issues/193757) | `compilation` | 2.15 nightly CPU |
| [#199258](https://github.com/pytorch/pytorch/issues/199258) | `checkpointing` | 2.14 CPU; 2.15 nightly CPU |
| [#200524](https://github.com/pytorch/pytorch/issues/200524) | `autograd` | 2.15 nightly CPU |
| [#198071](https://github.com/pytorch/pytorch/issues/198071) | `tensor_metadata` | 2.15 nightly CPU |
| [#199644](https://github.com/pytorch/pytorch/issues/199644) | `tensor_metadata` | 2.15 nightly CPU |
| [#200924](https://github.com/pytorch/pytorch/issues/200924) | `graph_lifecycle` | 2.15.0+cpu release (author tested); closed Oct 2026 |

## Test-by-test scope notes

### #202526
- API: `torch.jit.freeze / nn.Linear + nn.BatchNorm1d`
- Correct behavior: Freezing must preserve bn(h) + h when Linear output h has multiple consumers.
- Reported bug signature: Frozen TorchScript folds BatchNorm into the Linear and changes the other consumer.
- Upstream test evidence: 2.15.0+cpu release
- Caution: TorchScript is deprecated and may be outside the final Mirage scope; input and module weights are fixed, no RNG.

### #198064
- API: `torch.compile(dynamic=True) / SymInt.__round__`
- Correct behavior: round(n, -1) on symbolic sizes must perform the same decimal rounding as Python.
- Reported bug signature: Compiled dynamic-shape program drops negative ndigits and scales by n*5 rather than rounded value.
- Upstream test evidence: 2.14 CPU and 2.15 nightly CPU

### #198077
- API: `torch.fx.GraphModule / pickle round trip / operator.iadd`
- Correct behavior: Pickling and restoring an FX GraphModule must preserve its in-place mutation semantics.
- Reported bug signature: Unpickled GraphModule changes operator.iadd into out-of-place addition, leaving input unchanged.
- Upstream test evidence: 2.14 CPU and 2.15 nightly CPU
- Caution: Uses Python pickle on a locally created object; never load an untrusted pickle file.

### #197896
- API: `torch.compile / closure-captured mutable state in local class`
- Correct behavior: A helper method must update closure-captured state in compiled as in eager execution.
- Reported bug signature: Under Dynamo the local helper method executes without replaying list.append side effects.
- Upstream test evidence: 2.14 CPU and 2.15 nightly CPU

### #205991
- API: `torch.compile / class attribute mutation and instance read`
- Correct behavior: An instance attribute read after assigning the class attribute within the same function must see the new value 5.
- Reported bug signature: Dynamo reads the old class attribute and returns 0 instead of 5.
- Upstream test evidence: 2.15 stable CPU (author tested)

### #203806
- API: `torch.compile / torch._foreach_copy_ / swapped tensor inputs`
- Correct behavior: Copying [b.clone(),a.clone()] into [a,b] must swap both tensors.
- Reported bug signature: Inductor writes the first destination early, so both destinations get the same data.
- Upstream test evidence: 2.14.1 CPU; 2.15 unconfirmed
- Caution: The issue was later closed; verify that 2.15 release still has this signature.

### #200053
- API: `torch.optim.RMSprop / alpha range validation`
- Correct behavior: RMSprop alpha >1 should be rejected as an invalid exponential-average parameter.
- Reported bug signature: alpha=1.5 is accepted, produces negative square_avg and NaN model weights.
- Upstream test evidence: 2.15 nightly CPU

### #203565
- API: `torch.nn.utils.rnn.pack_padded_sequence / invalid sequence lengths`
- Correct behavior: Sequence lengths exceeding T must be rejected rather than producing contradictory metadata.
- Reported bug signature: PackedSequence.batch_sizes claims more elements than PackedSequence.data contains.
- Upstream test evidence: 2.10.0 and 2.12.0+cpu; 2.15 unconfirmed
- Caution: Input lengths are invalid; this is an input-validation/state-integrity case, not a valid training numerics case.

### #201947
- API: `torch.asinh / torch.acosh float16 backward`
- Correct behavior: For x=1000 the analytic derivative is finite and close to 0.001.
- Reported bug signature: The backward formula squares 1000 in float16, overflows, and returns zero gradient.
- Upstream test evidence: 2.14.1 CPU; issue closed Nov 2026, release 2.15 unconfirmed
- Caution: This is a nonzero-gradient numerical precision problem, not a tensor-layout defect.

### #193757
- API: `torch.compile / F.binary_cross_entropy target validation`
- Correct behavior: BCE must reject targets outside [0,1] in eager and compiled modes.
- Reported bug signature: CPU Inductor calculates a finite value for target=1.5 instead of rejecting it.
- Upstream test evidence: 2.15 nightly CPU
- Caution: Input is intentionally outside documented valid range; audit may reject such cases.

### #199258
- API: `torch.utils.checkpoint.checkpoint(use_reentrant=False) / torch.compile`
- Correct behavior: A nonreentrant checkpoint containing x*1.0 is a valid identity and must preserve gradients.
- Reported bug signature: Inductor min-cut partitioner raises NetworkXError: node source not in graph.
- Upstream test evidence: 2.14 CPU; 2.15 nightly CPU
- Caution: Issue was closed after 2.15 release test channel; exact exception can depend on backend.

### #200524
- API: `torch.compile / torch.full(fill_tensor_requires_grad)`
- Correct behavior: torch.full should reject an autograd-tracked 0-D tensor fill value as eager does.
- Reported bug signature: Dynamo accepts the invalid fill and permits backward through the fill tensor.
- Upstream test evidence: 2.15 nightly CPU
- Caution: Input violates eager API contract. Check final dataset eligibility.

### #198071
- API: `torch.compile / torch.clamp int8 out-of-range Python bounds`
- Correct behavior: clamp(int8,max=300) must not wrap upper bound 300 into int8 44.
- Reported bug signature: Inductor wraps the upper bound to 44 and clamps valid 127 down to 44.
- Upstream test evidence: 2.15 nightly CPU
- Caution: Eager validation differs between 2.14 and 2.15; do not hardcode one eager outcome.

### #199644
- API: `torch.compile / Tensor.item / unbacked float64 precision`
- Correct behavior: A captured float64 scalar 16777219 must stay exact through one-element output kernels.
- Reported bug signature: CPU Inductor narrows the unbacked scalar to float32, changing 16777219 to 16777220.
- Upstream test evidence: 2.15 nightly CPU
- Caution: Smaller fixed-input adaptation of GitHub reproducer, avoids allocating a 16-million-element tensor. Needs 2.15 confirmation.

### #200924
- API: `torch.compile / dict-emptiness guards`
- Correct behavior: A compiled function must re-evaluate bool(dict) when its input changes from empty to non-empty.
- Reported bug signature: Graph cached for empty dict is wrongly reused and yields old branch result for a non-empty dict.
- Upstream test evidence: 2.15.0+cpu release (author tested); closed Oct 2026
- Caution: Issue was closed before the current date. Confirm that target 2.15.0 wheel still has the bug.

