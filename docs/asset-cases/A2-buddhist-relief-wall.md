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

### 5.(重出版,本次採用)以 #4 清場板為基準重出 2 視圖 + height
盲生的 #2 #3 繼承了供桌/壁龕(見 QC),改餵 `buddhist-relief-wall-cleaned-ortho.png` 重出,並在句中再鎖一次隔離:

**5a — 2 視圖(重出):**
```text
Using the attached CLEANED relief-wall plate (already isolated — no altar, no
candlesticks, no candles, no side niches, no scene props) as the single source of truth,
render it as a 2-VIEW orthographic turntable in ONE image: front | 3/4 raking angle
(camera ~35° to the wall face to reveal relief depth and how far each figure projects
from the back plane), two equal panels left to right. IDENTICAL panel in both — same
geometry, proportions, polychrome, height and centering as the source. Keep it fully
isolated: NO altar, NO candles, NO niches, NO scene elements. Flat even diffuse lighting,
neutral grey (#808080) background, NO cast shadows, strictly orthographic (no perspective).
Maximum carved-relief detail, reconstruct cropped/occluded areas. Asset reference for
multiview-to-3D.
```
**5b — height(重出):**
```text
A height / displacement map of the attached CLEANED relief-wall plate (the isolated panel
only — no altar, no candlesticks, no niches). Head-on orthographic, perfectly flat front
view: pure grayscale where WHITE = nearest (figures and halo projecting forward) and
BLACK = deepest (blue back plane / recesses), smooth tonal gradient following carved depth,
no color, no lighting, no cast shadows, no scene props. Aligned 1:1 with the cleaned front
albedo plate. For displacement / normal baking.
```
> 跑法:參考圖放 #4,兩張同 seed,重出後覆蓋 `buddhist-relief-wall-2view.png` / `-height.png`(舊盲生版留存改 `-blind` 後綴)。

---

## 產出(4 張,依 4 組提示詞順序生成)

| # | 提示詞 | 檔名(存到 `images/`) | 說明 |
|---|---|---|---|
| 1 | STEP 1 FRONT | `buddhist-relief-wall-front-ortho.png` | head-on 正交、主尊施無畏印 + 四脇侍 + 飛天祥雲、藍底彩繪;風格/轉正成立,**但殘留供桌/燭台/壁龕**(未清場、未完全去光) |
| 2 | STEP 2 2 視圖 | `buddhist-relief-wall-2view.png` | front \| 3/4 掠射,讀得出牆板厚度與浮雕凸出量;**繼承了 #1 的供桌/壁龕**(盲生,未先清場) |
| 3 | height pass | `buddhist-relief-wall-height.png` | 灰階深度圖,近白遠黑;**同樣帶進供桌**,需以清場後的板重出 |
| 4 | 清場 pass | `buddhist-relief-wall-cleaned-ortho.png` | 供桌/燭台/壁龕已刪、裁切到牆板、灰底 —— **這張才是乾淨的 image-to-3D 正視板** |

![1 正視板(未清場)](images/buddhist-relief-wall-front-ortho.png)
![2 兩視圖](images/buddhist-relief-wall-2view.png)
![3 height map](images/buddhist-relief-wall-height.png)
![4 清場後正視板](images/buddhist-relief-wall-cleaned-ortho.png)

> ⚠️ **4 張圖待存入** `docs/asset-cases/images/`,檔名對齊上表(我無法把對話裡的圖轉存進 repo)。

---

## 學到的(可複用結論)

- ✅ **`re-orient … IGNORE the concept's camera angle/perspective` 對「斜退的建築牆板」成立。** 原圖那面往深處斜退的牆被成功壓成 head-on 正交立面 —— 印證 concept-to-3D 〈核心鐵律〉那句不只對小道具有效,對大牆板一樣鎖得住視角。
- ✅ **STYLE 不靠 PASS-2 STYLE BIBLE 就咬住了。** 純 image-grounded extract 就保住 5–6 世紀中式石窟風、礦物藍/朱/金斑駁彩繪、風化崩缺石材,**沒漂成日式仁王 / 印度神廟**。→ 印證「原圖=真相,文字只寫呈現規格」勝過堆設計文字。
- ⚠️ **`NO scene elements` 只被執行一半 —— 這是本案最大教訓。** 模型保留了 in-situ 的**供桌、青銅鼎、燭台、點燃蠟燭、玫瑰花瓣、左右壁龕 + 鳥**,背景也不是純 `#808080`。
  → **修法:列點刪 > 泛詞否定。** 與其寫 `NO scene elements`,不如逐項點名要刪的東西(見上方 prompt 4),對「牆板帶附屬供桌」這種 in-situ 構圖才清得乾淨。
- ⚠️ **蠟燭是點燃的 = 殘留小光源 + 暖調溢光**,踩到「4 大殺手」之一。進 image-to-3D 前必跑一次清場 + 去光 pass,否則火焰/暖光會被烤進貼圖。
- ⚠️ **本批是「盲生」4 張 —— 沒先確認 CLEAN front 就往下跑,結果 #2 兩視圖、#3 height 都繼承了 #1 的供桌/壁龕。** 正好踩中 pipeline〈三視一致性協議〉警告的「別三張盲生」。**正確順序應是 FRONT → 清場(#4)→ 確認乾淨 → 才用乾淨板出 #2 兩視圖 + #3 height。** → 目前 #2 #3 需以 `buddhist-relief-wall-cleaned-ortho.png` 為基礎重出一次。
- 📌 **下一步序列:** 以 #4 清場板為基準 → 重出 2 視圖(front | 3/4 掠射)+ height pass(都從乾淨板來)→ 餵 Tripo 3.0 / Hunyuan3D 2.5 multi-view → 中模 + 貼圖,淺浮雕細節用 height 做位移。
- 📌 右牆(立佛列 + 大坐佛浮雕)是另一塊獨立牆板,另開一輪同模板,只換 `[PROP]` 描述。
