---
name: asset-cutout
description: 把概念圖 / AI 生成圖拆成可用的「去背資產」SOP。內含三種去背模式對照(純 matting 零改動 / edit-inpaint 去背+補圖保留原像素 / 重新生成不保留打光)、背景色選擇規則(避開資產既有色)、保留指定顏色(如發光彩窗、霓虹)的鎖句、透明↔純色互轉(棋盤格轉純色)、以及接多視圖 turnaround 的前處理。觸發詞:「去背」「退底」「扣圖」「透明背景」「補圖」「inpaint」「cutout」「拆概念圖出資產」「棋盤格轉純色」「換純色底」「某顏色被去掉 / 要保留某色」「turnaround 前處理」「整包資產去背」。
---

# Asset Cutout SOP — 概念圖拆資產 / 去背 / 補圖

把一張概念圖(或 AI 生成圖)變成乾淨、可重複使用的遊戲/合成資產。核心三問:**要不要保留原始像素?要不要補被遮住的部分?背景要透明還是純色?**

---

## 0. 30 秒決策樹

```
來源圖乾淨、沒被遮、只想去背 ──────────────► 模式 1.0 純 matting(最忠實)
主體被霧/樹/其他物件遮住,要補回缺角 ──────► 模式 1.1 去背 + 補圖(edit/inpaint)
要乾淨、可重打光的全新素材,不在意像素一致 ─► 模式 1.2 重新生成(T2I/extract)

背景色:能透明就透明 → 否則中性灰 #808080 → 真要色鍵才挑「資產缺席色」
要保留的發光色(紫窗/霓虹…):一律加「色彩鎖句」(§4)
```

---

## 1. 表 A — 去背三模式

| 模式 | 動原始像素? | 能補被遮部分? | 保留原打光/顏色? | 推薦工具 | 何時選 |
|---|---|---|---|---|---|
| **1.0 純 matting** | ❌ 零改動 | ❌ 補不了 | ✅ 100% 原樣 | remove.bg / SAM / BiRefNet / rembg / PS「選取主體」 | 來源已乾淨、無遮擋、要最忠實 |
| **1.1 去背 + 補圖(edit/inpaint)** | 只動背景 + 補缺角 | ✅ 合理重建 | ✅ 保留(靠鎖句) | **Flux Kontext** / Seedream edit | 主體被霧/樹/欄杆遮住,要補回 |
| **1.2 重新生成(T2I/extract)** | 全部重畫 | ✅ | ❌ **重打光、可能改色** | Nano Banana Pro / Seedream T2I | 要乾淨可重打光素材,不在意像素一致 |

> 黃金原則:**愈往下,愈方便、但離原稿愈遠。** 能用 1.0 就別用 1.1,能 1.1 就別 1.2。

---

## 2. 表 B — 背景色怎麼挑

**規則:色鍵幕色必須是「資產上完全沒有的顏色」。但現代 AI matting 是語意分割,根本不需要幕色 → 直接透明或中性灰最省事。**

| 背景色 | 用在 | 注意 |
|---|---|---|
| **透明 transparent** | 母檔 / 引擎 | 首選,最有彈性 |
| **中性灰 #808080** | 通用 / turnaround 的 ref | AI matting 無視底色;模型吃純色 ref 比吃透明穩 |
| 純綠 #00FF00 | 主體**無綠**時才行 | 綠苔/植被資產會被挖破 + 綠邊溢色 |
| 純洋紅 #FF00FF | 主體**無洋紅**時才行 | 洋紅/紫光資產會被吃掉 |
| 飽和橘 #FF6A00 | 真要手動色鍵 | 多數冷調資產的缺席色,對比夠;key 時開 spill suppression |

> 範例(哥德陵墓 = 綠苔 + 紫窗):綠幕、洋紅幕**都不能用**(兩色都在資產上)→ 走透明 / `#808080`,真要色鍵才用橘。

---

## 3. 表 C — 保留指定顏色 & 別踩的雷

| ✅ 要做 | ❌ 別做 |
|---|---|
| 明講要保留的色是主體一部分(見 §4 鎖句) | 用模糊動詞 `clean up / remove glow / isolate` → 會把發光色當效果刪掉 |
| edit 模式只下「動什麼、留什麼」指令 | edit 模式貼 `[STYLE]`/長描述 → 觸發重畫,顏色守不住 |
| 一次只改 1–2 件事 | 同一指令塞「去背+補圖+換光+改色」 |
| matting 時開邊緣羽化、**關**「淨化顏色 / Decontaminate Colors」 | 用硬 threshold → 吃掉半透明發光 bloom 邊 |

---

## 4. 可重用積木(複製貼上)

```text
# 色彩鎖句(保留發光彩窗 / 霓虹 / 任何易被當效果刪掉的色)
The glowing <COLOR> <PART> are PART of the subject — preserve their exact
color and emissive glow, do NOT dim, desaturate, recolor, or remove them.
   例:<COLOR>=magenta-purple, <PART>=stained-glass windows

# [BG] 去背用(生成/重畫時)
single isolated object, centered, entire object in frame, soft even neutral
lighting, transparent background, no cast shadow, crisp clean silhouette
edges, alpha-matte ready
   ⮕ 端點不支援透明 → 改 "flat #808080 background";最後才考慮 "flat #FF6A00 background"

# [STYLE] 風格鎖(只用於 1.2 重新生成,整包資產共用以求一致)
stylized-realistic game asset, hand-painted PBR materials, <世界觀/材質/色盤>,
moss lichen and age weathering, matte surface, <藝術方向>
   ⚠️ 不要在 1.0 / 1.1 模式貼這塊

# [ORTHO] 多視圖 turnaround
orthographic turnaround, the SAME object in 4 views on one sheet — front,
3/4 front, side, rear — identical scale, flat even studio lighting, plain
light-gray background, no perspective distortion, modeling reference sheet

# [NEG] 負面
blurry, low quality, watermark, text, duplicated extra objects, perspective
distortion, harsh cast shadows, busy background, oversaturated
```

---

## 5. 各模式現成 prompt

**1.1 — 只去背、主體不動**(來源 = 乾淨圖)
```text
# Flux Kontext (edit)
Remove the background and make it transparent. Keep the entire subject
exactly as-is — do not change its shape, materials, textures, or colors.
<色彩鎖句>. Only the background changes.
```

**1.1 — 去背 + 補圖**(來源 = 被遮的概念圖)
```text
# Flux Kontext / Seedream edit
Keep ONLY the <主體>; remove the fog, trees, and everything else, and make the
background transparent. Where the <主體> is hidden behind fog or branches,
reconstruct the missing parts to complete its silhouette, matching the
surrounding material — do NOT invent new structures. <色彩鎖句>. Keep
everything else unchanged.
```
> Seedream 加分招:在原圖上把主體框起來(bounding box)或塗掉其他區域,它的 visual-cue 編輯會更準。

**1.2 — 重新生成乾淨素材**
```text
# Nano Banana Pro / Seedream T2I — 上傳概念圖當 style ref
Using the attached concept art as style reference, extract ONLY the <主體>:
<關鍵特徵 3-5 個>. [STYLE]. [BG].
```

**1.2b — 正交正視參考板(image-to-3D 用,✅ 實測 2026-06-23 / A1 陵墓)**
```text
# Nano Banana Pro / Seedream — 上傳概念圖
From the attached concept art, extract ONLY the [PROP]. Re-render as one complete,
isolated object, centered and fully visible, front orthographic view, on a flat
neutral grey (#808080) seamless background. Perfectly even diffuse studio lighting,
NO cast shadows, NO rim light, NO scene elements. Maximum sculptural detail.
High-resolution clean reference plate for image-to-3D.
```
> 換 `[PROP]` 即可套任何資產;產出乾淨正視板,直接餵 image-to-3D / concept-to-3D pipeline。要多視圖再接 §4 `[ORTHO]` turnaround。實戰紀錄見 `docs/asset-cases/A1-mausoleum.md`。

---

## 6. 透明 ↔ 純色互轉(棋盤格其實不是圖)

編輯器的**棋盤格 = 顯示「透明」**,PNG 已有乾淨 alpha。墊任何純色都無損,**保留透明 PNG 當母檔**,純色另存。

```bash
# ImageMagick(批量最快)
magick in.png -background "#808080" -flatten out_gray.png
```
```python
# Python / PIL
from PIL import Image
im = Image.open("in.png").convert("RGBA")
bg = Image.new("RGBA", im.size, "#808080")
Image.alpha_composite(bg, im).convert("RGB").save("out_gray.png")
```
- **PS / Photopea / GIMP**:底下加「純色填色圖層」→ 輸出。
- 用途選底:引擎/母檔→**透明**;turnaround 的 ref→**#808080 純灰**;預覽→任意對比色檢查殘邊。

---

## 7. 整套管線

```
概念圖
 └─ 盤點分類(建築 / 道具地面 / 自然地景)
     └─ 每件:選去背模式(1.0 / 1.1 / 1.2)
         └─ 輸出 透明 PNG(母檔) + #808080 灰底版(turnaround ref)
             └─ 多視圖 turnaround([ORTHO],用乾淨灰底 hero 當 ref)
                 └─ 入庫(同一 seed + 同一 [STYLE] 保整包一致)
```

---

## 8. 如何叫用這份 SOP

- 一鍵:輸入 **`/asset-cutout`**,再貼圖。
- 自然語言(會自動觸發):「**照 asset-cutout 的 1.1 模式幫我把這張去背+補圖,保留紫窗**」。
- 指名檔案:「讀 `.claude/skills/asset-cutout/SKILL.md`,用裡面的色彩鎖句處理這張」。
- 去背的「寫對 prompt」細節(各模型簽名/禁忌)以 `ai-media-generator` skill 的 reference 為準。
