# PyTorch Issue #198077

上游標題：[fx] A pickle / `torch.save` round trip silently changes what a `GraphModule` computes: in-place operator nodes (`operator.iadd`, `imul`, …) come back out-of-place, so the input is no longer mutated and dtype errors disappear

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198077) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`incorrect_state`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.fx.GraphModule` | 主要受測 API |

## 觸發條件

含 operator.iadd 的 GraphModule 經 pickle round trip。

## 正確行為與實際行為

**Expected Behavior：** 保持原地修改 input 的副作用。

**Actual Behavior：** 恢復後變成 out-of-place add，input 不變。

## 錯誤簽名（Bug Signature）

恢復後變成 out-of-place add，input 不變。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Unpickled GraphModule changes operator.iadd into out-of-place addition, leaving input unchanged.

## 分類理由與根因證據

FX 由程式碼重建圖時缺少 Proxy.__iadd__ 語意；未涉及 autograd graph lifecycle。

上游內文／討論提供機制分析，未自行修補驗證：FX 由程式碼重建圖時缺少 Proxy.__iadd__ 語意；未涉及 autograd graph lifecycle。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198077)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「恢復後變成 out-of-place add，input 不變」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「保持原地修改 input 的副作用」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/incorrect_state/torch_198077/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198077) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198077/`
- 新路徑：`bugs/needs_review/incorrect_state/torch_198077/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`6429e7bb5b5d71e95eca35ee754aafa945d703d9d0c3b2f3e51e83a39638f917`
- metadata.json SHA-256：`ce3d1bb0d4b25ad457d4cf58cfc580666d70f085f2b0869a1b2125964ddacc2c`
- 核對時 Issue body SHA-256：`59d8320fc280a5301678a27d82b3de4886fc2356c3d18c36c7503827a352ce79`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
