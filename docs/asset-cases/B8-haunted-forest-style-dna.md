# 實戰紀錄 — B8 萬聖夜魔森背景:風格 DNA 分析 + 衍生圖風格鎖句

> 一張「萬聖夜恐怖魔法森林」完成插畫的風格拆解,目的 = 之後用它產生**同風格衍生圖**
> (換場景/換母題,但色盤、光、筆觸、構圖文法不變)。
> 對應工作流:`ai-media-generator`(風格參考 / prompt 設計)。
> ⚠️ 與 B1 夜霧森林**不是同一系列** — 同屬深青綠夜森林色系,但本圖是敘事插畫
> (雙月、臉雲、紅眼、發光符文、骷髏),風格 DNA 獨立記錄。

**🔑 關鍵字:** `B8`、`魔森`、`萬聖森林`、`風格 DNA`、`風格鎖句`、
`haunted forest`、`衍生圖`、`style reference`、`--sref`

## 來源(索引)

- **素材:** 萬聖夜恐怖魔法森林完成插畫(16:9 橫幅,約 2K)— 源圖檔待入庫
  `images/b8-haunted-forest-source.png`(⚠️ 待補:從對話上傳存檔)
- **用途:** 當**風格母本(STYLE TRUTH)**,產生同風格衍生背景圖
- **日期:** 2026-07-19
- **狀態:** ✅ 風格分析定案;⏳ 衍生圖生產待開工

---

## 風格 DNA(五層拆解)

### 1. 定位

**西式手繪暗黑奇幻(dark fantasy)遊戲背景插畫,萬聖節 horror 主題。**
渲染介於半寫實與繪本式誇張之間:物件造型誇張化(慘叫臉雲、帶裂紋雙月),
但材質(樹皮/苔蘚/骨頭)畫到半寫實。柔邊數位筆刷,**非照片寫實、非 3D render**。
氣質是「戲劇化的恐怖舞台」而非紀實恐怖 — 略帶繪本感的 spooky。

### 2. 構圖文法(可套用到所有衍生圖)

| 元件 | 規則 |
|---|---|
| **舞台框景** | 左右兩株巨大扭曲枯樹當「舞台簾幕」,枝椏向中央伸展形成天然拱門 vignette(近對稱) |
| **導引線** | 中央泥土小徑從底邊引向畫面中心的黑暗深處(單點透視) |
| **三層深度** | 前景(高細節樹框+地面散件)→ 中景(霧中樹林剪影+點狀光)→ 遠景(天空焦點) |
| **亮度焦點** | 天空上中(月),全圖唯一大亮區;視線動線 = 月 → 雲 → 樹縫深處 → 小徑 |
| **地平線** | 下 1/3,天空占上半 |
| **parallax 天生分層** | 前/中/後景邊界清楚,可直接拆層 |

### 3. 色彩

- **主宰色:近單色調的低飽和深青綠**(desaturated dark teal-green),全圖壓灰壓暗
- **值域:** 整體 low-key;最亮 = 月盤(冷灰白),最暗 = 中景樹叢(近黑)
- **僅有的兩個點綴色(accent):**
  - **冷青 cyan** — 樹幹魔法裂紋/符文,局部自發光
  - **血紅 red** — 黑暗中成群獸眼,全圖唯一暖警示色
- 地面帶少量**濁黃褐枯草**(dead grass ochre)打破單色
- 無任何高飽和純色

### 4. 光

- 主光 = **頂部中央月光**,冷白;月周雲被照亮(volumetric 感)
- 前景樹幹只留**邊緣光(rim light)**,主體大量留黑
- 發光體(符文/紅眼)= **小半徑光暈、不照亮環境**的裝飾性 emissive
- 中景底部**地面霧**墊高明度、柔化剪影
- 恐怖片打光:低對比中間調 + 深黑陰影,暗部不提亮

### 5. 筆觸/材質

- 雲:大軟筆混色;樹皮/苔蘚/骨:中硬筆刷點畫,半寫實
- 細節密度梯度:前景高(苔點/菌/蛛網絲)→ 中景剪影化 → 遠景霧化(大氣透視)

---

## 母題清單(motif inventory — 衍生圖抽換用)

1. 扭曲禿枝老樹 + 垂掛松蘿  2. 樹幹層孔菌  3. 樹皮青色發光裂紋/符文
4. 枝角蛛網  5. 慘叫人臉雲  6. 雙月(大月帶裂紋+小月)  7. 黑暗中成群紅眼
8. 地面骷髏+散骨  9. 地面霧  10. 枯黃草叢  11. 中央泥徑

> ⚠️ **每張衍生圖挑 2–4 個母題即可** — 全上 = 多離散小物件注意力稀釋
> (B1 踩坑 #8 同理),而且張張全家福會讓套圖沒有節奏。

---

## 風格鎖句(逐字保存 — 衍生圖 prompt 的固定段落)

> 用法:下面整塊當 prompt 的「風格段」逐字沿用,前面只換「主題/構圖描述」。
> 全部用描述性詞、無 artist name — Flux / Nano Banana 系(訓練時刷掉畫家名)也吃。

```text
STYLE: hand-painted dark fantasy game background illustration, painterly
digital brushwork — soft blended clouds, semi-realistic bark, moss and
bone textures. NOT photorealistic, NOT a 3D render.

PALETTE LOCK: near-monochromatic desaturated dark teal-green night
palette; deep shadows stay near-black. Only two accent colors allowed —
cold cyan glow (magical cracks and runes) and small blood-red glows
(creature eyes in the dark); dull ochre dead grass is the only warm
note. All colors muted, no saturated hues.

LIGHTING LOCK: single cold moonlight key from the top of the frame,
backlit clouds, thin rim light on foreground silhouettes; heavy low-key
horror grading — do not brighten the shadows. Ground fog softens the
midground; glowing elements keep a SMALL glow radius and do not
illuminate their surroundings.

COMPOSITION: giant twisted bare trees as left/right stage curtains
forming a natural arch vignette; a central dirt path leads the eye into
the dark depth; three depth layers — detailed foreground frame,
silhouetted misty midground, glowing sky focal point; horizon in the
lower third, 16:9.
```

---

## 平台路線(衍生圖生產)

| 路線 | 做法 | 備註 |
|---|---|---|
| **首選:image-grounded(Nano Banana Pro / NB2)** | 本圖當 style reference 掛參考圖,文字只寫「新主題 + 構圖差異 + 上方 PALETTE/LIGHTING LOCK」 | NB 多圖參考是 superpower;與 B1「STYLE TRUTH 質感參考板」用法一致;Leonardo 設定照 B1 表(Enhance None / Style None / 比例=輸入) |
| **Midjourney** | `--sref <本圖>` + `--sw 200-400`,`--ar 16:9 --s 400-750`(fantasy 甜蜜點) | prompt 用 comma chips 改寫鎖句重點,不貼整段散文 |
| **純文字平台(Seedream / Flux)** | 直接用上方風格鎖句整段 + 主題句 | Seedream 重要詞放前;Flux 80–200 字自然段 OK |

**沿用 B1 鎖句字典:** 曝光鎖(暗部不提亮)、光暈半徑鎖(符文/紅眼不長大)、
深度鎖(霧線後不銳化)、畫框鎖(16:9 不 outpaint)— 逐字見
[B1 紀錄](B1-forest-bg-4k-detail.md#鎖句字典可複用)。

---

## 類型分流警告(若要放大本圖)

本圖 = **手繪筆觸 + 多離散小物件**(骷髏/菌/蛛網/紅眼/臉雲)→ 按 B1/B3 教訓,
**禁跑 NB2 全圖材質保真 pass**(會抹筆觸、重擲小物件),要 4K 只走
**純保真放大分支**(Topaz / Real-ESRGAN / UU 最低 creativity)。
衍生圖「重新生成」不受此限 — 那是生新圖,不是保真放大。

---

## 待辦

- ☐ 源圖入庫 `images/b8-haunted-forest-source.png`
- ☐ 首張衍生圖試產(建議先做「同構圖換母題」最小變異,驗風格鎖句有效性)
- ☐ 驗收:衍生圖與母本並排 — 色盤/明度分佈/筆觸密度一致,僅內容不同
