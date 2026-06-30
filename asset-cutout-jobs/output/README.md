# 去背成果 — 只留下立體植物(寬葉)

來源:`asset-cutout-jobs/input/asset-cutout-jobsinputsource.png`(2048×2048 苔蘚地面)

## 做法(asset-cutout 模式 1.0 純 matting,零重畫)
- 通用去背(rembg u2net/isnet)與顏色去背都失敗:目標植物與苔蘚**同色同紋理**,無法自動分離。
- 改用 **SAM(Segment Anything)+ 方框提示**,逐株框選明顯的寬葉植物(蓮座/酢漿草叢),
  以原圖像素切出,其餘(苔蘚毯、細草、泥土)全部去除。
- 背景填純橘 `#FF6A00`(綠色資產的缺席色,利於後續色鍵)。

## 檔案
- `plants-cutout-transparent.png` — 透明背景母檔(RGBA,建議保留此檔)
- `plants-cutout-orange.png` — 橘底 `#FF6A00` 版(預覽 / 色鍵用)
- `preview-orange-768.png` — 縮圖

> 像素 100% 來自原圖,未經任何重繪或風格化。若要增/減特定植物,可再指定。
