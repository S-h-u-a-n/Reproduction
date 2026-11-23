# PyTorch Issue #200924

上游標題：[dynamo] `not d` and `bool(d)` on a dict input add no guard on its emptiness, so the graph is reused with wrong results

[GitHub Issue](https://github.com/pytorch/pytorch/issues/200924) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.compile` | 主要受測 API |

## 觸發條件

先空 dict 再非空 dict 的 bool(dict)。

## 正確行為與實際行為

**Expected Behavior：** 依當次容器內容選擇結果。

**Actual Behavior：** 重用舊空 dict 路徑。

## 錯誤簽名（Bug Signature）

重用舊空 dict 路徑。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Graph cached for empty dict is wrongly reused and yields old branch result for a non-empty dict.

## 分類理由與根因證據

上游指出 dict truthiness 缺少 emptiness guard；一般 Python cache，非訓練狀態。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 dict truthiness 缺少 emptiness guard；一般 Python cache，非訓練狀態。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/200924)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/200924#issuecomment-6407558146)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「重用舊空 dict 路徑」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「依當次容器內容選擇結果」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_200924/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/200924) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_200924/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_200924/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`77cb41dd08de97a4423e6d8605d8ea60d3b5b23089e56f093d4da3b9e355764b`
- metadata.json SHA-256：`f8e4097cfcd19f48a05b27166d4f7fdd3000b33e7201816e16ca6ed62c80e687`
- 核對時 Issue body SHA-256：`531cd0bda977c708337f19424bc7b18029eac570a2e0aa5fdcbf1b51a4a7f825`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
