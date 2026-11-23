# tensor_representation / wrong_gradient

[總目錄](../../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

Observation 定義：第一階／高階導數、Jacobian 或 tangent 與正確參考不符。

## 分類準則（Classification Criteria）

先滿足 `tensor_representation` 的根因分類，再以 `wrong_gradient` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**8**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_gradient` | 8 |

## API 摘要（API Summary）

唯一 API 數：15；Issue/API 配對數：19。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.Tensor.as_strided_` | 1 |
| `torch.Tensor.conj` | 1 |
| `torch.Tensor.imag` | 1 |
| `torch.Tensor.unsqueeze` | 1 |
| `torch.Tensor.view` | 1 |
| `torch.autograd.Function` | 1 |
| `torch.cdist` | 1 |
| `torch.compile` | 5 |
| `torch.compiler.nested_compile_region` | 1 |
| `torch.func.jacrev` | 1 |
| `torch.linalg.pinv` | 1 |
| `torch.linalg.slogdet` | 1 |
| `torch.nn.functional.adaptive_max_pool3d` | 1 |
| `torch.no_grad` | 1 |
| `torch.ops.aten.adaptive_max_pool3d_backward` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197084](torch_197084/README.md) | `torch.linalg.pinv`：主要受測 API | 固定 full-column-rank complex64 矩陣、編譯後反向時，完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP。 | Issue 後續更正將原因連至 #198118 的 conjugate view 遺失，不能僅因 gradient 錯誤歸為訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/197084) |
| [#197084](torch_197084/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 固定 full-column-rank complex64 矩陣、編譯後反向時，完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP。 | Issue 後續更正將原因連至 #198118 的 conjugate view 遺失，不能僅因 gradient 錯誤歸為訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/197084) |
| [#197888](torch_197888/README.md) | `torch.ops.aten.adaptive_max_pool3d_backward`：CPU backward kernel | CPU adaptive max pool backward scatters gradients to the wrong input elements when it reads channels_last_3d indices in storage order. | The CPU backward kernel ignores the strides of noncontiguous channels_last_3d indices. | [原文](https://github.com/pytorch/pytorch/issues/197888) |
| [#197888](torch_197888/README.md) | `torch.nn.functional.adaptive_max_pool3d`：Produces pooling indices | CPU adaptive max pool backward scatters gradients to the wrong input elements when it reads channels_last_3d indices in storage order. | The CPU backward kernel ignores the strides of noncontiguous channels_last_3d indices. | [原文](https://github.com/pytorch/pytorch/issues/197888) |
| [#200572](torch_200572/README.md) | `torch.autograd.Function`：主要受測 API | custom Function 輸出為 input view，再回傳其 view時，custom backward 被跳過。 | 上游指出只檢查直接 grad_fn，額外 view 導致誤分類為 alias_of_input；主要是 alias metadata。 | [原文](https://github.com/pytorch/pytorch/issues/200572) |
| [#200572](torch_200572/README.md) | `torch.Tensor.unsqueeze`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | custom Function 輸出為 input view，再回傳其 view時，custom backward 被跳過。 | 上游指出只檢查直接 grad_fn，額外 view 導致誤分類為 alias_of_input；主要是 alias metadata。 | [原文](https://github.com/pytorch/pytorch/issues/200572) |
| [#200572](torch_200572/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | custom Function 輸出為 input view，再回傳其 view時，custom backward 被跳過。 | 上游指出只檢查直接 grad_fn，額外 view 導致誤分類為 alias_of_input；主要是 alias metadata。 | [原文](https://github.com/pytorch/pytorch/issues/200572) |
| [#201649](torch_201649/README.md) | `torch.compiler.nested_compile_region`：主要受測 API | 連續呼叫 nested region，forward 保存 region input 供 backward時，第一個梯度錯誤依賴 y。 | 上游指出 InvokeSubgraph MultiOutput 缺少 input-output alias 資訊，scheduler 重用仍被保存的 storage。 | [原文](https://github.com/pytorch/pytorch/issues/201649) |
| [#201649](torch_201649/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 連續呼叫 nested region，forward 保存 region input 供 backward時，第一個梯度錯誤依賴 y。 | 上游指出 InvokeSubgraph MultiOutput 缺少 input-output alias 資訊，scheduler 重用仍被保存的 storage。 | [原文](https://github.com/pytorch/pytorch/issues/201649) |
| [#202364](torch_202364/README.md) | `torch.Tensor.as_strided_`：主要受測 API | view 的 shape/stride 原地變更後 mul_，再 compiled backward時，forward 正確、gradient=[2,6,6,6]。 | 原文確認 view metadata mutation 是觸發條件；未確認錯誤 backward 的完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/202364) |
| [#202364](torch_202364/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | view 的 shape/stride 原地變更後 mul_，再 compiled backward時，forward 正確、gradient=[2,6,6,6]。 | 原文確認 view metadata mutation 是觸發條件；未確認錯誤 backward 的完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/202364) |
| [#204407](torch_204407/README.md) | `torch.linalg.slogdet`：主要受測 API | A=z.conj().imag，negative view、stride=(4,2)、offset=1時，off-diagonal gradient 轉置，real gradient 仍零。 | 上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。 | [原文](https://github.com/pytorch/pytorch/issues/204407) |
| [#204407](torch_204407/README.md) | `torch.Tensor.conj`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | A=z.conj().imag，negative view、stride=(4,2)、offset=1時，off-diagonal gradient 轉置，real gradient 仍零。 | 上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。 | [原文](https://github.com/pytorch/pytorch/issues/204407) |
| [#204407](torch_204407/README.md) | `torch.Tensor.imag`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | A=z.conj().imag，negative view、stride=(4,2)、offset=1時，off-diagonal gradient 轉置，real gradient 仍零。 | 上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。 | [原文](https://github.com/pytorch/pytorch/issues/204407) |
| [#204426](torch_204426/README.md) | `torch.compile`：Enters the compiled path | Compiled autograd connects a view created under no_grad back to its input, producing gradient [2,3,3,3] where eager produces [2,2,2,2]. | Compiled Autograd incorrectly connects a no_grad view to its input. | [原文](https://github.com/pytorch/pytorch/issues/204426) |
| [#204426](torch_204426/README.md) | `torch.no_grad`：Disables gradient recording for view creation | Compiled autograd connects a view created under no_grad back to its input, producing gradient [2,3,3,3] where eager produces [2,2,2,2]. | Compiled Autograd incorrectly connects a no_grad view to its input. | [原文](https://github.com/pytorch/pytorch/issues/204426) |
| [#204426](torch_204426/README.md) | `torch.Tensor.view`：Creates the aliased view | Compiled autograd connects a view created under no_grad back to its input, producing gradient [2,3,3,3] where eager produces [2,2,2,2]. | Compiled Autograd incorrectly connects a no_grad view to its input. | [原文](https://github.com/pytorch/pytorch/issues/204426) |
| [#205112](torch_205112/README.md) | `torch.func.jacrev`：主要受測 API | cdist(p=1) 的 jacrev 使用 batched cotangents時，各 Jacobian slice 重複第一個 cotangent 的結果。 | 上游指出 cdist_backward batching rule 沒有傳遞僅 grad 被 vmap 的 batch 維；主要為 tensor batching 表示。 | [原文](https://github.com/pytorch/pytorch/issues/205112) |
| [#205112](torch_205112/README.md) | `torch.cdist`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | cdist(p=1) 的 jacrev 使用 batched cotangents時，各 Jacobian slice 重複第一個 cotangent 的結果。 | 上游指出 cdist_backward batching rule 沒有傳遞僅 grad 被 vmap 的 batch 維；主要為 tensor batching 表示。 | [原文](https://github.com/pytorch/pytorch/issues/205112) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197084](torch_197084/README.md)：上游將此梯度症狀連結至 #198118；Issue 保留兩筆，獨立根因不應直接計為兩個。 
- [#202364](torch_202364/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#204407](torch_204407/README.md)： 必須同時保留 negative bit、stride=(4,2)、offset=1 與 alias；z.grad.imag 必須包含 A=-imag(z) 的負號鏈式法則。
