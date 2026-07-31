# 實戰紀錄 — A4 明亮森林植被叢「忠實區域去背」(三圈原樣拆件)

> 概念圖拆資產 / 去背案例。對應工作流:`/asset-cutout`。
> 目標:把使用者在明亮 mid-key JRPG 森林背景(B11 同風格)上**紅圈標記的 3 個區域**,
> **原封不動地去背**(圈內畫面原樣保留,只換背景 + 只補被前景擋住的缺口),背景填純色。
> **不是**把某個植物當「品種」重畫成乾淨單株。

## 核心教訓(本案例第一手,務必先讀)

**忠實區域去背 ≠ 單株品種重建。** 首輪誤把目標寫成
`keep ONLY the dark bush / remove the ferns / reconstruct to complete its rounded silhouette`
→ 模型丟掉原畫、**重繪成一顆通用圓球灌木**(掉進模式 1.2 重新生成),原筆觸/葉形全失真。

> **正解要反過來:保留圈內全部原像素,只換背景、只補「被前景擋住」的洞。**
> 主詞從「keep ONLY <某株>」改成「keep ALL foliage as painted」;
> 動作從「reconstruct / complete silhouette」改成「ONLY change bg + ONLY fill covered gaps」。

## 來源(索引)

- **平台:** 純去背走 remove.bg / rembg / SAM / PS;補遮擋走 Gemini NB2 / Seedream edit(實際生成在使用者端跑)
- **日期:** 2026-07-31
- **原始素材:** 明亮 JRPG 森林背景概念圖(古樹拱門 + 亮劍蕨/鳥巢蕨 + 藍菇 + 苔地);使用者以**紅圈標記三處植被叢**,要求各自原樣去背
- **開發分支:** `claude/plant-concept-breakdown-n8y1o1`

## 目標盤點 — 三圈(3 件,各自整區去背)

| # | 圈 | 內容(原樣保留) | 前景遮擋 | 建議路線 |
|---|---|---|---|---|
| 圈L | 左 | 亮劍蕨 + 深叢 + 地面藤蔓/小葉叢(整團) | 低 | **A 純去背** |
| 圈M | 中 | 蕨 + 鳥巢蕨 + 深叢團塊 | 高(大樹幹穿過) | **B 去背+補遮擋** |
| 圈R | 右 | 深圓叢 + 藤蔓 + 蕨(整團) | 低–中 | **A 純去背**(缺口小手補) |

## 兩路線決策(照 asset-cutout 表 A)

```
圈內幾乎沒被前景擋 ───► 路線 A 純 matting(模式 1.0):零重畫、最忠實
                         裁圈 → remove.bg/rembg/SAM/PS「選取主體」→ 透明 → 墊純色
                         被樹幹穿過的小缺口 → PS 手補幾筆,或不管
前景樹幹/枝大幅穿過 ───► 路線 B 去背+補遮擋(模式 1.1):edit + 保真鎖 prompt
                         只換底 + 只補被擋處,接受少量重繪風險 → reroll 挑圖
```

> **先裁圈:** 把每個紅圈區域裁成一張獨立圖 —— 裁框本身就是選區,去背只需處理「圈內 vs 圈外」,不必靠文字指認哪株。

## 逐字 prompt

### 路線 A — 純去背(無 prompt,工具操作)

```
1. 裁圈 → 獨立圖
2. remove.bg / rembg / SAM / PS「選取主體」→ 透明 PNG(母檔)
   ⚠️ matting 設定:開邊緣羽化、關「淨化顏色 / Decontaminate Colors」(保半透明葉緣 bloom)
3. 墊純色:透明母檔上加純色填色圖層(洋紅/灰/任意皆可,語意分割不需色鍵)
   magick in.png -background "#808080" -flatten out.png
4. 被前景穿過的缺口小 → PS 仿製章手補;缺口大 → 改走路線 B
```

### 路線 B — 去背 + 補遮擋(保真鎖,餵裁好的單圈)· 定版

> 目標鎖定:**三圈裡的「深色叢灌木」那一團**(非整區、非亮蕨)。
> 治「假圓球」關鍵:**拿掉** `reconstruct / complete rounded silhouette`,
> **改成** `Do NOT turn it into a smooth round bush` + `keep its natural silhouette`。

```text
Keep the dark leafy shrub exactly as it is painted in this image — same shape,
same leaves, same dark teal-green colors and brushstrokes. Do NOT repaint it,
do NOT turn it into a smooth round bush. Remove everything else — the bright
ferns, tree trunks, ivy, grass, mushrooms, background forest — and put the
shrub on a solid magenta #FF00FF background. Only where the shrub is hidden
behind a trunk or fern, fill that gap with matching dark leaves so it stays in
one piece. Keep its natural silhouette.
```

三圈深叢定位:左圈=亮蕨右後那團 · 中圈=鳥巢蕨後方那團 · 右圈=最完整那團。

### 負面

```text
repaint, re-render, regenerate, new plant, generic round bush, smoothed leaves,
changed silhouette, gradient background, vignette, cast shadow, watermark, text
```

## 鎖句字典(本案例新增)

| 鎖句 | 用途 | 狀態 |
|---|---|---|
| `Keep ALL the foliage EXACTLY as painted ... Do NOT repaint, redraw, smooth, re-render, or restyle any plant` | 忠實鎖:防 edit 模型把整區重繪(治「通用圓球」失真) | ⏳ 待驗 |
| `ONLY change the background ... fill ONLY those covered gaps ... do NOT change the overall silhouette` | 限縮動作:只換底 + 只補被擋處,不許重建輪廓 | ⏳ 待驗 |
| `place ... magenta #FF00FF (RGB 255,0,255) ... no gradient, no vignette, no shadow`(A3 沿用) | edit 路線的純色底 | ✅ 沿用 |

## 對照表(錯 vs 對)

| | 首輪(❌ 變通用圓球) | 修正(✅ 忠實去背) |
|---|---|---|
| 主詞 | `keep ONLY the dark bush` | `keep ALL the foliage as painted` |
| 動作 | `reconstruct / complete silhouette` | `ONLY change bg + ONLY fill covered gaps` |
| 模式 | 滑進 1.2 重新生成 | 鎖在 1.0 matting / 1.1 保真 edit |
| 結果 | 原畫丟失、重畫圓球 | 圈內原樣保留 |

## 驗收

- **主判:** 去背後把可見部分疊回原圖同位置比對 —— 葉形/筆觸/色值需**逐點吻合**(這是忠實去背,有 ground truth,不接受風格漂移)。
- **補遮擋處:** 只驗與鄰葉風格一致、無新增植物/花;輪廓不得被改。
- **另檢:** 邊緣殘留半透明底色(路線 A 關 Decontaminate)、右下 Gemini ✨ 浮水印(路線 B 手動填色)。

## 狀態

✅ **保真 prompt 首次實測成功(2026-07-31,使用者端 Gemini)。** 深叢保留原筆觸/葉形/暗色,
**未再變假圓球** → 定版 prompt(拿掉 reconstruct/complete silhouette + 加 keep natural silhouette)有效。

**本輪待收兩點:**
1. **整張圖丟進去 → 三圈深叢黏成一整條**(模型合併)。要各圈獨立資產 → 先裁單圈再跑;要一整條背景牆 → 可直接用。
2. **底部殘留亮綠小草叢 + 右下 ✨ 浮水印**。收尾句:
   `Also remove every bright light-green fern, grass blade, and low ground plant — keep ONLY the dark teal-green shrub masses. Remove any sparkle or watermark.`
   或孤立殘留直接手動擦(套索填 #FF00FF,10 秒)。

### 圖檔索引(待補)

| 檔名 | 內容 | 狀態 |
|---|---|---|
| `a4-source-annotated.jpg` | 原圖 + 三紅圈標記 | ⏳ 待使用者上傳 |
| `a4-crop-{L,M,R}.jpg` | 三圈裁圖(=選區) | ⏳ |
| `a4-cutout-{L,M,R}.png` | 三圈去背成品(透明母檔) | ⏳ |
| `a4-fail-generic-bush.png` | 首輪失真範例(通用圓球,重繪教訓) | ⏳ 使用者手邊已有 |

## 學到的(一句話版)

**忠實區域去背的成敗在「主詞與動作」:主詞要 `keep ALL as painted`(不是 keep only 某株)、動作要 `only change bg + only fill covered gaps`(不是 reconstruct)——一寫成「重建完整輪廓」就滑進重繪,原畫必失真。能純 matting 就別用 edit;要補遮擋才用 edit + 保真鎖。**
