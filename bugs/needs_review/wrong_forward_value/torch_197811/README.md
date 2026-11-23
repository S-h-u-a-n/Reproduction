# PyTorch Issue #197811

上游標題：[dynamo] torch.compile silently reuses a graph when closures capture different Tensor method descriptors

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197811) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.__add__` | 主要受測 API |
| `torch.Tensor.__mul__` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

兩個 closure 分別擷取 Tensor 的加法與乘法 descriptor。

## 正確行為與實際行為

**Expected Behavior：** x=6,y=3 時分別回傳 9、18。

**Actual Behavior：** 乘法 closure 重用加法圖而回傳 9。

## 錯誤簽名（Bug Signature）

乘法 closure 重用加法圖而回傳 9。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> The cached compiled graph for multiplication reuses addition and incorrectly returns 9.

## 分類理由與根因證據

捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。

上游內文／討論提供機制分析，未自行修補驗證：捕獲 descriptor 的 guard 不完整，屬一般 Python callable 快取語意。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197811)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_197811`。本案檢查的是「乘法 closure 重用加法圖而回傳 9」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「x=6,y=3 時分別回傳 9、18」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_197811/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197811) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197811/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_197811/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`380466ab407f79e493355a049a5d169900df234fed70d1e2ad90b7d91db219f0`
- metadata.json SHA-256：`6a78bc273ef52264942a527aefb4ef2d8bbc38eb87d39777afe08aa439f11075`
- 核對時 Issue body SHA-256：`b7655b15c28cfe8cd34ef8be14dc272a57d239313ebce4ca064e7d6489e7c9e4`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
