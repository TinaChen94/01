# GPT Image（OpenAI 生圖 / 圖編輯）

> **校準日期：2026-11-09。** 版本、尺寸、參考圖上限的資料大多來自第三方部落格，各家說法不一致；
> 官方文件（developers.openai.com）本次從雲端環境連不到，**動到付費、批次或 API 參數前，先回官方文件確認。**
> 標 ✅ = 本 repo 實測；標 📰 = 網路資料（未經官方頁確認）。

---

## 版本（2026-11）

| 模型 | 定位 | 來源 |
|---|---|---|
| **GPT Image 2.6 Flare** | 生成 + 編輯，**快速迭代** | ✅ Leonardo 介面描述 / 📰 2026-11-04 發布 |
| **GPT Image 2.6 Sunburst** | 生成 + 編輯，**細節型視覺** | ✅ Leonardo 介面描述 |
| GPT Image 2.5（Flare / Sunburst） | 上一代，2026-09-08 | 📰 |
| GPT Image 2（`gpt-image-2`） | 「簡單 prompt 就有好構圖」，2026-04-21 | ✅ Leonardo 介面 / 📰 |
| gpt-image-1 / 1.5 / 1-mini | 舊版，陸續下架（2026-10 ~ 2026-12） | 📰 |

- 📰 API ID 寫法：`gpt-image-2.6-flare`、`gpt-image-2.6-sunburst`
- **怎麼選：** 草稿、多輪試配置 → **Flare**；定稿、細節多（石材、紋飾）→ **Sunburst**。
- 在 Leonardo 上三個都標 **Image Ref**（可上傳參考圖）。

## 尺寸限制 📰

- 自訂尺寸：**長寬都是 16 的倍數**，比例 **1:3 ~ 3:1**，最大 **3840×2160**
- 常用：1024×1024、1536×1024、1024×1536、2048×2048、3840×2160
- 超過 2560×1440 官方標為實驗性
- 一次 1–10 張
- ⚠️ 平台（如 Leonardo、ChatGPT App）可能只開放部分比例。**選不到輸入圖的比例 → 選最接近的橫/直式，出圖後 PS 裁切**，不要讓模型自己重新構圖。

## 參考圖上限 📰（說法衝突）

- GPT Image 2：約 4 張；GPT Image 2.5：最多 16 張（編輯）
- ✅ 實測 2.6 Flare 一次吃 **4 張**（灰盒 + 氣氛 + 設定稿 + 定位圖）正常。
- 官方建議：**參考圖越少越好管**。

---

## 社群 / 官方建議寫法 📰

1. **參考圖編號 + 一張一個任務。** 「Image 1 = 構圖、Image 2 = 氣氛…」。沒指派角色的參考圖會被不可預期地混進結果。
2. **說清楚怎麼組合。** 哪個元素從哪張來、放在哪裡；用 left / right / foreground / background 這類空間詞。
3. **局部編輯句型：** `Change only X. Keep everything else exactly the same.`（官方舉例的最清楚寫法）
4. **一輪只改一件事**，看結果再改下一件。
5. **不要在一張圖混兩個目標**（例如產品照 + 生活情境），拆兩張。
6. 文字渲染：要出現的字用引號包起來、寫清楚位置與字體風格。

## 本 repo 實測（✅ 2026-11-09，熔岩走道案）

同一段 **4 圖 prompt**（灰盒構圖權威 + 氣氛圖 + 柱子設定稿 + 火盆橘框定位圖），NB 2 與 GPT Image 2.6 Flare 對照：

| 項目 | GPT 2.6 Flare | Nano Banana 2 |
|---|---|---|
| 構圖 / 透視對齊灰盒 | ✅ | ✅ |
| 火盆數量、位置（橘框定位） | ✅ 6 個全對 | ✅（2 張中 1 張多畫 2 個） |
| 色調 | 更暗、對比更強 | 偏暖亮 |
| 地面 | ⚠️ 濕亮反光（沒寫 dry 就會出現） | ⚠️ 幾灘熔岩 |
| 柱子結構照設定稿 | ❌ 照灰盒形狀畫 | ❌ 同樣照灰盒 |
| 裝飾面朝向 | ⚠️ 紋章刻到錯的面 | — |

**結論：**
- 原本以為「NB 寫法 GPT 不吃」，**實測推翻**：角色標籤 + 定位圖 + LOCK 句，GPT 2.6 一樣能用。
- **灰盒幾何 > 參考設定稿**：兩個模型都一樣。柱子結構對不上不是模型問題，是灰盒形狀跟設定稿不一致 → 改灰盒，或先把設定稿的柱子拼貼進灰盒再跑。
- GPT 預設偏愛**濕亮地面、反光**：要乾地面必寫 `dry, matte floor — no wet shine, no reflections, no puddles`。

## GPT 版 prompt 寫法建議

- 句子寫成**完整口語句**，少用全大寫區塊標題；重要限制直接寫「do not…」。
- 結構順序：**每張參考圖的角色 → 要做的事（逐項）→ 要保留的東西 → 禁止清單**。
- 結構細節用**百分比 / 數量**寫死（例：「top 10%: cap… 10–27%: spike ring…」「exactly six braziers」）。
- 參考圖裡**只想借材質、不想借形狀**的，要明寫 `use only its material, not its shape`。
- 要像素級對位（投影、合成）→ 跟 NB 一樣，**生成後 PS 遮罩貼回**，不要期待模型逐像素保留。

---

## 來源

- 實測：`docs/asset-cases/`（熔岩要塞案例，2026-11）
- 📰 [GPT Image（Wikipedia）](https://en.wikipedia.org/wiki/GPT_Image)
- 📰 [GPT Image 2.6 overview（OpenArt）](https://openart.ai/blog/gpt-image-2-6-overview/)
- 📰 [GPT Image 2.6 Prompt Guide（OpenArt）](https://openart.ai/blog/gpt-image-2-6-prompt-guide/)
- 📰 [OpenAI Cookbook：Image generation prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- 📰 [OpenAI Academy：Creating images with ChatGPT](https://openai.com/academy/image-generation/)
- 📰 [OpenAI image API models & shutdown dates（aifreeapi）](https://www.aifreeapi.com/en/posts/openai-image-generation-api-models)
- 📰 [GPT Image 2.5 Prompt Guide（fuser）](https://fuser.studio/articles/gpt-image-prompt-guide)
