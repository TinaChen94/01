# 實戰紀錄 — A2 中式石窟佛教浮雕牆 Buddhist Relief Wall

> 概念圖拆資產 / concept→3D 案例。對應工作流:`ai-media-generator` 的 concept-to-3D pipeline(`templates/concept-to-3d-pipeline.md`)。
> 資產分類:**[B] 場景模組件**(大型、結構性、淺浮雕牆板 → 2 視圖 + height pass)。

## 來源(索引)
- **生成平台:** Nano Banana Pro(推薦主跑,轉正+結構一致最強)/ Seedream 5.0(中式文物材質備援) — 實際平台待本人補
- **日期:** 2026-06-24
- **原始素材:** 洞窟佛寺概念圖中,左側藍底彩繪佛教浮雕牆(主尊立佛 + 四脇侍菩薩 + 上方飛天/祥雲)
- **前一案例:** [A1 哥德陵墓](A1-mausoleum.md)

---

## 用到的 prompt(逐字保存)

### 1. STEP 1 — FRONT 正交底板(斜退牆 → 轉正 + 去戲劇光)
原概念圖的牆是往深處斜退的,本句靠 `re-orient … IGNORE camera angle` 轉成 head-on 正交,並剝掉 god ray / 洞窟綠光 / 紅幡反光 / 燭光。
```text
From the attached concept art, extract ONLY the Buddhist relief wall panel (the LEFT
carved stone wall: blue-ground painted relief with standing bodhisattva/Buddha figures
in arched niches) and re-orient it to a true head-on FRONT orthographic view — camera
perpendicular to the wall face, at eye level, the panel facing the viewer directly;
IGNORE the concept's camera angle and perspective (do NOT copy the receding/angled 3-4
view). Re-render as one complete, isolated flat wall panel, centered and fully visible,
on a flat neutral grey (#808080) seamless background. Perfectly even diffuse studio
lighting, de-lit TRUE albedo, NO cast shadows, NO rim light, NO god rays, NO green cave
glow, NO red banner light spill, NO scene elements. Maximum carved-relief and polychrome
detail, reconstruct cropped edges. High-resolution clean reference plate for image-to-3D.
```

### 2. STEP 2 — 2 視圖(front 確認後;第二視用 3/4 掠射讀浮雕深度)
```text
The Buddhist relief wall panel from the confirmed front plate, as an orthographic
turntable in ONE image: front | 3/4 raking angle (camera ~35° to the wall to reveal
relief depth and how far each figure projects from the back plane), two equal panels
left to right. IDENTICAL panel in both — same geometry, proportions, materials, height
and centering. Flat even diffuse lighting, neutral grey (#808080) background, NO shadows,
strictly orthographic (no perspective). Maximum carved-relief detail, reconstruct
occluded and cropped areas. Asset reference for multiview-to-3D.
```

### 3. height / displacement pass(淺浮雕牆必出)
```text
A height / displacement map of the same Buddhist relief wall panel, head-on orthographic,
perfectly flat front view: pure grayscale where WHITE = nearest (figures projecting
forward) and BLACK = deepest (back plane / recesses), smooth tonal gradient following
carved depth, no color, no lighting, no cast shadows. Aligned 1:1 with the front albedo
plate. For displacement / normal baking.
```

### 4.(修正層,出圖偏才加)清場 pass — 把殘留供桌/燭台/壁龕刪掉
本次 STEP 1 殘留了 in-situ 供桌與壁龕(見下方 QC),需要這句針對性清場:
```text
Edit this plate. Keep the relief wall panel EXACTLY unchanged (geometry, figures,
polychrome, proportions). Remove everything that is NOT the relief panel: the stone
altar table, the bronze censer, the brass candlesticks and lit candles, the scattered
rose petals, and the two side wall niches with birds. Crop to the relief panel only,
extend the background to flat neutral grey (#808080), de-lit even diffuse light, no
flames, no warm glow.
```

---

## 產出

### 正視參考板(head-on 正交,image-to-3D 用)
![浮雕牆正視參考板](images/buddhist-relief-wall-front-ortho.png)

> ⚠️ **圖待存入** — 把對話裡生成的 front plate 另存為 `images/buddhist-relief-wall-front-ortho.png`(對齊上方引用名)。

head-on 正交、主尊立佛施無畏印 + 四脇侍 + 上方飛天祥雲、藍底彩繪、風化石材 —— 風格與轉正都成立;但**尚未清場 / 尚未完全去光**(見下)。

---

## 學到的(可複用結論)

- ✅ **`re-orient … IGNORE the concept's camera angle/perspective` 對「斜退的建築牆板」成立。** 原圖那面往深處斜退的牆被成功壓成 head-on 正交立面 —— 印證 concept-to-3D 〈核心鐵律〉那句不只對小道具有效,對大牆板一樣鎖得住視角。
- ✅ **STYLE 不靠 PASS-2 STYLE BIBLE 就咬住了。** 純 image-grounded extract 就保住 5–6 世紀中式石窟風、礦物藍/朱/金斑駁彩繪、風化崩缺石材,**沒漂成日式仁王 / 印度神廟**。→ 印證「原圖=真相,文字只寫呈現規格」勝過堆設計文字。
- ⚠️ **`NO scene elements` 只被執行一半 —— 這是本案最大教訓。** 模型保留了 in-situ 的**供桌、青銅鼎、燭台、點燃蠟燭、玫瑰花瓣、左右壁龕 + 鳥**,背景也不是純 `#808080`。
  → **修法:列點刪 > 泛詞否定。** 與其寫 `NO scene elements`,不如逐項點名要刪的東西(見上方 prompt 4),對「牆板帶附屬供桌」這種 in-situ 構圖才清得乾淨。
- ⚠️ **蠟燭是點燃的 = 殘留小光源 + 暖調溢光**,踩到「4 大殺手」之一。進 image-to-3D 前必跑一次清場 + 去光 pass,否則火焰/暖光會被烤進貼圖。
- 📌 **下一步序列:** 清場 pass(prompt 4)→ 比對原圖確認 → STEP 2 兩視圖(front | 3/4 掠射)→ height pass → 餵 Tripo 3.0 / Hunyuan3D 2.5 multi-view → 中模 + 貼圖,淺浮雕細節用 height 做位移。
- 📌 右牆(立佛列 + 大坐佛浮雕)是另一塊獨立牆板,另開一輪同模板,只換 `[PROP]` 描述。
