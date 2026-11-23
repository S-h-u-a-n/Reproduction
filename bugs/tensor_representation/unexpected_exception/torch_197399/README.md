# PyTorch Issue #197399

上游標題：`torch.compile` (inductor) raises `IndexError` at trace time on a valid `Tensor.set_` storage rebind — eager works

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197399) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`unexpected_exception`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`storage_aliasing`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.Tensor.set_` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

把空 tensor 的 storage 重綁成長度一後讀 x[0]。

## 正確行為與實際行為

**Expected Behavior：** size metadata 隨重綁更新，合法讀取成功。

**Actual Behavior：** 仍以舊空 shape 追蹤並拋 IndexError。

## 錯誤簽名（Bug Signature）

仍以舊空 shape 追蹤並拋 IndexError。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> Fake-tensor tracing fails to update the rebound size and raises IndexError when reading x[0].

## 分類理由與根因證據

上游指出 functional tensor 內層已更新，但 wrapper TensorImpl metadata 未同步。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 functional tensor 內層已更新，但 wrapper TensorImpl metadata 未同步。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197399)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197399#issuecomment-5760673971)、[討論 2](https://github.com/pytorch/pytorch/issues/197399#issuecomment-6985198382)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「仍以舊空 shape 追蹤並拋 IndexError」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「size metadata 隨重綁更新，合法讀取成功」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/unexpected_exception/torch_197399/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197399) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197399/`
- 新路徑：`bugs/tensor_representation/unexpected_exception/torch_197399/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`1a0da4d1bdc45c33476ae220581f8652c1fd9af3d31137a1d828efae7123e81d`
- metadata.json SHA-256：`c17ef8fe3f6e6c4eee7dd9f6991e1913505b36d4605393d40f19c06dac460450`
- 核對時 Issue body SHA-256：`5825d37cfe980a959bed443b99a72c292e686afe16028e7f552a338d7ef60f42`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
