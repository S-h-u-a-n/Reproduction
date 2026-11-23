# training_state / incorrect_state

[總目錄](../../README.md)

## 分類定義（Category Definition）

autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。

Observation 定義：alias 寫入後的可觀察狀態、Python 容器副作用、物件／parameter 存活等狀態不符；不代表 Primary Cause 必為 training_state。

## 分類準則（Classification Criteria）

先滿足 `training_state` 的根因分類，再以 `incorrect_state` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**13**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `incorrect_state` | 13 |

## API 摘要（API Summary）

唯一 API 數：21；Issue/API 配對數：23。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.compile` | 3 |
| `num_batches_tracked` | 1 |
| `torch._dynamo.graph_break` | 1 |
| `torch.amp.autocast` | 1 |
| `torch.amp.GradScaler` | 1 |
| `torch.ao.quantization.observer.PerChannelMinMaxObserver` | 1 |
| `torch.autocast` | 1 |
| `torch.distributed.checkpoint.state_dict.get_optimizer_state_dict` | 1 |
| `torch.distributed.checkpoint.state_dict.set_optimizer_state_dict` | 1 |
| `torch.nn.BatchNorm1d` | 1 |
| `torch.nn.utils.clip_grad_norm_` | 1 |
| `torch.nn.utils.get_total_norm` | 1 |
| `torch.optim.Adam` | 1 |
| `torch.optim.Optimizer.load_state_dict` | 1 |
| `torch.optim.Optimizer.state_dict` | 1 |
| `torch.optim.SGD` | 1 |
| `torch.optim.SGD.load_state_dict` | 1 |
| `torch.optim.swa_utils.AveragedModel` | 1 |
| `torch.Tensor.add_` | 1 |
| `torch.Tensor.detach` | 1 |
| `torch.utils.checkpoint.create_selective_checkpoint_contexts` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#192202](torch_192202/README.md) | `torch.distributed.checkpoint.state_dict.get_optimizer_state_dict` | 載入 optimizer checkpoint 時，凍結其中一個參數使還原的狀態由兩組減為一組。 | Root cause not confirmed；分類依本地案例的觸發條件與觀察結果。 | [原文](https://github.com/pytorch/pytorch/issues/192202) |
| [#192202](torch_192202/README.md) | `torch.distributed.checkpoint.state_dict.set_optimizer_state_dict` | 載入 optimizer checkpoint 時，凍結其中一個參數使還原的狀態由兩組減為一組。 | Root cause not confirmed；分類依本地案例的觸發條件與觀察結果。 | [原文](https://github.com/pytorch/pytorch/issues/192202) |
| [#195488](torch_195488/README.md) | `torch.amp.autocast` | index_select throws IndexError, compiled context retains the nesting count while eager would restore it. | 編譯區域發生例外時 autocast nesting 未正常清理，造成後續訓練狀態洩漏。 | [原文](https://github.com/pytorch/pytorch/issues/195488) |
| [#195488](torch_195488/README.md) | `torch.compile` | index_select throws IndexError, compiled context retains the nesting count while eager would restore it. | 編譯區域發生例外時 autocast nesting 未正常清理，造成後續訓練狀態洩漏。 | [原文](https://github.com/pytorch/pytorch/issues/195488) |
| [#196083](torch_196083/README.md) | `torch.optim.Optimizer.state_dict`：Exports optimizer state | SGD momentum_buffer shares data_ptr across optimizers and a destination step modifies the source buffer. | In-process optimizer state transfer aliases SGD momentum buffers; updating the new optimizer mutates the original optimizer state. | [原文](https://github.com/pytorch/pytorch/issues/196083) |
| [#196083](torch_196083/README.md) | `torch.optim.Optimizer.load_state_dict`：Loads momentum state into the destination optimizer | SGD momentum_buffer shares data_ptr across optimizers and a destination step modifies the source buffer. | In-process optimizer state transfer aliases SGD momentum buffers; updating the new optimizer mutates the original optimizer state. | [原文](https://github.com/pytorch/pytorch/issues/196083) |
| [#198624](torch_198624/README.md) | `torch.Tensor.detach` | Detached alias 的原地加法在 eager 保留 autograd history，編譯後回傳值失去梯度歷史。 | Root cause not confirmed；分類依本地案例的觸發條件與觀察結果。 | [原文](https://github.com/pytorch/pytorch/issues/198624) |
| [#198624](torch_198624/README.md) | `torch.Tensor.add_` | Detached alias 的原地加法在 eager 保留 autograd history，編譯後回傳值失去梯度歷史。 | Root cause not confirmed；分類依本地案例的觸發條件與觀察結果。 | [原文](https://github.com/pytorch/pytorch/issues/198624) |
| [#198624](torch_198624/README.md) | `torch.compile` | Detached alias 的原地加法在 eager 保留 autograd history，編譯後回傳值失去梯度歷史。 | Root cause not confirmed；分類依本地案例的觸發條件與觀察結果。 | [原文](https://github.com/pytorch/pytorch/issues/198624) |
| [#199151](torch_199151/README.md) | `torch.ao.quantization.observer.PerChannelMinMaxObserver` | PerChannelMinMaxObserver loses float64 on reset, unlike MinMaxObserver. | PerChannelMinMaxObserver 在 reset 後丟失 float64 dtype 設定，導致狀態 dtype 回退。 | [原文](https://github.com/pytorch/pytorch/issues/199151) |
| [#201158](torch_201158/README.md) | `torch.utils.checkpoint.create_selective_checkpoint_contexts` | Forward output matches eager but forward.storage contains different activation values. | Selective checkpointing 快取持有 Inductor 之後重用的 buffer，導致已儲存的中間 Tensor 被覆寫。 | [原文](https://github.com/pytorch/pytorch/issues/201158) |
| [#201615](torch_201615/README.md) | `torch.optim.SGD`：Exercises the fused optimizer step | Fused SGD has a NaN momentum_buffer after a skipped first step and corrupts its first actual update. | A skipped fused-SGD step creates uninitialized momentum state, making the next valid optimizer update NaN. | [原文](https://github.com/pytorch/pytorch/issues/201615) |
| [#201615](torch_201615/README.md) | `torch.amp.GradScaler`：Skips the first optimizer step on nonfinite gradients | Fused SGD has a NaN momentum_buffer after a skipped first step and corrupts its first actual update. | A skipped fused-SGD step creates uninitialized momentum state, making the next valid optimizer update NaN. | [原文](https://github.com/pytorch/pytorch/issues/201615) |
| [#201669](torch_201669/README.md) | `torch.optim.SGD.load_state_dict`：Reloads FP32 momentum for bfloat16 parameters | FP32 momentum buffer [1025,1.00390625] is narrowed to bfloat16 [1024,1.0] after load_state_dict. | Optimizer state reload silently narrows FP32 momentum buffers to bfloat16 because the parameter dtype is bfloat16. | [原文](https://github.com/pytorch/pytorch/issues/201669) |
| [#202706](torch_202706/README.md) | `torch.autocast`：Decorates the recursively called function | Autocast starts disabled but is left enabled after a recursive call of the same decorated function. | Nested calls of an autocast decorator accidentally reuse context state, leaving autocast enabled after exit. | [原文](https://github.com/pytorch/pytorch/issues/202706) |
| [#203921](torch_203921/README.md) | `torch.optim.swa_utils.AveragedModel` | 兩次 EMA 更新後，浮點參數已更新，int64 buffer 仍為 1，預期為 2。 | Root cause not confirmed；分類依本地案例的觸發條件與觀察結果。 | [原文](https://github.com/pytorch/pytorch/issues/203921) |
| [#204269](torch_204269/README.md) | `torch.nn.utils.clip_grad_norm_`：Public gradient-clipping entry point | A pair of gradient tensors with three nonzero elements returns a total 0-norm of two. | The 0-norm of gradients counts nonzero tensors instead of nonzero gradient elements. | [原文](https://github.com/pytorch/pytorch/issues/204269) |
| [#204269](torch_204269/README.md) | `torch.nn.utils.get_total_norm`：Computes the total gradient norm | A pair of gradient tensors with three nonzero elements returns a total 0-norm of two. | The 0-norm of gradients counts nonzero tensors instead of nonzero gradient elements. | [原文](https://github.com/pytorch/pytorch/issues/204269) |
| [#204339](torch_204339/README.md) | `torch.optim.Adam`：主要受測 API | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204339](torch_204339/README.md) | `torch._dynamo.graph_break`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204339](torch_204339/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204775](torch_204775/README.md) | `torch.nn.BatchNorm1d`：Training module under test | After an empty then a real batch, num_batches_tracked=2 and running_mean=running_var=0.5 instead of counter=1, mean=1, var=0. | Root cause not confirmed. An empty training batch advances the cumulative BatchNorm counter and changes the weight of the next running-statistics update. | [原文](https://github.com/pytorch/pytorch/issues/204775) |
| [#204775](torch_204775/README.md) | `num_batches_tracked`：Batch counter observed before and after the real batch | After an empty then a real batch, num_batches_tracked=2 and running_mean=running_var=0.5 instead of counter=1, mean=1, var=0. | Root cause not confirmed. An empty training batch advances the cumulative BatchNorm counter and changes the weight of the next running-statistics update. | [原文](https://github.com/pytorch/pytorch/issues/204775) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#204339](torch_204339/README.md)：根因證據尚不足；分類依已知必要觸發條件。 使用內部 optimizer API、GC 控制與弱引用；只驗證 parameter lifetime，沒有聲稱 optimizer 數值更新錯誤。
- [#195488](torch_195488/README.md)：Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
- [#199151](torch_199151/README.md)：Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
- [#201158](torch_201158/README.md)：Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
