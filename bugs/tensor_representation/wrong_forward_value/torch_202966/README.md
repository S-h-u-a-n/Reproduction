# PyTorch Issue #202966

上游標題：`kl_divergence(Wishart, Wishart)` is wrong for batched distributions and has no gradient with respect to the parameters of `p`

[GitHub Issue](https://github.com/pytorch/pytorch/issues/202966) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`training_state`
- Primary Observation：`wrong_forward_value`
- Secondary Observations：`wrong_gradient`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`autograd`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.distributions.kl_divergence` | 主要受測 API |
| `torch.distributions.Wishart` | 共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 |

## 觸發條件

batched Wishart KL 且 p 的 df/covariance 要求梯度。

## 正確行為與實際行為

**Expected Behavior：** 每個 batch 符合解析 KL，p 參數有非零導數。

**Actual Behavior：** df term 錯跨 batch 加總，兩類 p 參數梯度皆 None。

## 錯誤簽名（Bug Signature）

df term 錯跨 batch 加總，兩類 p 參數梯度皆 None。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> The complete batch vector matches subtracting the df term summed across the batch instead of per item. p.df and p covariance gradients are both None despite nonzero reference derivatives. Both manifestations are tested; the policy may split their root counts. float64 rtol/atol=1e-10 for KL; finite-difference h=1e-4 is diagnostic, not a wrong-value snapshot.

## 分類理由與根因證據

上游指出 event-rank contraction 錯用到 batch 軸；另有獨立的 p natural parameters detach 問題，需決定根因拆分政策。

上游內文／討論提供機制分析，未自行修補驗證：上游指出 event-rank contraction 錯用到 batch 軸；另有獨立的 p natural parameters detach 問題，需決定根因拆分政策。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/202966)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/202966#issuecomment-6568193781)、[討論 2](https://github.com/pytorch/pytorch/issues/202966#issuecomment-6580958926)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「df term 錯跨 batch 加總，兩類 p 參數梯度皆 None」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「每個 batch 符合解析 KL，p 參數有非零導數」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_forward_value/torch_202966/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/202966) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

同一 Issue 測到 batch-axis contraction 與 p 參數梯度斷連；是否拆成兩個根因計數需決定。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_202966/`
- 新路徑：`bugs/tensor_representation/wrong_forward_value/torch_202966/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`bbe2eacc285efcf7f1cd72be1432c518bb60710385222b0cd3fcf2705105809f`
- metadata.json SHA-256：`ac9f31b0680592113178db766621ce802bbb51203610534bfa8163c578080425`
- 核對時 Issue body SHA-256：`03e1ae27f2fe36628da751b72af5f6915f3f7255bb136508d21a170a04af05d9`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
