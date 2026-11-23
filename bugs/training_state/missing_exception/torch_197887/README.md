# PyTorch Issue #197887

上游標題：[inductor] Autograd's "modified by an inplace operation" check is lost when a view of a graph input is saved for backward: `x @ w`, `bmm`, `einsum`, 3-D `F.linear` silently return wrong gradients after `x` is modified in place

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197887) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`training_state`
- Secondary Cause：`tensor_representation`
- Primary Observation：`missing_exception`
- Secondary Observations：`wrong_gradient, incorrect_state`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.matmul` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

forward 保存 input view 後，原地修改 input 再 backward。

## 正確行為與實際行為

**Expected Behavior：** saved-variable 版本檢查應報錯。

**Actual Behavior：** 沒有例外，使用已修改資料計算梯度。

## 錯誤簽名（Bug Signature）

沒有例外，使用已修改資料計算梯度。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Inductor backward returns gradient of modified input rather than raising the version-counter error.

## 分類理由與根因證據

上游指出 reinterpret_tensor 建立獨立 version counter，破壞 saved tensor 的版本一致性。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 reinterpret_tensor 建立獨立 version counter，破壞 saved tensor 的版本一致性。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197887)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197887#issuecomment-5764747224)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_197887`。本案檢查的是「沒有例外，使用已修改資料計算梯度」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「saved-variable 版本檢查應報錯」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/training_state/missing_exception/torch_197887/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197887) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197887/`
- 新路徑：`bugs/training_state/missing_exception/torch_197887/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`7f30c4064c03243b2501f47964c8a5f222e4d8aa37bde4456894ac067c3bb3cd`
- metadata.json SHA-256：`b33611bac707ab65bcb1dc6b9d4653f93d51c23818dbb97d0b8ef331b8607b8a`
- 核對時 Issue body SHA-256：`feb2283aae0aa5cda3d4b40aacef2fce790a770fdb98c8d4424cfa7bbaa2aff1`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
