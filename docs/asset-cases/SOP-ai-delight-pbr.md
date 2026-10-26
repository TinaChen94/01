# SOP — AI 去光 → PBR 整套貼圖(de-light → PBR maps)

> **叫用詞:** 使用者說「AI PBR」「去光出 PBR」「做整套貼圖」「照 AI PBR 配方」即指此 SOP — 先讀本檔再動手。
> **用途:** 把一張**帶打光的材質/場景圖**轉成**不受光的 PBR 整套貼圖**(base / height / normal / roughness / metallic / AO),之後導入 Blender / 引擎**重新打光**。
> **對應工作流:** `ai-media-generator`(de-light / concept→3D / 重打光)+ A10/A11(PBR 派生)+ A2(去光鐵律)。
> **平台:** [Leonardo.ai](https://app.leonardo.ai/),Image2Image + Nano Banana 2。程序派生工具在 [`tools/pbr-derive/`](../../tools/pbr-derive/)。

---

## 0. 先分型(決定做法與「重打光」成不成立)

| 類型 | 例 | 特徵 | 重打光品質 | seamless |
|---|---|---|---|---|
| **場景板(scene plate)** | 哥德壁龕牆、交叉肋拱頂 | 深度落差大(凸雕/深龕/退縮) | 平板+displacement 只反應表面起伏;**深凸凹不會真自遮蔽**,要真幾何(concept→3D 出 mesh)才自然 | **關**(不是 tile) |
| **可平鋪材質(tileable)** | 方石地板 | 近平面、要四方連續 | 平板+normal/height 就夠 | **開** |

> **鐵律:** 場景板若要石像鬼/深龕**真的擋光投影**,平面 PBR 給不了 → 走 concept→3D 出 mesh 再烘。平面 PBR 是「快、夠用」路線,下面配方兩型通用,差別只在 **seamless 開關** 與 **height 語義**。

---

## 1. 平台固定設定(Leonardo,每一格都一樣)

- 上傳**來源圖滿版、無 letterbox**;輸出 **Dimensions 比例 = 輸入比例**(多為 1:1)
- **Image2Image / Image Guidance 開**,**Model/Platform = Nano Banana 2**
- **Prompt Enhance = None、Style = None**
- **Creativity / Strength 最低段(≈0.2–0.35)** — 對齊命脈,別高
- tileable 類:**Tiling / Seamless 開**;場景板:關
- 灰階圖(height/rough/AO/metallic)若被加色 → 事後 PS 去飽和

---

## 2. Step 1 — 去打光(de-light → 真 albedo)

**image-grounded 鐵律(A2):餵原圖,絕不用純文字重述物件。** 文字只寫「要刪什麼光」。

### 2.1 「列點刪 > 泛詞否定」(A2 最大教訓)
`NO scene elements` / `remove lighting` 這類泛詞**只會被執行一半**。必須**逐項點名**要刪的光源與現象。常見「4 大殺手」:
1. 點燃光源(蠟燭/壁燈)的**火光 + 暖溢光**(→ 寫 `unlit dark metal` 把燈具變死物)
2. 冷色**背光 / rim**(窗光)
3. 深凹處的**投影 / AO**
4. 四周 / 底部的**暗角 vignette**;場景整體的**明暗漸層**

### 2.2 去光模板(填 `[ASSET]` / `[刪除清單]` / `[保色或中性化]`)
```text
From the attached image, keep the [ASSET] EXACTLY as-is (all geometry, proportions,
layout, carvings — unchanged), but fully DE-LIGHT it into a true flat albedo plate.
Remove ALL baked lighting: [逐項點名:火光+暖溢光 / 冷藍rim / 深凹投影+AO / 暗角vignette /
明暗漸層]. Re-render with perfectly even, flat, shadowless diffuse light so every surface
reads its own true de-lit color — [保色: keep the warm X hue  |  中性化: neutralize to
true neutral cool-grey stone, no warm tint]. NO cast shadows, NO rim light, NO glow, NO
vignette, NO color tint. [場景: head-on frontal orthographic | tileable: top-down ortho,
SEAMLESS and TILEABLE on all 4 edges]. Square 1:1, zero perspective. Clean de-lit albedo
plate for PBR.
```
- **保色 vs 中性化**:暖色材質(暖褐拱頂)若要保個性 → 保色;若要跟冷灰場景同用 → 中性化(negative 加擋 `brown/sepia/warm`)。
- **殘留暖光補刀 pass**:`Edit this plate: neutralize the remaining warm cast around both sconces to match the neutral stone; extinguish both flames, keep the fixtures as unlit metal.`

### 2.3 去光驗收(過了才進 Step 2 —— A2「別盲生」)
疊回原圖比**剪影/比例沒漂** · 暖/冷色偏**中性化** · 烤光影攤平 · tileable 類**巨觀亮度均勻**(否則平鋪鬼影)。

---

## 3. Step 2 — 出 PBR 整套貼圖

### 3.1 兩條共通鐵律
- **對齊鎖(每格開頭必加):** `Convert the attached image into a [MAP] map. Keep every element in the EXACT same position and scale, aligned pixel-for-pixel; do NOT move, add, remove, crop or redraw anything; only replace surface values.`
- **擋 albedo 汙染(height/AO 必加):** 明講「亮度只看**形狀/凹凸**,不看石頭本身深淺色」。否則深色石會被誤讀成凹陷。

### 3.2 各 map 模板

**① BASE COLOR** = 去光板洗淨(攤平巨觀明暗 + **抬黑位**,縫不留純黑,sRGB)。
> 偏黑/死黑是 A10 踩過的坑:勾縫 sRGB 若=0,進引擎疊 AO/法線自陰影會**雙重變黑**。抬到 ≥40。

**② HEIGHT / DISPLACEMENT**(決定重打光吃不吃深度,**先跑這張,normal 靠它派生**)
```text
...Pure grayscale. Base brightness ONLY on how far each element PROTRUDES from/RECEDES into
the surface — NOT on the stone's own light/dark color (a dark stone in front stays BRIGHT, a
pale surface deep in a recess stays DARK). [場景: 凸雕/柱=最亮, 平牆=中, 深龕/窗=最黑 |
tileable 硬地板: FLAT uniform block tops, crisp chamfer then STEEP near-vertical drop into
BLACK joints]. NO color, NO lighting, NO cast shadows, NO albedo detail.
```
> **軟/硬 height**:寫 `rounded curvature` → **枕頭軟邊**(石頭像氣墊,通常不要);要**堅硬切石地板** → `FLAT block top + steep near-vertical drop + sharp chamfer`,negative 擋 `rounded/pillow/inflated/soft edges`。

**③ ROUGHNESS**:材質分級 — 風化石 ~0.85、磨光/潮 ~0.55、金屬件 ~0.4、玻璃 ~0.15;加對齊鎖 + `ignore tonal shading, base on material only`。

**④ METALLIC**:**別燒圖當常數**。
- 純石材(拱頂/地板)= **整張純黑 0** → 程序生或 PS 填黑,不花額度。
- 有金屬件(壁燈)= **hard mask**:石=黑、鐵件=白,無漸層。

**⑤ AMBIENT OCCLUSION**:凸面/塊頂=白,深龕/縫/裂/角=暗;加 `base on geometric cavities ONLY, IGNORE tonal shading already painted`。

**⑥ NORMAL** → **別用生成式,從 ②height 派生**(見 §4 重點教訓)。

**⑦ SPECULAR** → metal/rough 工作流**不出**(引擎純量 0.5)。

### 3.3 跑法(別盲生)
先只跑 **②HEIGHT** 反覆到滿意(凸凹對、軟硬對、無 albedo 汙染)→ 再 ③⑤ 各自獨立 → ⑥normal 從 height 派生 → ④metallic 程序生 → 打包 ORM。

---

## 4. 🔴 關鍵教訓(血淚實證)

### 4.1 NORMAL 一律從 HEIGHT 派生,別用生成式(本案最大教訓)
生成模型**是「畫」顏色、不是「算」梯度**,給不出物理正確的法線向量場。地板 normal **連燒三張全錯**:
1. **塊頂偏紫**(非精準 128,128,255);
2. **邊緣紅綠方向不一致**(同塊四邊配色亂)→ 打光各邊反光矛盾;
3. **縫是黑的**(照抄 height 黑縫)——**normal 不該有任何黑**,黑=向量 (0,0,0) 無效;縫底其實也是朝上的藍,只有**側壁**是紅綠。
> **正解:** 用乾淨 height 跑 [`tools/pbr-derive/height_to_normal.py`](../../tools/pbr-derive/height_to_normal.py) → 數學算的,平面精準 (128,128,255)、邊緣方向一致、**OpenGL + DirectX 兩版**都給、跟 height 100% 對齊。硬邊地板把 `--blur` 壓到 0.3 保銳利。
> 生成式 normal 的驗收(真要燒):平面接近純藍、**無黑**、邊緣紅綠方向一致;偏紫/亂/有黑 = 失敗。

### 4.2 顏色只動 base color,其他 5 張看「形狀」
height/normal/roughness/metallic/AO 只由**形狀與材質**決定,**與 albedo 深淺無關**。所以:
- 調亮/調色/換色盤 → **只需重做 base**,其他 5 張不用重做;
- 生 height/rough/AO 時用深版或淺版當來源**結果一樣**(但**淺版/明暗分得開的當來源更好讀**,模型較不會把深色誤判成凹陷)。

### 4.3 配同場景色盤用 Match Color,別靠生圖形容詞(「太白」坑)
把暖褐拱頂調成跟冷灰牆同一套時,生圖重調色容易**過白**(明度沒對上)。**明度是統計量**,生圖靠形容詞壓不準 → 用 **Match Color 程序移植**(lab 均值/標準差把牆的明度直接搬過來),一次到位、零幾何漂移。

### 4.4 其他
- **抬黑位**:去光板勾縫別留純黑(程序:homomorphic 攤平 + 反除 AO + 黑位下限 sRGB 48)。
- **t2i height ≠ 真深度**(A2):正式位移從 3D 網格烘;平面 PBR 用它驅動 displacement 堪用。

---

## 5. 導入 Blender / 引擎 — 接線 + 踩坑

**接線**:base→Base Color(**sRGB**);normal→`Normal Map`→Normal;height→`Displacement`→Material Output Displacement;roughness→Roughness;metallic→Metallic;AO→(選)`MixRGB` Multiply **Fac 0.3–0.5** 進 Base Color。**灰階圖全設 `Non-Color`。**

**踩坑速查(本案實拍抓到的):**

| 症狀 | 元凶 | 修 |
|---|---|---|
| **石頭暗+悶、肋/塊邊假高光爆白** | **Metallic = 1.0**(石頭被當金屬!) | Metallic 設 **0** 或接純黑 metallic 貼圖 |
| 磚面悶、髒、死黑 | **AO 重複相乘**(base 已去光又全乘 AO,引擎再算一次) | AO 別全乘進 base;Fac 降 0.3,或只走間接光 |
| 整體偏暗壓灰 | Blender **AgX** View Transform | 改 **Standard** 或 Exposure +0.5~1 |
| 凸起看起來凹進去 | **normal 綠通道慣例反**(OpenGL/DirectX) | normal 後 `Separate Color`→G `Invert`→`Combine`;UE 用 `-normal-dx.png` |
| height 沒真凸 | 沒開真位移 | 材質 `Settings→Surface→Displacement: Displacement Only` + 物件 Subdivision |
| 邊緣太硬/太軟 | Normal Map **Strength** | 調 0.6–1.0 |

**色彩空間速查:** Base=**sRGB**;Normal/Height/Roughness/Metallic/AO=**Non-Color(Linear)**。**ORM 打包:** R=AO / G=Roughness / B=Metallic。

---

## 6. 三個 worked example(實證·含 Leonardo 連結)

### B-wall — 哥德壁龕牆([B] 場景板,冷灰,有金屬壁燈)
深浮雕場景,中「4 大殺手」全餐。PBR 全套 ✅(metallic 教科書級:石黑+鐵壁燈白)。normal 待從 height 派生(生成版 512+慣例未知)。

**成品圖(repo 內嵌):**

| 素材(帶光) | base color(去光) | height |
|---|---|---|
| ![source](images/gothic-wall-01-source.jpg) | ![basecolor](images/gothic-wall-04-basecolor.jpg) | ![height](images/gothic-wall-06-height.jpg) |

| normal | roughness | metallic | AO |
|---|---|---|---|
| ![normal](images/gothic-wall-07-make-normal.jpg) | ![roughness](images/gothic-wall-09-make-roughness.jpg) | ![metallic](images/gothic-wall-11-make-metallic.jpg) | ![ao](images/gothic-wall-13-make-ao.jpg) |

**原圖連結(Leonardo):** 去光 · [HEIGHT](https://app.leonardo.ai/generation/image/height-displacement-map-attached-gothic-wall-plate-685613c6-d7ea-4735-bf68-454b594e92ee) · [NORMAL](https://app.leonardo.ai/generation/image/convert-attached-grayscale-height-map-into-tangent-abffc0d0-42a9-488b-affc-9182e7939c81) · [ROUGHNESS](https://app.leonardo.ai/generation/image/roughness-map-attached-gothic-wall-plate-grayscale-cd7b90d3-c443-4da4-afb0-432062445605) · [METALLIC](https://app.leonardo.ai/generation/image/metallic-map-attached-gothic-wall-plate-solid-ea81db84-d126-42da-b8fe-842bf9acc70f) · [AO](https://app.leonardo.ai/generation/image/ambient-occlusion-map-attached-gothic-wall-plate-e004a405-b4bd-499d-b1dd-f8a0168e0791)

### B-ceiling — 交叉肋拱頂([B] 場景板,暖褐/灰石兩版,無金屬)
去光出**暖褐 + 中性灰**兩版(同場景用選灰)。metallic = 純黑。

**成品圖(repo 內嵌):**

| 素材(帶光) | 去光·暖褐 | 去光·灰石(採用) |
|---|---|---|
| ![source](images/vault-14-source.jpg) | ![delit-brown](images/vault-15-delit-brown.jpg) | ![delit-grey](images/vault-16-delit-grey.jpg) |

| height | normal | roughness | AO |
|---|---|---|---|
| ![height](images/vault-19-height.jpg) | ![normal](images/vault-20-make-normal.jpg) | ![roughness](images/vault-22-make-roughness.jpg) | ![ao](images/vault-24-make-ao.jpg) |

**原圖連結(Leonardo):** [去光·暖褐](https://app.leonardo.ai/generation/image/attached-vaulted-ceiling-image-keep-architecture-d39ced0b-b48c-40c9-aee6-d421b2e1e542) · [去光·灰石](https://app.leonardo.ai/generation/image/attached-vaulted-ceiling-image-keep-architecture-8d490406-018e-4e46-b9b6-a5b2e2389904) · [HEIGHT](https://app.leonardo.ai/generation/image/convert-attached-image-into-height-displacement-e27e9371-9f8e-4d4a-b07d-960f82ec2068) · [NORMAL](https://app.leonardo.ai/generation/image/convert-attached-grayscale-height-map-into-tangent-2ceb20e5-36b3-4c53-b8e0-7330a6e067d8) · [ROUGHNESS](https://app.leonardo.ai/generation/image/convert-attached-image-into-roughness-map-bb5bd918-1384-480c-8ae7-bf3468dea20c) · [AO](https://app.leonardo.ai/generation/image/convert-attached-image-into-ambient-occlusion-map-5f775332-7f36-4a79-a81c-9c5053109196)

### B-floor — 方石地板([C] tileable,seamless,無金屬)
tileable 材質。去光 → **提亮** → height **軟邊失敗 → 改硬邊切石**(flat top+steep drop)→ normal **生成三連敗 → 從 height 派生才對**。

**成品圖(repo 內嵌):**

| 素材(帶光) | base color(去光+提亮) | height ✅硬邊 |
|---|---|---|
| ![source](images/floor-25-source.jpg) | ![basecolor](images/floor-27-basecolor-light.jpg) | ![height](images/floor-30-make-height-hard.jpg) |

| normal | roughness | AO |
|---|---|---|
| ![normal](images/floor-34-make-normal-fixed.jpg) | ![roughness](images/floor-36-make-roughness.jpg) | ![ao](images/floor-38-make-ao.jpg) |

**失敗反例(存證):**

| ❌ height 太軟(枕頭感) | ❌ 生成 normal 有黑縫(無效向量) |
|---|---|
| ![height-soft](images/floor-28-make-height-soft.jpg) | ![normal-bad](images/floor-33-make-normal-bad.jpg) |

> metallic = 純黑(無金屬件)。`floor-34` 為生成式「禁黑」normal;**定版 normal 建議從 `floor-30` 硬 height 用 `tools/pbr-derive/height_to_normal.py` 派生**。

**原圖連結(Leonardo):** [去光](https://app.leonardo.ai/generation/image/attached-stone-tile-texture-keep-every-block-crack-558d8a8f-864d-4a0f-98af-15723f201a96) · [HEIGHT·軟邊失敗](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-height-4adb440c-ac86-48a7-91a4-9f26d2db4c68) · [HEIGHT·硬邊✅](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-height-f289844a-6b64-4b89-a53f-06020f17e364) · [NORMAL·禁黑版](https://app.leonardo.ai/generation/image/convert-attached-height-map-into-tangent-space-779abb84-6e15-4fa5-8f56-2fe37eb820ed) · [ROUGHNESS](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-roughness-a7c0ad58-03ae-4c3c-b14b-0f72e485a790) · [AO](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-ambient-4d7a68b1-d470-4e9b-ac36-7db80dd31189)

---

## 7. 程序工具([`tools/pbr-derive/`](../../tools/pbr-derive/))

- **`height_to_normal.py`** — height → normal(**OpenGL + DirectX 兩版**,梯度算、附 QC 平均值);`--strength` 控強度、`--blur` 控銳利(硬邊用 0.3)。
- **`derive_pbr.py`** — 去光 albedo → 整套(洗淨 base + height + normal + roughness + metallic + AO + ORM 打包);含 `clean_albedo()`(攤平+抬黑位)、擋 albedo 汙染。

```bash
python3 tools/pbr-derive/height_to_normal.py <height>.png --outdir <dir> --prefix <name> --strength 2.5 --blur 0.3
```

---

## 8. 待補(TODO)

- [x] 三案**成品圖入庫** `images/`(`gothic-wall-*` 1-13 / `vault-*` 14-24 / `floor-*` 25-38),三案 worked example 皆已內嵌成品圖庫 + 失敗反例。
- [ ] 三案 normal **程序派生定版**(取代生成版,從各案硬 height 跑 `height_to_normal.py`),各附 QC 平均值。
- [ ] B-floor **四方連續驗縫**(offset 半格)+ 引擎 3×3 驗收。
- [ ] B-wall 若走 concept→3D:補 3/4 掠射視圖 + image-to-3D 出 mesh 流程。
- [ ] B-ceiling 暖→灰 **Match Color 程序版**(治「太白」)留檔。
- [ ] 把 §3.2 各 map 模板收進 `ai-media-generator` skill 當標準片段。

---

## 9. 逐字 prompt 全集 + Leonardo 結果(三案實跑存檔)

> 三案在 Leonardo(Image2Image / Nano Banana 2 / Prompt Enhance·Style = None / Creativity 最低)實跑的**逐字 prompt**,每段配**它自己的 Leonardo 結果連結**。通用模板見 §3.2。

---

### 9.1 B-wall 哥德壁龕牆(場景板,seamless 關)

**① 去光 de-light** → [Leonardo 結果](https://app.leonardo.ai/generation/image/attached-image-keep-architecture-exactly-all-68c69df7-895e-49c7-bdf0-0ae4c221abbd)
```text
From the attached image, keep the architecture EXACTLY as-is (all geometry, proportions,
layout, carvings, the two gargoyle statues, the pointed-arch tracery window, the balustrade
— unchanged), but fully DE-LIGHT it into a true flat albedo plate. Remove ALL baked lighting:
the two lit wall-sconce flames and their warm orange glow and cast light on the surrounding
stone; the cool blue light and rim glow from the window; every cast shadow and ambient-
occlusion darkening inside the niches, arches and recesses; and the dark vignette at the edges
and floor. Re-render with perfectly even, flat, shadowless diffuse studio light so every
surface reads its own true de-lit color — neutral cool-grey weathered gothic stone, the iron
sconce fixtures as unlit dark metal, the window tracery and glass as their own base tones. NO
cast shadows, NO rim light, NO warm or blue color tint, NO glow, NO vignette, NO flames. Head-
on frontal orthographic, zero added perspective. Clean high-resolution de-lit albedo plate for
PBR / image-to-3D.
```
殘留暖光補刀 pass(A2 §4 做法):
```text
Edit this plate: neutralize the remaining warm cast on the stone around both sconces to match
the neutral grey stone elsewhere; extinguish both candle flames, keep the iron sconce cups as
unlit metal.
```

**② HEIGHT / DISPLACEMENT** → [Leonardo 結果](https://app.leonardo.ai/generation/image/height-displacement-map-attached-gothic-wall-plate-685613c6-d7ea-4735-bf68-454b594e92ee)
```text
HEIGHT / DISPLACEMENT map of the attached gothic wall plate, grayscale, aligned pixel-for-
pixel. Encode real depth: the two gargoyle statues and their corbels projecting forward =
brightest; pilasters, sconces and balustrade = mid-high; the flat wall face = mid-grey; the
arched niches, recessed tracery window and all deep recesses = darkest. Smooth tonal gradient
following true depth. Pure grayscale, NO color, NO lighting, NO cast shadows.
```

**③ NORMAL(從 height)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-grayscale-height-map-into-tangent-abffc0d0-42a9-488b-affc-9182e7939c81)
```text
Convert the attached grayscale HEIGHT map into a tangent-space NORMAL map, aligned pixel-for-
pixel — keep every element in the EXACT same position and scale, do NOT move, redraw, add or
crop anything; only translate height into surface normals. Interpret the input as elevation:
BRIGHT = raised toward the viewer, DARK = recessed. Output a tangent-space normal map that is
predominantly blue-violet (flat areas ≈ RGB 128,128,255); the RED channel encodes left-right
slope, the GREEN channel encodes up-down slope; every raised edge and rounded form bulges
outward, every recess, groove and niche edge slopes inward, following the height gradients.
OpenGL convention (green = +Y, up). NO albedo, NO color tint, NO lighting, NO cast shadows, NO
ambient occlusion. Square 1:1, same framing, zero perspective. Non-color data map.
```

**④ ROUGHNESS** → [Leonardo 結果](https://app.leonardo.ai/generation/image/roughness-map-attached-gothic-wall-plate-grayscale-cd7b90d3-c443-4da4-afb0-432062445605)
```text
ROUGHNESS map of the attached gothic wall plate, grayscale, aligned. Weathered matte stone and
moss = light grey (high ~0.85); polished stone edges and damp spots = mid grey (~0.55); the
iron sconce metal = darker grey (~0.4); the window glass = dark (~0.15). NO hue, NO lighting,
NO highlights.
```

**⑤ METALLIC** → [Leonardo 結果](https://app.leonardo.ai/generation/image/metallic-map-attached-gothic-wall-plate-solid-ea81db84-d126-42da-b8fe-842bf9acc70f)
```text
METALLIC map of the attached gothic wall plate: SOLID BLACK (0.0) for all stone, statues,
tracery and glass; PURE WHITE (1.0) only on the two iron/bronze wall-sconce fixtures. Hard-
edged mask, no gradient, no lighting, no color.
```

**⑥ AMBIENT OCCLUSION** → [Leonardo 結果](https://app.leonardo.ai/generation/image/ambient-occlusion-map-attached-gothic-wall-plate-e004a405-b4bd-499d-b1dd-f8a0168e0791)
```text
AMBIENT OCCLUSION map of the attached gothic wall plate, grayscale, aligned. Exposed forward
faces (gargoyle tops, pilaster fronts, wall face) = white; deep arched niches, recessed window
bay, corbel undersides and tight crevices = soft dark grey. Soft contact occlusion only, NO
directional light, NO cast shadows, NO color.
```

**全套 QC:**

| Map | 判定 | 備註 |
|---|---|---|
| ① base color | ✅ | 去光板 |
| ② HEIGHT | ✅ 讚 | 石像鬼/柱前凸亮、壁龕/窗深黑,凸凹對 |
| ③ ROUGHNESS | ✅ 堪用 | 石材高糙(淺)+ 縫略暗;要確認鐵壁燈/玻璃有無壓暗 |
| ④ METALLIC | ✅✅ 完美 | 純黑 + 只兩支鐵壁燈=白,教科書級 |
| ⑤ AO | ✅ | 凸面白、壁龕/凹縫暗;略帶 render 感但可用 |
| ⑥ NORMAL | ✅(待派生定版) | 生成版 512 + 慣例未知 → 建議從 ②height 用腳本派生 |

---

### 9.2 B-ceiling 交叉肋拱頂(場景板,seamless 關)

**① 去光 — 暖褐版(保色)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/attached-vaulted-ceiling-image-keep-architecture-d39ced0b-b48c-40c9-aee6-d421b2e1e542)
```text
From the attached vaulted-ceiling image, keep the architecture EXACTLY as-is (all geometry,
proportions, layout, the X-crossing ribs, the central and corner carved rosette bosses, and
the brick coursing — unchanged), but fully DE-LIGHT it into a true flat albedo plate. Remove
ALL baked lighting: the overall light-to-dark shading gradient across the vault (bright center
fading to dark edges), the dark vignette and shadowed gradients in the four corners where the
vault curves away, every baked highlight and cast shadow on the ribs and bosses, and the
ambient-occlusion darkening along the sides of every rib. Re-render with perfectly even, flat,
shadowless diffuse light so every surface reads its own true de-lit color — keep the warm brown
sandstone hue of the stone and ribs as their own flat albedo, uniform brightness edge to edge.
NO shading gradient, NO vignette, NO cast shadows, NO highlights, NO ambient occlusion, NO
color-temperature shift. Flat top-down orthographic, square 1:1, zero perspective. Clean high-
resolution de-lit albedo plate for PBR.
```
negative:`lighting gradient, vignette, cast shadows, highlights, ambient occlusion, baked light, directional light, perspective, blurry, watermark, text`

**① 去光 — 灰石版(中性化)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/attached-vaulted-ceiling-image-keep-architecture-8d490406-018e-4e46-b9b6-a5b2e2389904)
> 同暖褐版,`keep the warm brown hue` 換成 → `ALSO neutralize the warm brown color grade: convert the stone to true neutral cool-grey gothic stone (no brown, no sepia, no warm tint), the ribs a slightly darker neutral grey.`
> negative 加:`brown tint, sepia, warm color cast`。
> 選版:要跟 B-wall(冷灰)同場景 → 用灰石版;獨立暖調場景 → 暖褐版。

**② HEIGHT** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-image-into-height-displacement-e27e9371-9f8e-4d4a-b07d-960f82ec2068)
```text
Convert the attached image into a HEIGHT / DISPLACEMENT map. Keep every element in the EXACT
same position and scale, aligned pixel-for-pixel; do NOT redraw or move anything. Pure
grayscale. Base the brightness ONLY on how far each element PROTRUDES from the ceiling surface
— NOT on the stone's own light/dark color. The X-crossing ribs, the border ribs and their
mouldings protruding forward = brightest; the central and corner carved rosette bosses = bright
(boss center highest); the flat brick field = mid-grey; mortar joints and the grooves alongside
every rib = dark. Smooth tonal gradient following relief only. NO color, NO lighting, NO cast
shadows, NO albedo texture detail.
```

**③ NORMAL(從 height)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-grayscale-height-map-into-tangent-2ceb20e5-36b3-4c53-b8e0-7330a6e067d8)
```text
Convert the attached grayscale HEIGHT map into a tangent-space NORMAL map, aligned pixel-for-
pixel — keep every element in the EXACT same position and scale, do NOT move, redraw, add or
crop anything; only translate height into surface normals. Interpret the input as elevation:
BRIGHT = raised toward the viewer, DARK = recessed. Output a tangent-space normal map that is
predominantly blue-violet (flat brick field ≈ RGB 128,128,255); the RED channel encodes left-
right slope, the GREEN channel encodes up-down slope; the raised X-ribs, border ribs and
rosette bosses bulge outward, the grooves beside each rib and the mortar joints slope inward,
following the height gradients. OpenGL convention (green = +Y, up). NO albedo, NO color tint,
NO lighting, NO cast shadows, NO ambient occlusion. Square 1:1, same framing, zero perspective.
Non-color data map.
```

**④ ROUGHNESS** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-image-into-roughness-map-bb5bd918-1384-480c-8ae7-bf3468dea20c)
```text
Convert the attached image into a ROUGHNESS map, grayscale, aligned pixel-for-pixel; keep every
element in place, do NOT redraw. Weathered matte stone bricks = light grey (high ~0.85); the
smoother rib mouldings and boss tops = mid grey (~0.6); mortar joints = mid-high (~0.8). NO hue,
NO lighting, NO highlights. Ignore any tonal variation already in the plate.
```

**⑤ AMBIENT OCCLUSION** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-image-into-ambient-occlusion-map-5f775332-7f36-4a79-a81c-9c5053109196)
```text
Convert the attached image into an AMBIENT OCCLUSION map, grayscale, aligned pixel-for-pixel;
keep every element in place, do NOT redraw. Exposed forward faces (rib tops, boss tops, flat
brick surface) = white; the grooves alongside the ribs, the mortar joints, the recesses of the
carved rosettes and the four corners where the vault curves away = soft dark grey. Soft contact
occlusion ONLY — base it on geometric cavities, IGNORE any tonal shading already painted in the
plate. NO directional light, NO cast shadows, NO color.
```
> metallic = 純黑(無金屬件),程序生即可。

---

### 9.3 B-floor 方石地板(tileable,**seamless 開**)

**① 去光(tileable)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/attached-stone-tile-texture-keep-every-block-crack-558d8a8f-864d-4a0f-98af-15723f201a96)
```text
From the attached stone-tile texture, keep every block, crack, chip and joint EXACTLY in place
— do NOT move, redraw, add or crop anything; only remove the lighting. DE-LIGHT it into a true
flat albedo: remove ALL baked highlights and specular sheen on the raised stone tops, remove
the ambient-occlusion shadow darkening inside the mortar joints and cracks (keep the mortar's
own dark color, but flatten the extra shadow), and even out any overall luminance gradient so
there are no light/dark patches that would repeat when tiled. Keep the true dark blue-grey
weathered stone hue. Perfectly even, flat, shadowless diffuse albedo, uniform macro brightness
edge to edge. NO cast shadows, NO highlights, NO ambient occlusion, NO directional shading, NO
vignette, NO color shift. Seamless and TILEABLE on all 4 edges, square 1:1, top-down
orthographic, zero perspective. Clean PBR base color map.
```
> 之後另跑**提亮 pass**(嫌太暗):`Brighten ... to a LIGHTER mid-grey stone, block faces ~45-60% grey, mortar joints mid dark grey (not pure black), keep the cool blue-grey hue, do NOT blow out to white. Seamless tileable.`

**② HEIGHT — ❌ 太軟失敗版(枕頭感)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-height-4adb440c-ac86-48a7-91a4-9f26d2db4c68)
```text
Convert the attached stone-tile image into a HEIGHT / DISPLACEMENT map. Keep every block, crack
and joint in the EXACT same position and scale, aligned pixel-for-pixel; do NOT redraw or move
anything. Pure grayscale. Base the brightness ONLY on how far each area protrudes — NOT on the
stone's own dark/light color: the raised, rounded stone-block tops = brightest/light grey; the
flat block faces = mid-grey; the mortar joints between blocks and the cracks splitting them =
darkest/black; smooth tonal falloff over each block's rounded curvature. Seamless and TILEABLE
on all 4 edges, square 1:1. NO color, NO lighting, NO cast shadows, NO albedo detail. Grayscale
non-color data.
```
> ❌ 問題:`rounded curvature` → 石塊變枕頭鼓起、軟邊。

**② HEIGHT — ✅ 調整堅硬版(正解)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-height-f289844a-6b64-4b89-a53f-06020f17e364)
```text
Convert the attached stone-tile image into a HEIGHT / DISPLACEMENT map, aligned pixel-for-pixel;
keep every block, crack and joint in place, do NOT redraw. Pure grayscale. Make it a HARD-EDGED
cut-stone floor: each block top is FLAT and uniform light grey (NO rounded pillow bulge, NO
inflated dome), with a small crisp chamfer at the block edge then a STEEP near-vertical drop
into the mortar joints; the joints and cracks are narrow and BLACK. High contrast between flat
tops and deep joints, sharp edges, minimal edge rounding. Seamless and TILEABLE on all 4 edges,
square 1:1. NO color, NO lighting, NO cast shadows, NO albedo detail.
```
> negative 擋軟邊:`rounded, pillow, inflated, dome, bulging, soft edges, bevel too wide, smooth curvature`

**③ NORMAL — 禁黑版(生成式天花板實證)** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-height-map-into-tangent-space-779abb84-6e15-4fa5-8f56-2fe37eb820ed)
> 生成式 normal 連三錯(偏紫 / 邊方向亂 / **縫是黑的**=無效向量)。此為最後「禁黑」版,仍不保證正確 —— **正解是 §7 腳本從 height 派生**。
```text
Convert the attached HEIGHT map into a tangent-space NORMAL map. CRITICAL: the output must
contain NO black and NO dark pixels anywhere — every pixel is a normal vector, so the whole map
stays in the blue/periwinkle range. Flat block tops = uniform RGB (128,128,255). The mortar
joints and crack BOTTOMS also face up, so they are ALSO periwinkle blue (128,128,255), NOT
black. ONLY the thin steep SIDE WALLS between a block top and a joint get strong red/green slope
colors (a bright band on each edge). Do NOT copy the black joints from the height — convert them
to blue floor with colored side walls. RED = left-right slope, GREEN = up-down slope, OpenGL
(green = +Y up). No albedo, no lighting, no shadows. Seamless tileable, 1:1.
```

**④ ROUGHNESS** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-roughness-a7c0ad58-03ae-4c3c-b14b-0f72e485a790)
```text
Convert the attached stone-tile image into a ROUGHNESS map, grayscale, aligned pixel-for-pixel;
keep every block, crack and joint in place, do NOT redraw. Weathered matte stone block faces =
light grey (high roughness ~0.85); smoother/polished worn block tops and damp spots = mid grey
(~0.6); the mortar joints and cracks = mid-high grey (~0.8). Even, no hotspots. Ignore any tonal
shading already in the image — base it on material only. NO hue, NO lighting, NO highlights.
Seamless and TILEABLE on all 4 edges, square 1:1. Linear non-color data.
```

**⑤ AMBIENT OCCLUSION** → [Leonardo 結果](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-ambient-4d7a68b1-d470-4e9b-ac36-7db80dd31189)
```text
Convert the attached stone-tile image into an AMBIENT OCCLUSION map, grayscale, aligned pixel-
for-pixel; keep every block, crack and joint in place, do NOT redraw. Exposed raised block tops
= white (no occlusion); the mortar joints between blocks and the cracks splitting them = soft
dark grey (occluded); a slight darkening where block edges meet. Soft contact occlusion only —
base it on geometric cavities, IGNORE any tonal shading already in the image. NO directional
light, NO cast shadows, NO color, NO highlights. Seamless and TILEABLE on all 4 edges, square
1:1. Linear non-color data.
```
> metallic = 純黑(石材,無金屬),程序生即可。

---

> **共用 negative(灰階 data map 類):** `color tint, hue, albedo detail, baked lighting, cast shadows, highlights, directional light, seams, misaligned, perspective, blurry, watermark, text`
