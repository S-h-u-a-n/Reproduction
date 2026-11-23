# PyTorch Issue #187806

上游標題：F.gelu(approximate='none'): 1+erf catastrophic cancellation — up to 57% relative error in fp32 around x≈−5, zeros the negative tail

[GitHub Issue](https://github.com/pytorch/pytorch/issues/187806) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`other`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.nn.functional.gelu` | 主要受測 API |
| `torch.special.erfc` | 建立正確參考的控制 API |

## 觸發條件

固定負值 float32 的 GELU 尾端。

## 正確行為與實際行為

**Expected Behavior：** erfc 與 math.erfc 參考皆為有限非零負值。

**Actual Behavior：** 內建 GELU 回傳零。

## 錯誤簽名（Bug Signature）

內建 GELU 回傳零。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Float32 builtin GELU zeros the negative tail through cancellation, whereas the equivalent erfc formula stays nonzero.

## 分類理由與根因證據

Issue 指向 erf 公式的相消，屬數值公式問題，無 tensor 表示或訓練狀態觸發證據。

上游內文／討論提供機制分析，未自行修補驗證：Issue 指向 erf 公式的相消，屬數值公式問題，無 tensor 表示或訓練狀態觸發證據。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/187806)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/187806#issuecomment-4764776705)、[討論 2](https://github.com/pytorch/pytorch/issues/187806#issuecomment-4766545188)、[討論 3](https://github.com/pytorch/pytorch/issues/187806#issuecomment-4792650823)、[討論 4](https://github.com/pytorch/pytorch/issues/187806#issuecomment-4861864557)、[討論 5](https://github.com/pytorch/pytorch/issues/187806#issuecomment-6871564837)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「內建 GELU 回傳零」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「erfc 與 math.erfc 參考皆為有限非零負值」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_187806/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/187806) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_187806/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_187806/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`4c4ef5f17c0a123980427dd1ceeb5e432f1c5071ef2d9bd5edf267a5eb5d9f73`
- metadata.json SHA-256：`78492bfa49032e22524795ebf963d902487ed04e704e562cc5a04d8a170e03d8`
- 核對時 Issue body SHA-256：`5410ab3bcc330683c1c11629965f1cf010cd61c6cb410deaf2c0204b491958c2`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
