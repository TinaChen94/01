# Concept Art → 3D 資產拆分工作流 (Concept-to-3D Asset Pipeline)

**用途：** 丟「任一張」參考圖 / concept art，自動產出 ① 資產清單(分 3 類) ② 每個物件各自對應的去背 / 多視圖 / 3D 提示詞。給遊戲/影視/3D 列印的高模生成前置。

---

## ✅ 主模板 — 個別物件四步驟(front 確認 → 4 視圖 → 3/4 → 45° iso)★

**逐物件、依序做、別跳步:**
1. **STEP 1 先出 front** ── 換 `[PROP]`、附概念圖,只跑 ① front plate。先別碰視圖。
2. **確認** ── 比對原圖:造型/材質/比例對不對、乾不乾淨?**不對 → 看下面〈🧭 一頁速查〉修到對,先別往下。**
3. **STEP 2 出 4 視圖** ── 拿**確認過的 front 圖**當參考跑 ②(orthographic 多視圖,餵 multiview-to-3D)。
4. **STEP 3 出 3/4 視圖** ── 一樣拿確認過的 front 當參考跑 ③(單張立體 hero,餵 single-image-to-3D)。
5. **STEP 4 出 45° 等角視圖** ── 一樣拿確認過的 front 當參考跑 ④(true isometric,零透視,餵 single-image-to-3D)。

**① FRONT(先做這個,確認再往下)**
```
From the attached concept art, extract ONLY the [PROP]. Re-render as one complete, isolated object, centered and fully visible, front orthographic view, on a flat neutral grey (#808080) seamless background. Perfectly even diffuse studio lighting, NO cast shadows, NO rim light, NO scene elements. Maximum sculptural detail. High-resolution clean reference plate for image-to-3D.
```

**② 4 視圖(orthographic 多視圖;front 確認後,附確認過的 front)**
```
The [PROP] from the confirmed front plate, as a 4-VIEW orthographic turntable in ONE image: front | left side | right side | back, four equal panels left to right. IDENTICAL object in all four panels — same geometry, proportions, materials, height and centering. Flat even diffuse lighting, neutral grey (#808080) background, NO shadows, strictly orthographic (no perspective). Maximum sculptural detail, reconstruct all occluded areas. Asset reference for multiview-to-3D.
```

**③ 3/4 視圖(單張立體 hero,給 3D AI 生成;附確認過的 front)**
```
The [PROP] from the confirmed front plate, as a single 3/4 hero view for image-to-3D generation: rotated ~35° to show the front and one side, tilted ~25° from above to reveal the top surfaces. One complete, isolated object, centered and fully visible, on a flat neutral grey (#808080) seamless background. Even diffuse studio lighting, NO cast shadows, NO rim light, NO scene elements, near-orthographic (no wide-angle distortion). SAME geometry, proportions and materials as the front plate. Maximum sculptural detail, reconstruct all occluded areas. High-resolution single-image reference for image-to-3D generation.
```

**④ 45° 等角視圖(true isometric,給 3D AI 生成;附確認過的 front)**
```
The [PROP] from the confirmed front plate, as a single 45-degree front-side angle for image-to-3D generation: true 45-degree isometric projection (45° azimuth, ~30° downward tilt), parallel projection, no perspective distortion, no vanishing point, centered. One complete, isolated object, fully visible, on a flat neutral grey (#808080) seamless background. Even diffuse studio lighting, NO cast shadows, NO rim light, NO scene elements. SAME geometry, proportions and materials as the front plate. Maximum sculptural detail, reconstruct all occluded areas. High-resolution single-image reference for image-to-3D generation.
```

> **四組各有用途:** ① front 鎖基準 → ② 4 視圖餵**多視圖**轉 3D(Rodin/Tripo 多圖)→ ③ 3/4 hero 餵**單圖**轉 3D(自然立體角)→ ④ 45° 等角餵**單圖**轉 3D(true parallel projection,零透視變形、零滅點,最乾淨)。
> **③ vs ④:** ③ 是自然 hero 角(~35°/~25°、near-ortho);④ 是**精確等角**(45°/30°、全平行投影、無滅點),要無變形/等角素材就用 ④。
> **要 3 視圖?** ② 把 `right side` 拿掉、`four`→`three` 即可。Master Prompt / SPEC / 修正層都是選配。

**核心心法：** 沒有真正的「一鍵」。圖上那種乾淨拆解圖是 4 段管線的產物 ──
`①盤點分類 → ②單件去背攤平 → ③正交多視圖 → ④影像轉3D`。
②③ 做得乾不乾淨，直接決定 ④ 成敗。最大殺手是把「概念圖的戲劇打光版」直接丟進 3D AI(god rays / 紅光 / 景深會被烤進貼圖)。所以拆分階段的第一要務是 **去戲劇光、攤平、去背、補全遮擋**。

---

## 🧭 一頁速查:症狀 → 修法(從這裡開始)★

**主流程(每個物件):**
`PASS 1 極簡提取(只填 [PROP],原圖為準) → 出圖 → 比對原圖 → 偏了? → 對症跳 PASS 2 修正節`
> 沒偏就直接進 3D。偏了**別整條重跑**,只針對偏掉那一點加鎖。

**症狀 → 跳哪節(對症下藥):**

| 你看到的症狀 | 跳這節 / 怎麼修 |
|---|---|
| 物件被「重畫」、不像原圖、自己長出細節 | **退回 PASS 1**:prompt 砍到只剩 `[PROP]`,別塞 SPEC/風格 |
| 抽不乾淨:背景殘留、混進別的物件 | PASS 1 加 `extract ONLY the [PROP]` + `NO scene elements` |
| 顏色/材質不對(被光染、材質認錯) | →**§顏色 / 材質辨識錯誤 → 修正機制** |
| 姿勢不對(手臂/坐姿)、缺件(漏頭光環)、比例歪 | →**§姿勢 / 造型辨識錯誤 → 修正機制** |
| 畫風跑掉(變日式/印度、太精緻乾淨、失彩繪斑駁) | →**§畫風 / 樣式漂移 → STYLE LOCK** |
| 多視圖各格不一致(高度/比例/材質跳動) | 強化 `IDENTICAL — same geometry / proportions / materials / height / centering` |
| 背面 / 遮擋處亂編 | 4-VIEW 已含 `reconstruct occluded`;仍不行 → 給概念圖裁切或 pose 當 ref |
| 進 3D 後表面爛、光影被烤進貼圖 | 查**4 大殺手**:投影 / rim 光 / 景深 / 戲劇打光 |

**兩條鐵律:**
1. **修正順序:幾何(姿勢/造型)→ 表面(顏色/材質)→ 畫風。** 幾何先修,否則表面白修。
2. **圖鎖 > 文字鎖:** 偏得兇就丟參考圖(概念圖裁切 / 材質照 / 火柴人 pose),比堆文字準太多。

---

## 兩種引擎(別搞混)

| 工作 | 用什麼 |
|---|---|
| **盤點 + 自動寫提示詞**(下方 Master Prompt) | 視覺 LLM:Gemini 3 Pro / Claude / 本 session ── 會「看圖 + 輸出文字」的模型 |
| **執行去背 / 多視圖**(產圖) | 圖像模型:**Nano Banana Pro** 結構一致性最強、**Seedream 5.0** 中式文物材質最準、Flux Kontext |
| **影像轉 3D 高模** | **Rodin Gen-2**(英雄件多圖)、**Tripo 3.0 / Meshy 5**(一般)、**Hunyuan3D 2.5**(中式文物/開源) |

---

## 三類定義 + 分類決策樹

| 類別 | 定義 | 視圖數 | 3D 走向 |
|---|---|---|---|
| **[A] 英雄道具** 單件精修·多視圖重建 | 小~中、唯一、細節吃重、會被特寫 | **4 視圖**(前/左/右/背) | 高模 + PBR,Rodin 多圖 |
| **[B] 場景模組物件** | 大型/結構性、定義空間、唯一或少量、中景看 | 2 視圖 | 中模,Tripo/Hunyuan |
| **[C] 可複用可拼模組** | 重複 ≥3 次 **或** 格狀/可平鋪(地磚/牆段/階梯/柱/燭台陣列) | **1 正交平拍** | 低模 **或 PBR 材質**,模數化拼接 |

**對每個物件套這個順序判斷：**
1. 重複 ≥3 次 **或** 是 tile/格狀(地/牆/階/柱/欄)？→ **[C]**
2. 否則,大型/結構性/定義房間(神像/大浮雕/寶座/大家具)？→ **[B]**
3. 否則(小、唯一、細節吃重、英雄互動)？→ **[A]**

---

## 主控生成器 Master Prompt(進階 / 批次 — 一次處理整張圖的很多物件才用)

> **只做幾件?用最上面的〈✅ 主模板〉就好,別跑這個。** 這個是「一張圖很多物件、想自動分類 + 批次出 prompt」時才用的引擎,輸出 = 清單表格 + 每物件可複製提示詞。它走兩段式(PASS 1 極簡 → 偏了才修),但**單件提取請優先用主模板,最不會偏**。

```
ROLE: You are a senior 3D art director + technical artist running a concept-to-3D
asset pipeline. I will give you ONE reference image (concept art / scene).

GOAL: Turn the image into a production-ready asset breakdown AND auto-write the
exact generation prompts for each asset, ready to paste into image + 3D tools.

STEP 1 — INVENTORY & CLASSIFY
List every distinct physical object in the image. Classify each into exactly one:
  [A] HERO PROP — small/medium, unique, detail-critical, seen up close. 4-view + high-poly.
  [B] SCENE MODULE — large/structural set piece defining the space, unique/low-count,
      medium distance. 2 views.
  [C] REUSABLE/TILEABLE MODULE — repeats >=3x OR is grid/tile-like (floor, wall,
      step, pillar, fence), meant to be instanced/tiled. 1 orthographic flat capture;
      flat surfaces become PBR materials, not meshes.
Decision order per object:
  1. Repeats >=3x OR tile/grid-like? -> [C]
  2. Else large/structural/room-defining? -> [B]
  3. Else (small, unique, hero-detail)? -> [A]
Output Section 1 as a table:
  | # | asset name | category A/B/C | instance count | occlusion note (hidden parts
  to reconstruct?) | view count |

STEP 1.5 — PER-ASSET VISUAL SPEC (precision pass — run for EVERY asset; this is what
makes each object's description accurate instead of generic)
Observe the reference and write a dense visual spec across these 7 axes (one concrete
clause each, only from what is visible; for occluded parts infer from the visible
style and tag "(inferred)"):
  1. FORM & SCALE — silhouette, proportion, real-world size estimate
  2. PARTS — structural sub-components, so 3D rebuilds the real structure
  3. MATERIAL & FINISH — the TRUE material + surface finish (de-lit: what it is
     actually made of, NOT how the scene light tints it). If the concept lighting
     makes it ambiguous, list the top 2 candidates with confidence high/med/low.
  4. COLOR — the TRUE albedo color under neutral light (mentally remove the scene's
     god-rays / colored light / shadow), incl. variation, gilding, staining. If the
     lit look differs a lot, add it separately as "lit: ...".
  5. ORNAMENT / SURFACE DETAIL — carvings, motifs, relief, inscriptions, patterns
  6. AGE / WEAR STATE — chips, cracks, moss, soot, dust, verdigris, repairs
  7. SIGNATURE FEATURE — the 1-2 details that uniquely identify THIS object
  8. POSE & GESTURE (figures / creatures / characters only) — limb-by-limb position
     (each arm, hand, leg, head tilt), asymmetry, gesture/mudra; tag occluded limbs
     "(inferred)"; if the 2D pose reads ambiguously, note 2 readings + confidence.
Then compress the axes (incl. pose for figures) into ONE dense phrase (~20-40 words, 5-8 high-signal
descriptors). That phrase is the asset's [SPEC]. Print it under the asset's table row.
NOTE: the [SPEC] is documentation + the reference for the CORRECTION pass — do NOT paste
it into the pass-1 extraction/3-view prompts (those use the plain [PROP] name; the concept
image is the reference, and heavy text makes the model re-invent the object and drift).

STEP 1.8 — DERIVE STYLE BIBLE (once per reference image; used in the CORRECTION pass to
pull a drifted asset back onto the concept's art style — NOT prepended to pass 1)
Extract a 5-line project style bible (apply it only when an asset's style drifts):
  - TRADITION/ERA — the specific cultural art/sculpture lineage, AND what it is NOT
  - STYLIZATION LEVEL — refined vs archaic/eroded; what to avoid (clean ZBrush, museum-refined)
  - PROPORTION LANGUAGE — squat/heavy vs elegant/slender, head/hand scale
  - SURFACE/WEATHERING — erosion, chips, patina, faded polychrome pigment remnants
  - MOOD/FINISH — palette + painterly vs clean render
The style bible controls FORM/DESIGN/WEATHERING only — it does NOT re-introduce
dramatic lighting; keep the de-lit neutral lighting from the killers rule.

STEP 2 — AUTO-GENERATE PROMPTS (two passes)
PASS 1 (default) — for EVERY asset, output the minimal template for its category, filling
the [PROP] slot with the plain object name only. Do NOT inject the dense [SPEC] or the
STYLE BIBLE here: the attached concept image IS the reference, and heavy text makes the
model re-invent the object and drift off-target. Keep it minimal and image-grounded.
PASS 2 (correction, only if an asset drifts) — add ONLY the locks that target the actual
deviation: SPEC design anchors, STYLE BIBLE, occlusion-reconstruction, pose lock, or the
material/color fix (see the correction sections). Always pass the concept crop as the
reference. Keep code blocks clean. Output prompts in English; keep cultural nouns precise.

== If [A] HERO PROP ==
  CLEAN PLATE (run in Nano Banana Pro / Seedream) — single hero detail plate:
  "From the attached concept art, extract ONLY the [PROP]. Re-render as one complete,
   isolated object, centered and fully visible, front orthographic view, on a flat
   neutral grey (#808080) seamless background. Perfectly even diffuse studio lighting,
   NO cast shadows, NO rim light, NO scene elements. Maximum sculptural detail.
   High-resolution clean reference plate for image-to-3D."
  4-VIEW TURNTABLE (run in Nano Banana Pro, AFTER the front plate is confirmed) — multiview-to-3D:
  "The [PROP] from the confirmed front plate, as a 4-VIEW orthographic turntable in ONE
   image: front | left side | right side | back, four equal panels left to right.
   IDENTICAL object in all four panels — same geometry, proportions, materials, height
   and centering. Flat even diffuse lighting, neutral grey (#808080) background, NO
   shadows, strictly orthographic (no perspective). Maximum sculptural detail, reconstruct
   all occluded areas. Asset reference for multiview-to-3D."
  3/4 HERO VIEW (run after the front is confirmed) — single-image-to-3D:
  "The [PROP] from the confirmed front plate, as a single 3/4 hero view for image-to-3D:
   rotated ~35° to show front + one side, tilted ~25° from above to reveal the top.
   Isolated, centered, fully visible, flat neutral grey (#808080) seamless background,
   even diffuse light, NO shadows, NO rim light, near-orthographic (no wide-angle
   distortion). SAME geometry, proportions, materials as the front. Maximum sculptural
   detail, reconstruct occluded areas. Single-image reference for image-to-3D generation."
  45° ISO VIEW (run after the front is confirmed) — single-image-to-3D, zero-distortion:
  "The [PROP] from the confirmed front plate, as a single 45-degree front-side angle:
   true 45-degree isometric projection (45° azimuth, ~30° downward tilt), parallel
   projection, no perspective distortion, no vanishing point, centered. Isolated, fully
   visible, flat neutral grey (#808080) seamless background, even diffuse light, NO
   shadows, NO rim light. SAME geometry, proportions, materials as the front. Maximum
   sculptural detail, reconstruct occluded areas. Single-image reference for image-to-3D."
  3D: multi-view → Rodin Gen-2 / Tripo 3.0 (feed the 4 panels); OR single-image → feed
   the 3/4 hero OR the 45° iso to Tripo / Meshy / Hunyuan3D. PBR on, quad/remesh on, high poly.

== If [B] SCENE MODULE ==
  CLEAN PLATE: (same clean-plate prompt as [A])
  2-3 VIEW TURNTABLE (run in Nano Banana Pro):
  "The [PROP] from the reference, as an orthographic turntable in ONE image:
   front | 3/4 [| back if asymmetric], equal panels left to right. IDENTICAL object in
   all panels — same geometry, proportions, materials, height and centering. Flat even
   diffuse lighting, neutral grey (#808080) background, NO shadows, strictly orthographic.
   Maximum sculptural detail, reconstruct occluded areas. Asset reference for multiview-to-3D."
  3D: Tripo 3.0 or Hunyuan3D 2.5, multi-view, texture high. If it is a low-relief
   panel, also export a height/displacement pass.

== If [C] REUSABLE/TILEABLE MODULE ==
  If tile/surface (floor, wall, ground):
  "Top-down orthographic flat texture tile of the [PROP]: perfectly SEAMLESS and
   TILEABLE on all 4 edges, square 1:1, shot straight from directly above, zero
   perspective, even diffuse light, NO directional shadow, NO baked highlight, scale
   matches a 1m x 1m module, flat de-lit albedo suitable as a PBR base color map."
  If discrete repeating object (candlestick, pillar, pot):
  Use the [A] 3-view turntable prompt, then instance/duplicate in-scene.
  3D: flat surfaces -> convert to PBR material (base + normal + height), no mesh;
   discrete objects -> Tripo single/multi-view, assemble a modular kit at a unified
   grid size so pieces snap together.

RULES
- Never invent objects not in the image; for hidden parts, infer from visible style and tag "(inferred)".
- PASS 1 extraction/3-view uses the plain [PROP] name + minimal boilerplate — the concept image is the reference; do NOT over-constrain with the dense [SPEC] (it makes the model re-invent and drift off-target).
- Apply [SPEC] anchors / STYLE BIBLE / occlusion / pose / material locks only as a PASS-2 correction on assets that actually drift — target the specific deviation, don't stack everything.
- For material/color, describe the TRUE de-lit albedo (not the scene-lit tint); if ambiguous, list 2 candidates + confidence.
- If a figure's pose/form drifts, lock POSE limb-by-limb in the correction pass; pose drift is a failure even if color and style are right.
- Preserve each asset's real design, material, color, proportions.
- One object per generated image; if a scene has >5 objects, batch them 3-4 at a time.
```

---

## 手動填空模板(只想處理單一物件時,不跑 Master Prompt 也能用)

> **★ 兩段式原則:第一次極簡(只填道具名 [PROP],讓原圖當依據)→ 偏了才加修正層(SPEC/風格/姿勢/材質鎖)。** 第一次塞太多文字 = 模型照文字重畫 = 偏離原圖。

### Template A — 英雄道具(四步:front → 確認 → 4 視圖 + 3/4 + 45°iso)
1. **去背攤平**(NBP/Seedream):把 `[A] CLEAN PLATE` 的 `[PROP]` 換成**道具名**(只填名字,別塞 SPEC),先出 front。
2. **確認 front** ── 對了再往下;不對先修(見〈🧭 一頁速查〉)。
3. **4 視圖 + 3/4 + 45°iso**(NBP):拿確認過的 front 當參考,跑 `[A] 4-VIEW TURNTABLE`、`[A] 3/4 HERO VIEW`、`[A] 45° ISO VIEW`。
4. **偏了才修**:結果跑掉 → 修正層(SPEC 錨點 / STYLE BIBLE / 鎖姿勢/材質,見下方各節)。
5. **3D**:多視圖→Rodin;單圖(3/4)→Tripo/Meshy/Hunyuan → 高模 PBR。

### Template B — 場景模組物件(2 視圖)
1. 去背攤平(同 A 的 CLEAN PLATE)。
2. 2 視圖(上方 `[B] 2-VIEW`)。
3. 3D：Tripo 3.0 / Hunyuan3D 2.5,multi-view。淺浮雕牆 → 另出 height pass。

### Template C — 可複用可拼模組(1 平拍)
- 平面類(地/牆) → `[C] tile/surface` 平拍 → **轉 PBR 材質**(別生 mesh)。
- 立體重複件(燭台/柱) → 走 A 的 4 視圖做 1 個 → 場景內陣列複製。
- **統一 grid 尺寸**(如 1m×1m),才能像積木拼。

---

## 精確描述 (Per-Asset Visual Spec) — 7 軸 + 姿勢 rubric ★

工作流的「精準」全靠這一步:**每個物件先寫 7 軸 SPEC,再把 SPEC(不是名字)填進提示詞。** 每次都套同一份 rubric,描述就穩定精準、不漏細節 ── 這就是「讓每次每個物件的描述更精準」的機制。

| 軸 | 問什麼 | 例(青銅香爐) |
|---|---|---|
| 1 FORM & SCALE | 輪廓·比例·真實尺寸 | 三足圓鼎,矮胖,約 40cm 高 |
| 2 PARTS | 結構零件拆解 | 爐身 + 雙立耳 + 拱形鏤空蓋 + 三獸足 |
| 3 MATERIAL & FINISH | 材質 + 表面處理 | 鑄造青銅,霧面 |
| 4 COLOR | 精確顏色含變化 | 青黑底,凹處銅綠 verdigris,耳緣磨亮露金 |
| 5 ORNAMENT | 雕飾·紋樣·銘文 | 腹部饕餮獸面浮雕,蓋頂蟠龍鈕 |
| 6 AGE / WEAR | 損耗狀態 | 香灰積垢,足部氧化斑,一處缺角 (inferred) |
| 7 SIGNATURE | 唯一識別特徵 | 蟠龍蓋鈕 + 饕餮獸面 |
| 8 POSE & GESTURE(人形/生物才填) | 逐肢位置·不對稱·手印 | 香爐非人形→免;守護神例:右臂抬起前伸、左手按膝、正坐 |

**壓成一句 [SPEC](就是要填進提示詞的東西):**
> *a squat three-legged bronze ding censer ~40cm tall, twin upright loop handles, pierced domed lid with a coiled-dragon finial, taotie beast-mask relief on the belly, three beast-claw legs; matte cast bronze, blue-black patina with verdigris in the recesses and rubbed-gold highlights on the rims, soot-stained, oxidized feet.*

這段 [SPEC] 是**盤點文件 + 修正層的依據**,第一次提取**不要**塞進 prompt(會讓模型照文字重畫而偏離原圖)。等出圖偏了,再從這裡挑「就是這一個」的錨點去修(見下方修正各節)。

**精準度自檢(每個 SPEC 過一遍,六項都過才送):**
☐ 7 軸都有具體值(沒有空軸)　☐ 顏色含「變化/磨損」不只一個平色
☐ 講出 1-2 個唯一特徵(SIGNATURE)　☐ 遮擋/推測處標了 (inferred)
☐ 材質/顏色標的是 TRUE albedo(不是被場景光染的色);低信心有列 2 個候選
☐ 人形/生物有填 POSE 軸(逐肢);2D 歧義姿勢有標信心

---

## 辨識錯誤修正 — 先講順序(組合錯誤必看)★

物件常常**姿勢 + 造型 + 顏色 + 材質一起錯**(像守護神那次)。修的順序很重要,順序錯會重工:

> **① 先鎖姿勢/造型(幾何)→ ② 再鎖顏色/材質(表面)→ ③ 最後鎖畫風(美術方向)。**

因為材質編輯預設「幾何不動」── 你若先修好顏色再改姿勢,顏色得重來。**幾何永遠先修。** 三段各有專節:姿勢/造型(下方)、顏色/材質、畫風(STYLE LOCK)。

---

## 姿勢 / 造型辨識錯誤 → 修正機制 ★

**會錯的根因:** ① 遮擋 ── 概念圖把下半身/手臂藏住(守護神下半身被供桌擋),AI 用猜的;② 透視前縮 ── 2D 壓縮讓 AI 誤判肢體位置;③ 2D 歧義 ── 一隻抬起的手在 3D 有多種解;④ 模型先驗 ── 給「典型對稱姿」(雙手放膝)取代特定不對稱姿;⑤ 單視圖 ── 只有正面時,側/背姿是 AI 編的。

> **顏色/材質錯好修(改表面、保幾何);姿勢/造型錯難修(要動幾何)。** 分開處理,大動作優先丟 3D。

| 情況 | 修法 | 為何 |
|---|---|---|
| 還沒生圖 / 姿勢中度偏 | 路徑 A:改 SPEC 的 POSE 軸逐肢重鎖,重生 | 文字逐肢鎖死 |
| 姿勢/造型明顯錯、要精準 | 路徑 B:給**姿勢參考圖**(最強) | 圖鎖姿勢 >> 文字 |
| 已生 3D / 大幅改姿 | 路徑 C:在 3D 裡 rig + 重擺 | 3D 擺姿比 2D 可靠太多 |

### 路徑 A — 改 SPEC 的 POSE 軸,逐肢重鎖(重生)
```
For asset [name], the pose/silhouette was misread. Lock the pose EXACTLY, limb by limb:
head [e.g. tilted slightly down]; right arm [raised, extended forward at shoulder height,
open palm, fingers spread]; left arm [low, resting on left knee]; legs [seated, knees
apart, left foot forward]; overall silhouette [squat and broad]. Keep material, ornament
and identity unchanged. Regenerate the turnaround.
```

### 路徑 B — 姿勢參考圖(最強)
給一張「正確姿勢」參考 ── 概念圖裁切、擺好姿的人偶/3D mannequin 截圖、甚至手繪火柴人標手臂位置:
```
Ref 1 = the asset (keep its design, material, ornament).
Ref 2 = pose reference (a posed figure / mannequin / stick-figure sketch).
Re-render the object from ref 1 in the EXACT pose and silhouette of ref 2. Keep ref 1's
design and material; take ONLY the pose / limb positions from ref 2. De-lit neutral light.
```
> 連火柴人草圖都有效 ── pose 是「空間關係」,圖比文字精準太多。

### 路徑 C — 已生 3D:在 3D 裡重擺姿(大動作首選)
- 大幅改姿(抬手、換坐站、轉頭)→ 模型 **rig 起來在 Blender 擺**,或 sculpt 微調。比讓 2D 模型「移動一隻手臂」(常崩)穩定可控太多。
- 訣竅:**生模時就用中性/對稱姿(T/A-pose 或正坐)**,複雜姿勢留到 3D ── 一開始別逼 AI 生難姿,後面更好控。

### 造型 / 比例錯(silhouette / proportion / 缺件)
- 缺件(漏頭光環)、比例錯(太修長)→ 屬幾何:走路徑 A(補進 FORM/PARTS 軸 + 概念圖當 ref)或 3D 補雕。
- 這類也吃下方 STYLE LOCK 的「概念圖當風格參考圖」修法。

---

## 顏色 / 材質辨識錯誤 → 修正機制 ★

**會錯的根因:** 8 成的顏色/材質誤判來自「概念圖的戲劇打光」騙了 AI ── 洞窟綠光、god-ray 橘光、紅幡反光,把石頭染成綠、把青銅染成金。所以 STEP 1.5 已要求標 **TRUE albedo + 低信心列 2 候選**,從源頭減少誤判。若還是辨識錯,照下面修,**不要整條重跑**。

**先判斷:錯在哪一段 → 用哪個修法(越早改越省):**

| 發現錯誤時 | 用修法 | 成本 |
|---|---|---|
| 還沒生圖(只有 SPEC) | 路徑 1:改 SPEC | 最低 |
| 圖生了、3D 還沒 | 路徑 2:image edit 改材質保幾何 | 低 |
| 3D 已生 | 路徑 3:retexture(不重生 geometry) | 中 |

### 路徑 1 — 改 SPEC(還沒生圖,首選)
只改材質/顏色軸,其他軸不動,重出該物件 SPEC + 提示詞:
```
For asset [name], the material/color was misidentified. Correct it: TRUE material =
[correct material], TRUE albedo color = [correct color]. Keep all other SPEC axes
(form, parts, ornament, wear, signature) unchanged. Re-output the [SPEC] phrase and
regenerate this asset's CLEAN PLATE and multi-view prompts only.
```

### 路徑 2 — 已生圖:只改材質、保幾何(NBP / Seedream / Flux Kontext)
**純文字版:**
```
Edit this asset plate. Keep the geometry, silhouette, proportions, ornament and
orientation EXACTLY unchanged. Change ONLY the surface material and color: re-render
as [correct material, e.g. dark patinated bronze with verdigris in the recesses],
TRUE albedo under even neutral light, de-lit matte, no colored light spill. Do not
alter shape, parts, or detail.
```
**附材質參考圖版(最可靠):**
```
Ref 1: the asset plate.  Ref 2: a material swatch / photo of [correct material].
Apply the material from ref 2 onto the object in ref 1. Strictly preserve ref 1's
geometry, silhouette, ornament and proportions; change only surface material and
color to match ref 2. Even neutral light, de-lit matte albedo.
```
> 給一張**真實材質照片**當 ref 2,是顏色/材質修正最穩的做法(Seedream `the material from ref N` + `strictly preserve`;NBP 多圖 blend;Flux Kontext 改材質)。

### 路徑 3 — 已生 3D:retexture(別重生 geometry)
- Rodin / Tripo / Meshy:用 **re-texture / texture-prompt** 重貼,或直接餵路徑 2 修好的正確 albedo 圖當貼圖來源;幾何不動。
- 或進 Blender / Substance 換材質球 ── 高模幾何保留,只換 PBR。

### 防錯小招(下次更不容易辨識錯)
1. **先去戲劇光再描述** ── 心裡把 god-ray / 彩色光拔掉,描 albedo。
2. **低信心就先問人** ── SPEC 標 (low) 的材質,生圖前先跟使用者確認一句,比事後重做省。
3. **存材質參考庫** ── 青銅/玉/漆木/砂岩各備 1 張真實照,辨識存疑就丟 ref 2 鎖死。

---

## 畫風 / 樣式漂移 → STYLE LOCK ★

顏色/材質修對後,最常見的下一個落差是 **畫風與樣式跑掉** ── 生成件技術上乾淨,但「不像同一個美術方向」:文化傳統漂移(中式石窟→日式仁王/印度神廟)、精緻度漂移(古樸風化→乾淨 ZBrush 高模)、比例漂移(矮壯→修長)、失去斑駁彩繪與筆觸。

**根因:** ① 模型套訓練先驗(講「守護神像」給最常見最精緻版);② turnaround 的「clean 3D reference」字眼推向乾淨渲染;③ prompt 只描述物件、沒鎖**美術方向**;④ 抽單件時丟掉概念圖這個風格錨。

### 修法 1 — STYLE BIBLE(從概念圖萃取一次,貼進每個 prompt)
```
STYLE BIBLE (append to EVERY asset prompt):
- TRADITION/ERA: [e.g. 5-6th c. Chinese Buddhist cave-grotto (Yungang/Longmen/Dunhuang)];
  NOT [e.g. Japanese Nio/Myo-o], NOT [e.g. Indian/Gandhara temple].
- STYLIZATION: [e.g. archaic, primitive, monumental, eroded] game-concept sculpt;
  NOT clean modern 3D render, NOT crisp ZBrush hard-surface, NOT museum-refined.
- PROPORTION: [e.g. squat, heavy, broad, large head and hands].
- SURFACE: [e.g. eroded stone / patinated bronze, chipped edges, faded polychrome
  pigment remnants — mineral blue / vermilion / gold in the recesses].
- MOOD: [e.g. painterly concept surfacing, muted atmospheric earth palette].
```

### 修法 2 — 用概念圖當風格參考圖(最強)
把概念圖裁到該物件當 ref,連同 prompt 一起送:
```
Ref = the asset cropped from the original concept. This is the SAME object from the
concept. Match its sculpting style, proportion, archaism and weathering EXACTLY;
change only the viewing angle and the lighting (to clean de-lit neutral). Do not
refine, re-stylize, or modernize the design.
```
> 文字鎖風格弱,**圖鎖風格強**。Seedream `the style/proportion of ref 1` + NBP 多圖一致性,把畫風咬住。

### 修法 3 — 反漂移負面句
對著你看到的漂移方向寫否定:`NOT Japanese Nio style` / `NOT clean ZBrush detail` /
`less refined, more eroded and archaic` / `squatter and heavier proportions` /
`keep remnant polychrome pigment`。

### 重要分界:風格 ≠ 打光
STYLE LOCK 只鎖**造型/比例/風化/文化傳統**,**不要**因此把戲劇打光加回來 ── turnaround 仍維持 de-lit 中性光(否則又踩 4 大殺手)。

### 風格自檢(每件出圖後比對概念圖,四項都對才過)
☐ 文化/年代傳統一致(沒跑成別國別代)　☐ 精緻度一致(沒被過度精修/3D 化)
☐ 比例語言一致(矮壯/修長對得上)　☐ 斑駁/彩繪/筆觸質感一致

---

## 通用品質金句 +「4 大殺手」

**金句(驗證過的標準,每張都要有):**
`From the attached concept art, extract ONLY the [PROP]` · `one complete, isolated object, centered and fully visible` · `front orthographic view` · `flat neutral grey (#808080) seamless background` · `perfectly even diffuse studio lighting` · `NO cast shadows / NO rim light / NO scene elements` · `maximum sculptural detail` · `high-resolution clean reference plate for image-to-3D`
**多視圖加(front 確認後):**`4-VIEW turntable in ONE image: front | left side | right side | back, four equal panels` · `IDENTICAL object in all panels — same geometry, proportions, materials, height and centering`
**3/4 立體 hero 加(給單圖轉 3D):**`single 3/4 hero view for image-to-3D` · `rotated ~35°, tilted ~25° from above` · `near-orthographic (no wide-angle distortion)` · `same geometry / proportions / materials as the front`
**45° 等角加(零變形單圖轉 3D):**`single 45-degree front-side angle` · `true 45-degree isometric projection (45° azimuth, ~30° downward tilt)` · `parallel projection, no perspective distortion, no vanishing point, centered`

**進 3D 前必殺的 4 個東西(出現任一 = 3D 必爛):**
1. ❌ 投影 / cast shadow　2. ❌ rim light / god rays / 邊緣光
3. ❌ 景深模糊 DoF / 動態模糊　4. ❌ 高反差戲劇打光(要攤平成 albedo)

---

## 3D 工具路由表

| 類別 | 輸入 | 工具 + 設定 | 輸出 |
|---|---|---|---|
| [A] 英雄件 | 4 視圖 + 3/4 + 45°iso | **Rodin Gen-2** 多圖 / **Tripo·Meshy** 單圖(3/4 或 45°iso),PBR+quad remesh,high poly | 高模+PBR → ZBrush/Blender 精修 |
| [B] 場景件 | 單件+2 視 | **Tripo 3.0 / Hunyuan3D 2.5** multi-view,texture 高 | 中模+貼圖 |
| [C]-立體 | 4 視圖×1 | Tripo 單/多視 → 模數化 kit | 低模可拼件 |
| [C]-平面 | top-down 平拍 | **轉 PBR 材質**(base+normal+height),不生 mesh | 可無限平鋪 |

---

## 命名 / 資料夾規範(讓工作流可重複、可交接)

```
/<project>/
  inventory.csv              # Master Prompt 的清單表存這
  /hero/<name>/   plate.png  turnaround.png  model.glb
  /module/<name>/ plate.png  2view.png       model.glb
  /kit/<name>/    tile.png   material/        model.glb
```

---

## QC 檢查表(每張進 3D 前過一遍)

- ☐ 純中性背景、物件完整不裁切
- ☐ 無投影、無 rim light、無 god rays、無景深模糊(4 大殺手)
- ☐ de-lit 攤平,albedo 看得清(非高反差戲劇光)
- ☐ 多視圖之間:同一物件、同尺寸、同對齊
- ☐ 模組件四邊可無縫平鋪;統一 grid 尺寸
- ☐ 被遮擋部位已補全

---

## 範例輸出(以中式洞窟廟宇圖示範 Master Prompt 會吐什麼)

| # | asset | 類 | 數量 | 遮擋 | 視圖 |
|---|---|---|---|---|---|
| 1 | 力士/天王坐像(鎧甲·火焰冠) | B | 1 | 下半身被供桌擋,需補 | 2 |
| 2 | 佛教浮雕牆板 | B | 2 | 邊緣裁切,需補 | 2 |
| 3 | 青銅鼎/香爐 | **A** | 1 | 腳部被擋 | 4 |
| 4 | 烏鴉 | A | 3 | 無 | 4 |
| 5 | 燭台/燈台 | **C** | 6 | 無 | 4(做1個複製) |
| 6 | 供桌/長案 | B | 1 | 無 | 2 |
| 7 | 石板地磚 | **C** | 鋪滿 | 無 | 1 平拍→PBR |
| 8 | 紅地毯 / 玫瑰花瓣 | C | 鋪滿 | 無 | 平拍→材質+scatter |

→ 接著 Master Prompt 會對 #1~#8 各自吐出填好的去背 / 多視圖 / 3D 提示詞區塊。

---

## 三個現實提醒

1. **AI 高模拓撲是亂的**(三角網)。當數位雕塑/基模很好,進引擎仍需 retopo + 烘法線。
2. **多視圖 >> 單視圖** ── 願意多出 turnaround,3D 品質跳級,別省。
3. **地/毯/花瓣別硬建模** → 走 PBR 材質 + scatter,省 10 倍且更可控,這才是「可拼場景」正解。

---

## 連結

- Nano Banana Pro(拆分/多視圖一致性)→ [../references/nano-banana.md](../references/nano-banana.md)
- Seedream 5.0(中式文物材質)→ [../references/seedream.md](../references/seedream.md)
- Flux Kontext(去背/局部編輯)→ [../references/flux.md](../references/flux.md)
- 結果有瑕疵的修法 → [../references/quality-control.md](../references/quality-control.md)
