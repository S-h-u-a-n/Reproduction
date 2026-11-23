# training_state / unexpected_exception

[總目錄](../../README.md)

## 分類定義（Category Definition）

autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。

Observation 定義：本應成功或可由使用者 handler 處理的操作，拋出非預期 Python／編譯例外；不等同 process crash。

## 分類準則（Classification Criteria）

先滿足 `training_state` 的根因分類，再以 `unexpected_exception` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**5**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `unexpected_exception` | 5 |

## API 摘要（API Summary）

唯一 API 數：8；Issue/API 配對數：11。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.compile` | 4 |
| `torch.Tensor.backward` | 1 |
| `torch._dynamo.compiled_autograd._enable` | 1 |
| `torch.linalg.vander` | 1 |
| `torch.nn.Parameter` | 1 |
| `torch.nn.functional.interpolate` | 1 |
| `torch.utils.checkpoint.checkpoint` | 1 |
| `torch.vander` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197092](torch_197092/README.md) | `torch.nn.functional.interpolate`：主要受測 API | compiled autograd、bilinear interpolation backward時，fake-tensor propagation 出現 isIntList INTERNAL ASSERT。 | 問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/197092) |
| [#197092](torch_197092/README.md) | `torch._dynamo.compiled_autograd._enable`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | compiled autograd、bilinear interpolation backward時，fake-tensor propagation 出現 isIntList INTERNAL ASSERT。 | 問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/197092) |
| [#197092](torch_197092/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled autograd、bilinear interpolation backward時，fake-tensor propagation 出現 isIntList INTERNAL ASSERT。 | 問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/197092) |
| [#199215](torch_199215/README.md) | `torch.nn.Parameter`：主要受測 API | 整數 Parameter(requires_grad=False)，freezing 且 discard_parameters時，內層 RuntimeError 指出僅浮點 dtype 可要求梯度。 | freezing 丟棄 parameter 時建立 ErasedTensor 並無條件 requires_grad_(True)，屬 parameter lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/199215) |
| [#199215](torch_199215/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 整數 Parameter(requires_grad=False)，freezing 且 discard_parameters時，內層 RuntimeError 指出僅浮點 dtype 可要求梯度。 | freezing 丟棄 parameter 時建立 ErasedTensor 並無條件 requires_grad_(True)，屬 parameter lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/199215) |
| [#199258](torch_199258/README.md) | `torch.utils.checkpoint.checkpoint`：主要受測 API | use_reentrant=False，區域中含 x*1.0時，NetworkXError: node source not in graph。 | 上游 min-cut 分析指出 identity elimination 與 checkpoint recomputation tags 使分割圖退化。 | [原文](https://github.com/pytorch/pytorch/issues/199258) |
| [#199258](torch_199258/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | use_reentrant=False，區域中含 x*1.0時，NetworkXError: node source not in graph。 | 上游 min-cut 分析指出 identity elimination 與 checkpoint recomputation tags 使分割圖退化。 | [原文](https://github.com/pytorch/pytorch/issues/199258) |
| [#199941](torch_199941/README.md) | `torch.vander`：主要受測 API | vander 輸出求和後 backward時，saved-variable inplace-modification RuntimeError。 | 上游指出建立 Vandermonde 的 inplace slice 寫入破壞 autograd 保存版本。 | [原文](https://github.com/pytorch/pytorch/issues/199941) |
| [#199941](torch_199941/README.md) | `torch.linalg.vander`：建立正確參考的控制 API | vander 輸出求和後 backward時，saved-variable inplace-modification RuntimeError。 | 上游指出建立 Vandermonde 的 inplace slice 寫入破壞 autograd 保存版本。 | [原文](https://github.com/pytorch/pytorch/issues/199941) |
| [#204544](torch_204544/README.md) | `torch.compile` | Static backward twice succeeds, dynamic retained backward raises donated buffers error. | 動態維度編譯後的 retained backward 誤判 donated buffer 不可重複使用。 | [原文](https://github.com/pytorch/pytorch/issues/204544) |
| [#204544](torch_204544/README.md) | `torch.Tensor.backward` | Static backward twice succeeds, dynamic retained backward raises donated buffers error. | 動態維度編譯後的 retained backward 誤判 donated buffer 不可重複使用。 | [原文](https://github.com/pytorch/pytorch/issues/204544) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197092](torch_197092/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#204544](torch_204544/README.md)：Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
