# needs_review / unexpected_exception

[總目錄](../../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

Observation 定義：本應成功或可由使用者 handler 處理的操作，拋出非預期 Python／編譯例外；不等同 process crash。

## 分類準則（Classification Criteria）

先滿足 `needs_review` 的根因分類，再以 `unexpected_exception` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**2**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `unexpected_exception` | 2 |

## API 摘要（API Summary）

唯一 API 數：3；Issue/API 配對數：4。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.compile` | 2 |
| `torch.nn.Parameter` | 1 |
| `torch.nn.functional.linear` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#204945](torch_204945/README.md) | `torch.nn.Parameter`：主要受測 API | compiled function 內建立 Parameter 後檢查 type(p)時，SYNTHETIC_LOCAL NameError／InternalTorchDynamoError。 | 上游定位一般 type-source guard 引用了不可 guard 的 SyntheticLocalSource；未顯示訓練狀態毀損，故保留 needs_review。 | [原文](https://github.com/pytorch/pytorch/issues/204945) |
| [#204945](torch_204945/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled function 內建立 Parameter 後檢查 type(p)時，SYNTHETIC_LOCAL NameError／InternalTorchDynamoError。 | 上游定位一般 type-source guard 引用了不可 guard 的 SyntheticLocalSource；未顯示訓練狀態毀損，故保留 needs_review。 | [原文](https://github.com/pytorch/pytorch/issues/204945) |
| [#205823](torch_205823/README.md) | `torch.nn.functional.linear`：主要受測 API | freezing=True 且 enable_linear_binary_folding=True，乘 parameter reciprocal時，FX graph reciprocal use-before-definition 例外。 | 上游定位 linear binary folding 的節點排序；本例推論 graph rewrite，沒有訓練狀態或 tensor 表示根因證據。 | [原文](https://github.com/pytorch/pytorch/issues/205823) |
| [#205823](torch_205823/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | freezing=True 且 enable_linear_binary_folding=True，乘 parameter reciprocal時，FX graph reciprocal use-before-definition 例外。 | 上游定位 linear binary folding 的節點排序；本例推論 graph rewrite，沒有訓練狀態或 tensor 表示根因證據。 | [原文](https://github.com/pytorch/pytorch/issues/205823) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#204945](torch_204945/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 原測試捕捉較寬的外層 Exception，再檢查 SYNTHETIC_LOCAL／NameError 訊息鏈；本次不修改其斷言。
- [#205823](torch_205823/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 freezing 與 linear binary folding 兩個開關及 reciprocal 節點順序不可省略。
