#!/usr/bin/env python3
"""
Derive a full PBR map set from a single de-lit albedo plate.

用途:把「已去光的 albedo 板」程序化派生成整套 PBR 貼圖,跟 base 100% 對齊
(對應 A10/A11 SOP「normal/height/AO 從真實高低落差算」的正路)。

產出(全部寫到 --outdir,前綴 --prefix):
  <p>-basecolor.png   洗淨 albedo(攤平巨觀光照 + 抬黑位)      sRGB
  <p>-height.png      灰階高度(micro bump,細節起伏)          Non-Color 16-bit
  <p>-normal.png      切線空間法線(OpenGL Y+,從 height Sobel)  Non-Color
  <p>-roughness.png   粗糙度(石材高糙、暗處金屬略降)            Non-Color
  <p>-metallic.png    金屬遮罩(預設近純黑;可用 --metal-mask 疊) Non-Color
  <p>-ao.png          環境遮蔽(從 height cavity)                Non-Color
  <p>-orm.png         打包 R=AO / G=Rough / B=Metal              Non-Color
  <p>-preview.png     base×AO 快速預覽(僅檢查用)

⚠️ 限制:單圖派生的是「表面 micro 起伏」(石紋/縫/雕花細節),
不是「巨觀深度」(石像鬼往前凸、壁龕往後凹)。要石像鬼真的擋光,
巨觀 height 請改用單目深度模型(Depth-Anything/MiDaS)或生成式 height,
再與本腳本的 micro height 疊合(--macro-depth 疊入)。
"""
import argparse, sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, uniform_filter


def srgb_to_linear(x):
    a = 0.055
    return np.where(x <= 0.04045, x / 12.92, ((x + a) / (1 + a)) ** 2.4)


def linear_to_srgb(x):
    a = 0.055
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, (1 + a) * (x ** (1 / 2.4)) - a)


def load_rgb(path):
    im = Image.open(path).convert("RGB")
    return np.asarray(im).astype(np.float32) / 255.0


def save_gray(arr, path, bit16=False):
    arr = np.clip(arr, 0, 1)
    if bit16:
        Image.fromarray((arr * 65535).astype(np.uint16), mode="I;16").save(path)
    else:
        Image.fromarray((arr * 255).astype(np.uint8), mode="L").save(path)


def save_rgb(arr, path):
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), mode="RGB").save(path)


def luminance(rgb):
    return rgb @ np.array([0.2126, 0.7152, 0.0722], np.float32)


def clean_albedo(rgb, flatten=0.55, black_lift=48 / 255):
    """homomorphic 攤平巨觀明暗 + 抬黑位,避免進 Blender 疊乘變死黑(A10 踩坑修法)。"""
    lin = srgb_to_linear(rgb)
    lum = luminance(lin) + 1e-4
    sigma = max(rgb.shape[:2]) * 0.12
    illum = gaussian_filter(lum, sigma)              # 低頻當「殘留光照」估計
    illum /= illum.mean()
    corr = lum / (illum ** flatten)                  # 反除,攤平巨觀
    scale = (corr / lum)[..., None]
    out = lin * scale
    out = linear_to_srgb(out)
    out = black_lift + (1 - black_lift) * out         # 抬黑位,不留純黑
    return np.clip(out, 0, 1)


def make_height(rgb, detail=1.0, macro=None):
    """單圖 micro height:去色後取局部細節;可疊入外部巨觀深度圖(0=遠,1=近)。"""
    lum = luminance(srgb_to_linear(rgb))
    base = gaussian_filter(lum, max(rgb.shape[:2]) * 0.02)   # 中頻大形
    hi = lum - gaussian_filter(lum, 2.0)                     # 高頻細節(縫/雕花)
    h = base + detail * hi
    h = (h - h.min()) / (h.ptp() + 1e-6)
    if macro is not None:
        h = 0.7 * macro + 0.3 * h                            # 巨觀主導,micro 疊細節
        h = (h - h.min()) / (h.ptp() + 1e-6)
    return h


def height_to_normal(h, strength=2.0):
    """Sobel 求梯度 → 切線空間法線(OpenGL:綠 = +Y 上)。"""
    gy, gx = np.gradient(h)
    nx = -gx * strength
    ny = -gy * strength
    nz = np.ones_like(h)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    n = np.stack([nx / ln, ny / ln, nz / ln], -1)
    return n * 0.5 + 0.5


def height_to_ao(h, radius_frac=0.03, strength=1.0):
    """cavity AO:高度低於鄰域平均 → 遮蔽。"""
    r = int(max(h.shape) * radius_frac)
    local = uniform_filter(h, size=max(3, r))
    ao = 1.0 - strength * np.clip(local - h, 0, None) * 4.0
    return np.clip(gaussian_filter(ao, 1.0), 0, 1)


def make_roughness(rgb, lo=0.55, hi=0.9, metal_mask=None, metal_rough=0.4):
    """亮=高糙(風化石)、暗=略低(磨光/潮);金屬遮罩區壓到 metal_rough。"""
    lum = luminance(srgb_to_linear(rgb))
    r = lo + (hi - lo) * np.clip(lum, 0, 1)
    if metal_mask is not None:
        r = np.where(metal_mask > 0.5, metal_rough, r)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("albedo")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--prefix", default="gothic-alcove")
    ap.add_argument("--macro-depth", default=None,
                    help="選配:外部巨觀深度圖(灰階,白=近),讓石像鬼/壁龕吃光")
    ap.add_argument("--metal-mask", default=None,
                    help="選配:金屬遮罩(白=金屬,如鐵壁燈),餵 metallic/roughness")
    ap.add_argument("--normal-strength", type=float, default=2.0)
    args = ap.parse_args()

    import os
    os.makedirs(args.outdir, exist_ok=True)
    p = lambda s: os.path.join(args.outdir, f"{args.prefix}-{s}.png")

    rgb = load_rgb(args.albedo)
    macro = None
    if args.macro_depth:
        macro = luminance(load_rgb(args.macro_depth))
        macro = (macro - macro.min()) / (macro.ptp() + 1e-6)
    metal = None
    if args.metal_mask:
        metal = luminance(load_rgb(args.metal_mask))

    base = clean_albedo(rgb)
    h = make_height(rgb, macro=macro)
    normal = height_to_normal(h, args.normal_strength)
    ao = height_to_ao(h)
    rough = make_roughness(rgb, metal_mask=metal)
    metallic = metal if metal is not None else np.zeros(rgb.shape[:2], np.float32)

    save_rgb(base, p("basecolor"))
    save_gray(h, p("height"), bit16=True)
    save_rgb(normal, p("normal"))
    save_gray(rough, p("roughness"))
    save_gray(metallic, p("metallic"))
    save_gray(ao, p("ao"))
    save_rgb(np.stack([ao, rough, metallic], -1), p("orm"))
    save_rgb(base * ao[..., None], p("preview"))

    print("wrote:")
    for s in ["basecolor", "height", "normal", "roughness", "metallic", "ao", "orm", "preview"]:
        print("  ", p(s))
    print(f"size = {rgb.shape[1]}x{rgb.shape[0]}")


if __name__ == "__main__":
    sys.exit(main())
