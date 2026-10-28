# 實戰紀錄 — C1 模組化走廊灰模 Bake → 驗接縫(Blender 自動化 Pipeline)

> 目標:哥德走廊 6 組模組(直向 ×2、橫向 ×2、十字 ×1、橫向穿堂 ×1)貼圖還在同事手上,
> 只能用 AI PBR 當暫代材質打光。要確認**現在打的光,在 6 組模組拼接處能不能順利接續**。
> 做法:全部換中性灰 → 每組合併 + 第二套 UV → 在**拼好的完整場景**裡 bake 純光影 →
> 以自發光顯示 bake 結果巡接縫。
>
> **本篇範圍 = 第一段(「換電腦作業」之前)**:灰模驗接縫 pipeline。
> 第二段(換電腦後:同事貼圖進來後的 COMBINED bake、地板 36 塊分層烘焙 + PS 合成)另篇待補。

- **Claude 對話連結(本案全程:作法討論 → 腳本迭代 → bake 實測 → 法線修復 → 紀錄;同串續篇亦在此):**
  `https://claude.ai/code/session_01BEBwyiUGGcpDC64eDLhAJs`
- **全紀錄 — 線上文件版(A1 分頁:Q1~Q14 討論原文 + 腳本 + Gemini 解說,即上傳的 3 段對話):**
  [Google Docs](https://docs.google.com/document/d/1g2Q4WUa63tBAq5T58IAHFdzpmPzESFmj3_EH0RtsZZM/edit?tab=t.g2xtgg2thkm2#heading=h.k9cu2ipw3hrf)

**🔑 關鍵字:** `C1`、`灰模 bake`、`驗接縫`、`模組接縫`、`BakeUV`、`UV2`、`GREY_TEST`、
`#767676`、`DENSITY`、`px/m`、`Diffuse bake`、`法線反面`、`Face Orientation`、`洋紅色貼圖`、
`Blender bake pipeline`

## 狀態

- ✅ **pipeline 跑通**(Blender 4.5 / Cycles GPU):15~16 個 `_J` 模組全數 bake、存 EXR、
  自發光預覽巡接縫。直向段與相鄰段交界平順,燈光擺法一致。
- ⚠️ TURN(十字)模組仍有少量反面未修完,該區 bake 為黑,待回頭修。
- ⬜ Bake 本身仍是**手動按鈕**(準備與收尾已腳本化),目標改成全自動。
- 整理日期:2026-10-28

---

## 0. 核心原則(先讀)

| 原則 | 為什麼 |
|---|---|
| **先拼好、再打光、整場 bake** | 光是關卡(Level)的屬性,不是模組(Asset)的屬性 |
| **可以一組一組 bake,但其他模組要全部顯示** | Cycles bake 會算整個場景;鄰居在場,遮蔽與反彈光就對得上。真正會壞的是「單一模組擺在空場景裡 bake」:開口外面是空的 → 開口端 AO/GI 偏差 → 拼起來必有光縫,而且分不清是打光錯還是 bake 錯 |
| **只留室內光** | World Strength = 0;外部光會把接縫暗部偷偷填亮,掩蓋問題 |
| **全場一種中性灰** | 排除貼圖變數;灰模就有縫 = 模型問題,不是光的問題 |
| **一個模組 = 一顆材質 + 兩套 UV** | UV1(原本,tiling,超出 0~1)給正式貼圖;UV2 `BakeUV`(0~1、不重疊)給光影。等同 UE lightmap 用第二套 UV |
| **固定像素密度(px/m)** | 大小模組清晰度一致,接縫不會「一邊糊一邊清楚」 |

**問題出在哪一步(分流表)**

| 看到的問題 | 出在 |
|---|---|
| 灰模就有縫 | 模型:接口頂點沒對齊 / 邊界法線方向不一致 |
| 加燈後才有縫 | 燈的擺放不一致 |
| 換貼圖後才有縫 | 貼圖或 UV(AI 暫代貼圖建議 Box / triplanar 投影,跨模組連續) |

---

## 1. Pipeline 總覽(7 步)

腳本全在 [`tools/blender-modular-bake/`](../../tools/blender-modular-bake/),
Scripting 分頁 → New → 貼上 → Run(或 Alt+P)。**全程在另存的測試檔做**(合併/刪材質不可逆)。

| 步 | 階段 | 腳本 | 目的 |
|---|---|---|---|
| 1 | 模型合併與清理 | `01_join_clean.py` | 每組零件 → 一個 `_J` 網格;保留父層 Empty / Collection,清空殼 Empty |
| 2 | 強制中性灰 | `02_force_grey.py`(步驟 1 已換灰可略) | 清空遺留材質欄位,統一 `GREY_TEST`(#767676) |
| 3 | 展 Bake 專用 UV | `03_bake_uv.py` | 每個 `_J` 新增 `BakeUV` 並 Smart UV Project,不動 UV1 |
| 4 | 法線反面修復 | `04_fix_normals.py` | 燈光 + 視角投票翻正反面,避免 bake 死黑 |
| 5 | 解析度 + bake 目標 | `05_bake_targets.py` | 依表面積算解析度(DENSITY 16 px/m),建 `BAKE_` 專屬材質 + 空白 float 圖 |
| 6 | 準備 Bake → **手動按 Bake** | `06_prepare_bake.py` | 切回灰材質、選取全部 `_J` |
| 7 | 存 EXR + 自發光預覽 | `07_save_and_preview.py` | 存 `//bake/*.exr`、綁路徑、接 Emission、存 .blend |
| 救援 | 洋紅色 / 換電腦 | `08_relink.py` | 重新連結 bake 圖 |

> 步驟 4 放在 5 前面或後面都可以,只要在 bake 前做完;修了法線的模組要重 bake。

---

## 2. 前置:場景與灰材質

### 2.1 關掉外部光(對話 Q2)

- **World 分頁(紅色地球)→ Surface → Strength = 0**。套了 HDRI 時 Color 欄顯示的是圖名、點不到色塊,
  改 Strength 最簡單,之後改回 1 就恢復。
- 要在**第 4 顆球 Rendered** 才吃 World 設定;第 3 顆 Material Preview 用內建預覽 HDRI,Strength 0 也還是亮的。
  Rendered 下畫面全黑 = 外部光已關乾淨。
- 曾考慮「做盒子屏蔽 HDRI」:可行但坑多(盒子要全黑 albedo 0、要封閉有厚度、開口外看出去是黑),
  **直接關 World 最乾淨**。
- 引擎端(UE):關 Sky Light / Directional / SkyAtmosphere;**Exposure 設 Manual 固定**,
  否則 Auto Exposure 會把兩模組的亮度差補償抹平,誤判接得很順。
- 有窗光設計時分兩步:先純室內光驗接縫 → 再加回月光檢查窗光在各模組(尤其十字/橫向旋轉後)是否一致。

### 2.2 中性灰材質 GREY_TEST(對話 Q3、Q4)

- Base Color **Hex `767676`**(= 18% 反射率中性灰,linear 0.18)、Roughness 0.5。
  - 用 Hex 輸入;RGB 分頁是線性值,要填 0.18 不是 0.46。
  - 想貼近偏暗石材可用 `#5A5A5A`,但驗接縫先用 `#767676` 最好看出縫。
- 名稱注意:實際檔案是 **`GREY_TEST`(E)**,不是 GRAY(A);腳本與材質名必須一字不差。
- 兩種套法:

| 方法 | 做法 | 適用 |
|---|---|---|
| Material Override | View Layer 分頁 → Override → Material 選 GREY_TEST | 只想**看**灰模;不動原材質;只在 Rendered 生效 |
| 真的替換 | 做一顆只有 1 行 GREY_TEST 的 Cube → 全選、最後點 Cube → Ctrl+L → Link Materials;或跑 `02_force_grey.py` | **要 bake**(每組要有自己的材質) |

> Ctrl+L 會把「作用中物件的整份材質清單」複製過去:Cube 有 1 行,大家就 1 行;Cube 有 2 行,大家就 2 行。

---

## 3. 七步詳解

### 步驟 1 — 模型合併與清理(`01_join_clean.py`,對話 Q5、Q7、Q8)

- **做什麼**:選取模組 Root Empty → 底下所有可見網格 `make_single_user` → **Convert to Mesh** → Join →
  命名 `<模組>_J`,放回原 Empty 底下(保持世界座標)、同 Collection,遞迴刪掉變空的子 Empty。
- **痛點**:一組模組由上百個零件組成,bake 時每個零件一張圖無法管理。
- **為何要 Convert to Mesh**:Mirror / Array / Bevel 等修改器還不是真的面;直接 Ctrl+J,
  非作用中物件的修改器會被丟掉(Array 柱子只剩 1 根),作用中物件的修改器會套到整個合併體上。
- **注意**:先 **Alt+H** 顯示全部,隱藏的零件不會被合併(腳本會列 ⚠ 清單)。
  實例:`FLAG.007`(旗子)、`FOUNTAIN.010`(噴泉)當時被隱藏沒併進 `_J` — 仍參與遮光反光,不影響接縫,
  但全選 bake 時**不能選到它們**(沒有 bake 目標會報錯)。
- **版本演進**:初版 all-in-one 腳本(合併+材質+UV 一次做)用 `parent_clear` 把合併體拉出 Empty、
  也不清空殼;v2 改為放回 Empty + `temp_override`(新版 Blender context)+ CLEAN_EMPTY,定案。
- 手動版:Select Hierarchy → Ctrl+點一個網格當作用中(**不能是 Empty**)→ Object > Convert > Mesh → Ctrl+J。

### 步驟 2 — 強制中性灰(`02_force_grey.py`,對話 Q6)

- **痛點**:原模型(Maya 來源)每個物件帶 8 個材質欄位(WATER、FLOOR_ID、WHITE_H_LINE…),一格格換太慢。
- `materials.clear()` + `append(GREY_TEST)` → 每物件只剩 1 行。
- **為什麼可以只留一顆**:bake 的是 Diffuse 光影(Color 關掉),材質顏色不影響結果。
  保留 8 顆反而要在 8 顆材質裡各放 bake 節點、都指同一張圖、都設選中,少一顆就報錯。
- **代價**:測試檔裡「哪個面用哪顆材質」的記錄沒了 → 貼回正式貼圖時用**主檔**,不用測試檔。

### 步驟 3 — 展 Bake 專用 UV(`03_bake_uv.py`,對話 Q9)

- 對每個 `_J`:新增(或沿用)`BakeUV` → 設為 active(反白)→ 編輯模式全選 → Smart UV Project
  (Angle 66°、Island Margin **0.005**)。
- **為什麼要第二套**:原本的 UV1 是 tiling 用,散在 0~1 外面;bake 只寫 0~1,超出會重疊/遺失。
- **兩個圖示別搞混**:**反白** = 編輯/bake 用哪套 → BakeUV;**相機圖示** = 算圖用哪套 → 留在 UV1。
- **一次只展一個物件**:多選一起展,UV 會被擠進同一個正方形,bake 互搶位置(腳本已逐一處理)。
- 新增的那行一開始是 UV1 的複製品,超出方格是正常的,Smart UV 會重展。
- 驗收:UV Editing → 點物件 Tab → A:全部在一個正方形內、互不重疊。

### 步驟 4 — 雙階段法線反面修復(`04_fix_normals.py`,對話 Q13)

- **症狀**:bake 後某段牆整片死黑,但拱肋還有光。開 **Overlays → Face Orientation**:
  Blender 4.2+ 正面透明、**背面紅色** → 牆面整片紅 = 面反了。
- **為什麼平常算圖看不出來,bake 卻黑**:Cycles 算圖會把背面當正面算;bake 照法線方向收光,
  反面朝牆外收光 → 牆外沒燈 → 黑。Maya 預設雙面顯示,所以來源檔一直沒被發現(鏡射縮放 -1 的零件最常見)。
- **腳本機制**:
  - 第一段(巨觀):每個相連零件(island)先統一方向,再用「場景點光 + 眼睛位置」對大面發 raycast 投票,
    背對多數光源的整塊翻轉。
  - 第二段(微觀):從**當前透視視窗的眼睛**對每個面發 raycast,看得到、但背對眼睛的面逐面翻正。
- **用法**:Layout 透視視窗 Walk(Shift+`)站到紅色前停住 → 跑腳本 → 看 Console 第一行確認抓的是**透視、大尺寸**視窗 →
  回去看紅色;其他區域走過去再跑。
- **迭代史(4~5 版,定案 v4)**:
  - v2 只靠燈光投票:室內單片薄板判斷不穩。
  - v3「看得到的就修」:抓錯視窗(Scripting 分頁的小 3D 視窗)→ 眼睛位置錯。
  - v3.1:抓到 Layout 左邊的**俯視線框圖**,眼睛卡在建築裡,反而把正確的窗翻錯。
  - v4:只取透視模式中面積最大的視窗 + 先整塊修正(順便復原上一版翻錯的)再逐面修 → 定案。
- **限制**:只修「燈光 + 當前視角」看得到的面,不是全場無死角;需要走位多跑幾次。
- 手動版:Tab → A → Shift+N(Recalculate Outside;對單片薄板偶爾判斷錯)→ 剩下的紅色 L 選取 → Alt+N → Flip。

### 步驟 5 — 依表面積算解析度 + bake 目標(`05_bake_targets.py`,對話 Q10)

- **痛點**:模組大小差很多;一律 2048 → 小模組細、大模組糊,接縫「一邊清楚一邊糊」看起來就是一條縫,
  但那是解析度造成的,不是打光錯。
- **公式**:`res = 2^round(log2( sqrt(表面積 / PACK) × DENSITY ))`,夾在 512~4096;PACK 0.6 = Smart UV 約用掉 60% 空間。
- 同時建 **`BAKE_<物件>` 專屬材質**(GREY_TEST 複本)+ **同名空白 float 圖**,並把 Image 節點設為選中(= bake 目標)。
  **共用一顆 GREY_TEST 會全部 bake 到同一張圖互相覆蓋。**
- **實測調參**:

| DENSITY | 結果 |
|---|---|
| 32 | 哥德細節多,表面積巨大(十字 4.7 萬 m²)→ 16 張全卡 4096;px/m 14.6~40.2,**差 2.75 倍** ❌;16 張 4096 float 約 4.3 GB |
| **16(定案)** | 3 張 4096 + 其餘 2048;px/m **14.6~20.1,差 1.4 倍** ✅;約 1.6 GB |

- 16 px/m ≈ 一個像素 6 cm:光影漸層、牆角暗部、地上光斑都清楚,驗接縫夠用;只有窗花小陰影不夠細。
- 判讀規則:各模組「實際 px/m」差 **2 倍以內**即可;出現「⚠ 已達上限」→ 整體調低 DENSITY 讓全部一起降,維持一致。
- 手動版(估算):N 面板看 Dimensions 最長邊 → 60m+ 4096 / 30~60 2048 / 15~30 1024 / <15 512;
  材質複製(名稱欄右邊的複製圖示)→ Shading 新增 Image Texture(32-bit Float、不勾 Alpha)→ 不接線、點選讓它白框。
- 後續改良:第二段(換電腦後)的版本改為**量實際 UV 面積**再換算、上限放到 8192,見續篇。

### 步驟 6 — 準備 Bake + 手動按 Bake(`06_prepare_bake.py`,對話 Q11、Q14)

- 腳本:把顯示模式的 Emission 斷開、BSDF 接回 Output(切回灰材質),Image 節點設回 active,選取全部 `_J`。
  **為何要切回**:材質正在讀那張圖顯示,bake 又要寫同一張 → 報錯。
- **Bake 前檢查**:燈光 Collection 全部勾選(沒勾的燈不參與 bake)、World Strength 0、所有 `_J` 顯示。
- **Render 分頁設定**:

| 項目 | 設定 | 備註 |
|---|---|---|
| Render Engine / Device | Cycles / GPU Compute | |
| **Sampling → Render → Max Samples** | **256** | ⚠️ 不是 Viewport 那組;bake 只吃 Render 的 |
| Noise Threshold / Denoise | 對 bake 無效 | bake 一律跑滿樣本;不支援降噪 → 雜點只能靠 samples 壓 |
| **Bake Type** | **Diffuse** | 不用 Combined:會乘上 18% 灰材質色,整張偏暗 |
| Contributions | Direct ✅ Indirect ✅ **Color ❌** | = 純光影(照到多少光記多少) |
| View From | Above Surface | |
| Target | Image Textures | |
| Clear Image | ✅ | |
| Margin | 16 px(Adjacent Faces) | 防 UV 邊界滲色 |

- Bake 按鈕灰色 = 沒選物件 / 在 Edit Mode / 選到 Empty。
- **先試 bake 一個小模組**再全跑:正常 = 燈附近亮、角落暗,暖橘冷藍都有;UV 圖大片黑 = 空白與背面(正常);
  全黑 = 燈 Collection 沒開;雜點多 = samples 不夠。
- **samples 實測**:64 雜點明顯 → 256 漸層平滑、驗接縫夠用(2048 模組約 **40 秒**)。
- **時間估算**(與像素數成正比):13 個 2048 × 40s + 3 個 4096 × 160s ≈ **17 分鐘**(512 samples 約 35 分鐘)。
  跑的時候不要操作 Blender。

### 步驟 7 — 存 EXR + 自發光預覽(`07_save_and_preview.py`,對話 Q12、Q14)

- 存 `//bake/BAKE_*.exr`(.blend 旁的 bake 資料夾)→ 每顆 BAKE_ 材質加 `UVMap(BakeUV)` → Image → **Emission** → Output →
  存 .blend。切 **Material Preview** 巡場景:只剩自發光,不受燈光/HDRI 影響,不用即時算光,畫面流暢。
- **為何 EXR**:PNG 超過 1.0 的亮度會截斷,燈附近一片死白;EXR 保留完整亮度,之後調曝光還看得到細節。
- 手動存的設定:Image Editor → Save As → OpenEXR / RGB / **Float (Half)** / ZIP / Color Space Linear Rec.709 /
  **Save As Render 不勾**(勾了會套顯示色彩轉換,數值不再是原始光影)。
- 顯示切換:原本有一支 `MODE = "BAKED" / "LIT"` 開關腳本;最終被 06(切回 LIT + 選取)與 07(存檔 + 切 BAKED)兩支吸收。

### 巡接縫判讀

| 看到的 | 原因 | 處理 |
|---|---|---|
| 接口一條細亮線/暗線 | 邊界法線不一致或頂點沒對齊 | 修模型 |
| 接口兩側整片亮度不同 | 燈光擺放不一致 | 調燈(燈做成模組附屬物件,同相對位置) |
| 一邊清楚一邊糊 | 解析度不同 | 目前差 1.4 倍,不明顯 |
| 黑色斑塊/亮點 | UV 重疊或 margin 不夠 | 重展該模組 UV |
| 整段牆死黑、骨架有光 | 法線反面 | 步驟 4 |
| 洋紅色 | 找不到貼圖 | `08_relink.py` |
| 很平順看不出交界 | ✅ 打光接得起來 | — |

**修完要重 bake 的循環**:06(切回灰 + 選取;只想重 bake 部分就改選那幾個)→ Bake → 07。

---

## 4. 踩坑紀錄

| # | 現象 | 原因 | 解法 |
|---|---|---|---|
| 1 | 一開始想「6 組各自攤 UV、各自 bake 再拼」 | 單模組空場景 bake,開口端缺鄰居遮蔽/反彈 → 必有光縫 | 拼好、全部顯示,再逐組 bake |
| 2 | World Strength 0 了畫面還是亮 | 看的是 Material Preview(內建 HDRI) | 切 Rendered 檢查 |
| 3 | Ctrl+L 後每個物件出現兩行 GREY_TEST | 來源 Cube 本身有 2 行材質 | 來源只留 1 行;或用 02 腳本 |
| 4 | 合併後物件跑出 Empty 之外 | 初版腳本 `parent_clear` | v2 放回 Empty + 保持世界座標 |
| 5 | 有零件沒被合併(旗子、噴泉) | 合併時被隱藏 | 先 Alt+H;漏掉的不在接口就不用管,但別選進 bake |
| 6 | DENSITY 32 時全部 4096、清晰度差 2.75 倍、記憶體 4.3 GB | 哥德細節表面積太大 | DENSITY 16 |
| 7 | Bake Type 是 Combined | 會乘上灰材質色,偏暗 | Diffuse + Color 關 |
| 8 | 改了 samples 雜點還在 | 改到 Viewport 的 Max Samples | 改 **Render** 的 Max Samples |
| 9 | 存完圖重開,只有手動存的那張正常,其他洋紅 | 存檔腳本 `img.save(filepath=…)` 沒讓 Blender 記住路徑 | 改 `filepath_raw` + `save()`;已存的跑 `08_relink.py` 後 Ctrl+S |
| 10 | 某段整片死黑 | Maya 鏡射零件法線反了;算圖看不出、bake 才現形 | Face Orientation 確認 → 步驟 4 |
| 11 | 法線腳本把正確的窗翻錯 | 抓到 Scripting 小視窗 / Layout 俯視圖的眼睛位置 | v4:只取透視模式、面積最大的視窗 |

### 外部 AI(Gemini)解說的勘誤

- ❌「Diffuse bake 把 `use_pass_color = False` 會整張全黑,應設 True」— **錯**。
  Diffuse 的 Color 關掉 = 只要 Direct + Indirect 光照,正是本流程要的純光影;實測 bake 出暖/冷光正常。
  設 True 反而會乘上材質顏色。
- ⚠️「法線腳本 v4 能無死角全自動修完」— **言過其實**:它只處理燈光與當前視角看得到的面,要走位多跑;
  TURN 模組至今仍有殘留紅面。

---

## 5. 工具(已入庫)

| 檔案 | 對話出處 | 做什麼 |
|---|---|---|
| [`01_join_clean.py`](../../tools/blender-modular-bake/01_join_clean.py) | Q8 腳本 3(v2) | 選取模組 → Convert + Join 成 `_J`、放回 Empty、清空殼、換 GREY_TEST |
| [`02_force_grey.py`](../../tools/blender-modular-bake/02_force_grey.py) | Q6 腳本 2 | 選取物件的材質全清空 → 只剩 GREY_TEST |
| [`03_bake_uv.py`](../../tools/blender-modular-bake/03_bake_uv.py) | Q9 | 所有 `_J` 新增 BakeUV + Smart UV(margin 0.005) |
| [`04_fix_normals.py`](../../tools/blender-modular-bake/04_fix_normals.py) | Q13 v4 | 燈光 + 視角 raycast 雙階段翻正反面 |
| [`05_bake_targets.py`](../../tools/blender-modular-bake/05_bake_targets.py) | Q10 腳本 10 | 表面積 → 解析度(DENSITY 16)、BAKE_ 材質 + 空白 float 圖、印 px/m 表 |
| [`06_prepare_bake.py`](../../tools/blender-modular-bake/06_prepare_bake.py) | Q14 準備 | 切回灰材質 + 選取全部 `_J` |
| [`07_save_and_preview.py`](../../tools/blender-modular-bake/07_save_and_preview.py) | Q14 收尾 | 存 EXR(記住路徑)+ Emission 預覽 + 存 .blend |
| [`08_relink.py`](../../tools/blender-modular-bake/08_relink.py) | Q12 救援 | 重新連結 `//bake/*.exr`,列出缺圖 |

> 未入庫:Q5 初版 all-in-one 腳本(合併 + 材質 + UV;已被 01/03/05 取代)、
> `MODE = BAKED/LIT` 顯示切換腳本(已被 06/07 吸收)、法線腳本 v2/v3。

---

## 6. 待辦

- ⬜ **Bake 自動化**:把「06 → Bake → 07」串成一支(逐模組 `bpy.ops.object.bake` + 存檔 + 進度紀錄),
  不再手動按鈕。(第二段已用 `final_ver` / `split_<TAG>` 自訂屬性做到批次與續跑,見續篇)
- ⬜ TURN 模組殘留反面修完 → 重 bake。
- ⬜ 漏併零件(FLAG / FOUNTAIN)視需要單獨處理。
- ⬜ 續篇:同事貼圖進來後的 COMBINED bake(GLOSSY 用暫時相機 @ 模組中心眼高)、
  地板 36 塊分層烘焙(LIGHT / GLOSS / DETAIL / 場景 AO)+ PS 合成 + AI 細節對燒。
