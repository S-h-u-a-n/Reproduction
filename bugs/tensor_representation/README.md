# tensor_representation

[總目錄](../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

## 分類準則（Classification Criteria）

Primary Cause 必須符合本類機制；觀察錯誤可以屬於不同 Observation。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**58**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `wrong_gradient` | 8 |
| `wrong_forward_value` | 22 |
| `wrong_optimizer_update` | 1 |
| `incorrect_state` | 4 |
| `wrong_metadata` | 8 |
| `unexpected_exception` | 13 |
| `missing_exception` | 2 |

## API 摘要（API Summary）

唯一 API 數：75；Issue/API 配對數：117。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.compile` | 35 |
| `torch.cat` | 3 |
| `torch.Tensor.set_` | 2 |
| `torch.add` | 2 |
| `torch.any` | 2 |
| `torch.linalg.lu_solve` | 2 |
| `torch.linalg.pinv` | 2 |
| `torch.softmax` | 2 |
| `DTensor.from_local` | 1 |
| `numpy.cumsum` | 1 |
| `torch.SymInt.__round__` | 1 |
| `torch.Tensor.__torch_function__` | 1 |
| `torch.Tensor.add_` | 1 |
| `torch.Tensor.as_strided_` | 1 |
| `torch.Tensor.conj` | 1 |
| `torch.Tensor.detach` | 1 |
| `torch.Tensor.div` | 1 |
| `torch.Tensor.fill_diagonal_` | 1 |
| `torch.Tensor.imag` | 1 |
| `torch.Tensor.index_add` | 1 |
| `torch.Tensor.index_put_` | 1 |
| `torch.Tensor.item` | 1 |
| `torch.Tensor.real` | 1 |
| `torch.Tensor.scatter_add` | 1 |
| `torch.Tensor.scatter_reduce` | 1 |
| `torch.Tensor.split` | 1 |
| `torch.Tensor.trunc_` | 1 |
| `torch.Tensor.unfold` | 1 |
| `torch.Tensor.unsqueeze` | 1 |
| `torch.Tensor.view` | 1 |
| `torch._foreach_copy_` | 1 |
| `torch._subclasses.fake_tensor.FakeTensorMode` | 1 |
| `torch._subclasses.functional_tensor.dispatch_functionalize` | 1 |
| `torch.all` | 1 |
| `torch.amax` | 1 |
| `torch.autograd.Function` | 1 |
| `torch.autograd.forward_ad.unpack_dual` | 1 |
| `torch.cdist` | 1 |
| `torch.clamp` | 1 |
| `torch.compiler.nested_compile_region` | 1 |
| `torch.dequantize` | 1 |
| `torch.distributions.Wishart` | 1 |
| `torch.distributions.kl_divergence` | 1 |
| `torch.div` | 1 |
| `torch.eq` | 1 |
| `torch.func.jacrev` | 1 |
| `torch.imag` | 1 |
| `torch.isin` | 1 |
| `torch.linalg.slogdet` | 1 |
| `torch.linalg.solve` | 1 |
| `torch.linalg.solve_triangular` | 1 |
| `torch.linalg.vector_norm` | 1 |
| `torch.nn.Conv2d` | 1 |
| `torch.nn.functional.adaptive_max_pool2d` | 1 |
| `torch.nn.functional.adaptive_max_pool3d` | 1 |
| `torch.nn.functional.grouped_mm` | 1 |
| `torch.nn.functional.linear` | 1 |
| `torch.nn.functional.soft_margin_loss` | 1 |
| `torch.no_grad` | 1 |
| `torch.ops.aten._fused_moving_avg_obs_fq_helper_functional` | 1 |
| `torch.ops.aten.adaptive_max_pool3d_backward` | 1 |
| `torch.ops.aten.unsqueeze_.default` | 1 |
| `torch.optim.SGD` | 1 |
| `torch.save` | 1 |
| `torch.scatter` | 1 |
| `torch.slice_scatter` | 1 |
| `torch.sparse_coo_tensor` | 1 |
| `torch.sparse_csr_tensor` | 1 |
| `torch.utils._python_dispatch.TorchDispatchMode` | 1 |
| `torch.view_as_complex_copy` | 1 |
| `torch.Tensor.copy_` | 1 |
| `torch.Tensor.expand` | 1 |
| `torch.Tensor.fill_` | 1 |
| `torch.cond` | 1 |
| `torch.cummax(out=...)` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#192639](wrong_metadata/torch_192639/README.md) | `torch.autograd.forward_ad.unpack_dual`：主要受測 API | dual tensor 經 dispatch_functionalize 包裝時，tangent 變成 None。 | Issue 指出 wrapper 的 _fw_grad 讀取沒有轉向底層 dual tensor；主要是 tensor 包裝表示遺失。 | [原文](https://github.com/pytorch/pytorch/issues/192639) |
| [#192639](wrong_metadata/torch_192639/README.md) | `torch._subclasses.functional_tensor.dispatch_functionalize`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | dual tensor 經 dispatch_functionalize 包裝時，tangent 變成 None。 | Issue 指出 wrapper 的 _fw_grad 讀取沒有轉向底層 dual tensor；主要是 tensor 包裝表示遺失。 | [原文](https://github.com/pytorch/pytorch/issues/192639) |
| [#195451](incorrect_state/torch_195451/README.md) | `torch.slice_scatter`：主要受測 API | functional scatter、輸入 mutation 與回傳結果時，回傳結果 alias 輸入，修改結果連帶改變輸入。 | 上游 reinplace／copy-back 分析指出 fresh output 被當成 input alias。 | [原文](https://github.com/pytorch/pytorch/issues/195451) |
| [#195451](incorrect_state/torch_195451/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | functional scatter、輸入 mutation 與回傳結果時，回傳結果 alias 輸入，修改結果連帶改變輸入。 | 上游 reinplace／copy-back 分析指出 fresh output 被當成 input alias。 | [原文](https://github.com/pytorch/pytorch/issues/195451) |
| [#197084](wrong_gradient/torch_197084/README.md) | `torch.linalg.pinv`：主要受測 API | 固定 full-column-rank complex64 矩陣、編譯後反向時，完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP。 | Issue 後續更正將原因連至 #198118 的 conjugate view 遺失，不能僅因 gradient 錯誤歸為訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/197084) |
| [#197084](wrong_gradient/torch_197084/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 固定 full-column-rank complex64 矩陣、編譯後反向時，完整梯度符合缺少 conjugation 的 SVD 結果所導出的錯誤 VJP。 | Issue 後續更正將原因連至 #198118 的 conjugate view 遺失，不能僅因 gradient 錯誤歸為訓練狀態。 | [原文](https://github.com/pytorch/pytorch/issues/197084) |
| [#197097](unexpected_exception/torch_197097/README.md) | `torch.linalg.vector_norm`：主要受測 API | shape=(0,5)、ord=inf、dim=-1時，錯判 reduction 維度為空並拋例外。 | 上游指出負維度未正規化，導致空 batch 與 reduction 維度混淆。 | [原文](https://github.com/pytorch/pytorch/issues/197097) |
| [#197097](unexpected_exception/torch_197097/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | shape=(0,5)、ord=inf、dim=-1時，錯判 reduction 維度為空並拋例外。 | 上游指出負維度未正規化，導致空 batch 與 reduction 維度混淆。 | [原文](https://github.com/pytorch/pytorch/issues/197097) |
| [#197399](unexpected_exception/torch_197399/README.md) | `torch.Tensor.set_`：主要受測 API | 把空 tensor 的 storage 重綁成長度一後讀 x[0]時，仍以舊空 shape 追蹤並拋 IndexError。 | 上游指出 functional tensor 內層已更新，但 wrapper TensorImpl metadata 未同步。 | [原文](https://github.com/pytorch/pytorch/issues/197399) |
| [#197399](unexpected_exception/torch_197399/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 把空 tensor 的 storage 重綁成長度一後讀 x[0]時，仍以舊空 shape 追蹤並拋 IndexError。 | 上游指出 functional tensor 內層已更新，但 wrapper TensorImpl metadata 未同步。 | [原文](https://github.com/pytorch/pytorch/issues/197399) |
| [#197448](wrong_forward_value/torch_197448/README.md) | `torch.Tensor.expand`：主要受測 API | 以 Inductor 編譯後，對 expand 視圖執行 fill_ 的 base 值為 [8, 7, 6, 5]，eager 為 [2, 2, 2, 2]。 | 本地測試對照同一 base 的 eager 與 Inductor 結果，分類依展開視圖的原地寫入。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/197448) |
| [#197448](wrong_forward_value/torch_197448/README.md) | `torch.Tensor.fill_`：共同觸發的原地寫入操作 | 以 Inductor 編譯後，對 expand 視圖執行 fill_ 的 base 值為 [8, 7, 6, 5]，eager 為 [2, 2, 2, 2]。 | 本地測試對照同一 base 的 eager 與 Inductor 結果，分類依展開視圖的原地寫入。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/197448) |
| [#197448](wrong_forward_value/torch_197448/README.md) | `torch.compile`：觸發編譯路徑的入口 | 以 Inductor 編譯後，對 expand 視圖執行 fill_ 的 base 值為 [8, 7, 6, 5]，eager 為 [2, 2, 2, 2]。 | 本地測試對照同一 base 的 eager 與 Inductor 結果，分類依展開視圖的原地寫入。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/197448) |
| [#197888](wrong_gradient/torch_197888/README.md) | `torch.ops.aten.adaptive_max_pool3d_backward`：CPU backward kernel | CPU adaptive max pool backward scatters gradients to the wrong input elements when it reads channels_last_3d indices in storage order. | The CPU backward kernel ignores the strides of noncontiguous channels_last_3d indices. | [原文](https://github.com/pytorch/pytorch/issues/197888) |
| [#197888](wrong_gradient/torch_197888/README.md) | `torch.nn.functional.adaptive_max_pool3d`：Produces pooling indices | CPU adaptive max pool backward scatters gradients to the wrong input elements when it reads channels_last_3d indices in storage order. | The CPU backward kernel ignores the strides of noncontiguous channels_last_3d indices. | [原文](https://github.com/pytorch/pytorch/issues/197888) |
| [#197893](incorrect_state/torch_197893/README.md) | `torch.Tensor.div`：主要受測 API | 編譯 x/1 後修改回傳 tensor時，結果與 input 共用 storage，修改相互影響。 | remove_no_ops 把圖輸出替換為 input，改變 alias 契約。 | [原文](https://github.com/pytorch/pytorch/issues/197893) |
| [#197893](incorrect_state/torch_197893/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 編譯 x/1 後修改回傳 tensor時，結果與 input 共用 storage，修改相互影響。 | remove_no_ops 把圖輸出替換為 input，改變 alias 契約。 | [原文](https://github.com/pytorch/pytorch/issues/197893) |
| [#198056](wrong_metadata/torch_198056/README.md) | `numpy.cumsum`：主要受測 API | 編譯 int8 NumPy 累加時，維持 int8 dtype 並發生 wraparound。 | NumPy 到 tensor 的 dtype promotion 表示未保存。 | [原文](https://github.com/pytorch/pytorch/issues/198056) |
| [#198056](wrong_metadata/torch_198056/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 編譯 int8 NumPy 累加時，維持 int8 dtype 並發生 wraparound。 | NumPy 到 tensor 的 dtype promotion 表示未保存。 | [原文](https://github.com/pytorch/pytorch/issues/198056) |
| [#198064](wrong_forward_value/torch_198064/README.md) | `torch.SymInt.__round__`：主要受測 API | dynamic shape 長度使用 round(n,-1)時，忽略負 ndigits，使用原 n。 | Issue 指出 symbolic size 的 SymInt.__round__ 表示遺失 ndigits，與具體整數語意不同。 | [原文](https://github.com/pytorch/pytorch/issues/198064) |
| [#198064](wrong_forward_value/torch_198064/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | dynamic shape 長度使用 round(n,-1)時，忽略負 ndigits，使用原 n。 | Issue 指出 symbolic size 的 SymInt.__round__ 表示遺失 ndigits，與具體整數語意不同。 | [原文](https://github.com/pytorch/pytorch/issues/198064) |
| [#198071](wrong_forward_value/torch_198071/README.md) | `torch.clamp`：主要受測 API | int8 輸入與超出範圍的 Python max=300時，bound 轉成 int8 的 44，127 被截到 44。 | 上游指出 scalar bound 過早縮窄到 tensor dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198071) |
| [#198071](wrong_forward_value/torch_198071/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | int8 輸入與超出範圍的 Python max=300時，bound 轉成 int8 的 44，127 被截到 44。 | 上游指出 scalar bound 過早縮窄到 tensor dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198071) |
| [#198081](wrong_metadata/torch_198081/README.md) | `torch.any`：主要受測 API | uint8 reduction 後再做整數算術時，變成 bool，後續計算變為 int64 的 300。 | reduction 把輸入轉 bool 後沒有回復 uint8 輸出表示。 | [原文](https://github.com/pytorch/pytorch/issues/198081) |
| [#198081](wrong_metadata/torch_198081/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | uint8 reduction 後再做整數算術時，變成 bool，後續計算變為 int64 的 300。 | reduction 把輸入轉 bool 後沒有回復 uint8 輸出表示。 | [原文](https://github.com/pytorch/pytorch/issues/198081) |
| [#198095](wrong_forward_value/torch_198095/README.md) | `torch.compile`：主要受測 API | 共享 storage 的 base 與切片輸入，修改 base 後回傳切片的 view時，錯誤回傳 t0 第一列。 | 上游指出 synthetic base 重映射 base_idx 後仍使用舊 view metadata。 | [原文](https://github.com/pytorch/pytorch/issues/198095) |
| [#198102](wrong_forward_value/torch_198102/README.md) | `torch.Tensor.unfold`：主要受測 API | 不重疊 unfold view 的寫入，base 中間有未覆蓋位置時，未覆蓋的位置被歸零。 | functionalization 的 unfold inverse 使用 backward scatter 的歸零邏輯，破壞 view 寫回。 | [原文](https://github.com/pytorch/pytorch/issues/198102) |
| [#198102](wrong_forward_value/torch_198102/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 不重疊 unfold view 的寫入，base 中間有未覆蓋位置時，未覆蓋的位置被歸零。 | functionalization 的 unfold inverse 使用 backward scatter 的歸零邏輯，破壞 view 寫回。 | [原文](https://github.com/pytorch/pytorch/issues/198102) |
| [#198118](wrong_forward_value/torch_198118/README.md) | `torch.linalg.pinv`：主要受測 API | complex128 pinv 經 pass-through TorchDispatchMode時，符合缺少 conjugation 的完整 SVD 公式。 | 上游指出內部 lazy conjugate view 在 Python dispatch 路徑未正確物化；與 #197084 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198118) |
| [#198118](wrong_forward_value/torch_198118/README.md) | `torch.utils._python_dispatch.TorchDispatchMode`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | complex128 pinv 經 pass-through TorchDispatchMode時，符合缺少 conjugation 的完整 SVD 公式。 | 上游指出內部 lazy conjugate view 在 Python dispatch 路徑未正確物化；與 #197084 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198118) |
| [#198155](missing_exception/torch_198155/README.md) | `torch.softmax`：主要受測 API | int64 輸入的 softmax 經 Inductor時，回傳整數 tensor 而不報錯。 | operator dtype 支援契約在 lowering 被放寬；僅收錄原 Issue 眾多組合中的 int64 softmax。 | [原文](https://github.com/pytorch/pytorch/issues/198155) |
| [#198155](missing_exception/torch_198155/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | int64 輸入的 softmax 經 Inductor時，回傳整數 tensor 而不報錯。 | operator dtype 支援契約在 lowering 被放寬；僅收錄原 Issue 眾多組合中的 int64 softmax。 | [原文](https://github.com/pytorch/pytorch/issues/198155) |
| [#198669](unexpected_exception/torch_198669/README.md) | `torch.softmax`：主要受測 API | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#198669](unexpected_exception/torch_198669/README.md) | `torch.eq`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#198669](unexpected_exception/torch_198669/README.md) | `torch.div`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#198669](unexpected_exception/torch_198669/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#198851](wrong_metadata/torch_198851/README.md) | `torch.any`：主要受測 API | reduction 指定 dim=()時，編譯後回傳 scalar。 | 空維度 tuple 在 reduction shape 語意上不一致；原文沒有確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198851) |
| [#198851](wrong_metadata/torch_198851/README.md) | `torch.all`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | reduction 指定 dim=()時，編譯後回傳 scalar。 | 空維度 tuple 在 reduction shape 語意上不一致；原文沒有確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198851) |
| [#198851](wrong_metadata/torch_198851/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | reduction 指定 dim=()時，編譯後回傳 scalar。 | 空維度 tuple 在 reduction shape 語意上不一致；原文沒有確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198851) |
| [#198852](wrong_metadata/torch_198852/README.md) | `torch.cat`：主要受測 API | 空 float64 tensor 與多個非空 float32 tensor 串接時，輸出 float32。 | 上游指出 cat decomposition 移除空 tensor 後重算 dtype，遺失 promotion 資訊。 | [原文](https://github.com/pytorch/pytorch/issues/198852) |
| [#198852](wrong_metadata/torch_198852/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 空 float64 tensor 與多個非空 float32 tensor 串接時，輸出 float32。 | 上游指出 cat decomposition 移除空 tensor 後重算 dtype，遺失 promotion 資訊。 | [原文](https://github.com/pytorch/pytorch/issues/198852) |
| [#198868](wrong_metadata/torch_198868/README.md) | `torch.scatter`：主要受測 API | scalar input 與 empty index時，shape 變成 (1,)。 | scalar／空 index 的 tensor rank 表示不一致；上游未確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198868) |
| [#198868](wrong_metadata/torch_198868/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | scalar input 與 empty index時，shape 變成 (1,)。 | scalar／空 index 的 tensor rank 表示不一致；上游未確認完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/198868) |
| [#198994](wrong_metadata/torch_198994/README.md) | `torch.nn.functional.soft_margin_loss`：主要受測 API | input float32、target float64時，Inductor 回傳 float64。 | 上游修補討論指出 opmath promotion 後應 cast 回 input dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198994) |
| [#198994](wrong_metadata/torch_198994/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | input float32、target float64時，Inductor 回傳 float64。 | 上游修補討論指出 opmath promotion 後應 cast 回 input dtype。 | [原文](https://github.com/pytorch/pytorch/issues/198994) |
| [#199020](wrong_forward_value/torch_199020/README.md) | `torch.cummax(out=...)`：主要受測 API | cummax 的 values 與 indices 使用同一個 out tensor 時，回傳的 values 被 indices 覆寫。 | 本地測試比較獨立輸出和共享 out tensor，並檢查 storage 指標，範圍限於 int64 cummax。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/199020) |
| [#199211](unexpected_exception/torch_199211/README.md) | `torch.isin`：主要受測 API | test_elements 為無法直接 flatten 的非連續多維 tensor時，view-size compatibility RuntimeError。 | 上游定位 isin CPU kernel 使用 view(-1) 而不是可複製的 reshape。 | [原文](https://github.com/pytorch/pytorch/issues/199211) |
| [#199214](unexpected_exception/torch_199214/README.md) | `torch.dequantize`：主要受測 API | 普通 float input 先 dequantize 再原地 trunc_時，functionalization 拋 copy_／dequantize assertion。 | 上游指出非量化 dequantize 的 input alias 語意使 mutation copy-back 目標追蹤錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/199214) |
| [#199214](unexpected_exception/torch_199214/README.md) | `torch.Tensor.trunc_`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 普通 float input 先 dequantize 再原地 trunc_時，functionalization 拋 copy_／dequantize assertion。 | 上游指出非量化 dequantize 的 input alias 語意使 mutation copy-back 目標追蹤錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/199214) |
| [#199214](unexpected_exception/torch_199214/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 普通 float input 先 dequantize 再原地 trunc_時，functionalization 拋 copy_／dequantize assertion。 | 上游指出非量化 dequantize 的 input alias 語意使 mutation copy-back 目標追蹤錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/199214) |
| [#199229](wrong_forward_value/torch_199229/README.md) | `torch.Tensor.set_`：Rebinds the destination tensor storage | Compiled output is 10.0 instead of the eager 7.0 after Tensor.set_ then mutation of old storage. | Compiled Tensor.set_ storage rebinding incorrectly retains a dependency on mutated old storage. | [原文](https://github.com/pytorch/pytorch/issues/199229) |
| [#199229](wrong_forward_value/torch_199229/README.md) | `torch.compile`：Exercises the compiled storage-rebinding path | Compiled output is 10.0 instead of the eager 7.0 after Tensor.set_ then mutation of old storage. | Compiled Tensor.set_ storage rebinding incorrectly retains a dependency on mutated old storage. | [原文](https://github.com/pytorch/pytorch/issues/199229) |
| [#199350](unexpected_exception/torch_199350/README.md) | `torch.view_as_complex_copy`：主要受測 API | pooling 後接 view_as_complex_copy，Inductor 選擇 layout時，fallback 拋 last dimension stride 1 RuntimeError。 | 上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。 | [原文](https://github.com/pytorch/pytorch/issues/199350) |
| [#199350](unexpected_exception/torch_199350/README.md) | `torch.nn.functional.adaptive_max_pool2d`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | pooling 後接 view_as_complex_copy，Inductor 選擇 layout時，fallback 拋 last dimension stride 1 RuntimeError。 | 上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。 | [原文](https://github.com/pytorch/pytorch/issues/199350) |
| [#199350](unexpected_exception/torch_199350/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | pooling 後接 view_as_complex_copy，Inductor 選擇 layout時，fallback 拋 last dimension stride 1 RuntimeError。 | 上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。 | [原文](https://github.com/pytorch/pytorch/issues/199350) |
| [#199571](unexpected_exception/torch_199571/README.md) | `torch.linalg.solve`：主要受測 API | complex right solve(left=False) 的輸出取 imag時，view_as_real 不接受 unresolved conjugated tensor。 | right solve 的 lazy conjugate bit 沒有在編譯分解中妥善處理。 | [原文](https://github.com/pytorch/pytorch/issues/199571) |
| [#199571](unexpected_exception/torch_199571/README.md) | `torch.imag`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | complex right solve(left=False) 的輸出取 imag時，view_as_real 不接受 unresolved conjugated tensor。 | right solve 的 lazy conjugate bit 沒有在編譯分解中妥善處理。 | [原文](https://github.com/pytorch/pytorch/issues/199571) |
| [#199571](unexpected_exception/torch_199571/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | complex right solve(left=False) 的輸出取 imag時，view_as_real 不接受 unresolved conjugated tensor。 | right solve 的 lazy conjugate bit 沒有在編譯分解中妥善處理。 | [原文](https://github.com/pytorch/pytorch/issues/199571) |
| [#199644](wrong_forward_value/torch_199644/README.md) | `torch.Tensor.item`：主要受測 API | 擷取 float64 scalar 16777219 再傳入 CPU 編譯 kernel時，兩者皆變成 16777220。 | 上游定位 C++ kernel scalar 參數宣告為 const float，縮窄原本的 float64 表示。 | [原文](https://github.com/pytorch/pytorch/issues/199644) |
| [#199644](wrong_forward_value/torch_199644/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 擷取 float64 scalar 16777219 再傳入 CPU 編譯 kernel時，兩者皆變成 16777220。 | 上游定位 C++ kernel scalar 參數宣告為 const float，縮窄原本的 float64 表示。 | [原文](https://github.com/pytorch/pytorch/issues/199644) |
| [#199920](wrong_metadata/torch_199920/README.md) | `torch.ops.aten._fused_moving_avg_obs_fq_helper_functional`：主要受測 API | per-channel fake quant observer 首次使用，八個 channel時，min/max 仍為零長、scale/zero-point 仍為一。 | 上游 meta function 未模擬 observer buffer resize；主要是 tensor metadata，次要涉及訓練 buffer。 | [原文](https://github.com/pytorch/pytorch/issues/199920) |
| [#199920](wrong_metadata/torch_199920/README.md) | `torch._subclasses.fake_tensor.FakeTensorMode`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | per-channel fake quant observer 首次使用，八個 channel時，min/max 仍為零長、scale/zero-point 仍為一。 | 上游 meta function 未模擬 observer buffer resize；主要是 tensor metadata，次要涉及訓練 buffer。 | [原文](https://github.com/pytorch/pytorch/issues/199920) |
| [#200572](wrong_gradient/torch_200572/README.md) | `torch.autograd.Function`：主要受測 API | custom Function 輸出為 input view，再回傳其 view時，custom backward 被跳過。 | 上游指出只檢查直接 grad_fn，額外 view 導致誤分類為 alias_of_input；主要是 alias metadata。 | [原文](https://github.com/pytorch/pytorch/issues/200572) |
| [#200572](wrong_gradient/torch_200572/README.md) | `torch.Tensor.unsqueeze`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | custom Function 輸出為 input view，再回傳其 view時，custom backward 被跳過。 | 上游指出只檢查直接 grad_fn，額外 view 導致誤分類為 alias_of_input；主要是 alias metadata。 | [原文](https://github.com/pytorch/pytorch/issues/200572) |
| [#200572](wrong_gradient/torch_200572/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | custom Function 輸出為 input view，再回傳其 view時，custom backward 被跳過。 | 上游指出只檢查直接 grad_fn，額外 view 導致誤分類為 alias_of_input；主要是 alias metadata。 | [原文](https://github.com/pytorch/pytorch/issues/200572) |
| [#200599](wrong_forward_value/torch_200599/README.md) | `torch.linalg.lu_solve`：主要受測 API | LU[:,None] 的 singleton batch stride 非標準時，解為 [0.2,0.6,5,-1]。 | CPU kernel 用 singleton 維度 stride 當作相鄰矩陣距離。 | [原文](https://github.com/pytorch/pytorch/issues/200599) |
| [#200925](wrong_forward_value/torch_200925/README.md) | `torch.compile`：主要受測 API | 先以不同 offset 的重疊 views 暖機，再傳同 offset aliases時，沿用第一次 synthetic-base offset，寫錯位置。 | 上游 synthetic-base cache guard 未完整描述 storage partition／view offset；必須保留前置呼叫。 | [原文](https://github.com/pytorch/pytorch/issues/200925) |
| [#201268](wrong_forward_value/torch_201268/README.md) | `torch.add`：主要受測 API | CSR out.values() 為合法 stride=2 view時，values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element。 | 上游定位 mkl_result_copy_ 線性複製 nnz，忽略 destination values stride。 | [原文](https://github.com/pytorch/pytorch/issues/201268) |
| [#201268](wrong_forward_value/torch_201268/README.md) | `torch.sparse_csr_tensor`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | CSR out.values() 為合法 stride=2 view時，values 為 [11,-99]，寫入相鄰 storage 而非第二個 logical element。 | 上游定位 mkl_result_copy_ 線性複製 nnz，忽略 destination values stride。 | [原文](https://github.com/pytorch/pytorch/issues/201268) |
| [#201590](incorrect_state/torch_201590/README.md) | `torch.cond`：主要受測 API | aot_eager 接受同時執行 copy_ 並回傳輸入 alias 的 cond 分支，無 mutation 的 alias 控制組被拒絕。 | 本地測試比較 mutation 與非 mutation 分支，並檢查回傳值和輸入的 storage 指標。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/201590) |
| [#201590](incorrect_state/torch_201590/README.md) | `torch.Tensor.copy_`：共同觸發的原地寫入操作 | aot_eager 接受同時執行 copy_ 並回傳輸入 alias 的 cond 分支，無 mutation 的 alias 控制組被拒絕。 | 本地測試比較 mutation 與非 mutation 分支，並檢查回傳值和輸入的 storage 指標。 Root cause not confirmed。 | [原文](https://github.com/pytorch/pytorch/issues/201590) |
| [#201649](wrong_gradient/torch_201649/README.md) | `torch.compiler.nested_compile_region`：主要受測 API | 連續呼叫 nested region，forward 保存 region input 供 backward時，第一個梯度錯誤依賴 y。 | 上游指出 InvokeSubgraph MultiOutput 缺少 input-output alias 資訊，scheduler 重用仍被保存的 storage。 | [原文](https://github.com/pytorch/pytorch/issues/201649) |
| [#201649](wrong_gradient/torch_201649/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 連續呼叫 nested region，forward 保存 region input 供 backward時，第一個梯度錯誤依賴 y。 | 上游指出 InvokeSubgraph MultiOutput 缺少 input-output alias 資訊，scheduler 重用仍被保存的 storage。 | [原文](https://github.com/pytorch/pytorch/issues/201649) |
| [#202364](wrong_gradient/torch_202364/README.md) | `torch.Tensor.as_strided_`：主要受測 API | view 的 shape/stride 原地變更後 mul_，再 compiled backward時，forward 正確、gradient=[2,6,6,6]。 | 原文確認 view metadata mutation 是觸發條件；未確認錯誤 backward 的完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/202364) |
| [#202364](wrong_gradient/torch_202364/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | view 的 shape/stride 原地變更後 mul_，再 compiled backward時，forward 正確、gradient=[2,6,6,6]。 | 原文確認 view metadata mutation 是觸發條件；未確認錯誤 backward 的完整內部根因。 | [原文](https://github.com/pytorch/pytorch/issues/202364) |
| [#202416](unexpected_exception/torch_202416/README.md) | `torch.compile`：Enters the compiled path | Inductor raises a ViewMeta output-shape assertion while eager works. | AOTAutograd mishandles ViewMeta replay when returning both a view and detached alias. | [原文](https://github.com/pytorch/pytorch/issues/202416) |
| [#202416](unexpected_exception/torch_202416/README.md) | `torch.Tensor.detach`：Creates the detached alias | Inductor raises a ViewMeta output-shape assertion while eager works. | AOTAutograd mishandles ViewMeta replay when returning both a view and detached alias. | [原文](https://github.com/pytorch/pytorch/issues/202416) |
| [#202482](wrong_forward_value/torch_202482/README.md) | `torch.cat`：主要受測 API | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202482](wrong_forward_value/torch_202482/README.md) | `torch.nn.functional.linear`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202482](wrong_forward_value/torch_202482/README.md) | `torch.Tensor.index_put_`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202482](wrong_forward_value/torch_202482/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | Linear 輸出參與 cat，按固定索引順序修改 cat 後再讀 Linear時，符合讀到已被覆寫 cat storage 的完整錯誤模式。 | Inductor 讓 producer 直接寫入 cat buffer，形成不應有的 alias。 | [原文](https://github.com/pytorch/pytorch/issues/202482) |
| [#202726](unexpected_exception/torch_202726/README.md) | `torch.Tensor.real`：主要受測 API | real dtype 的 __torch_function__ subclass 在 compiled 中取 .real時，source must be None 的 AssertionError。 | 上游懷疑 real 的 identity alias 與 subclass source tracking 衝突；未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/202726) |
| [#202726](unexpected_exception/torch_202726/README.md) | `torch.Tensor.__torch_function__`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | real dtype 的 __torch_function__ subclass 在 compiled 中取 .real時，source must be None 的 AssertionError。 | 上游懷疑 real 的 identity alias 與 subclass source tracking 衝突；未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/202726) |
| [#202726](unexpected_exception/torch_202726/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | real dtype 的 __torch_function__ subclass 在 compiled 中取 .real時，source must be None 的 AssertionError。 | 上游懷疑 real 的 identity alias 與 subclass source tracking 衝突；未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/202726) |
| [#202862](unexpected_exception/torch_202862/README.md) | `torch.ops.aten.unsqueeze_.default`：主要受測 API | 直接對 graph input 呼叫 OpOverload 的 inplace rank-changing view時，guard creation 拋 IndexError。 | tensor rank metadata 改變與 guard 建立不一致；上游也明確指出是 Python exception 而非 process crash。 | [原文](https://github.com/pytorch/pytorch/issues/202862) |
| [#202862](unexpected_exception/torch_202862/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 直接對 graph input 呼叫 OpOverload 的 inplace rank-changing view時，guard creation 拋 IndexError。 | tensor rank metadata 改變與 guard 建立不一致；上游也明確指出是 Python exception 而非 process crash。 | [原文](https://github.com/pytorch/pytorch/issues/202862) |
| [#202966](wrong_forward_value/torch_202966/README.md) | `torch.distributions.kl_divergence`：主要受測 API | batched Wishart KL 且 p 的 df/covariance 要求梯度時，df term 錯跨 batch 加總，兩類 p 參數梯度皆 None。 | 上游指出 event-rank contraction 錯用到 batch 軸；另有獨立的 p natural parameters detach 問題，需決定根因拆分政策。 | [原文](https://github.com/pytorch/pytorch/issues/202966) |
| [#202966](wrong_forward_value/torch_202966/README.md) | `torch.distributions.Wishart`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | batched Wishart KL 且 p 的 df/covariance 要求梯度時，df term 錯跨 batch 加總，兩類 p 參數梯度皆 None。 | 上游指出 event-rank contraction 錯用到 batch 軸；另有獨立的 p natural parameters detach 問題，需決定根因拆分政策。 | [原文](https://github.com/pytorch/pytorch/issues/202966) |
| [#203078](wrong_forward_value/torch_203078/README.md) | `torch.Tensor.scatter_add`：主要受測 API | expanded index stride=(1,0)，self 比 index 更寬時，寫入 row 0、1，row sums=[16,16,0]。 | 上游定位 expanded-index fast path 把 index width 當成 destination row stride。 | [原文](https://github.com/pytorch/pytorch/issues/203078) |
| [#203078](wrong_forward_value/torch_203078/README.md) | `torch.Tensor.scatter_reduce`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | expanded index stride=(1,0)，self 比 index 更寬時，寫入 row 0、1，row sums=[16,16,0]。 | 上游定位 expanded-index fast path 把 index width 當成 destination row stride。 | [原文](https://github.com/pytorch/pytorch/issues/203078) |
| [#203485](unexpected_exception/torch_203485/README.md) | `torch.nn.functional.grouped_mm`：主要受測 API | sum().backward() 傳入 stride=[0,0] 的 broadcast gradient時，Invalid strides/sizes RuntimeError。 | 上游確認零 stride gradient 未被 grouped_mm backward 適當 materialize；根因分類依 layout 觸發。 | [原文](https://github.com/pytorch/pytorch/issues/203485) |
| [#203806](wrong_forward_value/torch_203806/README.md) | `torch._foreach_copy_`：主要受測 API | 以 [b.clone(),a.clone()] 複製回 [a,b]時，兩個 tensor 都得到原 b 的值。 | 上游重現指出編譯器在讀完 clone source 前就寫 destination，破壞 storage 資料依賴。 | [原文](https://github.com/pytorch/pytorch/issues/203806) |
| [#203806](wrong_forward_value/torch_203806/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 以 [b.clone(),a.clone()] 複製回 [a,b]時，兩個 tensor 都得到原 b 的值。 | 上游重現指出編譯器在讀完 clone source 前就寫 destination，破壞 storage 資料依賴。 | [原文](https://github.com/pytorch/pytorch/issues/203806) |
| [#203852](missing_exception/torch_203852/README.md) | `torch.Tensor.index_add`：主要受測 API | 整數 tensor 配 floating alpha=2.5 或 0.5時，alpha 靜默截為 2 或 0。 | 上游提議補 alpha_check，主要是 scalar-to-tensor dtype 相容契約；是否連 2.0 也拒絕仍是上游政策。 | [原文](https://github.com/pytorch/pytorch/issues/203852) |
| [#203866](unexpected_exception/torch_203866/README.md) | `DTensor.from_local`：Wraps the local tensor as a DTensor | torch.save raises an invalid-storage RuntimeError for a DTensor with a nonzero storage offset while the zero-offset control serializes. | A nonzero storage offset makes the DTensor placeholder pointer appear nonzero during serialization. | [原文](https://github.com/pytorch/pytorch/issues/203866) |
| [#203866](unexpected_exception/torch_203866/README.md) | `torch.save`：Serializes the wrapper | torch.save raises an invalid-storage RuntimeError for a DTensor with a nonzero storage offset while the zero-offset control serializes. | A nonzero storage offset makes the DTensor placeholder pointer appear nonzero during serialization. | [原文](https://github.com/pytorch/pytorch/issues/203866) |
| [#204181](wrong_forward_value/torch_204181/README.md) | `torch.Tensor.fill_diagonal_`：主要受測 API | 非連續 7x2 column view，wrap=True時，寫入 view 外的第三欄，漏掉 wrapped cell。 | 上游懷疑 wrapped diagonal 索引使用 contiguous 假設；layout 觸發已知，完整根因未確認。 | [原文](https://github.com/pytorch/pytorch/issues/204181) |
| [#204407](wrong_gradient/torch_204407/README.md) | `torch.linalg.slogdet`：主要受測 API | A=z.conj().imag，negative view、stride=(4,2)、offset=1時，off-diagonal gradient 轉置，real gradient 仍零。 | 上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。 | [原文](https://github.com/pytorch/pytorch/issues/204407) |
| [#204407](wrong_gradient/torch_204407/README.md) | `torch.Tensor.conj`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | A=z.conj().imag，negative view、stride=(4,2)、offset=1時，off-diagonal gradient 轉置，real gradient 仍零。 | 上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。 | [原文](https://github.com/pytorch/pytorch/issues/204407) |
| [#204407](wrong_gradient/torch_204407/README.md) | `torch.Tensor.imag`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | A=z.conj().imag，negative view、stride=(4,2)、offset=1時，off-diagonal gradient 轉置，real gradient 仍零。 | 上游分析指出 negative fallback clone 改變 layout，forward LU 與 backward 對原 layout 的轉置判斷不一致。 | [原文](https://github.com/pytorch/pytorch/issues/204407) |
| [#204426](wrong_gradient/torch_204426/README.md) | `torch.compile`：Enters the compiled path | Compiled autograd connects a view created under no_grad back to its input, producing gradient [2,3,3,3] where eager produces [2,2,2,2]. | Compiled Autograd incorrectly connects a no_grad view to its input. | [原文](https://github.com/pytorch/pytorch/issues/204426) |
| [#204426](wrong_gradient/torch_204426/README.md) | `torch.no_grad`：Disables gradient recording for view creation | Compiled autograd connects a view created under no_grad back to its input, producing gradient [2,3,3,3] where eager produces [2,2,2,2]. | Compiled Autograd incorrectly connects a no_grad view to its input. | [原文](https://github.com/pytorch/pytorch/issues/204426) |
| [#204426](wrong_gradient/torch_204426/README.md) | `torch.Tensor.view`：Creates the aliased view | Compiled autograd connects a view created under no_grad back to its input, producing gradient [2,3,3,3] where eager produces [2,2,2,2]. | Compiled Autograd incorrectly connects a no_grad view to its input. | [原文](https://github.com/pytorch/pytorch/issues/204426) |
| [#204442](wrong_forward_value/torch_204442/README.md) | `torch.add` | CSR out control equals 2*A, while CSC out equals (2*A).T instead of 2*A. | CSR 輸入搭配 CSC out 的 layout 未檢查，回傳轉置的錯誤結果。 | [原文](https://github.com/pytorch/pytorch/issues/204442) |
| [#204446](wrong_forward_value/torch_204446/README.md) | `torch.Tensor.add_`：主要受測 API | 對 base[1] 的 contiguous 非零 offset view 加 COO時，錯改 row 2。 | 上游定位 sparse CPU kernel 重複套用 storage_offset；本地刻意只測 allocation 內的錯位寫入。 | [原文](https://github.com/pytorch/pytorch/issues/204446) |
| [#204446](wrong_forward_value/torch_204446/README.md) | `torch.sparse_coo_tensor`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 對 base[1] 的 contiguous 非零 offset view 加 COO時，錯改 row 2。 | 上游定位 sparse CPU kernel 重複套用 storage_offset；本地刻意只測 allocation 內的錯位寫入。 | [原文](https://github.com/pytorch/pytorch/issues/204446) |
| [#205112](wrong_gradient/torch_205112/README.md) | `torch.func.jacrev`：主要受測 API | cdist(p=1) 的 jacrev 使用 batched cotangents時，各 Jacobian slice 重複第一個 cotangent 的結果。 | 上游指出 cdist_backward batching rule 沒有傳遞僅 grad 被 vmap 的 batch 維；主要為 tensor batching 表示。 | [原文](https://github.com/pytorch/pytorch/issues/205112) |
| [#205112](wrong_gradient/torch_205112/README.md) | `torch.cdist`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | cdist(p=1) 的 jacrev 使用 batched cotangents時，各 Jacobian slice 重複第一個 cotangent 的結果。 | 上游指出 cdist_backward batching rule 沒有傳遞僅 grad 被 vmap 的 batch 維；主要為 tensor batching 表示。 | [原文](https://github.com/pytorch/pytorch/issues/205112) |
| [#205497](wrong_optimizer_update/torch_205497/README.md) | `torch.optim.SGD`：主要受測 API | CPU fused=True，parameter 與 transposed gradient 的 stride 不同時，依 memory order 配對，形成置換的錯誤更新。 | 上游指出 fused CPU kernel 忽略各 tensor stride；optimizer 是症狀場景，主要機制是 layout。 | [原文](https://github.com/pytorch/pytorch/issues/205497) |
| [#205616](wrong_forward_value/torch_205616/README.md) | `torch.amax`：主要受測 API | 零維 CPU tensor x=3，out=x時，輸出與 input 都被改為 -inf。 | 上游定位 reduction 先把 out 初始化為 identity，覆蓋尚未讀取的 aliased input；是否應明確拒絕 overlap 待上游決策。 | [原文](https://github.com/pytorch/pytorch/issues/205616) |
| [#205620](wrong_forward_value/torch_205620/README.md) | `torch.linalg.solve_triangular`：主要受測 API | A=diag(2,4)、B=diag(6,20)，out=A時，回傳 identity。 | 上游 source inspection 指出先把 B 複製到 out，因 out=A 覆蓋係數矩陣。 | [原文](https://github.com/pytorch/pytorch/issues/205620) |
| [#205682](incorrect_state/torch_205682/README.md) | `torch.cat`：主要受測 API | 同正軸 cat 後按原長度 split，另有 mixed dtype 控制時，寫 split 修改 input；第一份 mixed output 留在 int32。 | 上游 ablation 指向 cat_splitwithsizes_replace 重寫，丟失新 storage 與 dtype promotion。 | [原文](https://github.com/pytorch/pytorch/issues/205682) |
| [#205682](incorrect_state/torch_205682/README.md) | `torch.Tensor.split`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 同正軸 cat 後按原長度 split，另有 mixed dtype 控制時，寫 split 修改 input；第一份 mixed output 留在 int32。 | 上游 ablation 指向 cat_splitwithsizes_replace 重寫，丟失新 storage 與 dtype promotion。 | [原文](https://github.com/pytorch/pytorch/issues/205682) |
| [#205682](incorrect_state/torch_205682/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 同正軸 cat 後按原長度 split，另有 mixed dtype 控制時，寫 split 修改 input；第一份 mixed output 留在 int32。 | 上游 ablation 指向 cat_splitwithsizes_replace 重寫，丟失新 storage 與 dtype promotion。 | [原文](https://github.com/pytorch/pytorch/issues/205682) |
| [#205810](unexpected_exception/torch_205810/README.md) | `torch.compile`：Exercises the Inductor backward path | Inductor backward fails on replication_pad2d_backward with stride/size metadata mismatch for channels-last CPU tensor. | Compiled Conv2d with replicate padding fails in backward because FakeTensor/meta strides differ from actual channels-last CPU output. | [原文](https://github.com/pytorch/pytorch/issues/205810) |
| [#205810](unexpected_exception/torch_205810/README.md) | `torch.nn.Conv2d`：Applies replicate padding to channels-last CPU input | Inductor backward fails on replication_pad2d_backward with stride/size metadata mismatch for channels-last CPU tensor. | Compiled Conv2d with replicate padding fails in backward because FakeTensor/meta strides differ from actual channels-last CPU output. | [原文](https://github.com/pytorch/pytorch/issues/205810) |
| [#206126](wrong_forward_value/torch_206126/README.md) | `torch.linalg.lu_solve`：Solves with an output that aliases the LU factor | LU factor aliases the out argument and yields a large residual while independent/rhs output are correct. | Output aliases LU factor, overwriting data required for the solve. | [原文](https://github.com/pytorch/pytorch/issues/206126) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#197084](wrong_gradient/torch_197084/README.md)：上游將此梯度症狀連結至 #198118；Issue 保留兩筆，獨立根因不應直接計為兩個。 
- [#198056](wrong_metadata/torch_198056/README.md)： Issue 包含多種 dtype/shape 症狀；本地只測 int8 cumsum。
- [#198118](wrong_forward_value/torch_198118/README.md)：與 #197084 共用 conjugate-view 根因線索；Issue 數不等於獨立根因數。 
- [#198155](missing_exception/torch_198155/README.md)：compiled 對不支援 eager dtype 的擴充，是否一律視為漏例外，需確認收錄政策。 Issue 的 134 operators／418 pairs 不屬本地驗證範圍；本地僅 int64 softmax。
- [#198669](unexpected_exception/torch_198669/README.md)： 上游討論連至 #196743 的 scaled-softmax rewrite；該 Issue 不在本次清單，未另增案例。
- [#198851](wrong_metadata/torch_198851/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#198868](wrong_metadata/torch_198868/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#199350](unexpected_exception/torch_199350/README.md)： 例外除了字串亦檢查 traceback 的 operator identity；此內部結構可能隨 build 變動。
- [#200925](wrong_forward_value/torch_200925/README.md)： 必須保留先前 alias-layout 暖機及同程序 graph reuse；不是只跑最後一次呼叫。
- [#201268](wrong_forward_value/torch_201268/README.md)： 本地固定 nnz 的 backing storage 錯寫不等於已驗證 allocation 外 memory corruption。
- [#202364](wrong_gradient/torch_202364/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#202726](unexpected_exception/torch_202726/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#202966](wrong_forward_value/torch_202966/README.md)：同一 Issue 測到 batch-axis contraction 與 p 參數梯度斷連；是否拆成兩個根因計數需決定。 
- [#203852](missing_exception/torch_203852/README.md)：對整數 tensor 的 integral float alpha 是否也拒絕，仍是上游相容性政策；本例只測非整數值。 
- [#204181](wrong_forward_value/torch_204181/README.md)：根因證據尚不足；分類依已知必要觸發條件。 
- [#204407](wrong_gradient/torch_204407/README.md)： 必須同時保留 negative bit、stride=(4,2)、offset=1 與 alias；z.grad.imag 必須包含 A=-imag(z) 的負號鏈式法則。
- [#204446](wrong_forward_value/torch_204446/README.md)： 本地只驗證 allocation 內的錯誤 row，未執行上游 heap corruption／process crash 變體。與 #59101 的重複根因尚未確認。
- [#205497](wrong_optimizer_update/torch_205497/README.md)： 本地只測 CPU fused SGD 與 gradient stride 差異；未覆蓋 Adam、AdamW、Adagrad 或 expanded-param heap corruption。
- [#205616](wrong_forward_value/torch_205616/README.md)：上游傾向拒絕 input/output overlap；需區分支援 alias 的正確值與明確拒絕兩種修復契約。 本地只測 amax scalar alias，不把上游其他 reductions 都列為已測 API。
- [#205620](wrong_forward_value/torch_205620/README.md)：out=A 的支援或明確拒絕政策尚待確認；本例只證明現有靜默錯解。 

- [#203866](unexpected_exception/torch_203866/README.md)：本次全套執行停在 Gloo 初始化，未執行序列化斷言。
- [#204442](wrong_forward_value/torch_204442/README.md)：Validity on PyTorch 2.15.0+cpu requires ten independent-process passes and preservation of all comparison controls. A pytest PASS is not proof of an independent root cause.
