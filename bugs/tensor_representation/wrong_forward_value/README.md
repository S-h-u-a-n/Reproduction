# tensor_representation / wrong_forward_value

[總目錄](../../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

Observation 定義：forward 或一般數值運算回傳錯誤值，包含 NaN／Inf／signed zero 模式；不把梯度或 optimizer 更新混入。

## 分類準則（Classification Criteria）

先滿足 `tensor_representation` 的根因分類，再以 `wrong_forward_value` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**20**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_forward_value` | 20 |

## API 摘要（API Summary）

唯一 API 數：24；Issue/API 配對數：34。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.compile` | 9 |
| `torch.add` | 2 |
| `torch.linalg.lu_solve` | 2 |
| `torch.SymInt.__round__` | 1 |
| `torch.Tensor.add_` | 1 |
| `torch.Tensor.fill_diagonal_` | 1 |
| `torch.Tensor.index_put_` | 1 |
| `torch.Tensor.item` | 1 |
| `torch.Tensor.scatter_add` | 1 |
| `torch.Tensor.scatter_reduce` | 1 |
| `torch.Tensor.set_` | 1 |
| `torch.Tensor.unfold` | 1 |
| `torch._foreach_copy_` | 1 |
| `torch.amax` | 1 |
| `torch.cat` | 1 |
| `torch.clamp` | 1 |
| `torch.distributions.Wishart` | 1 |
| `torch.distributions.kl_divergence` | 1 |
| `torch.linalg.pinv` | 1 |
| `torch.linalg.solve_triangular` | 1 |
| `torch.nn.functional.linear` | 1 |
| `torch.sparse_coo_tensor` | 1 |
| `torch.sparse_csr_tensor` | 1 |
| `torch.utils._python_dispatch.TorchDispatchMode` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#198064](torch_198064/README.md) | `torch.SymInt.__round__`：主要受測 API | dynamic shape 長度使用 round(n,-1)時，忽略負 ndigits，使用原 n。 | Issue 指出 symbolic size 的 SymInt.__round__ 表示遺失 ndigits，與具體整數語意不同。 | [原文](https://github.com/pytorch/pytorch/issues/198064) |
| [#198064](torch_198064/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | dynamic shape 長度使用 round(n,-1)時，忽略負 ndigits，使用原 n。 | Issue 指出 symbolic size 的 SymInt.__round__ 表示遺失 ndigits，與具體整數語意不同。 | [原文](https://github.com/pytorch/pytorch/issues/198064) |
| [#198071](torch_198071/README.md) | `torch.clamp`：主要受測 API | int8 輸入與超出範圍的 Python max=300時，bound 轉成 int8 的 44，127 被截到 44。 | 上游指出 scalar bound 過早縮窄到 tensor dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198071) |
| [#198071](torch_198071/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | int8 輸入與超出範圍的 Python max=300時，bound 轉成 int8 的 44，127 被截到 44。 | 上游指出 scalar bound 過早縮窄到 tensor dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198071) |
| [#198095](torch_198095/README.md) | `torch.compile`：主要受測 API | 共享 storage 的 base 與切片輸入，修改 base 後回傳切片的 view時，錯誤回傳 t0 第一列。 | 上游指出 synthetic base 重映射 base_idx 後仍使用舊 view metadata。 | [原文](https://github.com/pytorch/pytorch/issues/198095) |
| [#198102](torch_198102/README.md) | `torch.Tensor.unfold`：主要受測 API | 不重疊 unfold view 的寫入，base 中間有未覆蓋位置時，未覆蓋的位置被歸零。 | functionalization 的 unfold inverse 使用 backward scatter 的歸零邏輯，破壞 view 寫回。 | [原文](https://github.com/pytorch/pytorch/issues/198102) |
| [#198102](torch_198102/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 不重疊 unfold view 的寫入，base 中間有未覆蓋位置時，未覆蓋的位置被歸零。 | functionalization 的 unfold inverse 使用 backward scatter 的歸零邏輯，破壞 view 寫回。 | [原文](https://github.com/pytorch/pytorch/issues/198102) |
| [#198118](torch_198118/README.md) | `torch.linalg.pinv`：主要受測 API | complex128 pinv 經 pass-through TorchDispatchMode時，符合缺少 conjugation 的完整 SVD 公式。 | 上游指出內部 lazy conjugate view 在 Python dispatch 路徑未正確物化；與 #197084 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198118) |
| [#198118](torch_198118/README.md) | `torch.utils._python_dispatch.TorchDispatchMode`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | complex128 pinv 經 pass-through TorchDispatchMode時，符合缺少 conjugation 的完整 SVD 公式。 | 上游指出內部 lazy conjugate view 在 Python dispatch 路徑未正確物化；與 #197084 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198118) |
| [#199229](torch_199229/README.md) | `torch.Tensor.set_`：Rebinds the destination tensor storage | Compiled output is 10.0 instead of the eager 7.0 after Tensor.set_ then mutation of old storage. | Compiled Tensor.set_ storage rebinding incorrectly retains a dependency on mutated old storage. | [原文](https://github.com/pytorch/pytorch/issues/199229) |
| [#199229](torch_199229/README.md) | `torch.compile`：Exercises the compiled storage-rebinding path | Compiled output is 10.0 instead of the eager 7.0 after Tensor.set_ then mutation of old storage. | Compiled Tensor.set_ storage rebinding incorrectly retains a dependency on mutated old storage. | [原文](https://github.com/pytorch/pytorch/issues/199229) |
| [#199644](torch_199644/README.md) | `torch.Tensor.item`：主要受測 API | 擷取 float64 scalar 16777219 再傳入 CPU 編譯 kernel時，兩者皆變成 16777220。 | 上游定位 C++ kernel scalar 參數宣告為 const float，縮窄原本的 float64 表示。 | [原文](https://github.com/pytorch/pytorch/issues/199644) |
| [#199644](torch_199644/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 擷取 float64 scalar 16777219 再傳入 CPU 編譯 kernel時，兩者皆變成 16777220。 | 上游定位 C++ kernel scalar 參數宣告為 const float，縮窄原本的 float64 表示。 | [原文](https://github.com/pytorch/pytorch/issues/199644) |
| [#200599](torch_200599/README.md) | `torch.linalg.lu_solve`：主要受測 API | LU[:,None] 的 singleton batch stride 非標準時，解為 [0.2,0.6,5,-1]。 | CPU kernel 用 singleton 維度 stride 當作相鄰矩陣距離。 | [原文](https://github.com/pytorch/pytorch/issues/200599) |
| [#200925](torch_200925/README.md) | `torch.compile`：主要受測 API | 先以不同 offset 的重疊 views 暖機，再傳同 offset aliases時，沿用第一次 synthetic-base offset，寫錯位置。 | 上游 synthetic-base cache guard 未完整描述 storage partition／view offset；必須保留前置呼叫。 | [原文](https://github.com/pytorch/pytorch/issues/200925) |
| [#201268](torch_201268/README.md) | `torch.add`：主要受測 API | CSR out.values() 為合法 stride=2 view時，values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element。 | 上游定位 mkl_result_copy_ 線性複製 nnz，忽略 destination values stride。 | [原文](https://github.com/pytorch/pytorch/issues/201268) |
| [#201268](torch_201268/README.md) | `torch.sparse_csr_tensor`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | CSR out.values() 為合法 stride=2 view時，values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element。 | 上游定位 mkl_result_copy_ 線性複製 nnz，忽略 destination values stride。 | [原文](https://github.com/pytorch/pytorch/issues/201268) |
| [#202482](torch_202482/README.md) | `torch.cat`：主要受測 API | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202482](torch_202482/README.md) | `torch.nn.functional.linear`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202482](torch_202482/README.md) | `torch.Tensor.index_put_`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202482](torch_202482/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202966](torch_202966/README.md) | `torch.distributions.kl_divergence`：主要受測 API | batched Wishart KL 且 p 的 df/covariance 要求梯度時，df term 錯跨 batch 加總，兩類 p 參數梯度皆 None。 | 上游指出 event-rank contraction 錯用到 batch 軸；另有獨立的 p natural parameters detach 問題，需決定根因拆分政策。 | [原文](https://github.com/pytorch/pytorch/issues/202966) |
| [#202966](torch_202966/README.md) | `torch.distributions.Wishart`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | batched Wishart KL 且 p 的 df/covariance 要求梯度時，df term 錯跨 batch 加總，兩類 p 參數梯度皆 None。 | 上游指出 event-rank contraction 錯用到 batch 軸；另有獨立的 p natural parameters detach 問題，需決定根因拆分政策。 | [原文](https://github.com/pytorch/pytorch/issues/202966) |
| [#203078](torch_203078/README.md) | `torch.Tensor.scatter_add`：主要受測 API | expanded index stride=(1,0)，self 比 index 更寬時，寫入 row 0、1，row sums=[16,16,0]。 | 上游定位 expanded-index fast path 把 index width 當成 destination row stride。 | [原文](https://github.com/pytorch/pytorch/issues/203078) |
| [#203078](torch_203078/README.md) | `torch.Tensor.scatter_reduce`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | expanded index stride=(1,0)，self 比 index 更寬時，寫入 row 0、1，row sums=[16,16,0]。 | 上游定位 expanded-index fast path 把 index width 當成 destination row stride。 | [原文](https://github.com/pytorch/pytorch/issues/203078) |
| [#203806](torch_203806/README.md) | `torch._foreach_copy_`：主要受測 API | 以 [b.clone(),a.clone()] 複製回 [a,b]時，兩個 tensor 都得到原 b 的值。 | 上游重現指出編譯器在讀完 clone source 前就寫 destination，破壞 storage 資料依賴。 | [原文](https://github.com/pytorch/pytorch/issues/203806) |
| [#203806](torch_203806/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 以 [b.clone(),a.clone()] 複製回 [a,b]時，兩個 tensor 都得到原 b 的值。 | 上游重現指出編譯器在讀完 clone source 前就寫 destination，破壞 storage 資料依賴。 | [原文](https://github.com/pytorch/pytorch/issues/203806) |
| [#204181](torch_204181/README.md) | `torch.Tensor.fill_diagonal_`：主要受測 API | 非連續 7x2 column view，wrap=True時，寫入 view 外的第三欄，漏掉 wrapped cell。 | 上游懷疑 wrapped diagonal 索引使用 contiguous 假設；layout 觸發已知，完整根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204181) |
| [#204442](torch_204442/README.md) | `torch.add` | CSR out control equals 2*A, while CSC out equals (2*A).T instead of 2*A. | CSR 輸入搭配 CSC out 的 layout 未檢查，回傳轉置的錯誤結果。 | [原文](https://github.com/pytorch/pytorch/issues/204442) |
| [#204446](torch_204446/README.md) | `torch.Tensor.add_`：主要受測 API | 對 base[1] 的 contiguous 非零 offset view 加 COO時，錯改 row 2。 | 上游定位 sparse CPU kernel 重複套用 storage_offset；本地刻意只測 allocation 內的錯位寫入。 | [原文](https://github.com/pytorch/pytorch/issues/204446) |
| [#204446](torch_204446/README.md) | `torch.sparse_coo_tensor`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 對 base[1] 的 contiguous 非零 offset view 加 COO時，錯改 row 2。 | 上游定位 sparse CPU kernel 重複套用 storage_offset；本地刻意只測 allocation 內的錯位寫入。 | [原文](https://github.com/pytorch/pytorch/issues/204446) |
| [#205616](torch_205616/README.md) | `torch.amax`：主要受測 API | 零維 CPU tensor x=3，out=x時，輸出與 input 都被改為 -inf。 | 上游定位 reduction 先把 out 初始化為 identity，覆蓋尚未讀取的 aliased input；是否應明確拒絕 overlap 待上游決策。 | [原文](https://github.com/pytorch/pytorch/issues/205616) |
| [#205620](torch_205620/README.md) | `torch.linalg.solve_triangular`：主要受測 API | A=diag(2,4)、B=diag(6,20)，out=A時，回傳 identity。 | 上游 source inspection 指出先把 B 複製到 out，因 out=A 覆蓋係數矩陣。 | [原文](https://github.com/pytorch/pytorch/issues/205620) |
| [#206126](torch_206126/README.md) | `torch.linalg.lu_solve`：Solves with an output that aliases the LU factor | LU factor aliases the out argument and yields a large residual while independent/rhs output are correct. | Output aliases LU factor, overwriting data required for the solve. | [原文](https://github.com/pytorch/pytorch/issues/206126) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#198118](torch_198118/README.md)：與 #197084 共用 conjugate-view 根因線索；Issue 數不等於獨立根因數。 
- [#200925](torch_200925/README.md)： 必須保留先前 alias-layout 暖機及同程序 graph reuse；不是只跑最後一次呼叫。
- [#201268](torch_201268/README.md)： 本地固定 nnz 的 backing storage 錯寫不等於已驗證 allocation 外 memory corruption。
- [#202966](torch_202966/README.md)：同一 Issue 測到 batch-axis contraction 與 p 參數梯度斷連；是否拆成兩個根因計數需決定。 
- [#204181](torch_204181/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#204446](torch_204446/README.md)： 本地只驗證 allocation 內的錯誤 row，未執行上游 heap corruption／process crash 變體。與 #59101 的重複根因尚未確認。
- [#205616](torch_205616/README.md)：上游傾向拒絕 input/output overlap；需區分支援 alias 的正確值與明確拒絕兩種修復契約。 本地只測 amax scalar alias，不把上游其他 reductions 都列為已測 API。
- [#205620](torch_205620/README.md)：out=A 的支援或明確拒絕政策尚待確認；本例只證明現有靜默錯解。 
- [#204442](torch_204442/README.md)：Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
