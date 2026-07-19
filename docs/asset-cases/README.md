# 資產拆解 / 去背 實戰紀錄

各資產「概念圖 → 去背 / 補圖 / 多視圖」的實戰案例。
對應工作流:`/asset-cutout`(去背 SOP)+ `ai-media-generator` 的 concept-to-3D pipeline。

## 案例索引

| 資產 | 紀錄 | 內容 |
|---|---|---|
| **A1 哥德陵墓 Mausoleum** | [A1-mausoleum.md](A1-mausoleum.md) | ✅ 逐字 prompt + 成品圖 + 可複用結論 |
| **A2 中式石窟佛教浮雕牆** | [A2-buddhist-relief-wall.md](A2-buddhist-relief-wall.md) | ✅ concept→3D:2 視圖 + height pass(場景模組件) |
| **A3 夜森林枯樹拆件 — 去背 + 補圖(洋紅底)** | [A3-forest-tree-cutout-inpaint.md](A3-forest-tree-cutout-inpaint.md) | ✅ 模式 1.1 六件拆件 + 洋紅工作底 + 逐字 prompt ×5 + 踩坑 ×8(緊裁換主角/殘留分流/浮水印) |
| **A10+A11 墓園地面材質(苔蘚草地/石板路)** | [A10-A11-ground-tiles.md](A10-A11-ground-tiles.md) | ✅ top-down 平拍 → PBR 材質(可平鋪模組,不生 mesh) |
| **B1 夜霧森林地面背景(4K 放大 + 材質細節)** | [B1-forest-bg-4k-detail.md](B1-forest-bg-4k-detail.md) | ✅ 定案管線 + 逐字 prompt + 鎖句字典 + 踩坑紀錄 + 驗收 checklist |
| **B2 灰盒 → 夜森林地面模組(master tile)** | [B2-greybox-module-pipeline.md](B2-greybox-module-pipeline.md) | ✅ 貼材質灰盒管線 + 三路線成敗對照 + 逐字 prompt 三連 + 技法字典 |
| **B3 手繪筆觸概念圖 NB2 失敗實證** | [B3-fenske-painterly-4k.md](B3-fenske-painterly-4k.md) | ❌「不能強求」範例:筆觸+角色型硬跑 NB2 材質保真 pass = 重繪級漂移(簽名搬家鐵證);此型一律走純保真放大分支 |
| **B6 三相機管線(遊戲/出圖/生成)** | [B6-three-camera-pipeline.md](B6-three-camera-pipeline.md) | ✅ 相機解耦架構 + 反解相機(homography)+ 品質三資源 + 踩坑 ×8;B7 的上游(注:文中 B4/B5 連結仍在 `claude/b2-greybox-experiment-fgsc06` 分支) |
| **B7 三相機 → Unreal 重現** | [B7-unreal-camera-port.md](B7-unreal-camera-port.md) | ✅ 三相機全數通過(UE 5.5,HFOV 91.49°/116.81°/80.93° 零誤差,CAM_GEN2 pitch = 反解俯角原數字):腳本 + 鎖檔 json ×3 + 圖解 SOP + 實戰踩坑(B4/B5 紀錄在 `claude/b2-greybox-experiment-fgsc06` 分支) |
| **B8 萬聖夜魔森背景(風格 DNA + 衍生圖鎖句)** | [B8-haunted-forest-style-dna.md](B8-haunted-forest-style-dna.md) | ✅ 五層風格拆解 + 母題清單 + 逐字風格鎖句 + 平台路線;⏳ 衍生圖待產(與 B1 非同系列) |

> 之後每拆一個資產(鐵欄杆、墓碑、枯樹…),就在這張表加一列、連到對應的 `*.md`。

## 最新預覽 — A1 陵墓正視參考板

![A1 mausoleum front orthographic](images/mausoleum-front-ortho.png)
