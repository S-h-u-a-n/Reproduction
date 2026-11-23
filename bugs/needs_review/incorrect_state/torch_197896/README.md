# PyTorch Issue #197896

上游標題：[dynamo] Mutations of a closure-captured list/dict are silently dropped when they happen in a method of a locally defined class instantiated inside the compiled function (`fullgraph=True`, no graph break)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197896) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`incorrect_state`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.compile` | 主要受測 API |

## 觸發條件

compiled function 內建立 local class，方法修改 closure list。

## 正確行為與實際行為

**Expected Behavior：** 每次呼叫應重播 list.append。

**Actual Behavior：** tensor 結果正常但 list 未更新。

## 錯誤簽名（Bug Signature）

tensor 結果正常但 list 未更新。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Under Dynamo the local helper method executes without replaying list.append side effects.

## 分類理由與根因證據

上游指出 local class method 的來源追蹤遺失，屬 Python side-effect replay。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 local class method 的來源追蹤遺失，屬 Python side-effect replay。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197896)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197896#issuecomment-5768666734)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「tensor 結果正常但 list 未更新」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「每次呼叫應重播 list.append」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/incorrect_state/torch_197896/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197896) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197896/`
- 新路徑：`bugs/needs_review/incorrect_state/torch_197896/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`fa302057d51e821a5e04575397d08f44ebcd491f0524dfd08e30a71e643b52f3`
- metadata.json SHA-256：`f85a6179a43b70d800b538730554d1fb310966a2fac4794956fedd5fa2b5ffef`
- 核對時 Issue body SHA-256：`c7f466432d1591bdf7a4666818966c9571ea789bb4da35018f2b3c79bbfd8281`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
