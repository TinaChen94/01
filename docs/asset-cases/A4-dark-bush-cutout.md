# 實戰紀錄 — A4 明亮森林植被叢去背(概念圖拆件)

> 概念圖拆資產 / 去背案例。對應工作流:`/asset-cutout`。
> 從明亮 mid-key JRPG 森林背景(B11 同風格)把紅圈標記的植被叢**去背 + 補遮擋 + 純色底**,保留原筆觸。
> **以下兩版皆實測成功、產出可直接當素材。** 平台:Gemini(Nano Banana 2 edit);工作底色 `#FF00FF` 洋紅(本資產深綠=缺席色)。

---

## ✅ 成功版 1 — 「dark shrub」保真去背(合併成一條)

抽出深色叢灌木、保留原筆觸,**未變假圓球**。整張圖丟進去 → 三圈深叢合併成一條,適合當**背景植被牆**。

```text
Keep the dark leafy shrub exactly as it is painted in this image — same shape,
same leaves, same dark teal-green colors and brushstrokes. Do NOT repaint it,
do NOT turn it into a smooth round bush. Remove everything else — the bright
ferns, tree trunks, ivy, grass, mushrooms, background forest — and put the
shrub on a solid magenta #FF00FF background. Only where the shrub is hidden
behind a trunk or fern, fill that gap with matching dark leaves so it stays in
one piece. Keep its natural silhouette.
```

**關鍵:** 拿掉 `reconstruct / complete rounded silhouette`,改 `Do NOT turn it into a smooth round bush` + `Keep its natural silhouette` → 模型不重繪,只保留原叢 + 補被擋處。

---

## ✅ 成功版 2 — 「3 red circles」指名分件(三叢乾淨分開)

指名紅圈數量,一次跑出**三叢分開**的成品,原筆觸完整、乾淨俐落。適合當**獨立 set-dressing 資產**(每圈整叢:蕨 + 寬葉 + 深叢)。

```text
This image has 3 red circles. Extract only the plants inside the red circles.
Remove everything else and put them on a solid magenta #FF00FF background.
Keep the plants exactly as painted — do not repaint or restyle them. Where a
plant is hidden behind a tree trunk, fill in that part so it looks complete.
Ignore the red circle lines themselves.
```

**關鍵:** 指名 `N red circles` 讓模型自己分件 → 三圈自動分三叢;**單數主詞 `the shrub` 會合併成一條**(=成功版 1 的行為)。

---

## 收尾

- 右下 Gemini **✨ 浮水印** → 手動擦(套索填 `#FF00FF`,10 秒)。
- 要**獨立資產** → 成品畫布切成 N 張 PNG;要**背景牆** → 直接用。
- 洋紅底 → 色鍵去背(開 spill suppression、關 Decontaminate Colors)→ 透明 PNG 母檔 + `#808080` 灰底版。

> 備註:若要「**精準只留深叢、排除同色的蕨/藤/地被**」,AI edit 做不到(同色無邊分不出),需回 Photopea 手動套索選取。上面兩版抽的是**整叢**。
