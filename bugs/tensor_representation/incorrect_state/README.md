# tensor_representation / incorrect_state

[總目錄](../../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

Observation 定義：alias 寫入後的可觀察狀態、Python 容器副作用、物件／parameter 存活等狀態不符；不代表 Primary Cause 必為 training_state。

## 分類準則（Classification Criteria）

先滿足 `tensor_representation` 的根因分類，再以 `incorrect_state` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**4**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `incorrect_state` | 4 |

## API 摘要（API Summary）

唯一 API 數：7；Issue/API 配對數：9。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.Tensor.div` | 1 |
| `torch.Tensor.split` | 1 |
| `torch.cat` | 1 |
| `torch.compile` | 3 |
| `torch.slice_scatter` | 1 |
| `torch.Tensor.copy_` | 1 |
| `torch.cond` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#195451](torch_195451/README.md) | `torch.slice_scatter`：主要受測 API | functional scatter、輸入 mutation 與回傳結果時，回傳結果 alias 輸入，修改結果連帶改變輸入。 | 上游 reinplace／copy-back 分析指出 fresh output 被當成 input alias。 | [原文](https://github.com/pytorch/pytorch/issues/195451) |
| [#195451](torch_195451/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | functional scatter、輸入 mutation 與回傳結果時，回傳結果 alias 輸入，修改結果連帶改變輸入。 | 上游 reinplace／copy-back 分析指出 fresh output 被當成 input alias。 | [原文](https://github.com/pytorch/pytorch/issues/195451) |
| [#197893](torch_197893/README.md) | `torch.Tensor.div`：主要受測 API | 編譯 x/1 後修改回傳 tensor時，結果與 input 共用 storage，修改相互影響。 | remove_no_ops 把圖輸出替換為 input，改變 alias 契約。 | [原文](https://github.com/pytorch/pytorch/issues/197893) |
| [#197893](torch_197893/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 編譯 x/1 後修改回傳 tensor時，結果與 input 共用 storage，修改相互影響。 | remove_no_ops 把圖輸出替換為 input，改變 alias 契約。 | [原文](https://github.com/pytorch/pytorch/issues/197893) |
| [#201590](torch_201590/README.md) | `torch.cond`：主要受測 API | aot_eager 接受同時執行 copy_ 並回傳輸入 alias 的 cond 分支，無 mutation 的 alias 控制組被拒絕。 | 本地測試比較 mutation 與非 mutation 分支，並檢查回傳值和輸入的 storage 指標。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/201590) |
| [#201590](torch_201590/README.md) | `torch.Tensor.copy_`：共同觸發的原地寫入操作 | aot_eager 接受同時執行 copy_ 並回傳輸入 alias 的 cond 分支，無 mutation 的 alias 控制組被拒絕。 | 本地測試比較 mutation 與非 mutation 分支，並檢查回傳值和輸入的 storage 指標。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/201590) |
| [#205682](torch_205682/README.md) | `torch.cat`：主要受測 API | 同正軸 cat 後按原長度 split，另有 mixed dtype 控制時，寫 split 修改 input；第一份 mixed output 留在 int32。 | 上游 ablation 指向 cat_splitwithsizes_replace 重寫，丟失新 storage 與 dtype promotion。 | [原文](https://github.com/pytorch/pytorch/issues/205682) |
| [#205682](torch_205682/README.md) | `torch.Tensor.split`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 同正軸 cat 後按原長度 split，另有 mixed dtype 控制時，寫 split 修改 input；第一份 mixed output 留在 int32。 | 上游 ablation 指向 cat_splitwithsizes_replace 重寫，丟失新 storage 與 dtype promotion。 | [原文](https://github.com/pytorch/pytorch/issues/205682) |
| [#205682](torch_205682/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 同正軸 cat 後按原長度 split，另有 mixed dtype 控制時，寫 split 修改 input；第一份 mixed output 留在 int32。 | 上游 ablation 指向 cat_splitwithsizes_replace 重寫，丟失新 storage 與 dtype promotion。 | [原文](https://github.com/pytorch/pytorch/issues/205682) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

