# 實戰紀錄 — A3 夜森林枯樹拆件 — 去背 + 補圖(洋紅底)

> 概念圖拆資產 / 去背 + 補圖案例。對應工作流:`/asset-cutout` **模式 1.1(edit/inpaint,保留原像素)**。
> 本案例核心新知:**主體顯著度搶戲 → 用「緊裁換主角」解;孤立殘留 → 手動填色,不耗生成 pass。**

## 來源(索引)

- **生成平台:** Google Gemini(Nano Banana 2 edit)
- **日期:** 2026-07-19
- **原始素材:** 夜森林概念圖(雙月 + 骷髏雲 + 拱門雙樹 + 青綠發光裂紋),標記 4 物件拆件,實作中擴為 6 件
- **背景色決策:** 工作底色 `#FF00FF` 洋紅(本包資產無洋紅 = 缺席色);`#808080` 撞樹皮/骨灰、橘 `#FF6A00` 撞層架菌/枯草 → 皆不可用。印證 asset-cutout 表 B「挑資產缺席色」。

## 資產清單(6 件)

| # | 資產 | 遮擋程度 | 特記 |
|---|---|---|---|
| 1 | 左側拱門主樹(青綠裂紋+苔蘚+層架菌) | 中(霧/交錯枝) | 殘留手動補 |
| 2 | 右側拱門主樹(同上鏡像) | 中 | remove 清單全套烙進第一輪 |
| 3 | 左根部骸骨叢(頭骨×3+散骨) | 高(藏樹根) | 獨立地面 prop,補土墩底座 |
| 4 | 右根部頭骨+散骨 | 高 | 同上,規模小 |
| 5 | 左場景背景小樹(faint 青綠裂紋) | 極高(半棵藏主樹後) | 緊裁換主角後才成功 |
| 6 | 右場景背景小樹 | 極高 | 緊裁後一次過 |

## 定案管線

```
原圖(高解析)
 └─ 裁圖:物件佔畫面 ≥50%,邊距 10–15%(像素預算,B2 Crop-Gen-Paste)
     │   被遮物件 → 遮擋物只裁「貼著主體的一段」,絕不讓遮擋物完整樹形入鏡
     └─ 模式 1.1 edit prompt(洋紅底句 + 色彩鎖句 + remove 標配清單)
         └─ 一次一件,reroll 1–3 張挑圖(驗收:只嚴比可見半邊;重建側只看風格)
             └─ 殘留分流:孤立於平坦底 → 手動填 #FF00FF(10 秒)
             │           與主體交疊 → 單目標 cleanup pass(一次一事)
             └─ 色鍵去洋紅(開 spill suppression、關 Decontaminate Colors)
                 └─ 透明 PNG 母檔 + #808080 灰底版(洋紅版只當工作檔,不入庫)
```

---

## 逐字 prompt(驗證通過版)

### 1. 主樹模板(踩坑教訓已烙進 remove 清單)

```text
Keep ONLY the large twisted dead tree in the center of the image — the one
with the glowing teal-cyan cracks on its trunk. Remove the mossy tree trunk
at the far left edge, the smaller background trees, the background forest,
the skulls and bones at the base, fog, sky, moons, path, all spiderwebs, the
white diamond-shaped sparkle, and everything else, and place it on a flat,
solid, uniform magenta #FF00FF (RGB 255, 0, 255) background that fills the
entire background area — no gradient, no vignette, no shadow. Where branches
or roots are cut off by the image edge or hidden behind fog, reconstruct
them and complete the silhouette with natural tapering branch and root tips,
matching the existing gnarled bark material — do NOT invent new structures.
Keep the moss, hanging lichen, and shelf fungi on the trunk. The glowing
teal-cyan cracks and their soft emissive bloom are PART of the subject —
preserve their exact color and glow, do NOT dim, desaturate, recolor, or
remove them. Keep everything else unchanged.
```

### 2. 根部骸骨叢(獨立地面 prop)

```text
Keep ONLY the cluster of skulls and bones nestled in the mossy roots at the
base of the large central tree. Remove the tree trunk, branches, path, fog,
all spiderwebs, the white diamond-shaped sparkle, and everything else, and
place it on a flat, solid, uniform #FF00FF magenta background — no gradient,
no vignette, no shadow on the background. Where the bones or roots are hidden
behind the trunk or buried in soil, reconstruct the missing parts and finish
the base with a small clump of dark earth so it reads as a self-contained
ground prop. Match the existing aged bone, root bark, and moss materials —
do NOT invent new structures or add extra skulls. Keep everything else
unchanged.
```

### 3. 背景小樹(極高遮擋 — 必須先「緊裁換主角」)

前置:以小樹為中心緊裁 — 小樹 = 畫面唯一完整樹形、佔比 ≥50%;
遮擋主樹只留無頭無根的柱狀前景(從左/右緣進場,方位詞跟著改)。

```text
The image shows a bare dead tree in the center, partially hidden behind the
thick mossy trunk of a larger foreground tree entering from the left edge.
Keep ONLY the smaller bare dead tree in the center — the one with faint
teal-cyan cracks on its trunk. Remove the foreground trunk and its roots,
the background forest, fog, the red glowing eyes in the distance, all
spiderwebs, the grass, and everything else, and place the tree on a flat,
solid, uniform magenta #FF00FF (RGB 255, 0, 255) background that fills the
entire background area — no gradient, no vignette, no shadow. Where the tree
is hidden behind the foreground trunk or cut off by the image edge,
reconstruct the hidden trunk, branches, and root base, and complete it as
ONE whole free-standing tree with natural tapering branch tips, matching its
existing gnarled bark and silhouette style. Do NOT invent structures beyond
completing this one tree — no extra trees, no moss, fungi, skulls, or webs.
The faint glowing teal-cyan cracks are PART of the subject — preserve their
exact color and glow. Keep the visible parts exactly unchanged.
```

### 4. Cleanup pass(單目標,只在殘留與主體交疊時用)

```text
Remove the smaller bare dead tree standing behind and to the right of the
main tree's trunk — the one rising from behind the root mound. Fill the
revealed areas with the same flat, solid, uniform #FF00FF background. Where
the removed tree overlapped the main tree, reconstruct the main tree's bark
and root edges cleanly. Do NOT change anything else — keep the main tree's
shape, bark, moss, shelf fungi, and the glowing teal-cyan cracks exactly
unchanged.
```

### 5. 失敗輸出跳板句(Plan B — 場景已簡化成「洋紅底 + 兩物件」時)

```text
Two dead trees stand on a flat magenta background: a large one in the
foreground and a smaller one behind it to the right. DELETE the large
foreground tree completely and keep ONLY the smaller tree. Reconstruct the
parts of the smaller tree that were hidden behind the foreground tree,
completing it as ONE whole free-standing tree matching its existing bark and
silhouette style. Fill everything else with the same flat, solid, uniform
magenta #FF00FF background.
```

## 鎖句字典(本案例新增/驗證)

| 鎖句 | 用途 | 狀態 |
|---|---|---|
| `place it on a flat, solid, uniform magenta #FF00FF (RGB 255, 0, 255) background that fills the entire background area — no gradient, no vignette, no shadow` | 洋紅工作底;色名+hex+RGB 三保險 | ✅ |
| `The glowing teal-cyan cracks and their soft emissive bloom are PART of the subject — preserve their exact color and glow, do NOT dim, desaturate, recolor, or remove them.` | 青綠發光裂紋鎖(A1 紫窗鎖句換色沿用) | ✅ |
| remove 標配清單:`all spiderwebs, the smaller background trees, the white diamond-shaped sparkle, the red glowing eyes in the distance` | 第一輪就排除,省 cleanup pass | ✅ |
| `Do NOT invent structures beyond completing this one tree — no extra trees, no moss, fungi, skulls, or webs` | 高遮擋重建的幾何滲漏鎖 | ✅ |

---

## 踩坑(可複用教訓)

1. **主體顯著度搶戲 — 純文字空間指定壓不過畫面最大物件。**「keep only 後面那棵小樹」連跑數次,模型都把最大最完整的主樹當主角(甚至進入重繪模式把整包重畫)。**解法 = 緊裁換主角**:裁到目標是畫面唯一完整樹形,遮擋物只剩無頭無根的柱狀前景 → 一次過。加強語氣、加字均無效(B2 教訓再驗證)。
2. **模型會拒刪「高顯著殘留」。** 左緣帶亮青綠裂紋的殘幹,cleanup pass 點名三次都不刪。**孤立在平坦底色上的殘留一律手動套索填 `#FF00FF`(10 秒、零風險)**,只有與主體交疊的殘留才值得生成 pass。
3. **每疊一輪 pass = 全圖重編碼一次。** 實測第二輪輸出解析度掉檔(≈2K→1K)、苔蘚細節與裂紋 bloom 同步衰減。修正盡量回到最高保真的那一輪上做;掉的解析度照 B1 配方 Universal Upscaler 2× 最低 creativity 拉回。
4. **半透明元素(蜘蛛網)會透出底色,染色後救不回。** 網壓在洋紅上整片帶粉紅殘紋 → 場景裝飾物在**第一輪** remove 清單就排除,不留到後段。
5. **faint 發光會被放大。** 原圖一條淡裂紋,輸出變多條亮裂紋 — 生成偏好,字壓不住;解法 = reroll 挑圖或後製壓暗,不改 prompt 硬跑。
6. **失敗輸出可當跳板。** 拆件失敗但場景已簡化成「洋紅底+兩物件」時,歧義大減,一句 `DELETE the large foreground tree` 就能收 — 比回原圖重跑省(但注意教訓 3 的畫質代價,且該輸出若已進重繪模式、細節被剝掉,不可回頭當另一件資產的母檔)。
7. **右下白/粉菱形「亮片」= Gemini ✨ 浮水印**(A1 同款)。prompt 移除不可靠,固定手動填色,入庫前必修。
8. **驗收雙標準:** 可見半邊嚴格比對原圖(枝形、裂紋位置);被遮重建側只驗風格一致 + 無幾何滲漏(偷長第二棵樹/憑空加苔蘚骸骨),本來就沒有 ground truth。另檢查 cast shadow 違規(prompt 有禁令仍偶發,色鍵會留髒邊 → 直接淘汰該張)。

## 產出(圖檔待補 — 檔名前綴 `a3-`)

| 建議檔名 | 內容 |
|---|---|
| `a3-source-annotated.png` | 原圖 + 4 紅箭頭標記 |
| `a3-main-tree-magenta.png` | 左主樹洋紅底(手動補殘幹後定案版) |
| `a3-small-tree-left-magenta.png` | 左場景小樹(緊裁法產出,手動填左緣殘幹) |
| `a3-small-tree-right-magenta.png` | 右場景小樹(緊裁法一次過) |
| `a3-fail-saliency.png` | 失敗鐵證:小樹拆件被主樹搶主角(重繪模式,苔蘚被剝) |
| `a3-crop-recipe.png` | 緊裁示範:遮擋物只留柱狀前景 |

## 學到的(一句話版)

**去背+補圖的成敗在「裁圖」不在「prompt」:先用裁切決定誰是主角,prompt 只負責鎖住它。** 殘留分流(孤立→手動、交疊→單目標 pass)+ 洋紅工作底 + 透明母檔收尾,即為可量產配方。
