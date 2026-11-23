# training_state / wrong_gradient

[總目錄](../../README.md)

## 分類定義（Category Definition）

autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。

Observation 定義：第一階／高階導數、Jacobian 或 tangent 與正確參考不符。

## 分類準則（Classification Criteria）

先滿足 `training_state` 的根因分類，再以 `wrong_gradient` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**12**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_gradient` | 12 |

## API 摘要（API Summary）

唯一 API 數：16；Issue/API 配對數：20。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.Tensor.backward` | 1 |
| `torch.acosh` | 1 |
| `torch.asinh` | 1 |
| `torch.autograd.Function` | 1 |
| `torch.autograd.forward_ad` | 1 |
| `torch.autograd.grad` | 2 |
| `torch.compile` | 4 |
| `torch.distributions.Categorical` | 1 |
| `torch.distributions.kl_divergence` | 1 |
| `torch.hypot` | 1 |
| `torch.linalg.solve` | 1 |
| `torch.nn.functional.avg_pool1d` | 1 |
| `torch.nn.functional.cosine_similarity` | 1 |
| `torch.nn.functional.layer_norm` | 1 |
| `torch.segment_reduce` | 1 |
| `torch.special.log_ndtr` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#198119](torch_198119/README.md) | `torch.nn.functional.avg_pool1d`：主要受測 API | ceil_mode=True，最後 pooling window 只有兩個有效元素時，完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]。 | 上游明確定位 avg_pool backward lowering 的 divisor，forward 正常；以 backward 規則錯誤分類。 | [原文](https://github.com/pytorch/pytorch/issues/198119) |
| [#198119](torch_198119/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | ceil_mode=True，最後 pooling window 只有兩個有效元素時，完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]。 | 上游明確定位 avg_pool backward lowering 的 divisor，forward 正常；以 backward 規則錯誤分類。 | [原文](https://github.com/pytorch/pytorch/issues/198119) |
| [#200600](torch_200600/README.md) | `torch.linalg.solve`：主要受測 API | forward-over-reverse，backward 的 create_graph=False時，一個 tangent 消失、另一個只剩一半。 | backward 因 GradMode 關閉改讀沒有 fw tangent 的 saved LU，破壞混合 AD 的狀態傳遞。 | [原文](https://github.com/pytorch/pytorch/issues/200600) |
| [#200600](torch_200600/README.md) | `torch.autograd.forward_ad`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | forward-over-reverse，backward 的 create_graph=False時，一個 tangent 消失、另一個只剩一半。 | backward 因 GradMode 關閉改讀沒有 fw tangent 的 saved LU，破壞混合 AD 的狀態傳遞。 | [原文](https://github.com/pytorch/pytorch/issues/200600) |
| [#201089](torch_201089/README.md) | `torch.compile`：主要受測 API | forward 原地增加 counter buffer，再以其算出的 scale 作用在 Linear時，forward 正確但 weight gradient 為 0.3。 | 上游指出 min-cut 保存已會被 copy_ 改寫的 buffer，backward 重新計算時讀到新值。 | [原文](https://github.com/pytorch/pytorch/issues/201089) |
| [#201633](torch_201633/README.md) | `torch.segment_reduce`：主要受測 API | max/min 有兩個相同 extrema，incoming gradient 為負時，回傳 [-1,-1,0]，正梯度控制正常。 | 上游定位 backward 分配 tied extrema 梯度時對負值處理錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/201633) |
| [#201947](torch_201947/README.md) | `torch.asinh`：主要受測 API | float16 x=1000 的 backward時，導數為零。 | 上游明確定位 backward 公式先平方 x，half 中間值溢位；歸在 backward 規則，非僅因症狀是梯度。 | [原文](https://github.com/pytorch/pytorch/issues/201947) |
| [#201947](torch_201947/README.md) | `torch.acosh`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | float16 x=1000 的 backward時，導數為零。 | 上游明確定位 backward 公式先平方 x，half 中間值溢位；歸在 backward 規則，非僅因症狀是梯度。 | [原文](https://github.com/pytorch/pytorch/issues/201947) |
| [#201970](torch_201970/README.md) | `torch.compile`：主要受測 API | 先普通 backward 編譯暖機，再相同 graph 以 retain_graph=True 重複 backward時，第二次梯度變成 8。 | 上游指出 FX cache key 沒有 donation 資訊，重用會覆寫 saved buffer 的 backward。 | [原文](https://github.com/pytorch/pytorch/issues/201970) |
| [#201970](torch_201970/README.md) | `torch.Tensor.backward`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 先普通 backward 編譯暖機，再相同 graph 以 retain_graph=True 重複 backward時，第二次梯度變成 8。 | 上游指出 FX cache key 沒有 donation 資訊，重用會覆寫 saved buffer 的 backward。 | [原文](https://github.com/pytorch/pytorch/issues/201970) |
| [#202965](torch_202965/README.md) | `torch.distributions.kl_divergence`：主要受測 API | p logits 含 -inf，對其求 KL gradient時，loss 正確但整列梯度 NaN。 | 上游定位 forward masking 未移除 multiplication backward 中的 0*(-inf)，再經 softmax backward 擴散。 | [原文](https://github.com/pytorch/pytorch/issues/202965) |
| [#202965](torch_202965/README.md) | `torch.distributions.Categorical`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | p logits 含 -inf，對其求 KL gradient時，loss 正確但整列梯度 NaN。 | 上游定位 forward masking 未移除 multiplication backward 中的 0*(-inf)，再經 softmax backward 擴散。 | [原文](https://github.com/pytorch/pytorch/issues/202965) |
| [#203946](torch_203946/README.md) | `torch.nn.functional.cosine_similarity`：主要受測 API | norm(x1)<eps<norm(x2)，float64 固定向量時，第一分量只有一半，第二分量正確。 | 上游指出 norm clamp 在 no-grad guard 下原地執行，使 autograd 圖保留應被截斷的導數項。 | [原文](https://github.com/pytorch/pytorch/issues/203946) |
| [#204478](torch_204478/README.md) | `torch.nn.functional.layer_norm`：Layer normalization under test | A parameter gradient of a loss involving second input derivatives differs from an independent formula. | Built-in layer normalization has incorrect reverse-mode third derivatives. | [原文](https://github.com/pytorch/pytorch/issues/204478) |
| [#204478](torch_204478/README.md) | `torch.autograd.grad`：Computes higher-order derivatives | A parameter gradient of a loss involving second input derivatives differs from an independent formula. | Built-in layer normalization has incorrect reverse-mode third derivatives. | [原文](https://github.com/pytorch/pytorch/issues/204478) |
| [#204825](torch_204825/README.md) | `torch.autograd.Function`：主要受測 API | compiled custom Function 的可微 backward，再求二階導數時，只剩普通路徑的 1。 | 上游定位 custom backward 以 grad mode 關閉追蹤，導致高階圖丟失 Function 貢獻。 | [原文](https://github.com/pytorch/pytorch/issues/204825) |
| [#204825](torch_204825/README.md) | `torch.autograd.grad`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | compiled custom Function 的可微 backward，再求二階導數時，只剩普通路徑的 1。 | 上游定位 custom backward 以 grad mode 關閉追蹤，導致高階圖丟失 Function 貢獻。 | [原文](https://github.com/pytorch/pytorch/issues/204825) |
| [#204825](torch_204825/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled custom Function 的可微 backward，再求二階導數時，只剩普通路徑的 1。 | 上游定位 custom backward 以 grad mode 關閉追蹤，導致高階圖丟失 Function 貢獻。 | [原文](https://github.com/pytorch/pytorch/issues/204825) |
| [#205653](torch_205653/README.md) | `torch.hypot`：主要受測 API | float64 x=3s,y=4s，incoming=1.25s，s=2**±600時，大 scale 為 inf，小 scale 為零。 | 上游引用 backward 公式 grad*other/result，中間乘積先溢位或下溢。 | [原文](https://github.com/pytorch/pytorch/issues/205653) |
| [#205654](torch_205654/README.md) | `torch.special.log_ndtr`：主要受測 API | float64 負尾 x=-2**30、-2**35時，前者為極大錯值，後者為正無限。 | 上游指出 backward 的指數式含兩個大負數相減，消去導致導數錯誤；以解析界限判定。 | [原文](https://github.com/pytorch/pytorch/issues/205654) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#201947](torch_201947/README.md)： 上游列為 #203520 數值穩定性 umbrella 的 duplicate；umbrella 不等於已證明所有 operators 共用同一修補。
- [#201970](torch_201970/README.md)： 必須保留測試內的普通 backward 暖機與 cache/donation 狀態；不可任意清空所需 cache。
