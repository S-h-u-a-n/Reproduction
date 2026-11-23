# PyTorch Issue #197889

上游標題：[pt2] Python float argument that changes between calls goes stale in the cached graph (residual of #194976): norm `eps`, `huber_loss` delta, SDPA `scale`, `interpolate(scale_factor=...)` keep an earlier value (`interpolate`: old output shape)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197889) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_metadata`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.nn.functional.interpolate` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

同程序依序傳入 scale 0.9、0.5、0.25、2.0。

## 正確行為與實際行為

**Expected Behavior：** 輸出尾維依序為 7、6、5、12。

**Actual Behavior：** 實際為 7、6、6、6，後兩次 shape 過期。

## 錯誤簽名（Bug Signature）

實際為 7、6、6、6，後兩次 shape 過期。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Preserve four calls in one process, scale sequence 0.9,0.5,0.25,2.0: expected output tail sizes 7,6,5,12; compiled sizes 7,6,6,6. All complete output shapes are checked.

## 分類理由與根因證據

上游指向 AOT cache 省略 float specialization guards；本例沒有訓練狀態，不能因 cache 名稱而歸入 training_state。

上游內文／討論提供機制分析，未自行修補驗證：上游指向 AOT cache 省略 float specialization guards；本例沒有訓練狀態，不能因 cache 名稱而歸入 training_state。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197889)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197889#issuecomment-5769751990)、[討論 2](https://github.com/pytorch/pytorch/issues/197889#issuecomment-6115356093)、[討論 3](https://github.com/pytorch/pytorch/issues/197889#issuecomment-6900939606)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「實際為 7、6、6、6，後兩次 shape 過期」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「輸出尾維依序為 7、6、5、12」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_metadata/torch_197889/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197889) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

四次 scale 呼叫的程序歷史是必要條件；不得將四次拆成四個互不相關程序。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197889/`
- 新路徑：`bugs/needs_review/wrong_metadata/torch_197889/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`7d1305e182bfe669ff1ec3389565bf2bbfd549951f9b2a91545f52d2571456d9`
- metadata.json SHA-256：`2714d4fcfcd4aa53c3b888344239197d0644be4757c817378e987bc89573ddd3`
- 核對時 Issue body SHA-256：`149da50002193bd6b5b50d8bb42419d2180df64b795b7f9219c7643ceae361f6`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
