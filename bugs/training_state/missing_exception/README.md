# training_state / missing_exception

[總目錄](../../README.md)

## 分類定義（Category Definition）

autograd graph／saved tensor、version counter／inplace mutation、backward／高階梯度規則、optimizer／parameter lifecycle、checkpoint／activation recomputation、training buffer mutation 與 retained graph 狀態。

Observation 定義：必要的輸入驗證、dtype 契約或 autograd version conflict 沒有拋出應有例外。

## 分類準則（Classification Criteria）

先滿足 `training_state` 的根因分類，再以 `missing_exception` 作主要可觀察簽名；其餘症狀只列 Secondary。

先判定觸發機制，再選主要觀察；secondary 不另外複製案例。分類理由來自本地測試與上游內文／討論，不只取用舊 metadata。

## 資料夾摘要（Folder Summary）

Issue 數量：**4**（不重複 Issue ID）。

| Observation | Issue 數量 |
| --- | ---: |
| `missing_exception` | 4 |

## API 摘要（API Summary）

唯一 API 數：5；Issue/API 配對數：8。

| API | 涉及 Issue 數 |
| --- | ---: |
| `torch.Tensor.apply_` | 1 |
| `torch.Tensor.detach` | 2 |
| `torch.compile` | 3 |
| `torch.full` | 1 |
| `torch.matmul` | 1 |

## Issue／API 詳細說明與 GitHub 來源

| Issue | API 與作用 | 觀察／範圍 | 分類依據 | GitHub |
| --- | --- | --- | --- | --- |
| [#197887](torch_197887/README.md) | `torch.matmul`：主要受測 API | forward 保存 input view 後，原地修改 input 再 backward時，沒有例外，使用已修改資料計算梯度。 | 上游指出 reinterpret_tensor 建立獨立 version counter，破壞 saved tensor 的版本一致性。 | [原文](https://github.com/pytorch/pytorch/issues/197887) |
| [#197887](torch_197887/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | forward 保存 input view 後，原地修改 input 再 backward時，沒有例外，使用已修改資料計算梯度。 | 上游指出 reinterpret_tensor 建立獨立 version counter，破壞 saved tensor 的版本一致性。 | [原文](https://github.com/pytorch/pytorch/issues/197887) |
| [#200524](torch_200524/README.md) | `torch.full`：主要受測 API | fill value 是 requires_grad=True 的零維 tensor時，接受並建立可向 fill 反傳的 graph。 | Dynamo 將 full 重寫為 empty().fill_()，意外建立本不應存在的 autograd 連結。 | [原文](https://github.com/pytorch/pytorch/issues/200524) |
| [#200524](torch_200524/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | fill value 是 requires_grad=True 的零維 tensor時，接受並建立可向 fill 反傳的 graph。 | Dynamo 將 full 重寫為 empty().fill_()，意外建立本不應存在的 autograd 連結。 | [原文](https://github.com/pytorch/pytorch/issues/200524) |
| [#202806](torch_202806/README.md) | `torch.Tensor.detach`：主要受測 API | eager 已保存 weight，再透過 compiled detached alias 修改時，沒有版本遞增，backward 靜默使用新 weight。 | 上游明確將此歸為漏掉 version check；不存在合法的「修改後仍應得到舊梯度」契約。 | [原文](https://github.com/pytorch/pytorch/issues/202806) |
| [#202806](torch_202806/README.md) | `torch.compile`：觸發編譯／快取路徑的必要入口 | eager 已保存 weight，再透過 compiled detached alias 修改時，沒有版本遞增，backward 靜默使用新 weight。 | 上游明確將此歸為漏掉 version check；不存在合法的「修改後仍應得到舊梯度」契約。 | [原文](https://github.com/pytorch/pytorch/issues/202806) |
| [#205134](torch_205134/README.md) | `torch.Tensor.apply_`：主要受測 API | 保存 x 後，對 detach alias 執行 apply_ 乘十時，版本不變，backward 靜默回傳 [20,40]。 | 上游確認 apply_ 原地寫入沒有 bump version；[2,4] 不可當作已修改情境的合法答案。 | [原文](https://github.com/pytorch/pytorch/issues/205134) |
| [#205134](torch_205134/README.md) | `torch.Tensor.detach`：共同觸發、狀態／表示操作或參考 API；範圍限於本案測試 | 保存 x 後，對 detach alias 執行 apply_ 乘十時，版本不變，backward 靜默回傳 [20,40]。 | 上游確認 apply_ 原地寫入沒有 bump version；[2,4] 不可當作已修改情境的合法答案。 | [原文](https://github.com/pytorch/pytorch/issues/205134) |

## 已知限制（Known Limitations）

歷史搬移驗證：原始整批 100 passed；暫存新結構整批 100 passed；正式搬移後 100 passed, 7 warnings。每階段一次，沿用 compiler cache，非十次隔離／冷編譯。

high／medium 為分類信心，不是上游根因獨立認證。原始 metadata 可能仍標記 pending；第一個修復版本未追查。數值或 ISA 相關簽名不得外推至其他環境。

- [#205134](torch_205134/README.md)： 未修改控制的 [2,4] 不能作為修改後的正確梯度；正確契約是版本衝突例外。本例只測 apply_，未測 Issue 的 map_ 變體。
