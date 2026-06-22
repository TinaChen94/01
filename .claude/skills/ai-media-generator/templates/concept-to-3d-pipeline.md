# Concept Art → 3D 資產拆分工作流 (Concept-to-3D Asset Pipeline)

**用途：** 丟「任一張」參考圖 / concept art，自動產出 ① 資產清單(分 3 類) ② 每個物件各自對應的去背 / 多視圖 / 3D 提示詞。給遊戲/影視/3D 列印的高模生成前置。

**核心心法：** 沒有真正的「一鍵」。圖上那種乾淨拆解圖是 4 段管線的產物 ──
`①盤點分類 → ②單件去背攤平 → ③正交多視圖 → ④影像轉3D`。
②③ 做得乾不乾淨，直接決定 ④ 成敗。最大殺手是把「概念圖的戲劇打光版」直接丟進 3D AI(god rays / 紅光 / 景深會被烤進貼圖)。所以拆分階段的第一要務是 **去戲劇光、攤平、去背、補全遮擋**。

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
| **[A] 英雄道具** 單件精修·3視圖重建 | 小~中、唯一、細節吃重、會被特寫 | **4 視圖** | 高模 + PBR,Rodin 多圖 |
| **[B] 場景模組物件** | 大型/結構性、定義空間、唯一或少量、中景看 | 2 視圖 | 中模,Tripo/Hunyuan |
| **[C] 可複用可拼模組** | 重複 ≥3 次 **或** 格狀/可平鋪(地磚/牆段/階梯/柱/燭台陣列) | **1 正交平拍** | 低模 **或 PBR 材質**,模數化拼接 |

**對每個物件套這個順序判斷：**
1. 重複 ≥3 次 **或** 是 tile/格狀(地/牆/階/柱/欄)？→ **[C]**
2. 否則,大型/結構性/定義房間(神像/大浮雕/寶座/大家具)？→ **[B]**
3. 否則(小、唯一、細節吃重、英雄互動)？→ **[A]**

---

## ★ 主控生成器 Master Prompt(核心:貼這段 + 任一參考圖到視覺 LLM)

> 輸出 = 清單表格 + 每個物件的「可直接複製」提示詞。這就是「放任一張圖都能自動出清單與對應 prompt」的引擎。

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
  3. MATERIAL & FINISH — exact material + surface finish (e.g. patinated cast bronze,
     lacquered wood, weathered painted sandstone)
  4. COLOR — precise colors incl. variation, gilding, staining
  5. ORNAMENT / SURFACE DETAIL — carvings, motifs, relief, inscriptions, patterns
  6. AGE / WEAR STATE — chips, cracks, moss, soot, dust, verdigris, repairs
  7. SIGNATURE FEATURE — the 1-2 details that uniquely identify THIS object
Then compress the 7 axes into ONE dense phrase (~20-40 words, 5-8 high-signal
descriptors). That phrase is the asset's [SPEC]. Print it under the asset's table row.

STEP 2 — AUTO-GENERATE PROMPTS
For EVERY asset, output a block with ready-to-paste prompts using the template for
its category. Replace every [asset SPEC] slot with that asset's full [SPEC] phrase
from STEP 1.5 — never the bare name; the dense spec is what makes extraction and 3D
accurate. Keep code blocks clean (no commentary inside). Output prompts in English;
keep cultural nouns precise.

== If [A] HERO PROP ==
  CLEAN PLATE (run in Nano Banana Pro / Seedream):
  "Using the reference, extract and isolate the [asset SPEC]. Re-render as a single
   3D-asset plate: pure neutral grey #808080 background, centered, fully visible;
   even soft studio light, NO cast shadow, NO rim light, NO god rays, NO color spill;
   de-lit matte so albedo is readable; orthographic front, no perspective, no DoF
   blur; preserve exact design, material, color, proportions; reconstruct any hidden
   or cropped parts. Single object only."
  4-VIEW TURNAROUND (run in Nano Banana Pro):
  "Orthographic turnaround of the [asset SPEC], 4 views in one horizontal row on pure
   white: FRONT | LEFT SIDE | BACK | 3/4. Identical scale, alignment and height;
   the SAME object in every view with consistent design/material/color/detail; even
   flat light, no shadow, no perspective; de-lit matte; 3D-modeling reference style."
  3D: Rodin Gen-2, multi-image input (feed all 4 views), PBR on, quad/remesh on,
   high poly. Alt: Tripo 3.0 multi-view.

== If [B] SCENE MODULE ==
  CLEAN PLATE: (same clean-plate prompt as [A])
  2-VIEW (run in Nano Banana Pro):
  "Orthographic two-view of the [asset SPEC] on pure white: FRONT | 3/4. Same object,
   identical scale, even flat light, no shadow, no perspective, de-lit matte,
   reconstruct hidden parts."
  3D: Tripo 3.0 or Hunyuan3D 2.5, multi-view, texture high. If it is a low-relief
   panel, also export a height/displacement pass.

== If [C] REUSABLE/TILEABLE MODULE ==
  If tile/surface (floor, wall, ground):
  "Top-down orthographic flat texture tile of [asset SPEC]: perfectly SEAMLESS and
   TILEABLE on all 4 edges, square 1:1, shot straight from directly above, zero
   perspective, even diffuse light, NO directional shadow, NO baked highlight, scale
   matches a 1m x 1m module, flat de-lit albedo suitable as a PBR base color map."
  If discrete repeating object (candlestick, pillar, pot):
  Use the [A] 4-view turnaround prompt, then instance/duplicate in-scene.
  3D: flat surfaces -> convert to PBR material (base + normal + height), no mesh;
   discrete objects -> Tripo single/multi-view, assemble a modular kit at a unified
   grid size so pieces snap together.

RULES
- Never invent objects not in the image; for hidden parts, infer from visible style and tag "(inferred)".
- Every prompt must carry the asset's full [SPEC] (7-axis dense phrase), not the bare name.
- Preserve each asset's real design, material, color, proportions.
- One object per generated image; if a scene has >5 objects, batch them 3-4 at a time.
```

---

## 手動填空模板(只想處理單一物件時,不跑 Master Prompt 也能用)

### Template A — 英雄道具(4 視圖)
0. **先寫 7 軸 SPEC**(見下節「精確描述」)── 這段精確描述才是要填的內容,不是只填名字。
1. **去背攤平**(NBP/Seedream):把 `[A] CLEAN PLATE` 的 `[asset SPEC]` 換成那段 SPEC。
2. **4 視圖**(NBP):同一段 SPEC 套進 `[A] 4-VIEW TURNAROUND` 的 `[asset SPEC]`。
3. **3D**：Rodin Gen-2 → 上傳 4 視圖 → PBR + quad remesh + high poly。

### Template B — 場景模組物件(2 視圖)
1. 去背攤平(同 A 的 CLEAN PLATE)。
2. 2 視圖(上方 `[B] 2-VIEW`)。
3. 3D：Tripo 3.0 / Hunyuan3D 2.5,multi-view。淺浮雕牆 → 另出 height pass。

### Template C — 可複用可拼模組(1 平拍)
- 平面類(地/牆) → `[C] tile/surface` 平拍 → **轉 PBR 材質**(別生 mesh)。
- 立體重複件(燭台/柱) → 走 A 的 4 視圖做 1 個 → 場景內陣列複製。
- **統一 grid 尺寸**(如 1m×1m),才能像積木拼。

---

## 精確描述 (Per-Asset Visual Spec) — 7 軸 rubric ★

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

**壓成一句 [SPEC](就是要填進提示詞的東西):**
> *a squat three-legged bronze ding censer ~40cm tall, twin upright loop handles, pierced domed lid with a coiled-dragon finial, taotie beast-mask relief on the belly, three beast-claw legs; matte cast bronze, blue-black patina with verdigris in the recesses and rubbed-gold highlights on the rims, soot-stained, oxidized feet.*

把這段塞進 CLEAN PLATE / 4-VIEW 的 `[asset SPEC]`,出圖與 3D 才會精準到「就是這一個」,而非泛泛的香爐。

**精準度自檢(每個 SPEC 過一遍,四項都過才送):**
☐ 7 軸都有具體值(沒有空軸)　☐ 顏色含「變化/磨損」不只一個平色
☐ 講出 1-2 個唯一特徵(SIGNATURE)　☐ 遮擋/推測處標了 (inferred)

---

## 通用品質金句 +「4 大殺手」

**金句(每張去背攤平圖都要有):**
`pure neutral grey #808080 / white background` · `even flat studio light` · `de-lit matte, readable albedo` · `orthographic, no perspective` · `single object, fully visible` · `reconstruct hidden parts` · `preserve exact design/material/color`

**進 3D 前必殺的 4 個東西(出現任一 = 3D 必爛):**
1. ❌ 投影 / cast shadow　2. ❌ rim light / god rays / 邊緣光
3. ❌ 景深模糊 DoF / 動態模糊　4. ❌ 高反差戲劇打光(要攤平成 albedo)

---

## 3D 工具路由表

| 類別 | 輸入 | 工具 + 設定 | 輸出 |
|---|---|---|---|
| [A] 英雄件 | 4 視圖 | **Rodin Gen-2** multi-image,PBR+quad remesh,high poly | 高模+PBR → ZBrush/Blender 精修 |
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
