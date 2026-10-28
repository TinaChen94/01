# blender-modular-bake — 模組化場景灰模 Bake 驗接縫

完整說明、原理、踩坑:[`docs/asset-cases/B14-blender-modular-bake-pipeline.md`](../../docs/asset-cases/B14-blender-modular-bake-pipeline.md)

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
