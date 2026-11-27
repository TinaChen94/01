# EnvCube 環境貼圖工具(本機網頁版)

> 對應案例:[A13〈EnvCube 建議〉](../../docs/asset-cases/A13-trap-props-saw-spike.md) —— Unity 不受光(Unlit)shader 的金屬光澤只能靠 EnvCube 反射。

## 檔案

| 檔案 | 用途 |
|---|---|
| `envcube-tool.html` | 本機網頁工具:下載後**雙擊用 Chrome / Edge 打開**,不用網路、不用安裝,檔案不上傳 |
| `EnvCubeImporter.cs` | Unity 自動匯入腳本:放進 `Assets/Editor/`,檔名含 `envcube` 的 PNG 自動設成 Cube + 正確 Mapping |

## 最簡單用法(3 步,小白版)

1. 打開 `envcube-tool.html`,把**一張場景截圖**拖進第 1 格(遊戲畫面、Unity Scene 截圖都可以;截圖周圍的白邊 / 介面條會自動裁掉)。
2. 第 2 格選金屬感覺:**拉絲 / 霧面**(推薦)或**亮面**。
3. 第 3 格按「下載環境貼圖(2:1)」→ 拖進 Unity → 放進材質的 Cube 欄位 → CustCube Scale 先設 0.3。

原理:直接把截圖包成一圈 360° 環境(背面用鏡射接起來、不會有接縫),再做「金屬對比」處理:只調整明暗(亮處更亮、暗處更暗),每個像素的顏色不變,最後把整體平均色調還原成截圖的色調 → 對比變強但場景色調不跑;滑桿「金屬對比」越高越強烈。不需要懂光源設定;下方「進階設定」不開也沒關係。

## 進階設定用法

1. **來源**(擇一或混用)
   - 「套用預設:哥德大廳(A13)」:暖色吊燈、四扇藍色彩窗、一圈火把、深色地面。
   - 拖入**場景截圖** →「從截圖自動抓光源」:抓最亮的幾個區域當光源、上中下色帶當天空 / 地平線 / 地面漸層;可選「光源鏡射到背後」。
     截圖裡看不到光源(只有地面反光)時,抓到的會是地面亮點,建議改用預設再手調。
2. **手調**:每個光源可改方位、仰角、大小、強度、顏色,也能新增 / 刪除;漸層三色可改。
3. **金屬粗糙度**:0 = 亮面(中心鐵圈、刃口),0.5 以上 = 拉絲 / 霧面(銅盤,推薦先用)。
4. **反射預覽**:用滑桿調 CustCube Scale、Base Decay Ratio、Color(HDR)、頂點色 Alpha,即時看金屬球效果;右下會產生對應的 Unity 設定文字。
   預覽公式是從面板標籤推測:`底色 × Color × (1 − Decay × Scale × Alpha) + 環境 × Scale × Alpha`,以 Unity 實際畫面為準。
5. **輸出**:下載 2:1 經緯圖(`envcube_latlong_*.png`)或鏡面球(`envcube_ball_*.png`)。

## Unity 匯入

- **有裝 `EnvCubeImporter.cs`**:把下載的 PNG 拖進專案就自動設好(`_latlong` → Cylindrical、`_ball` → Spheremap、Fixup Edge Seams、sRGB、Max 1024)。舊檔右鍵 → Reimport。
- **沒裝**:Texture Shape = Cube;Mapping 依檔案選 Latitude-Longitude 或 Mirrored Ball;勾 Fixup Edge Seams;Apply。

## 注意

- 平面 quad 法線都一樣 → 反射只會是一片單色;EnvCube 要用在有倒角的 3D 模型上。
- 主貼圖用不帶高光的版本,避免雙重高光。
- 切到 shader 變亮:先把 CustCube Scale 拉到 0 確認,再從 0.3 往上加。
