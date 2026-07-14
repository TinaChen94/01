# 實戰紀錄 — B8 寫實貼圖 → 手繪風格化(style transfer)提示詞配方

> 寫實風四方連續地面貼圖 → 《Ruined King》/ Battle Chasers 級手繪厚塗風格。
> 對應工作流:`ai-media-generator`;前置知識:[B1](B1-forest-bg-4k-detail.md)(鎖句字典)、
> [B2](B2-greybox-module-pipeline.md)(圖案活化/材質色票板/頂光)、
> [B3](B3-fenske-painterly-4k.md)(手繪風 ×  NB2 保真 pass 禁忌)。

**🔑 關鍵字:** `B8`、`風格轉換`、`手繪風格化`、`style transfer`、`厚塗`、
`hand-painted`、`Ruined King 風`、`四方連續風格化`、`tileable 風格轉換`、
`筆觸化`、`寫實轉手繪`

**狀態:✅ v3 重繪定性版實戰通過(2026-07-14)** — 筆觸小而密、細節密度保持、
分佈與色盤跟輸入對齊、無越界物件。歷程:v1 過度寫意 → v2 零變化 → v3 通過。
**待辦:PS Offset 50/50 驗縫、引擎 3×3 鋪排驗收、成品圖入庫 `images/b8-*`。**

## 來源(索引)

- **輸入素材:** 寫實風四方連續地面貼圖(1:1,苔蘚坡地 + 底部土路,日光自然色)
- **風格目標:** 《Ruined King: A League of Legends Story》遊戲截圖 ×3
  (青綠夜色石板競技場 ×2、暖色叢林土地 ×1)
- **平台:** Leonardo.ai AI Creation / **Nano Banana 2**(沿用 B1/B2 主力)
- **任務定性:** ~~B2 的「增強」模式~~ → **修正(踩坑 #2 後):風格轉換必須用
  「重繪」定性**(照版面從空白畫布重畫),edit/保留定性會得到零變化的認同解;
  分佈真相由 layout 鎖承擔,不由 edit 定性承擔

---

## 目標風格解剖(圖1–3 共同特徵 → prompt token 對照)

| # | 視覺特徵 | 對應 token |
|---|---|---|
| 1 | 筆觸可見且自信 — 大筆平塗一筆到位,無照片噪點 | `confident visible brushstrokes`, `broad flat brush strokes`, `no photographic noise or grain` |
| 2 | 形狀塊面化 — 石板/土塊歸納成大塊面,每面 2–3 個明度階 | `simplified chunky planar shapes`, `stepped value planes` |
| 3 | 明度結構誇張 — 對比拉大,AO 是「畫上去的深色塊」 | `exaggerated value structure`, `hand-painted ambient occlusion in crevices` |
| 4 | 陰影色相偏移 — 暗部往青/藍紫偏,不是單純變黑;亮部偏暖 | `hue-shifted shadows (shadows lean teal, not black)`, `warm-cool color contrast` |
| 5 | 輪廓收邊意識 — 物件邊緣有暗線或亮 rim(漫畫 DNA) | `crisp painted edge accents` |
| 6 | 細節是「暗示」不是「渲染」— 遠看豐富,近看是幾筆 | `suggested detail, not rendered detail`, `gouache-like matte finish` |

風格錨(文字):`hand-painted stylized game art texture`。
⚠️ NB2 對 artist name 無效(訓練時 scrub,見 community-prompt-patterns),
**風格主要靠參考圖攜帶,文字只描述「畫法」**。

---

## 風險分析(開跑前必讀)

| # | 風險 | 對策 |
|---|---|---|
| 1 | **幾何滲漏**:圖1–3 整張餵 → 角色/火焰特效/傷害數字/競技場圓形構圖滲入貼圖(B2 踩坑 #1 同型) | **材質色票板**(B2 技法):從三張截圖各裁 2–3 塊「純地面特寫」(石板面、土地面),避開角色/特效/UI,拼成一張 1:1 色票板當風格參考。**禁止整張餵** |
| 2 | **四方連續被打斷**:風格 pass 是重繪級,邊緣筆觸不會自動 wrap | prompt 加四方連續鎖(下方);**出圖後必做 PS Offset 50/50 驗縫**;縫帶修復交給確定性工具(PS 仿製印章/內容感知),因 NB2 區域修復=全圖重繪(B1 教訓) |
| 3 | **紋理尺度漂移**:風格化時苔丘被畫大一號 | B1 尺度鎖:`the texture scale stays identical to the input` |
| 4 | **方向光烙進貼圖** → 模組不可旋轉 | B2 頂光句:只允許 zenith 光,禁水平方向光與長投影 |
| 5 | **風格化成品再過 NB2 保真 pass = 筆觸被抹**(B3 鐵證:筆觸型圖跑 NB2 材質 pass 必漂移) | 風格化後如需放大,**只走純保真放大分支**(Topaz / Real-ESRGAN / UU 最低 creativity),不回鍋 NB2 |
| 6 | 長出越界物件(蘑菇/花/小石堆) | 禁止清單照 B1 慣例保底 |

---

## 前置作業:材質色票板製作

1. 圖1(青綠夜石板):裁競技場地面 2 塊(避開角色腳、火焰、`47` 數字)
2. 圖2(暖色叢林):裁沙土地面 2 塊(避開角色、藍色氣浪、綠色浮石)
3. 圖3(深色石板):裁前景石板 1–2 塊(避開角色、火圈、`CRITICAL 280`)
4. PS 拼成一張 1:1 方板(純材質特寫,無任何構圖/物件) → 存為風格參考

> 若貼圖要進夜森林專案(B1/B2 世界觀),色票板以圖1/圖3 的青綠夜色塊為主;
> 若保留日光自然色,則以圖2 暖土塊 + 圖1 石板「畫法」為主,色相靠 prompt 鎖回輸入圖。

> **📌 實戰註記(v3 通過輪):** 實際使用的 ref 2 並非嚴格材質特寫色票板,
> 而是 **4 張「無角色/無 UI」的純環境美術圖拼成 2×2 拼板**(Ruined King
> 場景圖,地面佔畫面大宗)— 未發生幾何滲漏,構圖也未滲入。
> 判讀:滲漏防線的重點是 **①畫面裡沒有角色/特效/UI ②拼板稀釋單張構圖
> ③輸出端有 layout 鎖**;三者都在時,環境圖拼板可用,且比材質特寫多帶
> 「大中小筆觸層次」資訊。有角色/UI 的截圖仍必須裁成材質特寫。

## 平台設定(Leonardo.ai AI Creation)

| 設定 | 值 | 備註 |
|---|---|---|
| Model | Nano Banana 2 | |
| Image Dimensions | **1:1(2048×2048)** | 輸入是 1:1 → 輸出比例對齊(B1 鐵律);1024→2048 = 2× 安全倍率。要 4K 再走純放大分支(風險 #5) |
| Prompt Enhance | None | 鎖句型 prompt 一律關 |
| Style | None | 避免疊色調,與色盤指令衝突 |
| Private Mode | On | |

---

## 逐字 prompt

### 1. 主配方 v3 — 重繪定性版(ref 1 = 寫實貼圖、ref 2 = 材質色票板)

v2 零變化後的反轉版:定性從「edit 保留」反轉成「**照版面從空白畫布重畫**」,
加**強制重繪條款**;v2 的三鎖保留但措辭放軟(尤其細節密度鎖不再綁「跟照片一樣」)。

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

> 校準邏輯:v1(寫意)與 v3 之間如果還有落差,兩張輸出可用 Plan B
> 互混;v3 若分佈漂移,把 LAYOUT 段的 `macro distribution` 強化為
> `the distribution must stay recognizable when overlaid`(但別再回到
> v2 的 pixel 對齊措辭 — 那是零變化的根源)。

### 1-old. 淘汰版 v2 — 收斂版(❌ 零變化,留作對照)

v1 過度寫意後的修正版:新增**筆觸尺度鎖、細節密度鎖、苔蘚形態鎖**,
並刪除 v1 的授權減密句(`detail is suggested by brushwork, not rendered`)。
結果:輸出≈原圖,風格完全沒轉 — 保留鎖過量 + edit 定性,模型取「認同解」。

```text
Reference image 1 is the BASE — a seamless, tileable ground texture
(near top-down): green moss slopes with exposed dirt and a sandy path
along the bottom. Its layout is the truth: the moss / dirt / path
DISTRIBUTION PATTERN, the texture scale, and the square 1:1 canvas are
all correct and final.

Reference image 2 is the STYLE TARGET — cropped material swatches from
a hand-painted stylized game. Use it ONLY for the painting technique.

TASK: repaint reference 1 as a TIGHT, CONTROLLED hand-painted game
texture — painterly but disciplined, like a professional hand-painted
ground texture for a game engine, NOT a loose concept sketch.

BRUSH SCALE LOCK (critical): brush strokes stay SMALL. The largest
single visible stroke is no wider than 2% of the canvas. Stroke size
follows the input's texture granularity — small dabs and speckles for
moss, short strokes for twigs and litter. NO long sweeping strokes,
NO large gestural swirls, NOT impressionistic, NOT abstract.

DETAIL DENSITY LOCK: keep the same visual detail density as the input
— at 100% zoom the result shows roughly the same amount of small
shapes as the photo, each painted crisply with 2-3 value steps
instead of photographic noise.

MOSS SHAPE LOCK: moss stays LOW ROUNDED CUSHIONS with fine speckled
granularity, matching the input's clump size. Do NOT reinterpret moss
as leafy fronds, ferns, bushes, grass blades or any side-view foliage
— everything reads as a flat ground surface seen from above.

KEEP EXACTLY: the square 1:1 canvas (no crop, zoom, extend or
outpaint), the moss / dirt / path distribution pattern (overlaying
the result on the input must line up), and the texture scale. The
texture must remain SEAMLESSLY TILEABLE — left/right and top/bottom
edges wrap perfectly, brushwork flows continuously across the borders.

STYLE: stepped value planes, hue-shifted shadows that lean teal
instead of black, crisp painted edge accents, gouache-like matte
finish. PALETTE: keep the natural daylight green-and-earth palette of
reference 1. LIGHTING: soft zenith light only — no horizontal light
direction, no cast shadows.

Do NOT add any objects: no plants, flowers, mushrooms, standing grass
tufts, stones, props, characters or footprints.
```

> 風格強度旋鈕:v2 出來若**太照片**(筆觸感不足)→ 尺度鎖放寬到
> `no wider than 4% of the canvas`;若**仍太寫意** → 先走 Plan B(下方
> PS 混合),不要繼續加禁令堆疊。

### 1a. 量產版 v4 — 成品錨鏈(套圖/重抽一致性用)

第一張用 v3 抽到滿意後,那張成品升格為 **master 錨**;之後每一張
(同 tile 重抽、或套圖其他 tile)都用本版:**ref 1 = 該張的寫實 tile、
ref 2 = master 成品**(色票板退役 — 參考圖數量最小化,B2 #9)。
與 v3 的差異只有前兩段,其餘段落逐字照 v3:

```text
Reference image 1 is the LAYOUT GUIDE — a seamless, tileable ground
texture (near top-down). Take from it ONLY: the terrain distribution
layout, the texture scale, and the square 1:1 canvas.

Reference image 2 is a FINISHED TILE from this exact tile set — the
STYLE & PALETTE ANCHOR. The result must look like it was painted by
the same artist, in the same session, for the same tile set: match
its exact color palette, value range, brush stroke size, moss shape
language and overall matte finish. Do NOT introduce any hue that
does not exist in reference 2 — no red-brown moss, no new path
colors, no shifted greens.

TASK: paint a completely NEW hand-painted game texture from a blank
canvas, following reference 1's layout, in reference 2's exact
style. This is a FULL REPAINT, not an edit: no photographic pixels
from reference 1 may survive. Every area must show visible,
deliberate brush marks — if any region still looks like a photo,
that region is wrong.

[BRUSH SCALE / MOSS / LAYOUT & TILING / STYLE DETAILS / LIGHTING /
Do NOT add objects — 五段逐字照 v3,PALETTE 句改為:
PALETTE: match reference 2 exactly.]
```

殘餘的輕微色偏**不要重抽** — PS `Image > Adjustments > Match Color`
以 master 為 source 拉齊(確定性收尾,把色盤的骰子收走);
形狀級的變異(路形/苔丘位置)才需要重抽,開 4 挑 1。

#### v4.1 — 角色消歧完整版(踩坑 #4/#5 後的量產定版,逐字可貼)

ref 1 與 ref 2 同為地面 tile 時,模型會混淆兩張的角色 → 錨失效。
v4.1 = 消歧段 + v3 骨架 + 反 genre / 反石板 / 禁新色相三保險:

```text
Reference image 1 is the LAYOUT GUIDE and reference image 2 is the
STYLE ANCHOR. They are different tiles from the SAME tile set, so they
look similar — do NOT confuse their roles:
- Reference 1 decides WHERE everything is: the exact moss / dirt /
  path layout, and the square 1:1 canvas. Nothing about its layout may
  change.
- Reference 2 decides HOW everything is painted: its exact color
  palette, value range, brush stroke size, moss shape language and
  overall matte finish. Nothing about its layout may be copied.
- If they conflict: reference 1 wins for placement, reference 2 wins
  for paint.

TASK: paint a completely NEW hand-painted game texture from a blank
canvas, following reference 1's layout, in reference 2's exact style —
as if painted by the same artist, in the same session, for the same
tile set. This is a FULL REPAINT, not an edit: no photographic pixels
from reference 1 may survive. Every area must show visible, deliberate
brush marks — if any region still looks like a photo, that region is
wrong. Painterly but disciplined, NOT a loose concept sketch.

SCALE: the moss clumps, path grain and brush stroke size in the result
are the SAME physical size as in reference 2 — do not enlarge or
simplify them. The largest single visible stroke is no wider than 2%
of the canvas: small dabs and speckles for moss, short strokes for
twigs and litter. NO long sweeping strokes, no large gestural swirls,
not impressionistic. Detail stays DENSE — stylized does not mean
simplified.

MOSS: low rounded cushions with fine speckled granularity, exactly
like reference 2 — not leafy fronds, ferns, bushes or rounded bush
balls. This is a flat ground TEXTURE seen from above, not a stylized
game-map illustration — no cartoon map look. Any dirt path from
reference 1 stays a plain dirt path exactly like reference 2 — do NOT
turn it into cobblestones or stone slabs.

PALETTE: match reference 2 exactly. Do NOT introduce any hue that does
not exist in reference 2 — no red-brown moss, no new path colors, no
shifted greens.

LAYOUT & TILING: keep the square 1:1 canvas (no crop, zoom or
outpaint) and reference 1's macro distribution. The texture must be
SEAMLESSLY TILEABLE — left/right and top/bottom edges wrap perfectly.

LIGHTING: soft zenith light only — no horizontal light direction, no
cast shadows. Gouache-like matte finish, stepped value planes,
hue-shifted shadows leaning teal instead of black.

Do NOT add objects: no plants, flowers, mushrooms, standing grass
tufts, stones, props, characters or footprints.
```

> 首驗建議:先跑 `_B`(純苔,與 master 差異最大、角色最不易混),
> 驗證錨鏈接上與否的最乾淨樣本。
> **實戰結果(踩坑 #6):風格錨定成功、但 master 構圖滲漏 → 升級 v4.2。**

#### v4.2 — master 色票板錨(踩坑 #6 後的量產定版,逐字可貼)

**前置:master 色票板製作** — PS 從 master 成品裁 4–6 塊無構圖材質特寫
(苔區 ×2–3、深土區 ×1–2、路面 ×1,路面裁到只剩沙土質感、看不出路形),
拼成一張 1:1 方板 = 新的 ref 2。風格像素 100% 是 master 的,構圖歸零。

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

Do NOT add objects: no plants, flowers, mushrooms, standing grass
tufts, stones, props, characters or footprints.
```

### 1a-alt. master 拼貼統一法(套圖最穩解 — 把任務推回「增強」區間)

v4/v4.1 仍不穩時放棄「逐張重繪」,改用 B2 貼材質灰盒的邏輯:
**風格與色盤由像素直接繼承,AI 只做它最穩的縫合**。

1. PS 開 master 成品,把「苔區 / 土區 / 路面」當素材庫;
2. 照每張 tile 寫實版的分佈,把 master 素材粗拼出該 tile 的手繪版
   (套索粗選 + 蓋章即可,接縫醜沒關係);
3. NB2 跑「無縫統一 pass」(**edit 定性** — 風格已在,回到增強區間):

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

優點:色盤/筆觸 100% 同套(像素就是 master 的)、零 genre 漂移;
代價:每張要 10–20 分鐘 PS 手工。七張套圖規模下,這條通常比重抽便宜。

> ~~備選:同輪 strip 生成~~ — **❌ 已實戰否決(踩坑 #5)**:多張 tile
> 拼一起生成,模型會把拼圖當「一個場景」畫 — 交界被暈接、道路被合理化
> 成新材質、像素預算腰斬,每張 tile 的獨立性與 wrap 邊全毀。
> **tile 生成鐵律:一次一張、單張滿版。**

### 1b. Plan B — PS 透明度混合(零抽獎的風格強度旋鈕)

風格 pass 輸出(即使偏寫意)疊在原寫實圖上,**圖層不透明度 50–70%**
= 直接手動調風格強度;分佈對位因兩張同構圖天然吻合。混完若筆觸與照片
噪點打架,可選配再跑一次輕量統一 pass:

```text
Unify this ground texture into a consistent hand-painted finish:
remove the remaining photographic noise so every area shows the same
tight, small brushwork. Do NOT change the layout, colors, texture
scale or detail density — this is a finish-unification pass only.
```

### 1c. 淘汰版 v1(❌ 過度寫意,留作對照)

v1 與 v2 差異:無筆觸尺度/細節密度/苔蘚形態三鎖,且含
`moss becomes clustered painterly clumps with clear light and shadow
planes`(給了往「葉叢」重新解釋的空間)與
`detail is suggested by brushwork, not rendered`(直接授權減密)。
產出:筆觸尺度爆大、苔蘚變側視蕨葉叢、土路寫意漩渦、細節密度大降。
完整 v1 文字見 git 歷史(b8a1b76)。

### 2. 色盤變體句(擇一,取代/追加在主配方結尾)

保留輸入圖自然色(預設):

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

### 3. 驗縫後的縫帶修復

先做 **PS Offset(位移 50%/50%)驗縫**。縫帶小破 → PS 仿製印章/內容感知收掉
(首選,確定性);大面積風格斷裂才考慮 AI 縫修,且只在 offset 版上遮罩限定跑
(Leonardo Canvas inpaint),參考句:

```text
This is the same hand-painted ground texture with the canvas wrapped
(offset by 50%), so the old borders now form a cross-shaped seam
through the middle. Repaint ONLY the narrow seam band so the
brushwork, color and texture flow continuously across it. Everything
outside the seam band stays pixel-identical: same palette, same brush
style, same texture scale. Do not add anything new.
```

> ⚠️ NB2 沒有真遮罩 — 它的「區域修復」= 全圖重繪(B1 教訓)。
> AI 縫修一定要走有遮罩的 inpaint 工具,否則縫修好、全圖又重擲。

---

## 七張套圖量產 SOP(v4 錨鏈依序算)

> 套圖:`T_Forest_Ground_F / Fb / B / Bb / Bc / C / H`(直路×2、純苔×3、
> 轉角、橫路),每張輸出 ≥2048。
> **同輪 strip 出局的原因:** 7×2048=14336px > NB2 上限 4096;硬拼單格只剩
> ~585px,像素預算死(B1 鐵律)。一致性改由錨鏈承擔。

1. **輸入檢查:** 每張寫實 tile 滿版 1:1;Dimensions 設 **2048×2048**
   (輸入 1024 → 2×,安全倍率)。同日、同設定(Enhance/Style = None)跑完全套。
2. **定 master:** 已通過的 v3 成品(對應 `_H` 底部橫路)= master 錨,不重抽。
3. **排程(由易到難,材質最像 master 的先跑):**
   `B → Bb → Bc`(純苔,無路)→ `F → Fb`(直路)→ `C`(轉角)。
4. **每張:** v4 prompt 逐字不動(LAYOUT GUIDE 描述是通用寫法,無需逐張改字),
   ref 1 = 該張寫實 tile、ref 2 = master;**開 4 挑 1**(挑分佈最貼 + 無套外色相)。
5. **全套出完 → PS Match Color:** 每張以 master 為 source 拉齊色盤
   (確定性收尾;輕微色偏不重抽)。
6. **驗縫兩層(排最後,B1「修縫在細節 pass 之後」原則):**
   ① 每張自身 Offset 50/50 驗 wrap;
   ② **套內互拼** — 按接縫規則兩兩拼(F 接 B、H 接 C…),只修縫帶
   (PS 仿製印章優先;AI 只在有遮罩的 inpaint 工具上跑縫帶)。
7. **要 4096:** 全套用**同一個純保真放大器同參數** 2×
   (Real-ESRGAN / Topaz / UU 最低 creativity),禁回鍋 NB2(B3 鐵證)。

成本估算:6 張 × 開 4 = 24 次生成 + master 已在手。

## 管線總覽

```
寫實 tile(1:1 滿版)
  + 材質色票板(圖1–3 裁純地面特寫拼板 — 禁整張餵)
  → NB2 手繪風格化 pass(主配方,1:1 2048)
  → PS Offset 50/50 驗縫 → 縫帶修(PS 優先)
  →(如需 4K)純保真放大分支 2×(Topaz / Real-ESRGAN / UU 最低 creativity;禁回鍋 NB2)
  → 引擎鋪 tile 驗收(3×3 陣列看重複感與縫)
```

## 驗收 checklist

- ☐ 疊回原圖 50% 透明度:苔/土/路分佈圖案重合,只有「畫法」變了
- ☐ 100% 原寸:是筆觸不是「照片+濾鏡」(無殘留照片噪點)
- ☐ 紋理尺度與輸入一致(苔丘沒被畫大一號)
- ☐ PS Offset 50/50:十字縫帶無明顯斷筆/色階跳變
- ☐ 光影無水平方向性(旋轉安全)、無長投影
- ☐ 無越界物件(蘑菇/花/立草/石堆/腳印)
- ☐ 引擎 3×3 鋪排:無高對比筆觸造成的週期重複感
  (若有 → 把該筆觸區在 PS 壓一點對比,或換一張候選)

## 踩坑紀錄

| # | 現象 | 根因 | 解法 |
|---|---|---|---|
| 1 | (v1)筆觸尺度爆大(單筆≈角色寬)、苔蘚被重繪成側視蕨葉叢、土路寫意漩渦、細節密度大降 — 「太過寫意」 | ①只定義「畫法」沒鎖「筆觸尺度/細節密度」→ 模型用自己習慣的大筆觸作畫 ②`painterly clumps with light and shadow planes` 給苔蘚往葉叢重新解釋的空間(B1 踩坑 #6 歧義物件同型)③`detail is suggested, not rendered` 直接授權減密 — 禍首句 | v2 三鎖:**筆觸尺度鎖**(單筆 ≤2% 畫布)+ **細節密度鎖**(100% 原寸小形狀數量≈輸入)+ **苔蘚形態鎖**(low rounded cushions,禁 fronds/ferns/side-view foliage);刪授權減密句 |
| 2 | (v2)輸出≈原圖,風格完全沒轉 — 「沒有變化」 | **保留鎖過量 + edit 定性 = 認同解**:密度鎖綁「跟照片一樣多的小形狀」+「疊圖必須 line up」,等於下令複製輸入;B1 踩坑 #7 同型(保真定性下模型不敢動) | v3 定性反轉:`paint a completely NEW texture from a blank canvas, following reference 1's layout` + **強制重繪條款**(`no photographic pixels may survive — if any region still looks like a photo, that region is wrong`);密度/分佈鎖措辭放軟(macro distribution,不綁 pixel 對齊) |
| 3 | (v3 量產)同 prompt 重抽三張拼不成一套:色盤/明度漂移、土路形狀不同、其中一張長出紅褐苔 — 「單張生成不穩定」 | **NB2 無 seed + 重繪定性 = 高變異**;B1 套圖鐵律(同日同配方同 prompt)只鎖得住保真 pass,鎖不住重繪 pass;色票板只定「畫法」,沒定「這一套的確切色值」 | **v4 成品錨鏈**:ref 2 改掛「已通過的 v3 成品」當 STYLE & PALETTE ANCHOR(`painted by the same artist, in the same session, for the same set` + 禁新色相條款);殘餘色偏用 **PS Match Color**(以 master 為 source)確定性收尾;仍有變異就開 N 挑 1 |
| 4 | (v4 套圖 tile)苔變青綠灌木球、顆粒比 master 大數倍、路變奶黃 — 三鎖全失守,整體掉進「卡通俯視 RPG 地圖」genre | ①**參考圖角色混淆**:ref 1(layout)與 ref 2(master 錨)同為「苔地+土路」tile,外觀高度相似 → 模型分不清「誰管 where 誰管 how」,錨失效後自由發揮 ②「俯視 + 道路」觸發 NB2 的 stylized game map 先驗 ③(檢查項)確認 Enhance/Style 仍為 None ④事後確認:此輪輸入是 **4 合 1 拼圖**(踩坑 #5 的第一次發作) | **v4.1 角色消歧版**:開頭明寫「兩張很像但角色不同」+ WHERE/HOW 分工 + PRIORITY 條款(B2 技法);尺度直接綁 ref 2(`same physical size as in reference 2`);加**反 genre 條款**(`a flat ground TEXTURE, not a stylized game-map illustration — no rounded bush balls`)。更穩走 **master 拼貼統一法**(見 1a-alt) |
| 5 | (4 合 1 生成)四張 tile 拼 2×2 一次跑:材質糊掉、四象限交界被暈接、土路被重新解釋成**石板路**、角落壓暗 — 「合一後變醜」 | ①**像素預算**:2048 輸出下每張 tile 只分到 1024px,微觀苔粒畫不出來 → 糊(B1 白邊 / B2 模組佔比 第四度應驗)②**模型把拼圖當一個場景**:十字交會的路被「合理化」成石板大道、象限交界被暈接、整圖打氣氛光 — 每張 tile 的獨立性與 wrap 邊全毀 ③「俯視地圖」genre 先驗再度觸發 | **tile 生成鐵律:一次一張、單張滿版**。4 合 1 沒有任何補救 prompt — 一致性需求由 v4.1 錨鏈或 1a-alt 拼貼統一法承擔,不由「同輪合成」承擔。拼板唯一合法用途 = 風格參考(色票板),絕不當生成目標 |
| 6 | (v4.1 跑 `_F`)風格全對(色盤/筆觸/苔形同 master,消歧成功),但 ref 1 的貫穿直路中段消失、底部長出 master 的橫向沙帶 — **layout 被錨滲漏**,直路未出下緣,tile 接不了縫 | **成品錨 = 整張 tile = 帶構圖的圖** → B2 踩坑 #1 幾何滲漏在錨身上發作;`Nothing about its layout may be copied` 文字鎖不住(B2 已證);另外「路徑淡出」是模型對長路徑的慣性,需獨立鎖 | **v4.2:master 色票板化** — 把 master 裁成 4–6 塊無構圖材質特寫拼板當 ref 2(風格像素全保留、構圖歸零);加**路徑連續鎖**(`every path must enter and exit the canvas edges exactly where it does in reference 1 — must NOT fade out or stop mid-tile`) |

## 鎖句字典(B8 新增)

| 鎖 | 用途 | 關鍵句 |
|---|---|---|
| **筆觸尺度鎖** | 防大筆寫意化 | `brush strokes stay SMALL — the largest single visible stroke is no wider than 2% of the canvas; stroke size follows the input's texture granularity` |
| **細節密度鎖** | 防風格化=減細節 | `keep the same visual detail density as the input — at 100% zoom roughly the same amount of small shapes, painted crisply instead of photographic noise` |
| **形態鎖(苔蘚)** | 防材質被重新解釋成別種植被 | `moss stays LOW ROUNDED CUSHIONS with fine speckled granularity — do NOT reinterpret as leafy fronds, ferns, bushes or side-view foliage` |
| **收斂定性句** | 給「緊的手繪」心智模型 | `a TIGHT, CONTROLLED hand-painted game texture — painterly but disciplined, NOT a loose concept sketch` |
| **重繪定性句** | 治零變化(edit → 重繪反轉) | `paint a completely NEW hand-painted texture from a blank canvas, following reference 1's layout — a FULL REPAINT, not an edit` |
| **強制重繪條款** | 不留照片像素的驗收律 | `no photographic pixels from reference 1 may survive — if any region still looks like a photo, that region is wrong` |
| **成品錨(同套一致性)** | 治無 seed 重抽漂移 | `a FINISHED TILE from this exact tile set — painted by the same artist, in the same session, for the same set: match its exact palette, value range, brush stroke size and finish` |
| **禁新色相條款** | 防單張長出套外顏色 | `do NOT introduce any hue that does not exist in reference 2 — no red-brown moss, no new path colors` |

## 學到的(累積中)

- ✅ **「手繪風」預設會帶三個副作用:筆觸變大、細節變少、歧義材質被重新解釋。**
  三者都要各自上鎖 — 風格詞只管「像不像手繪」,不管「畫多細」。
- ✅ **正面授權句比禁令危險**(B1「定性句>禁令」的反面):
  `suggested, not rendered` 一句就讓模型合法丟掉一半細節。
  風格 prompt 裡每一句「允許」都要想一遍會被放大成什麼。
- 📌 風格強度最便宜的旋鈕不是 prompt,是 **PS 圖層不透明度**(Plan B)—
  同構圖疊圖天然對位,零抽獎。
- ✅ **風格轉換的力度是單擺,兩端都會死**:v1(風格詞無鎖 → 過度寫意)、
  v2(保留鎖過量 + edit 定性 → 認同解/零變化)。正解結構 =
  **重繪定性(給變化的力)+ 少數硬鎖(給不變的框)** — 鎖要鎖
  「尺度/形態/版面」這些框架量,不能鎖「跟輸入一樣」這種認同量。
- ✅ **B2「增強模式極穩」不適用於風格轉換**:增強(材質變高清)與
  風格轉換(渲染方式整個換掉)是相反方向 — 前者要 edit 定性,
  後者必須重繪定性,拿錯定性就掉進對應的坑(B1 #7 / B8 #2 同型)。
- ✅ **v3 一次通過(重繪定性 + 三鎖組合驗證成立)**:筆觸尺度鎖(≤2%)
  出來的筆觸大小剛好,細節密度、苔蘚形態、分佈、色盤全數保持 —
  「重繪給力、硬鎖給框」的結構是風格轉換的正解模板。
- ✅ **風格參考的滲漏防線可以放寬到「無角色環境圖拼板」**:
  4 張無角色/無 UI 的場景圖拼 2×2,配合輸出端 layout 鎖,未發生
  幾何滲漏 — 拼板本身就稀釋了單張構圖的權重。有角色/UI 才必須
  裁材質特寫(B2 踩坑 #1 的滲漏源是「單張強構圖 + 畫面主體」)。
- ✅ **多張 tile 絕不合一生成(踩坑 #5)**:模型把拼圖讀成「一個場景」—
  交界暈接、道路被合理化成石板、氣氛光壓角;且像素預算腰斬 →
  **筆觸相對變粗、材質糊**(2048 出圖每格只剩 1024,筆觸尺度是絕對
  像素量,格子越小筆觸看起來越粗)。一次一張、單張滿版;
  一致性交給錨鏈/拼貼法,不交給「同輪」。
- ✅ **風格化 pass 的量產一致性要靠「成品錨鏈」,不能靠重抽紀律**:
  NB2 無 seed,重繪定性的輪間變異(色盤/路形)是結構性的 —
  B1 套圖鐵律只對保真 pass 有效。正解 = 第一張定 master →
  之後每張掛 master 當風格+色盤錨(concept-to-3d 的一致性錨協議
  在貼圖管線同樣成立);輕微色偏用 PS Match Color 確定性拉齊,
  重抽只留給形狀級變異。
