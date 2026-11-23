# tensor_representation / wrong_optimizer_update

[總目錄](../../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

Observation 定義：optimizer step 對 parameter 產生錯誤數值更新。

## 分類準則（Classification Criteria）

先滿足 `tensor_representation` 的根因分類，再以 `wrong_optimizer_update` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**1**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_optimizer_update` | 1 |

## API 摘要（API Summary）

唯一 API 數：1；Issue/API 配對數：1。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.optim.SGD` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#205497](torch_205497/README.md) | `torch.optim.SGD`：主要受測 API | CPU fused=True，parameter 與 transposed gradient 的 stride 不同時，依 memory order 配對，形成置換的錯誤更新。 | 上游指出 fused CPU kernel 忽略各 tensor stride；optimizer 是症狀場景，主要機制是 layout。 | [原文](https://github.com/pytorch/pytorch/issues/205497) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#205497](torch_205497/README.md)： 本地只測 CPU fused SGD 與 gradient stride 差異；未覆蓋 Adam、AdamW、Adagrad 或 expanded-param heap corruption。
