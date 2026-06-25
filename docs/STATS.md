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
| 觀測期間 | 2026-06-17 → 2026-06-25(9 天) |
| 分支(分流) | 8(7 條 `claude/*` + `main`) |
| 參與 session | 8 |
| Skills / 框架 | 3 skills + 1 框架 |
| 原創工作流檔 | 3 |
| 資產案例 | 6 件(分布在 5 個檔) |
| 不重複成品圖 | 19 張 |

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
| **A11** | 石板路 cobblestone | [C] 可平鋪 PBR | ⭐ PBR 全套 ✅(含 ORM / Blender bake) | 10 |
| **B1** | 哥德陵墓 concept→3D | [B] 場景模組 | ⚠️ WIP、純 prompt、無圖 | 0 |
| **graveyard-props** | 墓園道具(欄杆 / 門柱 / 墓碑) | 去背 job | ⚠️ 墓碑待做、無圖入庫 | 0 |

> - A1 / A10 / A11 / B1 出自**同一張哥德墓園概念圖**;A2 為另一張洞窟佛寺概念圖。
> - **A1 = 同檔多分支複本**(blob 相同,非內容重複);**B1 與 A1 僅「名字像」**(同一棟,但 B1 是未完成 WIP)。

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
| `A10-A11-ground-tiles.md` | claude/trusting-knuth-f11ltb | 2026-06-23 13:15 | 4 | 2026-06-23 14:32 | `01MwFuhN6` |
| `A2-buddhist-relief-wall.md` | claude/relaxed-bardeen-n9esux | 2026-06-24 13:57 | 7 | 2026-06-24 14:24 | `013jQQysa` |
| `B1-gothic-mausoleum.md` | main | 2026-06-25 06:32 | 1 | 2026-06-25 06:32 | `01R1izqY5` |
| `RECORD.md` | main | 2026-06-25 06:32 | 1 | 2026-06-25 06:32 | `01R1izqY5` |

### 成品圖

- **不重複圖檔(blob)**:19 張
- **依案例**:A1 哥德陵墓 2 · A10 苔蘚草地 1 · A11 石板路 10 · A2 佛教浮雕牆 6
- **各分支圖檔數(含複本)**:claude/affectionate-lamport-2jpqa6 2 · claude/quirky-wright-rkdcey 13 · claude/relaxed-bardeen-n9esux 8 · claude/trusting-knuth-f11ltb 13 · main 19

### 各分支貢獻(相對 main 的獨有 commit)

| 分支 | 獨有 commit | 期間 |
|---|---:|---|
| main | 18 | 全部 merge 線 |
| claude/adoring-lamport-sh6fgh | 1 | 2026-06-23 → 2026-06-23 |
| claude/affectionate-lamport-2jpqa6 | 5 | 2026-06-23 → 2026-06-25 |
| claude/festive-volta-sft8rv | 0 | — |
| claude/inspiring-darwin-hm3u4u | 19 | 2026-06-22 → 2026-06-23 |
| claude/quirky-wright-rkdcey | 8 | 2026-06-23 → 2026-06-24 |
| claude/relaxed-bardeen-n9esux | 11 | 2026-06-23 → 2026-06-24 |
| claude/trusting-knuth-f11ltb | 7 | 2026-06-23 → 2026-06-23 |

<!-- AUTO:END -->

---

## 註記

- 本頁為「快照 + 可重跑腳本」混合:**機器算時間/次數,人工標完成度**。完整刷新請跑腳本後再請 Claude 補人工欄位。
- 🔎 倉庫健檢:`python3 scripts/gen_stats.py --lint` 會掃出 0 圖案例 / 孤兒圖 / 散落圖 / 多路徑重複 / 斷掉內嵌。
- ✅ **遺漏已解決**:`main` 已於 2026-06-25 的 `b001957`(Consolidate all asset data, pre-cleanup safety)收齊**全部 5 案例 + 19 圖**(B1 / props 仍 0 圖未完成,但檔已在 main)。
- ✅ **本工作分支(`quirky-wright`)已示範清理**:A10/A11 歸位、根目錄散圖清空。
- ⚠️ **重複 / 散圖尚未清**:`main`、`affectionate-lamport`、`relaxed-bardeen` 三處各仍有 9 張根目錄散圖 →`--lint` 顯示**散落圖 27、多路徑重複 9**。`main` 是 pre-cleanup 安全備份,清理那一刀(刪根目錄散圖)還沒落在 main 上。
