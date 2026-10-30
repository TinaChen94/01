# blender-final-bake — 正式貼圖 → 單張 Combined Bake(古堡打光二版)

完整說明、路線演進、踩坑:[`docs/asset-cases/C2-blender-final-combined-bake.md`](../../docs/asset-cases/C2-blender-final-combined-bake.md)
(上游:[`C1`](../../docs/asset-cases/C1-blender-modular-bake-pipeline.md) 灰模驗接縫)

Blender 4.x(Cycles)。Scripting 分頁 → **Text → Open** 開檔(或貼上)→ Alt+P。**一律在另存的副本執行**(腳本會自動存檔)。
模組放在 Collection `TINA_HIGH`(其他專案改腳本開頭 `COLLECTION`)。

| 順序 | 檔案 | Blender 文字區塊中文名 | 要先選取? |
|---|---|---|---|
| 0 | `00_check_uv_res.py` | `00_檢查UV_解析度` | ❌(重複 Alt+P 到「全部完成!」) |
| 1 | `01_bake_final_all.py` | `01_正式bake_全部` | ❌(一次一個,重複 Alt+P) |
| 1b | `01b_bake_final_targets.py` | `01_正式bake_指定` | TARGETS 填名稱,或留空用選取 |
| 2 | `02_bake_quick_targets.py` | `02_指定bake_試算` | TARGETS 填名稱 |
| 3 | `03_toggle_view.py` | `03_切換檢查` | ✅(ONLY_SELECTED=True 時) |
| 選用 | `opt_bake_ao.py` | `腳本C_bakeAO` | ❌(本案未採用) |

前置:World Strength 依打光設定、燈光 Collection 全開、所有模組顯示。
Bake 圖存在 `.blend` 旁的 `bake_final/`(`FINAL_<模組>.exr`);換電腦要一起帶走。
存檔或匯出前:`03_toggle_view.py` 設 `MODE = "RESTORE"`、`ONLY_SELECTED = False` 跑一次,恢復同事材質。
