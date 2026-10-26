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
- [去光·暖褐](https://app.leonardo.ai/generation/image/attached-vaulted-ceiling-image-keep-architecture-d39ced0b-b48c-40c9-aee6-d421b2e1e542) · [去光·灰石](https://app.leonardo.ai/generation/image/attached-vaulted-ceiling-image-keep-architecture-8d490406-018e-4e46-b9b6-a5b2e2389904) · [HEIGHT](https://app.leonardo.ai/generation/image/convert-attached-image-into-height-displacement-e27e9371-9f8e-4d4a-b07d-960f82ec2068) · [NORMAL](https://app.leonardo.ai/generation/image/convert-attached-grayscale-height-map-into-tangent-2ceb20e5-36b3-4c53-b8e0-7330a6e067d8) · [ROUGHNESS](https://app.leonardo.ai/generation/image/convert-attached-image-into-roughness-map-bb5bd918-1384-480c-8ae7-bf3468dea20c) · [AO](https://app.leonardo.ai/generation/image/convert-attached-image-into-ambient-occlusion-map-5f775332-7f36-4a79-a81c-9c5053109196)

### B-floor — 方石地板([C] tileable,seamless,無金屬)
tileable 材質。去光 → **提亮** → height **軟邊失敗 → 改硬邊切石**(flat top+steep drop)→ normal **生成三連敗 → 從 height 派生才對**。
- [去光](https://app.leonardo.ai/generation/image/attached-stone-tile-texture-keep-every-block-crack-558d8a8f-864d-4a0f-98af-15723f201a96) · [HEIGHT·軟邊失敗](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-height-4adb440c-ac86-48a7-91a4-9f26d2db4c68) · [HEIGHT·硬邊✅](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-height-f289844a-6b64-4b89-a53f-06020f17e364) · [NORMAL·禁黑版](https://app.leonardo.ai/generation/image/convert-attached-height-map-into-tangent-space-779abb84-6e15-4fa5-8f56-2fe37eb820ed) · [ROUGHNESS](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-roughness-a7c0ad58-03ae-4c3c-b14b-0f72e485a790) · [AO](https://app.leonardo.ai/generation/image/convert-attached-stone-tile-image-into-ambient-4d7a68b1-d470-4e9b-ac36-7db80dd31189)

---

## 7. 程序工具([`tools/pbr-derive/`](../../tools/pbr-derive/))

- **`height_to_normal.py`** — height → normal(**OpenGL + DirectX 兩版**,梯度算、附 QC 平均值);`--strength` 控強度、`--blur` 控銳利(硬邊用 0.3)。
- **`derive_pbr.py`** — 去光 albedo → 整套(洗淨 base + height + normal + roughness + metallic + AO + ORM 打包);含 `clean_albedo()`(攤平+抬黑位)、擋 albedo 汙染。

```bash
python3 tools/pbr-derive/height_to_normal.py <height>.png --outdir <dir> --prefix <name> --strength 2.5 --blur 0.3
```

---

## 8. 待補(TODO)

- [ ] 三案**成品圖入庫** `images/`(`gothic-wall-*` / `vault-*` / `floor-tile-*`),把上方 Leonardo 連結換成 repo 內嵌圖。
- [ ] 三案 normal **程序派生定版**(取代生成版),各附 QC 平均值。
- [ ] B-floor **四方連續驗縫**(offset 半格)+ 引擎 3×3 驗收。
- [ ] B-wall 若走 concept→3D:補 3/4 掠射視圖 + image-to-3D 出 mesh 流程。
- [ ] B-ceiling 暖→灰 **Match Color 程序版**(治「太白」)留檔。
- [ ] 把 §3.2 各 map 模板收進 `ai-media-generator` skill 當標準片段。
