# 📊 產出統計總表 — `TinaChen94/01`

> 這個 repo **註冊以來(2026-06-17 起)** 產出的 skills / 工作流 / 資產案例 / 成品圖總表,
> 含每項的 **產生時間、異動次數、最後修改時間**。
>
> - **下半部「自動統計」** 由 [`scripts/gen_stats.py`](../scripts/gen_stats.py) 跨**所有 `claude/*` 分支**掃出 git 歷史,可隨時重跑刷新。
> - **上半部「分類 / 完成度」** 是人工(Claude)標註 —— 機器算不出來的東西:完成度、資產分類、結論。
> - 📌 快照日期見自動區塊的時間戳。時間皆為 UTC。

---

## 🔄 如何更新這頁

```bash
python3 scripts/gen_stats.py            # 重新掃描所有分支,刷新下方「自動統計」區塊
python3 scripts/gen_stats.py --stdout   # 只印出、不寫檔(預覽)
python3 scripts/gen_stats.py --no-fetch # 離線(略過 git fetch)
```

- ✅ **會自動抓的**:只有 `gen_stats.py` 的 `TRACK` 清單裡的路徑 —— 案例檔
  `docs/asset-cases/*.md`、`.../examples/*.md`、`asset-cutout-jobs/*/*.md`,外加少數指名的
  工作流檔(concept-to-3d-pipeline / concept-to-3d(-v2) / asset-cutout SKILL / depth-relight-pipeline)。
  放進這些路徑,跑腳本就進統計。
- ⚠️ **不會自動抓 —— 新增下列務必手動處理,否則統計會漏**:
  **新 skill**、**新 reference / template / tool**、**SKILL 版本升級(例:V2 `concept-to-3d-v2.md`)**、skills 目錄變動。
  → 把新路徑加進 `gen_stats.py` 的 `TRACK`(之後也會自動刷新),**或**直接跟 Claude 說
  「**有新增 SKILL / 更新統計**」,我會讀檔、登錄 §1/§3、補 `TRACK`。
- 🧰 **人工欄位(完成度 / 分類 / 結論、§1 skills、§3 SOP)**:機器算不出、要讀檔內容 → 跟我說「更新統計」我重讀後補。

---

## 總覽

| 指標 | 數字 |
|---|---|
| 觀測期間 | 2026-06-17 → 2026-10-26(約 4 個月) |
| 分支(分流) | 11(10 條 `claude/*` + `main`;另有 1 條 `TinaChen94-patch-1`) |
| 參與 session | ~20 |
| Skills / 框架 | 3 skills + 1 框架 |
| 原創工作流檔 | 5(含 concept→3D **V2** 雙軌、去光→PBR `delight-pbr`) |
| 資產案例 | 27 件(分布在 26 個檔) |
| 不重複成品圖 | 283 張 |

---

## 1. Skills / 框架

| 名稱 | 類型 | 來源 | 產生時間 |
|---|---|---|---|
| **ai-media-generator** | skill | 第三方安裝(Hao, MIT) | 2026-06-17 |
| **code-cleanup-helper** | skill | 第三方安裝(Hao, MIT) | 2026-06-17 |
| **video-autopilot-kit** | 框架(非 skill) | 第三方 vendoring | 2026-06-17 |
| **asset-cutout** | skill | ⭐**原創** | 2026-06-23 |

> 各原創檔的精確 commit 統計見下方「自動統計 → 檔案統計」。

---

## 2. 資產案例(完成度 / 分類)

| 案例 | 主題 | 分類 | 完成度 | 成品圖 |
|---|---|---|---|---:|
| **A1** | 哥德陵墓 Mausoleum | [A] 去背 / 正交板 | 2D 板 ✅、未進 3D | 2 |
| **A2** | 中式石窟佛教浮雕牆 | [A/B] concept→3D de-lit+height | 2D 板 ✅ | 6 |
| **A3** | 夜森林枯樹拆件 — 去背 + 補圖(模式 1.1、洋紅底) | [A] 去背 / inpaint | ✅(在 `plant-concept-breakdown` 分支) | 11 |
| **A4-bush** | 明亮森林植被叢去背(圈選分件) | [A] 2D 保真去背 | ✅(在 `plant-concept-breakdown` 分支) | — |
| **A4-castle** | 古堡哥德大廳 — 概念圖拆解(建築四件、保光影軌) | [A] concept→3D 拆件 | ✅(10-26,main) | 多件 |
| **A5-castle** | 古堡哥德大廳 — 三視圖重建(道具 turnaround → image-to-3D) | [A] concept→3D turnaround | ✅(10-26,main) | 多張 |
| **A10** | 苔蘚草地 | [C] 可平鋪 | base albedo ✅、未派生 PBR | 1 |
| **A11** | 石板路 cobblestone | [C] 可平鋪 PBR | ⭐ PBR 全套 ✅(含 ORM / Blender bake / de-lit 校正) | 11 |
| **A12** | 哥德雙開門 — 顏色範圍自動遮罩(紅色區域加強) | [A] 2D 局部調色 / 遮罩 | ✅(10-26,遮罩驗收) | 5 |
| **B1-gothic** | 哥德陵墓 concept→3D(examples) | [B] 場景模組 | ⚠️ WIP、純 prompt、無圖 | 0 |
| **B2-statue** | 青銅武將像 物件合成(examples) | [B] 物件合成 | ✅ 完成(森林 / 沼澤 2 變體) | 5 |
| **B1-forest** | 夜霧森林地面背景 — 4K 放大 + 材質保真管線 | 品質 / 放大管線(game bg) | ✅ 已驗證(16 迭代;A/B 版 + 多場景反例) | 13 |
| **B2-greybox** | 灰盒 → 夜森林地面模組(master tile) | greybox→模組 生成管線 | ✅ 三路線攻關(色標 / 深度 / Crop-Gen-Paste) | 11 |
| **B3-fenske** | 手繪筆觸奇幻概念圖 — NB2 保真 pass | 放大**反例**(類型分流實證) | ✅ 反面教材(筆觸型不能強求) | 2 |
| **B4-tileset** | master 貼圖 → 套圖變體道路縫合(同圖材質替換) | 變體 / 套圖管線 | ✅ 已併 main(套圖三規則 / 四方連續 SOP) | 15 |
| **B5-snow** | master 主題翻譯:森林 → 雪地(薄 / 厚 / 冰殼三檔) | 變體 / 換皮管線 | ✅ 已併 main(鎖分層 / 鏈要短) | 10 |
| **B6-camera** | 三相機管線(生成 / 出圖 / 遊戲相機解耦 + homography) | 相機 / 投影管線 | ✅ master 貼圖皆由此產出 | 15 |
| **B7-unreal** | 三相機 → Unreal 重現(數值直搬) | 相機移植 | ✅ 三相機全通過(UE 5.5) | 28 |
| **B8** | 場景就地生成障礙物(石堆/倒木;紅圈定位 + 尺寸錨定) | 物件置放 | ✅ | 6 |
| **B9** | 樹資產重上色(幾何滲漏根治 / 材質特寫路線) | 重上色 / 風格轉移 | ✅ | 6 |
| **B10** | 萬聖夜魔森 — 風格 DNA + 鎖句(暗黑插畫) | 風格 DNA | ✅ 路線 A 一次過 | 3 |
| **B11** | 月夜 RPG 森林 — 風格 DNA(明亮日式) | 風格 DNA | ✅ | 8 |
| **B12** | 跨圖天空移植(只搬天空層 + 天空後製) | 雙參考合成 | ✅ | 4 |
| **B13** | 寫實貼圖 → 手繪風格轉移(Ruined King 級) | style transfer | ✅ 定版 + 七套圖量產 | 20 |
| **B14** | 半寫實暗黑森林地面 — 風格 DNA | 風格 DNA | ⚠️ 在 `image-style-analysis` 分支 | — |
| **graveyard-props** | 墓園道具(欄杆 / 門柱 / 墓碑) | 去背 job | ⚠️ 墓碑待做、無圖入庫 | 0 |
| **plants-cutout** | 立體寬葉植物去背(SAM 方框;苔蘚同色分不開) | 去背 job(純 matting) | ✅ 完成(透明母檔 + 橘底 + v1/v2 變體) | 5 |

> - ⚠️ **編號撞名**:**B 系兩套** — `examples/` 的 B1-gothic / B2-statue(concept→3D 示範)vs `docs/asset-cases/` 的 B1-forest … B14(背景 / 管線);**A4 兩個** — `A4-dark-bush-cutout`(植被去背)vs `A4-castle-concept-decomposition`(古堡拆解)。
> - **B 系主線**:B1-forest→B2-greybox→B3→B4→B5→B6→B7(夜森林 game bg / 灰盒→引擎);**風格 DNA 群** B10 / B11 / B14 各為獨立風格;A4-castle / A5-castle 為古堡 concept→3D 姊妹篇。
> - **A1 = 同檔多分支複本**(blob 相同,非內容重複)。

---

## 3. 已沉澱的可複用模板 / SOP

> 從實測案例固化成可重用的模板 / SOP(機器掃不出,人工登錄)。

| 模板 / SOP | 位置 | 可搜尋入口 | 來源 |
|---|---|---|---|
| **物件合成進場景**(物件放進背景圖、鎖位鎖比例、整包對齊環境光照反射) | `references/nano-banana.md` §物件合成進場景 | `SKILL.md` 🪧「物件合成 / 把物件放進場景 / game art background asset」 | B2 案例實測 |
| **concept→3D 資產 pipeline**(front → 多視 → 3/4 → 45° iso) | `templates/concept-to-3d-pipeline.md` | `SKILL.md`「concept→3D / 拆概念圖 / 三視圖重建」 | inspiring-darwin(18 次迭代) |
| **image-grounded concept→3D 憲法 + V2 雙軌**(原圖=真相;**V2** 升級為保光影 ↔ de-lit 雙軌 + 正交鎖 + A4/A5 救援招式,V1 保留) | `references/concept-to-3d-v2.md`(V1 原版:`concept-to-3d.md`) | `SKILL.md` 硬規則 / 已指向 V2 | 014ecc8 → V2(687e7c0) |
| **去背 / 拆資產 SOP**(三模式 + 缺席色背景 + 正視參考板) | `skills/asset-cutout/` | `/asset-cutout` | A1 案例 |
| **Depth→Relight→Fusion 打光管線**(depth map + 光向控制圖鎖死光影、解 NB 無 seed;附 2 個 HTML 工具:深度打光器 / prompt 卡片庫) | `references/depth-relight-pipeline.md` + `tools/` | `SKILL.md` 指標 | ✅ 已併入 `main`(PR #9) |
| **去光 → PBR 整套貼圖(de-light → PBR maps)**(帶光材質/場景圖 → 去光真 albedo → 派生 base/height/normal/rough/metallic/AO;**normal 一律從 height 派生**、Blender 重打光踩坑、場景板 vs 可平鋪分型) | `docs/asset-cases/SOP-ai-delight-pbr.md`(完整案例)+ `references/delight-pbr.md`(自動反射片段)+ `tools/pbr-derive/` | `CLAUDE.md` / `SKILL.md`「delight pbr / delight / AI PBR / 去光出 PBR / 照 AI PBR 配方」 | 三 worked example(牆 / 拱頂 / 地板) |
| **4K 放大 / 材質保真 pass 管線**(類型分流:純保真 vs 生成式 pass、鎖句字典、letterbox 白邊坑) | `docs/asset-cases/B1-forest-bg-4k-detail.md`(B3 為反例) | 「B1 紀錄 / 4K 放大 / 材質保真」關鍵字 | B1-forest / B3-fenske |
| **灰盒 → game art 模組管線**(色標灰盒 / 深度 guidance / Crop-Gen-Paste、頂光、幾何滲漏) | `docs/asset-cases/B2-greybox-module-pipeline.md` | 「B2 紀錄 / 灰盒 / greybox」關鍵字 | B2-greybox |
| **三相機管線 + 引擎移植**(生成/出圖/遊戲相機解耦、homography 投影攤平、相機數值搬 Unreal) | `docs/asset-cases/B6-three-camera-pipeline.md` → `B7-unreal-camera-port.md` | 「三相機 / 相機解耦 / CineCamera / UE 相機」 | B6 / B7 |
| **master 變體 / 主題翻譯**(區域編輯鏈「老三樣」、換皮、厚度檔位) | `B4-master-variant-tileset.md` / `B5-theme-translation-snow.md` | 「套圖變體 / 材質替換 / 主題翻譯 / 森林轉雪」 | B4 / B5(已併 main) |
| **風格母本重打光公式**(兩段式:Phase 1 風格建檔一次 → Phase 2 場景重打光,可跨風格複用) | `docs/asset-cases/SOP-style-relight.md` | `CLAUDE.md`「照打光公式 / 打光公式 / 風格建檔」 | B10 首度驗證;`image-style-analysis` |
| **風格 DNA 拆解 + 衍生鎖句**(色盤 / 光 / 筆觸 / 構圖文法 分層拆解 → 產同風格衍生圖) | `B10` / `B11` / `B14` 案例 | 「風格 DNA / 風格鎖句」 | B10 / B11 / B14 |
| **顏色範圍自動遮罩**(HSV 門檻逐像素抓遮罩、只在遮罩內加強、保留 alpha;碎片化單色區不用手選) | `docs/asset-cases/A12-door-color-range-mask.md` + `tools/color-range-mask/color_mask.py` | 「照 A12 / 顏色遮罩 / 加強某色」 | A12 |

---

## 📈 自動統計

<!-- AUTO:START -->
> ⏱️ 自動產生於 `scripts/gen_stats.py`,掃描 11 個分支。異動次數 = 觸及該檔的 commit 數(含建立);時間為 UTC。

### 檔案統計(產生 / 異動 / 最後修改)

| 檔案 | 所在分支 | 產生時間 | 異動次數 | 最後修改 | 最近 session |
|---|---|---|---:|---|---|
| `concept-to-3d-pipeline.md` | claude/inspiring-darwin-hm3u4u | 2026-06-22 14:42 | 18 | 2026-06-23 08:33 | `01B7V59G5` |
| `SKILL.md` | claude/light-branches-background-removal-24n9sf | 2026-06-23 09:36 | 2 | 2026-06-23 12:01 | `01HFm82dQ` |
| `A1-mausoleum.md` | claude/light-branches-background-removal-24n9sf | 2026-06-23 11:56 | 2 | 2026-06-23 12:28 | `01HFm82dQ` |
| `A10-A11-ground-tiles.md` | claude/trusting-knuth-f11ltb | 2026-06-23 13:15 | 5 | 2026-06-26 05:31 | `01MwFuhN6` |
| `A2-buddhist-relief-wall.md` | claude/plant-concept-breakdown-n8y1o1 | 2026-07-10 14:40 | 2 | 2026-07-31 05:05 | `015Te6zoy` |
| `B1-forest-bg-4k-detail.md` | main | 2026-07-10 14:40 | 2 | 2026-07-26 08:34 | `011YGmpRj` |
| `B1-gothic-mausoleum.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `B2-greybox-module-pipeline.md` | main | 2026-07-10 14:40 | 3 | 2026-07-26 21:56 | `01Mcptxmy` |
| `B2-statue-into-forest.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `B3-fenske-painterly-4k.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `B7-unreal-camera-port.md` | main | 2026-07-10 14:40 | 18 | 2026-07-11 12:48 | `01NN4jy2a` |
| `README.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `README.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `RECORD.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `concept-to-3d.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `depth-relight-pipeline.md` | main | 2026-07-10 14:40 | 1 | 2026-07-10 14:40 | `01NN4jy2a` |
| `B6-three-camera-pipeline.md` | main | 2026-07-11 12:48 | 3 | 2026-07-26 08:45 | `01Mcptxmy` |
| `A3-forest-tree-cutout-inpaint.md` | claude/plant-concept-breakdown-n8y1o1 | 2026-07-19 11:53 | 18 | 2026-07-31 05:05 | `015Te6zoy` |
| `SOP-style-relight.md` | claude/image-style-analysis-72zhrh | 2026-07-20 04:03 | 21 | 2026-07-28 07:19 | `01QQg5a3h` |
| `B8-scene-obstacle-placement.md` | main | 2026-07-26 07:11 | 4 | 2026-07-26 08:19 | `01CRZQW5i` |
| `B9-tree-trunk-restyle.md` | main | 2026-07-26 07:58 | 2 | 2026-07-26 08:18 | `01PPTafL3` |
| `B10-haunted-forest-style-dna.md` | main | 2026-07-26 14:49 | 1 | 2026-07-26 14:49 | `01QQg5a3h` |
| `B11-moonlit-jrpg-forest-style-dna.md` | main | 2026-07-26 14:49 | 1 | 2026-07-26 14:49 | `01QQg5a3h` |
| `B12-sky-transplant.md` | main | 2026-07-26 21:30 | 1 | 2026-07-26 21:30 | `01AxGHb9X` |
| `B4-master-variant-tileset.md` | main | 2026-07-26 21:50 | 1 | 2026-07-26 21:50 | `01Mcptxmy` |
| `B5-theme-translation-snow.md` | main | 2026-07-26 21:50 | 1 | 2026-07-26 21:50 | `01Mcptxmy` |
| `B13-handpainted-style-transfer.md` | main | 2026-07-27 16:25 | 4 | 2026-07-27 16:47 | `01Gif5qPY` |
| `B14-realistic-forest-floor-style-dna.md` | claude/image-style-analysis-72zhrh | 2026-07-28 07:03 | 10 | 2026-07-28 09:05 | `01QQg5a3h` |
| `A4-dark-bush-cutout.md` | claude/plant-concept-breakdown-n8y1o1 | 2026-07-31 04:08 | 11 | 2026-07-31 07:29 | `015Te6zoy` |
| `README.md` | main | 2026-09-02 04:04 | 1 | 2026-09-02 04:04 | `0139cX4Bb` |
| `A4-castle-concept-decomposition.md` | main | 2026-10-25 17:09 | 13 | 2026-10-26 00:54 | `0139cX4Bb` |
| `A5-castle-turnaround-image-to-3d.md` | main | 2026-10-25 19:23 | 22 | 2026-10-26 06:59 | `0139cX4Bb` |
| `concept-to-3d-v2.md` | main | 2026-10-26 06:57 | 1 | 2026-10-26 06:57 | `0139cX4Bb` |
| `SOP-ai-delight-pbr.md` | main | 2026-10-26 10:59 | 10 | 2026-10-26 12:31 | `01JNKQQWf` |
| `delight-pbr.md` | main | 2026-10-26 12:08 | 3 | 2026-10-26 12:20 | `01JNKQQWf` |
| `color_mask.py` | main | 2026-10-26 12:38 | 2 | 2026-10-26 12:39 | `017KFxVMr` |
| `A12-door-color-range-mask.md` | main | 2026-10-26 12:39 | 1 | 2026-10-26 12:39 | `017KFxVMr` |

### 成品圖

- **不重複圖檔(blob)**:283 張
- **依案例**:A1 哥德陵墓 2 · A10 苔蘚草地 1 · A11 石板路 11 · A2 佛教浮雕牆 6
- **各分支圖檔數(含複本)**:claude/a10-a11-a2-assets-fv7p41 299 · claude/great-davinci-7u4stk 304 · claude/image-style-analysis-72zhrh 191 · claude/light-branches-background-removal-24n9sf 30 · claude/object-placement-lighting-6gat9k 25 · claude/plant-concept-breakdown-n8y1o1 191 · claude/trusting-knuth-f11ltb 14 · claude/unity-camera-unreal-export-m50ht8 100 · main 304

### 各分支貢獻(相對 main 的獨有 commit)

| 分支 | 獨有 commit | 期間 |
|---|---:|---|
| main | 239 | 全部 merge 線 |
| claude/a10-a11-a2-assets-fv7p41 | 0 | — |
| claude/adoring-lamport-sh6fgh | 7 | 2026-06-17 → 2026-06-23 |
| claude/great-davinci-7u4stk | 0 | — |
| claude/image-style-analysis-72zhrh | 10 | 2026-07-28 → 2026-07-28 |
| claude/inspiring-darwin-hm3u4u | 21 | 2026-06-17 → 2026-06-23 |
| claude/light-branches-background-removal-24n9sf | 36 | 2026-06-17 → 2026-07-01 |
| claude/object-placement-lighting-6gat9k | 31 | 2026-06-17 → 2026-06-28 |
| claude/plant-concept-breakdown-n8y1o1 | 11 | 2026-07-31 → 2026-07-31 |
| claude/trusting-knuth-f11ltb | 14 | 2026-06-17 → 2026-06-26 |
| claude/unity-camera-unreal-export-m50ht8 | 0 | — |

<!-- AUTO:END -->

---

## 註記

- 本頁為「快照 + 可重跑腳本」混合:**機器算時間/次數,人工標完成度**。完整刷新請跑腳本後再請 Claude 補人工欄位。
- 🔎 倉庫健檢:`python3 scripts/gen_stats.py --lint`(0 圖案例 / 孤兒圖 / 散落圖 / 多路徑重複 / 斷掉內嵌,數字以即時跑為準)。🧹 fetch 已加 `--prune` → **遠端刪掉的分支會自動從統計移除**。
- ✅ **大多已收斂在 `main`**:約 27 案例 + 多數 SOP 在 `main`(統計頁 / `gen_stats.py` 亦以 main 為正本);**B4 / B5 已補進 main**;**新進 main:A12 顏色範圍遮罩 + SOP 去光→PBR(delight-pbr,含三 worked example 與 `tools/pbr-derive/`)**。仍在分支未併 main:**A3 / A4-bush**(`plant-concept-breakdown`)、**B14 / SOP 打光公式**(`image-style-analysis`)。
- 🧹 **分支現況**:現存 **11 條**(10 `claude/*` + `main`)+ `TinaChen94-patch-1`。活躍:`plant-concept-breakdown`(A3/A4-bush)、`image-style-analysis`(B14 / 打光公式 SOP)。可清(獨有 commit = 0、內容已在 main):`a10-a11-a2-assets` / `great-davinci` / `unity-camera-unreal-export`;另舊分支 `adoring` / `inspiring` / `trusting` / `light-branches` / `object-placement` 內容亦已在 main。
- ✅ **depth-relight 打光管線 + 2 工具已併入 `main`**(PR #9 / `3760178`)。
- ⚠️ **`main` 仍 pre-cleanup**:根目錄 9 張散圖保留作備份(`--lint` 可查)。要清跟我說。
