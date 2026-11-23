# training_state / wrong_metadata

[總目錄](../../README.md)

## 分類定義（Category Definition）

autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。

Observation 定義：shape、dtype、rank、tangent 表示或 checkpoint tensor metadata 錯誤。

## 分類準則（Classification Criteria）

先滿足 `training_state` 的根因分類，再以 `wrong_metadata` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**1**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_metadata` | 1 |

## API 摘要（API Summary）

唯一 API 數：2；Issue/API 配對數：2。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.distributed.checkpoint.DefaultSavePlanner` | 1 |
| `torch.distributed.checkpoint.save` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#204188](torch_204188/README.md) | `torch.distributed.checkpoint.save`：主要受測 API | enable_plan_caching=True，兩次 save 只有 dtype 由 bf16 變 fp16時，仍記錄 bf16，無 cache 控制組正確。 | 上游定位 class-level save plan cache 比較沒有 tensor_data.properties，屬 checkpoint state lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/204188) |
| [#204188](torch_204188/README.md) | `torch.distributed.checkpoint.DefaultSavePlanner`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | enable_plan_caching=True，兩次 save 只有 dtype 由 bf16 變 fp16時，仍記錄 bf16，無 cache 控制組正確。 | 上游定位 class-level save plan cache 比較沒有 tensor_data.properties，屬 checkpoint state lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/204188) |

## 已知限制（Known Limitations）

原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#204188](torch_204188/README.md)： 兩次保存與 planner class cache 的順序是觸發條件；完整批次驗證仍保留測試原有清理邏輯。
