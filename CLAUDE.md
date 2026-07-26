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
- **B6** — 三相機管線(遊戲/出圖/生成相機解耦、反解相機 homography、
  品質三資源);B7 的上游,B4/B5 在 `claude/b2-greybox-experiment-fgsc06` 分支
- **B8** — 場景就地生成障礙物(石堆/倒木堆):紅圈定位法(placement map)、
  OBJECT-PLACEMENT 定性句、整包光影對齊、**尺寸錨定法**(治「大一點」尺寸震盪)

## 進行中

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
