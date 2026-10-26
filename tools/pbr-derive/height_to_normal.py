#!/usr/bin/env python3
"""
從 HEIGHT / DISPLACEMENT 灰階圖派生切線空間 NORMAL map(比生成式準,梯度真實)。

同時輸出 OpenGL(Y+,Blender/Unity 直接用)與 DirectX(Y-,UE 用)兩版。

用法:
  python3 height_to_normal.py height.png --outdir <dir> --prefix gothic-alcove \
      [--strength 2.5] [--blur 0.6]
"""
import argparse, os, sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter


def load_gray(path):
    im = Image.open(path).convert("L")
    return np.asarray(im).astype(np.float32) / 255.0


def height_to_normal(h, strength=2.5, y_up=True):
    gy, gx = np.gradient(h)
    nx = -gx * strength
    ny = -gy * strength * (1.0 if y_up else -1.0)   # OpenGL Y+ / DirectX Y-
    nz = np.ones_like(h)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    n = np.stack([nx / ln, ny / ln, nz / ln], -1)
    return (n * 0.5 + 0.5)


def save_rgb(arr, path):
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGB").save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("height")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--prefix", default="gothic-alcove")
    ap.add_argument("--strength", type=float, default=2.5,
                    help="法線強度;凹凸太平調高、太誇張調低(建議 1.5–3.5)")
    ap.add_argument("--blur", type=float, default=0.6,
                    help="height 先輕微高斯模糊去階梯雜訊(0=不模糊)")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    h = load_gray(args.height)
    if args.blur > 0:
        h = gaussian_filter(h, args.blur)

    gl = height_to_normal(h, args.strength, y_up=True)
    dx = height_to_normal(h, args.strength, y_up=False)

    p_gl = os.path.join(args.outdir, f"{args.prefix}-normal.png")        # OpenGL 預設
    p_dx = os.path.join(args.outdir, f"{args.prefix}-normal-dx.png")     # DirectX(UE)
    save_rgb(gl, p_gl)
    save_rgb(dx, p_dx)

    # QC:健康的切線 normal 平均應接近 (128,128,255)
    m = (gl.reshape(-1, 3).mean(0) * 255).round().astype(int)
    print(f"wrote {p_gl}  (OpenGL Y+, Blender/Unity)")
    print(f"wrote {p_dx}  (DirectX Y-, UE — 綠通道已反轉)")
    print(f"size = {h.shape[1]}x{h.shape[0]}")
    print(f"QC mean RGB = {tuple(m)}  (健康值≈(128,128,255),偏藍表面朝前)")


if __name__ == "__main__":
    sys.exit(main())
