# 實戰紀錄 — B8 寫實貼圖 → 手繪風格化(style transfer)提示詞配方

> 寫實風四方連續地面貼圖 → 《Ruined King》/ Battle Chasers 級手繪厚塗風格。
> 對應工作流:`ai-media-generator`;前置知識:[B1](B1-forest-bg-4k-detail.md)(鎖句字典)、
> [B2](B2-greybox-module-pipeline.md)(圖案活化/材質色票板/頂光)、
> [B3](B3-fenske-painterly-4k.md)(手繪風 × NB2 保真 pass 禁忌)。

**🔑 關鍵字:** `B8`、`風格轉換`、`手繪風格化`、`style transfer`、`厚塗`、
`hand-painted`、`Ruined King 風`、`四方連續風格化`、`tileable 風格轉換`、
`筆觸化`、`寫實轉手繪`

**狀態:✅ 配方定版 + 七張套圖量產完成(2026-07-14)** — v3(定調)+ v4.2(量產)
兩段式;master(`_B`)+ 六張 tile + 色票板庫(通用 ×3 / `_C` 專屬 / v3 風格板)
全數入庫(見〈產出對照〉)。歷程 v1→v4.2 的七次踩坑在下方查詢區。
**待辦:Match Color 對齊、雙層驗縫(Offset + 套內互拼)、引擎 3×3 鋪排驗收。**

> 📖 **本檔結構:上半 = 生產區(流程 + 逐字 prompt,拿了就用);
> 下半 = 查詢區(風格解剖/踩坑/鎖句字典/版本歷程,給日後 Claude 與除錯用)。**
>
> **狀態標記:`✅ 實戰驗證` = 本輪真的跑通(v3/v4.2/master 色票板/拼板庫/
> 相機距離分區合成);`📝 提案未驗證` = 我預先備妥、尚未實測(縫帶修復、
> 備援 A 拼貼統一法、備援 B 全圖透明度版與輕量統一 pass)— 別當成已驗證。**

**🔗 連結:**
[Leonardo 產圖](https://app.leonardo.ai/generation/image/reference-image-1-layout-guide-seamless-tileable-8d8b1b2a-e121-49da-8d13-abc896ac3cbf)
· [對話紀錄(攻關全程)](https://claude.ai/code/session_01Gif5qPYdeoPTbF7HyHv9Ka)

## 🪄 日後複用:一句話召喚本流程

> **對 Claude 說:「照 B8 配方做一套新套圖」**(或 `B8`／`手繪風格化`／
> `風格轉換套圖`)+ 一句主題,例:「照 B8 做一套**雪地**地磚套圖,X 張,
> 目標風格 OO」。

**附帶給 Claude 4 樣(缺了會被問):**
1. 寫實原圖(每張 tile 的 ref 1,滿版 1:1)
2. 目標風格參考(遊戲截圖/概念圖 → 裁風格板)
3. 張數與類型(純底/走道/轉角…)
4. 色域特例(有無特殊色需專屬板,如 `_C` 棕紅土)

Claude 自動跑:`v3 定調(挑 master)→ 裁 master 色票板 → v4.2 逐張量產
→ Match Color → 驗縫 → 引擎驗收`,遇坑查下方〈踩坑紀錄〉對症。
⚠️ 非有機材質(地磚/建築)另有難點,見下方〈跨主題適用性〉。

---

# 🟢 生產區

## 🎯 定調 → 量產 兩段式流程(核心)

> 適用於每個新關卡 / 新材質套。核心:**v3 = 探索模式(高變異是特性)、
> v4.2 = 錨定模式(像素級釘死)** — 兩者的變異度差在 ref 2 的性質:
> 泛用風格參考只給「畫法方向」,筆觸落點每抽浮動(2% 是天花板不是定值
> + NB2 無 seed);master 色票板則是筆觸的實體樣本,照著畫。

1. **定調段(v3):** 拿該套最有代表性的一張 tile,開 4–8 挑 1 —
   **筆觸大小與色盤一起挑**(選中者 = 整套的基因);
2. 選中的成品 = **master → 裁成 master 色票板**(細則見 v4.2 前置);
3. **量產段(v4.2):** 其餘 tile 全掛 master 色票板,
   變異從「風格浮動」縮到「抽卡微差」,開 4 挑 1;
4. **收尾:** Match Color 對 master → 雙層驗縫 → (要 4K)純保真放大。

三條鐵律:
- **一次一張、單張滿版**(多張合一生成 = 必爛,見踩坑 #5);
- **同套所有 tile 同一輸出解析度**(筆觸是絕對像素量);
- **風格化成品絕不回鍋 NB2 放大**(B3 鐵證;要 4K 走 Topaz / Real-ESRGAN /
  UU 最低 creativity)。

## 平台設定(Leonardo.ai AI Creation)

| 設定 | 值 | 備註 |
|---|---|---|
| Model | Nano Banana 2 | |
| Image Dimensions | **1:1(2048×2048)** | 輸入 1:1 → 輸出比例對齊(B1 鐵律);1024→2048 = 2× 安全倍率 |
| Prompt Enhance | None(首選)/ Auto 可接受 | 🆕 實測(2026-07-14):**Auto 依 prompt 長度判斷,B8 這種 300 字級鎖句長文不會被改寫**,v3/v4.2 全程 Auto 下通過。但 Auto 門檻是黑盒,能選 None 就選 None |
| Style | None | 避免疊色調,與色盤指令衝突 |
| **Use Fixed Seed**(Advanced Settings) | **On,全套同一 seed** | 🆕 2026-07-14 實戰發現:Leonardo 介面有固定 seed(先前誤判 NB2 無 seed)。固定 seed 可稍降輪間變異、提高成功率 — **定調段抽中 master 時把 seed 記進紀錄,量產全套沿用**。注意:seed 只是降變異,錨鏈(master 色票板)仍是主防線 |
| Private Mode | On | |

## ① v3 — 定調用完整提示詞(探索模式)

**參考圖:ref 1 = 該張寫實 tile(滿版單張)、ref 2 = 泛用風格拼板**
(目標遊戲的無角色/無 UI 環境圖 2×2,或材質特寫色票板)。
開 4–8 挑 1,選中者升格 master。

```text
Reference image 1 is the LAYOUT GUIDE — a seamless, tileable ground
texture (near top-down): green moss slopes with exposed dirt and a
sandy path along the bottom. Take from it ONLY: the moss / dirt / path
distribution layout, the texture scale, and the square 1:1 canvas.

Reference image 2 is the STYLE TARGET — material swatches from a
hand-painted stylized game. The finished image must look like it was
painted by the same artist with the same brushes.

TASK: paint a completely NEW hand-painted game texture from a blank
canvas, following reference 1's layout. This is a FULL REPAINT, not an
edit: no photographic pixels from reference 1 may survive. Every area
must show visible, deliberate brush marks — if any region still looks
like a photo, that region is wrong. Painterly but disciplined, like a
professional hand-painted ground texture, NOT a loose concept sketch.

BRUSH SCALE: strokes stay SMALL — the largest single visible stroke no
wider than 2% of the canvas: small dabs and speckles for moss, short
strokes for twigs and litter. NO long sweeping strokes, no large
gestural swirls, not impressionistic. Detail stays DENSE: many small
crisp shapes, each with 2-3 value steps — stylized does not mean
simplified.

MOSS: low rounded cushions with fine speckled granularity, same clump
size as reference 1 — not leafy fronds, ferns, bushes or side-view
foliage; everything reads as flat ground seen from above.

LAYOUT & TILING: keep the square 1:1 canvas (no crop, zoom or
outpaint) and reference 1's macro distribution of moss / dirt / path.
The texture must be SEAMLESSLY TILEABLE — left/right and top/bottom
edges wrap perfectly.

STYLE DETAILS: stepped value planes, hue-shifted shadows leaning teal
instead of black, crisp painted edge accents, gouache-like matte
finish. PALETTE: natural daylight green-and-earth tones matching
reference 1. LIGHTING: soft zenith light only — no horizontal light
direction, no cast shadows.

Do NOT add objects: no plants, flowers, mushrooms, standing grass
tufts, stones, props, characters or footprints.
```

**色盤變體句(擇一,取代 PALETTE 句):**

保留輸入自然色(預設):
```text
PALETTE: keep the natural daylight green-and-earth palette of
reference 1 — take only the PAINTING TECHNIQUE from reference 2, not
its color grading.
```

轉夜森林青綠色(接 B1/B2 世界觀):
```text
PALETTE: shift the whole texture into the muted dark teal-green night
palette of reference 2 — deep teal-shadowed moss, cool grey-brown
soil — while keeping the moss / dirt / path distribution pattern of
reference 1 unchanged. Do not brighten.
```

## ② v4.2 — 量產用完整提示詞(錨定模式,含反鏡像鎖)

**前置:master 色票板製作。** PS 從 master 成品裁 4–6 塊無構圖材質特寫
(苔區 ×2–3、深土區 ×1–2、路面 ×1),拼成 1:1 方板 = ref 2。細則:

1. **裁塊一律 100% 原尺寸**,禁止放大(放大 = 尺度錨被帶大);
2. **不帶任何交界線**(路緣/分區邊界 = 形狀資訊 = 滲漏載體;路面只裁內部);
3. **不收暗部漸層/模糊區塊**(糊塊會被學成「模糊也是風格」);
4. **「清晰」= 筆觸級清晰,不是照片級清晰**:放大 100%,
   能數出一筆一筆的色塊 → 進板;看得到毛絲/碎石顆粒/照片雜訊 → 不進板
   (那是 master 重繪不徹底的區域,進板 = 教模型畫照片);
5. **格數不用湊滿** — 4–6 格全純勝過 9 格摻照片塊,好區域可重複裁。
6. **板的色域必須涵蓋該張 tile 的所有材質色**(2026-07-14 實戰,`_C` 案例):
   「禁新色相條款」是雙面刃 — 防套外色,但 **tile 該有、板上沒有的色
   也會被 clamp 掉**(`_C` 棕紅土 + 通用板 → 被拉成土黃)。
   特殊色域的 tile 要配**專屬板**(在板上補該色的材質塊)。

**🗂 拼板庫制(實戰運作方式,2026-07-14 定型):**

| 板 | 用途 | 備註 |
|---|---|---|
| 通用板 ×1–3 | v4.2 量產,一般 tile | 偶發:ref 1 剛好有與板相似的色塊時會被牽引 → 換另一張通用板試 |
| 特殊色域專屬板 | 色域特殊的 tile(如 `_C` 棕紅土) | 通用板會把特殊色 clamp 成板上最近色;專屬板補該色塊即解 |
| 泛用風格板(v3 用) | ①定調:生不同筆觸大小 ②v4.2 各板全失敗時 fallback 回 v3 | 目標遊戲環境圖拼板(無角色/UI) |

**參考圖:ref 1 = 該張寫實 tile(滿版單張)、ref 2 = 對應的色票板(按上表選板)。**

```text
Reference image 1 is the LAYOUT GUIDE — a seamless, tileable ground
texture (near top-down). Follow its layout EXACTLY: where the moss,
dirt and path are, and the square 1:1 canvas. Every path in reference
1 must appear in the result at the same position and width, and must
enter and exit the canvas edges exactly where it does in reference 1 —
paths must NOT fade out, narrow away or stop mid-tile (required for
tiling).

Reference image 2 is the STYLE ANCHOR — cropped material close-ups
from a FINISHED TILE of this exact tile set. It defines HOW everything
is painted: the exact color palette, value range, brush stroke size,
moss shape language and overall matte finish. It contains NO layout
information — ALL layout comes from reference 1 only.

TASK: paint a completely NEW hand-painted game texture from a blank
canvas, following reference 1's layout, in reference 2's exact style —
as if painted by the same artist, in the same session, for the same
tile set. This is a FULL REPAINT, not an edit: no photographic pixels
from reference 1 may survive. Every area must show visible, deliberate
brush marks — if any region still looks like a photo, that region is
wrong. Painterly but disciplined, NOT a loose concept sketch.

SCALE: the moss clumps, path grain and brush stroke size match
reference 2 exactly — do not enlarge or simplify them. The largest
single visible stroke is no wider than 2% of the canvas. NO long
sweeping strokes, no large gestural swirls, not impressionistic.
Detail stays DENSE — stylized does not mean simplified.

MOSS: low rounded cushions with fine speckled granularity, exactly
like reference 2 — not leafy fronds, ferns, bushes or rounded bush
balls. This is a flat ground TEXTURE seen from above, not a stylized
game-map illustration. Any dirt path stays a plain dirt path — do NOT
turn it into cobblestones or stone slabs.

PALETTE: match reference 2 exactly. Do NOT introduce any hue that does
not exist in reference 2.

LAYOUT & TILING: keep the square 1:1 canvas (no crop, zoom or
outpaint) and reference 1's layout everywhere. The texture must be
SEAMLESSLY TILEABLE — left/right and top/bottom edges wrap perfectly.

LIGHTING: soft zenith light only — no horizontal light direction, no
cast shadows. Gouache-like matte finish, stepped value planes,
hue-shifted shadows leaning teal instead of black.

NO SYMMETRY: the moss and dirt shapes must be asymmetric and natural —
the left and right halves must NOT mirror each other.

Do NOT add objects: no plants, flowers, mushrooms, standing grass
tufts, stones, props, characters or footprints.
```

**選配鎖 — 反暗角(僅當要把「源頭就有的邊緣暗帶」趁風格化洗掉才加;
原套件引擎鋪排本來就 OK 就別加,會跟 ref 1 打架):**

```text
UNIFORM EXPOSURE: brightness and color stay UNIFORM across the whole
canvas — no darkened edges, no vignette, no atmospheric gradient
toward the borders, even if the layout guide has darker edges.
```

## 七張套圖量產 SOP

> 套圖:`T_Forest_Ground_F / Fb / B / Bb / Bc / C / H`(直路×2、純苔×3、
> 轉角、橫路),每張輸出 ≥2048。
> 同輪 strip 出局的原因:7×2048=14336px > NB2 上限 4096;硬拼單格只剩
> ~585px,像素預算死(B1 鐵律)。一致性由錨鏈承擔。

1. **輸入檢查:** 每張寫實 tile 滿版 1:1;同日、同設定跑完全套。
2. **定 master:** 已通過的成品(`_B`)= master,裁色票板。
3. **排程(由易到難):** `H → Bb → Bc`(純苔)→ `F → Fb`(直路)→ `C`(轉角)。
4. **每張:** v4.2 逐字不動(通用寫法,無需逐張改字),只換 ref 1;
   **開 4 挑 1**(挑卡三看:筆觸尺度貼 master、無套外色相、路貫穿到邊)。
5. **全套出完 → PS Match Color:** 以 master 為 source 拉齊色盤
   (輕微色偏不重抽;重抽只留給路形/苔丘位置的形狀級變異)。
6. **驗縫兩層(排最後):** ①每張自身 Offset 50/50 驗 wrap
   ②套內互拼(F 接 H、B 接 C…)只修縫帶 — PS 仿製印章優先。
7. **要 4096:** 全套同一個純保真放大器同參數 2×,禁回鍋 NB2。

某張連抽不順(特別是轉角 `_C`)→ 別硬耗,切「拼貼統一法」(下方備援)。

## 縫帶修復(驗縫後)　📝 提案未驗證

> **狀態:此段是提案,尚未實戰** — 本輪還沒做過 offset 50/50 驗縫,
> 下方 prompt 為預先備妥,真正跑過後再改標 ✅ 並補踩坑。

縫帶小破 → PS 仿製印章/內容感知(首選,確定性);大面積風格斷裂才走 AI,
且只在 offset 版上**有遮罩的 inpaint 工具**(Leonardo Canvas)跑:

```text
This is the same hand-painted ground texture with the canvas wrapped
(offset by 50%), so the old borders now form a cross-shaped seam
through the middle. Repaint ONLY the narrow seam band so the
brushwork, color and texture flow continuously across it. Everything
outside the seam band stays pixel-identical: same palette, same brush
style, same texture scale. Do not add anything new.
```

> ⚠️ NB2 沒有真遮罩 — 它的「區域修復」= 全圖重繪(B1 教訓)。

## 備援方案

### A. master 拼貼統一法(逐張重繪不穩時的最穩解 — 任務推回「增強」區間)　📝 提案未驗證

> **狀態:此段是提案,從未執行** — 當初為「連抽失敗」備的退路,
> 但本輪 v4.2 錨鏈就成功了,沒走到這條;下方 prompt 未實測。

1. PS 開 master 成品,「苔區/土區/路面」當素材庫;
2. 照該張 tile 寫實版分佈,粗拼出手繪版(套索+蓋章,接縫醜沒關係);
3. NB2 跑無縫統一 pass(**edit 定性** — 風格已在像素裡):

```text
This image is a game ground texture assembled in Photoshop from
hand-painted material patches — the style, palette and brushwork are
already correct and final. Its only problem: visible patch seams and
a few repeated-looking areas.

TASK: blend the patch seams so the brushwork flows naturally, and add
subtle variation to obviously repeated patches. This is a FINISH pass:
keep the layout, palette, brush stroke size, texture scale and the
square 1:1 canvas exactly. The texture must remain seamlessly tileable
— left/right and top/bottom edges wrap perfectly.

Do not restyle, do not repaint untouched areas, do not add any
objects.
```

優點:色盤/筆觸 100% 同套、零 genre 漂移;代價:每張 10–20 分鐘手工。

### B. 原圖 × 產出 遮罩混合(風格強度旋鈕,零抽獎)

核心 = 風格 pass 輸出疊在原寫實圖上,靠遮罩/透明度控制「露多少原圖細節」
(同構圖天然對位,零抽獎)。**兩種施用形式:**

- **✅ 相機距離分區遮罩(實戰驗證 — master 完成圖即用此法)**:
  近相機處(前方走道)mask 透原圖增精緻、遠相機處用產出 100%。
  見 master 段〈製作程序〉;這是本案例真正用到的收尾手法。
- **📝 全圖 50–70% 透明度(提案未驗證)**:整張統一一個透明度手動調強度 —
  概念上可行、未在本輪單獨實測(實戰是走上面的分區遮罩版)。

> 📝 **輕量統一 pass(未驗證)**:分區混合後若筆觸與照片噪點打架,
> 理論上可再跑此 pass 統一,但本輪未用到:
>
> ```text
> Unify this ground texture into a consistent hand-painted finish:
> remove the remaining photographic noise so every area shows the same
> tight, small brushwork. Do NOT change the layout, colors, texture
> scale or detail density — this is a finish-unification pass only.
> ```

## 管線總覽

```
寫實 tile(1:1 滿版)
  → ① v3 定調(泛用風格拼板,開 4–8 挑 1)→ master
  → ② master 裁色票板(細則五條)
  → ③ v4.2 量產(其餘 tile 逐張,開 4 挑 1)
  → ④ Match Color 對 master → Offset 驗縫 + 套內互拼驗縫(PS 修縫)
  → ⑤(如需 4K)純保真放大 2×(禁回鍋 NB2)
  → ⑥ 引擎 3×3 鋪排驗收
```

## 驗收 checklist

- ☐ 疊回原圖 50% 透明度:苔/土/路分佈圖案重合,只有「畫法」變了
- ☐ 100% 原寸:是筆觸不是「照片+濾鏡」(無殘留照片噪點)
- ☐ 紋理尺度與輸入一致(苔丘沒被畫大一號)
- ☐ 路(有路的張)貫穿到畫布邊,無中途淡出
- ☐ 無左右鏡像對稱感
- ☐ PS Offset 50/50:十字縫帶無明顯斷筆/色階跳變
- ☐ 光影無水平方向性(旋轉安全)、無長投影
- ☐ 無越界物件(蘑菇/花/立草/石堆/腳印)
- ☐ 引擎 3×3 鋪排:無高對比筆觸造成的週期重複感
  (若有 → 該區 PS 壓對比,或換候選)

## 產出對照(成品 + 素材圖)

### master(`_B`,v3 定調通過 — 整套基因)

> 此段為 master 的**完整定調實錄**:v3 提示詞 + 兩張參考圖 + 相機距離分區合成程序。

### ① v3 定調提示詞

> **逐字見生產區〈① v3 — 定調用完整提示詞〉;此 master 即用該 prompt 產出
> (ref 1 = 原圖、ref 2 = 泛用風格板)。**

### ② 兩張參考圖

| 圖1 原圖(寫實 ref 1) | 圖2 風格板 ref 2(`b8-style-board-v3`) |
|---|---|
| ![b8 master b source](images/b8-master-b-source.jpg) | ![b8 style board v3](images/b8-style-board-v3.jpg) |

### ⭐ 製作程序(相機距離分區合成 — 定調 + 精緻度兩全)

> **1. v3 定調:1 原圖 + 1 遊戲風格拼板 → 先算出筆觸大小**
>
> **2. 開好幾張 → 選擇 / 合成**(挑筆觸對的,必要時多張合成)
>
> **3. 前方走道(近相機)→ mask 透出原圖,增加精緻度**
>    (配合遊戲鏡頭近景實際看到的清晰度)
>
> **4. 走道後方(遠相機)→ 用產出物 100%**(風格化,配合鏡頭遠景)
>
> **5. 調整成 tile**

> 💡 **心法:近相機處要細節 → 混原圖;遠相機處可放心風格化 → 純產出。**
> 本質 = 備援 B(PS 透明度混合)**按「相機距離」分區施用** — 不是全圖統一強度。

### v3 產出圖(raw — 定調成品,合成前)
![b8 master B raw](images/b8-master-b.jpg)

### ⭐ 完成圖(相機距離分區合成後 — 升格為 master)
![b8 master B final](images/b8-master-b-final.png)

### 量產 tile 定稿(v4.2)
| H | Bb | Bc |
|---|---|---|
| ![b8 tile H](images/b8-tile-h.png) | ![b8 tile Bb](images/b8-tile-bb.png) | ![b8 tile Bc](images/b8-tile-bc.png) |
| **F** | **Fb** | **C** |
| ![b8 tile F](images/b8-tile-f.png) | ![b8 tile Fb](images/b8-tile-fb.png) | ![b8 tile C](images/b8-tile-c.png) |

### ⭐ 製作程序(v4.2 量產 — 對照 master 段的 (1) v3)

> **1. 輸入:地板原圖(ref 1)+ 1 參考拼圖(ref 2 = v3 產出截圖裁的 4 塊)→ 改圖**
>
> **2. 拼圖也會影響產出 → 換著給**(不同拼板出不同結果,見〈拼板庫制〉)
>
> **3. 產出後調整成 tile**

> ### ⚠️ 拼圖跟原圖差太多 → 重出素材
> **色域/材質對不上時(如 `_C` 棕紅土),重新用 v3 產出該色域的素材圖,
> 或從既有素材裡找出適合的拼圖重拼。**
> (呼應「**板的色域 = 輸出色域上限**」— 板涵蓋不到的材質色會被 clamp。)

### 色票板庫(ref 2 素材)
| 通用板 1 | 通用板 2 | 通用板 3 |
|---|---|---|
| ![b8 swatch general 1](images/b8-swatch-general-1.jpg) | ![b8 swatch general 2](images/b8-swatch-general-2.jpg) | ![b8 swatch general 3](images/b8-swatch-general-3.jpg) |

- **`_C` 棕紅土專屬板**(治通用板把棕紅土 clamp 成土黃,踩坑見拼板庫表):
  ![b8 swatch C redsoil](images/b8-swatch-c-redsoil.jpg)
- **泛用風格板(v3 定調用)**:![b8 style board v3](images/b8-style-board-v3.jpg)

### 輸入寫實 tile 一覽
![b8 input tiles](images/b8-input-tiles.jpg)

---

# 🔵 查詢區(風格解剖 / 踩坑 / 字典 / 版本歷程)

## 來源(索引)

- **輸入素材:** 寫實風四方連續地面貼圖套組 ×7(1:1,苔蘚坡地 + 土路變體)
- **風格目標:** 《Ruined King: A League of Legends Story》遊戲截圖
- **平台:** Leonardo.ai AI Creation / **Nano Banana 2**(沿用 B1/B2 主力)
- **產圖連結(Leonardo):** <https://app.leonardo.ai/generation/image/reference-image-1-layout-guide-seamless-tileable-8d8b1b2a-e121-49da-8d13-abc896ac3cbf>
- **對話紀錄(本案例攻關全程):** <https://claude.ai/code/session_01Gif5qPYdeoPTbF7HyHv9Ka>
- **任務定性:** ~~B2 的「增強」模式~~ → **修正(踩坑 #2):風格轉換必須用
  「重繪」定性**(照版面從空白畫布重畫),edit/保留定性會得到零變化的認同解;
  分佈真相由 layout 鎖承擔,不由 edit 定性承擔

## 目標風格解剖(Ruined King 級厚塗 → prompt token 對照)

| # | 視覺特徵 | 對應 token |
|---|---|---|
| 1 | 筆觸可見且自信 — 大筆平塗一筆到位,無照片噪點 | `confident visible brushstrokes`, `broad flat brush strokes`, `no photographic noise or grain` |
| 2 | 形狀塊面化 — 石板/土塊歸納成大塊面,每面 2–3 個明度階 | `simplified chunky planar shapes`, `stepped value planes` |
| 3 | 明度結構誇張 — 對比拉大,AO 是「畫上去的深色塊」 | `exaggerated value structure`, `hand-painted ambient occlusion in crevices` |
| 4 | 陰影色相偏移 — 暗部往青/藍紫偏,不是單純變黑;亮部偏暖 | `hue-shifted shadows (shadows lean teal, not black)`, `warm-cool color contrast` |
| 5 | 輪廓收邊意識 — 物件邊緣有暗線或亮 rim(漫畫 DNA) | `crisp painted edge accents` |
| 6 | 細節是「暗示」不是「渲染」— 遠看豐富,近看是幾筆 | `suggested detail, not rendered detail`(⚠️ 此 token 禁入 prompt — 踩坑 #1 禍首,僅作風格描述), `gouache-like matte finish` |

風格錨(文字):`hand-painted stylized game art texture`。
⚠️ NB2 對 artist name 無效(訓練時 scrub,見 community-prompt-patterns),
**風格主要靠參考圖攜帶,文字只描述「畫法」**。

## 風險分析(踩坑前的預判 + 實戰修正)

| # | 風險 | 對策 |
|---|---|---|
| 1 | **幾何滲漏**:帶構圖的參考圖(整張截圖/整張 master)→ 構圖滲入,文字鎖不住 | 材質色票板(裁掉構圖);無角色/無 UI 的環境圖拼板也可(拼板稀釋構圖),但 **master 同族 tile 必須色票板化**(踩坑 #6) |
| 2 | **四方連續被打斷**:風格 pass 是重繪級,邊緣筆觸不會自動 wrap | prompt 四方連續鎖 + 出圖後必做 PS Offset 50/50 驗縫;縫帶修復交確定性工具 |
| 3 | **紋理尺度漂移** | 尺度綁 ref 2 實體樣本(v4.2 SCALE 段) |
| 4 | **方向光烙進貼圖** → 不可旋轉 | B2 頂光句:只允許 zenith,禁水平光與長投影 |
| 5 | **風格化成品再過 NB2 = 筆觸被抹**(B3 鐵證) | 只走純保真放大分支 |
| 6 | 長出越界物件 | 禁止清單保底 |

## 踩坑紀錄(v1 → v4.2 全歷程)

| # | 現象 | 根因 | 解法 |
|---|---|---|---|
| 1 | (v1)筆觸尺度爆大(單筆≈角色寬)、苔蘚被重繪成側視蕨葉叢、土路寫意漩渦、細節密度大降 — 「太過寫意」 | ①只定義「畫法」沒鎖「筆觸尺度/細節密度」→ 模型用自己習慣的大筆觸作畫 ②`painterly clumps with light and shadow planes` 給苔蘚往葉叢重新解釋的空間(B1 踩坑 #6 歧義物件同型)③`detail is suggested, not rendered` 直接授權減密 — 禍首句 | v2 三鎖:**筆觸尺度鎖**(單筆 ≤2% 畫布)+ **細節密度鎖**(100% 原寸小形狀數量≈輸入)+ **苔蘚形態鎖**(low rounded cushions,禁 fronds/ferns/side-view foliage);刪授權減密句 |
| 2 | (v2)輸出≈原圖,風格完全沒轉 — 「沒有變化」 | **保留鎖過量 + edit 定性 = 認同解**:密度鎖綁「跟照片一樣多的小形狀」+「疊圖必須 line up」,等於下令複製輸入;B1 踩坑 #7 同型(保真定性下模型不敢動) | v3 定性反轉:`paint a completely NEW texture from a blank canvas, following reference 1's layout` + **強制重繪條款**(`no photographic pixels may survive — if any region still looks like a photo, that region is wrong`);密度/分佈鎖措辭放軟(macro distribution,不綁 pixel 對齊) |
| 3 | (v3 量產)同 prompt 重抽三張拼不成一套:色盤/明度漂移、土路形狀不同、其中一張長出紅褐苔 — 「單張生成不穩定」 | **NB2 無 seed + 重繪定性 = 高變異**;B1 套圖鐵律(同日同配方同 prompt)只鎖得住保真 pass,鎖不住重繪 pass;泛用色票板只定「畫法」,沒定「這一套的確切色值」 | **v4 成品錨鏈**:ref 2 改掛「已通過的 v3 成品」當 STYLE & PALETTE ANCHOR + 禁新色相條款;殘餘色偏用 **PS Match Color** 確定性收尾;仍有變異就開 N 挑 1 |
| 4 | (v4 套圖 tile)苔變青綠灌木球、顆粒比 master 大數倍、路變奶黃 — 三鎖全失守,整體掉進「卡通俯視 RPG 地圖」genre | ①**參考圖角色混淆**:ref 1(layout)與 ref 2(master 錨)同為「苔地+土路」tile,外觀高度相似 → 模型分不清「誰管 where 誰管 how」,錨失效後自由發揮 ②「俯視 + 道路」觸發 NB2 的 stylized game map 先驗 ③(檢查項)確認 Enhance/Style 仍為 None ④事後確認:此輪輸入是 **4 合 1 拼圖**(踩坑 #5 的第一次發作) | **v4.1 角色消歧版**:開頭明寫「兩張很像但角色不同」+ WHERE/HOW 分工 + PRIORITY 條款(B2 技法);尺度直接綁 ref 2;加**反 genre 條款**(`a flat ground TEXTURE, not a stylized game-map illustration — no rounded bush balls`) |
| 5 | (4 合 1 生成)四張 tile 拼 2×2 一次跑:材質糊掉、筆觸相對變粗、四象限交界被暈接、土路被重新解釋成**石板路**、角落壓暗 — 「合一後變醜」 | ①**像素預算**:2048 輸出下每張 tile 只分到 1024px,微觀苔粒畫不出來 → 糊、筆觸相對粗(B1 白邊 / B2 模組佔比 第四度應驗)②**模型把拼圖當一個場景**:十字交會的路被「合理化」成石板大道、象限交界被暈接、整圖打氣氛光 — 每張 tile 的獨立性與 wrap 邊全毀 ③「俯視地圖」genre 先驗再度觸發 | **tile 生成鐵律:一次一張、單張滿版**。4 合 1 沒有任何補救 prompt;拼板唯一合法用途 = 風格參考(色票板),絕不當生成目標 |
| 6 | (v4.1 跑 `_F`)風格全對(色盤/筆觸/苔形同 master,消歧成功),但 ref 1 的貫穿直路中段消失、底部長出 master 的橫向沙帶 — **layout 被錨滲漏**,直路未出下緣,tile 接不了縫 | **成品錨 = 整張 tile = 帶構圖的圖** → B2 踩坑 #1 幾何滲漏在錨身上發作;`Nothing about its layout may be copied` 文字鎖不住(B2 已證);「路徑淡出」是模型對長路徑的慣性,需獨立鎖 | **v4.2:master 色票板化**(風格像素全保留、構圖歸零)+ **路徑連續鎖**(`every path must enter and exit the canvas edges exactly where it does in reference 1 — must NOT fade out or stop mid-tile`) |
| 7 | (v4.2 跑 `_F`)三大驗收全過(路貫穿/無橫帶滲漏/風格同套 — 色票板錨成立),殘餘:左右暗色漸層帶 + 左右苔丘鏡像;第二抽反而照片感回歸(重繪不足) | 暗帶**事後確認源自 ref 1 原圖**(非模型發明 — layout 鎖忠實重現,行為正確);鏡像 = 生成對稱性 artifact(B1 踩坑 #4 同型);照片感回歸 = 拼板未修(暗糊塊仍在)+ 抽卡變異 | 暗帶:**決策點在源頭** — 原套件引擎鋪排 OK 就保留;想洗掉才加 UNIFORM EXPOSURE 鎖。鏡像:反鏡像鎖(已入 v4.2 常駐)。照片感:修拼板(暗糊塊/照片塊優先)+ 回第一抽收檔 |

### 踩坑證據圖

| #1 v1 過度寫意 | #2 v2 零變化 |
|---|---|
| ![b8 fail v1 loose](images/b8-fail-v1-loose.jpg) | ![b8 fail v2 nochange](images/b8-fail-v2-nochange.png) |
| 筆觸爆大、苔變側視蕨葉叢、土路寫意漩渦 | 輸出≈原圖,風格完全沒轉(edit 定性認同解)|

| #4 v4 卡通地圖 genre | #5 4 合 1 生成 |
|---|---|
| ![b8 fail v4 genre](images/b8-fail-v4-genre.png) | ![b8 fail 4in1](images/b8-fail-4in1.webp) |
| 苔變青綠灌木球、路變奶黃、掉進 RPG 地圖 genre | 材質糊、交界暈接、土路被合理化成石板路 |

## 鎖句字典(B8 新增)

| 鎖 | 用途 | 關鍵句 |
|---|---|---|
| **筆觸尺度鎖** | 防大筆寫意化 | `brush strokes stay SMALL — the largest single visible stroke is no wider than 2% of the canvas` |
| **細節密度鎖** | 防風格化=減細節 | `Detail stays DENSE — stylized does not mean simplified` |
| **形態鎖(苔蘚)** | 防材質被重新解釋成別種植被 | `moss stays LOW ROUNDED CUSHIONS with fine speckled granularity — do NOT reinterpret as leafy fronds, ferns, bushes or side-view foliage` |
| **收斂定性句** | 給「緊的手繪」心智模型 | `a TIGHT, CONTROLLED hand-painted game texture — painterly but disciplined, NOT a loose concept sketch` |
| **重繪定性句** | 治零變化(edit → 重繪反轉) | `paint a completely NEW hand-painted texture from a blank canvas, following reference 1's layout — a FULL REPAINT, not an edit` |
| **強制重繪條款** | 不留照片像素的驗收律 | `no photographic pixels from reference 1 may survive — if any region still looks like a photo, that region is wrong` |
| **角色消歧段** | ref 相似時防 where/how 混淆 | `They look similar — do NOT confuse their roles: Reference 1 decides WHERE... Reference 2 decides HOW... If they conflict: reference 1 wins for placement, reference 2 wins for paint` |
| **成品錨(同套一致性)** | 治無 seed 重抽漂移 | `cropped material close-ups from a FINISHED TILE of this exact tile set — painted by the same artist, in the same session` |
| **禁新色相條款** | 防單張長出套外顏色 | `do NOT introduce any hue that does not exist in reference 2` |
| **反 genre 條款** | 防掉進卡通地圖先驗 | `a flat ground TEXTURE seen from above, not a stylized game-map illustration — no rounded bush balls, no cartoon map look` |
| **路徑連續鎖** | 防長路徑中途淡出 | `every path must enter and exit the canvas edges exactly where it does in reference 1 — must NOT fade out, narrow away or stop mid-tile` |
| **反鏡像鎖** | 防左右對稱 artifact | `the left and right halves must NOT mirror each other` |
| **反暗角鎖(選配)** | 洗掉源頭邊緣暗帶時用 | `no darkened edges, no vignette, no atmospheric gradient toward the borders, even if the layout guide has darker edges` |

## 版本歷程(淘汰版對照,完整文字見 git 歷史)

| 版本 | 定性 | 結果 | 關鍵差異 |
|---|---|---|---|
| v1 | 重繪,無鎖 | ❌ 過度寫意 | 含 `suggested, not rendered` 授權減密句(禍首);苔變蕨葉叢 |
| v2 | edit 保留 + 三鎖 | ❌ 零變化 | 密度鎖綁「跟照片一樣」+ pixel 對齊 = 認同解(完整文字:commit 988ba02)|
| **v3** | **重繪 + 三鎖(放軟)** | **✅ 定調用** | 生產區 ① |
| v4 | v3 + 整張 master 當錨 | ⚠️ 錨混淆/滲漏 | ref 1/ref 2 同族相似 → 角色混淆(#4)、構圖滲漏(#6) |
| v4.1 | v4 + 角色消歧段 | ⚠️ 風格對、layout 漏 | 消歧有效,但整張 master 的構圖仍滲(完整文字:commit 0cfda81)|
| **v4.2** | **v4.1 + master 色票板化 + 路徑連續鎖 + 反鏡像鎖** | **✅ 量產定版** | 生產區 ② |

## 跨主題適用性(換材質時怎麼改)

框架(兩段式流程/重繪定性/消歧段/尺度密度鎖/四方連續鎖/固定 seed/拼板庫/
Match Color/雙層驗縫)**主題無關,直接沿用**。換主題只換三個槽位:
①形態鎖(換 MOSS 段 + 該材質的歧義防線)②禁止清單 ③拼板重做 + v3 重定調一個 master。

| 主題 | 難度 | 專屬風險(要進形態鎖的) |
|---|---|---|
| **雪地** | 低 | 亮部過曝、藍影洗灰;歧義物件被補完(B1 雪山骸骨前科,搬輪廓鎖);雪筆觸軟,拼板「筆觸級清晰」判準放寬 |
| **火山熔岩** | 中 | 發光裂縫 = emissive → 搬 B1 光暈半徑鎖;palette 明文允許高飽和橙紅;防「熔岩流動」場景化(鎖成靜態材質) |
| **地磚 / 人造建築** | **高** | ①磚縫是幾何非紋理,人眼對直線錯位極敏感 → layout 鎖升級成磚縫網格 pixel 級跟 ref 1,必做 overlay ②AI 畫長直線會歪/斷 ③wrap 邊磚縫要跨邊對齊,驗縫嚴一級 ④防砌法被重新解釋(亂石↔方磚)。可考慮先出線稿層當幾何真相(B2 貼材質灰盒邏輯)|

> 新主題沿用 B8 開新案例檔(B9 雪地、B10 地磚…),只記「槽位怎麼填 + 該主題踩的坑」,
> 框架引用 B8,不整份重寫。

## 學到的(累積中)

- ✅ **「手繪風」預設會帶三個副作用:筆觸變大、細節變少、歧義材質被重新解釋。**
  三者都要各自上鎖 — 風格詞只管「像不像手繪」,不管「畫多細」。
- ✅ **正面授權句比禁令危險**(B1「定性句>禁令」的反面):
  `suggested, not rendered` 一句就讓模型合法丟掉一半細節。
  風格 prompt 裡每一句「允許」都要想一遍會被放大成什麼。
- ✅ **風格轉換的力度是單擺,兩端都會死**:v1(風格詞無鎖 → 過度寫意)、
  v2(保留鎖過量 + edit 定性 → 認同解/零變化)。正解結構 =
  **重繪定性(給變化的力)+ 少數硬鎖(給不變的框)** — 鎖要鎖
  「尺度/形態/版面」這些框架量,不能鎖「跟輸入一樣」這種認同量。
- ✅ **B2「增強模式極穩」不適用於風格轉換**:增強(材質變高清)與
  風格轉換(渲染方式整個換掉)是相反方向 — 前者要 edit 定性,
  後者必須重繪定性,拿錯定性就掉進對應的坑(B1 #7 / B8 #2 同型)。
- ✅ **風格化 pass 的量產一致性要靠「成品錨鏈」,不能靠重抽紀律**:
  重繪定性的輪間變異是結構性的 — B1 套圖鐵律只對保真 pass 有效。
  正解 = 定調 master → master 色票板錨 → Match Color 收尾;
  重抽只留給形狀級變異(concept-to-3d 一致性錨協議在貼圖管線同樣成立)。
  > 🆕 更正(2026-07-14):先前多處寫「NB2 無 seed」— **Leonardo 介面
  > Advanced Settings 其實有 Use Fixed Seed**,實戰確認固定 seed 可稍降
  > 輪間變異、提高成功率。修正後的一致性配方 = **錨鏈(主)+ 固定 seed(輔)
  > + Match Color(收尾)** 三層;seed 記錄慣例:master 抽中那輪的 seed
  > 記入紀錄,量產全套沿用。
- ✅ **錨也會滲漏**:整張成品 tile 當風格錨,構圖照樣滲(#6)—
  「材質色票板化」是錨的必要形態,不是選配。滲漏的載體永遠是構圖。
- ✅ **多張 tile 絕不合一生成(#5)**:模型把拼圖讀成「一個場景」+
  像素預算腰斬 → 筆觸相對變粗、材質糊、交界暈接。一次一張、單張滿版。
- ✅ **色票板的「純度」= 量產品質上限**:板上每一格都在教模型「照這樣畫」—
  照片級清晰的塊(毛絲/碎石/雜訊)= 教它畫照片;判準是
  「數得出筆數」而不是「看起來清楚」。
- ✅ **風格參考的滲漏防線分兩級**:泛用風格參考(不同族的圖)可用
  「無角色/無 UI 環境圖拼板」(拼板稀釋構圖);**同族圖(master tile)
  必須裁成無構圖材質特寫** — 越像輸出目標的參考,滲漏風險越高。
- ✅ **禁新色相條款是雙面刃 → 拼板庫制**(`_C` 案例):條款把「板上沒有的色」
  一律 clamp 掉 — 包括 tile 本來就該有的(棕紅土被拉成土黃)。
  結論:**板的色域 = 該張輸出的色域上限**;色票板不是一張而是一個庫
  (通用板 ×N + 特殊色域專屬板),按 tile 的材質色選板。
  另:ref 1 與板恰好有相似色塊時會互相牽引,換另一張通用板即可。
- ✅ **相機距離分區合成**(master 定調實錄):風格強度不必全圖統一 —
  **近相機處(前方走道)mask 透出原圖增精緻度、遠相機處用產出物 100%**。
  近景人眼看得到細節、遠景吃風格化剛好,兩全。本質是備援 B(PS 透明度混合)
  按相機距離分區施用,而非全圖一個強度。
- 📌 風格強度最便宜的旋鈕不是 prompt,是 **PS 圖層不透明度**(備援 B)—
  同構圖疊圖天然對位,零抽獎。
