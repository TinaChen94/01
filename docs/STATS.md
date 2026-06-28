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
| 觀測期間 | 2026-06-17 → 2026-06-28(12 天) |
| 分支(分流) | 6(5 條 `claude/*` + `main`) |
| 參與 session | 9 |
| Skills / 框架 | 3 skills + 1 框架 |
| 原創工作流檔 | 3 |
| 資產案例 | 7 件(分布在 6 個檔) |
| 不重複成品圖 | 25 張 |

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
| **B1** | 哥德陵墓 concept→3D | [B] 場景模組 | ⚠️ WIP、純 prompt、無圖 | 0 |
| **B2** | 青銅武將像 — 物件合成進場景 | [B] 物件合成(放進背景、對齊光影) | ✅ 完成(暖陽森林 / 冷霧枯林 2 變體) | 5 |
| **graveyard-props** | 墓園道具(欄杆 / 門柱 / 墓碑) | 去背 job | ⚠️ 墓碑待做、無圖入庫 | 0 |

> - A1 / A10 / A11 / B1 出自**同一張哥德墓園概念圖**;A2 為洞窟佛寺;B2 為青銅武將像 + 森林/沼澤場景合成。
> - **A1 = 同檔多分支複本**(blob 相同,非內容重複);**B1 與 A1 僅「名字像」**(同一棟,但 B1 是未完成 WIP)。

---

## 3. 已沉澱的可複用模板 / SOP

> 從實測案例固化成可重用的模板 / SOP(機器掃不出,人工登錄)。

| 模板 / SOP | 位置 | 可搜尋入口 | 來源 |
|---|---|---|---|
| **物件合成進場景**(物件放進背景圖、鎖位鎖比例、整包對齊環境光照反射) | `references/nano-banana.md` §物件合成進場景 | `SKILL.md` 🪧「物件合成 / 把物件放進場景 / game art background asset」 | B2 案例實測 |
| **concept→3D 資產 pipeline**(front → 多視 → 3/4 → 45° iso) | `templates/concept-to-3d-pipeline.md` | `SKILL.md`「concept→3D / 拆概念圖 / 三視圖重建」 | inspiring-darwin(18 次迭代) |
| **image-grounded concept→3D 憲法**(原圖=真相,別用文字代理) | `references/concept-to-3d.md` | `SKILL.md` 硬規則 | session `014ecc8` |
| **去背 / 拆資產 SOP**(三模式 + 缺席色背景 + 正視參考板) | `skills/asset-cutout/` | `/asset-cutout` | A1 案例 |

---

## 📈 自動統計

<!-- AUTO:START -->
> ⏱️ 自動產生於 `scripts/gen_stats.py`,掃描 6 個分支。異動次數 = 觸及該檔的 commit 數(含建立);時間為 UTC。

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

### 成品圖

- **不重複圖檔(blob)**:25 張
- **依案例**:A1 哥德陵墓 2 · A10 苔蘚草地 1 · A11 石板路 11 · A2 佛教浮雕牆 6
- **各分支圖檔數(含複本)**:claude/affectionate-lamport-2jpqa6 2 · claude/trusting-knuth-f11ltb 14 · main 25

### 各分支貢獻(相對 main 的獨有 commit)

| 分支 | 獨有 commit | 期間 |
|---|---:|---|
| main | 25 | 全部 merge 線 |
| claude/adoring-lamport-sh6fgh | 1 | 2026-06-23 → 2026-06-23 |
| claude/affectionate-lamport-2jpqa6 | 5 | 2026-06-23 → 2026-06-25 |
| claude/festive-volta-sft8rv | 0 | — |
| claude/inspiring-darwin-hm3u4u | 19 | 2026-06-22 → 2026-06-23 |
| claude/trusting-knuth-f11ltb | 8 | 2026-06-23 → 2026-06-26 |

<!-- AUTO:END -->

---

## 註記

- 本頁為「快照 + 可重跑腳本」混合:**機器算時間/次數,人工標完成度**。完整刷新請跑腳本後再請 Claude 補人工欄位。
- 🔎 倉庫健檢:`python3 scripts/gen_stats.py --lint`(0 圖案例 / 孤兒圖 / 散落圖 / 多路徑重複 / 斷掉內嵌,數字以即時跑為準)。🧹 fetch 已加 `--prune` → **遠端刪掉的分支會自動從統計移除**。
- ✅ **全數收斂到 `main`**:6 案例(A1 / A2 / A10-A11 / B1 / B2 / props)+ A11 de-lit + 物件合成模板皆在 `main`;統計頁與 `gen_stats.py` 也以 `main` 為正本。
- 🧹 **分支已清理**:`quirky-wright`、`object-placement-lighting`、`relaxed-bardeen`、`sync-a11-delight` 皆已刪除(內容無遺失,`--prune` 已反映)→ 現存 6 分支;PR #8 已關閉(被 `81288c6` 取代)。
- ⚠️ **`main` 仍 pre-cleanup**:根目錄 9 張散圖保留作備份(`--lint` 可查)。要清跟我說。
