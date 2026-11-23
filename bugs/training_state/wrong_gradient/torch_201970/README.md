# PyTorch Issue #201970

上游標題：[inductor] FX graph cache key ignores donated buffers, so a second backward after retain_graph=True is silently wrong

[GitHub Issue](https://github.com/pytorch/pytorch/issues/201970) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`無`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`graph_lifecycle`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.compile` | 主要受測 API |
| `torch.Tensor.backward` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

先普通 backward 編譯暖機，再相同 graph 以 retain_graph=True 重複 backward。

## 正確行為與實際行為

**Expected Behavior：** 兩次梯度皆為 4。

**Actual Behavior：** 第二次梯度變成 8。

## 錯誤簽名（Bug Signature）

第二次梯度變成 8。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Reusing a cached compiled backward with donated buffers clobbers saved values and yields an incorrect second gradient.

## 分類理由與根因證據

上游指出 FX cache key 沒有 donation 資訊，重用會覆寫 saved buffer 的 backward。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 FX cache key 沒有 donation 資訊，重用會覆寫 saved buffer 的 backward。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/201970)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/201970#issuecomment-6804658887)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「第二次梯度變成 8」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「兩次梯度皆為 4」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/wrong_gradient/torch_201970/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/201970) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

必須保留測試內的普通 backward 暖機與 cache/donation 狀態；不可任意清空所需 cache。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_201970/`
- 新路徑：`bugs/training_state/wrong_gradient/torch_201970/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`1cdb4951b071790577abcf6b6f6342eeec8060d819681aaee6d3437ba5675967`
- metadata.json SHA-256：`9074445045a226356a38294d38d3e2c07df68d72bd5007be2f09b2e156ef29a9`
- 核對時 Issue body SHA-256：`f0f97f080e0bd3506e32c72011d34b6e47139d50ecb4f65d3adc47bbaf30f50b`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
