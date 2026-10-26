"""按色相/飽和度/亮度門檻自動抓顏色遮罩,並只在遮罩內加強。

用法(A12 定案參數 = 預設值):
    python3 color_mask.py door.webp --out-dir out/
    python3 color_mask.py door.webp --sat-min 0.35 --hue-min 330   # A12 第一張門用的寬門檻

輸出:<name>_mask.png(白=選取)、<name>_boost.png(保留原 alpha)、<name>_compare.png(原圖|遮罩|加強)
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def color_mask(rgb, hue_min, hue_max, sat_min, val_min):
    a = rgb.astype(float) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = np.maximum(mx - mn, 1e-6)
    s = (mx - mn) / np.maximum(mx, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6,
                 np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    # hue_min <= hue_max:一般區間;hue_min > hue_max:跨 0°(紅色,如 335~20)
    hue_ok = ((h >= hue_min) & (h <= hue_max)) if hue_min <= hue_max else ((h >= hue_min) | (h <= hue_max))
    return hue_ok & (s > sat_min) & (mx > val_min)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--out-dir", default=".")
    p.add_argument("--hue-min", type=float, default=335, help="色相下限(度);大於 hue-max 時跨 0°")
    p.add_argument("--hue-max", type=float, default=20, help="色相上限(度)")
    p.add_argument("--sat-min", type=float, default=0.45)
    p.add_argument("--val-min", type=float, default=0.10)
    p.add_argument("--median", type=int, default=5, help="去雜點濾波尺寸(奇數)")
    p.add_argument("--feather", type=float, default=1.5, help="邊緣羽化 px")
    p.add_argument("--sat-gain", type=float, default=1.3)
    p.add_argument("--val-gain", type=float, default=1.35)
    args = p.parse_args()

    src = Image.open(args.image)
    alpha = src.getchannel("A") if src.mode in ("RGBA", "LA") else None
    im = src.convert("RGB")
    rgb = np.asarray(im)

    sel = color_mask(rgb, args.hue_min, args.hue_max, args.sat_min, args.val_min)
    if alpha is not None:
        sel &= np.asarray(alpha) > 0
    mask = (Image.fromarray((sel * 255).astype("uint8"))
            .filter(ImageFilter.MedianFilter(args.median))
            .filter(ImageFilter.GaussianBlur(args.feather)))
    print(f"selected: {sel.mean():.1%} of pixels")

    hsv = np.asarray(im.convert("HSV")).astype(float)
    hsv[..., 1] = np.clip(hsv[..., 1] * args.sat_gain, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * args.val_gain, 0, 255)
    boost = np.asarray(Image.fromarray(hsv.astype("uint8"), "HSV").convert("RGB")).astype(float)
    m = np.asarray(mask).astype(float)[..., None] / 255
    out = Image.fromarray((rgb * (1 - m) + boost * m).astype("uint8"))

    stem = Path(args.image).stem
    od = Path(args.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    mask.save(od / f"{stem}_mask.png")
    w, h = im.size
    cmp = Image.new("RGB", (w * 3, h))
    for i, x in enumerate((im, mask.convert("RGB"), out)):
        cmp.paste(x, (w * i, 0))
    cmp.save(od / f"{stem}_compare.png")
    if alpha is not None:
        out = out.convert("RGBA")
        out.putalpha(alpha)
    out.save(od / f"{stem}_boost.png")


if __name__ == "__main__":
    main()
