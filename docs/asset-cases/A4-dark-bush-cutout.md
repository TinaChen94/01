# 實戰紀錄 — A4 明亮森林深色圓叢灌木拆件 — 去背 + 補圖(洋紅底)

> 概念圖拆資產 / 去背 + 補圖案例。對應工作流:`/asset-cutout` **模式 1.1(edit/inpaint,保留原像素)**。
> 目標:從明亮 mid-key JRPG 森林背景(B11 同風格)拆出**深色圓叢灌木**(深墨綠、低細節、當背景填充的圓團塊),**不是**搶眼的亮蕨。
> 本案例沿用 A3 兩大核心:**緊裁換主角**(治「亮蕨搶戲」)、**洋紅工作底 + 殘留手動分流**。

## 來源(索引)

- **生成平台:** Google Gemini(Nano Banana 2 edit)/ Seedream edit 思路(實際生成在使用者端跑)
- **日期:** 2026-07-31
- **原始素材:** 明亮 JRPG 森林背景概念圖(古樹拱門 + 亮劍蕨/鳥巢蕨 + 藍菇 + 苔地);使用者以**紅圈標記三處深色圓叢**為拆件目標
- **開發分支:** `claude/plant-concept-breakdown-n8y1o1`
- **背景色決策:** 工作底色 `#FF00FF` 洋紅(本資產=深綠,無洋紅=缺席色);綠幕吃綠叢、`#808080` 撞深綠中間調 → 皆不可用。印證 asset-cutout 表 B「挑資產缺席色」,與 A3 同一森林世界共用。

## 目標盤點 — 三圈深色叢(3 件)

| # | 資產 | 位置 | 遮擋程度 | 特記 |
|---|---|---|---|---|
| 叢L | 深色圓叢 · 左圈 | 亮劍蕨右後方 | 中(蕨葉壓前) | 亮劍蕨顯著度搶戲 → 緊裁 |
| 叢M | 深色叢 · 中圈 | 鳥巢蕨左側偏後 | 高(蕨+樹幹) | 遮擋最高,務必裁到深叢佔比 ≥50% |
| 叢R | 深色圓叢 · 右圈 | 右側圓叢帶藤蔓 | 中 | **最完整 → 建議當 hero 母株,先跑** |

> 深色叢 = 低細節暗部團塊,天生顯著度輸給亮蕨/鳥巢蕨;**純文字「keep only 深叢」會被搶戲(A3 教訓 1)→ 一律緊裁換主角。**

## 決策表(照 asset-cutout SOP)

| 項目 | 決定 | 理由 |
|---|---|---|
| 去背模式 | **1.1 去背 + 補圖** | 深叢被亮蕨/樹幹/藤蔓遮住缺角,要補回圓輪廓;要保留原像素 |
| 工作底色 | **洋紅 `#FF00FF`** | 深叢是綠 → 綠幕吃掉;灰 `#808080` 撞深綠中間調;洋紅=缺席色(同 A3) |
| 裁圖 | **緊裁換主角**(A3 教訓 1) | 亮蕨壓過深叢 → 裁到深叢是唯一完整團塊,亮蕨只留無完整輪廓的邊緣 |
| 色鎖 | 鎖深墨綠、禁提亮/去飽和 | 深叢無發光色,但生成偏好把暗部提亮 → 明講鎖住 |

## 定案管線(沿用 A3)

```
原圖(高解析)
 └─ 裁圖:深叢佔畫面 ≥50%,邊距 10–15%(像素預算,B2 Crop-Gen-Paste)
     │   亮蕨/樹幹等遮擋物 → 只裁「貼著深叢的一段」,絕不讓亮蕨完整輪廓入鏡
     └─ 模式 1.1 edit prompt(洋紅底句 + 深綠色鎖 + remove 清單)
         └─ 一次一叢,reroll 1–3 張挑圖(驗收:可見半邊嚴比團塊形;補回側只看風格+無滲漏)
             └─ 殘留分流:孤立於平坦底 → 手動填 #FF00FF(10 秒)
             │           與主體交疊 → 單目標 cleanup pass(一次一事)
             └─ 色鍵去洋紅(開 spill suppression、關 Decontaminate Colors)
                 └─ 透明 PNG 母檔 + #808080 灰底版(洋紅版只當工作檔,不入庫)
```

## 逐字 prompt(規劃版,待實跑)

### 通用版(叢R,最乾淨,先跑這張)

```text
Keep ONLY the dark rounded leafy bush in the center of the image — the deep
teal-green hand-painted foliage clump. Remove the bright green ferns, the
bird's-nest fern, the tree trunks and roots, the ivy vines, the ground grass,
the mushrooms, the distant forest, and everything else, and place it on a flat,
solid, uniform magenta #FF00FF (RGB 255, 0, 255) background that fills the
entire background area — no gradient, no vignette, no shadow. Where the bush is
hidden behind fern fronds, trunks, or cut off by the image edge, reconstruct the
missing foliage to complete its rounded silhouette, matching the existing dark
leafy clumps and painterly brush style — do NOT invent new plants or add flowers.
Keep its dark teal-green painterly colors and soft leaf clumps exactly — do NOT
brighten, desaturate, or recolor it. Keep everything else unchanged.
```

### 叢L / 叢M(同一份,只改開頭空間詞 + remove 清單首位)

- **叢L** 開頭改:`Keep ONLY the dark rounded bush to the right of and behind the large bright sword fern`;remove 清單首位加:`the large bright arching sword fern in front`。
- **叢M** 開頭改:`Keep ONLY the dark flat-topped bush mass left of the bird's-nest fern`;remove 清單首位加:`the bright bird's-nest fern and the feathery fern beside it`。此張遮擋最高 → **務必裁到深叢佔比 ≥50%、亮蕨只剩無完整輪廓的一角。**

### 負面

```text
blurry, low quality, watermark, text, extra plants, flowers, bright highlights,
perspective distortion, cast shadow, busy background, oversaturated
```

## 鎖句字典(本案例沿用/新增)

| 鎖句 | 用途 | 狀態 |
|---|---|---|
| `place it on a flat, solid, uniform magenta #FF00FF (RGB 255, 0, 255) background that fills the entire background area — no gradient, no vignette, no shadow` | 洋紅工作底;色名+hex+RGB 三保險(A3 沿用) | ✅ 沿用 |
| `Keep its dark teal-green painterly colors and soft leaf clumps exactly — do NOT brighten, desaturate, or recolor it.` | 深叢暗部色鎖(治生成提亮暗部) | ⏳ 待驗 |
| `reconstruct the missing foliage to complete its rounded silhouette, matching the existing dark leafy clumps ... do NOT invent new plants or add flowers` | 圓輪廓補回 + 幾何滲漏鎖(A3 樹形鎖換植被版) | ⏳ 待驗 |

## 驗收雙標準(沿用 A3 教訓 8)

- **可見半邊:** 嚴比原圖團塊外形、葉簇分佈、暗部色。
- **補回側:** 無 ground truth → 只驗風格一致(painterly 葉簇)+ 無幾何滲漏(偷長第二叢/憑空加花)。
- **另檢:** cast shadow 違規(有禁令仍偶發,色鍵會留髒邊 → 淘汰該張);右下 Gemini ✨ 浮水印固定手動填色。

## 狀態

⏳ **規劃完成、待實跑。** 配方(模式/底色/裁圖/逐字 prompt)已定,實際生成需在使用者端 Gemini/Leonardo 跑;跑完回填批次成功率、逐張判定與成品圖(比照 A3 表格)。

### 圖檔索引(待補)

| 檔名 | 內容 | 狀態 |
|---|---|---|
| `a4-source-annotated.jpg` | 原圖 + 三紅圈拆件標記 | ⏳ 待使用者上傳 |
| `a4-crop-bush-{L,M,R}.jpg` | 三叢緊裁圖(亮蕨只留邊緣一角) | ⏳ |
| `a4-gen-*` | 生成批次,逐張判定 | ⏳ |

## 學到的(一句話版,待實跑驗證)

**深色填充叢的難點不在「像素」在「顯著度」:它天生輸給亮蕨 → 先靠緊裁把它變成畫面主角,prompt 只負責鎖深綠色 + 補圓輪廓;洋紅工作底 + 殘留手動分流收尾,即 A3 配方的植被填充版。**
