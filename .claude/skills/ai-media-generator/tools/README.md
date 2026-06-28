# 美術管線工具 (Art Pipeline Tools)

兩支單檔網頁工具，搭配 `ai-media-generator` 的「深度圖控制打光」流程使用。
完整工作流見 [../references/depth-relight-pipeline.md](../references/depth-relight-pipeline.md)。

> 來源：使用者自製/提供的工作流工具，收錄於此作為可複用資產。

---

## 1. `depth-relight.html` — 深度圖 3D 打光工具

把一張灰階 **depth map** 擠成 2.5D 浮雕，用三點燈(主光/補光/邊光)即時打光，
輸出「打好光的灰階控制圖」，當作 Nano Banana 的**光影姿勢參考**。

**用法：**
1. 瀏覽器開啟此檔
2. 右上「載入深度圖」選一張 **1:1** 的 depth map（用 prompt-copier 的 Depth Map prompt 生）
3. 左邊雷達盤拖動 K/F/R 三盞燈調光向；右邊調幾何參數
4. 「下載截圖」存成 2048 PNG

**參數速記：**
| 參數 | 作用 | 物件預設 | 場景建議 |
|---|---|---|---|
| 深度強度 Depth | 浮雕高度 | 26–45 | **調低**(避免前後景拉爆) |
| 立體銳利度 Sharpness | 法線對比 | 5–6 | 同 |
| 背景剔除 Cutoff | 丟掉暗部當背景 | 0.05 | **設 0**(場景暗部是內容) |
| 邊緣透明度 Edge Fade | 邊界羽化 | 10 | 同 |
| 鏡頭透視 | Ortho/15°/45° | Ortho | Ortho |

**限制：** 它是**單張高度場(2.5D)**，不是真 3D。淺景深/正面場景好用；
深景深(近物+遠景分離大)會把前後拉成一片 → 深場景請當「光向控制圖」餵 NB，別當最終算圖。

## 2. `prompt-copier.html` — 美術 Prompt 卡片庫

一鍵複製常用 game-art prompt：多重參考融合(風格/光影/姿勢分離)、Depth/AO/ID map、
三視圖、素模、背面、PVC、九宮格、高清、動漫轉真人、光影強化等。

> 卡片縮圖讀 `images/` 夾(此處未附)，缺圖會自動顯示佔位圖，不影響複製功能。

---

## 依賴 / 離線

`depth-relight.html` 從 CDN 載入 three.js r128 + OrbitControls，**需連網**才會顯示 3D。
要離線使用：下載 three.min.js 與 OrbitControls.js 放同目錄，把 `<script src=...>` 兩行
改成本地相對路徑即可。
