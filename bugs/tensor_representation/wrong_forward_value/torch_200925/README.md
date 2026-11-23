# PyTorch Issue #200925

上游標題：[aot_autograd] Cached synthetic-base graph uses stale storage and view offsets

[GitHub Issue](https://github.com/pytorch/pytorch/issues/200925) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`無`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`incorrect_state`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`storage_aliasing`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.compile` | 主要受測 API |

## 觸發條件

先以不同 offset 的重疊 views 暖機，再傳同 offset aliases。

## 正確行為與實際行為

**Expected Behavior：** 依第二次真實 view layout 更新完整 base 與輸出。

**Actual Behavior：** 沿用第一次 synthetic-base offset，寫錯位置。

## 錯誤簽名（Bug Signature）

沿用第一次 synthetic-base offset，寫錯位置。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> AOTAutograd synthetic base cache incorrectly reuses a prior view offset and mutation layout.

## 分類理由與根因證據

上游 synthetic-base cache guard 未完整描述 storage partition／view offset；必須保留前置呼叫。

上游內文／討論提供機制分析，未自行修補驗證：上游 synthetic-base cache guard 未完整描述 storage partition／view offset；必須保留前置呼叫。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/200925)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/200925#issuecomment-6792669813)、[討論 2](https://github.com/pytorch/pytorch/issues/200925#issuecomment-6970440897)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_issue_200925`。本案檢查的是「沿用第一次 synthetic-base offset，寫錯位置」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「依第二次真實 view layout 更新完整 base 與輸出」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_200925/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/200925) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

無待決的分類問題；不代表 testcase 已獲人工認證。

必須保留先前 alias-layout 暖機及同程序 graph reuse；不是只跑最後一次呼叫。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_200925/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_200925/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`3a8444869dc2c4fe4fb74dcb34a4eaa4328bf6f395ac10b87cb693bb099b9109`
- metadata.json SHA-256：`98449480c657cd4d0c13c87638cbb66eec671622f42a4e9e24ef81b6b2103197`
- 核對時 Issue body SHA-256：`2157c191260718e3acd0a2bd48cb6cff2e3443aa0ab89df0b109d16580f8834d`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
