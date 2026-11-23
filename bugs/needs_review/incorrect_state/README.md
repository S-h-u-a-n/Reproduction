# needs_review / incorrect_state

[總目錄](../../README.md)

## 分類定義（Category Definition）

根因證據不足，或目前已知機制無法合理歸入前兩類；也包含純數值公式、一般 Python 副作用／guard、code generation 等待研究範圍決策的案例。並不表示未復現或 testcase 無效。

Observation 定義：alias 寫入後的可觀察狀態、Python 容器副作用、物件／parameter 存活等狀態不符；不代表 Primary Cause 必為 training_state。

## 分類準則（Classification Criteria）

先滿足 `needs_review` 的根因分類，再以 `incorrect_state` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**3**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `incorrect_state` | 3 |

## API 摘要（API Summary）

唯一 API 數：3；Issue/API 配對數：4。

| API | 涉及 Issue 數 |
| --- | ---: |
| `collections.OrderedDict.move_to_end` | 1 |
| `torch.compile` | 2 |
| `torch.fx.GraphModule` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197896](torch_197896/README.md) | `torch.compile`：主要受測 API | compiled function 內建立 local class，方法修改 closure list時，tensor 結果正常但 list 未更新。 | 上游指出 local class method 的來源追蹤遺失，屬 Python side-effect replay。 | [原文](https://github.com/pytorch/pytorch/issues/197896) |
| [#198077](torch_198077/README.md) | `torch.fx.GraphModule`：主要受測 API | 含 operator.iadd 的 GraphModule 經 pickle round trip時，恢復後變成 out-of-place add，input 不變。 | FX 由程式碼重建圖時缺少 Proxy.__iadd__ 語意；未涉及 autograd graph lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/198077) |
| [#198189](torch_198189/README.md) | `collections.OrderedDict.move_to_end`：主要受測 API | compiled function 重排傳入的 OrderedDict時，重排副作用被省略。 | 上游指出 should_reconstruct_all 未設定；屬 Python 容器狀態而非訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/198189) |
| [#198189](torch_198189/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled function 重排傳入的 OrderedDict時，重排副作用被省略。 | 上游指出 should_reconstruct_all 未設定；屬 Python 容器狀態而非訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/198189) |

## 已知限制（Known Limitations）

原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197896](torch_197896/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198077](torch_198077/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
- [#198189](torch_198189/README.md)：研究範圍：目前機制不宜合理歸入另兩類，保留待決定。 
