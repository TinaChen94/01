# 實戰紀錄 — B8 寫實貼圖 → 手繪風格化(style transfer)提示詞配方

> 寫實風四方連續地面貼圖 → 《Ruined King》/ Battle Chasers 級手繪厚塗風格。
> 對應工作流:`ai-media-generator`;前置知識:[B1](B1-forest-bg-4k-detail.md)(鎖句字典)、
> [B2](B2-greybox-module-pipeline.md)(圖案活化/材質色票板/頂光)、
> [B3](B3-fenske-painterly-4k.md)(手繪風 ×  NB2 保真 pass 禁忌)。

**🔑 關鍵字:** `B8`、`風格轉換`、`手繪風格化`、`style transfer`、`厚塗`、
`hand-painted`、`Ruined King 風`、`四方連續風格化`、`tileable 風格轉換`、
`筆觸化`、`寫實轉手繪`

**狀態:⏳ 草案 — prompt 配方設計完成,未實戰。實戰後補產出圖與踩坑。**

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

### 1. 主配方 — 手繪風格化 pass(ref 1 = 寫實貼圖、ref 2 = 材質色票板)

```text
Reference image 1 is the BASE — a seamless, tileable ground texture
(near top-down): green moss slopes with exposed dirt and a sandy path
along the bottom. Its layout is the truth: the moss / dirt / path
DISTRIBUTION PATTERN, the texture scale, and the square 1:1 canvas are
all correct and final.

Reference image 2 is the STYLE TARGET — cropped material swatches from
a hand-painted stylized game. Use it ONLY for the painting technique:
confident visible brushstrokes, simplified chunky planar shapes,
stepped value planes, exaggerated value structure, hue-shifted shadows
that lean teal instead of black, crisp painted edge accents, and a
gouache-like matte finish. Do NOT copy any layout, objects or
composition from it.

TASK: repaint reference 1 in reference 2's hand-painted style — as if
a concept artist repainted the SAME ground by hand. Replace all
photographic noise and photo grain with deliberate brush marks: moss
becomes clustered painterly clumps with clear light and shadow planes;
dirt and the sandy path become broad warm strokes with a few crisp
accents; detail is suggested by brushwork, not rendered.

KEEP EXACTLY: the square 1:1 canvas (do NOT crop, zoom, extend or
outpaint), the distribution pattern of moss / dirt / path, and the
texture scale — identical to the input. The texture must remain
SEAMLESSLY TILEABLE: the left and right edges must wrap perfectly
into each other, and the top and bottom edges must wrap perfectly
into each other — brushwork flows continuously across the borders.

LIGHTING: soft light from straight above (zenith) only — moss clump
tops catch gentle light, crevices fall into soft painted shadow; no
horizontal light direction, no long cast shadows.

Do NOT add any objects: no plants, flowers, mushrooms, standing grass
tufts, stones, props, characters or footprints.
```

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

## 學到的(實戰後補)

- (待補)
