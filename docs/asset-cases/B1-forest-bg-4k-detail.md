# 實戰紀錄 — B1 夜霧森林地面背景：4K 放大 + 地面材質細節管線

> Game background asset 的「保真放大 → 增加細節」品質管線驗證紀錄。
> 對應工作流:`ai-media-generator`(quality-control / 放大與細節 pass 思路)。

## 來源(索引)
- **素材:** 夜霧森林地面背景(前景兩棵樹幹 + 苔蘚草地,16:9 滿版約 2K)
  - 版本 A:純黑背景(cutout / 夜景合成用)
  - 版本 B:青綠霧中枯樹背景(完整場景版)
- **用途:** 投影(camera projection)回 3D 灰盒場景
- **平台:** Leonardo Universal Upscaler(保真 2× 放大)+ Google Gemini Nano Banana Pro(細節 pass)
- **日期:** 2026-07-02
- **結果:** ✅ 最終版「材質保真 pass」達成期望 — 地面紋理細節提升至 UE5 掃描質感,構圖/色調/景深零漂移

---

## 最終定案管線

```
滿版 16:9 原檔(2K,無白邊 letterbox!)
  → Leonardo Universal Upscaler 2×(creativity 最低檔)
  → Gemini Nano Banana Pro「材質保真 pass」(下方最終 prompt)
  → 100% 原寸驗收(見 checklist)
  →(套圖時)四張同配方 → 互拼驗縫 → 縫帶 inpaint → 進引擎投影驗收
```

---

## 用到的 prompt(逐字保存)

### 1. 最終版 — 地面材質保真 pass(✅ 驗證成功)

適用:要「地面紋理變高清(UE5 / Megascans 級)」而**不要**多出草叢/石頭/枯枝等物件。

```text
Enhance the ground surface of this dark misty forest game background.
This is a TEXTURE-FIDELITY pass, NOT an object pass — think of it as
replacing the ground material with a higher-resolution scan of the SAME
material.

INCREASE ONLY surface micro-detail on the existing ground: finer moss
granularity with subtle natural clumping, richer soil and dirt texture
with small variations in color and roughness, damp organic sheen where
the ground is darker, and gentle ambient-occlusion depth inside the
existing ground crevices and undulations. Target quality: photorealistic
PBR ground material, Unreal Engine 5 / Quixel Megascans scan fidelity.

Do NOT place anything on the ground: no standing grass blades or tufts,
no twigs, no branches, no stones or pebbles lying on the surface, no
leaves, no debris. The ground stays a continuous surface — only its
texture resolution becomes richer. Every existing shape, contour and
silhouette stays exactly as it is.

FRAME LOCK: keep the exact original 16:9 canvas, framing and camera — do
NOT crop, zoom, extend or outpaint. The two foreground tree trunks,
bushes and ground contours stay at their exact position and size.

PRESERVE THE DEPTH: the distant bare trees in the teal fog stay soft,
hazy and unsharpened — no detail or contrast behind the fog line; fog
density unchanged.

STRICT: no new objects of any kind, do not brighten the shadows, keep
the muted dark teal-green night palette exactly.
```

### 2. 變體 — 純黑背景版的放大/細節鎖句(版本 A 素材用)

黑背景 cutout 素材時,把 FRAME LOCK / DEPTH 段換成**黑鎖 + 邊緣鎖 + 曝光鎖**:

```text
STRICT: keep the pure black background exactly pure black (#000000) — do
NOT add noise, fog, stars, gradient or any texture into the black areas.
Keep the silhouette edges of the tree trunks and foliage against the
black background crisp and clean, no glow, no fringing. Do not brighten
the shadows — preserve the dark, muted night-forest grade and the exact
color palette.
```

### 3. 淘汰版 — 物件式細節 pass(❌ 不符本需求,留作對照)

允許清單寫「草葉/苔蘚塊/枯枝/小石」→ 產出**立起來的草叢與散落石塊**,
是「往地上放東西」不是「材質變高清」。要材質就用 prompt 1 的
TEXTURE-FIDELITY 寫法;要植被豐富度才用允許清單寫法。

---

## 產出對照

### 原圖(2K 滿版,細節 pass 前)
![B1 forest original](images/b1-forest-original.png)

### 最終成品(材質保真 pass 後 — UE5 級地面紋理)
![B1 forest final texture pass](images/b1-forest-final-texture.png)

---

## 踩坑紀錄(依時間序)

| # | 現象 | 根因 | 解法 |
|---|---|---|---|
| 1 | Universal Upscaler 放大後綠色被提亮、往白天跑;細節是「抹平再銳化」的假細節 | **輸入是帶白邊 letterbox 的方形縮小版**,場景有效解析度只剩一半 | 一律用滿版原檔輸入;白邊裁掉 |
| 2 | NBP 細節 pass 輸出變 1:1、鏡頭拉近、多出大石/粗枝(甚至頭骨狀石頭) | 又餵了 letterbox 版 → 模型把白邊當 outpaint 區重新構圖 | 滿版輸入 + prompt 加 **FRAME LOCK** 段 |
| 3 | 細節長對了但地上多出草叢、枯枝、碎石(非需求) | 允許清單 = 「放置物件」指令 | 改寫成 TEXTURE-FIDELITY pass(prompt 1),物件全進禁止清單 |
| 4 | 遠景枯樹有左右鏡像對稱 artifact | 原圖生成時的對稱性瑕疵 | 選配修法:`Fix the mirrored symmetry in the distant background branches — make the tree silhouettes asymmetric and natural, while keeping them equally soft and hazy in the fog.` |

---

## 鎖句字典(可複用)

| 鎖 | 用途 | 關鍵句 |
|---|---|---|
| **畫框鎖** | 防裁切/變焦/outpaint | `keep the exact original 16:9 canvas, framing and camera — do NOT crop, zoom, extend or outpaint` |
| **黑鎖** | 純黑背景不長噪點/霧/星 | `pure black stays exactly pure black (#000000), do NOT add noise, fog, stars, gradient` |
| **邊緣鎖** | cutout 輪廓不糊不發光 | `silhouette edges ... crisp and clean, no glow, no fringing` |
| **曝光鎖** | 暗部不被偷提亮 | `do not brighten the shadows — preserve the dark, muted grade` |
| **深度鎖** | 霧後遠景不被銳化 | `distant trees in the fog stay soft, hazy and unsharpened — no detail or contrast behind the fog line` |
| **霧量鎖** | 霧不被清掉或加厚 | `do not thin out or thicken the fog` |
| **尺度鎖** | 紋理不被畫大一號 | `the ground texture scale stays identical to the input` |
| **定性句** | 給模型正確心智模型 | `This is a TEXTURE-FIDELITY pass, NOT an object pass — a higher-resolution scan of the SAME material` |
| **允許/禁止成對** | 控制細節種類 | ADD ONLY 清單 + do NOT 清單同時出現,缺一不可 |

---

## 驗收 checklist(100% 原寸)

- ☐ 輸出檔實際解析度達標(檔案屬性確認,別信平台標稱)
- ☐ 疊回原圖 50% 透明度:輪廓/地形線完全重合,只有表面細節變豐富
- ☐ 黑區吸管 RGB ≈ 0,0,0(版本 A)/ 霧區依然柔焦(版本 B)
- ☐ 輪廓交界無亮邊 fringe、無糊化
- ☐ 暗部亮度與飽和度未被抬升(對照原圖)
- ☐ 細節是「真的長出來」不是「抹平+銳化」
- ☐ 地面分區還在(綠苔區 vs 土路區沒被均質化)
- ☐ 沒有越界物件(花/蘑菇/動物/頭骨/大石/光束/螢火蟲)

---

## 學到的(可複用結論)

- ✅ **輸入檔比例 = 第一品質變數。** letterbox 白邊連續造成兩種不同災難(假細節+色偏、outpaint 重構圖) — 任何放大/細節工具,輸入一律滿版。
- ✅ **「增加細節」有兩種,prompt 寫法完全不同:** 物件式(允許清單:草葉/枯枝/小石)vs 材質式(表面屬性詞:granularity / roughness variation / damp sheen / AO in crevices)。要 UE5 質感 = 材質式。
- ✅ **定性句 > 禁令堆疊。** 開頭一句「這是材質保真 pass,等於同一塊地的高解析掃描」比一百條 do NOT 有效;禁令當保險。
- ✅ **Universal Upscaler 在滿版輸入 + creativity 最低 + 2× 下可用**;它的抬色調問題是 letterbox 誘發,非本體缺陷。
- ✅ **放大倍率 2× 安全、4× 危險** — sheet 排版時盡量讓單格底圖 ≥2K。
- 📌 **套圖(tileset)延伸:** 四張 tile 同一天、同模型版本、同 prompt 逐字、同參數跑;細節 pass 會動到接縫 → **修縫必須排在細節 pass 之後**(相鄰兩張拼一起只 inpaint 縫帶)。
