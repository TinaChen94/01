# 實戰紀錄 — B7 三相機 → Unreal 重現(相機1 ✅)

> 目標:[B6](B6-three-camera-pipeline.md) 的三相機(遊戲/出圖/生成)在 Unreal
> 裡重現**逐像素相同的鏡頭畫面**。第一階段先做相機1(遊戲相機)。
> 路線:數值直搬(確定性轉換),不走 FBX 相機匯入(filmback 常被改寫)。
> B6 在分支 `claude/b2-greybox-experiment-fgsc06` 上。

**🔑 關鍵字:** `B7`、`Unreal 相機`、`UE 相機`、`CineCamera`、`filmback`、
`相機搬 UE`、`Blender 轉 Unreal`、`座標系轉換`、`FOV 水平垂直`

## 狀態

- ✅ **相機1 實機驗收通過**(2026-07-11,UE 5.5)— Blender→UE 轉換路線成立
- 階段:①相機1 ✅ → ②相機2(待做)→ ③相機3 CAM_GEN2(待做)

## 工具(已入庫)

| 檔案 | 跑在哪 | 做什麼 |
|---|---|---|
| [`tools/unreal-camera-port/blender_cam_export.py`](../../tools/unreal-camera-port/blender_cam_export.py) | Blender Text Editor | 讀相機 `matrix_world`(B6 踩坑 #4:多層 rig 不抄面板)+ Sensor Fit 展開,轉 UE 座標,寫出 `cam_unreal.json` |
| [`tools/unreal-camera-port/unreal_cam_import.py`](../../tools/unreal-camera-port/unreal_cam_import.py) | UE Python(Output Log → Cmd 切 Python) | 讀 json 生成 CineCameraActor,filmback/focal 照抄、位姿套用、關景深 |

### cam_unreal.json 是什麼

兩支腳本之間的**交接檔**:Blender 和 Unreal 是獨立軟體,腳本不能直接對話,
所以 Blender 端把「重建這顆相機需要的所有數字」打包成一個 JSON,
UE 端腳本照單全收建出一模一樣的相機。

```
Blender(有相機1的場景)                Unreal(空關卡)
blender_cam_export.py  →  cam_unreal.json  →  unreal_cam_import.py
       (寫出)              (同機路徑/隨身碟)        (讀入,照著建相機)
```

裡面裝什麼(全部是**已轉換成 Unreal 格式**的值):

| 欄位 | 內容 | 例子 |
|---|---|---|
| `focal_mm` | 焦距 | 13.46 |
| `sensor_mm` | 有效 sensor 寬高(Sensor Fit 已展開) | 27.64 × 15.5475 |
| `location_cm` | 相機世界位置(已做 Y 鏡像 + 公尺→公分) | 如 [0, 1000, 500] |
| `rotator_deg` | UE 的 pitch/yaw/roll(已從 Blender 旋轉反解) | 如 pitch −20 |
| `fov_deg` | 換算出的水平/垂直 FOV — 給 UE 面板**驗算**用 | 91.51 / 60.02 |
| `resolution`、`clip_m`、`name` | 解析度、裁剪距離、相機名 | 紀錄與命名用 |

它幫你避開的坑:相機1 掛在 Unity 匯入的多層 rig 裡(B6 踩坑 #4),
面板顯示局部座標,手抄必錯;座標系轉換(右手→左手、公尺→公分)與
Sensor Fit 展開也容易算錯方向——全部由匯出腳本算好、凍結在 JSON 裡,
**不手抄任何數字**。

檔案位置:執行 Blender 腳本後存在 **.blend 檔旁邊**(同資料夾)。
Blender 與 Unreal 不在同一台機器時,複製這個 JSON 過去即可——
它是純文字的「相機身分證」,記事本也能開。

## 相機1 參數與換算

Blender 端(來源:B6 `b6-cam1-lens.png`):

| 項目 | 值 |
|---|---|
| Focal Length | 13.46 mm |
| Sensor | 27.64 mm,Sensor Fit = **Auto** |
| Resolution | 1920×1080(16:9,Auto → 27.64 吃橫向) |
| 有效 sensor | **27.64 × 15.5475 mm**(27.64 × 1080/1920) |
| 水平 FOV | 2·atan(13.82/13.46) = **91.51°** |
| 垂直 FOV | **60.02°** ≈ Unity 標準 vFOV 60° ← 佐證這顆確實是 Unity 遊戲相機 |
| Clip | 0.3 – 200 m |

Unreal 端(CineCameraActor)——**照抄,不換算**:

| CineCamera 欄位 | 值 |
|---|---|
| Filmback → Sensor Width | 27.64 mm |
| Filmback → Sensor Height | 15.5475 mm |
| Current Focal Length | 13.46 mm |
| Current Aperture | 22(縮小光圈)+ Focus Method = Disable(關景深) |
| 驗算 | 細節面板 Current FOV 應顯示 ≈ 91.5°(UE 的 FOV 是**水平**) |

> ⚠️ 別用普通 Camera Actor 的 FOV 欄位對數字:UE 的 FOV 定義是**水平**、
> Unity 是**垂直**,「都填 60」會差一大截。CineCamera 走 filmback+focal
> 這條路完全繞開 FOV 定義差異 —— 與 B6 的結論同源:焦距永遠跟 sensor
> 成對決定視角,照抄整對就零誤差。

## 座標系對照(為什麼是 x, −y, z ×100)

| | 手性 | Up | 單位 | 相機朝向 |
|---|---|---|---|---|
| Blender | 右手 | Z | m | 局部 −Z(up = 局部 +Y) |
| Unity | 左手 | Y | m | 局部 +Z |
| Unreal | 左手 | Z | cm | 局部 +X(rotator:pitch/yaw/roll) |

- Blender → UE:**(x, y, z) → (x, −y, z)**,位置 ×100。一個 Y 鏡像補齊
  右手↔左手差,這也正是 Blender 預設 FBX 匯出 → UE 預設匯入對 mesh 做的事,
  所以**相機(本腳本)與模組 mesh(FBX)各走各的路,到 UE 會重合**。
- Rotator:yaw/pitch 從 forward 向量反解,roll 從 up 對比「無滾轉 up」取角
  (已用已知位姿驗算:朝 −Y 俯 20° → yaw −90° / pitch −20° / roll 0 ✓)。
  Unity rig 帶滾轉也照搬,不假設 roll = 0。

## SOP(相機1)

1. **Blender**:開 B6 場景 .blend → 確認 scene camera = 相機1(或在腳本
   `CAM_NAME` 填名字)→ Text Editor 執行 `blender_cam_export.py`
   → 得 `cam_unreal.json`(在 .blend 旁)
2. **Blender**:相機1 渲一張 1920×1080 灰盒基準圖(驗收用)
3. **模組進 UE**:同一個 .blend 選模組全部 mesh(主體+前緣條,B6 踩坑 #5)
   → File → Export → FBX(勾 Selected Objects,其餘**預設**)→ UE 匯入
   (Import Uniform Scale = 1,擺在原點、零旋轉——mesh 的世界位置已烙在 FBX 裡)
4. **UE**:啟用 Python Editor Script Plugin → 改 `unreal_cam_import.py` 的
   `JSON_PATH` → Output Log 執行 → 生成 `CAM1_GAME`(以 json 裡的相機名為準)
5. **UE**:右鍵 CineCameraActor → Pilot,或開 Cinematic Viewport;
   CineCamera 預設 Constrain Aspect Ratio = On,黑邊即 16:9 取景框
6. **驗收(B6 鎖檔法)**:High Resolution Screenshot 1920×1080 →
   PS 疊到步驟 2 的 Blender render 上 50% 透明度,灰盒梯形四邊應幾乎重合
   (誤差個位數像素)。重合即鎖檔,再繼續相機2/3。

## 相機1 實測紀錄(2026-07-11 定案值)

json 定案值(比面板的四捨五入值更精確,以此為準):

| 項目 | 定案值 | UE 端實測 |
|---|---|---|
| focal | **13.4622 mm** | Current Focal Length 13.4622 ✓ |
| 有效 sensor | **27.6352 × 15.5448 mm** | Filmback 同值,Aspect 1.777778 ✓ |
| location(UE cm) | **[150.0, −2035.964, 93.312]** | Transform 同值 ✓ |
| rotator | **pitch −24.0° / yaw 90° / roll 0** | Rotation (0, −23.9999, 90) ✓(UE 顯示順序 Roll/Pitch/Yaw) |
| 水平 FOV | 預測 91.49° | **Current HFOV 91.492805** ✓ 零誤差 |

畫面驗收:UE Pilot 視角與 Blender 基準圖構圖相符,通過。
rotator 數字乾淨(整數 −24°/90°)= `matrix_world` 正確攤平了六層 rig。

### 解析度插曲(重要觀念)

第一次匯出 json 時場景 Resolution 是 4096×2286(配合 5504×3072 成品圖比例),
垂直 FOV 算出 59.61° ≠ 遊戲的 60°。改回 1920×1080 重跑才定案。

- **水平視野跟解析度無關**(Auto fit 橫向吃 sensor,永遠 91.49°),
  比例只影響直向多看/少看一點
- **素材不同永遠不需要動相機**(透視不住在貼圖裡,B6 心法):
  json 只在「換相機」時才多一份,最終就是相機1/2/3 各一份,鎖檔沿用
- 5504×3072(1.7917)那個比例屬於**相機3 的反解畫布**,輪到相機3 再用
- 鐵則:驗收時渲圖、json、截圖三處**同一顆相機同一個比例**

## 實戰踩坑(相機1 這輪實際遇到)

| # | 現象 | 根因 | 解法 |
|---|---|---|---|
| 1 | 填 `CAM_NAME` 時不知道填哪個 | rig 六層鏈:`[System]→CameraSystem Variant→MainCamera→WorldAnchor→LocalAnchor→Camera`,且相機**資料塊**也叫 MainCamera(綠色圖示)跟第三層空物件撞名 | 填**物件**名 `Camera`(橘色圖示、倒數第二層);絕不填 `MainCamera` |
| 2 | json 的 name 變 `Camera.001` | 操作中誤複製出第二顆相機(位姿相同故數據無害) | Outliner 搜 Camera 刪複製品;渲基準圖前確認 scene camera 與 json 同一顆 |
| 3 | 從網頁另存腳本變 `.py.txt` | Windows 自動加副檔名 | Blender 端無所謂(只看內容);**UE 端執行檔案必須是 `.py`** — 檔案總管開「顯示副檔名」後 F2 改名 |
| 4 | Text Editor 沒有 ▶ 按鈕 | 編輯器區塊太窄,按鈕被擠出畫面 | 用 **Text 選單 → Run Script**(等效)或 Alt+P |
| 5 | UE 貼整段腳本報 `Could not load Python file '# unreal_cam_import.py'` | UE Python 輸入列看到內容含 `.py` 字樣,把整段輸入當**檔名**去載入(console 怪癖) | 不貼內容,改成在 Python 模式直接輸入**腳本檔完整路徑**執行:`C:/.../unreal_cam_import.py` |
| 6 | `HighResShot` 報 SyntaxError | 輸入列還在 Python 模式 | **Cmd 模式吃引擎指令、Python 模式吃程式碼**,拍圖前切回 Cmd:`HighResShot 1920x1080` |
| 7 | 視口紅字 Video memory exhausted | 測試關卡帶 Landscape+體積雲,顯存超支 | 驗收用 Empty/Basic Level 重建(模組+相機 30 秒重生);高解析截圖前尤其要處理,否則可能破圖 |

### UE 端操作備忘

- 截圖指令(Cmd 模式、Pilot 中):`HighResShot 1920x1080`,
  存到 `<專案>\Saved\Screenshots\WindowsEditor\HighresScreenshot0000N.png`(取最大編號)
- Pilot 中**不可用 WASD/滑鼠飛行** — 那會直接搬動相機本體;誤動 → 退出 Pilot、Ctrl+Z,或重跑腳本重生
- 按 G(Game View)藏圖示再截圖
- `Aspect Ratio Axis Constraint = Maintain X-Axis FOV` 是正確預設(對應 Blender Auto fit 橫向吃 sensor),不用動

## 預防踩坑(照 B6 經驗預埋)

| # | 風險 | 預防 |
|---|---|---|
| 1 | Unity rig 多層父子鏈,面板是局部座標(B6 #4 同源) | 腳本讀 `matrix_world`,不手抄 |
| 2 | 相機與 mesh 走不同轉換路徑 → 對不上 | mesh 走 Blender 預設 FBX → UE 預設匯入;相機走本腳本;兩者同一個 Y 鏡像 |
| 3 | UE 景深把畫面糊掉,誤判「對不上」 | 腳本已關 Focus + 光圈 22 |
| 4 | 拿普通 Camera 的 FOV 欄對 Unity 的 60 | 只用 CineCamera filmback+focal |
| 5 | 視口比例不是 16:9,構圖看起來不同 | Pilot + Constrain Aspect Ratio;驗收一律用 1920×1080 截圖 |
| 6 | rig 帶負縮放(鏡像)→ forward/up 反向 | 匯出腳本會偵測並警告;渲出來顛倒就回報處理 |
| 7 | UE 全域近裁剪(預設 10cm)吃掉超近物 | 相機1 clip start 0.3m=30cm,不受影響;若之後要更近,改 Project Settings → Near Clip Plane |

## 待辦

- [x] 相機1 實機走一輪 SOP → 驗收通過(2026-07-11;定案值見「相機1 實測紀錄」節)
- [ ] 相機1 嚴格鎖檔(選配):PS 50% 疊圖量化誤差(目前為目測相符);
  乾淨 Empty Level 重建一份,解掉顯存警告
- [ ] 相機2:同 focal 13.46,filmback 直接吃 43.77 × 24.62(B6 已算好的
  Sensor Fit=Vertical 那組)——UE 不用管 Sensor Fit,寬高照填就是那個視野
- [ ] 相機3(CAM_GEN2):21.10mm + 5504×3072 畫布 → filmback 36 × 20.09
  (36 × 3072/5504);先確認 CAM_GEN2 的 sensor 設定再定案
- [ ] 三顆都鎖檔後:把 UE 端截圖與對照結論回填本篇,狀態轉全 ✅
