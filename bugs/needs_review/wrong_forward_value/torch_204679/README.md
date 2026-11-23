# PyTorch Issue #204679

上游標題：CPU prod of BFloat16/Half accumulates in the input dtype (dense and sparse CSR)

[GitHub Issue](https://github.com/pytorch/pytorch/issues/204679) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`needs_review`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`other`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.prod` | 主要受測 API |

## 觸發條件

AVX512 CPU 對 1000 個 BF16 129/128 求積。

## 正確行為與實際行為

**Expected Behavior：** Decimal 參考轉 BF16 為 2400。

**Actual Behavior：** 本 build 回傳 1632。

## 錯誤簽名（Bug Signature）

本 build 回傳 1632。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Dense BF16 CPU prod returns the upstream-reported 1632 on this AVX512 build. This exact wrong value is an environment-scoped signature, not a claim for every SIMD width, CSR path or float16 input; these variants remain outside validation.

## 分類理由與根因證據

上游指出 partial product 用輸入 dtype 累加而非寬型別；輸出 dtype 沒錯，屬 accumulator 精度政策。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 partial product 用輸入 dtype 累加而非寬型別；輸出 dtype 沒錯，屬 accumulator 精度政策。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/204679)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/204679#issuecomment-6840362982)、[討論 2](https://github.com/pytorch/pytorch/issues/204679#issuecomment-6840923622)、[討論 3](https://github.com/pytorch/pytorch/issues/204679#issuecomment-6844677819)、[討論 4](https://github.com/pytorch/pytorch/issues/204679#issuecomment-6847011235)、[討論 5](https://github.com/pytorch/pytorch/issues/204679#issuecomment-6847348562)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_204679`。本案檢查的是「本 build 回傳 1632」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「Decimal 參考轉 BF16 為 2400」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/needs_review/wrong_forward_value/torch_204679/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/204679) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

研究範圍：目前機制不宜合理歸入另兩類，保留待決定。

1632 是這個 AVX512 build 的錯值，不是跨 ISA 常數；本例未測 CSR 或 float16。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_204679/`
- 新路徑：`bugs/needs_review/wrong_forward_value/torch_204679/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`dd0a13ec7a1c6ed509d4e7e4a3c6c65f83094b9e1269696e4cb1c3f58adefee9`
- metadata.json SHA-256：`16badb6dd7d0b4c7ff3fa2fa671990749270055a6d67d534f35785aaa92224ee`
- 核對時 Issue body SHA-256：`aedda51fd4da8412eb712dd25401b987ac2023ada1428081d9d00e53cab93626`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
