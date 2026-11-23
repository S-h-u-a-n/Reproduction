# PyTorch Issue #194347

上游標題：[inductor][cpu] `torch.minimum` with signed zeros returns +0.0 under `torch.compile` on CPU while eager returns -0.0

[GitHub Issue](https://github.com/pytorch/pytorch/issues/194347) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`compilation`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.minimum` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

CPU 編譯 minimum(-0,+0)。

## 正確行為與實際行為

**Expected Behavior：** 保留本 build eager 參考的負零 signbit。

**Actual Behavior：** 回傳正零。

## 錯誤簽名（Bug Signature）

回傳正零。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Compiled CPU minimum loses sign bit and returns positive zero.

## 分類理由與根因證據

Issue 討論 SIMD minimum 的 tie／signed-zero 語意；屬數值契約，非 tensor 表示。

上游內文／討論提供機制分析，未自行修補驗證：Issue 討論 SIMD minimum 的 tie／signed-zero 語意；屬數值契約，非 tensor 表示。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/194347)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/194347#issuecomment-5373937352)、[討論 2](https://github.com/pytorch/pytorch/issues/194347#issuecomment-5382458012)、[討論 3](https://github.com/pytorch/pytorch/issues/194347#issuecomment-5775822275)、[討論 4](https://github.com/pytorch/pytorch/issues/194347#issuecomment-6897173063)、[討論 5](https://github.com/pytorch/pytorch/issues/194347#issuecomment-6914887271)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_194347`。本案檢查的是「回傳正零」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「保留本 build eager 參考的負零 signbit」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_194347/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/194347) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。；signed-zero 的 eager 比較是否納入研究契約，需研究者決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_194347/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_194347/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`06595bf6c2e8c14cee804ca9b630725a94b95782d52940ea984fdcfe9839a389`
- metadata.json SHA-256：`3a158ece9a3feca1ed4dc46de9a46c0ccda60352c6ce18da602ac55183f06ba7`
- 核對時 Issue body SHA-256：`a13d150eda95628da2408c37e117b1b167701de78e9b266ebc2a097f8e61c458`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
