# 實戰紀錄 — A10 苔蘚草地 + A11 石板路(墓園地面材質)

> 概念圖拆資產案例。延續 [A1 哥德陵墓](A1-mausoleum.md),同一張哥德墓園概念圖的「地面層」。
> 對應工作流:`/asset-cutout`(表 B 背景色 / 平鋪) + `ai-media-generator` concept-to-3D pipeline。
> 兩件皆 **[C] 可複用可平鋪模組** → top-down 平拍 → **轉 PBR 材質(不生 mesh)**。

## 來源(索引)
- **生成平台:** 使用者生成(平台待補 — 推測 Nano Banana Pro / Seedream T2I)
- **日期:** 2026-06-23
- **原始素材:** 哥德墓園概念圖的地面 — 石板路(A11) + 苔蘚草地(A10)
- **墓園資產進度:** A1 陵墓 ✅(見 `A1-mausoleum.md`)· **A10 ✅ · A11 ✅** · 其餘(A2–A9)待做

---

## 用到的 prompt(逐字保存)

### A11 — 石板路 / 鵝卵石鋪面(top-down 無縫平鋪)
```text
Top-down orthographic flat texture tile derived from the cobblestone/flagstone path in
the attached concept art: perfectly SEAMLESS and TILEABLE on all 4 edges, square 1:1,
shot straight from directly above, zero perspective, even diffuse light, NO directional
shadow, NO baked highlight, NO purple/green scene tint (true de-lit albedo). Irregular
weathered stone slabs with moss in the cracks and dirt in the joints, scale matches a
1m x 1m module, flat albedo suitable as a PBR base color map.
```

### A10 — 苔蘚草地(top-down 平鋪)
```text
Top-down orthographic flat texture tile derived from the mossy grass ground in the
attached concept art: perfectly SEAMLESS and TILEABLE on all 4 edges, square 1:1, shot
straight from directly above, zero perspective, even diffuse light, NO directional
shadow, NO baked highlight, NO green scene tint (true de-lit albedo). Mossy turf with
grass blades, small weeds and dirt, scale matches a 1m x 1m module, flat albedo
suitable as a PBR base color map.
```

---

## 產出

### A11 石板路材質 tile
![cobblestone path tile](images/cobblestone-path-tile.png)
> ⏳ 待存入 `images/cobblestone-path-tile.png`(同 A1 流程:先存文字紀錄,成品圖另一 commit 同步)

top-down、灰/赭不規則石板、縫隙嵌苔 — 對應概念圖石板路材質。

### A10 苔蘚草地材質 tile
![mossy ground tile](images/mossy-ground-tile.png)
> ⏳ 待存入 `images/mossy-ground-tile.png`

top-down、真綠 albedo、苔塊 + 草葉 + 酢漿草 + 枯枝 + 碎石 + 泥土 — 對應概念圖地被層。

---

## QC(對照 pipeline「進 3D 前 QC 檢查表」)

| 檢查項 | A11 石板路 | A10 苔蘚草地 |
|---|---|---|
| top-down 正交、零透視 | ✅ | ✅ |
| de-lit(無投影 / 無 rim / 無景深) | ✅ | ✅ |
| 去除概念圖綠霧/紫光染色 → 真 albedo | ✅(灰/赭中性) | ✅(真綠,未被場景光染) |
| 內容對應原圖 | ✅ 風化石板 + 縫苔 | ✅ 苔+草+酢漿草+枝石 |
| 四邊無縫平鋪 | ⚠️ 待引擎 offset 驗 | ⚠️ 待引擎 offset 驗 |
| 巨觀亮度均勻(避免平鋪鬼影) | ⚠️ 略有明暗大塊 → 需 flatten | ✅ 大致均勻 |
| 浮水印 / 邊角 | 入庫前檢查右下角 | 入庫前檢查右下角 |

---

## 學到的(可複用結論)

- ✅ **`top-down orthographic flat texture tile … SEAMLESS and TILEABLE on all 4 edges … NO baked highlight … true de-lit albedo … PBR base color map`** 這組詞對 [C] 平面類資產有效,產出可直接當 base color → **值得收進 SOP 當「地面/牆面材質」標準模板**。
- ✅ **`NO purple/green scene tint` 是關鍵句。** 把概念圖的綠霧 / 紫光擋在門外,拿到中性 albedo;少了這句,地面會被烤上場景色,平鋪時整片偏綠/偏紫。
- 📌 **[C] 平面類的產出是「材質貼圖」,不是 mesh。** 下一步在 Substance/引擎派生 normal + height + roughness + AO;石板縫苔可轉 mask 驅動程序化苔蘚。
- ⚠️ **A10 草葉是「畫進平面」的。** 當純地面 albedo OK,但俯視是平的;要立體草 / 酢漿草請改用 **scatter 卡片(geometry)疊在地面上**,別靠烤進貼圖的草葉 —— 呼應 pipeline「地/毯/草別硬建模 → PBR + scatter」。
- ⚠️ **平鋪前先 flatten 巨觀亮度。** A11 有明暗大塊,直接平鋪會出現重複鬼影;高通 / de-light 壓平 albedo 後再拼。
- ⚠️ **入庫前檢查右下浮水印**(沿用 A1 的 Gemini ✨ 經驗),裁掉/修掉再進材質庫。

---

## PBR 派生 — 從 base 出 7 張貼圖(以 A11 石板路示範)

> [C] 平面類資產的下一步:base color 有了 → 派生整套 PBR map 進引擎。
>
> **兩條路:**
> - **(A) 推薦 — 派生:** base 丟 **Substance Sampler「Image to Material」/ Materialize(免費)/ DeepBump**,normal/height/AO 用實際高低落差「算」出來,跟 base 100% 對齊,比文生圖準。
> - **(B) txt2img:** img2img 餵 base、**denoise 0.2–0.35(對齊命脈,別調高)**、1:1、seamless 開、固定 seed。下列 7 段為 (B) 的逐字提示詞。

### 1. BASE COLOR(albedo)✅ — 洗乾淨、壓平巨觀明暗
```text
Refine the attached cobblestone tile into a clean PBR BASE COLOR / albedo map: remove
ALL baked lighting, cast shadows, ambient occlusion and specular highlights; flatten to
even de-lit diffuse albedo. Keep the true stone hues (grey, tan, ochre) and the green
moss in the joints. EVEN macro luminance — no light/dark patches that repeat when tiled.
Seamless and tileable on all 4 edges, square 1:1, zero perspective. Color/sRGB texture.
```

### 2. NORMAL(tangent-space)⚠️ 建議改用 height 派生(DeepBump / NormalMap-Online)
```text
Tangent-space NORMAL map for the attached cobblestone tile, aligned pixel-for-pixel.
Predominantly blue-violet (base RGB ~128,128,255); RED channel encodes left-right slope,
GREEN channel encodes up-down slope; rounded stone tops bulge outward, mortar joints,
cracks and moss gaps recess inward. OpenGL convention (green = +Y up). NO baked color,
NO lighting, NO AO, NO shadows. Seamless tileable, square 1:1. Non-color data map.
```
> 引擎:UE 用 **DirectX(Y-)** → 反轉綠通道;Unity/Blender 用 **OpenGL(Y+)** 直接用。

### 3. HEIGHT / DISPLACEMENT ✅
```text
HEIGHT / DISPLACEMENT map for the attached cobblestone tile, grayscale, aligned
pixel-for-pixel. Raised stone tops = white/light; mortar joints, cracks and moss gaps =
black/dark; smooth tonal falloff over each stone's rounded curvature. Pure grayscale, NO
color, NO lighting, NO cast shadows. Seamless tileable, square 1:1, 16-bit, non-color data.
```

### 4. ROUGHNESS ✅ — 乾石/苔 0.85、磨光/潮濕 0.5–0.6、泥縫 0.8
```text
ROUGHNESS map for the attached cobblestone tile, grayscale, aligned pixel-for-pixel.
Dry porous stone and moss = light grey (high roughness ~0.85); worn/polished stone tops
and damp spots = mid-dark grey (lower ~0.55); dirt and mortar = mid-high grey (~0.8).
NO hue, NO lighting, NO highlights. Seamless tileable, square 1:1, linear non-color data.
```

### 5. METAL(metallic)= 常數,**別生** → 整張純黑 0.0
```text
METALLIC map for a stone path = SOLID PURE BLACK (0.0) across the entire tile — stone,
moss and dirt are all non-metallic dielectrics. Flat black, no texture. Square 1:1,
linear non-color data.
```

### 6. SPECULAR = 看工作流,多半**不出 map**
- **Metal/Rough(UE5/Unity/glTF/Blender):沒有 specular 貼圖**,引擎內 Specular 純量留預設 **0.5**(=F0 0.04)。
- **Spec/Gloss(舊工作流)才需要**,石材 = 近乎均勻深灰 `#2E2E2E`(linear 0.04):
```text
SPECULAR (F0/reflectivity) map for the attached stone path: near-uniform very dark grey
(~sRGB #2E2E2E, linear 0.04 dielectric), with faint darkening in porous moss/dirt and a
slight lift on polished stone tops. NO color, NO lighting. Seamless tileable, square 1:1,
linear non-color data.
```

### 7. AMBIENT OCCLUSION(AO)✅(⚠️ 最好也用 height 派生)— 凸頂白 1.0、苔縫/裂縫最暗 ~0.3–0.5
```text
AMBIENT OCCLUSION map for the attached cobblestone tile, grayscale, aligned
pixel-for-pixel. Exposed raised stone tops = white (no occlusion); deep mortar joints,
cracks and moss-filled gaps between stones = soft dark grey (occluded ambient light).
Soft contact-occlusion only — NO directional lighting, NO cast shadows, NO color, NO
highlights. Seamless tileable, square 1:1, linear non-color data map.
```

### 📊 通道 / 色彩空間速查(裝進引擎別搞錯)
| Map | 色彩空間 | 重點 |
|---|---|---|
| Base Color | **sRGB** | 唯一的 color 圖 |
| Normal | Linear(raw) | OpenGL Y+;UE 反轉綠通道 |
| Height | Linear(raw) | 驅動 displacement / parallax |
| Roughness | Linear(raw) | 石 0.7–0.9 |
| Metallic | Linear(raw) | **= 黑 0** |
| Specular | Linear(raw) | metal/rough 不出圖;spec/gloss → #2E2E2E |
| AO | Linear(raw) | 柔和遮蔽,非方向陰影 |

### 📦 ORM 打包(UE5 / glTF 省記憶體)
把三張灰階塞進一張 RGB:**R = AO ·　G = Roughness ·　B = Metallic(=全黑 0)** → 合成 `T_cobble_ORM`,引擎直接吃。

### 共用 negative + img2img 參數
```text
# negative
color tint, hue, baked lighting, cast shadows, highlights, ambient occlusion,
perspective, bevel, vignette, visible seams, misaligned, blurry, watermark, text
```
- 餵 A11 albedo 當輸入 · **denoise 0.2–0.35(對齊命脈)** · 1:1 · seamless/tileable 開 · 固定 seed · 灰階圖若被加色 → 事後去飽和。

### 可靠度結論
- ✅ height / roughness / AO / base 用 txt2img img2img 可用。
- ⚠️ **normal / AO 最準是從 height 派生**(Substance / Materialize / DeepBump 用真實高低落差算)。
- 🚫 **metal = 純黑常數,別燒圖;specular 在 metal/rough 根本不出 map**(留純量 0.5)。
