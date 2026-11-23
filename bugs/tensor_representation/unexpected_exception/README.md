# tensor_representation / unexpected_exception

[總目錄](../../README.md)

## 分類定義（Category Definition）

Tensor 的 shape、stride、contiguity、storage offset、view／alias、dtype／metadata、conjugate／negative view、重疊 storage、layout 或 materialization；包括直接由這些機制導致的寫入、梯度與編譯問題。

Observation 定義：本應成功或可由使用者 handler 處理的操作，拋出非預期 Python／編譯例外；不等同 process crash。

## 分類準則（Classification Criteria）

先滿足 `tensor_representation` 的根因分類，再以 `unexpected_exception` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**14**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `unexpected_exception` | 14 |

## API 摘要（API Summary）

唯一 API 數：23；Issue/API 配對數：32。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.compile` | 10 |
| `DTensor.from_local` | 1 |
| `torch.autograd.functional.jacobian` | 1 |
| `torch.dequantize` | 1 |
| `torch.div` | 1 |
| `torch.eq` | 1 |
| `torch.func.jacfwd` | 1 |
| `torch.imag` | 1 |
| `torch.isin` | 1 |
| `torch.linalg.solve` | 1 |
| `torch.linalg.vector_norm` | 1 |
| `torch.nn.Conv2d` | 1 |
| `torch.nn.functional.adaptive_max_pool2d` | 1 |
| `torch.nn.functional.grouped_mm` | 1 |
| `torch.ops.aten.unsqueeze_.default` | 1 |
| `torch.save` | 1 |
| `torch.softmax` | 1 |
| `torch.Tensor.__torch_function__` | 1 |
| `torch.Tensor.detach` | 1 |
| `torch.Tensor.real` | 1 |
| `torch.Tensor.set_` | 1 |
| `torch.Tensor.trunc_` | 1 |
| `torch.view_as_complex_copy` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197097](torch_197097/README.md) | `torch.linalg.vector_norm`：主要受測 API | shape=(0,5)、ord=inf、dim=-1時，錯判 reduction 維度為空並拋例外。 | 上游指出負維度未正規化，導致空 batch 與 reduction 維度混淆。 | [原文](https://github.com/pytorch/pytorch/issues/197097) |
| [#197097](torch_197097/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | shape=(0,5)、ord=inf、dim=-1時，錯判 reduction 維度為空並拋例外。 | 上游指出負維度未正規化，導致空 batch 與 reduction 維度混淆。 | [原文](https://github.com/pytorch/pytorch/issues/197097) |
| [#197399](torch_197399/README.md) | `torch.Tensor.set_`：主要受測 API | 把空 tensor 的 storage 重綁成長度一後讀 x[0]時，仍以舊空 shape 追蹤並拋 IndexError。 | 上游指出 functional tensor 內層已更新，但 wrapper TensorImpl metadata 未同步。 | [原文](https://github.com/pytorch/pytorch/issues/197399) |
| [#197399](torch_197399/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 把空 tensor 的 storage 重綁成長度一後讀 x[0]時，仍以舊空 shape 追蹤並拋 IndexError。 | 上游指出 functional tensor 內層已更新，但 wrapper TensorImpl metadata 未同步。 | [原文](https://github.com/pytorch/pytorch/issues/197399) |
| [#198669](torch_198669/README.md) | `torch.softmax`：主要受測 API | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#198669](torch_198669/README.md) | `torch.eq`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#198669](torch_198669/README.md) | `torch.div`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#198669](torch_198669/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | eq 產生 bool，除法升成 floating 後 softmax時，rewrite 嘗試對 bool 做 negation 而拋例外。 | 上游指出 scaled-softmax rewrite 用原 bool dtype 形成常數，忽略運算間的 dtype 轉換；與 #196743 相關。 | [原文](https://github.com/pytorch/pytorch/issues/198669) |
| [#199211](torch_199211/README.md) | `torch.isin`：主要受測 API | test_elements 為無法直接 flatten 的非連續多維 tensor時，view-size compatibility RuntimeError。 | 上游定位 isin CPU kernel 使用 view(-1) 而不是可複製的 reshape。 | [原文](https://github.com/pytorch/pytorch/issues/199211) |
| [#199214](torch_199214/README.md) | `torch.dequantize`：主要受測 API | 普通 float input 先 dequantize 再原地 trunc_時，functionalization 拋 copy_／dequantize assertion。 | 上游指出非量化 dequantize 的 input alias 語意使 mutation copy-back 目標追蹤錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/199214) |
| [#199214](torch_199214/README.md) | `torch.Tensor.trunc_`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 普通 float input 先 dequantize 再原地 trunc_時，functionalization 拋 copy_／dequantize assertion。 | 上游指出非量化 dequantize 的 input alias 語意使 mutation copy-back 目標追蹤錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/199214) |
| [#199214](torch_199214/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 普通 float input 先 dequantize 再原地 trunc_時，functionalization 拋 copy_／dequantize assertion。 | 上游指出非量化 dequantize 的 input alias 語意使 mutation copy-back 目標追蹤錯誤。 | [原文](https://github.com/pytorch/pytorch/issues/199214) |
| [#199350](torch_199350/README.md) | `torch.view_as_complex_copy`：主要受測 API | pooling 後接 view_as_complex_copy，Inductor 選擇 layout時，fallback 拋 last dimension stride 1 RuntimeError。 | 上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。 | [原文](https://github.com/pytorch/pytorch/issues/199350) |
| [#199350](torch_199350/README.md) | `torch.nn.functional.adaptive_max_pool2d`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | pooling 後接 view_as_complex_copy，Inductor 選擇 layout時，fallback 拋 last dimension stride 1 RuntimeError。 | 上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。 | [原文](https://github.com/pytorch/pytorch/issues/199350) |
| [#199350](torch_199350/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | pooling 後接 view_as_complex_copy，Inductor 選擇 layout時，fallback 拋 last dimension stride 1 RuntimeError。 | 上游指出 view_as_complex_copy 缺少 require_contiguous fallback 約束。 | [原文](https://github.com/pytorch/pytorch/issues/199350) |
| [#199571](torch_199571/README.md) | `torch.linalg.solve`：主要受測 API | complex right solve(left=False) 的輸出取 imag時，view_as_real 不接受 unresolved conjugated tensor。 | right solve 的 lazy conjugate bit 沒有在編譯分解中妥善處理。 | [原文](https://github.com/pytorch/pytorch/issues/199571) |
| [#199571](torch_199571/README.md) | `torch.imag`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | complex right solve(left=False) 的輸出取 imag時，view_as_real 不接受 unresolved conjugated tensor。 | right solve 的 lazy conjugate bit 沒有在編譯分解中妥善處理。 | [原文](https://github.com/pytorch/pytorch/issues/199571) |
| [#199571](torch_199571/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | complex right solve(left=False) 的輸出取 imag時，view_as_real 不接受 unresolved conjugated tensor。 | right solve 的 lazy conjugate bit 沒有在編譯分解中妥善處理。 | [原文](https://github.com/pytorch/pytorch/issues/199571) |
| [#200017](torch_200017/README.md) | `torch.autograd.functional.jacobian`：Exercises the failing vectorized forward-mode path and the reverse-mode control | strategy=forward-mode, vectorize=True raises a RuntimeError about a forward gradient having different size for a 1-D input to matmul. | Root cause not confirmed. The RuntimeError reports a tangent size mismatch for the 1-D matmul output. | [原文](https://github.com/pytorch/pytorch/issues/200017) |
| [#200017](torch_200017/README.md) | `torch.func.jacfwd`：Computes the working forward-mode reference | strategy=forward-mode, vectorize=True raises a RuntimeError about a forward gradient having different size for a 1-D input to matmul. | Root cause not confirmed. The RuntimeError reports a tangent size mismatch for the 1-D matmul output. | [原文](https://github.com/pytorch/pytorch/issues/200017) |
| [#202416](torch_202416/README.md) | `torch.compile`：Enters the compiled path | Inductor raises a ViewMeta output-shape assertion while eager works. | AOTAutograd mishandles ViewMeta replay when returning both a view and detached alias. | [原文](https://github.com/pytorch/pytorch/issues/202416) |
| [#202416](torch_202416/README.md) | `torch.Tensor.detach`：Creates the detached alias | Inductor raises a ViewMeta output-shape assertion while eager works. | AOTAutograd mishandles ViewMeta replay when returning both a view and detached alias. | [原文](https://github.com/pytorch/pytorch/issues/202416) |
| [#202726](torch_202726/README.md) | `torch.Tensor.real`：主要受測 API | real dtype 的 __torch_function__ subclass 在 compiled 中取 .real時，source must be None 的 AssertionError。 | 上游懷疑 real 的 identity alias 與 subclass source tracking 衝突；未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/202726) |
| [#202726](torch_202726/README.md) | `torch.Tensor.__torch_function__`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | real dtype 的 __torch_function__ subclass 在 compiled 中取 .real時，source must be None 的 AssertionError。 | 上游懷疑 real 的 identity alias 與 subclass source tracking 衝突；未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/202726) |
| [#202726](torch_202726/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | real dtype 的 __torch_function__ subclass 在 compiled 中取 .real時，source must be None 的 AssertionError。 | 上游懷疑 real 的 identity alias 與 subclass source tracking 衝突；未確認完整根因。 | [原文](https://github.com/pytorch/pytorch/issues/202726) |
| [#202862](torch_202862/README.md) | `torch.ops.aten.unsqueeze_.default`：主要受測 API | 直接對 graph input 呼叫 OpOverload 的 inplace rank-changing view時，guard creation 拋 IndexError。 | tensor rank metadata 改變與 guard 建立不一致；上游也明確指出是 Python exception 而非 process crash。 | [原文](https://github.com/pytorch/pytorch/issues/202862) |
| [#202862](torch_202862/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | 直接對 graph input 呼叫 OpOverload 的 inplace rank-changing view時，guard creation 拋 IndexError。 | tensor rank metadata 改變與 guard 建立不一致；上游也明確指出是 Python exception 而非 process crash。 | [原文](https://github.com/pytorch/pytorch/issues/202862) |
| [#203485](torch_203485/README.md) | `torch.nn.functional.grouped_mm`：主要受測 API | sum().backward() 傳入 stride=[0,0] 的 broadcast gradient時，Invalid strides/sizes RuntimeError。 | 上游確認零 stride gradient 未被 grouped_mm backward 適當 materialize；根因分類依 layout 觸發。 | [原文](https://github.com/pytorch/pytorch/issues/203485) |
| [#203866](torch_203866/README.md) | `DTensor.from_local`：Wraps the local tensor as a DTensor | torch.save raises an invalid-storage RuntimeError for a DTensor with a nonzero storage offset while the zero-offset control serializes. | A nonzero storage offset makes the DTensor placeholder pointer appear nonzero during serialization. | [原文](https://github.com/pytorch/pytorch/issues/203866) |
| [#203866](torch_203866/README.md) | `torch.save`：Serializes the wrapper | torch.save raises an invalid-storage RuntimeError for a DTensor with a nonzero storage offset while the zero-offset control serializes. | A nonzero storage offset makes the DTensor placeholder pointer appear nonzero during serialization. | [原文](https://github.com/pytorch/pytorch/issues/203866) |
| [#205810](torch_205810/README.md) | `torch.compile`：Exercises the Inductor backward path | Inductor backward fails on replication_pad2d_backward with stride/size metadata mismatch for channels-last CPU tensor. | Compiled Conv2d with replicate padding fails in backward because FakeTensor/meta strides differ from actual channels-last CPU output. | [原文](https://github.com/pytorch/pytorch/issues/205810) |
| [#205810](torch_205810/README.md) | `torch.nn.Conv2d`：Applies replicate padding to channels-last CPU input | Inductor backward fails on replication_pad2d_backward with stride/size metadata mismatch for channels-last CPU tensor. | Compiled Conv2d with replicate padding fails in backward because FakeTensor/meta strides differ from actual channels-last CPU output. | [原文](https://github.com/pytorch/pytorch/issues/205810) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#198669](torch_198669/README.md)： 上游討論連至 #196743 的 scaled-softmax rewrite；該 Issue 不在本次清單，未另增案例。
- [#199350](torch_199350/README.md)： 例外除了字串亦檢查 traceback 的 operator identity；此內部結構可能隨 build 變動。
- [#202726](torch_202726/README.md)：根因證據尚不足；分類依已知必要觸發條件。 

- [#203866](torch_203866/README.md)：本次全套執行停在 Gloo 初始化，未執行序列化斷言。
