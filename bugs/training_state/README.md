# training_state

[總目錄](../README.md)

## 分類定義（Category Definition）

autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。

## 分類準則（Classification Criteria）

Primary Cause 必須符合本類機制；觀察錯誤可以屬於不同 Observation。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**23**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_gradient` | 12 |
| `incorrect_state` | 2 |
| `wrong_metadata` | 1 |
| `unexpected_exception` | 4 |
| `missing_exception` | 4 |

## API 摘要（API Summary）

唯一 API 數：32；Issue/API 配對數：44。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.Tensor.apply_` | 1 |
| `torch.Tensor.backward` | 1 |
| `torch.Tensor.detach` | 2 |
| `torch._dynamo.compiled_autograd._enable` | 1 |
| `torch._dynamo.graph_break` | 1 |
| `torch.acosh` | 1 |
| `torch.asinh` | 1 |
| `torch.autograd.Function` | 1 |
| `torch.autograd.forward_ad` | 1 |
| `torch.autograd.grad` | 2 |
| `torch.compile` | 11 |
| `torch.distributed.checkpoint.DefaultSavePlanner` | 1 |
| `torch.distributed.checkpoint.save` | 1 |
| `torch.distributions.Categorical` | 1 |
| `torch.distributions.kl_divergence` | 1 |
| `torch.full` | 1 |
| `torch.hypot` | 1 |
| `torch.linalg.solve` | 1 |
| `torch.linalg.vander` | 1 |
| `torch.matmul` | 1 |
| `torch.nn.Parameter` | 1 |
| `torch.nn.functional.avg_pool1d` | 1 |
| `torch.nn.functional.cosine_similarity` | 1 |
| `torch.nn.functional.interpolate` | 1 |
| `torch.nn.functional.layer_norm` | 1 |
| `torch.nn.utils.clip_grad_norm_` | 1 |
| `torch.nn.utils.get_total_norm` | 1 |
| `torch.optim.Adam` | 1 |
| `torch.segment_reduce` | 1 |
| `torch.special.log_ndtr` | 1 |
| `torch.utils.checkpoint.checkpoint` | 1 |
| `torch.vander` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197092](unexpected_exception/torch_197092/README.md) | `torch.nn.functional.interpolate`：主要受測 API | compiled autograd、bilinear interpolation backward時，fake-tensor propagation 出現 isIntList INTERNAL ASSERT。 | 問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/197092) |
| [#197092](unexpected_exception/torch_197092/README.md) | `torch._dynamo.compiled_autograd._enable`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | compiled autograd、bilinear interpolation backward時，fake-tensor propagation 出現 isIntList INTERNAL ASSERT。 | 問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/197092) |
| [#197092](unexpected_exception/torch_197092/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled autograd、bilinear interpolation backward時，fake-tensor propagation 出現 isIntList INTERNAL ASSERT。 | 問題位於 backward node 的參數傳遞；上游僅提出 int-list／scalar packing 的疑似原因，未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/197092) |
| [#197887](missing_exception/torch_197887/README.md) | `torch.matmul`：主要受測 API | forward 保存 input view 後，原地修改 input 再 backward時，沒有例外，使用已修改資料計算梯度。 | 上游指出 reinterpret_tensor 建立獨立 version counter，破壞 saved tensor 的版本一致性。 | [原文](https://github.com/pytorch/pytorch/issues/197887) |
| [#197887](missing_exception/torch_197887/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | forward 保存 input view 後，原地修改 input 再 backward時，沒有例外，使用已修改資料計算梯度。 | 上游指出 reinterpret_tensor 建立獨立 version counter，破壞 saved tensor 的版本一致性。 | [原文](https://github.com/pytorch/pytorch/issues/197887) |
| [#198119](wrong_gradient/torch_198119/README.md) | `torch.nn.functional.avg_pool1d`：主要受測 API | ceil_mode=True，最後 pooling window 只有兩個有效元素時，完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]。 | 上游明確定位 avg_pool backward lowering 的 divisor，forward 正常；以 backward 規則錯誤分類。 | [原文](https://github.com/pytorch/pytorch/issues/198119) |
| [#198119](wrong_gradient/torch_198119/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | ceil_mode=True，最後 pooling window 只有兩個有效元素時，完整梯度 [1/3,1/3,2/3,1/3,2/3,1/3]。 | 上游明確定位 avg_pool backward lowering 的 divisor，forward 正常；以 backward 規則錯誤分類。 | [原文](https://github.com/pytorch/pytorch/issues/198119) |
| [#199215](unexpected_exception/torch_199215/README.md) | `torch.nn.Parameter`：主要受測 API | 整數 Parameter(requires_grad=False)，freezing 且 discard_parameters時，內層 RuntimeError 指出僅浮點 dtype 可要求梯度。 | freezing 丟棄 parameter 時建立 ErasedTensor 並無條件 requires_grad_(True)，屬 parameter lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/199215) |
| [#199215](unexpected_exception/torch_199215/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 整數 Parameter(requires_grad=False)，freezing 且 discard_parameters時，內層 RuntimeError 指出僅浮點 dtype 可要求梯度。 | freezing 丟棄 parameter 時建立 ErasedTensor 並無條件 requires_grad_(True)，屬 parameter lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/199215) |
| [#199258](unexpected_exception/torch_199258/README.md) | `torch.utils.checkpoint.checkpoint`：主要受測 API | use_reentrant=False，區域中含 x*1.0時，NetworkXError: node source not in graph。 | 上游 min-cut 分析指出 identity elimination 與 checkpoint recomputation tags 使分割圖退化。 | [原文](https://github.com/pytorch/pytorch/issues/199258) |
| [#199258](unexpected_exception/torch_199258/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | use_reentrant=False，區域中含 x*1.0時，NetworkXError: node source not in graph。 | 上游 min-cut 分析指出 identity elimination 與 checkpoint recomputation tags 使分割圖退化。 | [原文](https://github.com/pytorch/pytorch/issues/199258) |
| [#199941](unexpected_exception/torch_199941/README.md) | `torch.vander`：主要受測 API | vander 輸出求和後 backward時，saved-variable inplace-modification RuntimeError。 | 上游指出建立 Vandermonde 的 inplace slice 寫入破壞 autograd 保存版本。 | [原文](https://github.com/pytorch/pytorch/issues/199941) |
| [#199941](unexpected_exception/torch_199941/README.md) | `torch.linalg.vander`：建立正確參考的控制 API | vander 輸出求和後 backward時，saved-variable inplace-modification RuntimeError。 | 上游指出建立 Vandermonde 的 inplace slice 寫入破壞 autograd 保存版本。 | [原文](https://github.com/pytorch/pytorch/issues/199941) |
| [#200524](missing_exception/torch_200524/README.md) | `torch.full`：主要受測 API | fill value 是 requires_grad=True 的零維 tensor時，接受並建立可向 fill 反傳的 graph。 | Dynamo 將 full 重寫為 empty().fill_()，意外建立本不應存在的 autograd 連結。 | [原文](https://github.com/pytorch/pytorch/issues/200524) |
| [#200524](missing_exception/torch_200524/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | fill value 是 requires_grad=True 的零維 tensor時，接受並建立可向 fill 反傳的 graph。 | Dynamo 將 full 重寫為 empty().fill_()，意外建立本不應存在的 autograd 連結。 | [原文](https://github.com/pytorch/pytorch/issues/200524) |
| [#200600](wrong_gradient/torch_200600/README.md) | `torch.linalg.solve`：主要受測 API | forward-over-reverse，backward 的 create_graph=False時，一個 tangent 消失、另一個只剩一半。 | backward 因 GradMode 關閉改讀沒有 fw tangent 的 saved LU，破壞混合 AD 的狀態傳遞。 | [原文](https://github.com/pytorch/pytorch/issues/200600) |
| [#200600](wrong_gradient/torch_200600/README.md) | `torch.autograd.forward_ad`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | forward-over-reverse，backward 的 create_graph=False時，一個 tangent 消失、另一個只剩一半。 | backward 因 GradMode 關閉改讀沒有 fw tangent 的 saved LU，破壞混合 AD 的狀態傳遞。 | [原文](https://github.com/pytorch/pytorch/issues/200600) |
| [#201089](wrong_gradient/torch_201089/README.md) | `torch.compile`：主要受測 API | forward 原地增加 counter buffer，再以其算出的 scale 作用在 Linear時，forward 正確但 weight gradient 為 0.3。 | 上游指出 min-cut 保存已會被 copy_ 改寫的 buffer，backward 重新計算時讀到新值。 | [原文](https://github.com/pytorch/pytorch/issues/201089) |
| [#201633](wrong_gradient/torch_201633/README.md) | `torch.segment_reduce`：主要受測 API | max/min 有兩個相同 extrema，incoming gradient 為負時，回傳 [-1,-1,0]，正梯度控制正常。 | 上游定位 backward 分配 tied extrema 梯度時對負值處理錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/201633) |
| [#201947](wrong_gradient/torch_201947/README.md) | `torch.asinh`：主要受測 API | float16 x=1000 的 backward時，導數為零。 | 上游明確定位 backward 公式先平方 x，half 中間值溢位；歸在 backward 規則，非僅因症狀是梯度。 | [原文](https://github.com/pytorch/pytorch/issues/201947) |
| [#201947](wrong_gradient/torch_201947/README.md) | `torch.acosh`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | float16 x=1000 的 backward時，導數為零。 | 上游明確定位 backward 公式先平方 x，half 中間值溢位；歸在 backward 規則，非僅因症狀是梯度。 | [原文](https://github.com/pytorch/pytorch/issues/201947) |
| [#201970](wrong_gradient/torch_201970/README.md) | `torch.compile`：主要受測 API | 先普通 backward 編譯暖機，再相同 graph 以 retain_graph=True 重複 backward時，第二次梯度變成 8。 | 上游指出 FX cache key 沒有 donation 資訊，重用會覆寫 saved buffer 的 backward。 | [原文](https://github.com/pytorch/pytorch/issues/201970) |
| [#201970](wrong_gradient/torch_201970/README.md) | `torch.Tensor.backward`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 先普通 backward 編譯暖機，再相同 graph 以 retain_graph=True 重複 backward時，第二次梯度變成 8。 | 上游指出 FX cache key 沒有 donation 資訊，重用會覆寫 saved buffer 的 backward。 | [原文](https://github.com/pytorch/pytorch/issues/201970) |
| [#202806](missing_exception/torch_202806/README.md) | `torch.Tensor.detach`：主要受測 API | eager 已保存 weight，再透過 compiled detached alias 修改時，沒有版本遞增，backward 靜默使用新 weight。 | 上游明確將此歸為漏掉 version check；不存在合法的「修改後仍應得到舊梯度」契約。 | [原文](https://github.com/pytorch/pytorch/issues/202806) |
| [#202806](missing_exception/torch_202806/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | eager 已保存 weight，再透過 compiled detached alias 修改時，沒有版本遞增，backward 靜默使用新 weight。 | 上游明確將此歸為漏掉 version check；不存在合法的「修改後仍應得到舊梯度」契約。 | [原文](https://github.com/pytorch/pytorch/issues/202806) |
| [#202965](wrong_gradient/torch_202965/README.md) | `torch.distributions.kl_divergence`：主要受測 API | p logits 含 -inf，對其求 KL gradient時，loss 正確但整列梯度 NaN。 | 上游定位 forward masking 未移除 multiplication backward 中的 0*(-inf)，再經 softmax backward 擴散。 | [原文](https://github.com/pytorch/pytorch/issues/202965) |
| [#202965](wrong_gradient/torch_202965/README.md) | `torch.distributions.Categorical`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | p logits 含 -inf，對其求 KL gradient時，loss 正確但整列梯度 NaN。 | 上游定位 forward masking 未移除 multiplication backward 中的 0*(-inf)，再經 softmax backward 擴散。 | [原文](https://github.com/pytorch/pytorch/issues/202965) |
| [#203946](wrong_gradient/torch_203946/README.md) | `torch.nn.functional.cosine_similarity`：主要受測 API | norm(x1)<eps<norm(x2)，float64 固定向量時，第一分量只有一半，第二分量正確。 | 上游指出 norm clamp 在 no-grad guard 下原地執行，使 autograd 圖保留應被截斷的導數項。 | [原文](https://github.com/pytorch/pytorch/issues/203946) |
| [#204188](wrong_metadata/torch_204188/README.md) | `torch.distributed.checkpoint.save`：主要受測 API | enable_plan_caching=True，兩次 save 只有 dtype 由 bf16 變 fp16時，仍記錄 bf16，無 cache 控制組正確。 | 上游定位 class-level save plan cache 比較沒有 tensor_data.properties，屬 checkpoint state lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/204188) |
| [#204188](wrong_metadata/torch_204188/README.md) | `torch.distributed.checkpoint.DefaultSavePlanner`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | enable_plan_caching=True，兩次 save 只有 dtype 由 bf16 變 fp16時，仍記錄 bf16，無 cache 控制組正確。 | 上游定位 class-level save plan cache 比較沒有 tensor_data.properties，屬 checkpoint state lifecycle。 | [原文](https://github.com/pytorch/pytorch/issues/204188) |
| [#204269](incorrect_state/torch_204269/README.md) | `torch.nn.utils.clip_grad_norm_`：Public gradient-clipping entry point | A pair of gradient tensors with three nonzero elements returns a total 0-norm of two. | The 0-norm of gradients counts nonzero tensors instead of nonzero gradient elements. | [原文](https://github.com/pytorch/pytorch/issues/204269) |
| [#204269](incorrect_state/torch_204269/README.md) | `torch.nn.utils.get_total_norm`：Computes the total gradient norm | A pair of gradient tensors with three nonzero elements returns a total 0-norm of two. | The 0-norm of gradients counts nonzero tensors instead of nonzero gradient elements. | [原文](https://github.com/pytorch/pytorch/issues/204269) |
| [#204339](incorrect_state/torch_204339/README.md) | `torch.optim.Adam`：主要受測 API | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204339](incorrect_state/torch_204339/README.md) | `torch._dynamo.graph_break`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204339](incorrect_state/torch_204339/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | optimizer 初始化後 graph break，保留 GraphModules 再銷毀 optimizer時，optimizer 已釋放但 Parameter 被 resumed graph 保留。 | 原文指出 optimizer-owned parameter lifetime 與 resumed graph capture 有關；完整 reference-management 根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204339) |
| [#204478](wrong_gradient/torch_204478/README.md) | `torch.nn.functional.layer_norm`：Layer normalization under test | A parameter gradient of a loss involving second input derivatives differs from an independent formula. | Built-in layer normalization has incorrect reverse-mode third derivatives. | [原文](https://github.com/pytorch/pytorch/issues/204478) |
| [#204478](wrong_gradient/torch_204478/README.md) | `torch.autograd.grad`：Computes higher-order derivatives | A parameter gradient of a loss involving second input derivatives differs from an independent formula. | Built-in layer normalization has incorrect reverse-mode third derivatives. | [原文](https://github.com/pytorch/pytorch/issues/204478) |
| [#204825](wrong_gradient/torch_204825/README.md) | `torch.autograd.Function`：主要受測 API | compiled custom Function 的可微 backward，再求二階導數時，只剩普通路徑的 1。 | 上游定位 custom backward 以 grad mode 關閉追蹤，導致高階圖丟失 Function 貢獻。 | [原文](https://github.com/pytorch/pytorch/issues/204825) |
| [#204825](wrong_gradient/torch_204825/README.md) | `torch.autograd.grad`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | compiled custom Function 的可微 backward，再求二階導數時，只剩普通路徑的 1。 | 上游定位 custom backward 以 grad mode 關閉追蹤，導致高階圖丟失 Function 貢獻。 | [原文](https://github.com/pytorch/pytorch/issues/204825) |
| [#204825](wrong_gradient/torch_204825/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | compiled custom Function 的可微 backward，再求二階導數時，只剩普通路徑的 1。 | 上游定位 custom backward 以 grad mode 關閉追蹤，導致高階圖丟失 Function 貢獻。 | [原文](https://github.com/pytorch/pytorch/issues/204825) |
| [#205134](missing_exception/torch_205134/README.md) | `torch.Tensor.apply_`：主要受測 API | 保存 x 後，對 detach alias 執行 apply_ 乘十時，版本不變，backward 靜默回傳 [20,40]。 | 上游確認 apply_ 原地寫入沒有 bump version；[2,4] 不可當作已修改情境的合法答案。 | [原文](https://github.com/pytorch/pytorch/issues/205134) |
| [#205134](missing_exception/torch_205134/README.md) | `torch.Tensor.detach`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 保存 x 後，對 detach alias 執行 apply_ 乘十時，版本不變，backward 靜默回傳 [20,40]。 | 上游確認 apply_ 原地寫入沒有 bump version；[2,4] 不可當作已修改情境的合法答案。 | [原文](https://github.com/pytorch/pytorch/issues/205134) |
| [#205653](wrong_gradient/torch_205653/README.md) | `torch.hypot`：主要受測 API | float64 x=3s,y=4s，incoming=1.25s，s=2**±600時，大 scale 為 inf，小 scale 為零。 | 上游引用 backward 公式 grad*other/result，中間乘積先溢位或下溢。 | [原文](https://github.com/pytorch/pytorch/issues/205653) |
| [#205654](wrong_gradient/torch_205654/README.md) | `torch.special.log_ndtr`：主要受測 API | float64 負尾 x=-2**30、-2**35時，前者為極大錯值，後者為正無限。 | 上游指出 backward 的指數式含兩個大負數相減，消去導致導數錯誤；以解析界限判定。 | [原文](https://github.com/pytorch/pytorch/issues/205654) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197092](unexpected_exception/torch_197092/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#201947](wrong_gradient/torch_201947/README.md)： 上游列為 #203520 數值穩定性 umbrella 的 duplicate；umbrella 不等於已證明所有 operators 共用同一修補。
- [#201970](wrong_gradient/torch_201970/README.md)： 必須保留測試內的普通 backward 暖機與 cache/donation 狀態；不可任意清空所需 cache。
- [#204188](wrong_metadata/torch_204188/README.md)： 兩次保存與 planner class cache 的順序是觸發條件；完整批次驗證仍保留測試原有清理邏輯。
- [#204339](incorrect_state/torch_204339/README.md)：根因證據尚不足；分類依已知必要觸發條件。 使用內部 optimizer API、GC 控制與弱引用；只驗證 parameter lifetime，沒有聲稱 optimizer 數值更新錯誤。
- [#205134](missing_exception/torch_205134/README.md)： 未修改控制的 [2,4] 不能作為修改後的正確梯度；正確契約是版本衝突例外。本例只測 apply_，未測 Issue 的 map_ 變體。
