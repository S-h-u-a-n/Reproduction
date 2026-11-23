# PyTorch Issue #201268

上游標題：CSR `add(out=)` writes wrong values when `out`'s `values()` is non-contiguous

[GitHub Issue](https://github.com/pytorch/pytorch/issues/201268) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`incorrect_state`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_layout`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.add` | 主要受測 API |
| `torch.sparse_csr_tensor` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

CSR out.values() 為合法 stride=2 view。

## 正確行為與實際行為

**Expected Behavior：** values 為 [11,22]，間隙不被修改。

**Actual Behavior：** values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element。

## 錯誤簽名（Bug Signature）

values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> MKL CSR add(out=) writes contiguous storage positions rather than logical values() stride.

## 分類理由與根因證據

上游定位 mkl_result_copy_ 線性複製 nnz，忽略 destination values stride。

上游內文／討論提供機制分析，未自行修補驗證：上游定位 mkl_result_copy_ 線性複製 nnz，忽略 destination values stride。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/201268)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/201268#issuecomment-6429181294)、[討論 2](https://github.com/pytorch/pytorch/issues/201268#issuecomment-6588949474)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_201268`。本案檢查的是「values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「values 為 [11,22]，間隙不被修改」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_201268/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/201268) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

本地固定 nnz 的 backing storage 錯寫不等於已驗證 allocation 外 memory corruption。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_201268/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_201268/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`bb537579764a333886d2621a82c7e3e4286a26e521798603e21bbf84f5964678`
- metadata.json SHA-256：`44c77d7331d4ce2209bd8e14aa62d10ca0cafbf4fd6c85f81dfdef2407dd2107`
- 核對時 Issue body SHA-256：`00c2a497bcdb8efd646e9f70f303da9dcdd1dec90d8acd1df6b15917dc508479`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
