# 去光 → PBR 整套貼圖(de-light → PBR maps)

**用途:** 把一張**帶打光的材質/場景圖**轉成**不受光的 PBR 整套貼圖**(base / height / normal / roughness / metallic / AO),之後導入 Blender / 引擎**重新打光**。

**觸發詞:** 「**delight pbr**」「**delight**」「去光」「de-light」「不受光貼圖」「PBR 貼圖 / 整套貼圖」「出 normal / roughness / height / AO / metallic map」「材質圖轉 PBR」「導入 Blender 重打光」。(= 2 步驟:1 去打光 → 2 出 PBR 整套貼圖)

> 🤖 **本檔角色 = 自動反射片段(給 Claude 自動用的精簡操作版):** 模板 + 鐵律 + 踩坑表,任務沾到去光/PBR 時自動載入,照這份動手即可。
> 📒 **完整案例紀錄(給人翻的實戰:三 worked example + 逐字 prompt + 成品圖 + 踩坑全歷程)在 repo:** `docs/asset-cases/SOP-ai-delight-pbr.md` —— 要看「某案怎麼跑、哪張圖、哪次失敗」才翻那份,不必每次載。

---

## 0. 先分型

| 類型 | 例 | 重打光 | seamless |
|---|---|---|---|
| **場景板** | 牆 / 拱頂(深凸雕、深龕) | 平板+displacement 只反應表面;深凸凹不自遮蔽 → 要真幾何(concept→3D)才自然 | 關 |
| **可平鋪 tileable** | 地板 / 牆材質 | 平板+normal/height 就夠 | 開 |

## 1. 平台(Leonardo)

Image2Image + **Nano Banana 2**、**Prompt Enhance / Style = None**、**Creativity 最低段(0.2–0.35)**、輸出比例=輸入、滿版無 letterbox。tileable 類 **Tiling/Seamless 開**。

## 2. Step 1 去光(image-grounded,餵原圖)

**鐵律:列點刪 > 泛詞否定。**「4 大殺手」逐項點名:①點燃光源火光+暖溢光(→`unlit dark metal`)②冷色 rim/背光 ③深凹投影+AO ④暗角 vignette / 明暗漸層。

```text
From the attached image, keep the [ASSET] EXACTLY as-is (all geometry, proportions, layout,
carvings — unchanged), but fully DE-LIGHT it into a true flat albedo plate. Remove ALL baked
lighting: [逐項點名要刪的光]. Re-render with perfectly even, flat, shadowless diffuse light so
every surface reads its own true de-lit color — [保色: keep the warm X hue | 中性化: neutralize
to true neutral cool-grey stone]. NO cast shadows, NO rim light, NO glow, NO vignette, NO color
tint. [場景: head-on frontal orthographic | tileable: top-down ortho, SEAMLESS and TILEABLE on
all 4 edges]. Square 1:1, zero perspective. Clean de-lit albedo plate for PBR.
```
**驗收**(過了才往下,別盲生):疊回原圖比剪影/比例沒漂、色偏中性化、烤光影攤平、tileable 巨觀亮度均勻。

## 3. Step 2 PBR 各 map

**每格開頭加對齊鎖:** `Convert the attached image into a [MAP] map. Keep every element in the EXACT same position and scale, aligned pixel-for-pixel; do NOT move, add, remove, crop or redraw anything; only replace surface values.`

- **① BASE** = 去光板洗淨(攤平巨觀明暗 + **抬黑位**,縫別純黑,sRGB)。
- **② HEIGHT**(先跑,normal 靠它):`Base brightness ONLY on protrusion — NOT the stone's own light/dark color`(擋 albedo 汙染)。**軟/硬**:`rounded curvature`=枕頭軟邊(多半不要);硬切石=`FLAT block top + steep near-vertical drop + sharp chamfer`,negative 擋 `rounded/pillow/inflated/soft edges`。
- **③ ROUGHNESS**:材質分級(風化石~0.85 / 磨光~0.55 / 金屬~0.4 / 玻璃~0.15)+ `ignore tonal shading, base on material`。
- **④ METALLIC**:**別燒圖當常數**。純石材=整張純黑 0(程序生);有金屬件=hard mask(石黑/金屬白)。
- **⑤ AO**:凸面白、凹縫暗 + `base on geometric cavities ONLY, IGNORE tonal shading`。
- **⑥ NORMAL → 不要用生成式,從 ②height 派生**(見下)。⑦ SPECULAR:metal/rough 不出。

## 4. 🔴 鐵律:NORMAL 一律從 HEIGHT 派生

生成模型「畫顏色、不算梯度」→ normal 必錯(**實證三連敗**:平面偏紫 / 邊紅綠方向亂 / **縫是黑的**=無效向量)。正解:用乾淨 height 跑 `tools/pbr-derive/height_to_normal.py`(梯度算,平面精準 128,128,255、OpenGL+UE 兩版、跟 height 對齊;硬邊用 `--blur 0.3`)。
> 其他鐵律:**顏色只動 base**,height/normal/rough/metal/AO 只看形狀,深淺無關、可共用來源。配同場景色盤用 **Match Color**(生圖形容詞壓不準明度,會「太白」)。

## 5. Blender / 引擎踩坑(實拍抓到)

| 症狀 | 元凶 | 修 |
|---|---|---|
| 石頭暗悶 + 邊緣假高光爆白 | **Metallic = 1**(石頭被當金屬) | Metallic 設 **0** / 接純黑圖 |
| 磚面悶、死黑 | **AO 重複乘進 base**(去光後又全乘,引擎再算一次) | AO 別全乘;Fac 0.3 或只走間接光 |
| 整體壓暗 | Blender **AgX** | View Transform 改 **Standard** / Exposure +0.5~1 |
| 凸看成凹 | **normal 綠通道慣例反** | normal 後 `Separate Color`→G `Invert`→`Combine`;UE 用 DirectX 版 |
| height 沒真凸 | 沒開位移 | 材質 `Displacement: Displacement Only` + 物件 Subdivision |

**色彩空間:** Base=**sRGB**;Normal/Height/Roughness/Metallic/AO=**Non-Color**。ORM 打包:R=AO / G=Rough / B=Metal。
