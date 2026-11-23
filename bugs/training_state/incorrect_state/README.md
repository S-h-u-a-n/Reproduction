# training_state / incorrect_state

[總目錄](../../README.md)

## 分類定義（Category Definition）

autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。

Observation 定義：alias 寫入後的可觀察狀態、Python 容器副作用、物件／parameter 存活等狀態不符；不代表 Primary Cause 必為 training_state。

## 分類準則（Classification Criteria）

先滿足 `training_state` 的根因分類，再以 `incorrect_state` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**1**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `incorrect_state` | 1 |

## API 摘要（API Summary）

唯一 API 數：3；Issue/API 配對數：3。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch._dynamo.graph_break` | 1 |
| `torch.compile` | 1 |
| `torch.optim.Adam` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#204339](torch_204339/README.md) | `torch.optim.Adam`：主要受測 API | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204339](torch_204339/README.md) | `torch._dynamo.graph_break`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204339](torch_204339/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |

## 已知限制（Known Limitations）

原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#204339](torch_204339/README.md)：根因證據尚不足；分類依已知必要觸發條件。 使用內部 optimizer API、GC 控制與弱引用；只驗證 parameter lifetime，沒有聲稱 optimizer 數值更新錯誤。
