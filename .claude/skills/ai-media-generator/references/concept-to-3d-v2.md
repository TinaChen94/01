# concept→3D / 三視圖重建 / 拆概念圖 — **V2**(image-grounded SOP + 雙軌 + 正交鎖 + 救援鏈)

> **V2 = V1 超集。** V1 原版保留於 [concept-to-3d.md](concept-to-3d.md)(image-grounded 鐵律 + 勝利模板 + 三視協議,**不動,供日後參閱**)。
> V2 把 V1 的「de-lit 單軌」升級成 **雙軌(保光影 ↔ de-lit)**,並補進 A4 / A5 的實戰招式。
>
> **實證案例:**
> - **A4 — 古堡概念圖拆解(建築四件)**:紅框定位 / 反裁切 / HEX 鎖色 / 鎖結構換色調 / 廢墟救援鏈 / 地面材質
> - **A5 — 古堡三視圖重建(道具 turnaround)**:保光影↔de-lit 雙軌 / 正交鎖 / 固定世界光 / 鏡射左視
> - 檔案:`docs/asset-cases/A4-castle-concept-decomposition.md`、`A5-castle-turnaround-image-to-3d.md`

**觸發詞(同 V1):** 「拆掉這張概念圖」「concept→3D」「三視圖重建」「turnaround / model sheet」「正交立面」「image-to-3D 參考圖」「物件清單 / asset manifest」。

---

## 🔴 根本鐵律(同 V1,違反必漂移)

> **物件已經在圖裡了 → source of truth 永遠是那張圖,不准把物件翻成文字代理。**

image-grounded 的「抽取 + 重定向」,不是 text-to-image 的「從零描述」。
**文字只負責「呈現規格」(視角 / 否定來源相機 / 背景 / 打光 / 用途),不負責「物件長相」。** 長相交給圖。

---

## 🆕 V2 第一步:先問用途 → 選軌(雙軌)

拆出來的素材**給誰用**,決定走哪條軌。**順序固定:先保光影 → 再 de-lit。**

| 軌 | 呈現規格 | 給誰用 |
|---|---|---|
| **A 保光影軌** | **保留**原圖烘焙光影 / 色調(AO + 材質 + 立體光感);**移除**霧 / 大氣 / 遠近漸層 | 引擎「不受光 / emissive 材質球」的簡單 mock **直接貼**(貼圖自己要帶光) |
| **B de-lit 軌** | **均勻漫射平光、去光保 albedo**、無陰影 / 輪廓光 / 光束、`#808080` 無縫底 | **image-to-3D** 的乾淨輸入參考 |

- ⚠️ **de-lit = 去光保 albedo,不是去 albedo 變黏土。** 寫 `KEEP the [material] albedo, DE-LIT the lighting`;**不要** `remove the true albedo`(= 變灰黏土 / matcap)。(A5 踩坑句「去除真實反照率」就是害出黏土的原兇。)
- ⚠️ **順序不可反。** de-lit 把光資訊拿掉後**補不回**原概念圖的打光。要兩套 → 先出保光影,再 de-lit。
- **V1 的勝利模板(`#808080` + 平光 + 無影)= 本頁 B de-lit 軌。** A 保光影軌是 V2 新增(給不受光材質 mock)。

---

## ✅ 勝利模板(兩軌各一版,逐字可改)

把物件名填進 `[OBJECT]`、材質填 `[MATERIAL]`、視角換 `FRONT / LEFT-SIDE / BACK / 3-4`。第一視餵**原圖**;第二、三視**同時餵原圖 + 已產出的正確視圖**當一致性錨 + 固定 seed。

### A 保光影軌(給不受光 / emissive 材質 mock)

```text
From the attached concept art, extract ONLY the [OBJECT] and re-orient it to a true
head-on FRONT view, facing the viewer; IGNORE the concept's camera angle and
perspective (do NOT copy a low-angle, tilted or 3/4 view). One complete, isolated,
centered [OBJECT].

CRITICAL — preserve the source's baked lighting, colour and tone EXACTLY as painted:
the same key-light / shadow side, the exact [MATERIAL] colour, the ambient occlusion in
every crevice. Do NOT relight, do NOT change the tone or palette, do NOT flatten to
neutral studio light, do NOT add or remove shadows. This is a PRE-LIT asset for an
UNLIT / emissive material — reproduce the original lighting as-is. REMOVE only the
atmospheric haze / fog / distance desaturation.

FRAMING: the complete [OBJECT] fully in frame, generous margin all sides, nothing
cropped or touching the edge, centered on empty dark background. High-resolution game
asset plate.
```

### B de-lit 軌(給 image-to-3D,= V1 模板)

```text
From the attached concept art [and the front reference plate], extract ONLY the [OBJECT]
and re-orient it to a true head-on FRONT orthographic view; IGNORE the concept's camera
angle and perspective (do NOT copy a low-angle, tilted or 3/4 view). [SAME object,
identical proportions, materials and details as the reference plate.]

KEEP the real [MATERIAL] albedo — its true colours and all surface detail (do NOT turn
it into grey clay, do NOT remove the material). DE-LIT it: remove all baked-in lighting
— no key light, no shadow side, no dramatic highlights. Light it ONLY with perfectly
even, uniform, flat diffuse studio lighting. NO cast shadows, NO rim light, NO god rays
or light beams, NO scene elements.

Centered on a flat neutral grey (#808080) seamless background, complete, nothing cropped.
High-resolution clean de-lit albedo reference plate for image-to-3D.
```

---

## 🔒 正交鎖(turnaround / 立面必套,A5 驗證)

NB 預設是**有透視的戲劇鏡頭**(近大遠小、略仰角)。要壓成正交,把這段貼進任何視角 prompt:

```text
Render in TRUE ORTHOGRAPHIC PROJECTION (parallel projection), like a technical
model-sheet / turnaround elevation. NO perspective, NO foreshortening, NO vanishing
point, NO lens distortion, NO looking down from above, NO dramatic low/high angle. The
camera axis is perfectly horizontal, at the object's mid-height, perpendicular to the
view. Every part at the SAME scale regardless of depth, all parallel edges stay
parallel. Flat, even, undistorted elevation.
```

> ⚠️ **生成模型畫不出「數學上真正交」**——它本質是透視渲染器,上面這段只能**逼近**(壓平透視)。要 100% 真正交只有一條路:**拿這張逼近版當建模參考 → 建完模用 3D 正交相機 render**。逼近版比例/造型/光影夠準,當參考就收。

---

## 🔁 三視一致性協議 + 固定世界光(V1 + A5 擴充)

```
front:  input = 原圖                  → 出 front plate(疊原圖驗 silhouette)
side:   input = 原圖 + front plate     → prompt 加「SAME object as reference」
back:   input = 原圖 + front plate     → 同上
3/4:    input = front + side + back    → iso / parallel projection
```
- **固定 seed** 全程沿用;每出一視先疊回原圖比剪影/比例,過了才往下一視(別三張盲生)。

**A5 新增(A 保光影軌專用)——固定世界光 → 各視角明暗不同:**
- 光固定在世界空間:**正面迎光、側面前亮後暗、背面背光**(背面只剩薄暖 rim 打在輪廓上)。
- **左視 = 右視鏡射**(固定光下不用重算一張)。
- **EXPOSURE LOCK**:補 `keep the same dark low-key exposure as the front plate, do NOT brighten` → 治 NB 自動提亮。
- **壁掛件**(如壁式火把)背面貼牆 → model sheet **正 + 側(含牆架)就夠建模**,背視可省。

---

## 🧩 A4 實戰招式(拆建築 / 背景模組)

### 紅框定位(一張圖裡只抽某一區)
```text
Use the FIRST image as the source and the SECOND image ONLY to locate the target.
Reproduce ONLY the content inside the red outline — [the target]. Do NOT draw the red
line. Everything outside the red outline must become empty flat dark background.
```
+ **點名禁掉搶戲物件**(例:`do NOT render the central window / archway`)。治「NB 自動補成整個對稱場景」。

### 反裁切 FRAMING(治上下被切)
`show the COMPLETE [unit]: its ENTIRE height … nothing cropped or touching the edge … fills ~70–80%` + **高瘦比例(9:16)**。

### HEX 鎖色(顏色對不上時)
從原圖抽**實際色值**鎖 palette:`overall average ~#..., mid-tone #...–#..., deep near-black AO #..., highlight no brighter than #...`。底線手段:Python 逐階對映色盤 100% 鎖死。

### 鎖結構 + 換色調(雙參考,治結構漂移)
**結構一旦對了,別再重生成**(重生成會重畫幾何)。改用雙參考 recolour pass:
```text
Image A (FIRST) = the correct geometry. Keep its geometry EXACTLY as-is, pixel for
pixel. This is a RECOLOUR / RELIGHT pass only — do NOT change any structure.
Image B (SECOND) = the colour/lighting reference. Recolour Image A to match B exactly.
```

### 廢墟 / 縱深救援鏈(原圖是霧、無平面可抽)
**判讀先行:** 平面(可抽立面)vs 縱深 vista(無平面)。對 vista(霧 / 遠景走廊):
1. 走救援鏈:找 / 做一張**結構清楚的參考(廢墟圖)→ 修復成完整 → 鎖結構換色調 → 局部壓亮**;**或**
2. 當**背景板 backdrop**(背景風格 DNA 那套)處理,**不當可平鋪 game asset**(遠景多半是畫出來的背景)。

### 地面 / 材質類
**別硬拆爛素材**(斜角 + 低解析拉 top-down 必糊)。用**高品質現成磚 / 材質** → 「**鎖格鎖細節 + 換色**」(最穩 pass,不動幾何)。放大走 B1 配方(Style / Enhance = None;Dynamic = 糊的元兇)。

---

## 🧰 平台(同 V1,都要能吃參考圖)

| 平台 | 何時選 | 注意 |
|---|---|---|
| **Nano Banana Pro** | 預設首選;指令服從最好、多圖 reference = superpower | 自然段 80–150 字;比例到 UI 設 |
| **Flux 1.1 Kontext** | 要極寫實材質 / 精準局部編輯 | 偏寫實會偷加透視 → 句首壓 `strictly flat orthographic`;禁藝術家名、禁 `--ar` |
| **Seedream 5.0** | 中文場景 / 精簡 prompt | 重要詞在前 |

> 三家都支援 image input / edit。選錯的不是「模型」是「模式」——別用純 t2i 做這件事。

---

## ✅ 交付前 checklist(V1 + V2 擴充)

- [ ] 原圖當 **input** 餵進去?(沒有 = 直接違規)
- [ ] 文字只寫「呈現規格」,沒重述物件長相?
- [ ] **點名否定來源相機**(IGNORE low-angle / 3-4 / perspective)?
- [ ] **選對軌?** 保光影(不受光材質 mock)vs de-lit(image-to-3D)。要兩套 → **先保光影再 de-lit**。
- [ ] de-lit 有寫「**保 albedo、不要黏土**」?底 `#808080` + 平光 + 無影 / rim / beams?
- [ ] turnaround **固定世界光一致**(正迎光 / 側前亮後暗 / 背背光)?左視用鏡射?
- [ ] **正交鎖**有套?(知道只是逼近,真正交從 3D 相機)
- [ ] 第二 / 三視有餵前視 plate + **同 seed**?
- [ ] output 疊原圖驗 **silhouette**?

---

## 📌 擴充踩坑(A4 / A5)

1. **先保光影 → 再 de-lit,不可反。** de-lit 去光後補不回原打光。
2. **de-lit = 去光保 albedo ≠ 黏土。**「去除真實反照率」是害出黏土的踩坑句;正解寫「保本色、只去光影」。
3. **只還原框內 > 泛詞隔離** + 點名禁搶戲物件。
4. **反裁切要明寫**(FRAMING 整段 + 高瘦比例)。
5. **`even brightness overall` 會被讀成中性均光淺灰** → 保光影要明寫 match SOURCE + near-black AO + do NOT clay / studio。
6. **重生成會重畫幾何** → 結構對了改「鎖結構換色調」雙參考,別重跑整張。
7. **原圖是霧 / 縱深的區拉不出立面** → 救援鏈或當背景板。
8. **材質類換現成素材換色 > 硬拆**。
9. **正交 NB 只能逼近** → 真正交從 3D 相機、從網格烘 height / normal。
10. **固定世界光:各視角明暗不同;左視 = 右視鏡射;EXPOSURE LOCK 防提亮。**
11. **高空物件大膽簡化;數量 / 邊數鎖死寫;樓空填背板 / 填洞成浮雕**(透空進 3D 會破面)。
12. **edit-chain 會漂 → 畫風崩掉就止損回退**,回最佳版再分支。
13. **de-lit 去雜訊要分段**(NB de-lit 常帶雜訊,一句洗不乾淨就多跑幾階)。
14. **全是 re-render 非像素級保留** → 疊回原圖比例 / 數量可接受才收;要像素真值 / 真正交走 3D 建模烘。

---

## 📎 實證來源

- **V1 原版 SOP(保留):** [concept-to-3d.md](concept-to-3d.md)(2026-06,哥德教堂正面三視踩坑)
- **A4** 古堡概念圖拆解(建築四件):`docs/asset-cases/A4-castle-concept-decomposition.md`
- **A5** 古堡三視圖重建(道具 turnaround,保光影↔de-lit 雙軌):`docs/asset-cases/A5-castle-turnaround-image-to-3d.md`
- 相關佐證:`nano-banana.md`(多圖 reference)、`templates/concept-to-3d-pipeline.md`(四步驟主模板)
