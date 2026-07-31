# A4 明亮森林植被叢去背(概念圖拆件)

思路:**2D 保真去背**(不可重繪、洋紅 `#FF00FF` 底、直接當畫面素材)
觸發:拆概念圖植物 / 植被叢去背 / dark shrub / 森林植物拆件 / 圈選植物去背 / 3 red circles 分件 / 保原筆觸不重繪
引用 SKILL:`asset-cutout`(模式 1.1 保真去背)
平台:Gemini NB2 edit · 底色 `#FF00FF`(深綠缺席色)· 風格同 B11
狀態:✅ 兩版實測成功、產出可用

## 思路分流 — A4 ≠ A1(先認清要哪條)

| | **A1 陵墓** | **A4 植被叢(本卡)** |
|---|---|---|
| 目的 | concept **→ 3D** | **2D 素材直接用** |
| 模式 | **重新生成** re-render 乾淨正視板 | **保真去背** 留原筆觸 |
| 在意原像素? | ❌ 可重繪 | ✅ 不能重繪 |
| 產出 | 正交參考板餵 image-to-3D | 去背 PNG(背景牆 / set-dressing) |

- **「三視圖重建 / turnaround / model sheet」= A1 那條(→3D 重繪)**,不是本卡。
- 本卡是 2D 保真去背,直接貼畫面用,**必須留原畫、不能重繪**。

## 版1 — 保真去背(整圖跑 → 深叢合併成背景牆)

```text
Keep the dark leafy shrub exactly as it is painted in this image — same shape,
same leaves, same dark teal-green colors and brushstrokes. Do NOT repaint it,
do NOT turn it into a smooth round bush. Remove everything else — the bright
ferns, tree trunks, ivy, grass, mushrooms, background forest — and put the
shrub on a solid magenta #FF00FF background. Only where the shrub is hidden
behind a trunk or fern, fill that gap with matching dark leaves so it stays in
one piece. Keep its natural silhouette.
```
鎖:`Do NOT turn it into a smooth round bush` + `Keep its natural silhouette`;**拿掉** `reconstruct/complete silhouette`(這句會重繪成假圓球)。

## 版2 — 3 red circles 指名分件(一次跑出三叢分開)

```text
This image has 3 red circles. Extract only the plants inside the red circles.
Remove everything else and put them on a solid magenta #FF00FF background.
Keep the plants exactly as painted — do not repaint or restyle them. Where a
plant is hidden behind a tree trunk, fill in that part so it looks complete.
Ignore the red circle lines themselves.
```
鎖:指名 `N red circles` → 自動分件;單數 `the shrub` 會合併(=版1 行為)。抽的是圈內整叢(蕨+寬葉+深叢)。

## 收尾 / 限制
- ✨ 浮水印手動擦(套索填 `#FF00FF`);要獨立資產切 N 張 PNG;色鍵開 spill、關 Decontaminate。
- ⛔ 精準只留深叢、排同色蕨/藤 = AI 做不到(同色無邊)→ Photopea 手動套索。
- ⚠️ **洋紅底 key 出紫暈 = defringe 沒做,不是洋紅的錯**。別換底色救(換暗綠 → 暗叢融進底、認不出;死路)。
  正解:Photopea 開洋紅圖 → `色彩範圍`點洋紅 → `擴張 1px` → Delete → `圖層→修邊 Defringe 1–2px` → 透明 PNG。
  或 remove.bg 上傳(平色底自動去+修邊)。**要透明就走語意去背/defringe,底色換來換去都不對。**
