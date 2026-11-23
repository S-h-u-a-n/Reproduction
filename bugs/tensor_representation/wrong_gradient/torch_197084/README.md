# PyTorch Issue #197084

上游標題：[aot_autograd] wrong gradients for `torch.linalg.pinv` and `torch.linalg.matrix_sqrth` with complex input under torch.compile (aot_eager and inductor); eager, functorch and Dynamo-only are correct

[GitHub Issue](https://github.com/pytorch/pytorch/issues/197084) · [分類目錄](../README.md) · [總目錄](../../../README.md)

## 分類與主要 API

- Primary Cause：`tensor_representation`
- Secondary Cause：`training_state`
- Primary Observation：`wrong_gradient`
- Secondary Observations：`無`
- Classification Confidence：`high`（只指分類）
- 原始 metadata 分類：`autograd`；保留原文，不覆寫。

| API | 在本案的作用 |
| --- | --- |
| `torch.linalg.pinv` | 主要受測 API |
| `torch.compile` | 觸發編譯／快取路徑的必要入口 |

## 觸發條件

固定 full-column-rank complex64 矩陣、編譯後反向。

## 正確行為與實際行為

**Expected Behavior：** 梯度等於 -2*A@(A.H@A)^-2，並吻合 eager 高精度控制。

**Actual Behavior：** 完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP。

## 錯誤簽名（Bug Signature）

完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP。以下為既有 [metadata.json](metadata.json) 中的精確簽名，原文僅作詳細數值與容差補充，沒有改寫檔案：

> The compiled complex64 gradient matches the pinv VJP fed with the saved wrong SVD result (Vh.T/s)@U.H. Source: issue Sep 22 correction and target-build FunctionsManual.cpp pinv_backward; linked root #198118. Full tensor tolerance rtol=1e-5, atol=1e-6 allows small well-conditioned complex64 SVD/matmul roundoff. matrix_sqrth is outside this testcase.

## 分類理由與根因證據

Issue 後續更正將原因連至 #198118 的 conjugate view 遺失，不能僅因 gradient 錯誤歸為訓練狀態。

上游內文／討論提供機制分析，未自行修補驗證：Issue 後續更正將原因連至 #198118 的 conjugate view 遺失，不能僅因 gradient 錯誤歸為訓練狀態。

來源：[Issue 內文與討論](https://github.com/pytorch/pytorch/issues/197084)；2026-11-23 已讀 Issue 內文及頁面載入的討論（不代表所有分頁討論）。上游分析與本機的錯誤簽名驗證分開，不將推測視為確定根因。

可見討論定位：[討論 1](https://github.com/pytorch/pytorch/issues/197084#issuecomment-5770677350)。

## Reproducer 說明

[test_bug.py](test_bug.py) 保留原本操作、斷言、輸入、控制組與必要呼叫歷史。入口為 `test_known_bug_signature`。本案檢查的是「完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP」，PASS 表示已知錯誤仍存在，不是一般正確性測試。正確參考及預期為「梯度等於 -2*A@(A.H@A)^-2，並吻合 eager 高精度控制」。

從專案根目錄單案執行：

```bash
.venv/bin/python -m pytest -q -p no:cacheprovider --import-mode=importlib bugs/tensor_representation/wrong_gradient/torch_197084/test_bug.py
```

## 版本與驗證證據

- 本次實測：PyTorch `2.15.0+cpu`，git `d0f2af8b66b20da4baa50644c0cd3f887a2eae2e`。
- Python `3.14.10`、pytest `9.0.1`、`Linux-7.3.5-arch1-1-x86_64-with-glibc2.44`、CPU `AVX512`。
- 原 metadata 環境：`{"torch": "2.15.0+cpu", "python": "3.14.10", "platform": "linux_x86_64", "device": "cpu"}`。
- 原 metadata 紀錄：runs=10、passes=10、review=pending。這是繼承的紀錄，本次未重新完成十次獨立執行。
- 搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。
- 上游其他版本僅為 [Issue](https://github.com/pytorch/pytorch/issues/197084) 的報告，本次未重測；第一個修復版本：`unknown`。

## 限制與待確認事項

上游將此梯度症狀連結至 #198118；Issue 保留兩筆，獨立根因不應直接計為兩個。

只涵蓋目前 test_bug.py 的固定變體；不把 Issue 內所有 API、裝置或 dtype 變體視為已驗證。

本次是分類與搬移相容性工作，未修改或重新認證每個斷言；沒有完成 Mirage 接入。

## 原始資料保存與搬移追蹤

- 原路徑：`bugs/torch_197084/`
- 新路徑：`bugs/tensor_representation/wrong_gradient/torch_197084/`
- 原始必要檔案連同既有附屬檔案整個搬移，沒有複製成第二份 Case。
- test_bug.py SHA-256：`ec044614f45a3f01348732ddd46b90269af2e08fcfdfce7fea61dc4f283a1f1b`
- metadata.json SHA-256：`0f3f08a8dc2b26e2959cc6e00923401266d01cf8828901477b253d73f95d05f1`
- 核對時 Issue body SHA-256：`e4511fc4756a2ff54df3b807bcbbc0537b8e9edefad75fd84a90c164314a01b7`（指取得的 Markdown 內文，不是整個 HTML）。
- 完整備份、還原程序及批次驗證見[總目錄](../../../README.md)。
