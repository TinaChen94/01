# concept→3D / 三視圖重建 / 拆概念圖（image-grounded SOP）

**用途：** 任務是「從一張既有圖（概念圖 / 遊戲截圖 / 照片 / 設計稿）**抽出某個物件**，把它**轉成正交三視圖**（front / side / top）、做 reference plate、餵 image-to-3D」時，照這份做。

**觸發詞：** 「拆掉這張概念圖」「concept→3D」「三視圖重建」「turnaround / model sheet」「正交立面」「image-to-3D 參考圖」「物件清單 / asset manifest」。

---

## 🔴 根本鐵律（違反必漂移）

> **物件已經在圖裡了 → source of truth 永遠是那張圖，不准把物件翻成文字代理。**

這類任務本質是 **image-grounded 的「抽取 + 重定向」**，不是 text-to-image 的「從零描述」。
把物件描述成一段文字再從零生成 = 用 **lossy proxy** 取代原圖：文字必然有損，模型會用自己的先驗（generic 範式）把缺口補完 → 造型穩定地錯。

**文字只負責「呈現規格」，不負責「物件長相」。** 長相交給圖。

---

## ❌ 反模式 vs ✅ 正解

| 維度 | ❌ 反模式（會漂移） | ✅ 正解（image-grounded） |
|---|---|---|
| 任務模式 | text-to-image 從零生成 | **image-to-image，餵原圖 extract** |
| Source of truth | 自己寫的「設計聖經」文字 | **原圖本身** |
| 文字在描述什麼 | 物件長相（寫死細節） | **只描述呈現方式**：視角 / 背景 / 打光 / 輸出用途 |
| 對來源視角 | 只說 ortho，沒否定來源相機 | **明確 `IGNORE` 來源低角度/3-4/透視** |
| 一致性錨 | 文字描述（鎖在誤讀上） | **原圖 +（前一視 render）+ 固定 seed** |
| 過度描述 | 細節越寫越多 = 幻覺面積越大 | 物件交給圖，文字精簡 |

**為什麼「設計聖經文字」是陷阱：** 「先鎖一段文字描述保證三視一致」立意對（三視確實要一致），但**錨點選錯**——一致性該綁「原圖 + seed」，綁文字 = 把一致性穩穩鎖在你的誤讀上，於是會「一致地錯」。

---

## ✅ 勝利模板（逐字可改）

把物件名填進 `[OBJECT]`，視角換 `FRONT / LEFT-SIDE / TOP`。第一視餵**原圖**；第二、三視**同時餵原圖 + 已產出的正確視圖**當一致性錨。

```
From the attached concept art [and the front reference plate], extract ONLY
the [OBJECT] and re-orient it to a true head-on FRONT orthographic view —
camera perpendicular to the front, at eye level, the object facing the viewer
directly; IGNORE the concept's camera angle and perspective (do NOT copy a
low-angle, tilted or 3/4 view). [SAME object, identical proportions, materials
and details as the reference plate.] Re-render as one complete, isolated
object, centered and fully visible, on a flat neutral grey (#808080) seamless
background. Perfectly even diffuse studio lighting, NO cast shadows, NO rim
light, NO scene elements. Maximum sculptural detail. High-resolution clean
reference plate for image-to-3D.
```

**模板拆解（每段在幹嘛）：**
1. `extract ONLY the [OBJECT]` — 鎖定要抽的物件，丟掉場景其餘。
2. `re-orient to a true head-on … orthographic view` — 任務＝重定向既有物件，不是發明。
3. `IGNORE … do NOT copy low-angle/tilted/3-4` — **點名否定來源相機**（image-grounded 時最關鍵，不寫會沿用原圖視角）。
4. `SAME object, identical proportions…` — 第二/三視的一致性鎖（只在有 reference plate 時加）。
5. `#808080 seamless / even diffuse / NO shadows/rim/scene` — 乾淨呈現規格，給建模讀幾何。
6. `reference plate for image-to-3D` — 用途錨，把模型推向乾淨單體輸出。

---

## 🔁 三視一致性協議

```
front:  input = 原圖                    → 出 front plate（驗證 silhouette 疊原圖）
side:   input = 原圖 + front plate       → prompt 加「SAME object as reference」
top:    input = 原圖 + front + side      → 同上
```
- **固定 seed** 全程沿用。
- 每出一視，先**疊回原圖比剪影/比例**，過了才往下一視（不要三張一次盲生）。
- 細部 hero 元件（如玫瑰窗、門飾）可單獨再 extract 一張特寫 plate。

---

## 🧰 平台選擇（都要能吃參考圖）

| 平台 | 何時選 | 注意 |
|---|---|---|
| **Nano Banana Pro** | 預設首選；指令服從最好、多圖 reference 是 superpower、可渲染 title block | 自然段 80–150 字；不吃 `--ar`/`--params`，比例到 UI 設 |
| **Flux 1.1 Kontext** | 要極寫實材質、要對既有圖做精準局部編輯 | 偏寫實會偷加透視 → 句首再壓 `strictly flat orthographic, no perspective`；**禁藝術家名、禁 `--ar`** |
| **Seedream 5.0** | 中文場景 / 要精簡 prompt | 重要詞在前；英文 for photoreal 反而更準 |

> 共同點：**這三家都支援 image input / edit**。選錯的不是「模型」，是「模式」——別用任何一家的純 t2i 模式做這件事。

---

## ✅ 交付前 checklist

- [ ] 有沒有把**原圖當 input**餵進去？（沒有 = 直接違規）
- [ ] 文字是不是只寫「呈現規格」，沒去重述物件長相？
- [ ] 有沒有**點名否定來源相機**（IGNORE low-angle/3-4/perspective）？
- [ ] 背景 `#808080` + 平光 + 無投影/無 rim/無場景？
- [ ] 第二/三視有沒有把前一張正確 plate 也當 reference + 同 seed？
- [ ] output 疊原圖比過 silhouette？

---

## 📌 實證來源（2026-06）

本 SOP 來自一次真實踩坑：拆哥德教堂概念圖做正面三視圖時，先用 text-to-image「文字設計聖經」法 → 造型漂移成單一中殿大教堂＋透視＋自創門廊；改用上方 image-grounded extract 模板（餵原概念圖 + 明確否定來源相機）→ 造型一次正確。**教訓：concept→3D 全程 image-grounded，禁純文字 design-bible。**

相關佐證：`nano-banana.md`（「方式 B 上傳參考圖（最強）」「編輯＝講清楚改什麼+保留什麼」）、`community-prompt-patterns.md`（「Nano Banana Pro 多圖 reference = superpower」）。
