# Depth → Relight → Fusion 穩定打光管線

把「光打哪邊」從 AI 的隨機擲骰，變成**你用控制圖決定**的可重現流程。
核心:Nano Banana 沒有 seed(自回歸架構),要穩定就得**把輸入凍結 + 用控制圖鎖死形狀與光向**。
搭配工具:[../tools/depth-relight.html](../tools/depth-relight.html)、[../tools/prompt-copier.html](../tools/prompt-copier.html)。

---

## 為什麼要這條管線

我們一路上的漂移來自三個維度,這條管線把三個全鎖死:

| 漂移維度 | 用什麼鎖 |
|---|---|
| 形狀 / 姿勢 | depth map(從原圖或草稿生) |
| **光向** | depth-relight 工具的 Key/Fill/Rim 雷達盤 ★ |
| 材質 / 風格 | 風格參考圖 |

剩給 AI 的自由趨近於零 → 輸出自然穩定。**這就是「沒有 seed 也能穩」的答案。**

---

## 完整四步

```
原圖/草稿 ─①─▶ depth map ─②─▶ depth-relight 工具打光 ─▶ 光影控制圖
                                                              │
              風格參考圖 ───────────────③──────────────────▶ ④ 多重參考融合 ─▶ 成品
```

### ① 生 depth map(Nano Banana Pro)
```
depth map, grayscale, height map, z-depth, white is near, black is far,
high contrast, smooth gradient, 3d render style, no texture, no color, black background
```

### ② 用工具打光 → 下載控制圖
開 `depth-relight.html`,載入 depth map,雷達盤拖燈定光向,下載。
**物件**:Cutoff 0.05、Depth 26–45。**場景**:Cutoff 設 0、Depth 調低(見工具 README 限制說明)。

### ③ 準備風格參考圖
一張代表目標材質/畫風/色調的圖(只取風格,不取形狀)。

### ④ 多重參考融合(角色分離,防打架)
餵三張圖並**明確分派角色**——這是多參考最容易翻車的地方,務必鎖:
- **[SOURCE_CONTENT] 原始資料** — 身分、服裝、配件(要畫的主體)
- **[STYLE_REF] 風格參考** — 只取材質、畫風、色調,**忽略它的形狀/主體**
- **[POSE_LIGHTING_REF] 光影姿勢** — 只取動作 + 打光方向,**忽略它的服裝/配件**
- 🔑 **關鍵鎖**:套姿勢但**保留原角色的身體比例**,不要抄 pose 圖的體型

> 完整可貼的融合 system prompt 在 `prompt-copier.html` 的「多重參考融合」卡片(逐字保存)。

---

## 用在場景重打光

- **淺景深場景**(浮雕牆、立面、背景板、地貌)→ 工具可直接出圖。
- **深景深場景**(近物 + 遠景分離大,如森林)→ 工具是 2.5D 高度場,會把前後景拉成一片。
  **改當「場景光向控制圖」**:工具只決定光的方位,把控制圖 + 場景原圖餵 Nano Banana,
  遮擋與寫實交給 NB 的世界知識補。
- **只想換氛圍、不需精準** → 不必動工具,直接在 NB 下重打光指令最省事:
  ```
  保持這張場景的構圖與幾何完全不變，只重新打光：
  主光改為[左上方冷藍月光]、整體壓暗、加地面薄霧，陰影方向一致，photorealistic。
  ```

---

## 相關
- 物件合成模板(鎖材質光影) → [nano-banana.md → 物件合成進場景](nano-banana.md#物件合成進場景-game-asset--把物件放進背景圖--實測通用模板)
- B2 案例(物件放進場景) → [../examples/B2-statue-into-forest.md](../examples/B2-statue-into-forest.md)
- 強化版 AO map prompt(原工具版太簡略):
  ```
  ambient occlusion map, AO pass, grayscale, soft contact shadows in crevices and
  recesses, white where exposed, dark where occluded, no color, no texture,
  no direct lighting, smooth, white background
  ```
