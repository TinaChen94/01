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

## 進行中

- **灰盒模組實驗(未來 B2):** 灰盒 → 夜森林地面模組(master tile)。
  已定案規格:無方向性環境光、無霧、灰盒高度鎖、坎上苔蘚+灌木、
  行走區 = 霧面微潮深色泥土(NOT dry, NOT glossy)。
  關鍵教訓:灰盒要用「高度色標」渲染(淺灰=高台/深灰=行走面)消除高度歧義;
  AI 畫的深度圖 ≠ 3D 算的深度圖(前者高度不可信)。

## 平台操作要點(Leonardo.ai)

- 輸入圖一律滿版無 letterbox;輸出 Dimensions 比例 = 輸入圖比例
- Prompt Enhance 選 None、Style 選 None(避免改寫鎖句/疊色調)
- 細節 pass 用 Nano Banana 2;保真放大用 Universal Upscaler 2× 最低 creativity
