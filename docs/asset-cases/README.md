# 資產拆解 / 去背 實戰紀錄

各資產「概念圖 → 去背 / 補圖 / 多視圖」的實戰案例。
對應工作流:`/asset-cutout`(去背 SOP)+ `ai-media-generator` 的 concept-to-3D pipeline。

## 案例索引

| 資產 | 紀錄 | 內容 |
|---|---|---|
| **A1 哥德陵墓 Mausoleum** | [A1-mausoleum.md](A1-mausoleum.md) | ✅ 逐字 prompt + 成品圖 + 可複用結論 |
| **A2 中式石窟佛教浮雕牆** | [A2-buddhist-relief-wall.md](A2-buddhist-relief-wall.md) | ✅ concept→3D:2 視圖 + height pass(場景模組件) |
| **A3 夜森林枯樹拆件 — 去背 + 補圖(洋紅底)** | [A3-forest-tree-cutout-inpaint.md](A3-forest-tree-cutout-inpaint.md) | ✅ 模式 1.1 六件拆件 + 洋紅工作底 + 逐字 prompt ×7(實跑原文)+ 踩坑 ×8(緊裁換主角/殘留分流/浮水印) |
| **A4 明亮森林植被叢去背(概念圖拆件)** | [A4-dark-bush-cutout.md](A4-dark-bush-cutout.md) | ✅ 兩版實測成功可用:版1「dark shrub」保真去背(合併成背景牆)+ 版2「3 red circles」指名分件(三叢分開);含關鍵鎖句(keep natural silhouette 治假圓球、指名圈數自動分件)|
| **A10+A11 墓園地面材質(苔蘚草地/石板路)** | [A10-A11-ground-tiles.md](A10-A11-ground-tiles.md) | ✅ top-down 平拍 → PBR 材質(可平鋪模組,不生 mesh) |
| **B1 夜霧森林地面背景(4K 放大 + 材質細節)** | [B1-forest-bg-4k-detail.md](B1-forest-bg-4k-detail.md) | ✅ 定案管線 + 逐字 prompt + 鎖句字典 + 踩坑紀錄 + 驗收 checklist |
| **B2 灰盒 → 夜森林地面模組(master tile)** | [B2-greybox-module-pipeline.md](B2-greybox-module-pipeline.md) | ✅ 貼材質灰盒管線 + 三路線成敗對照 + 逐字 prompt 三連 + 技法字典 |
| **B3 手繪筆觸概念圖 NB2 失敗實證** | [B3-fenske-painterly-4k.md](B3-fenske-painterly-4k.md) | ❌「不能強求」範例:筆觸+角色型硬跑 NB2 材質保真 pass = 重繪級漂移(簽名搬家鐵證);此型一律走純保真放大分支 |
| **B4 master 貼圖 → 套圖變體道路縫合(同圖材質替換)** | [B4-master-variant-tileset.md](B4-master-variant-tileset.md) | ✅ 區域編輯鏈 + 套圖三規則 + 直路兩路線攻防(遮罩重畫失敗/佔位縫合正解)+ 端頭版 road_fade + 零變化除錯階梯 + 四方連續 SOP + 逐字勝利/失敗 prompt |
| **B5 master 主題翻譯:森林 → 雪地三檔位** | [B5-theme-translation-snow.md](B5-theme-translation-snow.md) | ✅ 主題翻譯/厚度/品種三層 pass + 鎖分層(大形鎖/小形授權)+ 鏈要短(調色歸 PS 預設)+ 色票板配比 + 踩坑 ×4 |
| **B6 三相機管線(遊戲/出圖/生成)** | [B6-three-camera-pipeline.md](B6-three-camera-pipeline.md) | ✅ 相機解耦架構 + 反解相機(homography)+ 品質三資源 + 踩坑 ×8;B7 的上游、B4/B5 的產出源 |
| **B7 三相機 → Unreal 重現** | [B7-unreal-camera-port.md](B7-unreal-camera-port.md) | ✅ 三相機全數通過(UE 5.5,HFOV 91.49°/116.81°/80.93° 零誤差,CAM_GEN2 pitch = 反解俯角原數字):腳本 + 鎖檔 json ×3 + 圖解 SOP + 實戰踩坑 |
| **B8 場景就地生成障礙物(石堆/倒木堆)** | [B8-scene-obstacle-placement.md](B8-scene-obstacle-placement.md) | ✅ 紅圈定位法(placement map)+ OBJECT-PLACEMENT 定性句 + 整包光影對齊;含**尺寸錨定法**(治「大一點」震盪)與尺寸迭代實錄 |
| **B9 樹資產重上色(材質特寫參考)** | [B9-tree-trunk-restyle.md](B9-tree-trunk-restyle.md) | ✅ 幾何滲漏根治法:風格參考圖裁成**無幾何材質特寫** + 極短中文 prompt(`不要改變構圖`);含 prompt 鎖形狀二連敗解剖 + 像素鎖備案(Crop-Gen-Paste + 遮罩) |
| **B10 萬聖夜魔森背景(風格 DNA + 衍生圖鎖句)** | [B10-haunted-forest-style-dna.md](B10-haunted-forest-style-dna.md) | ✅ 五層風格拆解 + 母題清單 + 逐字風格鎖句 + 平台路線 + 引擎場景重打光實測(✅ 路線 A);暗黑 low-key horror 風 |
| **B11 月夜 RPG 森林背景(風格 DNA + 衍生圖鎖句)** | [B11-moonlit-jrpg-forest-style-dna.md](B11-moonlit-jrpg-forest-style-dna.md) | ✅ 五層風格拆解 + 母題清單 + 逐字風格鎖句 + 平台路線;明亮夢幻 mid-key JRPG 風(與 B10 反向:暗部深藍通透不塗黑) |
| **B12 跨圖天空移植(圖1 天空換成圖2 天空)** | [B12-sky-transplant.md](B12-sky-transplant.md) | ✅ NB2 雙參考只搬一層:BASE/SKY DONOR 標籤 + 地平線鐵幕 + 樹冠縫隙透空鎖 + 重調色進 BASE 色盤;含天空 UE5 質感 pass(定性句平移)與紅圈畫記編輯搬光源(原開發分支編 B8,合併時改號) |
| **B13 寫實貼圖 → 手繪風格化(style transfer)** | [B13-handpainted-style-transfer.md](B13-handpainted-style-transfer.md) | ✅ 定版 + 七張套圖量產 — v3 定調/v4.2 量產兩段式 + master 色票板庫 + 逐字 prompt + 七次踩坑全歷程(生產區/查詢區雙結構;含成品圖) |

> 之後每拆一個資產(鐵欄杆、墓碑、枯樹…),就在這張表加一列、連到對應的 `*.md`。

## A 系列去背分流(先分兩條思路,再挑配方)

**鐵律:A1/A2 = concept→3D(可重繪、灰底、餵 image-to-3D);A3/A4 = 2D 保真去背(不可重繪、洋紅底、直接當畫面素材)。**

| 案例 | 目的 | 模式 | 底色 | 觸發關鍵字 | 引用 SKILL |
|---|---|---|---|---|---|
| **A1 陵墓** | 單體建築 → 3D 正視板 + 2D 去背 | 1.2 重繪 / 1.1 去背 | 灰 `#808080` / 橘 `#FF6A00` | 陵墓·建築拆件 / 正視參考板 / image-to-3D / 缺席色去背 / 發光彩窗保留 | `asset-cutout` + `ai-media-generator`(concept→3D) |
| **A2 浮雕牆** | 大型場景模組件 → 3D | 1.2 重繪(轉正+de-lit+清場) | 灰 `#808080` | 浮雕牆·牆板·場景模組件 / turnaround 2視圖 / height·displacement map / re-orient 轉正 / multiview-to-3D | `ai-media-generator`(concept-to-3D pipeline) |
| **A3 枯樹拆件** | 多物件 2D 去背 + 補圖(保原像素) | 1.1 edit/inpaint | 洋紅 `#FF00FF` | 去背·退底·扣圖 / 補圖·inpaint / 被遮擋補回 / 緊裁換主角 / 發光裂紋保留 / 殘留手動填色 | `asset-cutout`(模式 1.1) |
| **A4 植被叢** | 植被整叢 2D 保真去背 | 1.1 edit 保真 | 洋紅 `#FF00FF` | 植被叢去背 / dark shrub / 圈選植物 / 3 red circles 分件 / 保原筆觸不重繪 | `asset-cutout` |

> **底色為何不同:** →3D 要 de-lit 中性灰 `#808080`(模型吃純色 ref 穩);2D 去背要「資產缺席色」→ 森林深綠世界用洋紅 `#FF00FF`(綠幕吃綠、灰撞中間調)。A1 陵墓=綠苔+紫窗,兩色都在資產上 → 用橘 `#FF6A00`。

## 固定公式(SOP)

| 公式 | 檔案 | 內容 |
|---|---|---|
| **風格母本重打光(兩段式)** | [SOP-style-relight.md](SOP-style-relight.md) | Phase 1 風格建檔(一次)→ Phase 2 場景重打光(重複):前處理 + 佔位符 prompt 模板 + 驗收 + 失敗分流;叫用詞「照打光公式」 |

## 最新預覽 — A1 陵墓正視參考板

![A1 mausoleum front orthographic](images/mausoleum-front-ortho.png)
