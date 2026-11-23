# PyTorch Issue #198189

上游標題：[dynamo] `OrderedDict.move_to_end()` on a dict passed into a compiled function is silently dropped: the reorder is not replayed as a side effect, so an LRU cache evicts the wrong entry (`fullgraph=True` does not complain)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/198189) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`incorrect_state`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `collections.OrderedDict.move_to_end` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

compiled function 重排傳入的 OrderedDict。

## 正確行為與實際行為

**Expected Behavior：** key 順序與 eager 相同。

**Actual Behavior：** 重排副作用被省略。

## 錯誤簽名（Bug Signature）

重排副作用被省略。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Dynamo fails to replay the OrderedDict reordering side effect.

## 分類理由與根因證據

上游指出 should_reconstruct_all 未設定；屬 Python 容器狀態而非訓練狀態。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 should_reconstruct_all 未設定；屬 Python 容器狀態而非訓練狀態。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/198189)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/198189#issuecomment-5778791015)、[討論 2](https://github.com/pytorch/pytorch/issues/198189#issuecomment-5872683088)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「重排副作用被省略」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「key 順序與 eager 相同」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/incorrect_state/torch_198189/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/198189) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_198189/`
- 新路徑：`bugs/needs_review/incorrect_state/torch_198189/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`41a4a7ea149e2bef023c006a740570a8e2306609cb0b69ccc806af23914e08db`
- metadata.json SHA-256：`b4a3e61c456e694c19dba330a5dd0785e46e2dfb8d915568c0d01cc8d29c2749`
- 核對時 Issue body SHA-256：`6e6e17d1e9a80f3bb4569084f4902ac99e92ad1872382c45461aafd83ddaef05`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
