# needs_review / wrong_metadata

[總目錄](../../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

Observation 定義：shape、dtype、rank、tangent 表示或 checkpoint tensor metadata 錯誤。

## 分類準則（Classification Criteria）

先滿足 `needs_review` 的根因分類，再以 `wrong_metadata` 作主要可觀察簽名；其餘症狀只列 Secondary。

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
| `torch.compile` | 1 |
| `torch.nn.functional.interpolate` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197889](torch_197889/README.md) | `torch.nn.functional.interpolate`：主要受測 API | 同程序依序傳入 scale 0.9、0.5、0.25、2.0時，實際為 7、6、6、6，後兩次 shape 過期。 | 上游指向 AOT cache 省略 float specialization guards；本例沒有訓練狀態，不能因 cache 名稱而歸入 training_state。 | [原文](https://github.com/pytorch/pytorch/issues/197889) |
| [#197889](torch_197889/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 同程序依序傳入 scale 0.9、0.5、0.25、2.0時，實際為 7、6、6、6，後兩次 shape 過期。 | 上游指向 AOT cache 省略 float specialization guards；本例沒有訓練狀態，不能因 cache 名稱而歸入 training_state。 | [原文](https://github.com/pytorch/pytorch/issues/197889) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197889](torch_197889/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 四次 scale 呼叫的程序歷史是必要條件；不得將四次拆成四個互不相關程序。
