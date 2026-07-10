# 實戰紀錄 — B7 三相機 → Unreal 重現(🚧 實驗中)

> 目標:[B6](B6-three-camera-pipeline.md) 的三相機(遊戲/出圖/生成)在 Unreal
> 裡重現**逐像素相同的鏡頭畫面**。第一階段先做相機1(遊戲相機)。
> 路線:數值直搬(確定性轉換),不走 FBX 相機匯入(filmback 常被改寫)。
> B6 在分支 `claude/b2-greybox-experiment-fgsc06` 上。

**🔑 關鍵字:** `B7`、`Unreal 相機`、`UE 相機`、`CineCamera`、`filmback`、
`相機搬 UE`、`Blender 轉 Unreal`、`座標系轉換`、`FOV 水平垂直`

## 狀態

- 🚧 **實驗中** — 腳本已備,待在實機 Blender + Unreal 走一輪驗收
- 階段:①相機1(本篇)→ ②相機2 → ③相機3(CAM_GEN2)

## 工具(已入庫)

| 檔案 | 跑在哪 | 做什麼 |
|---|---|---|
| [`tools/unreal-camera-port/blender_cam_export.py`](../../tools/unreal-camera-port/blender_cam_export.py) | Blender Text Editor | 讀相機 `matrix_world`(B6 踩坑 #4:多層 rig 不抄面板)+ Sensor Fit 展開,轉 UE 座標,寫出 `cam_unreal.json` |
| [`tools/unreal-camera-port/unreal_cam_import.py`](../../tools/unreal-camera-port/unreal_cam_import.py) | UE Python(Output Log → Cmd 切 Python) | 讀 json 生成 CineCameraActor,filmback/focal 照抄、位姿套用、關景深 |

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

- [ ] 相機1 實機走一輪 SOP → 疊圖驗收 → 鎖檔(通過後本篇轉 ✅)
- [ ] 相機2:同 focal 13.46,filmback 直接吃 43.77 × 24.62(B6 已算好的
  Sensor Fit=Vertical 那組)——UE 不用管 Sensor Fit,寬高照填就是那個視野
- [ ] 相機3(CAM_GEN2):21.10mm + 5504×3072 畫布 → filmback 36 × 20.09
  (36 × 3072/5504);先確認 CAM_GEN2 的 sensor 設定再定案
- [ ] 三顆都鎖檔後:把 UE 端截圖與對照結論回填本篇,狀態轉 ✅
