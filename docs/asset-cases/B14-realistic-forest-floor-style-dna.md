# 實戰紀錄 — B14 半寫實暗黑森林地面場景:風格 DNA 分析 + 衍生圖風格鎖句

> 一張「半寫實暗黑森林地面」場景圖的風格拆解,目的 = 之後用它產生**同風格衍生圖**。
> 對應工作流:`ai-media-generator` + [SOP 打光公式](SOP-style-relight.md) Phase 1。
> ⚠️ 與 B10(暗黑手繪插畫)、B11(明亮動漫)**皆不同** — 本圖是**半寫實 3D-render 質感、
> 地面主導**的環境圖(近 UE5 / Megascans 掃描感),風格 DNA 獨立記錄。

**🔑 關鍵字:** `B14`、`寫實森林地面`、`半寫實暗黑森林`、`UE5 森林地面`、
`苔蘚地面場景`、`god rays 森林`、`風格 DNA`、`風格鎖句`、`--sref`

## 來源(索引)

- **素材:** 半寫實暗黑森林地面場景圖(16:9 橫幅,約 2K)— 源圖檔待入庫
  `images/b14-forest-floor-source.png`(⚠️ 待補:從對話上傳存檔)
- **用途:** 當**風格母本(STYLE TRUTH)**,產生同風格衍生背景圖 + 場景重打光
- **日期:** 2026-07-28
- **狀態:** ✅ 風格分析定案;⏳ 衍生圖生產待開工

---

## 風格 DNA(五層拆解)

### 1. 定位

**半寫實 3D-render 質感的暗黑奇幻森林地面環境圖(UE5 / Megascans 掃描級)。**
氣質**陰森、寫實、沉靜**,無卡通/繪本誇張。渲染 = 高保真 PBR 材質(苔蘚/泥土/落葉/樹皮
帶苔),接觸陰影(AO)扎實、體積光(god rays)柔和。**非手繪插畫(≠B10)、非動漫 cel(≠B11)、
非照片(仍有輕微繪畫理想化)。** 最接近 repo 內 **B1 夜霧森林地面**的寫實血緣,但 B14 是
**完整場景構圖**(含 god rays + 立石地標),B1 偏純地面材質板。

### 2. 構圖文法(可套用到所有衍生圖)

| 元件 | 規則 |
|---|---|
| **地面主導** | 低相機、前景苔蘚地面佔畫面**下 2/3**;地面是主角(材質細節密集) |
| **樹牆背景** | 中景一排帶苔板根(buttress root)巨樹幹橫成「樹牆」,底部消失在地平線 |
| **地標** | 左側一根帶苔立石(rune/menhir stone)當視覺錨;角落散置碎石板+小植叢 |
| **體積光** | 右上方 god rays / 光軸(Tyndall)斜穿樹冠,柔和不刺眼 |
| **中央亮塘** | 地面中央有一塊受光較亮的苔地(視線落點),四周漸暗(自然 vignette) |
| **地平線** | 上 1/3(天空/樹冠只留窄帶),天空不是重點 |
| **深度** | 前景高細節地面 → 中景樹牆剪影 → 遠景藍霧 |

### 3. 色彩

- **主宰色:低飽和大地色系** — 苔蘚**黃綠**(ground moss,全圖主要色感)+ 泥土**棕灰**
- **陰影/背景:** 冷**藍灰**(遠景霧 + 暗部),與中景暖苔綠成冷暖對比
- **樹皮:** 深棕灰帶苔綠斑
- **唯一暖點綴:** 右下角一小叢**暗紅/酒紅**植物(maroon accent,極小面積)
- 整體**低飽和、壓抑、潮濕感**;無高飽和純色、無發光體

### 4. 光

- **無硬 key** — 陰天/夜的**柔和環境光**打底
- 主氛圍 = 右上方**體積光軸(god rays)**斜穿樹冠,製造空氣感與方向暗示
- 中央苔地一塊**柔和受光亮塘**,邊緣自然壓暗(vignette 聚焦)
- **扎實 AO / 接觸陰影**:板根與立石根部、石塊底都有紮實暗接觸影 → 物件「坐」在地上有重量
- 潮濕反光:深色濕泥處有微弱漫反射;整體 low-key 中間調

### 5. 筆觸/材質

- **高保真 PBR 寫實材質**:苔蘚顆粒感、泥土粗糙變化、散落**落葉/枯枝/小石**碎屑層、樹皮苔斑
- 樹幹/立石:寫實凹凸 + 苔覆分佈,半立體扎實
- 細節密度梯度:前景地面**極高**(掃描級碎屑)→ 中景樹牆中 → 遠景霧化柔焦
- 📌 **與 B10/B11 的關鍵材質分界:B14 是有機微紋理寫實(草/苔/泥/落葉),
  放大走 NB2 材質保真 pass 有增益**(同 B1 類型分流);B10/B11 是筆觸/cel,放大只能純保真放大器。

---

## 母題清單(motif inventory — 衍生圖抽換用)

1. 帶苔板根(buttress root)巨樹幹  2. 帶苔立石 / rune 石(地標)  3. 苔蘚地面(黃綠塊)
4. 落葉/枯枝/碎石屑層  5. 右上 god rays 光軸  6. 中央受光亮塘  7. 散置苔石板
8. 遠景藍霧樹牆剪影  9. 暗紅小植叢(暖點綴)  10. 潮濕深泥反光

> ⚠️ **每張衍生圖挑 2–4 個母題即可**(B1 踩坑 #8:多離散小物件注意力稀釋)。
> god rays + 中央亮塘是本風格的「氣氛招牌」,想保留寫實森林感至少留這兩者其一。

---

## 風格鎖句(逐字保存 — 衍生圖 prompt 的固定段落)

> 用法:整塊當 prompt 的「風格段」逐字沿用,前面只換主題/構圖描述。
> 全描述性詞、無 artist name(Flux/NB 系才吃)。

```text
STYLE: semi-realistic rendered dark-fantasy forest-floor game
background, Unreal Engine 5 / Quixel Megascans scan fidelity — high-
detail PBR ground with moss, soil, scattered leaf litter and twigs;
mossy bark and stone. Painterly-realistic and atmospheric, NOT flat
illustration, NOT anime cel, NOT a photo.

PALETTE LOCK: muted desaturated earthy palette — mossy yellow-green
ground moss is the main color, brown-grey soil, cool blue-grey shadows
and distant haze; dark mossy bark. Low saturation, damp and moody. The
ONLY warm accent is a tiny maroon-red plant; no glowing elements, no
saturated hues.

LIGHTING LOCK: soft overcast/night ambient with NO hard key; gentle
volumetric god rays (Tyndall light shafts) slanting from the upper-
right through the canopy; a soft pool of light on the central mossy
ground with the edges falling into shadow (natural vignette); firm
ambient-occlusion contact shadows under roots, stones and debris so
everything sits grounded and heavy; low-key mid-tones, damp sheen on
dark wet soil.

COMPOSITION: low ground-level camera, the detailed mossy foreground
fills the lower two-thirds; large mossy buttress-root tree trunks form
a treeline wall across the mid-horizon; a standing mossy rune stone as
a left-side landmark; scattered mossy rocks and small plants anchoring
the corners; blue atmospheric haze behind the treeline; horizon in the
upper third, 16:9.
```

---

## 平台路線(衍生圖生產)

| 路線 | 做法 | 備註 |
|---|---|---|
| **首選:image-grounded(Nano Banana Pro / NB2)** | 本圖當 style reference 掛參考圖,文字只寫「新主題 + 構圖差異 + 上方 PALETTE/LIGHTING LOCK」 | Leonardo 設定照 B1 表(Enhance None / Style None / 比例=輸入) |
| **Midjourney** | `--sref <本圖>` + `--sw 200-400`,`--ar 16:9 --s 200-300 --style raw`(寫實 → 低 stylize) | 寫實風用 `--style raw`,別給 fantasy 高 stylize |
| **純文字平台(Seedream / Flux)** | 直接用上方風格鎖句整段 + 主題句;Flux 加寫實攝影詞(grain/AO/f-stop) | Flux 對寫實 PBR 質感支援好 |

**沿用 B1 鎖句字典:** 曝光鎖(暗部不提亮)、深度鎖(藍霧後不銳化)、
尺度鎖(紋理不畫大一號)、畫框鎖(16:9 不 outpaint)— 逐字見
[B1 紀錄](B1-forest-bg-4k-detail.md#鎖句字典可複用)。

---

## 用本圖做場景重打光(SOP Phase 2)

本圖可當 **LIGHTING & MOOD REFERENCE(IMAGE 2)** 給灰盒/引擎場景重打光成「半寫實暗黑森林氛圍」。
照 [SOP 打光公式](SOP-style-relight.md) Phase 2 走,relight 段定調換成 B14 方向:

- 質感:`semi-realistic PBR, UE5/Megascans fidelity`(**不要**寫 illustration / anime)
- 光:`soft overcast ambient + volumetric god rays from upper-right, no hard key`
- 暗部:`low-key mid-tones, firm AO contact shadows`(壓抑但紋理可讀)
- 色盤:`muted earthy — mossy yellow-green + brown-grey + cool blue-grey haze`
- 母題授權:想要森林感 → 補「god rays + 中央受光亮塘 + 帶苔立石地標」

> 🔑 **B10 / B11 / B14 三風格速記:** 同是暗森林,但
> **B10 = 暗黑手繪插畫(horror,壓灰塗黑)**、**B11 = 明亮動漫(mid-key 藍月,飽和)**、
> **B14 = 半寫實 render(UE5 質感,大地色 god rays)**。選錯母本 = 質感與氣氛全跑掉。
> 材質分流:**B14 走 NB2 材質保真放大**(有機微紋理);B10/B11 只能純保真放大器。

---

## 衍生應用 1 — 引擎拼裝場景重打光成 B14 氣氛(⏳ 待實測)

> 輸入:圖1 = 引擎森林場景(樹牆 + 苔地 + 前景土路,較亮平光);圖2 = B14 母本。
> 目標:暗黑半寫實 + god rays + 大地色氛圍。前處理:裁雜訊 / 滿版 / NB2·Enhance None·Style None。

```text
Two reference images. IMAGE 1 = SOURCE SCENE: a semi-realistic forest —
a row of mossy buttress-root tree trunks across the mid-horizon, a green
moss ground, and a dirt path in the foreground. IMAGE 2 = LIGHTING &
MOOD REFERENCE ONLY — take its lighting direction, color grade and
atmosphere; IGNORE its objects and layout: do NOT copy its rune stone,
specific trees or plants.

RELIGHT the source scene to match the reference mood: a dark, moody,
low-key semi-realistic forest at dusk; soft overcast ambient with NO
hard key light; gentle volumetric god rays (Tyndall light shafts)
slanting from the upper-right through the canopy; a soft pool of light
on the central moss ground with the edges falling into shadow (natural
vignette); firm ambient-occlusion contact shadows under the tree roots
and along the ground so everything sits grounded; damp sheen on the
darker soil. Desaturate to the muted earthy palette of IMAGE 2 — mossy
yellow-green ground, brown-grey soil and bark, cool blue-grey haze
behind the treeline; low-key mid-tones, do NOT leave any bright daylight
look, but keep the ground and bark texture readable in shadow.

GEOMETRY LOCK: every tree, root, the moss ground and the foreground path
keep their EXACT position, size and silhouette from IMAGE 1 — do not
move, add, remove or reshape anything; do not crop or zoom. This is a
RELIGHTING pass, NOT a repaint: same shapes and materials — only
lighting and color change. Keep the semi-realistic PBR / UE5 render
look; do NOT turn it into flat illustration or anime.

Add cool blue atmospheric haze between the distant trunks behind the
treeline; deepen the top canopy into shadow.
```

- **B14 relight 三要點**(對比 B10/B11):① 質感鎖 `PBR/UE5, NOT illustration/anime`
  ② 光靈魂 = god rays + 中央亮塘 + vignette ③ 扎實 AO 接觸陰影(物件坐地有重量)
- 驗收(照 SOP 5 條)+ 特別盯:壓暗後**苔地/樹皮紋理可讀**(別塗死黑)、god rays 方向單一。
- ⚠️ **實測 2026-07-28 ①:氣氛對但構圖漂移**(樹位置/樹牆重排)。修法(照 SOP 2b-alt):
  **COMPOSITION LOCK 移最前、逐項點名樹數/位置/樹牆/苔地/土路 + 「IMAGE 1=構圖權威,有疑慮聽 IMAGE 1」**,
  平台 image guidance 調高 / creativity 調低。根因:IMAGE 2(母本)版面滲進來帶跑構圖。
- ⚠️ **實測 2026-07-28 ②:構圖鎖住了但氣氛沒吃進去**(偏亮偏綠,丟 B14 暗黑大地色)。
  根因 = **兩鎖互打**:高 guidance 鎖構圖的同時把原圖亮固有光凍住,IMAGE 2 暗調套不進(同 SOP regrade 天花板)。
  **正解:構圖既對就凍住,氣氛交給 PS**(壓暗 Curves → 降飽和 → 陰影推冷藍灰 → vignette 保中央亮塘 →
  Screen 層加 god rays)。生成硬追兩鎖=打架;調色/氣氛歸 PS(全流程結論)。或兩步法:此版當底、
  第二 pass 降 guidance 只換氣氛(構圖可能微鬆)。

## 待辦

- ☐ 源圖入庫 `images/b14-forest-floor-source.png`;引擎場景 `images/b14-engine-scene-source.png`
- ☐ 衍生應用 1 實測(路線 A;不穩再走 SOP 路線 B depth 控制圖)
- ☐ 首張「同構圖換母題」衍生圖試產,驗風格鎖句有效性
- ☐(如需)用本圖當 IMAGE 2 跑一次場景重打光,驗證半寫實定調
- ☐ 驗收:衍生圖與母本並排 — 色盤/明度分佈/材質保真度一致,僅內容不同
