# PyTorch Issue #199920

上游標題：Fake/meta impl of `_fused_moving_avg_obs_fq_helper` ignores per-channel buffer resize, breaking AOTAutograd

[GitHub Issue](https://github.com/pytorch/pytorch/issues/199920) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`training_state`
- Primary Observation：`wrong_metadata`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`tensor_metadata`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.ops.aten._fused_moving_avg_obs_fq_helper_functional` | 主要受測 API |
| `torch._subclasses.fake_tensor.FakeTensorMode` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

per-channel fake quant observer 首次使用，八個 channel。

## 正確行為與實際行為

**Expected Behavior：** fake state shape 與真實 kernel 一樣更新為八。

**Actual Behavior：** min/max 仍為零長、scale/zero-point 仍為一。

## 錯誤簽名（Bug Signature）

min/max 仍為零長、scale/zero-point 仍為一。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> The meta implementation leaves min/max buffers at size 0 and scale/zero-point at size 1 rather than 8.

## 分類理由與根因證據

上游 meta function 未模擬 observer buffer resize；主要是 tensor metadata，次要涉及訓練 buffer。

上游內文／討論提供機制分析，未自行修補驗證：上游 meta function 未模擬 observer buffer resize；主要是 tensor metadata，次要涉及訓練 buffer。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/199920)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/199920#issuecomment-6025329382)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「min/max 仍為零長、scale/zero-point 仍為一」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「fake state shape 與真實 kernel 一樣更新為八」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_metadata/torch_199920/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/199920) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_199920/`
- 新路徑：`bugs/tensor_representation/wrong_metadata/torch_199920/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`c9565ebec120b2609c4a187d5972eb684340d4d81258e06afce8c17387e6581b`
- metadata.json SHA-256：`e45e114816669c8d7cf648f6035a6390211d4d915489fe4353e737d69bb79fdc`
- 核對時 Issue body SHA-256：`b937083d4ba8e1355a4061d302ee268b0689eebe2745c02071f756cafaf64a58`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
