# EnvCube 環境貼圖工具(本機網頁版)

> 對應案例:[A13〈EnvCube 建議〉](../../docs/asset-cases/A13-trap-props-saw-spike.md) —— Unity 不受光(Unlit)shader 的金屬光澤只能靠 EnvCube 反射。

## 檔案

| 檔案 | 用途 |
|---|---|
| `envcube-tool.html` | 本機網頁工具:下載後**雙擊用 Chrome / Edge 打開**,不用網路、不用安裝,檔案不上傳 |
| `EnvCubeImporter.cs` | Unity 自動匯入腳本:放進 `Assets/Editor/`,檔名含 `envcube` 的 PNG 自動設成 Cube + 正確 Mapping |

## envcube-tool.html 用法

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
