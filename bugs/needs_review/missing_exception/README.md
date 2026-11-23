# needs_review / missing_exception

[總目錄](../../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

Observation 定義：必要的輸入驗證、dtype 契約或 autograd version conflict 沒有拋出應有例外。

## 分類準則（Classification Criteria）

先滿足 `needs_review` 的根因分類，再以 `missing_exception` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**0**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `missing_exception` | 0 |

## API 摘要（API Summary）

唯一 API 數：0；Issue/API 配對數：0。

## Issue／API 詳細說明與 GitHub 來源

目前無案例。

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。
