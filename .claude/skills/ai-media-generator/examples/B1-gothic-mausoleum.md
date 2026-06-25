# 實戰案例:B1 哥德式陵墓 — Concept→3D 資產拆分

> 一張哥德墓園概念圖 → 拆出主建築 B1,跑完 front / rear / 45° 等角的完整紀錄。
> 用來示範 [../templates/concept-to-3d-pipeline.md](../templates/concept-to-3d-pipeline.md) 的主模板 + 修正層,並記錄兩個實證踩坑。
> 日期:2026-06-23　平台:Nano Banana Pro / Seedream（image-grounded 編輯）

---

## 資產定位

| 項目 | 內容 |
|---|---|
| 類別 | **[B] 場景模組**(大型結構、定義空間) |
| 來源 | 哥德墓園概念圖(3/4 斜角、綠霧 + 紫光戲劇打光) |
| 完成視圖 | ✅ Front(確認)・✅ Rear 立面・✅ 45° 等角(緊湊版) |
| 待辦 | (選)側面立面 → 多視圖轉 3D;或等角單圖轉 3D → retopo + 烘法線 |

## 設計鎖(de-lit albedo,進 3D 的真相)

- **石牆**:淺暖中性灰、苔痕、裂紋
- **屋頂**:深冷石板(炭灰藍)、陡哥德山牆、尖 finial
- **玻璃**:飽和深紫洋紅彩繪玻璃(尖拱長窗 + 圓形玫瑰窗)— **albedo,非發光**
- **正面**:三山牆對稱(中央 + 左右),拱形大門廊 + 石階
- **量體**:緊湊小教堂,側面約 3–4 個 bay,**不是長中殿**

## 視圖產出順序

1. **Front v1** — 初次提取:屋頂偏緩、屋頂/牆顏色糊
2. **Front v2 ✅ 確認** — 幾何先修(屋頂拉陡拉高、清掉中央峰後糊塊)→ 再拉開三材質顏色
3. **Rear 立面** — 對稱山牆 + 玫瑰窗 + 尖拱長窗 + 小服務門,無大門廊(inferred)
4. **45° 等角 ✅** — 緊湊量體,露正面 + 側面 + 屋頂面

---

## 最終可用 Prompt

### ① Front 修正(幾何 → 顏色;附原概念圖 + Front v1)
```
Ref 1 = the current front plate of this Gothic mausoleum (KEEP head-on front orthographic view, centering, flat neutral grey #808080 background, even diffuse de-lit lighting, no shadows, no rim light).
Ref 2 = the original concept art of the SAME building — TRUTH for roof form and material colors.

Fix TWO things, keep everything else identical:
1. ROOF FORM (first): re-shape to match Ref 2 — steeper, taller, sharper Gothic gables, higher pointed central gable, crisp ridgelines, taller sharper pinnacles; remove the heavy muddy mass behind the central peak. Keep the three-gable symmetrical facade, rose windows, arched door and side windows unchanged.
2. MATERIAL COLOR SEPARATION: roof = dark cool slate (charcoal blue-grey), clearly darker than walls; walls = lighter warm-neutral grey stone with light moss; glass = saturated deep purple-magenta. TRUE de-lit albedo — NO glow/emissive/rim/god-rays on the glass.

Maximum sculptural detail. High-resolution clean reference plate for image-to-3D.
```

### ② Rear 立面(附確認過的 Front)
```
Ref 1 = the confirmed FRONT plate of this Gothic mausoleum — TRUTH for materials, colors, roof, weathering and scale.

Produce ONE single REAR elevation (back view): true orthographic, camera perpendicular to the rear, no perspective, no vanishing point. SAME building as Ref 1 — identical stone color, dark slate roof, finial style, weathering and proportions; MATCH Ref 1's overall width, height, eaves line and roof pitch. Reconstruct the rear as a matching gable end inferred from the front: symmetrical stone gable, same slate roof and corner pinnacles, a rose window in the upper gable and tall lancet stained-glass below — but NO grand entrance portal (plainer: solid wall or a small service door). One complete, isolated building, centered, fully visible, flat neutral grey (#808080) seamless background. Flat even diffuse de-lit lighting, NO cast shadows, NO rim light, NO glow on the glass. Maximum sculptural detail, reconstruct all occluded areas. Asset reference for multiview-to-3D.
```

### ③ 45° 等角(緊湊版;**只附那張對的長等角,不要附正視圖**)
```
Ref 1 = my 45-degree isometric render of this Gothic mausoleum (the LONG version). KEEP its EXACT camera: true 45° isometric projection (45° azimuth, ~30° downward tilt), parallel projection, NO perspective, NO vanishing point. KEEP all materials, colors, slate roof, finials, front facade, portal and steps EXACTLY as in Ref 1.

Make ONE change only — the side flank is too long, SHORTEN it: reduce the repeating gabled window bays from five down to THREE, so depth (front-to-back) is only slightly larger than front width — a compact chapel, NOT a long nave. Close up the roof to match.

Do NOT rotate the building, do NOT switch to a front/elevation view, do NOT change the isometric angle, materials or any other detail. One complete, isolated building, fully visible, flat neutral grey (#808080) seamless background, even diffuse de-lit lighting, NO cast shadows, NO rim light, NO glow on the glass. High-resolution single-image reference for image-to-3D.
```

---

## 修正歷程 + 踩坑(實證)

1. **屋頂 + 顏色**:照鐵律「**幾何先於表面**」— 先改屋頂造型,再拉開材質顏色;原概念圖當真相、Front v1 當底做 image-edit。一次到位。

2. **🔴 等角側面失控變長**
   - 症狀:側面排了 5–6 個 bay → 整棟變長中殿。
   - 根因:prompt 寫 `repeating gabled window bays` 但**沒給數量** → 模型無限複製。
   - 修法:**指定 bay 數**(`THREE`)+ **鎖縱深比例**(`depth ≈ front width`)。

3. **🔴 等角退回正面視角(新發現,值得進主 skill)**
   - 症狀:修長度時,結果整個丟掉等角、變回近正面圖。
   - 根因:**把 head-on 的 Front 正視圖當 Ref 餵進去 + 一堆 `front facade` 字眼** → 「正面」訊號壓過「等角」訊號。
   - 修法:**等角/3-4 步驟只 anchor 在那張對的等角上,別餵正視圖**;相機鎖三次(`KEEP EXACT camera` + `do NOT rotate` + `do NOT switch to front view`),且**只改要改的那一點**。
   - 🧭 一般化規則:**要某個非正面視角時,參考圖就用「那個視角的圖」,不要混餵正視圖** — 不同相機的參考圖一起送,最強的相機訊號會贏。

---

## 接 3D

- **單圖路**:緊湊等角 → Tripo 3.0 / Meshy 5 / Hunyuan3D 2.5 單圖轉 3D(最快、變形少)。
- **多視圖路**:front + rear(+ side)→ Tripo / Hunyuan multiview(背面更準)。
- 大件建築 multiview 通常 > 單圖等角;進引擎前 retopo + 烘法線(AI 高模是亂三角網)。

## 檔案落點(建議)
```
/module/gothic-mausoleum/
  plate_front.png      # Front v2(確認)
  plate_rear.png       # Rear 立面
  iso_45.png           # 45° 等角(緊湊)
  side.png             # (選)側面立面
  model.glb            # 轉出的中模
```
