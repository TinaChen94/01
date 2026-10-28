# blender-modular-bake — 模組化場景灰模 Bake 驗接縫

完整說明、原理、踩坑:[`docs/asset-cases/C1-blender-modular-bake-pipeline.md`](../../docs/asset-cases/C1-blender-modular-bake-pipeline.md)

Blender 4.x(Cycles)。全部在 **Scripting 分頁 → New → 貼上 → Run** 執行,**全程在另存的測試檔做**。

| 順序 | 腳本 | 要先選取? |
|---|---|---|
| 1 | `01_join_clean.py` 合併 `_J` + 清空殼 Empty | ✅ 選模組 Root Empty |
| 2 | `02_force_grey.py` 全部換 GREY_TEST(01 已換可略) | ✅ 全選 |
| 3 | `03_bake_uv.py` 新增 BakeUV + Smart UV | ❌ 自動找 `_J` |
| 4 | `04_fix_normals.py` 法線反面修復 | ❌(先在 Layout 透視視窗 Walk 站好) |
| 5 | `05_bake_targets.py` 解析度 + BAKE_ 材質/空白圖 | ❌ |
| 6 | `06_prepare_bake.py` 切回灰 + 選取 → **手動按 Bake** | ❌ |
| 7 | `07_save_and_preview.py` 存 EXR + 自發光預覽 + 存檔 | ❌ |
| 救援 | `08_relink.py` 洋紅色 / 換電腦後重新連結 | ❌ |

前置:World Strength = 0、材質 `GREY_TEST`(#767676、Roughness 0.5)已存在、燈光 Collection 全開。
Bake 設定:Diffuse / Direct ✅ Indirect ✅ Color ❌ / Render Max Samples 256 / Margin 16 px。

## Blender 文字區塊中文命名(建議)

用 **Text → Open** 開檔後,在文字編輯器上方名稱欄改成中文,自己用時比較好認。
repo 檔名維持英文(傳給別人不會亂碼);編號保留,清單才會照順序排。

| 英文檔名(repo) | Blender 裡的中文名 |
|---|---|
| `01_join_clean.py` | `01_合併模型_清理階層` |
| `02_force_grey.py` | `02_全部換灰材質` |
| `03_bake_uv.py` | `03_新增BakeUV_展開` |
| `04_fix_normals.py` | `04_修正反面` |
| `05_bake_targets.py` | `05_計算解析度_建Bake圖` |
| `06_prepare_bake.py` | `06_Bake前準備_切灰選取` |
| `07_save_and_preview.py` | `07_存EXR_發光預覽` |
| `08_relink.py` | `08_救援_重新連結貼圖` |
