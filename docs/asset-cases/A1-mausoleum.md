# 實戰紀錄 — A1 哥德陵墓 Mausoleum

> 概念圖拆資產 / 去背案例。對應工作流:`/asset-cutout`(去背 SOP)+ `ai-media-generator` 的 concept-to-3D pipeline。

## 來源(索引)
- **生成平台:** Google Gemini(Nano Banana Pro)/ Flux Kontext · Seedream edit 思路
- **Gemini 對話連結(⚠️ 私人,僅本人登入可開,連結可能失效 → 真正內容見下方):**
  `https://gemini.google.com/app/c0462b50fd200778`
- **日期:** 2026-06-23
- **原始素材:** 哥德墓園概念圖中的主視覺陵墓

---

## 用到的 prompt(逐字保存)

### 1. 去背 + 補圖(edit/inpaint 思路 + 洋紅背景 + 紫色鎖句)
從原始概念圖抽出陵墓、補回被霧/樹遮住的石材、保留紫窗。
```text
Keep ONLY the gothic mausoleum; remove the fog, trees, fence, gravestones and
everything else, and make the background transparent. Where the mausoleum is
hidden behind fog or branches, reconstruct the missing stone to complete its
silhouette, matching the surrounding weathered stone and roof — do NOT invent
new structures or windows. Strictly preserve the building's original colors and
the glowing magenta-purple stained-glass windows; do NOT dim or desaturate the
purple. Keep everything else unchanged.
```
背景色變體(此資產 = 綠苔+紫窗,只能用缺席色橘):
```text
flat saturated orange #FF6A00 seamless background
（key 時開 spill suppression 抑制溢色)
```

### 2. 正交正視 reference plate(image-to-3D 用，通用 [PROP] 模板)
```text
From the attached concept art, extract ONLY the [PROP]. Re-render as one complete,
isolated object, centered and fully visible, front orthographic view, on a flat
neutral grey (#808080) seamless background. Perfectly even diffuse studio lighting,
NO cast shadows, NO rim light, NO scene elements. Maximum sculptural detail.
High-resolution clean reference plate for image-to-3D.
```

---

## 產出

### 橘底去背版(3/4 視角)
![mausoleum 橘底去背](images/mausoleum-orange-extract.png)

橘底 `#FF6A00`、完整建築含左側角塔 — 驗證「缺席色」去背(綠/洋紅幕都不能用),供手動 key。

### 正視參考板(灰底,image-to-3D 用)
![mausoleum 正視參考板](images/mausoleum-front-ortho.png)

正視角、灰底 `#808080`、對稱 — image-to-3D 正面參考板,由 SOP `1.2b` 模板產出。

---

## 學到的(可複用結論)

- ✅ **橘幕 `#FF6A00` 對「綠苔 + 紫窗」資產成立。** 綠幕吃青苔、洋紅幕吃紫窗,橘是缺席色 → 實測乾淨。印證 asset-cutout SOP「表 B:挑資產缺席色」。
- ✅ **紫色鎖句有效。** 兩張的 magenta 彩窗都完整保留、沒被去飽和。
- ✅ **`front orthographic view + #808080 + clean reference plate for image-to-3D`** 這組詞產出乾淨正視板,很適合接 image-to-3D;`[PROP]` 占位符可重複套到其他資產 → **值得收進 SOP 當標準模板**。
- ⚠️ 這兩張本質是 **重新生成(re-render，模式 1.2)**,不是像素級保留;要原汁原味請改走純 matting。
- ⚠️ 兩張右下角仍有 Gemini **✨ 浮水印**,入庫前裁掉/修掉。
