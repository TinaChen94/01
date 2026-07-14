# 實戰紀錄 — B8 寫實貼圖 → 手繪風格化(style transfer)提示詞配方

> 寫實風四方連續地面貼圖 → 《Ruined King》/ Battle Chasers 級手繪厚塗風格。
> 對應工作流:`ai-media-generator`;前置知識:[B1](B1-forest-bg-4k-detail.md)(鎖句字典)、
> [B2](B2-greybox-module-pipeline.md)(圖案活化/材質色票板/頂光)、
> [B3](B3-fenske-painterly-4k.md)(手繪風 ×  NB2 保真 pass 禁忌)。

**🔑 關鍵字:** `B8`、`風格轉換`、`手繪風格化`、`style transfer`、`厚塗`、
`hand-painted`、`Ruined King 風`、`四方連續風格化`、`tileable 風格轉換`、
`筆觸化`、`寫實轉手繪`

**狀態:⏳ 實戰中 — 第 1 輪(v1)過度寫意已淘汰,v2 收斂版(筆觸尺度鎖 + 細節密度鎖 + 苔蘚形態鎖)待驗。**

## 來源(索引)

- **輸入素材:** 寫實風四方連續地面貼圖(1:1,苔蘚坡地 + 底部土路,日光自然色)
- **風格目標:** 《Ruined King: A League of Legends Story》遊戲截圖 ×3
  (青綠夜色石板競技場 ×2、暖色叢林土地 ×1)
- **平台:** Leonardo.ai AI Creation / **Nano Banana 2**(沿用 B1/B2 主力)
- **任務定性:** B2 的「增強」模式 — 圖案分佈是真相,AI 只換「渲染方式」
  (照片噪點 → 手繪筆觸);**不是**從零生成

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

### 1. 主配方 v2 — 收斂版手繪風格化 pass(ref 1 = 寫實貼圖、ref 2 = 材質色票板)

v1 過度寫意後的修正版:新增**筆觸尺度鎖、細節密度鎖、苔蘚形態鎖**,
並刪除 v1 的授權減密句(`detail is suggested by brushwork, not rendered`)。

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

## 鎖句字典(B8 新增)

| 鎖 | 用途 | 關鍵句 |
|---|---|---|
| **筆觸尺度鎖** | 防大筆寫意化 | `brush strokes stay SMALL — the largest single visible stroke is no wider than 2% of the canvas; stroke size follows the input's texture granularity` |
| **細節密度鎖** | 防風格化=減細節 | `keep the same visual detail density as the input — at 100% zoom roughly the same amount of small shapes, painted crisply instead of photographic noise` |
| **形態鎖(苔蘚)** | 防材質被重新解釋成別種植被 | `moss stays LOW ROUNDED CUSHIONS with fine speckled granularity — do NOT reinterpret as leafy fronds, ferns, bushes or side-view foliage` |
| **收斂定性句** | 給「緊的手繪」心智模型 | `a TIGHT, CONTROLLED hand-painted game texture — painterly but disciplined, NOT a loose concept sketch` |

## 學到的(累積中)

- ✅ **「手繪風」預設會帶三個副作用:筆觸變大、細節變少、歧義材質被重新解釋。**
  三者都要各自上鎖 — 風格詞只管「像不像手繪」,不管「畫多細」。
- ✅ **正面授權句比禁令危險**(B1「定性句>禁令」的反面):
  `suggested, not rendered` 一句就讓模型合法丟掉一半細節。
  風格 prompt 裡每一句「允許」都要想一遍會被放大成什麼。
- 📌 風格強度最便宜的旋鈕不是 prompt,是 **PS 圖層不透明度**(Plan B)—
  同構圖疊圖天然對位,零抽獎。
