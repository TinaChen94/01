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

- **機器欄位(時間 / 異動次數 / 圖檔數)**:跑腳本即自動刷新。新案例只要放在
  `docs/asset-cases/*.md`、`.../examples/*.md`、`asset-cutout-jobs/*/RECORD.md` 等
  追蹤路徑下(見腳本 `TRACK` 清單),就會自動被統計到。
- **人工欄位(完成度 / 分類 / 結論)**:需要讀檔內容才寫得出來 → 跟我說一句「更新統計」,我重讀後補。

---

## 總覽

| 指標 | 數字 |
|---|---|
| 觀測期間 | 2026-06-17 → 2026-07-11(25 天) |
| 分支(分流) | 8(7 條 `claude/*` + `main`;另有 1 條 `TinaChen94-patch-1`) |
| 參與 session | 13 |
| Skills / 框架 | 3 skills + 1 框架 |
| 原創工作流檔 | 3 |
| 資產案例 | 15 件(分布在 14 個檔) |
| 不重複成品圖 | 124 張 |

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
| **A1** | 哥德陵墓 Mausoleum | [A] 主角 / 去背 | 2D 板 ✅、未進 3D | 2 |
| **A2** | 中式石窟佛教浮雕牆 | [B] 場景模組 | 2D + height ✅、未進 3D | 6 |
| **A10** | 苔蘚草地 | [C] 可平鋪 | base albedo ✅、未派生 PBR | 1 |
| **A11** | 石板路 cobblestone | [C] 可平鋪 PBR | ⭐ PBR 全套 ✅(含 ORM / Blender bake / de-lit 校正) | 11 |
| **B1-gothic** | 哥德陵墓 concept→3D(examples) | [B] 場景模組 | ⚠️ WIP、純 prompt、無圖 | 0 |
| **B2-statue** | 青銅武將像 物件合成(examples) | [B] 物件合成 | ✅ 完成(森林 / 沼澤 2 變體) | 5 |
| **B1-forest** | 夜霧森林地面背景 — 4K 放大 + 材質保真管線 | 品質 / 放大管線(game bg) | ✅ 已驗證(16 迭代;A/B 版 + 多場景反例) | 13 |
| **B2-greybox** | 灰盒 → 夜森林地面模組(master tile) | greybox→模組 生成管線 | ✅ 三路線攻關(色標 / 深度 / Crop-Gen-Paste) | 11 |
| **B3-fenske** | 手繪筆觸奇幻概念圖 — NB2 保真 pass | 放大**反例**(類型分流實證) | ✅ 反面教材(筆觸型不能強求) | 2 |
| **B4-tileset** | master 貼圖 → 套圖變體(同圖材質替換) | 變體 / 套圖管線 | ✅ 已驗收;⚠️ 在 `b2-greybox-experiment`、**待併 main** | 15 |
| **B5-snow** | master 主題翻譯:森林 → 雪地(三檔位雪) | 變體 / 換皮管線 | ✅ 已驗收;⚠️ 在 `b2-greybox-experiment`、**待併 main** | 10 |
| **B6-camera** | 三相機管線(生成 / 出圖 / 遊戲相機解耦 + homography) | 相機 / 投影管線 | ✅ master 貼圖皆由此產出(已在 main) | 15 |
| **B7-unreal** | 三相機 → Unreal 重現(數值直搬) | 相機移植 | ✅ 三相機全通過(UE 5.5, 07-11;已在 main) | 28 |
| **graveyard-props** | 墓園道具(欄杆 / 門柱 / 墓碑) | 去背 job | ⚠️ 墓碑待做、無圖入庫 | 0 |
| **plants-cutout** | 立體寬葉植物去背(SAM 方框;苔蘚同色分不開) | 去背 job(純 matting) | ✅ 完成(透明母檔 + 橘底 + v1-matting/v2-render 變體) | 5 |

> - ⚠️ **B 系有兩套(編號撞名、不同系列)**:`examples/` 的 **B1-gothic / B2-statue**(concept→3D 示範)vs `docs/asset-cases/` 的 **B1-forest / B2-greybox / B3-fenske**(4K / 灰盒品質管線)。
> - A1 / A10 / A11 / B1-gothic 出自**同一張哥德墓園概念圖**;A2 為洞窟佛寺;**B1-forest→B2-greybox→B3→B4→B5→B6→B7 為同一條「夜森林 game bg / 灰盒→引擎」管線攻關**(B3 反例;B6 三相機 → B7 進 Unreal)。
> - **A1 = 同檔多分支複本**(blob 相同,非內容重複)。

---

## 3. 已沉澱的可複用模板 / SOP

> 從實測案例固化成可重用的模板 / SOP(機器掃不出,人工登錄)。

| 模板 / SOP | 位置 | 可搜尋入口 | 來源 |
|---|---|---|---|
| **物件合成進場景**(物件放進背景圖、鎖位鎖比例、整包對齊環境光照反射) | `references/nano-banana.md` §物件合成進場景 | `SKILL.md` 🪧「物件合成 / 把物件放進場景 / game art background asset」 | B2 案例實測 |
| **concept→3D 資產 pipeline**(front → 多視 → 3/4 → 45° iso) | `templates/concept-to-3d-pipeline.md` | `SKILL.md`「concept→3D / 拆概念圖 / 三視圖重建」 | inspiring-darwin(18 次迭代) |
| **image-grounded concept→3D 憲法**(原圖=真相,別用文字代理) | `references/concept-to-3d.md` | `SKILL.md` 硬規則 | session `014ecc8` |
| **去背 / 拆資產 SOP**(三模式 + 缺席色背景 + 正視參考板) | `skills/asset-cutout/` | `/asset-cutout` | A1 案例 |
| **Depth→Relight→Fusion 打光管線**(depth map + 光向控制圖鎖死光影、解 NB 無 seed;附 2 個 HTML 工具:深度打光器 / prompt 卡片庫) | `references/depth-relight-pipeline.md` + `tools/` | `SKILL.md` 指標 | ✅ 已併入 `main`(PR #9) |
| **4K 放大 / 材質保真 pass 管線**(類型分流:純保真 vs 生成式 pass、鎖句字典、letterbox 白邊坑) | `docs/asset-cases/B1-forest-bg-4k-detail.md`(B3 為反例) | 「B1 紀錄 / 4K 放大 / 材質保真」關鍵字 | B1-forest / B3-fenske |
| **灰盒 → game art 模組管線**(色標灰盒 / 深度 guidance / Crop-Gen-Paste、頂光、幾何滲漏) | `docs/asset-cases/B2-greybox-module-pipeline.md` | 「B2 紀錄 / 灰盒 / greybox」關鍵字 | B2-greybox |
| **三相機管線 + 引擎移植**(生成/出圖/遊戲相機解耦、homography 投影攤平、相機數值搬 Unreal) | `docs/asset-cases/B6-three-camera-pipeline.md` → `B7-unreal-camera-port.md` | 「三相機 / 相機解耦 / CineCamera / UE 相機」 | B6 / B7 |
| **master 變體 / 主題翻譯**(區域編輯鏈「老三樣」、換皮、厚度檔位) | `B4-master-variant-tileset.md` / `B5-theme-translation-snow.md` | 「套圖變體 / 材質替換 / 主題翻譯 / 森林轉雪」 | B4 / B5(⚠️ 待併 main) |

---

## 📈 自動統計

<!-- AUTO:START -->
> ⏱️ 自動產生於 `scripts/gen_stats.py`,掃描 8 個分支。異動次數 = 觸及該檔的 commit 數(含建立);時間為 UTC。

### 檔案統計(產生 / 異動 / 最後修改)

| 檔案 | 所在分支 | 產生時間 | 異動次數 | 最後修改 | 最近 session |
|---|---|---|---:|---|---|
| `concept-to-3d-pipeline.md` | claude/inspiring-darwin-hm3u4u | 2026-06-22 14:42 | 18 | 2026-06-23 08:33 | `01B7V59G5` |
| `concept-to-3d.md` | main | 2026-06-23 07:43 | 1 | 2026-06-23 07:43 | `014ecc8Bz` |
| `SKILL.md` | main | 2026-06-23 09:36 | 2 | 2026-06-23 12:01 | `01HFm82dQ` |
| `A1-mausoleum.md` | main | 2026-06-23 11:56 | 2 | 2026-06-23 12:28 | `01HFm82dQ` |
| `A10-A11-ground-tiles.md` | claude/trusting-knuth-f11ltb | 2026-06-23 13:15 | 5 | 2026-06-26 05:31 | `01MwFuhN6` |
| `A2-buddhist-relief-wall.md` | main | 2026-06-25 06:32 | 1 | 2026-06-25 06:32 | `01R1izqY5` |
| `B1-gothic-mausoleum.md` | main | 2026-06-25 06:32 | 1 | 2026-06-25 06:32 | `01R1izqY5` |
| `RECORD.md` | main | 2026-06-25 06:32 | 1 | 2026-06-25 06:32 | `01R1izqY5` |
| `B2-statue-into-forest.md` | main | 2026-06-28 13:05 | 1 | 2026-06-28 13:05 | `01Gc5rJav` |
| `README.md` | main | 2026-06-28 13:05 | 1 | 2026-06-28 13:05 | `01Gc5rJav` |
| `depth-relight-pipeline.md` | main | 2026-06-28 15:34 | 1 | 2026-06-28 15:34 | `01Gc5rJav` |
| `B1-forest-bg-4k-detail.md` | main | 2026-07-02 14:30 | 16 | 2026-07-03 16:51 | `01MdNxesm` |
| `B2-greybox-module-pipeline.md` | claude/b2-greybox-experiment-fgsc06 | 2026-07-03 11:00 | 4 | 2026-07-05 13:17 | `01Mcptxmy` |
| `B3-fenske-painterly-4k.md` | main | 2026-07-03 16:51 | 3 | 2026-07-03 16:58 | `01MdNxesm` |
| `README.md` | main | 2026-07-05 10:44 | 1 | 2026-07-05 10:44 | `01BPFFu8E` |
| `B4-master-variant-tileset.md` | claude/b2-greybox-experiment-fgsc06 | 2026-07-07 09:21 | 11 | 2026-07-09 10:42 | `01Mcptxmy` |
| `B5-theme-translation-snow.md` | claude/b2-greybox-experiment-fgsc06 | 2026-07-07 16:22 | 2 | 2026-07-08 00:24 | `01Mcptxmy` |
| `B6-three-camera-pipeline.md` | claude/b2-greybox-experiment-fgsc06 | 2026-07-08 02:59 | 13 | 2026-07-08 04:30 | `01Mcptxmy` |
| `B7-unreal-camera-port.md` | main | 2026-07-10 14:40 | 18 | 2026-07-11 12:48 | `01NN4jy2a` |

### 成品圖

- **不重複圖檔(blob)**:124 張
- **依案例**:A1 哥德陵墓 2 · A10 苔蘚草地 1 · A11 石板路 11 · A2 佛教浮雕牆 6
- **各分支圖檔數(含複本)**:claude/b2-greybox-experiment-fgsc06 97 · claude/light-branches-background-removal-24n9sf 30 · claude/object-placement-lighting-6gat9k 25 · claude/trusting-knuth-f11ltb 14 · claude/unity-camera-unreal-export-m50ht8 100 · main 100

### 各分支貢獻(相對 main 的獨有 commit)

| 分支 | 獨有 commit | 期間 |
|---|---:|---|
| main | 108 | 全部 merge 線 |
| claude/adoring-lamport-sh6fgh | 1 | 2026-06-23 → 2026-06-23 |
| claude/b2-greybox-experiment-fgsc06 | 41 | 2026-07-05 → 2026-07-09 |
| claude/inspiring-darwin-hm3u4u | 19 | 2026-06-22 → 2026-06-23 |
| claude/light-branches-background-removal-24n9sf | 5 | 2026-06-30 → 2026-07-01 |
| claude/object-placement-lighting-6gat9k | 1 | 2026-06-28 → 2026-06-28 |
| claude/trusting-knuth-f11ltb | 6 | 2026-06-23 → 2026-06-26 |
| claude/unity-camera-unreal-export-m50ht8 | 0 | — |

<!-- AUTO:END -->

---

## 註記

- 本頁為「快照 + 可重跑腳本」混合:**機器算時間/次數,人工標完成度**。完整刷新請跑腳本後再請 Claude 補人工欄位。
- 🔎 倉庫健檢:`python3 scripts/gen_stats.py --lint`(0 圖案例 / 孤兒圖 / 散落圖 / 多路徑重複 / 斷掉內嵌,數字以即時跑為準)。🧹 fetch 已加 `--prune` → **遠端刪掉的分支會自動從統計移除**。
- ✅ **主要收斂在 `main`**:13 案例 + 9 個 SOP/模板在 `main`(統計頁 / `gen_stats.py` 亦以 main 為正本);⚠️ **B4 / B5 兩案例仍在 `b2-greybox-experiment` 分支、待併 main**。
- 🧹 **分支現況**:現存 **8 條**(7 `claude/*` + `main`)+ `TinaChen94-patch-1`。🆕 `b2-greybox-experiment`(B4/B5 待併、B6/B7 已進 main)、`unity-camera-unreal-export`(0 獨有 commit = 可刪)。**可刪**:`light-branches` / `object-placement` / `unity-camera-unreal-export`。早期 dev:`adoring` / `inspiring` / `trusting`。
- ✅ **depth-relight 打光管線 + 2 工具已併入 `main`**(PR #9 / `3760178`)。
- ⚠️ **`main` 仍 pre-cleanup**:根目錄 9 張散圖保留作備份(`--lint` 可查)。要清跟我說。
