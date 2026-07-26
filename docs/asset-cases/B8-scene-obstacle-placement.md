# 實戰紀錄 — B8 場景就地生成障礙物(紅圈定位 → 量體物件置放)

> 在**已定案的背景成品圖**上,就地生成量體大的擋路障礙物(石堆/倒木堆),
> 吃場景既有的主題、光線、材質。
> 對應工作流:`ai-media-generator`(nano-banana「物件合成進場景」實測模板);
> 前置知識:[B1](B1-forest-bg-4k-detail.md)(鎖句字典)、[B2](B2-greybox-module-pipeline.md)(增強 vs 生成)。

**🔑 關鍵字(日後對 Claude 說這些詞即可叫出本紀錄):**
`B8`、`B8 紀錄`、`照 B8 配方`、`障礙物`、`擋路`、`石堆`、`倒木堆`、
`物件置放`、`OBJECT-PLACEMENT pass`、`紅圈定位`、`placement map`、
`塗鴉定位`、`就地生成物件`、`量體物件`、`場景加物件`

## 來源(索引)

- **素材:**
  - 圖 1(BASE)= 夜森林月下背景成品(16:9 滿版,含枯樹群/土路/月亮)
  - 圖 2(PLACEMENT MAP)= 同一張圖用**紅筆圈出三個要放障礙物的區域**
- **平台:** Leonardo.ai AI Creation / **Nano Banana 2**
- **需求:** 依畫面主題 + 周圍光線 + 材質,在紅圈處生成量體大的障礙物 —
  左:石堆 / 中:倒木堆 / 右:石堆
- **日期:** 2026-07-26
- **結果:** ✅ 一次 pass 成功 — 三物件量體/風格/接地/打光全數合格,紅圈筆跡零殘留

---

## 最終定案管線

```
圖1 背景成品(滿版 16:9)+ 圖2 同圖紅圈標註(placement map)
  → NB2「OBJECT-PLACEMENT pass」(下方逐字 prompt)
  → Photoshop 遮罩合成:只取三塊障礙物 + 接觸陰影,貼回乾淨原圖
  → 色調微調(石堆壓暗偏青、倒木降飽和、遠物疊霧)
  → 進引擎投影驗收
```

> ⚠️ **遮罩合成不是選配。** NB2 是全圖重繪,樹輪廓會微漂移 —
> 投影管線(見 [B6](B6-three-camera-pipeline.md)/[B7](B7-unreal-camera-port.md))對輪廓零容忍,
> 必須只摳物件貼回原圖。

### 平台設定 — Leonardo.ai AI Creation

| 設定 | 值 | 備註 |
|---|---|---|
| Model | **Nano Banana 2** | 圖 1 在前(BASE)、圖 2 在後(placement map) |
| Image Dimensions | **16:9(4096×2304,Custom)** | 比例必須 = 輸入圖(B1 踩坑 #5) |
| Prompt Enhance | **None** | 會改寫 LOCKS 鎖句 |
| Style | **None** | preset 疊色調,與曝光鎖/色盤鎖衝突 |
| Number of generations | 1(開 4 挑 1) | |
| Private Mode | On | |

---

## 逐字 prompt(✅ 驗證成功,實際使用版)

```text
Reference image 1 is the BASE — a finished hand-painted night-forest
game background. Its camera, framing, trees, dirt path, ground
texture, sky and moon are all correct and final.

Reference image 2 is the SAME scene with three red circles. Use it
ONLY as a placement map for WHERE and HOW LARGE the new obstacles
must be — the red strokes themselves must NOT appear in the output.

TASK — OBJECT-PLACEMENT pass: add exactly THREE large impassable
obstacles, painted in the same hand-painted game-art style as the
scene:

1. LEFT circle area: a massive pile of weathered gray-brown
boulders, stacked naturally, edges softened by patches of moss.
2. CENTER circle area: a pile of fallen tree logs — broken trunks
and thick branches, bark matching the scene's gnarled trees —
lying across the far end of the dirt path and blocking it. It is
farther away, so it is smaller in the frame and slightly softer,
following the scene's aerial perspective.
3. RIGHT circle area: a massive pile of weathered boulders, similar
material to the left pile but stacked differently — not a mirror
copy.

INTEGRATION: each obstacle sits firmly on the ground with a natural
contact line — moss and low grass creep up its base. Match the
obstacle materials to the surrounding scene, and light them with the
scene's existing moon softlit ambient lighting, reflections and
diffuse bounce. Do not invent a new light source, no long cast
shadows.

LOCKS: keep the exact original 16:9 canvas, framing and camera — do
NOT crop, zoom, extend or outpaint. Every tree, the path, the ground,
the sky, clouds and moon stay exactly as they are — pixel-identical
outside the three obstacle areas. Do not brighten the shadows; keep
the muted dark teal-green night palette exactly. No other new
objects anywhere: no scattered rocks, no debris, no mushrooms, no
animals, no fireflies.
```

### 句子解剖(為什麼這樣寫)

| 段 | 作用 |
|---|---|
| `Reference image 1 is the BASE ... correct and final` | 角色標籤:定調圖 1 是既成事實,不是待改稿 |
| `Reference image 2 ... ONLY as a placement map ... red strokes must NOT appear` | **紅圈定位法**:用塗鴉圖傳位置+尺寸,免寫座標;明文排除筆跡 |
| `TASK — OBJECT-PLACEMENT pass` | **定性句**。這次是「放東西」,所以**不能**用 B1 的 TEXTURE-FIDELITY 定性 |
| `add exactly THREE` | 數量鎖,防模型多撒 |
| `not a mirror copy` | 防左右石堆偷懶鏡像(同 B1 踩坑 #4 對稱 artifact) |
| `farther away, so it is smaller and slightly softer, following the scene's aerial perspective` | **空氣透視鎖**:遠處倒木不畫成前景等大等銳,保住深度結構 |
| `sits firmly ... natural contact line — moss and low grass creep up its base` | **接地句**,治「貼紙感」 |
| `Match the ... surrounding scene, and light them with the scene's existing ... lighting, reflections and diffuse bounce` | **整包光影對齊**(skill 實測心法):不逐條指定影子方向,交給模型算 |
| `Do not invent a new light source, no long cast shadows` | 保住模組/背景的光照規格(B2 的旋轉安全思路) |
| `LOCKS: ... pixel-identical outside the three obstacle areas` | 畫框鎖 + 曝光鎖 + 色盤鎖(B1 鎖句字典) |
| `No other new objects anywhere: no scattered rocks, debris, mushrooms...` | 禁止清單,防 B1 踩坑 #3「順手撒一地」 |

### 尺寸微調 pass(迭代用 — 單圖,✅ 治震盪)

初版物件量體不合意時**不要用相對詞**(`大一點` / `矮一點` / `多一點`),
改用「四道尺寸鎖」把模糊需求量化:

```text
This image is the BASE and is nearly final. Make ONE change only:
enlarge the crossed fallen-log pile in the center.

SIZE TARGET — a small step up, not a dramatic change:
- Grow it by roughly 20-25% in overall size.
- Its top must stay clearly BELOW the dark tree canopy line behind
  it, and must NEVER overlap or touch the moon.
- Its height should end up slightly taller than the left boulder
  pile, not double it.
- Grow mainly in volume and height; keep its left and right ends
  roughly where they are — do not let it spread wider across the
  frame or merge into the tree line.
- Keep the same X-shaped crossed-log arrangement and the same
  number of logs, just larger and thicker. It still blocks the far
  end of the dirt path, and its base stays grounded at the exact
  same spot on the ground.

EVERYTHING ELSE IS LOCKED: the left and right boulder piles keep
their exact current size, height, position and shape. The trees,
sky, clouds, moon, dirt path, grass and ground stay pixel-identical.
Keep the exact original 16:9 canvas, framing and camera — do NOT
crop, zoom, extend or outpaint. Do not brighten the shadows; keep
the muted dark teal-green night palette. No new objects.
```

| 鎖 | 句子 | 防的事 |
|---|---|---|
| **百分比鎖** | `roughly 20-25% in overall size` | 把「一點點」量化 |
| **上界鎖** | `stay clearly BELOW the tree canopy line, NEVER overlap the moon` | 防爆成蓋住月亮的巨型堆 |
| **比較錨** | `slightly taller than the left boulder pile, not double it` | 用畫面內既有元素當量尺 |
| **寬度鎖** | `keep its left/right ends roughly where they are — do not spread wider or merge into the tree line` | 防橫向蔓延吃掉整個中景 |
| **已滿意元素凍結** | `the left and right boulder piles keep their exact current size...` | 沒點名的元素每輪都會跟著漂 |

---

## 尺寸迭代實錄(震盪過程 — 本案最大教訓)

| 輪 | 指令 | 結果 |
|---|---|---|
| v1 | (初版 OBJECT-PLACEMENT prompt) | ✅ 三物件到位;倒木堆偏小 |
| v2 | `中央倒木變多、左右落石堆矮一點` | ⚠️ 石堆降高**成功**;倒木**橫向蔓延**成橫貫中景的大片木牆,融進樹線 |
| v3 | `中央的倒木堆大一點` | ❌ **爆炸** — 長成蓋住月亮的巨型金字塔,壓垮整張構圖 |
| v4 | `中央的倒木比現在大一點點` | ❌ **過度回縮** — 縮回比 v1 略大而已,又太小 |
| v5 | 尺寸錨定 pass(百分比+上界+比較錨+寬度鎖) | (待跑) |

**觀察:** 相對尺寸詞(`大一點`/`一點點`)在 NB2 沒有穩定映射 —
同一個詞可以是 +20% 也可以是 +300%,且每輪從頭重擲,不會參考上一輪的幅度。
**「多一點」尤其危險:模型傾向往「橫向鋪開」解讀,而非「加高加厚」。**

---

## 產出對照

### 輸入 — 背景成品(BASE)
![b8 base](images/b8-base.png)

### 輸入 — 紅圈 placement map
![b8 placement map](images/b8-placement-map.png)

### 輸出 v1 — 三障礙物一次 pass(✅ 物件本體全數合格)
![b8 obstacles generated](images/b8-obstacles-generated.png)

### 輸出 v2 — 「倒木變多 + 石堆矮一點」(石堆 ✅ / 倒木橫向蔓延 ⚠️)
![b8 iter v2 sprawl](images/b8-iter-v2-sprawl.png)

### 輸出 v3 — 「倒木堆大一點」(❌ 爆炸成蓋住月亮的巨型金字塔)
![b8 iter v3 oversized](images/b8-iter-v3-oversized.png)

### 輸出 v4 — 「比現在大一點點」(❌ 過度回縮)
![b8 iter v4 undersized](images/b8-iter-v4-undersized.png)

> 📌 圖檔待補:上述 v2/v3/v4 與 base/placement map 請從 Leonardo 另存後
> 放入 `images/`,檔名依上方引用名稱。

---

## 驗收結果

| 項目 | 結果 |
|---|---|
| 三物件位置/量體對紅圈 | ✅ |
| 手繪風格一致(筆觸/苔蘚/樹皮) | ✅ 樹皮質感有對到場景枯樹 |
| 紅圈筆跡殘留 | ✅ 零殘留 |
| 接地(接觸陰影 + 草叢咬底緣) | ✅ 非貼紙感 |
| 左右石堆非鏡像 | ✅ 堆疊方式明顯不同 |
| 無新增光源 / 無長投影 | ✅ |
| 三區以外 pixel-identical | ❌ **全圖重繪如預期** — 樹群輪廓微漂移、前景草地變亮變鮮、原本橫向交叉路左段被草地蓋掉 |
| 遠處倒木空氣透視 | ⚠️ 有變小,但銳利度仍接近前景,需 PS 疊霧補 |

**結論:物件生成合格,幾何保真不合格(結構性,非 prompt 問題)→ 必走遮罩合成。**

---

## 踩坑紀錄

| # | 現象 | 根因 | 解法 |
|---|---|---|---|
| 1 | 三物件以外的區域全被重繪(樹輪廓漂移、草地提亮、交叉路左段消失) | `pixel-identical outside` 這類鎖句**擋不住 NB2 的全圖重繪本質**(B1 結論再度成立:NB2 無真正區域修復) | 鎖句只降低漂移幅度,**保真靠 PS 遮罩合成**,不靠 prompt |
| 2 | 石堆亮部偏亮灰,在暗夜場景裡略搶眼 | 模型對「boulder」的先驗打光比場景整體亮 | PS 曲線壓暗 + 色相微偏青;或 prompt 加曝光鎖強化句 |
| 3 | 遠處倒木堆銳利度接近前景 | 空氣透視鎖只寫了 `slightly softer`,權重不足 | PS 疊 5–10% 青綠平塗;或把該句改成明確比較級 |
| 4 | 樹皮偏暖橘褐,飽和度略高於場景 | 同 #2,材質先驗色偏暖 | PS 降飽和/偏冷 |
| 5 | `大一點` → 倒木堆爆炸成蓋住月亮的巨型金字塔;`一點點` → 又縮回太小 | **相對尺寸詞在 NB2 無穩定映射**,且每輪從頭重擲、不參考上一輪幅度 → 尺寸震盪 | **尺寸錨定法**:百分比 + 上界鎖(不超過樹冠線/不碰月亮)+ 畫面內比較錨(略高於左石堆)+ 寬度鎖,四鎖齊下 |
| 6 | `倒木變多` → 長成橫貫中景的木牆,融進樹線 | 「多」被解讀成**橫向鋪開**而非加高加厚;且未鎖寬度 | 想要體積就寫 `grow in volume and height`,同時鎖 `keep its left and right ends roughly where they are — do not spread wider` |
| 7 | 每輪只講中央倒木,左右石堆卻跟著漂 | **沒點名的元素 = 自由重擲** — 已滿意的元素不凍結就會變 | 每輪 prompt 明文列出**已定案元素凍結句**:`the left and right boulder piles keep their exact current size, height, position and shape` |

---

## 意外收穫(可複用)

**全圖重繪把舊瑕疵順手修掉了。** 本圖前一輪待修的地面「投影拖影糊帶」
(草地被拉出方向性模糊),在這次 OBJECT-PLACEMENT pass 中被一併重生成為清晰材質。
遮罩合成時可以把那幾塊糊帶區域**一併從新圖取用**(低頻地面材質,投影容錯高)—
等於一次 pass 解決「加障礙物」+「修糊帶」兩個需求,省掉一輪材質修復 pass。

📌 **推論:** 當一張圖同時有「要加物件」和「要修低頻材質」兩種需求時,
先跑物件 pass、再從結果中挑收穫,比分兩次跑省一輪。**高頻/幾何區域(樹、路型)
仍只能用原圖。**

---

## 技法字典(新增)

| 技法 | 用途 | 要點 |
|---|---|---|
| **紅圈定位法(placement map)** | 傳位置+尺寸,免寫座標 | 同一張圖複製一份畫紅圈當第 2 參考;prompt 必寫 `ONLY as a placement map` + `red strokes must NOT appear`。比文字描述方位穩,且尺寸資訊一併傳達 |
| **OBJECT-PLACEMENT 定性句** | 與 TEXTURE-FIDELITY 對立的另一種定性 | 要放東西就明說是 object pass,並用 `exactly N` 鎖數量 + 禁止清單封住「順手撒一地」 |
| **整包光影對齊** | 物件融入場景 | `Match the materials to the surrounding scene, and light them with the scene's existing lighting, reflections and diffuse bounce` — **不要**逐條寫影子方向/rim light 角度,會跟畫面打架 |
| **空氣透視鎖** | 遠處新物件不搶前景 | `It is farther away, so it is smaller in the frame and slightly softer, following the scene's aerial perspective` |
| **反鏡像鎖** | 成對物件不對稱 | `similar material to the left pile but stacked differently — not a mirror copy` |
| **物件收穫式遮罩** | 一次 pass 多重收穫 | 遮罩時除了目標物件,把新圖中**順手修好的低頻材質區**也一併取用;高頻/幾何區維持原圖 |
| **尺寸錨定法** | 治尺寸迭代震盪 | 禁用 `大一點/矮一點/多一點`。改四鎖齊下:①**百分比**(`roughly 20-25%`)②**上界鎖**(`stay below the canopy line, never overlap the moon`)③**畫面內比較錨**(`slightly taller than the left boulder pile, not double it`)④**寬度鎖**(`grow in volume and height, keep left/right ends where they are`)。核心 = 用**畫面既有元素當量尺**,模型才有可執行的參照 |
| **已定案元素凍結句** | 防已滿意的部分跟著漂 | 每輪 prompt 明文列出不准動的物件與其屬性(`keep their exact current size, height, position and shape`)。**沒點名 = 自由重擲** |

---

## 驗收 checklist

- ☐ 疊回原圖 50% 透明度:三塊區域以外完全重合(遮罩後)
- ☐ 紅圈筆跡零殘留
- ☐ 物件接地:接觸陰影 + 苔草爬底緣,非貼紙感
- ☐ 無新增光源、無長投影
- ☐ 暗部未提亮;天空/月亮/雲未動
- ☐ 遠處物件比前景軟、暗(空氣透視)
- ☐ 成對物件非鏡像
- ☐ 除指定物件外無越界物件(碎石/枯枝/蘑菇/螢火蟲)
- ☐ 引擎投影最終驗收

---

## 學到的(可複用結論)

- ✅ **塗鴉定位 > 文字方位。** 在同一張圖上畫紅圈當第 2 參考,一次把「哪裡 + 多大」
  兩個資訊傳給模型,比 `in the left foreground between the tree cluster and the path`
  這類文字描述穩得多。**代價只是一句「筆跡不得出現」**,實測零殘留。
- ✅ **定性句要對應任務型態,不能照抄。** B1 的 `TEXTURE-FIDELITY pass, NOT an object pass`
  在這裡是**反向**的 — 本任務就是 object pass。定性句是給模型正確心智模型,
  抄錯型態比不寫更糟。
- ✅ **光影「整包交出去」勝過逐條指定。** 這是 skill 裡 nano-banana 物件合成的核心心法,
  在本案再度驗證:只寫「向周圍對齊」,模型用世界知識算出的融入度,
  高於人工指定影子方向(且不會跟畫面既有光源打架)。
- ✅ **`pixel-identical` 是願望不是保證。** NB2 的全圖重繪本質讓任何「其餘不動」鎖句
  都只能降低幅度。**幾何保真的唯一可靠手段是遮罩合成** —
  再次印證 B1/B2 的「AI 大面積、確定性工具收尾」。
- ✅ **一次 pass 可以有複數收穫。** 全圖重繪的副作用(其他區域被重畫)在低頻材質區
  是**好事** — 挑著收即可。判斷準則:低頻(草地/土壤/苔蘚)可收,
  高頻/幾何(樹輪廓/路型/建物)必棄。
- ✅ **相對尺寸詞是抽獎,錨定才是控制。** `大一點`/`一點點` 在 NB2 沒有穩定映射 —
  同一個詞可以是 +20% 也可以是 +300%,而且**每輪從頭重擲,不會參考上一輪的幅度**,
  所以會無限震盪。要控尺寸就得給模型**畫面內的量尺**(比其他物件高多少)+ 百分比 +
  上界(不超過某條線)+ 方向(長高還是長寬)。**這是 B1「定性句 > 禁令堆疊」的尺寸版:
  給參照系,不給形容詞。**
- ✅ **「多」預設往橫向長。** 想要「更有份量」時,寫 `volume and height` 並鎖住左右端;
  只寫 `more` 會得到橫向鋪開、吃掉整個中景的木牆。
- ✅ **沒點名的元素 = 自由重擲。** 迭代時只講要改的那一個,已滿意的部分照樣漂。
  每輪都要帶**已定案元素凍結句**,把上一輪的成果一併寫進鎖裡。
- 📌 **待辦:** ①遮罩合成 + 色調微調收尾 ②引擎投影驗收(遊戲相機)
  ③若障礙物要當**可重複擺放的獨立資產**(掛 collider / 多場景重用),
  應改走 [A3](A3-forest-tree-cutout-inpaint.md) 拆件路線:洋紅底單獨生成 → 去背 → 引擎擺放,
  而非烙進背景圖
