# 專案說明

遊戲美術資產的 AI 生成實驗 repo:灰盒(greybox)→ game art background、
資產拆解/去背、4K 放大與細節增強管線。

## 實戰紀錄(重要 — 先讀索引)

所有驗證過的管線、逐字 prompt、鎖句字典、踩坑教訓都記錄在:

- **索引:** [docs/asset-cases/README.md](docs/asset-cases/README.md)
- **A1** — 哥德陵墓:概念圖拆資產/去背/正交參考板
- **B1** — 夜霧森林背景:4K 放大 + 地面材質細節管線(Leonardo Universal
  Upscaler 2× + Nano Banana 2 材質保真 pass;含鎖句字典與平台設定表)

使用者說「B1」「照 B1 配方」「鎖句字典」等,即指這些紀錄 — 先讀對應檔案再回答。

## 命名慣例

- `A*` = 資產拆解/去背案例;`B*` = 背景/模組生成管線案例
- 新案例:在 `docs/asset-cases/` 加 `<編號>-<slug>.md` 並更新索引表
- 案例圖檔放 `docs/asset-cases/images/`,檔名前綴對應編號(如 `b1-*.png`)

- **B2** — 灰盒 → 夜森林地面模組(master tile):貼材質灰盒管線
  (貼圖烙分佈 → NB2 圖案活化 → 頂光 polish → PS 收邊);
  三路線成敗對照(NB2 幾何滲漏 / SD 畫布填滿症 / 貼材質正解)
- **B4** — master 貼圖 → 套圖變體道路縫合(同圖材質替換):區域編輯鏈、
  套圖三規則、直路兩路線攻防、端頭版、零變化除錯、四方連續 SOP
- **B5** — master 主題翻譯:森林→雪地三檔位(薄雪/厚雪/冰殼):
  鎖分層(大形鎖/小形授權)、鏈要短(調色歸 PS 預設)、色票板配比
- **B6** — 三相機管線(遊戲/出圖/生成相機解耦、反解相機 homography、
  品質三資源);B7 的上游、B4/B5 的產出源
- **B8** — 場景就地生成障礙物(石堆/倒木堆):紅圈定位法(placement map)、
  OBJECT-PLACEMENT 定性句、整包光影對齊、**尺寸錨定法**(治「大一點」尺寸震盪)
- **B10** — 萬聖夜魔森背景:風格 DNA 五層拆解 + 母題清單 + 風格鎖句 +
  引擎場景重打光實測(✅ 路線 A 一次過)
- **B11** — 月夜 RPG 森林背景:明亮 mid-key 風格 DNA + 葉團渲染理想 +
  體積兩 pass(樹幹細節/葉團分開跑)+ PS 合成回引擎資產卡
- **B14** — 半寫實暗黑森林地面:UE5/Megascans 質感風格 DNA + 母題清單 +
  風格鎖句(B10/B11/B14 三風格速記:手繪插畫/動漫/半寫實 render;材質分流)
- **B12** — 跨圖天空移植(只搬一層):BASE/SKY DONOR 標籤 + 地平線鐵幕 +
  樹冠縫隙透空鎖 + 重調色進 BASE 色盤;附天空 UE5 質感 pass、紅圈畫記編輯搬光源
  (原開發分支編 B8,合併時 B8~B11 已被佔用故改號 B12)
- **SOP 打光公式** — `docs/asset-cases/SOP-style-relight.md`:
  Phase 1 風格建檔(一次)→ Phase 2 場景重打光(重複)。
  使用者說「照打光公式」「打光公式」「風格建檔」即指此 SOP — 先讀檔再動手。

## 進行中

- **B13 — 寫實貼圖 → 手繪風格化(style transfer):✅ 定版 + 七張套圖量產**
  (Ruined King 級厚塗;v3 定調 + v4.2 量產兩段式,master 色票板庫)。
  完整配方/七次踩坑/成品圖在
  `docs/asset-cases/B13-handpainted-style-transfer.md`(此分支新增;
  main 已有他人的 B8,故編為 B13);待辦:Match Color、驗縫、引擎 3×3 驗收。
- **B7 — 三相機 → Unreal 重現:✅ 三相機全數通過**(UE 5.5,數值直搬
  零誤差)。腳本與鎖檔 json ×3 在 `tools/unreal-camera-port/`,
  定案值/SOP/踩坑在 `docs/asset-cases/B7-unreal-camera-port.md` —
  日後在任何 UE 專案重現,跑 import 腳本指向 locked/ 的 json 即可。
- **B2 待辦:** 引擎投影最終驗收 → 通過後量產橫/直/十字/T 套圖
  (同配方同 prompt 三連);B1 穩定度矩陣「模組成品」格同時補上。
  關鍵教訓已收進 B2:幾何滲漏、像素預算(Crop-Gen-Paste)、
  頂光 = 立體感+可旋轉兩全、AI 畫的深度圖不可信。

## 平台操作要點(Leonardo.ai)

- 輸入圖一律滿版無 letterbox;輸出 Dimensions 比例 = 輸入圖比例
- Prompt Enhance 選 None、Style 選 None(避免改寫鎖句/疊色調)
- 細節 pass 用 Nano Banana 2;保真放大用 Universal Upscaler 2× 最低 creativity
