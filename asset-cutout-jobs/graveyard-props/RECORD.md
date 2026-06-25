# 紀錄 — Graveyard Props Pack 去背

> Asset-cutout job log. SOP: [`.claude/skills/asset-cutout/SKILL.md`](../../.claude/skills/asset-cutout/SKILL.md)
> 日期 2026-06-23 · 分支 `claude/adoring-lamport-sh6fgh`

## 來源 / Source
哥德式墓園概念圖(green-teal 霧林 + 紫光彩窗陵墓)。本 job 只抽 **props pack**:墓碑 + 鐵欄杆 + 石門柱。建築主體與地景不在本包。

## 決策 / Decisions
| 項目 | 選擇 | 理由 |
|---|---|---|
| 模式 | **1.1 去背 + 補圖(keep pixels)** | 保留原像素,補回被霧/欄杆/草遮住的缺角 |
| 背景 | **flat `#808080`** → matte 成透明母檔 | 場景同時有綠(苔/霧)+ 洋紅(紫光) → 綠幕/洋紅幕都不能用(§2);端點不出 alpha → 先灰底再去背 |
| 色彩鎖 | 鎖 **綠苔 + 粉紫地衣/小花** weathering | 防 model 把風化當髒污「洗乾淨」 |

## 資產狀態 / Asset status
| # | 資產 | 模式 | 出圖模型 | 狀態 | 備註 / QA |
|---|---|---|---|---|---|
| A | 鐵欄杆(連續 panel + 石基座) | 1.1 | Nano Banana (Gemini) | ✅ 已出 | 苔/鏽 patina 保留、矛尖 picket 連續。⚠️ 右下 ✦ 浮水印待裁;⚠️ 仍 RGB 灰底,待 matte |
| B | 石門柱 ×2(finial + 雕花鏡像對) | 1.1 | Nano Banana (Gemini) | ✅ 已出 | finial/卷草雕花/苔斑保留。⚠️ 同 ✦ 浮水印;若要單根可再切 1 根 |
| C | 墓碑 ×5–7(各自獨立) | 1.1 | — | ⏳ 待做 | 逐塊跑;crowded 區用 Seedream bounding-box visual cue |

## 待辦 / TODO（finalize 前必做）
- [ ] **裁掉 ✦ 浮水印**（A、B 右下角 Gemini/Nano Banana signature)— crop 或 inpaint
- [ ] **matte 灰底 → 透明母檔**:`rembg i x_grey.png x.png`（`#808080` 與資產無重疊 → 邊乾淨)
- [ ] 各存兩版:透明 PNG = **母檔**;`#808080` = **turnaround ref**(§6)
- [ ] 墓碑 ×5–7 逐塊去背(prompt 見下)
- [ ] (選)門柱對切成單根可重用 prop

## 用過的 prompt / Prompts used（可複現)

### A — 鐵欄杆
```text
Keep ONLY the black wrought-iron fence with its spear-tip pickets and the low
stone base it sits on; remove the green fog, the tombstones in front of it, the
ivy/shrubs growing through it, and everything else, and make the background a
flat #808080 grey. Where the fence is hidden behind fog, foliage, or
tombstones, reconstruct the missing pickets and rails into one continuous
unbroken panel, matching the existing picket spacing and ironwork — do NOT
invent new shapes or ornaments. The rust patina and green moss on the iron and
stone are PART of the fence — preserve their exact colors and weathering; do
NOT clean, repaint, recolor, or remove them. Keep everything else unchanged.
```

### B — 石門柱(對)
```text
Keep ONLY the pair of weathered stone gate pillars with their carved finial
tops; remove the iron fence, fog, steps, tombstones, foliage, and everything
else, and make the background a flat #808080 grey. Where each pillar is hidden
behind fog or adjacent railings, reconstruct the missing stone to complete the
full pillar from base to finial, matching the existing carving and erosion — do
NOT invent new structures. The green moss and lichen on the stone are PART of
the pillars — preserve their exact colors; do NOT clean or recolor them. Keep
everything else unchanged.
```

### C — 墓碑(逐塊,換 <descriptor>/<position>)
```text
Keep ONLY the single <LEANING MOSSY / TALL UPRIGHT / BROKEN SLAB> tombstone
<left of the path, foreground / nearest the fence on the right / ...>; remove
all other gravestones, the grass, fog, foliage, and everything else, and make
the background a flat #808080 grey. Where the base is buried in grass or moss,
reconstruct the missing lower portion to complete the whole slab, matching its
shape and material — do NOT invent new carvings. The green moss and pinkish
lichen and small flowers on the stone are PART of it — preserve their exact
colors and weathering; do NOT clean, scrub, recolor, or remove them. Keep
everything else unchanged.
```

**Negative（全用):**
```text
blurry, low quality, watermark, text, duplicated extra objects, perspective
distortion, harsh cast shadows, busy background, oversaturated
```

## 產物 / Output
PNG 放 `./assets/`(目前佔位 `.gitkeep`;貼圖時換成實檔):
```
assets/fence_panel_grey.png      assets/fence_panel.png        (透明母檔)
assets/gate_post_pair_grey.png   assets/gate_post_pair.png
assets/tombstone_01_grey.png     assets/tombstone_01.png       ...
```
灰底 ↔ 透明互轉(§6):
```bash
rembg i fence_panel_grey.png fence_panel.png            # 灰底 → 透明
magick fence_panel.png -background "#808080" -flatten fence_panel_grey.png  # 透明 → 灰底
```
