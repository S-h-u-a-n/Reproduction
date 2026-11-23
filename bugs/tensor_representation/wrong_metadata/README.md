# tensor_representation / wrong_metadata

[總目錄](../../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

Observation 定義：shape、dtype、rank、tangent 表示或 checkpoint tensor metadata 錯誤。

## 分類準則（Classification Criteria）

先滿足 `tensor_representation` 的根因分類，再以 `wrong_metadata` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**8**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_metadata` | 8 |

## API 摘要（API Summary）

唯一 API 數：11；Issue/API 配對數：17。

| API | 涉及 Issue 數 |
| --- | ---: |
| `numpy.cumsum` | 1 |
| `torch._subclasses.fake_tensor.FakeTensorMode` | 1 |
| `torch._subclasses.functional_tensor.dispatch_functionalize` | 1 |
| `torch.all` | 1 |
| `torch.any` | 2 |
| `torch.autograd.forward_ad.unpack_dual` | 1 |
| `torch.cat` | 1 |
| `torch.compile` | 6 |
| `torch.nn.functional.soft_margin_loss` | 1 |
| `torch.ops.aten._fused_moving_avg_obs_fq_helper_functional` | 1 |
| `torch.scatter` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#192639](torch_192639/README.md) | `torch.autograd.forward_ad.unpack_dual`：主要受測 API | dual tensor 經 dispatch_functionalize 包裝時，tangent 變成 None。 | Issue 指出 wrapper 的 _fw_grad 讀取沒有轉向底層 dual tensor；主要是 tensor 包裝表示遺失。 | [原文](https://github.com/pytorch/pytorch/issues/192639) |
| [#192639](torch_192639/README.md) | `torch._subclasses.functional_tensor.dispatch_functionalize`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | dual tensor 經 dispatch_functionalize 包裝時，tangent 變成 None。 | Issue 指出 wrapper 的 _fw_grad 讀取沒有轉向底層 dual tensor；主要是 tensor 包裝表示遺失。 | [原文](https://github.com/pytorch/pytorch/issues/192639) |
| [#198056](torch_198056/README.md) | `numpy.cumsum`：主要受測 API | 編譯 int8 NumPy 累加時，維持 int8 dtype 並發生 wraparound。 | NumPy 到 tensor 的 dtype promotion 表示未保存。 | [原文](https://github.com/pytorch/pytorch/issues/198056) |
| [#198056](torch_198056/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 編譯 int8 NumPy 累加時，維持 int8 dtype 並發生 wraparound。 | NumPy 到 tensor 的 dtype promotion 表示未保存。 | [原文](https://github.com/pytorch/pytorch/issues/198056) |
| [#198081](torch_198081/README.md) | `torch.any`：主要受測 API | uint8 reduction 後再做整數算術時，變成 bool，後續計算變為 int64 的 300。 | reduction 把輸入轉 bool 後沒有回復 uint8 輸出表示。 | [原文](https://github.com/pytorch/pytorch/issues/198081) |
| [#198081](torch_198081/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | uint8 reduction 後再做整數算術時，變成 bool，後續計算變為 int64 的 300。 | reduction 把輸入轉 bool 後沒有回復 uint8 輸出表示。 | [原文](https://github.com/pytorch/pytorch/issues/198081) |
| [#198851](torch_198851/README.md) | `torch.any`：主要受測 API | reduction 指定 dim=()時，編譯後回傳 scalar。 | 空維度 tuple 在 reduction shape 語意上不一致；原文沒有確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198851) |
| [#198851](torch_198851/README.md) | `torch.all`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | reduction 指定 dim=()時，編譯後回傳 scalar。 | 空維度 tuple 在 reduction shape 語意上不一致；原文沒有確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198851) |
| [#198851](torch_198851/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | reduction 指定 dim=()時，編譯後回傳 scalar。 | 空維度 tuple 在 reduction shape 語意上不一致；原文沒有確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198851) |
| [#198852](torch_198852/README.md) | `torch.cat`：主要受測 API | 空 float64 tensor 與多個非空 float32 tensor 串接時，輸出 float32。 | 上游指出 cat decomposition 移除空 tensor 後重算 dtype，遺失 promotion 資訊。 | [原文](https://github.com/pytorch/pytorch/issues/198852) |
| [#198852](torch_198852/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 空 float64 tensor 與多個非空 float32 tensor 串接時，輸出 float32。 | 上游指出 cat decomposition 移除空 tensor 後重算 dtype，遺失 promotion 資訊。 | [原文](https://github.com/pytorch/pytorch/issues/198852) |
| [#198868](torch_198868/README.md) | `torch.scatter`：主要受測 API | scalar input 與 empty index時，shape 變成 (1,)。 | scalar／空 index 的 tensor rank 表示不一致；上游未確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198868) |
| [#198868](torch_198868/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | scalar input 與 empty index時，shape 變成 (1,)。 | scalar／空 index 的 tensor rank 表示不一致；上游未確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198868) |
| [#198994](torch_198994/README.md) | `torch.nn.functional.soft_margin_loss`：主要受測 API | input float32、target float64時，Inductor 回傳 float64。 | 上游修補討論指出 opmath promotion 後應 cast 回 input dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198994) |
| [#198994](torch_198994/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | input float32、target float64時，Inductor 回傳 float64。 | 上游修補討論指出 opmath promotion 後應 cast 回 input dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198994) |
| [#199920](torch_199920/README.md) | `torch.ops.aten._fused_moving_avg_obs_fq_helper_functional`：主要受測 API | per-channel fake quant observer 首次使用，八個 channel時，min/max 仍為零長、scale/zero-point 仍為一。 | 上游 meta function 未模擬 observer buffer resize；主要是 tensor metadata，次要涉及訓練 buffer。 | [原文](https://github.com/pytorch/pytorch/issues/199920) |
| [#199920](torch_199920/README.md) | `torch._subclasses.fake_tensor.FakeTensorMode`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | per-channel fake quant observer 首次使用，八個 channel時，min/max 仍為零長、scale/zero-point 仍為一。 | 上游 meta function 未模擬 observer buffer resize；主要是 tensor metadata，次要涉及訓練 buffer。 | [原文](https://github.com/pytorch/pytorch/issues/199920) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#198056](torch_198056/README.md)： Issue 包含多種 dtype/shape 症狀；本地只測 int8 cumsum。
- [#198851](torch_198851/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#198868](torch_198868/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
