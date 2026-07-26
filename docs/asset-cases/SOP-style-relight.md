# SOP — 風格母本重打光公式(兩段式,可跨風格複用)

> 把「拿一張參考圖,將任意場景算成它的打光方向跟氣氛」固化成固定流程。
> 首個驗證實例:[B8 萬聖夜魔森](B8-haunted-forest-style-dna.md)(2026-07-20 路線 A 一次過)。
> 管線依據:`ai-media-generator` [depth-relight-pipeline](../../.claude/skills/ai-media-generator/references/depth-relight-pipeline.md)。

**🔑 叫用方式(對 Claude 說):**
- `照打光公式,風格建檔:<貼母本圖>` → 跑 Phase 1
- `照打光公式,母本=B8,場景=<貼場景圖>` → 跑 Phase 2(已建檔風格)
- `照打光公式:<貼場景圖+母本圖>` → 未建檔風格,Phase 1 簡化版 + Phase 2 一次做

---

## 全貌

```
Phase 1(每個風格只做一次)          Phase 2(每個場景重複 N 次)
┌─────────────────────┐            ┌──────────────────────────────┐
│ 輸入:風格母本 ×1     │            │ 輸入:場景圖 ×1 + 母本 ×1      │
│ 產出:B* 風格案例建檔  │──供查──▶  │ 前處理 → 雙圖融合 prompt →     │
│ (DNA/母題/鎖句)      │            │ 生成 → 驗收 →(不穩)路線 B     │
└─────────────────────┘            └──────────────────────────────┘
```

- **Phase 1 的產物是「檔」不是「答案」** — 建一次,之後所有衍生圖/重打光共用。
- **Phase 2 生成時母本圖一定要掛上平台**(IMAGE 2);案例編號只是讓 Claude
  免重新分析、直接調鎖句寫 prompt。
- 母本只用一次、不出系列 → Phase 1 可省略建檔,Claude 臨場分析直接進 Phase 2。

---

## Phase 1 — 風格建檔(每個風格一次)

**輸入:** 風格母本 1 張(完成度高的目標風格圖)。

**產出:** `docs/asset-cases/B*-<slug>.md` 案例,必含四件套:

1. **五層風格 DNA** — 定位 / 構圖文法 / 色彩(主宰色+點綴色) / 光(主光向+
   發光體規則) / 筆觸材質
2. **母題清單**(編號列表)— 衍生圖抽換用;**同時是 Phase 2 的逐項禁抄清單**
3. **風格鎖句**(逐字英文)— STYLE / PALETTE LOCK / LIGHTING LOCK / COMPOSITION
   四段,無 artist name(Flux/NB 系才吃)
4. **平台路線表** — image-grounded 首選 + MJ `--sref` 參數 + 純文字平台備援

更新索引:`README.md` 案例表 + `CLAUDE.md`(如為常用風格)。

---

## Phase 2 — 場景重打光(每個場景重複)

**輸入:** 圖 1 = 要打光的場景(灰盒 render / 引擎拼裝 viewport / 白天圖皆可);
圖 2 = 風格母本。

### 2a. 前處理(必做,B1 踩坑防線)

1. 裁掉歧義雜訊(viewport 地板斷面/鏡像物/UI)— 會被模型「補完」
2. 裁到目標比例**滿版無 letterbox**;輸出 Dimensions = 輸入比例
3. 灰底/空區定調:要 AI 補(prompt 明示)或維持素色之後摳掉
4. Leonardo:Nano Banana 2、Prompt Enhance **None**、Style **None**

### 2b. 雙圖融合 prompt 模板(佔位符版 — 逐段換皮即用)

> B8 驗證過的逐字實例見 [B8 衍生應用 1](B8-haunted-forest-style-dna.md#衍生應用-1--引擎拼裝場景重打光成-b8-氣氛-路線-a-一次過2026-07-20)。

```text
Two reference images. IMAGE 1 = SOURCE SCENE: [一句話描述場景內容].
IMAGE 2 = LIGHTING & MOOD REFERENCE ONLY — take its lighting direction,
color grade and atmosphere; IGNORE its objects and composition: do NOT
copy its [母題清單逐項點名,如 moons, cloud faces, skulls...].

RELIGHT the source scene to match the reference mood: [時段/天氣],
single [色溫] key light from [光向,如 the top-center of the sky];
[場景主體] become [明暗定位,如 dark massed silhouettes] with a thin
[rim light 描述] on their lit edges; the ground falls into deep shadow,
desaturated to the [母本色盤名] of IMAGE 2; [大氣元素,如 low ground
fog]; [整體 grading,如 heavy low-key horror grading] — do not leave
any [原圖光殘留,如 daylight brightness].

GEOMETRY LOCK: every object keeps its EXACT position, size and
silhouette from IMAGE 1 — do not move, add, remove or reshape anything;
do not crop or zoom. This is a RELIGHTING pass, NOT a repaint: same
brushwork, same shapes — only lighting and color change.

[空區處理,二選一:
The flat gray backdrop is empty sky: fill it with [母本天空描述] in the
same [色盤] grade.
/ Keep the flat gray backdrop untouched — do not paint anything into it.]
```

**分工鐵律:relight pass 只管光和色。** 母題/物件另開 pass 或引擎放資產卡
(一 pass 一件事,B1 打地鼠教訓)。

### 2b-alt. 鎖的高度 — relight pass vs 體積 pass(⚠️ 重要分岔)

「重打光」和「變立體」是**兩種不同的 pass,鎖的高度不同**,選錯 = 效果不對還以為公式壞了。

| | relight pass(預設) | 體積 pass(form pass) |
|---|---|---|
| **要什麼** | 只換光向/色調/氣氛 | 平的資產卡長出 3D 體積(葉團球化、樹幹圓柱化) |
| **鎖什麼** | 輪廓+位置+**筆觸/內部明暗**全鎖 | **只鎖外輪廓+位置**,放開內部重畫 |
| **定性句** | `RELIGHTING pass, NOT a repaint — same brushwork, same shapes` | `FORM & LIGHTING pass — REPAINT the interior for volume, keep only the outer silhouette` |
| **對位** | ✅ 逐像素對位保留,可投影回 3D | ❌ 內部紋理會漂移,**不可投影對位** |
| **代價** | 平的資產卡重上色後**仍是平的**(葉子扁) | 換來體積,失去像素級對位 |

- **症狀對照**:relight 後「光色對了但樹葉/樹皮還是扁平、像原卡換色」→ 不是 relight 沒做好,
  是**你要的其實是體積 pass**,relight 的筆觸鎖本來就會保住原本的扁平內部。
- **體積 pass 要具體描述塑形**(光靠「make it 3D」無效):
  葉團 = `clustered rounded masses, moonlit top + deep shadowed underside, layered front-to-back with self-shadowing`;
  樹幹 = `rounded cylindrical volume, raised ridges catch rim light, grooves in shadow, AO where roots meet ground`。
- **要又立體又能投影對位 = 做不到**:AI 這邊二選一。對位需求 → 立體感回引擎端換有厚度的樹模型;
  看起來像參考圖 → 走體積 pass 放棄對位。
- ✅ 實測:B9 場景(2026-07-23)relight 後樹葉扁平 → 改體積 pass(silhouette-lock + 內部重畫)得到圖 2 級體積。
- ⚠️ **體積 pass 副作用:構圖漂移。** 鎖鬆到只剩外輪廓時,模型常連版面一起重排
  (樹數/位置變、小徑改道)。修法:**加一段 COMPOSITION LOCK(最高優先)**逐項點名
  樹數/位置/小徑形狀,並宣告「IMAGE 1 = 構圖權威,有疑慮聽 IMAGE 1 不聽 IMAGE 2」,
  把體積重畫收窄成「鎖定版面之內、每棵既有樹的內部」;平台有 image guidance/strength
  就**調高**(creativity 調低)。✅ 實測 2026-07-23 重出修正構圖漂移。
- ✅ **定案(2026-07-24):體積 pass 完整配方 = COMPOSITION LOCK(最高優先,逐項點名樹數/
  位置/小徑形狀 + 「IMAGE 1 = 構圖權威」)+ 體積重畫收窄到「鎖定版面之內每棵既有樹的內部」。**
  一次同時拿到:構圖對位 + 圖 2 級葉團/樹幹體積 + B9 明亮 mid-key 藍月光色。兩步法未啟用。
- ⚠️ **體積 pass 二次副作用:樹幹 bark 細節漂移。** 體積 pass 重畫「內部」= 連樹幹的
  紋理/凹槽/節疤也被重畫。**根因:樹幹本來就有細節+半立體,不需要體積 pass;扁的只有葉團。**
  修法 = **按部位拆 pass**(一 pass 一件事的部位版):
  - **樹幹/枝/根 = PRESERVE + relight only**:`keep the EXACT bark texture, grooves, knots
    from IMAGE 1, only relight — do NOT redraw or add bark detail`
  - **葉團 = volume pass**:只對 canopy 重畫體積
  - 平台 image guidance 調高 / creativity 調低,讓「保留」部位更貼原圖
  - **樹幹要零漂移(投影對位)** → 連 relight 都別讓 AI 碰:PS 收尾,取體積 pass 的葉團+天空,
    遮罩把原樹幹像素貼回 + 曲線對齊月光亮度(B1「確定性工具收尾、把骰子收走」)。
- ⚠️ **葉團「暗成一片、層次不足」的真因(2026-07-25 理想圖校正):不是不夠亮,是①太冷藍 ②沒葉片筆觸 ③團塊沒分隔。**
  一開始誤判為「衝青白高光 sparkle」→ 貼理想圖後校正。層次**不靠加亮**,靠三件事:
  - **暖苔綠/橄欖綠中間調**(NOT 冷青藍;只在最深陰影袋才轉 blue-green)
  - **葉片筆觸**:`many small individual leaf dabs and sprigs catching soft light on edges — NOT smooth blobs, NOT flat dark mass`
  - **團塊分隔 + 枝幹透出**:`distinct rounded clumps with soft self-shadow gaps; dark branches show through gaps in the foliage`
  - 光要**柔和低對比**(soft gentle moonlight, gradual falloff),不是硬邊 rim light
  - 📌 教訓:「黯淡」先查**色溫(太藍?)+ 筆觸(太平滑?)**,不要反射性加亮 → 加亮會變塑膠感。
- ⚠️ **全局強度自我打架(關鍵):** 高 image guidance 保住樹幹的同時,也把**原本扁暗的葉子凍住**;
  單張 img2img 一個全局強度無法「樹幹貼緊 + 葉子大幅重塑」兼得。解法:
  ① **遮罩/inpaint 只重畫樹冠**(樹幹地面天空遮住,葉團區高創意度重畫)= 最乾淨;
  ② 無 inpaint → **兩步法**:保樹幹版當底,再整張跑一次 creativity 調高/guidance 調低,只聚焦葉團值域。
  ✅ 實測 2026-07-25:B9 保樹幹版葉子偏暗 → 樹冠 inpaint 值域重畫救回層次。

### 2b-plus. 選配句庫(按需插入模板)

| 情境 | 逐字句 | 驗證 |
|---|---|---|
| **板邊黑線**(引擎資產卡接縫關不掉) | `The thin black seam lines along the top edges of the terrain are render artifacts: blend them into the adjacent terrain — do not interpret them as walls, shadows or new objects.` | ✅ 場景 2(2026-07-21):細線被融進地形。⚠️ **侷限:只治細線** — 大面積卡斷面仍會被重新解釋(場景 3 失敗),治本走輸入端消歧義 |
| **中央缺口授權**(構圖有大片空區在地平線上,想補遠景) | `fill the central gap beyond the path with a distant silhouetted treeline dissolving into fog, matching the misty midground of IMAGE 2.` | ✅ 場景 2:補繪風格一致;⚠️ 授權補繪區不可用於投影對位 |
| **地面紋理保讀**(前景地面佔畫面大、怕壓暗成死黑) | `darken them WITHOUT losing the grass and soil texture, which must stay readable inside the shadow` | ⚠️ 場景 3 中句子本身生效(暗部紋理可讀),但該次整體因幾何誤會判失敗 |
| **路面月光微光**(選配,要氛圍才加) | `a faint cool sheen of moonlight may touch the path` | ⚠️ 場景 3 被放大成濕地/水感;不要水感就改成 `the path stays dry — no water, no puddles, no reflections` |
| **地形定調**(卡斷面遮不掉時的補救,⏳ 待實測) | `TERRAIN CLARIFICATION: the raised areas at left and right are gentle grassy banks — their edges slope softly down into the field, covered with the same grass and moss. Do NOT draw exposed dirt cliffs, rock ledges, terraces or floating platforms; no sharp elevation cuts.` | ⏳ 補救性質 — 對歧義幾何下指令仍是邀請解釋(B1 #6),優先治本 |

### 實測記錄(場景累計)

| # | 場景 | 特徵/風險點 | 結果 |
|---|---|---|---|
| 1 | 引擎拼裝(標準視角) | 灰底+下緣鏡像雜訊 | ✅ 路線 A 一次過(詳見 [B8 衍生應用 1](B8-haunted-forest-style-dna.md)) |
| 2 | 引擎拼裝(中距離空地) | 雙灰區+板邊黑線+中央缺口 | ✅ 一次過:板邊句/缺口授權句生效 |
| 3 | 引擎拼裝(低相機大前景) | **資產卡大斷面**+大面積地面壓暗 | ❌ **幾何誤會**:卡斷面被補完成土崖/浮台,路面微光被放大成水感;光/色/紋理本身合格 → 治本 = 輸入端消歧義(見失敗分流) |

### 2b-fin. 合成收尾(確定性工具,建議的定案手法)

多版各有好部位時,**別硬追一次生成到完美 → PS 合成各版最佳部位**(B1「把骰子收走」)。
前提:各版都走過 COMPOSITION LOCK → 構圖對齊,遮罩可對位。

- **選底**:體積/氛圍最近理想的當底
- **貼部位**:把另一版的好部位(常見:樹幹 bark / 暖調葉子)遮罩貼上
- **統一調整(最易穿幫處)**:接合後對貼上的部位加色溫+亮度校正,對齊底圖光向
  (例:冷青葉 → 色彩平衡往綠/黃、降 cyan,拉回暖苔綠理想)
- **補雜訊**:水感倒影/多餘元素從乾版補回
- **收邊**:接縫羽化 2–4px
- ✅ 實測 2026-07-26:B9 體積版(葉冠夠但偏青+水感)+ 保樹幹版 → 合成定案。

### 2c. 驗收(5 條)

- ☐ 50% 透明度疊回圖 1:輪廓完全重合(要投影回 3D 為硬需求)
- ☐ 暗部是「壓暗」不是「塗黑」— 陰影裡紋理仍可讀
- ☐ 色盤與母本並排一致,無原圖光殘留
- ☐ 光向單一:rim light 方向與 key light 一致,無多光源矛盾
- ☐ 無母題滲漏、無擅自加入物件(空區授權補繪除外 — 需另行確認可用性)

### 2d. 失敗分流

| 症狀 | 處置 |
|---|---|
| 光向亂飄(連跑不穩) | 升級**路線 B**:NB 生 depth map → `depth-relight.html`(場景:Cutoff 0、Depth 低)拖光向 → 控制圖+圖1+圖2 三圖融合 |
| 母題滲漏(月亮/骷髏跑進來) | 禁抄清單逐項點名補齊(泛寫 ignore 無效) |
| 輪廓漂移/構圖被動 | 檢查前處理(letterbox?雜訊?)→ 再犯就加強 GEOMETRY LOCK 逐物件點名 |
| 變成重繪(筆觸/材質換掉) | 確認定性句在場;仍犯 → 降低期待幅度,分兩次小步走(先壓暗調色、再加大氣) |
| **relight 後樹葉/樹皮仍扁平(像原卡換色)** | 這是要**體積 pass 不是 relight**(見 2b-alt):放開筆觸鎖只鎖外輪廓,具體描述葉團球化+樹幹圓柱化。代價:失去像素對位,要對位改回引擎端換立體樹模型 |
| **卡斷面被補完成懸崖/浮台(幾何誤會)** | 模型必須解釋高低差 → 發明了崖面。**治本 = 輸入端消歧義**(場景 3 實證,文字治不了):① 引擎端 — 相機微調避開斷面/高地前緣用地面卡遮住/卡加裙邊;② PS 端 — 粗筆刷 30 秒把斷面塗成草坡漸變草稿(不用精細,只給解讀方向)→ 重跑。補救(輸入改不了才用)= 地形定調句(見句庫,⏳)。板邊句只治細線,對大斷面無效 |
| 路面/地面出現水感反光 | 「月光微光」句被放大 → 移除該句或改 `the path stays dry — no water, no puddles, no reflections` |

---

## 引用鏈(改公式前回源頭查最新版)

- 角色分派融合 + 深景深場景路線 → [depth-relight-pipeline.md](../../.claude/skills/ai-media-generator/references/depth-relight-pipeline.md)
- 定性句/畫框鎖/曝光鎖 + letterbox・歧義物件踩坑 → [B1 鎖句字典](B1-forest-bg-4k-detail.md#鎖句字典可複用)
- NB 平台簽名(自然段/多圖參考/無 --params) → skill `community-prompt-patterns.md`
- 首個完整實例(含實測結果與觀察) → [B8](B8-haunted-forest-style-dna.md)
