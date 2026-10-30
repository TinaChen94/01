# 實戰紀錄 — C2 正式貼圖 → 單張 Combined Bake(古堡打光二版,Blender 自動化)

> 接續 [C1](C1-blender-modular-bake-pipeline.md)(灰模驗接縫)。同事交來**正式貼圖**:6 種模組共 19~20 個物件,
> 做成**共用的複合材質球**、貼圖用 UV1 重複平鋪。任務:重調燈光 → bake 驗證模組相接 →
> 因**引擎每個物件只能放一張貼圖、不能即時反射**,最終交付「同事貼圖 + 打光 + 反光」合成的**單張 FINAL 貼圖**。
>
> **本篇範圍(C2)**:從「燈光依模組分類整理」到「SM_TURN_A_HIGH2 正式算的腳本」。
> 之後的地板 36 塊分層烘焙 + PS 合成 + AI 細節對燒另篇(C3)待補。

- **Claude 對話連結:** `https://claude.ai/code/session_01BEBwyiUGGcpDC64eDLhAJs`
- **全紀錄 — 原始整理檔:** C201.docx / C202.docx(使用者整理,Q16 ~ Q2113 討論原文 + 腳本 + Gemini 解說;線上版連結待補)

**🔑 關鍵字:** `C2`、`Combined bake`、`FINAL 貼圖`、`單張貼圖`、`一物件一張圖`、`共用材質 bake`、
`__BAKE_TARGET__`、`暫時相機`、`Active Camera`、`EYE_HEIGHT`、`final_ver`、`VERSION`、`bake_res`、
`Pack Islands Concave`、`8192`、`試算`、`切換檢查`、`TURN`

## 狀態

- ✅ **古堡二版打光定案**:Combined + Glossy(View From = Active Camera,暫時相機在模組中央眼高 1.7 m),
  VERSION 3 全部模組 bake 完成;TURN(8192)以指定腳本先試算、再正式算。
- ✅ 清晰度一致:全部模組 14.6~16.8 px/m(最大差 1.15 倍;原本 3.1~14.9,差 5 倍)。
- ⬜ AO 腳本做好但最後沒用;EXR → 引擎格式輸出、地板材質對牆面反光的影響待討論(見待辦)。
- 整理日期:2026-10-30

---

## 0. 跟 C1 差在哪

| | C1 灰模驗接縫 | C2 正式貼圖 |
|---|---|---|
| 材質 | 全換中性灰,每組一顆 BAKE_ 材質 | **保留同事的共用材質**(牆、地板顏色影響反彈光,用真實材質才準) |
| 怎麼 bake 進共用材質 | 每組一顆專屬材質 | bake 前在**共用材質**裡暫時塞 `__BAKE_TARGET__` 圖片節點,逐物件換圖、bake 完刪除,材質還原 |
| Bake Type | Diffuse(Color 關)純光影 | 驗接縫階段同 C1;**交付用 Combined**(貼圖 + 光影 + 反光) |
| 預覽 | 改材質接 Emission | **物件層材質槽**(`slot.link = 'OBJECT'`)蓋一顆 Emission 預覽材質,同事材質完全不動;切回 `DATA` 就還原 |
| 解析度 | 表面積 × 假設 60% UV 用量 | **量實際 UV 面積**算,以 256 為單位,上限放到 8192 |
| 進度 | 手動按 Bake | 進度寫在物件自訂屬性,分批 / 一次一個 / 可續跑 |

---

## 1. 前置

### 1.1 燈光整理(對話 Q16)

- 同類燈(例如所有壁火)要一樣亮 → 全選,最後 Ctrl+點一盞調好的 → **Ctrl+L → Link Object Data**,
  之後改一盞全部跟著變。這是「燈光套件化」第一步,保證每個模組的燈一致,接縫才不會因燈亮度不同而對不上。

### 1.2 開工前三件事(對話 Q1701、Q1702)

| 做什麼 | 為什麼 |
|---|---|
| **另存副本**(例如 `..._bake_verify.blend`),確認標題列是新檔名 | 腳本會新增 UV、改 Render 設定、**自動 Ctrl+S**;開原檔跑會直接存進同事的檔案 |
| Face Orientation 檢查反面 | C1 時 VA、TURN 大量反面,bake 全黑 |
| World Strength = 0、曝光固定;記下原本 Max Samples | 只看室內燈;腳本會覆蓋 Render 設定 |

### 1.3 同事已有兩套 UV,能不能直接拿來 bake?(對話 Q1901)

- 同事模型有 `map1`(相機圖示,貼圖用,超出方格平鋪)與 `UVMap`(可能是 lightmap UV)。
- 檢查:UV Maps 點 `UVMap` 反白(相機圖示留在 map1)→ UV Editing → Tab → A → **Select → Select Overlap**。
- 結果:**有重疊也超出方格 → 不能用**,照原做法新增第三套 `BakeUV`。同事兩套 UV 都不動。

| UV | 用途 | 會被改嗎 |
|---|---|---|
| map1(相機圖示) | 同事貼圖 | ❌ |
| UVMap | 同事第二套 | ❌ |
| BakeUV(新增) | bake 用,不重疊 | 腳本新增 |

---

## 2. 檢查腳本:UV 用量與解析度(v1 → v2 → v3)

**目的**:bake 前先確認每個模組清晰度一致,不用等 20~30 分鐘 bake 完才發現某個模組糊掉。
只新增 UV2、印報表、(v2 起)寫 `ob["bake_res"]`,不 bake、不改材質。

### v1 → 抓到大問題(對話 Q1801、Q1902)

| 模組 | UV 用量 | px/m |
|---|---|---|
| HA_Aa / HA_Ab | 33~34% | 14.9 |
| VA 系列 | 13~19% | 6.7~8.3 |
| L_HA | 12% | 8.6 |
| **TURN** | **3%** | **3.1** |

- 原因:哥德拱圈、圓頂環這類**彎曲長條零件**,Smart UV 用外框方塊排列 → 外框大、實際面積小,空間浪費。
- 清晰度差 5 倍 → TURN 會一邊清楚一邊糊,接縫無從判斷。

### v2 解法(對話 Q1902)

1. **Pack Islands `shape_method='CONCAVE'`**:依零件實際形狀互相嵌合,彎曲長條塞進彼此空隙。
2. **解析度改用實際 UV 用量算**(numpy 量 UV 多邊形面積):`res = DENSITY × √(表面積 / UV用量)`,以 **256 為單位**(不再限 2 的次方),夾在 MIN/MAX。

### v3 分批 + 自動降級(對話 Q1904、Q1905)— **定案** `00_check_uv_res.py`

- v2 一次排 19 個,Concave 太吃資源,Blender 當掉。
- v3:每次 `BATCH = 2` 個、**每個前後都存檔**;進度存 `ob["uv_done"]`、`ob["uv_try"]`。
- **自動降級**:同一模組上次處理到一半當掉,下次自動換輕的排法:`CONCAVE → CONVEX → 不重排(只 Smart UV)`。
- 共用同一份 mesh 的物件一起標記完成。

### 結果與上限調整(對話 Q1906、Q1907)

| 模組 | MAX 4096 時 | **MAX 8192(定案)** |
|---|---|---|
| HA 系列(12 個) | 41~44% / 16.6~16.8 px/m | 2048 / 16.6~16.8 |
| VA 系列(5 個) | 31~35% / 15.7~16.4 | 2816~3328 / 15.7~16.4 |
| L_HA(2 個) | 26~27% / 12.8~13.2 | 4864~5120 / 15.6~16.0 |
| TURN(4.6 萬 m²) | 15% / **7.3** ❌ | **8192 / 14.6** |

- 改 `MAX_RES` 後重跑**只重算解析度**(UV 已完成),幾秒跑完;小模組維持原尺寸,只有撞上限的大模組自動往上開。
- 8192 float 圖約 1 GB 記憶體;32 GB 以下可改 6144(TURN 約 11 px/m)。
- L_HA、TURN 仍標「UV 用量偏低」= 圖裡空白多,解析度已補上,可忽略。

### 判斷是否當掉(對話 Q1904)

- 開 **Window → Toggle System Console**,每個模組印一行;TURN 一行可能等 10 分鐘以上。
- 工作管理員看 blender.exe 的 CPU:有跳動 = 在算;**持續 0% 超過 5 分鐘且 Console 無新訊息** = 可能當掉。
- 「沒有回應」、畫面不能點都是正常的。
- ⚠️ **不要點 Console 黑視窗**:會進入「選取」模式把 Blender 暫停;標題出現「選取 / Select」就按 Esc。
- 真當掉:Console 按 Ctrl+C;再不行就工作管理員結束,重開再跑(已存的進度不會丟)。

---

## 3. Bake 路線演進(怎麼走到 Combined + 暫時相機)

| 階段 | 做法 | 結果 / 為什麼換 |
|---|---|---|
| ① 腳本 A + B(Q1702~Q1908) | Diffuse(Color 關)純光影 bake 進 `BAKE_*.exr`;B 的 `VIEW` 只顯示光影 | ✅ 驗接縫最準:幾節亮度連續,暖色壁火與冷色窗光節奏一致 |
| ② 腳本 B v2/v3 `COMBINED` 預覽(Q2001~Q2104) | 複製同事材質,`底色貼圖 × 光影 (× AO)` 接 Emission | ❌ 偏平偏亮、旗子過紅:只抓到底色,同事節點群組(Shader_ENV)裡的暗化/AO/調色全被跳過;沒有反光 |
| ③ 腳本 C:AO(Q2102~Q2103) | 另外 bake 幾何 AO 乘進去 | 做好但最後沒用(Combined 本身已含遮蔽) |
| ④ 釐清引擎限制(Q2105) | **每個物件只能放一張貼圖、不能即時反射** | 同事貼圖是多模組共用平鋪 → 光影無法寫進共用貼圖 → 每個模組必須一張**專屬**圖(走 BakeUV) |
| ⑤ 腳本 E:Combined bake(Q2106) | 用同事完整材質算「貼圖 + 光影 + 反光」寫進一張 | Glossy + View From **Above Surface** → **整片發白**(每個面都假設被正對著看,都疊上一層反射);關 Glossy → **太黑**(Q2109) |
| ⑥ **定案(Q2110)** | Glossy 開 + View From **Active Camera**:每個模組 bake 時,腳本在**模組中央、最低點 + 1.7 m** 放暫時相機 `__BAKE_CAM__`,bake 完刪除、場景相機還原 | ✅ 接近 Rendered:金色布邊光澤、石材亮面、地上光斑都在 |

- 限制:反光亮點以「站在模組中央」的角度固定,玩家站別處會有偏差,但整體亮度與質感接近。
- 單張貼圖的容量天花板(Q2105):同事平鋪貼圖通常 256~512 px/m,單張專屬圖約 15~66 px/m,磚紋必然變糊;
  能提升的只有拆物件、刪看不到的面、同型模組共用一張(燈光須一致)。
- 遠景體積霧是空氣中的效果,不在表面上 → **bake 不進去**,引擎另外加霧。

---

## 4. 定案工具組與用法

腳本在 [`tools/blender-final-bake/`](../../tools/blender-final-bake/)(對應 Blender 文字區塊名稱見該資料夾 README)。

| 檔案 | Blender 區塊名 | 用途 |
|---|---|---|
| `00_check_uv_res.py` | 檢查腳本 v3 | 建 BakeUV + Concave 重排 + 算 `bake_res`(分批、可續跑) |
| `01_bake_final_all.py` | 01_正式bake_全部 | Combined + 反光,**一次一個**,一直 Alt+P;`final_ver` < `VERSION` 的才算;bake 完自動掛 FINALVIEW_ 預覽 |
| `01b_bake_final_targets.py` | 01_正式bake_指定 | 只算指定模組(TARGETS 或選取);舊圖自動備份 `_old.exr`;完成標 `final_ver = VERSION` |
| `02_bake_quick_targets.py` | 02_指定bake_試算 | `QUICK=True` 最多 2048 / 64 samples 試算(final_ver 設 0,之後仍會正式重算);`False` 正式算 |
| `03_toggle_view.py` | 03_切換檢查 | 選取模組 Alt+P:算圖結果 ↔ 同事貼圖;`RESTORE + ONLY_SELECTED=False` 存檔匯出前還原 |
| `opt_bake_ao.py` | 腳本 C | AO 分批 bake(選用,本案未採用) |

### 標準流程

```
00 檢查腳本 v3(重複 Alt+P 到「全部完成!」)→ 看表,px/m 一致
  ↓
02 試算一個小模組(例 SM_HA_Aa_HIGH1,<1 分鐘)→ 03 在 Rendered 下 TOGGLE 對照
  ↓  不像 → 調燈 / 參數 → 再試算
02 試算 TURN 一次(2048,約 2~4 分鐘)確認大模組也 OK
  ↓
01 正式 bake 全部(一直 Alt+P;HA 1~2 分 / VA 2~4 / L_HA 5~8 / TURN 15 分+)
  ↓
03 逐一 TOGGLE 驗收 → 存檔 / 匯出前 03 RESTORE
```

### 進度記錄規則(重要)

| 屬性 | 誰寫 | 意義 |
|---|---|---|
| `uv_done` / `uv_try` | 00 | UV 已排好 / 嘗試次數(降級用) |
| `bake_res` | 00 | bake 解析度,01/02 照這個開圖 |
| `final_ver` | 01、01b(正式) | 用哪個 VERSION bake 過;02 試算會設回 0 |

- **刪掉 EXR 不會讓 01 重算**(Q2112):01 看的是物件上的 `final_ver`,不是資料夾有沒有檔案;刪檔只會讓該模組畫面變回同事材質。
  要重算單一模組 → 用 01b 指定;或先 `bpy.data.objects["SM_TURN_A_HIGH2"].pop("final_ver", None)` 再跑 01。
- 調燈後要**全部**重 bake → `VERSION + 1`。
- 燈在接口附近 → 接口**兩側**模組都要重 bake,比對才準。
- 要改小圖(跑不動):改 00 的 `MAX_RES` / `DENSITY` 重跑 → 01/02 會自動用新尺寸。

### 比對時看什麼(03 TOGGLE,一律在 Rendered 下比)

| 看到的差異 | 判斷 |
|---|---|
| 算圖結果比較糊 | 正常,解析度上限約 16 px/m |
| 反光位置跟即時算圖不同 | 正常,反光固定在模組中央視角 |
| 亮度或顏色差很多 | 不正常(檢查 Glossy / View From / 鄰居是否還掛著預覽材質) |
| 一片黑或色塊 | 不正常,多半是 UV 或反面 |

### 腳本會改什麼、不會改什麼(Q2110)

- **會改且留在檔案**:Render Engine=Cycles、Max Samples、Bake 設定(Combined、Direct+Indirect、Diffuse+Glossy+Transmission+Emit、Active Camera、Margin 16)、各模組 active UV=BakeUV、`final_ver`、FINALVIEW_ 預覽材質(物件層)、自動存檔。
- **暫時、會自動清掉**:`__BAKE_CAM__` 相機、`__BAKE_TARGET__` 圖片節點。
- **完全不動**:燈光、World/HDRI、色彩管理、Light Paths、模型、UV1、同事材質內容。
- ⚠️ **色彩管理不會進到 EXR**:EXR 存線性值,Exposure / View Transform 不會 bake 進去;引擎有自己的 tone mapping,輸出給引擎前可能要另外轉換(例如 PNG)。

### 交給同事 / 換檔案(Q2110)

- 同事只要**看一樣的打光**:Append 燈光 Collection、World(HDRI)、霧;**色彩管理與 Light Paths / Clamping 是場景設定,Append 不會帶過去,要手動設成一樣**;確認 World 強度一致。
- 同事要**自己 bake**:同一套腳本,`COLLECTION` 改成他的名稱,新檔一定要先跑 00(進度存在物件上)。
- 最省事:把同事新版模組 append 進**你的**檔案,跑 00 + 01,把 `bake_final/FINAL_*.exr` 交出去。
- 換電腦:`.blend` 與 `bake_final/` 要放同一層一起帶走(否則 Uninitialized image)。

---

## 5. 踩坑紀錄

| # | 現象 | 原因 | 解法 |
|---|---|---|---|
| 1 | 同事的 UVMap 想直接當 bake UV | 有重疊、超出方格 | 新增第三套 BakeUV |
| 2 | TURN UV 用量 3%、清晰度差 5 倍 | Smart UV 用外框方塊排彎曲長條 | Pack Islands CONCAVE + 依實際 UV 用量算解析度 |
| 3 | 一次排 19 個 UV,Blender 當掉 | Concave 太吃資源 | v3 分批 + 每個前後存檔 + 自動降級 |
| 4 | 4096 上限時 TURN 只有 7.3 px/m | 4.6 萬 m² 裝不下 | MAX_RES 8192(僅撞上限的模組會變大) |
| 5 | 以為 Blender 當掉 | 點了 Console 黑視窗進入選取模式 | Console 按 Esc |
| 6 | bake 抓到檢視用材質 | 模組還在 VIEW / FINAL 預覽(物件層材質) | bake 前把**所有**模組切回 `DATA`(連鄰居也要,否則預覽自發光會反射到被 bake 的模組) |
| 7 | COMBINED 預覽偏平、旗子過紅 | 只抓底色 × 光影,跳過同事節點群組與反光 | 改 Combined bake 讓 Blender 用完整材質算 |
| 8 | Combined + Glossy 整片發白 | View From = Above Surface,每個面都疊正對反射 | Active Camera + 模組中央 1.7 m 暫時相機 |
| 9 | 關 Glossy 太黑 | 少了石材/布邊反光的亮度 | 同上(定案) |
| 10 | 刪了 TURN 的 EXR,01 不重算 | 01 看物件上的 `final_ver` | 01b 指定重算,或 pop `final_ver` |
| 11 | 01b 把 TARGETS 留空就報錯 | Gemini 只改註解說「留空=用選取」,程式沒實作 | 入庫版已補上 Q2111 的選取邏輯 |
| 12 | 怕算很久結果跟打光差很多 | — | 02 先低畫質試算(TURN 2048/64 約 2~4 分),滿意才正式算 |

### 外部 AI(Gemini)解說的勘誤

- ❌ Q1903 說腳本 A 是「Diffuse(光影與色彩)烘焙」— Color 是關的,**只有光影**。
- ❌ Q1707 說腳本 B 的 RESTORE「有致命 bug、同事材質會救不回來」— 預覽材質掛在**物件層**材質槽,同事材質留在網格(DATA)層,
  `slot.link = 'DATA'` 就切回原材質,實測也正常;並無此問題。
- ⚠️ Q2112 建議 `TARGETS = []` 註解寫「留空 = 自動用選取」,但沒改程式 → 照做會直接報錯(見踩坑 #11)。

---

## 6. 待辦

- ⬜ EXR(線性)→ 引擎用格式的輸出腳本(含色彩管理對齊)。
- ⬜ AO 是否要乘進最終圖(腳本已備:`opt_bake_ao.py`)。
- ⬜ 討論:地板材質是否影響周遭牆面的反光(Combined 會吃到地板的反射)。
- ⬜ 全紀錄線上文件連結補上。
- ⬜ C3:地板 36 塊分層烘焙(LIGHT / GLOSS / DETAIL / 場景 AO)+ PS 合成 + AI 細節對燒。
